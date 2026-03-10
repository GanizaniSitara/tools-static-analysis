"""Python code smell detectors."""

from __future__ import annotations
import os
import re

from .base import create_detector


# ── Critical Security Detectors ──────────────────────────────────────

def detect_hardcoded_secrets(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect hardcoded passwords, API keys, and tokens in Python code."""
    smells = []
    patterns = [
        (r'(?:password|passwd|pwd)\s*=\s*["\']([^"\']{8,})["\']', "password"),
        (r'(?:api_?key|apikey|token|secret|secret_key)\s*=\s*["\']([^"\']{16,})["\']', "api_key"),
        (r'(?:aws_access_key_id|aws_secret_access_key)\s*=\s*["\']', "cloud_credential"),
        (r'(?:DATABASE_URL|MONGO_URI|REDIS_URL)\s*=\s*["\'][^"\']*://[^"\']*["\']', "connection_string"),
    ]

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for pattern, secret_type in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                if re.search(r'(?:example|placeholder|test|demo|sample|xxx|changeme|TODO)', line, re.IGNORECASE):
                    continue
                if re.search(r'os\.(?:environ|getenv)', line):
                    continue
                smells.append({
                    "type": "hardcoded_secret",
                    "line": i + 1,
                    "context": stripped[:120],
                    "secret_type": secret_type,
                })
                break
    return smells


def detect_sql_injection(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect SQL injection via string formatting/concatenation."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        # f-string in SQL context
        if re.search(r'(?:execute|executemany|raw)\s*\(\s*f["\']', line):
            smells.append({
                "type": "sql_injection",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "f_string_sql",
            })
        # %-formatting in SQL context
        elif re.search(r'(?:execute|executemany|raw)\s*\([^)]*%\s', line):
            smells.append({
                "type": "sql_injection",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "percent_format_sql",
            })
        # .format() in SQL context
        elif re.search(r'(?:execute|executemany|raw)\s*\([^)]*\.format\s*\(', line):
            smells.append({
                "type": "sql_injection",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "format_sql",
            })
        # String concatenation in SQL
        elif re.search(r'(?:execute|executemany|raw)\s*\([^)]*\+', line):
            smells.append({
                "type": "sql_injection",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "concatenation_sql",
            })
    return smells


def detect_command_injection(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect command injection via os.system, subprocess with shell=True."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.search(r'\bos\.system\s*\(', line):
            smells.append({
                "type": "command_injection",
                "line": i + 1,
                "context": stripped[:120],
                "mechanism": "os.system",
            })
        elif re.search(r'\bos\.popen\s*\(', line):
            smells.append({
                "type": "command_injection",
                "line": i + 1,
                "context": stripped[:120],
                "mechanism": "os.popen",
            })
        elif re.search(r'subprocess\.(?:call|run|Popen|check_output|check_call)\s*\(', line):
            if re.search(r'shell\s*=\s*True', line):
                smells.append({
                    "type": "command_injection",
                    "line": i + 1,
                    "context": stripped[:120],
                    "mechanism": "subprocess_shell_true",
                })
    return smells


def detect_insecure_deserialization(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect pickle.loads and yaml.load without SafeLoader."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.search(r'\bpickle\.loads?\s*\(', line):
            smells.append({
                "type": "insecure_deserialization",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "pickle_load",
            })
        elif re.search(r'\byaml\.load\s*\(', line):
            if not re.search(r'Loader\s*=\s*(?:yaml\.)?SafeLoader', line):
                smells.append({
                    "type": "insecure_deserialization",
                    "line": i + 1,
                    "context": stripped[:120],
                    "pattern": "yaml_unsafe_load",
                })
    return smells


# ── High Security + Bug Detectors ────────────────────────────────────

def detect_weak_crypto(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect weak hash algorithms (MD5, SHA1) used for security."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.search(r'\bhashlib\.(?:md5|sha1)\s*\(', line):
            algo = "MD5" if "md5" in line else "SHA1"
            smells.append({
                "type": "weak_crypto",
                "line": i + 1,
                "context": stripped[:120],
                "algorithm": algo,
            })
    return smells


def detect_insecure_random(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect random module usage for security-sensitive operations."""
    smells = []
    for i, line in enumerate(lines):
        if re.search(r'\brandom\.(?:randint|choice|random|randrange|sample)\s*\(', line):
            context = "\n".join(lines[max(0, i - 5):min(len(lines), i + 5)])
            if re.search(r'(?:token|password|key|secret|session|auth|salt|nonce|otp)', context, re.IGNORECASE):
                smells.append({
                    "type": "insecure_random",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "recommendation": "Use secrets module instead",
                })
    return smells


def detect_exception_swallowing(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect bare except or except with pass."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Bare except
        if re.match(r'except\s*:', stripped):
            smells.append({
                "type": "exception_swallowing",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "bare_except",
            })
        # except ... : pass
        elif re.match(r'except\b', stripped):
            # Look ahead for pass
            for j in range(i + 1, min(len(lines), i + 3)):
                next_stripped = lines[j].strip()
                if next_stripped == "pass":
                    smells.append({
                        "type": "exception_swallowing",
                        "line": i + 1,
                        "context": stripped[:120],
                        "pattern": "except_pass",
                    })
                    break
                elif next_stripped and not next_stripped.startswith("#"):
                    break
    return smells


def detect_eval_exec(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect eval() and exec() usage."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if re.search(r'\beval\s*\(', line):
            smells.append({
                "type": "eval_exec",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "eval",
            })
        elif re.search(r'\bexec\s*\(', line):
            smells.append({
                "type": "eval_exec",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "exec",
            })
    return smells


# ── Medium Quality Detectors ─────────────────────────────────────────

def detect_god_functions(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect functions exceeding 100 lines."""
    smells = []
    func_pattern = re.compile(r'^(\s*)def\s+(\w+)\s*\(')
    func_stack: list[tuple[int, str, int]] = []  # (indent_len, name, start_line)

    for i, line in enumerate(lines):
        m = func_pattern.match(line)
        if m:
            indent_len = len(m.group(1))
            name = m.group(2)
            # Close any functions at same or higher indent
            while func_stack and func_stack[-1][0] >= indent_len:
                prev_indent, prev_name, prev_start = func_stack.pop()
                length = i - prev_start
                if length > 100:
                    smells.append({
                        "type": "god_method",
                        "line": prev_start + 1,
                        "context": f"Function {prev_name} is {length} lines",
                        "method_name": prev_name,
                        "length": length,
                    })
            func_stack.append((indent_len, name, i))

    # Close remaining
    for indent_len, name, start in func_stack:
        length = len(lines) - start
        if length > 100:
            smells.append({
                "type": "god_method",
                "line": start + 1,
                "context": f"Function {name} is {length} lines",
                "method_name": name,
                "length": length,
            })
    return smells


def detect_deep_nesting(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect deep indentation nesting (>4 levels)."""
    smells = []
    reported_funcs: set[int] = set()

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        # Assume 4-space indent; count levels
        level = indent // 4
        if level > 4 and i not in reported_funcs:
            # Find the enclosing function
            func_line = i
            for j in range(i - 1, -1, -1):
                if re.match(r'\s*def\s+', lines[j]):
                    func_line = j
                    break
            if func_line not in reported_funcs:
                reported_funcs.add(func_line)
                smells.append({
                    "type": "deep_nesting",
                    "line": i + 1,
                    "context": f"Nesting depth: {level}",
                    "depth": level,
                })
    return smells


def detect_long_parameter_list(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect functions with more than 5 parameters."""
    smells = []
    func_pattern = re.compile(r'^\s*def\s+(\w+)\s*\(([^)]*)\)')

    for i, line in enumerate(lines):
        m = func_pattern.match(line)
        if m:
            name = m.group(1)
            params_str = m.group(2).strip()
            if not params_str:
                continue
            params = [p.strip() for p in params_str.split(",") if p.strip()]
            # Exclude self/cls
            params = [p for p in params if p not in ("self", "cls")]
            if len(params) > 5:
                smells.append({
                    "type": "long_parameter_list",
                    "line": i + 1,
                    "context": f"Function {name} has {len(params)} parameters",
                    "method_name": name,
                    "param_count": len(params),
                })
    return smells


def detect_mutable_default_args(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect mutable default arguments (list, dict, set)."""
    smells = []
    for i, line in enumerate(lines):
        if re.search(r'def\s+\w+\s*\(', line):
            if re.search(r'=\s*(?:\[\]|\{\}|set\(\))', line):
                smells.append({
                    "type": "mutable_default_arg",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "recommendation": "Use None as default and initialize inside function",
                })
    return smells


# ── Low Style Detectors ──────────────────────────────────────────────

def detect_star_imports(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect wildcard imports (from x import *)."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'from\s+\S+\s+import\s+\*', stripped):
            smells.append({
                "type": "star_import",
                "line": i + 1,
                "context": stripped[:120],
            })
    return smells


def detect_global_variables(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect use of the global keyword."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'global\s+\w', stripped):
            smells.append({
                "type": "global_variable",
                "line": i + 1,
                "context": stripped[:120],
            })
    return smells


# ── Python Detector Registry ─────────────────────────────────────────

PYTHON_DETECTORS = [
    # Critical -- Security
    create_detector("hardcoded_secret",          detect_hardcoded_secrets,          "critical", "security"),
    create_detector("sql_injection",             detect_sql_injection,              "critical", "security"),
    create_detector("command_injection",         detect_command_injection,          "critical", "security"),
    create_detector("insecure_deserialization",  detect_insecure_deserialization,   "critical", "security"),
    # High -- Security + Bugs
    create_detector("weak_crypto",               detect_weak_crypto,               "high",    "security"),
    create_detector("insecure_random",           detect_insecure_random,           "high",    "security"),
    create_detector("eval_exec",                 detect_eval_exec,                 "high",    "security"),
    create_detector("exception_swallowing",      detect_exception_swallowing,      "high",    "bug"),
    # Medium -- Code Quality
    create_detector("god_method",                detect_god_functions,             "medium",  "quality"),
    create_detector("deep_nesting",              detect_deep_nesting,              "medium",  "quality"),
    create_detector("long_parameter_list",       detect_long_parameter_list,       "medium",  "quality"),
    create_detector("mutable_default_arg",       detect_mutable_default_args,      "medium",  "quality"),
    # Low -- Style
    create_detector("star_import",               detect_star_imports,              "low",     "style"),
    create_detector("global_variable",           detect_global_variables,          "low",     "style"),
]
