#!/usr/bin/env python3
"""
Refactoring Triage Analyzer — AI-Assisted Refactoring Prioritization

Scans .NET C# source files to identify refactoring targets based on:
  - Complexity metrics (cyclomatic, nesting, method length)
  - Code smells (sync-over-async, exception swallowing, precision-unsafe math, etc.)
  - Coupling danger (fan-in/fan-out from existing analysis)
  - Test coverage gaps

Usage:
  python 2_scan_smells.py /path/to/repos [output-dir]

Outputs:
  - refactoring-targets.json (machine-readable analysis)
  - refactoring-report.md (human-readable report)
"""

import argparse
import json
import os
import platform
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# Import detector registry
from detectors import get_detectors, SEVERITY_ORDER, SEVERITY_WEIGHTS

# ─── Config ───────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Refactoring Triage Analyzer")
parser.add_argument("scan_root", help="Directory containing repos to scan")
parser.add_argument("out_dir", nargs="?", default="output", help="Output directory")
parser.add_argument("--level", choices=["critical", "high", "medium", "low"], default="high",
                    help="Minimum severity level to report (default: high)")
_args = parser.parse_args()

SCAN_ROOT = os.path.abspath(_args.scan_root)
OUT_DIR = os.path.abspath(_args.out_dir)
SCAN_LEVEL = _args.level

_IS_WINDOWS = platform.system() == "Windows"
_MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB — skip files larger than this
_MAX_SCAN_DEPTH = 30  # max directory nesting depth
_MIN_INTERESTING_LINES = 50  # skip files with fewer lines
_PROGRESS_INTERVAL = 500  # print progress every N files

# Exclusion patterns
EXCLUDE_PATTERNS = [
    r"\\.(Designer|generated|AssemblyInfo)\.cs$",
    r"[\\/](obj|bin|node_modules|packages)[\\/]",
    r"[\\/]Migrations[\\/]",
]

# Projects to deprioritize (still scan, but reduce score)
DEPRIORITIZE_CATEGORIES = {"test", "sample", "localization", "tool"}

# Namespace patterns to deprioritize (logging, UI infrastructure)
DEPRIORITIZE_NAMESPACES = [
    r"\.Logging\.",
    r"\.Logger",
    r"\.UI\.Controls\.",
    r"\.UI\.Infrastructure\.",
    r"\.Xaml\.",
    r"\.Resources\.",
]

# Financial pricer detection patterns
FINANCIAL_PATTERNS = [
    r"Pricer",
    r"Pricing",
    r"Financial",
    r"Calc",
    r"Engine",
    r"Valuation",
    r"Greeks",
    r"BlackScholes",
    r"MonteCarlo",
]


# ─── Path Utilities (from 1_scan_projects.py) ────────────────────────

def _strip_long_prefix(p: str) -> str:
    """Strip the Windows ``\\\\?\\`` extended-length prefix."""
    if p.startswith("\\\\?\\UNC\\"):
        return "\\\\" + p[8:]  # \\?\UNC\server\share → \\server\share
    if p.startswith("\\\\?\\"):
        return p[4:]           # \\?\C:\foo → C:\foo
    return p


def _fs_path(p: str) -> str:
    """Return a path suitable for filesystem I/O (scandir, stat, read).

    On Windows, adds the ``\\\\?\\`` extended-length prefix for paths
    that exceed the legacy 260-char MAX_PATH limit.
    """
    if sys.platform == "win32":
        abs_p = os.path.abspath(p)
        if len(abs_p) >= 260 and not abs_p.startswith("\\\\?\\"):
            if abs_p.startswith("\\\\"):
                return "\\\\?\\UNC\\" + abs_p[2:]
            return "\\\\?\\" + abs_p
    return os.path.normpath(p) if p else p


def _normalize_path(p: str) -> str:
    """Return a clean, absolute, normalised path (no ``\\\\?\\`` prefix)."""
    if not p:
        return p
    cleaned = _strip_long_prefix(p)
    if os.path.isabs(cleaned):
        return os.path.normpath(cleaned)
    return os.path.normpath(os.path.abspath(cleaned))


def _relpath(path: str, start: str) -> str:
    """Compute os.path.relpath after stripping any ``\\\\?\\`` prefixes."""
    clean_path = _strip_long_prefix(os.path.normpath(path))
    clean_start = _strip_long_prefix(os.path.normpath(start))
    try:
        return os.path.relpath(clean_path, clean_start)
    except ValueError:
        return clean_path


