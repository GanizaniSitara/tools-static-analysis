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


# ─── Find all .cs files recursively ──────────────────────────────────

SKIP_DIRS = {".git", "node_modules", "bin", "obj", ".vs", ".idea", "packages",
              "TestResults", "artifacts", "__pycache__", ".nuget"}


def find_cs_files(
    directory: str,
    results: list | None = None,
    _depth: int = 0,
) -> list[str]:
    """Recursively find all .cs files, respecting exclusion patterns."""
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
            find_cs_files(full, results, _depth + 1)
        elif entry.name.endswith(".cs"):
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


# ─── Code Smell Detection ─────────────────────────────────────────────

def detect_exception_swallowing(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect catch blocks with empty body or just comments."""
    smells = []
    
    for i, line in enumerate(lines):
        if re.search(r'\bcatch\s*\(', line):
            # Find the catch block
            start = i
            brace_depth = 0
            in_block = False
            block_content = []
            
            for j in range(i, min(i + 20, len(lines))):  # Look ahead max 20 lines
                if '{' in lines[j]:
                    in_block = True
                    brace_depth += lines[j].count('{')
                
                if in_block:
                    block_content.append(lines[j].strip())
                
                brace_depth -= lines[j].count('}')
                if in_block and brace_depth == 0:
                    break
            
            # Check if block is empty or just has TODO
            non_empty_lines = [
                l for l in block_content 
                if l and l not in ['{', '}'] and not l.startswith('//')
            ]
            
            if len(non_empty_lines) == 0 or (len(non_empty_lines) == 1 and 'TODO' in non_empty_lines[0]):
                smells.append({
                    "type": "exception_swallowing",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    
    return smells


def detect_sync_over_async(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect sync-over-async patterns (.Result, .Wait(), .GetAwaiter().GetResult())."""
    smells = []
    
    patterns = [
        (r'\.Result\b', '.Result'),
        (r'\.Wait\s*\(', '.Wait()'),
        (r'\.GetAwaiter\s*\(\s*\)\.GetResult\s*\(', '.GetAwaiter().GetResult()'),
    ]
    
    for i, line in enumerate(lines):
        for pattern, name in patterns:
            if re.search(pattern, line):
                smells.append({
                    "type": "sync_over_async",
                    "line": i + 1,
                    "context": line.strip()[:80],
                    "pattern": name,
                })
    
    return smells


def detect_magic_numbers(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect hardcoded numeric literals (excluding common constants)."""
    smells = []

    # Expanded exclusion set: common constants, time/size constants
    exclude_numbers = {0, 1, -1, 2, 10, 100, 1000, 60, 24, 365, 1024, 0.0, 1.0, 0.5, 2.0}

    # Skip test files entirely
    basename = os.path.basename(path).lower()
    if any(t in basename for t in ['test', 'spec', 'mock', 'fake']):
        return smells

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue

        # Skip const declarations, enum defs, attribute args, switch cases
        if re.search(r'\bconst\b', line):
            continue
        if re.search(r'\benum\b', line):
            continue
        if re.search(r'^\s*\[', line):  # attribute lines
            continue
        if re.search(r'^\s*case\s+', line):
            continue
        # Skip array/collection initializers
        if '{' in line and '}' in line:
            continue
        # Skip simple variable declarations (int x = 5;)
        if re.search(r'\b(int|long|short|byte|float|double|decimal)\s+\w+\s*=\s*\d+', line):
            continue
        # Skip test assertions
        if re.search(r'\b(Assert|Expect|Should)\b', line, re.IGNORECASE):
            continue

        # Remove string literals and comments for analysis
        cleaned_line = re.sub(r'"[^"]*"', '', line)
        cleaned_line = re.sub(r'//.*$', '', cleaned_line)

        # Only flag numbers in actual logic (conditions, returns, operations)
        if any(op in cleaned_line for op in ['if', 'while', 'for', 'return', '==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '%']):
            numbers = re.findall(r'\b(\d+(?:\.\d+)?)\b', cleaned_line)
            for num_str in numbers:
                try:
                    num = float(num_str) if '.' in num_str else int(num_str)
                    if num not in exclude_numbers:
                        smells.append({
                            "type": "magic_number",
                            "line": i + 1,
                            "context": line.strip()[:80],
                            "value": num_str,
                        })
                except ValueError:
                    pass

    return smells


def detect_precision_unsafe_math(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect use of float/double for financial calculations."""
    smells = []
    
    # Financial keywords
    financial_keywords = [
        'price', 'amount', 'value', 'rate', 'margin', 'pnl', 
        'profit', 'loss', 'cost', 'premium', 'strike', 'notional'
    ]
    
    for i, line in enumerate(lines):
        # Check for float/double declarations
        if re.search(r'\b(float|double)\s+\w+', line, re.IGNORECASE):
            # Check if any financial keyword is nearby (within 3 lines)
            context_start = max(0, i - 3)
            context_end = min(len(lines), i + 4)
            context = ' '.join(lines[context_start:context_end]).lower()
            
            if any(keyword in context for keyword in financial_keywords):
                smells.append({
                    "type": "precision_unsafe_math",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    
    return smells


def detect_mutable_shared_state(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect static mutable fields (not readonly, not const)."""
    smells = []
    # Exclude well-known thread-safe / immutable types
    safe_types = re.compile(
        r'\b(ILogger|IOptions|IConfiguration|IServiceProvider|IMemoryCache|'
        r'ConcurrentDictionary|ConcurrentBag|ConcurrentQueue|ConcurrentStack|'
        r'ImmutableArray|ImmutableList|ImmutableDictionary|Lazy)\b'
    )

    for i, line in enumerate(lines):
        if 'static' in line and ('=' in line or ';' in line):
            # Skip readonly, const, event, method signatures
            if 'readonly' in line or 'const' in line:
                continue
            if re.search(r'\bevent\b', line):
                continue
            # Skip if the type is a known thread-safe type
            if safe_types.search(line):
                continue
            # Must actually be a static field declaration
            if re.search(r'\bstatic\b', line):
                smells.append({
                    "type": "mutable_shared_state",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })

    return smells


def detect_missing_null_checks(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect public methods with reference-type parameters that don't check for null (heuristic)."""
    smells = []

    # Skip test files
    basename = os.path.basename(path).lower()
    if any(t in basename for t in ['test', 'spec', 'mock', 'fake']):
        return smells

    # Value types that don't need null checks
    value_types = {'int', 'long', 'short', 'byte', 'float', 'double', 'decimal',
                   'bool', 'char', 'DateTime', 'DateTimeOffset', 'TimeSpan',
                   'Guid', 'CancellationToken', 'void'}

    for i, line in enumerate(lines):
        # Skip private methods
        if re.search(r'\bprivate\s+', line):
            continue
        # Only check public methods
        if not re.search(r'\bpublic\s+\w+\s+\w+\s*\(', line):
            continue
        # Skip if line has [NotNull] or [Required] attributes nearby (check prev 2 lines)
        context_before = '\n'.join(lines[max(0, i - 2):i + 1])
        if re.search(r'\[(NotNull|Required|NonNull)\]', context_before):
            continue

        # Extract parameter type-name pairs
        param_matches = re.findall(r'(\w+)\s+(\w+)(?:\s*[,\)])', line)

        if param_matches:
            method_body = '\n'.join(lines[i:min(i + 10, len(lines))])

            for param_type, param_name in param_matches:
                # Skip value types
                if param_type in value_types:
                    continue

                null_check_patterns = [
                    rf'\b{param_name}\s*==\s*null',
                    rf'\bnull\s*==\s*{param_name}',
                    rf'\b{param_name}\s*is\s*null',
                    rf'ArgumentNullException\.ThrowIfNull\s*\(\s*{param_name}',
                    rf'\b{param_name}\s*\?\?',
                    rf'\b{param_name}\s*!\.',  # null-forgiving operator
                ]

                has_null_check = any(re.search(pattern, method_body) for pattern in null_check_patterns)

                if not has_null_check:
                    smells.append({
                        "type": "missing_null_check",
                        "line": i + 1,
                        "context": line.strip()[:80],
                        "parameter": param_name,
                    })
                    break  # Only report once per method

    return smells


def detect_deep_inheritance(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect class declarations with multiple interfaces/base classes (>3 - heuristic).

    Note: This is a simplified heuristic that counts interfaces + base class.
    True deep inheritance analysis would require full type resolution across files.
    """
    smells = []
    
    for i, line in enumerate(lines):
        # Match class declarations with base classes/interfaces
        if re.search(r'\bclass\s+\w+\s*:', line):
            # Count number of items after the colon (base classes + interfaces)
            bases = line.split(':')[1] if ':' in line else ''
            # Count commas to get number of items
            base_count = len([b for b in bases.split(',') if b.strip()])
            
            # Flag if inheriting from many types (likely indicates complex inheritance)
            # This is a heuristic - not true depth but complexity indicator
            if base_count > 3:
                smells.append({
                    "type": "deep_inheritance",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    
    return smells


def detect_god_methods(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect methods exceeding 100 lines."""
    smells = []
    method_pattern = r'\b(public|private|protected|internal|static|virtual|override|abstract|async)\s+(?:\w+\s+)+(\w+)\s*\('
    for i, line in enumerate(lines):
        match = re.search(method_pattern, line)
        if match:
            method_name = match.group(2)
            brace_depth = 0
            found_opening = False
            end_line = i + 1
            for j in range(i, len(lines)):
                if '{' in lines[j]:
                    found_opening = True
                    brace_depth += lines[j].count('{')
                brace_depth -= lines[j].count('}')
                if found_opening and brace_depth == 0:
                    end_line = j + 1
                    break
            method_length = end_line - (i + 1)
            if method_length > 100:
                smells.append({
                    "type": "god_method",
                    "line": i + 1,
                    "context": f"Method {method_name} has {method_length} lines",
                })
    return smells


def detect_deep_nesting(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect methods with nesting depth > 4."""
    smells = []
    method_pattern = r'\b(public|private|protected|internal|static|virtual|override|abstract|async)\s+(?:\w+\s+)+(\w+)\s*\('
    for i, line in enumerate(lines):
        match = re.search(method_pattern, line)
        if match:
            method_name = match.group(2)
            brace_depth = 0
            max_depth = 0
            found_opening = False
            for j in range(i, len(lines)):
                if '{' in lines[j]:
                    found_opening = True
                    brace_depth += lines[j].count('{')
                    max_depth = max(max_depth, brace_depth)
                brace_depth -= lines[j].count('}')
                if found_opening and brace_depth == 0:
                    break
            # Subtract 1 for the method's own brace level
            if max_depth - 1 > 4:
                smells.append({
                    "type": "deep_nesting",
                    "line": i + 1,
                    "context": f"Method {method_name} has nesting depth {max_depth - 1}",
                })
    return smells


def detect_long_parameter_list(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect methods with more than 5 parameters."""
    smells = []
    method_pattern = r'\b(public|private|protected|internal|static|virtual|override|abstract|async)\s+(?:\w+\s+)+(\w+)\s*\('
    for i, line in enumerate(lines):
        match = re.search(method_pattern, line)
        if match:
            method_name = match.group(2)
            # Collect the full signature (may span multiple lines)
            sig = line
            paren_depth = sig.count('(') - sig.count(')')
            j = i
            while paren_depth > 0 and j + 1 < len(lines):
                j += 1
                sig += ' ' + lines[j]
                paren_depth += lines[j].count('(') - lines[j].count(')')
            # Extract everything inside outermost parens
            inner = re.search(r'\(([^)]*)\)', sig.replace('\n', ' '))
            if inner:
                params_str = inner.group(1).strip()
                if params_str:
                    param_count = len([p for p in params_str.split(',') if p.strip()])
                    if param_count > 5:
                        smells.append({
                            "type": "long_parameter_list",
                            "line": i + 1,
                            "context": f"Method {method_name} has {param_count} parameters",
                        })
    return smells


# ─── Security Detectors ───────────────────────────────────────────────

def detect_hardcoded_secrets(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect hardcoded passwords, API keys, secrets, and connection strings."""
    smells = []
    # Skip test files and development config
    basename = os.path.basename(path).lower()
    if any(t in basename for t in ['test', 'spec', 'mock', 'fake', 'stub', 'sample']):
        return smells
    if 'appsettings.development' in basename:
        return smells

    secret_pattern = re.compile(
        r'\b(password|passwd|pwd|apikey|api_key|secret|secretkey|secret_key|connectionstring|'
        r'access_key|token|auth_token|private_key)\s*[:=]\s*["\']([^"\']{8,})["\']',
        re.IGNORECASE
    )
    # Placeholders to exclude
    placeholder_pattern = re.compile(
        r'(\{[^}]+\}|<[^>]+>|\$\{|%[^%]+%|your[_-]|example|placeholder|changeme|xxx|todo|replace)',
        re.IGNORECASE
    )
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        for m in secret_pattern.finditer(line):
            value = m.group(2)
            if placeholder_pattern.search(value):
                continue
            smells.append({
                "type": "hardcoded_secret",
                "line": i + 1,
                "context": line.strip()[:80],
            })
            break  # One per line
    return smells


def detect_sql_injection(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect string concatenation/interpolation in SQL strings."""
    smells = []
    sql_keywords = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|EXEC|EXECUTE|DROP|ALTER)\b', re.IGNORECASE)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        # String concatenation in SQL
        if sql_keywords.search(line):
            # Check for string concat: "SELECT ... " + variable
            if re.search(r'"\s*\+\s*\w+', line) or re.search(r'\w+\s*\+\s*"', line):
                # Exclude parameterized patterns
                if not re.search(r'@\w+|\.Parameters\b|\.AddWithValue\b', line):
                    smells.append({
                        "type": "sql_injection",
                        "line": i + 1,
                        "context": line.strip()[:80],
                    })
                    continue
            # String interpolation in SQL: $"SELECT ... {variable}"
            if re.search(r'\$"[^"]*\b(SELECT|INSERT|UPDATE|DELETE|EXEC)\b[^"]*\{', line, re.IGNORECASE):
                # Exclude FromSqlRaw with params
                if not re.search(r'FromSql(Raw|Interpolated)\b', line):
                    smells.append({
                        "type": "sql_injection",
                        "line": i + 1,
                        "context": line.strip()[:80],
                    })
    return smells


def detect_insecure_deserialization(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect use of BinaryFormatter, SoapFormatter, and other insecure deserializers."""
    smells = []
    dangerous_types = re.compile(
        r'\b(BinaryFormatter|SoapFormatter|NetDataContractSerializer|LosFormatter)\b'
    )
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        if dangerous_types.search(line):
            smells.append({
                "type": "insecure_deserialization",
                "line": i + 1,
                "context": line.strip()[:80],
            })
        # JsonConvert.DeserializeObject with TypeNameHandling != None
        if 'TypeNameHandling' in line and 'None' not in line:
            if re.search(r'TypeNameHandling\s*[.=]\s*(All|Auto|Objects|Arrays)', line):
                smells.append({
                    "type": "insecure_deserialization",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    return smells


def detect_command_injection(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect Process.Start/ProcessStartInfo with string concat in arguments."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        if re.search(r'\b(Process\.Start|ProcessStartInfo)\b', line):
            # Check for string concat or interpolation in arguments
            if re.search(r'(\+\s*\w+|\$"[^"]*\{)', line):
                smells.append({
                    "type": "command_injection",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    return smells


def detect_weak_crypto(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect use of weak cryptographic algorithms."""
    smells = []
    weak_algos = re.compile(
        r'\b(MD5|SHA1|DES|TripleDES|RC2)\s*\.\s*Create\b'
    )
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        if weak_algos.search(line):
            smells.append({
                "type": "weak_crypto",
                "line": i + 1,
                "context": line.strip()[:80],
            })
    return smells


def detect_open_redirect(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect Redirect() with user-input parameters."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        if re.search(r'\bRedirect\s*\(', line):
            # Check if the argument references user input
            if re.search(r'(Request\.|returnUrl|redirectUrl|return_url|next|url)\b', line, re.IGNORECASE):
                # Exclude LocalRedirect and IsLocalUrl checks
                if not re.search(r'(LocalRedirect|IsLocalUrl|Url\.IsLocalUrl)', line):
                    smells.append({
                        "type": "open_redirect",
                        "line": i + 1,
                        "context": line.strip()[:80],
                    })
    return smells


def detect_xss(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect potential XSS via Html.Raw, Response.Write, and missing anti-forgery tokens."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        # Html.Raw with non-encoded input
        if re.search(r'@?Html\.Raw\s*\(', line):
            # Exclude if the argument is clearly a static string
            if not re.search(r'Html\.Raw\s*\(\s*"[^"]*"\s*\)', line):
                smells.append({
                    "type": "xss",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
        # Response.Write with variable input
        if re.search(r'Response\.Write\s*\(', line):
            if not re.search(r'Response\.Write\s*\(\s*"[^"]*"\s*\)', line):
                smells.append({
                    "type": "xss",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    # Check for POST actions missing ValidateAntiForgeryToken
    in_post_action = False
    post_line = 0
    has_antiforgery = False
    for i, line in enumerate(lines):
        if re.search(r'\[Http(Post|Put|Delete)\]', line):
            in_post_action = True
            post_line = i + 1
            has_antiforgery = False
        elif in_post_action:
            if re.search(r'\[ValidateAntiForgeryToken\]', line):
                has_antiforgery = True
            if re.search(r'\bpublic\s+(async\s+)?(IActionResult|ActionResult|Task)', line):
                if not has_antiforgery:
                    smells.append({
                        "type": "xss",
                        "line": post_line,
                        "context": f"POST action at line {post_line} missing [ValidateAntiForgeryToken]",
                    })
                in_post_action = False
    return smells


def detect_insecure_random(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect use of System.Random in security contexts."""
    smells = []
    # Security context keywords
    security_ctx = re.compile(
        r'\b(token|password|secret|key|nonce|salt|otp|verification|reset|auth|crypto|session)\b',
        re.IGNORECASE
    )
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        if re.search(r'\bnew\s+Random\s*\(', line):
            # Check surrounding context (5 lines before and after)
            context_start = max(0, i - 5)
            context_end = min(len(lines), i + 6)
            context_text = ' '.join(lines[context_start:context_end])
            if security_ctx.search(context_text):
                smells.append({
                    "type": "insecure_random",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    return smells


# ─── Detector Registry ────────────────────────────────────────────────

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

DETECTOR_REGISTRY = [
    # Critical — Security
    {"name": "hardcoded_secret",          "fn": detect_hardcoded_secrets,          "severity": "critical", "category": "security"},
    {"name": "sql_injection",             "fn": detect_sql_injection,              "severity": "critical", "category": "security"},
    {"name": "insecure_deserialization",  "fn": detect_insecure_deserialization,   "severity": "critical", "category": "security"},
    {"name": "command_injection",         "fn": detect_command_injection,          "severity": "critical", "category": "security"},
    # High — Security + Bugs
    {"name": "weak_crypto",               "fn": detect_weak_crypto,               "severity": "high",    "category": "security"},
    {"name": "open_redirect",             "fn": detect_open_redirect,             "severity": "high",    "category": "security"},
    {"name": "xss",                       "fn": detect_xss,                       "severity": "high",    "category": "security"},
    {"name": "insecure_random",           "fn": detect_insecure_random,           "severity": "high",    "category": "security"},
    {"name": "exception_swallowing",      "fn": detect_exception_swallowing,      "severity": "high",    "category": "bug"},
    {"name": "sync_over_async",           "fn": detect_sync_over_async,           "severity": "high",    "category": "bug"},
    # Medium — Code Quality
    {"name": "god_method",                "fn": detect_god_methods,               "severity": "medium",  "category": "quality"},
    {"name": "deep_nesting",              "fn": detect_deep_nesting,              "severity": "medium",  "category": "quality"},
    {"name": "long_parameter_list",       "fn": detect_long_parameter_list,       "severity": "medium",  "category": "quality"},
    {"name": "precision_unsafe_math",     "fn": detect_precision_unsafe_math,     "severity": "medium",  "category": "quality"},
    {"name": "deep_inheritance",          "fn": detect_deep_inheritance,          "severity": "medium",  "category": "quality"},
    # Low — Style/Noise
    {"name": "magic_number",              "fn": detect_magic_numbers,             "severity": "low",     "category": "style"},
    {"name": "missing_null_check",        "fn": detect_missing_null_checks,       "severity": "low",     "category": "style"},
    {"name": "mutable_shared_state",      "fn": detect_mutable_shared_state,      "severity": "low",     "category": "style"},
]


SEVERITY_WEIGHTS = {"critical": 15, "high": 8, "medium": 3, "low": 1}


def analyze_file(filepath: str, scan_root: str, level: str = "high") -> dict | None:
    """Analyze a single C# file for complexity and smells."""
    content = safe_read_text(filepath)
    if content is None:
        return None

    lines = content.split('\n')
    line_count = len(lines)

    # Skip small files
    if line_count < _MIN_INTERESTING_LINES:
        return None

    # Compute metrics
    cyclomatic = compute_cyclomatic_complexity(content)
    nesting_depth = compute_max_nesting_depth(content)
    method_count = count_methods(content)
    long_methods = detect_long_methods(content)

    # Detect smells via registry, filtered by severity level
    threshold = SEVERITY_ORDER[level]
    smells = []
    for det in DETECTOR_REGISTRY:
        if SEVERITY_ORDER[det["severity"]] <= threshold:
            found = det["fn"](filepath, content, lines)
            for s in found:
                s["severity"] = det["severity"]
                s["category"] = det["category"]
            smells.extend(found)

    # Compute complexity score
    complexity_score = cyclomatic + (nesting_depth * 3) + (len(long_methods) * 5)

    rel_path = _relpath(filepath, scan_root)

    return {
        "path": rel_path,
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
    print(f"Scanning for C# files in: {scan_root}")
    print(f"Severity level: {level} (running {' + '.join(s for s in SEVERITY_ORDER if SEVERITY_ORDER[s] <= SEVERITY_ORDER[level])})")
    cs_files = find_cs_files(scan_root)
    print(f"Found {len(cs_files)} C# files to analyze")

    # Load existing analysis
    analysis_data = load_existing_analysis(OUT_DIR)

    # Group files by project
    project_files = defaultdict(list)

    print("\nAnalyzing files...")
    analyzed_count = 0
    fallback_count = 0

    for i, filepath in enumerate(cs_files):
        if (i + 1) % _PROGRESS_INTERVAL == 0:
            print(f"  Progress: {i + 1}/{len(cs_files)} files analyzed")

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
    
    print(f"\nAnalyzed {analyzed_count} files (skipped {len(cs_files) - analyzed_count} small/excluded files)")
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
        "total_files_scanned": len(cs_files),
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
    
    # Compute summary statistics
    total_files_with_smells = sum(1 for p in projects for f in p["files"] if f["smell_count"] > 0)
    total_smells = sum(p["smell_count"] for p in projects)

    # Count smell types and severity counts across all projects
    all_smell_types = defaultdict(int)
    severity_counts = defaultdict(int)
    category_counts = defaultdict(int)
    for project in projects:
        for file in project["files"]:
            for smell in file["smells"]:
                all_smell_types[smell["type"]] += 1
                severity_counts[smell.get("severity", "low")] += 1
                category_counts[smell.get("category", "style")] += 1

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
    }
    
    # Save outputs
    print("\nGenerating outputs...")
    json_path = os.path.join(OUT_DIR, "refactoring-targets.json")
    md_path = os.path.join(OUT_DIR, "refactoring-report.md")
    
    save_json_output(output_data, json_path)
    generate_markdown_report(
        {
            "projects": projects,
            "summary": summary,
            "claudeCodeTargets": claude_targets,
        },
        md_path
    )
    
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print(f"  - {len(projects)} projects analyzed")
    print(f"  - {total_smells} total smells detected")
    if projects:
        print(f"  - Top project: {projects[0]['project']} (score: {projects[0]['refactoring_value_score']})")
    print("=" * 70)


if __name__ == "__main__":
    main()
