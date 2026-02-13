#!/usr/bin/env python3
"""
Refactoring Triage Analyzer — AI-Assisted Refactoring Prioritization

Scans .NET C# source files to identify refactoring targets based on:
  - Complexity metrics (cyclomatic, nesting, method length)
  - Code smells (sync-over-async, exception swallowing, precision-unsafe math, etc.)
  - Coupling danger (fan-in/fan-out from existing analysis)
  - Test coverage gaps

Usage:
  python refactor_triage.py /path/to/repos [output-dir]

Outputs:
  - refactoring-targets.json (machine-readable analysis)
  - refactoring-report.md (human-readable report)
"""

import json
import os
import platform
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────

SCAN_ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT_DIR = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "output")

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


# ─── Path Utilities (from analyze.py) ────────────────────────────────

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
    count += len(re.findall(r'\?[^:]*:', content))  # ternary
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

def detect_exception_swallowing(content: str) -> list[dict]:
    """Detect catch blocks with empty body or just comments."""
    smells = []
    lines = content.split('\n')
    
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


def detect_sync_over_async(content: str) -> list[dict]:
    """Detect sync-over-async patterns (.Result, .Wait(), .GetAwaiter().GetResult())."""
    smells = []
    lines = content.split('\n')
    
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


def detect_magic_numbers(content: str) -> list[dict]:
    """Detect hardcoded numeric literals (excluding common constants)."""
    smells = []
    lines = content.split('\n')
    
    # Exclude common constants
    exclude_numbers = {0, 1, -1, 2, 10, 100, 1000}
    
    for i, line in enumerate(lines):
        # Skip comments and strings
        if '//' in line or '/*' in line or '"' in line:
            continue
        
        # Skip lines that look like test data or example assignments
        if re.search(r'\bint\s+\w+\s*=\s*\d+\s*;', line):
            continue
        
        # Skip array/collection initializers
        if '{' in line and '}' in line:
            continue
        
        # Find numeric literals in actual logic (not declarations)
        # Look for numbers in expressions, method calls, comparisons
        if any(op in line for op in ['if', 'while', 'for', 'return', '==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '%']):
            numbers = re.findall(r'\b(\d+(?:\.\d+)?)\b', line)
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


def detect_precision_unsafe_math(content: str) -> list[dict]:
    """Detect use of float/double for financial calculations."""
    smells = []
    lines = content.split('\n')
    
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


def detect_mutable_shared_state(content: str) -> list[dict]:
    """Detect static mutable fields (not readonly, not const)."""
    smells = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Match static fields that are not readonly or const
        if re.search(r'\bstatic\s+(?!readonly|const)\w+', line):
            # Make sure it's a field declaration (has an assignment or semicolon)
            if '=' in line or ';' in line:
                smells.append({
                    "type": "mutable_shared_state",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    
    return smells


def detect_missing_null_checks(content: str) -> list[dict]:
    """Detect public methods with reference-type parameters that don't check for null (heuristic)."""
    smells = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Find public method signatures
        if re.search(r'\bpublic\s+\w+\s+\w+\s*\([^)]*\w+\s+\w+', line):
            # Extract parameter names (simple heuristic)
            params = re.findall(r'\w+\s+(\w+)(?:\s*,|\s*\))', line)
            
            if params:
                # Check if method body checks for null (within next 10 lines)
                method_body = '\n'.join(lines[i:min(i + 10, len(lines))])
                
                for param in params:
                    # Check for null checks
                    if not re.search(rf'\b{param}\s*==\s*null|\bnull\s*==\s*{param}|\b{param}\s*is\s*null', method_body):
                        smells.append({
                            "type": "missing_null_check",
                            "line": i + 1,
                            "context": line.strip()[:80],
                            "parameter": param,
                        })
                        break  # Only report once per method
    
    return smells


def detect_deep_inheritance(content: str) -> list[dict]:
    """Detect class declarations with deep inheritance (>3 levels - heuristic)."""
    smells = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Match class declarations with base classes
        if re.search(r'\bclass\s+\w+\s*:', line):
            # Count number of base classes/interfaces (simple heuristic)
            bases = line.split(':')[1] if ':' in line else ''
            base_count = len([b for b in bases.split(',') if b.strip()])
            
            # This is a simplified check - in reality would need full type resolution
            if base_count > 3:
                smells.append({
                    "type": "deep_inheritance",
                    "line": i + 1,
                    "context": line.strip()[:80],
                })
    
    return smells


def analyze_file(filepath: str, scan_root: str) -> dict | None:
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
    
    # Detect smells
    smells = []
    smells.extend(detect_exception_swallowing(content))
    smells.extend(detect_sync_over_async(content))
    smells.extend(detect_magic_numbers(content))
    smells.extend(detect_precision_unsafe_math(content))
    smells.extend(detect_mutable_shared_state(content))
    smells.extend(detect_missing_null_checks(content))
    smells.extend(detect_deep_inheritance(content))
    
    # Check for god methods
    for method in long_methods:
        if method.get("is_god_method"):
            smells.append({
                "type": "god_method",
                "line": method["line"],
                "context": f"Method {method['name']} has {method['length']} lines",
            })
    
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


def detect_test_coverage_gap(project: str, project_meta: list, analysis_data: dict) -> bool:
    """Check if a project has no corresponding test project."""
    # Look for test projects that reference this project
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
    """Compute the refactoring value score for a project."""
    project = project_data["project"]
    complexity_score = project_data["complexity_score"]
    smell_count = project_data["smell_count"]
    
    fan_in = analysis_data["fan_in"].get(project, 0)
    fan_out = analysis_data["fan_out"].get(project, 0)
    
    category = analysis_data["project_category"].get(project, "")
    has_tests = not detect_test_coverage_gap(project, analysis_data["project_meta"], analysis_data)
    
    test_gap_penalty = 0 if has_tests else 1
    deprioritize_discount = 20 if is_deprioritized_project(project, category) else 0
    
    score = (
        complexity_score * 2
        + smell_count * 3
        + (fan_in * fan_out) * 0.5
        + test_gap_penalty * 5
        - deprioritize_discount
    )
    
    return max(0, score)


# ─── Main Analysis ────────────────────────────────────────────────────

def analyze_all_files(scan_root: str) -> dict:
    """Scan all .cs files and compute metrics."""
    print(f"Scanning for C# files in: {scan_root}")
    cs_files = find_cs_files(scan_root)
    print(f"Found {len(cs_files)} C# files to analyze")
    
    # Load existing analysis
    analysis_data = load_existing_analysis(OUT_DIR)
    
    # Group files by project
    project_files = defaultdict(list)
    
    print("\nAnalyzing files...")
    analyzed_count = 0
    
    for i, filepath in enumerate(cs_files):
        if (i + 1) % _PROGRESS_INTERVAL == 0:
            print(f"  Progress: {i + 1}/{len(cs_files)} files analyzed")
        
        file_data = analyze_file(filepath, scan_root)
        if file_data is None:
            continue
        
        analyzed_count += 1
        
        # Find which project this file belongs to
        project = find_project_for_file(filepath, analysis_data["project_meta"], scan_root)
        if project:
            project_files[project].append(file_data)
        else:
            # Orphan file - store under special key
            project_files["_orphaned"].append(file_data)
    
    print(f"\nAnalyzed {analyzed_count} files (skipped {len(cs_files) - analyzed_count} small/excluded files)")
    print(f"Files grouped into {len(project_files)} projects")
    
    # Aggregate by project
    projects = []
    
    for project, files in project_files.items():
        if project == "_orphaned":
            continue
        
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
            smell_summary = ", ".join(
                f"{count} {smell}" 
                for smell, count in [(s, sum(1 for f in project["files"] for sm in f["smells"] if sm["type"] == s)) for s in project["top_smells"]][:3]
            )
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
        if any("precision_unsafe_math" in f["smells"] for f in project["files"] for s in [f["smells"]]):
            focus_areas.append("precision-unsafe math (double used for financial calculations)")
        if any("sync_over_async" in str(f["smells"]) for f in project["files"]):
            focus_areas.append("sync-over-async patterns")
        if any("god_method" in str(f["smells"]) for f in project["files"]):
            focus_areas.append("god methods (>100 lines)")
        if any("exception_swallowing" in str(f["smells"]) for f in project["files"]):
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
    Path(output_path).write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )
    print(f"Saved: {output_path}")


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
    
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved: {output_path}")


def main():
    """Main entry point."""
    print("=" * 70)
    print("Refactoring Triage Analyzer")
    print("=" * 70)
    print(f"Scan root: {SCAN_ROOT}")
    print(f"Output dir: {OUT_DIR}")
    print()
    
    # Analyze all files
    result = analyze_all_files(SCAN_ROOT)
    projects = result["projects"]
    
    # Compute summary statistics
    total_files_with_smells = sum(1 for p in projects for f in p["files"] if f["smell_count"] > 0)
    total_smells = sum(p["smell_count"] for p in projects)
    
    # Count smell types across all projects
    all_smell_types = defaultdict(int)
    for project in projects:
        for file in project["files"]:
            for smell in file["smells"]:
                all_smell_types[smell["type"]] += 1
    
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
    }
    
    # Generate Claude Code targets
    claude_targets = generate_claude_targets(projects)
    
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