def safe_read_text(filepath: str, max_size: int = _MAX_FILE_SIZE) -> str | None:
    """Read a text file, returning None if too large or unreadable."""
    norm_path = _fs_path(filepath)
    try:
        sz = Path(norm_path).stat().st_size
        if sz > max_size:
            return None
    except OSError:
        return None
    try:
        return Path(norm_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


# ─── Find all source files recursively ──────────────────────────────

SKIP_DIRS = {".git", "node_modules", "bin", "obj", ".vs", ".idea", "packages",
              "TestResults", "artifacts", "__pycache__", ".nuget", "target", "build", ".gradle"}


def find_source_files(
    directory: str,
    results: list | None = None,
    _depth: int = 0,
) -> list[str]:
    """Recursively find all .cs and .java files, respecting exclusion patterns."""
    if results is None:
        results = []
    if _depth > _MAX_SCAN_DEPTH:
        return results

    fs_dir = _fs_path(directory)
    if not os.path.exists(fs_dir):
        return results

    try:
        with os.scandir(fs_dir) as it:
            entries = list(it)
    except OSError:
        return results

    for entry in entries:
        full = _normalize_path(entry.path)
        try:
            is_dir = entry.is_dir(follow_symlinks=False)
        except OSError:
            continue

        if is_dir:
            if entry.name in SKIP_DIRS:
                continue
            find_source_files(full, results, _depth + 1)
        elif entry.name.endswith((".cs", ".java")):
            # Check exclusion patterns
            if not any(re.search(pattern, full) for pattern in EXCLUDE_PATTERNS):
                results.append(full)

    return results


# ─── Complexity Metrics ───────────────────────────────────────────────

def compute_cyclomatic_complexity(content: str) -> int:
    """Count decision points as a proxy for cyclomatic complexity."""
    # Count: if, else, switch, case, while, for, foreach, catch, ternary (?:), &&, ||
    count = 0
    count += len(re.findall(r'\bif\s*\(', content))
    count += len(re.findall(r'\belse\b', content))
    count += len(re.findall(r'\bswitch\s*\(', content))
    count += len(re.findall(r'\bcase\s+', content))
    count += len(re.findall(r'\bwhile\s*\(', content))
    count += len(re.findall(r'\bfor\s*\(', content))
    count += len(re.findall(r'\bforeach\s*\(', content))
    count += len(re.findall(r'\bcatch\s*\(', content))
    # Ternary operator - match ? followed by : but avoid nullable types
    # Look for ? not followed by > or . to avoid matching nullable types and member access
    count += len(re.findall(r'\?[^>.\s][^:]*:', content))
    count += len(re.findall(r'&&', content))
    count += len(re.findall(r'\|\|', content))
    return count


def compute_max_nesting_depth(content: str) -> int:
    """Calculate maximum brace nesting depth."""
    max_depth = 0
    current_depth = 0
    in_string = False
    in_char = False
    escape_next = False
    
    for i, char in enumerate(content):
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\':
            escape_next = True
            continue
        
        # Handle strings
        if char == '"' and not in_char:
            in_string = not in_string
            continue
        
        # Handle char literals
        if char == "'" and not in_string:
            in_char = not in_char
            continue
        
        # Skip if inside string or char
        if in_string or in_char:
            continue
        
        # Count braces
        if char == '{':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == '}':
            current_depth = max(0, current_depth - 1)
    
    return max_depth


def count_methods(content: str) -> int:
    """Count method signatures (public|private|protected|internal ... ()."""
    # Match method signatures
    pattern = r'\b(public|private|protected|internal|static|virtual|override|abstract|async)\s+(?:\w+\s+)+\w+\s*\('
    return len(re.findall(pattern, content))


def detect_long_methods(content: str) -> list[dict]:
    """Detect methods exceeding 50 lines (approximate)."""
    long_methods = []
    lines = content.split('\n')
    
    # Find method signatures
    method_pattern = r'\b(public|private|protected|internal|static|virtual|override|abstract|async)\s+(?:\w+\s+)+(\w+)\s*\('
    
    for i, line in enumerate(lines):
        match = re.search(method_pattern, line)
        if match:
            method_name = match.group(2)
            start_line = i + 1
            
            # Find the end of the method (approximate by counting braces)
            brace_depth = 0
            found_opening = False
            end_line = start_line
            
            for j in range(i, len(lines)):
                if '{' in lines[j]:
                    found_opening = True
                    brace_depth += lines[j].count('{')
                brace_depth -= lines[j].count('}')
                
                if found_opening and brace_depth == 0:
                    end_line = j + 1
                    break
            
            method_length = end_line - start_line
            if method_length > 50:
                long_methods.append({
                    "name": method_name,
                    "line": start_line,
                    "length": method_length,
                })
            
            # Check for god methods (>100 lines)
            if method_length > 100:
                long_methods[-1]["is_god_method"] = True
    
    return long_methods


# ─── Per-Smell LLM Prompt Templates ──────────────────────────────────

# ─── Per-Smell LLM Prompt Templates ──────────────────────────────────
# Each prompt is laser-focused: it instructs the LLM to ONLY evaluate and fix
# the specific finding, not review the whole file for unrelated issues.
# Placeholders: {file}, {line}, {context}, {project}

SMELL_PROMPTS = {
    "hardcoded_secret": (
        "SECURITY FINDING: Hardcoded secret detected.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this hardcoded secret. Do NOT review the rest of the file for other issues.\n"
        "1. Confirm whether the value is a real secret (password, API key, connection string) or a false positive.\n"
        "   Common false positives: key-name constants used for parsing (e.g. const string PASSWORD = \"password\"),\n"
        "   connection string builders/parsers, secret removal/masking/redaction methods, logging placeholders.\n"
        "2. If it is a real secret, propose a fix: move to environment variable, Azure Key Vault, user-secrets, or IConfiguration injection.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "sql_injection": (
        "SECURITY FINDING: Potential SQL injection via string concatenation/interpolation.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this SQL injection risk. Do NOT review the rest of the file for other issues.\n"
        "1. Confirm whether user-controlled input reaches this SQL string.\n"
        "2. If vulnerable, rewrite using parameterized queries (@param, SqlParameter, or EF Core interpolated SQL).\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "insecure_deserialization": (
        "SECURITY FINDING: Insecure deserialization detected.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this deserialization issue. Do NOT review the rest of the file for other issues.\n"
        "1. Identify the dangerous type (BinaryFormatter, SoapFormatter, TypeNameHandling.All, etc.).\n"
        "2. Propose a safe replacement: System.Text.Json, JsonSerializer with safe settings, or a custom binder.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "command_injection": (
        "SECURITY FINDING: Potential command injection via Process.Start with string concatenation.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this command injection risk. Do NOT review the rest of the file for other issues.\n"
        "1. Check whether user-controlled input flows into the process arguments.\n"
        "2. If vulnerable, propose using an argument array (no shell), input validation, or allowlisting.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "weak_crypto": (
        "SECURITY FINDING: Weak cryptographic algorithm in use.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this weak crypto usage. Do NOT review the rest of the file for other issues.\n"
        "1. Identify the algorithm (MD5, SHA1, DES, TripleDES, RC2).\n"
        "2. Determine whether it is used for security (signatures, passwords, tokens, certificates)\n"
        "   or non-security purposes (checksums, cache keys, ETags, content fingerprints, deduplication).\n"
        "   MD5/SHA1 for non-security hashing is generally acceptable and not a vulnerability.\n"
        "3. If security-relevant, replace with SHA-256/SHA-512 (hashing), AES-256 (encryption), or PBKDF2/Argon2 (passwords).\n"
        "4. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "open_redirect": (
        "SECURITY FINDING: Potential open redirect.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this redirect. Do NOT review the rest of the file for other issues.\n"
        "1. Confirm whether user input (returnUrl, redirectUrl, Request params) reaches the Redirect() call.\n"
        "2. If vulnerable, replace with LocalRedirect(), add Url.IsLocalUrl() validation, or use an allowlist.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "xss": (
        "SECURITY FINDING: Potential cross-site scripting (XSS).\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this XSS risk. Do NOT review the rest of the file for other issues.\n"
        "1. Determine the vector: Html.Raw with user input, Response.Write, or missing [ValidateAntiForgeryToken].\n"
        "2. For Html.Raw: encode via HtmlEncoder or use Razor's default encoding.\n"
        "3. For missing anti-forgery: add [ValidateAntiForgeryToken] to the POST action.\n"
        "4. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "insecure_random": (
        "SECURITY FINDING: System.Random used in a security-sensitive context.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this random number usage. Do NOT review the rest of the file for other issues.\n"
        "1. Confirm whether the value is used for tokens, passwords, nonces, or other security purposes.\n"
        "2. If so, replace System.Random with RandomNumberGenerator (System.Security.Cryptography).\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "exception_swallowing": (
        "BUG: Empty catch block swallows exception silently.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this empty catch block. Do NOT review the rest of the file for other issues.\n"
        "1. Determine what the catch block should do: log, rethrow, wrap, or handle the exception.\n"
        "2. Based on the surrounding context, propose the appropriate handler (ILogger, rethrow with throw;, etc.).\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "sync_over_async": (
        "BUG: Sync-over-async anti-pattern detected.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this sync-over-async call. Do NOT review the rest of the file for other issues.\n"
        "1. Identify the pattern: .Result, .Wait(), or .GetAwaiter().GetResult().\n"
        "2. Determine if the calling method can be made async (add async/await up the call chain).\n"
        "3. If it cannot be async (e.g., constructor, event handler), explain the threading risk and propose a safe alternative.\n"
        "4. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "god_method": (
        "CODE QUALITY: Method exceeds 100 lines.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this oversized method. Do NOT review the rest of the file for other issues.\n"
        "1. Identify logical blocks within the method that can be extracted into smaller methods.\n"
        "2. Propose an extract-method refactoring that preserves behavior.\n"
        "3. Show the method decomposition plan -- do not refactor other methods in the file."
    ),
    "deep_nesting": (
        "CODE QUALITY: Excessive nesting depth (>4 levels).\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this deeply nested code. Do NOT review the rest of the file for other issues.\n"
        "1. Identify guard clauses, early returns, or method extraction to reduce nesting.\n"
        "2. Propose a restructured version using inversion of control flow.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "long_parameter_list": (
        "CODE QUALITY: Method has more than 5 parameters.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this parameter list. Do NOT review the rest of the file for other issues.\n"
        "1. Group related parameters into a parameter object, record, or Options class.\n"
        "2. Consider whether Builder pattern or method overloads would be more appropriate.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "precision_unsafe_math": (
        "CODE QUALITY: float/double used where decimal precision may be required.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this precision issue. Do NOT review the rest of the file for other issues.\n"
        "1. Confirm whether this variable participates in financial calculations (price, amount, rate, margin).\n"
        "2. If so, change the type from float/double to decimal.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "deep_inheritance": (
        "CODE QUALITY: Class implements many interfaces or has complex inheritance.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this inheritance hierarchy. Do NOT review the rest of the file for other issues.\n"
        "1. Determine if the interfaces indicate too many responsibilities (violating Interface Segregation).\n"
        "2. Consider composition over inheritance or splitting the class.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "python_call": (
        "CROSS-TECHNOLOGY: C# code invokes Python.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this Python interop call. Do NOT review the rest of the file for other issues.\n"
        "1. Document the purpose of the Python call (calculation engine, data processing, ML model, etc.).\n"
        "2. Assess error handling: what happens if the Python process fails, times out, or returns unexpected output?\n"
        "3. Check for input sanitization if C# data is passed to the Python script.\n"
        "4. Evaluate whether this is the right integration approach or if a gRPC/REST/message-queue boundary would be safer.\n"
        "5. Show any minimal improvements needed -- do not refactor surrounding code."
    ),
    "magic_number": (
        "STYLE: Hardcoded numeric literal in logic.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this magic number. Do NOT review the rest of the file for other issues.\n"
        "1. Determine the meaning of the number from context.\n"
        "2. Extract it to a named constant with a descriptive name.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "missing_null_check": (
        "STYLE: Public method parameter lacks null check.\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this null-check gap. Do NOT review the rest of the file for other issues.\n"
        "1. Determine if the parameter is nullable and needs validation.\n"
        "2. Add ArgumentNullException.ThrowIfNull() or a null-check guard clause.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "mutable_shared_state": (
        "STYLE: Static mutable field (potential thread-safety issue).\n"
        "File: {file} (line {line})\n"
        "Context: {context}\n\n"
        "TASK: Evaluate ONLY this static mutable field. Do NOT review the rest of the file for other issues.\n"
        "1. Determine if the field is accessed from multiple threads.\n"
        "2. If so, make it readonly, use ConcurrentDictionary, Lazy<T>, or add synchronization.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
}


# ─── Triage Persistence ───────────────────────────────────────────────

TRIAGE_VERSION = 1
TRIAGE_FILE = "triage.json"
TRIAGE_STATUSES = {"unreviewed", "confirmed", "false_positive", "accepted_risk", "fixed"}


def make_finding_id(file_path: str, smell: dict) -> str:
    """Generate a stable finding ID from file path and smell data.

    Format: {type}::{normalized_path}:{line}
    """
    normalized = file_path.replace("\\", "/")
    return f"{smell['type']}::{normalized}:{smell.get('line', 0)}"


def load_triage(out_dir: str) -> dict:
    """Load existing triage.json from output directory."""
    triage_path = os.path.join(out_dir, TRIAGE_FILE)
    try:
        data = json.loads(Path(triage_path).read_text(encoding="utf-8"))
        if data.get("version") != TRIAGE_VERSION:
            print(f"  Warning: triage.json version mismatch (expected {TRIAGE_VERSION})")
        return data.get("dispositions", {})
    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  Warning: could not load {triage_path}: {exc}")
        return {}


def save_triage(out_dir: str, dispositions: dict):
    """Save triage.json to output directory."""
    triage_path = os.path.join(out_dir, TRIAGE_FILE)
    data = {
        "version": TRIAGE_VERSION,
        "generated": date.today().isoformat(),
        "dispositions": dispositions,
    }
    try:
        Path(triage_path).write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )
        print(f"Saved: {triage_path}")
    except OSError as e:
        print(f"ERROR: Failed to save {triage_path}: {e}", file=sys.stderr)


def apply_triage(projects: list, dispositions: dict) -> dict:
    """Apply existing triage dispositions to scan results.

    For each finding, looks up the finding ID in the dispositions dict.
    If a line-exact match isn't found, tries fuzzy matching by context
    within a +/-5 line window.

    Returns updated dispositions dict (with new findings added as unreviewed).
    """
    updated = dict(dispositions)  # preserve existing entries
    stats = {"matched": 0, "new": 0, "stale": 0}

    # Build a reverse index: (type, normalized_path) -> [(line, context, id)]
    # for fuzzy matching when line numbers shift
    existing_by_file: dict[tuple, list] = {}
    for fid, disp in dispositions.items():
        parts = fid.split("::", 1)
        if len(parts) != 2:
            continue
        smell_type = parts[0]
        file_line = parts[1]
        colon_idx = file_line.rfind(":")
        if colon_idx == -1:
            continue
        fpath = file_line[:colon_idx]
        try:
            line_num = int(file_line[colon_idx + 1:])
        except ValueError:
            continue
        key = (smell_type, fpath)
        if key not in existing_by_file:
            existing_by_file[key] = []
        existing_by_file[key].append((line_num, disp.get("context", ""), fid))

    matched_ids = set()

    for project in projects:
        for file_data in project.get("files", []):
            file_path = file_data.get("path", "")
            for smell in file_data.get("smells", []):
                fid = make_finding_id(file_path, smell)
                smell["findingId"] = fid

                if fid in updated:
                    # Exact match
                    smell["triageStatus"] = updated[fid].get("status", "unreviewed")
                    matched_ids.add(fid)
                    stats["matched"] += 1
                else:
                    # Try fuzzy match: same type+file, context match within 5 lines
                    norm_path = file_path.replace("\\", "/")
                    key = (smell["type"], norm_path)
                    fuzzy_match = None
                    if key in existing_by_file:
                        smell_line = smell.get("line", 0)
                        smell_ctx = smell.get("context", "")
                        for old_line, old_ctx, old_id in existing_by_file[key]:
                            if old_id in matched_ids:
                                continue
                            if abs(old_line - smell_line) <= 5 and old_ctx and old_ctx == smell_ctx:
                                fuzzy_match = old_id
                                break

                    if fuzzy_match and fuzzy_match in updated:
                        # Migrate the disposition to the new finding ID
                        old_disp = updated[fuzzy_match]
                        smell["triageStatus"] = old_disp.get("status", "unreviewed")
                        updated[fid] = dict(old_disp)
                        updated[fid]["context"] = smell.get("context", "")
                        matched_ids.add(fuzzy_match)
                        matched_ids.add(fid)
                        stats["matched"] += 1
                    else:
                        # New finding
                        smell["triageStatus"] = "unreviewed"
                        updated[fid] = {
                            "status": "unreviewed",
                            "reason": "",
                            "decidedBy": "",
                            "date": "",
                            "context": smell.get("context", ""),
                        }
                        stats["new"] += 1

    # Count stale dispositions (in triage but not matched to any current finding)
    stats["stale"] = sum(1 for fid in dispositions if fid not in matched_ids)

    print(f"  Triage: {stats['matched']} matched, {stats['new']} new, {stats['stale']} stale")
    return updated


def analyze_file(filepath: str, scan_root: str, level: str = "high") -> dict | None:
    """Analyze a single file for complexity and smells (supports C# and Java)."""
    # Detect language from file extension
    ext = os.path.splitext(filepath)[1].lower()
    language_map = {".cs": "csharp", ".java": "java"}
    language = language_map.get(ext, "unknown")

    if language == "unknown":
        return None

    content = safe_read_text(filepath)
    if content is None:
        return None

    lines = content.split('\n')
    line_count = len(lines)

    # Skip small files
    if line_count < _MIN_INTERESTING_LINES:
        return None

    # Compute metrics (currently C#-specific, but work for Java too)
    cyclomatic = compute_cyclomatic_complexity(content)
    nesting_depth = compute_max_nesting_depth(content)
    method_count = count_methods(content)
    long_methods = detect_long_methods(content)

    # Detect smells via registry, filtered by severity level
    detectors = get_detectors(language, level)
    smells = []
    for det in detectors:
        found = det["fn"](filepath, content, lines)
        for s in found:
            s["severity"] = det["severity"]
            s["category"] = det["category"]
            s["language"] = language  # Tag each smell with language
        smells.extend(found)

    # Compute complexity score
    complexity_score = cyclomatic + (nesting_depth * 3) + (len(long_methods) * 5)

    rel_path = _relpath(filepath, scan_root)

    return {
        "path": rel_path,
        "language": language,  # Add language to file metadata
        "lines": line_count,
        "cyclomatic": cyclomatic,
        "nesting_depth": nesting_depth,
        "method_count": method_count,
        "long_methods": len(long_methods),
        "complexity_score": complexity_score,
        "smells": smells,
        "smell_count": len(smells),
    }


# ─── Load Existing Analysis Data ──────────────────────────────────────

def load_json(path: str, default=None):
    """Load a JSON file, returning default on error."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        if default is None:
            print(f"  Warning: could not load {path}: {exc}")
            return {}
        return default


def load_existing_analysis(out_dir: str) -> dict:
    """Load existing analysis data from output directory."""
    print("Loading existing analysis data...")
    
    data = {
        "graph": load_json(os.path.join(out_dir, "graph.json"), {}),
        "project_meta": load_json(os.path.join(out_dir, "project-meta.json"), []),
        "flow_paths": load_json(os.path.join(out_dir, "flow-paths.json"), {}),
        "repos": load_json(os.path.join(out_dir, "repos.json"), []),
    }
    
    # Build lookup tables
    data["fan_in"] = {}
    data["fan_out"] = {}
    
    graph = data["graph"]
    if graph and "nodes" in graph:
        for node in graph["nodes"]:
            project = node.get("id")
            if project:
                data["fan_in"][project] = node.get("fanIn", 0)
                data["fan_out"][project] = node.get("fanOut", 0)
    
    # Build project category lookup
    data["project_category"] = {}
    data["project_layer"] = {}
    for pm in data["project_meta"]:
        project = pm.get("project")
        if project:
            data["project_category"][project] = pm.get("category", "")
            
            # Get layer from flow_paths if available
            bl = data["flow_paths"].get("businessLayers", {})
            layer_info = bl.get(project, {})
            data["project_layer"][project] = layer_info.get("layer", "")
    
    # Load test coverage data if available
    test_data = load_json(os.path.join(out_dir, "test-projects.json"), {})
    if test_data.get("coverage"):
        data["test_coverage"] = test_data["coverage"]
        print(f"  Loaded test coverage: {len(data['test_coverage'])} projects covered")

    # Warn if project-meta.json is empty or missing
    if not data["project_meta"]:
        print("  ⚠ WARNING: project-meta.json is empty or missing!")
        print("    Run 1_scan_projects.py first for best results.")
        print("    Falling back to directory-based project grouping.")

    return data


def find_project_for_file(filepath: str, project_meta: list, scan_root: str) -> str | None:
    """Find which project a file belongs to based on project paths."""
    filepath = _normalize_path(filepath)
    
    # Sort by path length (longest first) to match most specific project
    sorted_projects = sorted(
        project_meta,
        key=lambda p: len(p.get("globalPath") or p.get("path", "")),
        reverse=True
    )
    
    for pm in sorted_projects:
        # Get project path (may be relative to scan_root)
        proj_path = pm.get("globalPath") or pm.get("path", "")
        if not proj_path:
            continue
        
        # Make it absolute if it's relative
        if not os.path.isabs(proj_path):
            proj_path = os.path.join(scan_root, proj_path)
        
        proj_path = _normalize_path(proj_path)
        
        # Check if file is under this project directory
        proj_dir = os.path.dirname(proj_path)
        try:
            rel = _relpath(filepath, proj_dir)
            if not rel.startswith(".."):
                return pm.get("project")
        except ValueError:
            continue
    
    return None


def infer_project_from_path(filepath: str, scan_root: str) -> str:
    """Infer a project name from the file path when project-meta.json has no match.
    
    Strategy:
    1. Walk up from the file looking for a directory containing a .csproj file
    2. If found, use the .csproj filename (without extension) as the project name  
    3. If not found, use the parent directory name as a fallback
    """
    norm_path = _normalize_path(filepath)
    norm_root = _normalize_path(scan_root)
    
    # Walk up from file directory looking for a .csproj
    current = os.path.dirname(norm_path)
    while current and current != norm_root and len(current) >= len(norm_root):
        try:
            for entry in os.scandir(_fs_path(current)):
                if entry.name.endswith('.csproj') and entry.is_file():
                    return os.path.splitext(entry.name)[0]
        except OSError:
            pass
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    
    # Fallback: use parent directory name relative to scan root
    try:
        rel = _relpath(filepath, scan_root)
        parts = rel.replace("\\", "/").split("/")
        if len(parts) > 1:
            return parts[0]  # top-level directory under scan root
    except ValueError:
        pass
    
    return "_unknown"


def detect_test_coverage_gap(project: str, project_meta: list, analysis_data: dict) -> bool:
    """Check if a project has no corresponding test project.

    Uses test-projects.json coverage data when available, falling back to
    the original graph-edge check otherwise.
    """
    # Prefer test-projects.json coverage data if loaded
    test_coverage = analysis_data.get("test_coverage")
    if test_coverage is not None:
        return project not in test_coverage

    # Fallback: look for test projects that reference this project via graph edges
    graph = analysis_data.get("graph", {})
    edges = graph.get("links", [])

    for edge in edges:
        target = edge.get("target")
        source = edge.get("source")

        if target == project:
            # Check if source is a test project
            source_category = analysis_data["project_category"].get(source, "")
            if "test" in source_category.lower():
                return False

    return True


def is_deprioritized_project(project: str, category: str) -> bool:
    """Check if project should be deprioritized."""
    if category.lower() in DEPRIORITIZE_CATEGORIES:
        return True
    
    # Check namespace patterns
    for pattern in DEPRIORITIZE_NAMESPACES:
        if re.search(pattern, project, re.IGNORECASE):
            return True
    
    return False


def is_financial_project(project: str) -> bool:
    """Check if project is related to financial pricing."""
    for pattern in FINANCIAL_PATTERNS:
        if re.search(pattern, project, re.IGNORECASE):
            return True
    return False


# ─── Scoring ──────────────────────────────────────────────────────────

def compute_refactoring_value_score(
    project_data: dict,
    analysis_data: dict,
) -> float:
    """Compute the refactoring value score for a project.

    Uses severity-weighted smell scoring so security findings dominate.
    """
    project = project_data["project"]
    complexity_score = project_data["complexity_score"]

    # Severity-weighted smell score (replaces flat smell_count * 3)
    weighted_smell_score = 0
    for f in project_data.get("files", []):
        for smell in f.get("smells", []):
            sev = smell.get("severity", "low")
            weighted_smell_score += SEVERITY_WEIGHTS.get(sev, 1)

    fan_in = analysis_data["fan_in"].get(project, 0)
    fan_out = analysis_data["fan_out"].get(project, 0)

    category = analysis_data["project_category"].get(project, "")
    has_tests = not detect_test_coverage_gap(project, analysis_data["project_meta"], analysis_data)

    test_gap_penalty = 0 if has_tests else 1
    deprioritize_discount = 20 if is_deprioritized_project(project, category) else 0

    score = (
        complexity_score * 2
        + weighted_smell_score
        + (fan_in * fan_out) * 0.5
        + test_gap_penalty * 5
        - deprioritize_discount
    )

    return max(0, score)


# ─── Main Analysis ────────────────────────────────────────────────────

def analyze_all_files(scan_root: str, level: str = "high") -> dict:
    """Scan all .cs files and compute metrics."""
    print(f"Scanning for source files in: {scan_root}")
    print(f"Severity level: {level} (running {' + '.join(s for s in SEVERITY_ORDER if SEVERITY_ORDER[s] <= SEVERITY_ORDER[level])})")
    source_files = find_source_files(scan_root)
    print(f"Found {len(source_files)} source files to analyze")

    # Load existing analysis
    analysis_data = load_existing_analysis(OUT_DIR)

    # Group files by project
    project_files = defaultdict(list)

    print("\nAnalyzing files...")
    analyzed_count = 0
    fallback_count = 0

    for i, filepath in enumerate(source_files):
        if (i + 1) % _PROGRESS_INTERVAL == 0:
            print(f"  Progress: {i + 1}/{len(source_files)} files analyzed")

        file_data = analyze_file(filepath, scan_root, level=level)
        if file_data is None:
            continue
        
        analyzed_count += 1
        
        # Find which project this file belongs to
        project = find_project_for_file(filepath, analysis_data["project_meta"], scan_root)
        if not project:
            project = infer_project_from_path(filepath, scan_root)
            fallback_count += 1
        project_files[project].append(file_data)
    
    print(f"\nAnalyzed {analyzed_count} files (skipped {len(source_files) - analyzed_count} small/excluded files)")
    if fallback_count > 0:
        print(f"  ({fallback_count} files matched by directory fallback, not project-meta.json)")
    real_project_count = sum(1 for p in project_files if not p.startswith("_"))
    print(f"Files grouped into {real_project_count} projects")
    
    # Aggregate by project
    projects = []
    
    for project, files in project_files.items():
        
        total_lines = sum(f["lines"] for f in files)
        total_complexity = sum(f["complexity_score"] for f in files)
        total_smells = sum(f["smell_count"] for f in files)
        
        # Collect smell types
        smell_types = defaultdict(int)
        for f in files:
            for smell in f["smells"]:
                smell_types[smell["type"]] += 1
        
        top_smells = sorted(smell_types.items(), key=lambda x: -x[1])[:5]
        
        category = analysis_data["project_category"].get(project, "unknown")
        layer = analysis_data["project_layer"].get(project, "")
        fan_in = analysis_data["fan_in"].get(project, 0)
        fan_out = analysis_data["fan_out"].get(project, 0)
        has_tests = not detect_test_coverage_gap(project, analysis_data["project_meta"], analysis_data)
        
        # Get repo name from project metadata
        repo = ""
        for pm in analysis_data["project_meta"]:
            if pm.get("project") == project:
                repo = pm.get("repo", "")
                break
        
        project_data = {
            "project": project,
            "repo": repo,
            "category": category,
            "layer": layer,
            "fan_in": fan_in,
            "fan_out": fan_out,
            "has_tests": has_tests,
            "total_files": len(files),
            "total_lines": total_lines,
            "complexity_score": total_complexity,
            "smell_count": total_smells,
            "top_smells": [s[0] for s in top_smells],
            "smell_counts": dict(smell_types),  # Store full smell counts for later use
            "files": files,
        }
        
        # Compute refactoring value score
        score = compute_refactoring_value_score(project_data, analysis_data)
        project_data["refactoring_value_score"] = round(score, 2)
        
        projects.append(project_data)
    
    # Sort by refactoring value score
    projects.sort(key=lambda x: -x["refactoring_value_score"])
    
    return {
        "projects": projects,
        "total_files_scanned": len(source_files),
        "total_files_analyzed": analyzed_count,
        "analysis_data": analysis_data,
    }


# ─── Generate Claude Code Targets ─────────────────────────────────────

def generate_claude_targets(projects: list) -> dict:
    """Generate pre-formatted context summaries for Claude Code sessions."""
    targets = {
        "tier1_critical": [],
        "tier2_high": [],
        "tier3_medium": [],
    }
    
    for project in projects:
        score = project["refactoring_value_score"]
        
        # Determine tier
        if score > 100:
            tier = "tier1_critical"
            effort = "high"
        elif score > 50:
            tier = "tier2_high"
            effort = "medium"
        elif score > 20:
            tier = "tier3_medium"
            effort = "low"
        else:
            continue  # Skip low-value projects
        
        # Build explanation
        why_parts = [f"Refactoring value: {score}"]
        
        if project["smell_count"] > 0:
            # Use precomputed smell counts for efficiency
            smell_counts = project.get("smell_counts", {})
            top_3_smells = sorted(smell_counts.items(), key=lambda x: -x[1])[:3]
            smell_summary = ", ".join(f"{count} {smell}" for smell, count in top_3_smells)
            why_parts.append(smell_summary)
        
        if not project["has_tests"]:
            why_parts.append("no test coverage")
        
        if project["fan_in"] > 5:
            why_parts.append(f"fan-in={project['fan_in']}")
        
        why = ". ".join(why_parts) + "."
        
        # Get top files by complexity
        top_files = sorted(
            project["files"],
            key=lambda f: f["complexity_score"],
            reverse=True
        )[:5]
        
        # Build suggested prompt
        focus_areas = []
        if any(smell["type"] == "precision_unsafe_math" for f in project["files"] for smell in f["smells"]):
            focus_areas.append("precision-unsafe math (double used for financial calculations)")
        if any(smell["type"] == "sync_over_async" for f in project["files"] for smell in f["smells"]):
            focus_areas.append("sync-over-async patterns")
        if any(smell["type"] == "god_method" for f in project["files"] for smell in f["smells"]):
            focus_areas.append("god methods (>100 lines)")
        if any(smell["type"] == "exception_swallowing" for f in project["files"] for smell in f["smells"]):
            focus_areas.append("exception swallowing")
        if any(smell["type"] == "python_call" for f in project["files"] for smell in f["smells"]):
            focus_areas.append("Python interop calls (cross-technology boundary)")

        prompt = f"Review {project['project']} for refactoring."
        if focus_areas:
            prompt += f" Focus on: {', '.join(focus_areas)}."
        if not project["has_tests"]:
            prompt += f" This project has no test coverage."
        if project["fan_in"] > 5:
            prompt += f" This project has {project['fan_in']} downstream dependents."
        
        targets[tier].append({
            "project": project["project"],
            "why": why,
            "suggestedPrompt": prompt,
            "estimatedEffort": effort,
            "files": [f["path"] for f in top_files],
        })
    
    return targets


# ─── Output Generation ────────────────────────────────────────────────

def save_json_output(data: dict, output_path: str):
    """Save JSON output file."""
    output_dir = os.path.dirname(output_path)
    if output_dir:  # Only create directory if path has a directory component
        os.makedirs(output_dir, exist_ok=True)
    try:
        Path(output_path).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )
        print(f"Saved: {output_path}")
    except OSError as e:
        print(f"ERROR: Failed to save {output_path}: {e}", file=sys.stderr)
        sys.exit(1)


def generate_markdown_report(data: dict, output_path: str):
    """Generate human-readable markdown report."""
    projects = data["projects"]
    summary = data["summary"]
    claude_targets = data["claudeCodeTargets"]
    
    lines = [
        "# Refactoring Triage Report",
        "",
        f"**Generated:** {date.today().isoformat()}",
        f"**Scan Root:** {SCAN_ROOT}",
        "",
        "## Executive Summary",
        "",
        f"- **Total Files Scanned:** {summary['totalFilesScanned']}",
        f"- **Total Files with Smells:** {summary['totalFilesWithSmells']}",
        f"- **Total Smells:** {summary['totalSmells']}",
        "",
        "### Top Smell Types",
        "",
    ]
    
    for smell_data in summary["topSmellTypes"][:10]:
        lines.append(f"- **{smell_data['smell']}**: {smell_data['count']}")
    
    lines.extend([
        "",
        "## Top 30 Projects by Refactoring Value",
        "",
    ])
    
    for i, project in enumerate(projects[:30], 1):
        lines.extend([
            f"### {i}. {project['project']}",
            "",
            f"- **Refactoring Value Score:** {project['refactoring_value_score']}",
            f"- **Category:** {project['category']}",
            f"- **Layer:** {project['layer'] or 'N/A'}",
            f"- **Fan-in:** {project['fan_in']}, **Fan-out:** {project['fan_out']}",
            f"- **Has Tests:** {'Yes' if project['has_tests'] else '❌ No'}",
            f"- **Total Files:** {project['total_files']}, **Total Lines:** {project['total_lines']}",
            f"- **Complexity Score:** {project['complexity_score']}",
            f"- **Total Smells:** {project['smell_count']}",
            "",
            "**Top Smells:**",
            "",
        ])
        
        for smell in project["top_smells"][:5]:
            count = sum(1 for f in project["files"] for s in f["smells"] if s["type"] == smell)
            lines.append(f"- {smell}: {count}")
        
        lines.extend([
            "",
            "**Key Files:**",
            "",
        ])
        
        top_files = sorted(project["files"], key=lambda f: f["complexity_score"], reverse=True)[:3]
        for f in top_files:
            lines.append(f"- `{f['path']}` (complexity: {f['complexity_score']}, smells: {f['smell_count']})")
        
        lines.append("")
    
    # Financial projects section
    financial_projects = [p for p in projects if is_financial_project(p["project"])]
    if financial_projects:
        lines.extend([
            "## Financial Pricer Projects",
            "",
            "Projects detected as financial pricers (precision-critical):",
            "",
        ])
        
        for project in financial_projects[:10]:
            lines.extend([
                f"### {project['project']}",
                "",
                f"- **Refactoring Value Score:** {project['refactoring_value_score']}",
                f"- **Precision-unsafe math patterns:** {sum(1 for f in project['files'] for s in f['smells'] if s['type'] == 'precision_unsafe_math')}",
                f"- **Total Smells:** {project['smell_count']}",
                "",
            ])
    
    # Claude Code Session Plan
    lines.extend([
        "## Claude Code Session Plan",
        "",
        "### Tier 1: Critical Refactoring Targets (Immediate Focus)",
        "",
    ])
    
    for target in claude_targets["tier1_critical"][:5]:
        lines.extend([
            f"#### {target['project']}",
            "",
            f"**Why:** {target['why']}",
            "",
            f"**Suggested Prompt:**",
            "",
            f"> {target['suggestedPrompt']}",
            "",
            f"**Estimated Effort:** {target['estimatedEffort']}",
            "",
            "**Key Files:**",
            "",
        ])
        for file in target["files"][:5]:
            lines.append(f"- {file}")
        lines.append("")
    
    lines.extend([
        "### Tier 2: High-Value Refactoring (Next Phase)",
        "",
    ])
    
    for target in claude_targets["tier2_high"][:5]:
        lines.append(f"- **{target['project']}**: {target['why']}")
    
    lines.extend([
        "",
        "### Tier 3: Medium-Value Refactoring (Opportunistic)",
        "",
    ])
    
    for target in claude_targets["tier3_medium"][:5]:
        lines.append(f"- **{target['project']}**: {target['why']}")
    
    output_dir = os.path.dirname(output_path)
    if output_dir:  # Only create directory if path has a directory component
        os.makedirs(output_dir, exist_ok=True)
    try:
        Path(output_path).write_text("\n".join(lines), encoding="utf-8")
        print(f"Saved: {output_path}")
    except OSError as e:
        print(f"ERROR: Failed to save {output_path}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    print("=" * 70)
    print("Refactoring Triage Analyzer")
    print("=" * 70)
    print(f"Scan root: {SCAN_ROOT}")
    print(f"Output dir: {OUT_DIR}")
    print(f"Severity level: {SCAN_LEVEL}")
    print()

    # Fail fast: create output directory before doing any expensive work
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
    except OSError as e:
        print(f"ERROR: Cannot create output directory '{OUT_DIR}': {e}", file=sys.stderr)
        sys.exit(1)

    # Analyze all files
    result = analyze_all_files(SCAN_ROOT, level=SCAN_LEVEL)
    projects = result["projects"]

    # Load and apply triage dispositions
    print("\nApplying triage dispositions...")
    existing_triage = load_triage(OUT_DIR)
    updated_triage = apply_triage(projects, existing_triage)

    # Compute summary statistics
    total_files_with_smells = sum(1 for p in projects for f in p["files"] if f["smell_count"] > 0)
    total_smells = sum(p["smell_count"] for p in projects)

    # Count smell types, severity counts, and triage status across all projects
    all_smell_types = defaultdict(int)
    severity_counts = defaultdict(int)
    category_counts = defaultdict(int)
    triage_counts = defaultdict(int)
    for project in projects:
        for file in project["files"]:
            for smell in file["smells"]:
                all_smell_types[smell["type"]] += 1
                severity_counts[smell.get("severity", "low")] += 1
                category_counts[smell.get("category", "style")] += 1
                triage_counts[smell.get("triageStatus", "unreviewed")] += 1

    top_smell_types = [
        {"smell": smell, "count": count}
        for smell, count in sorted(all_smell_types.items(), key=lambda x: -x[1])[:10]
    ]

    top_projects = [p["project"] for p in projects[:10]]

    summary = {
        "totalFilesScanned": result["total_files_scanned"],
        "totalFilesWithSmells": total_files_with_smells,
        "totalSmells": total_smells,
        "topSmellTypes": top_smell_types,
        "topProjectsByScore": top_projects,
        "severityCounts": dict(severity_counts),
        "categoryCounts": dict(category_counts),
        "triageCounts": dict(triage_counts),
        "level": SCAN_LEVEL,
    }

    # Generate Claude Code targets
    claude_targets = generate_claude_targets(projects)

    # Clean up internal fields before output
    for project in projects:
        # Remove smell_counts (internal use only)
        project.pop("smell_counts", None)

    # Prepare output
    output_data = {
        "generated": date.today().isoformat(),
        "scanRoot": SCAN_ROOT,
        "summary": summary,
        "projects": projects,
        "claudeCodeTargets": claude_targets,
        "smellPrompts": SMELL_PROMPTS,
    }

    # Save outputs
    print("\nGenerating outputs...")
    json_path = os.path.join(OUT_DIR, "refactoring-targets.json")
    md_path = os.path.join(OUT_DIR, "refactoring-report.md")
    triage_path = os.path.join(OUT_DIR, TRIAGE_FILE)

    save_json_output(output_data, json_path)
    save_triage(OUT_DIR, updated_triage)
    generate_markdown_report(
        {
            "projects": projects,
            "summary": summary,
            "claudeCodeTargets": claude_targets,
        },
        md_path
    )

    triaged = total_smells - triage_counts.get("unreviewed", 0)
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print(f"  - {len(projects)} projects analyzed")
    print(f"  - {total_smells} total smells detected")
    print(f"  - {triaged}/{total_smells} findings triaged")
    if triage_counts.get("false_positive"):
        print(f"  - {triage_counts['false_positive']} marked as false positive")
    if projects:
        print(f"  - Top project: {projects[0]['project']} (score: {projects[0]['refactoring_value_score']})")
    print("=" * 70)


if __name__ == "__main__":
    main()
