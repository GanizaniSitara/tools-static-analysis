"""JavaScript/TypeScript code smell detectors."""

from __future__ import annotations
import os
import re

from .base import create_detector


# ── Critical Security Detectors ──────────────────────────────────────

def detect_hardcoded_secrets(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect hardcoded passwords, API keys, and tokens in JS/TS code."""
    smells = []
    patterns = [
        (r'(?:password|passwd|pwd)\s*[:=]\s*["\']([^"\']{8,})["\']', "password"),
        (r'(?:api_?key|apikey|token|secret|secret_key)\s*[:=]\s*["\']([^"\']{16,})["\']', "api_key"),
        (r'(?:AWS_ACCESS_KEY|AWS_SECRET|AZURE_KEY)\s*[:=]\s*["\']', "cloud_credential"),
        (r'(?:mongodb|postgres|mysql|redis)://[^:]+:[^@]+@', "connection_string"),
    ]

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue
        for pattern, secret_type in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                if re.search(r'(?:example|placeholder|test|demo|sample|xxx|changeme|TODO|process\.env)', line, re.IGNORECASE):
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
    """Detect SQL injection via template literals or concatenation."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        # Template literal in query context
        if re.search(r'(?:query|execute|raw)\s*\(\s*`[^`]*\$\{', line):
            smells.append({
                "type": "sql_injection",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "template_literal_sql",
            })
        # String concatenation in query
        elif re.search(r'(?:query|execute|raw)\s*\([^)]*\+', line):
            smells.append({
                "type": "sql_injection",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "concatenation_sql",
            })
    return smells


def detect_command_injection(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect command injection via child_process.exec or similar."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        if re.search(r'\bexec\s*\(\s*`[^`]*\$\{', line):
            smells.append({
                "type": "command_injection",
                "line": i + 1,
                "context": stripped[:120],
                "mechanism": "exec_template_literal",
            })
        elif re.search(r'\bexec\s*\([^)]*\+', line):
            smells.append({
                "type": "command_injection",
                "line": i + 1,
                "context": stripped[:120],
                "mechanism": "exec_concatenation",
            })
        elif re.search(r'child_process.*exec\s*\(', line):
            smells.append({
                "type": "command_injection",
                "line": i + 1,
                "context": stripped[:120],
                "mechanism": "child_process_exec",
            })
    return smells


def detect_xss(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect XSS via innerHTML, document.write, dangerouslySetInnerHTML."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        if re.search(r'\.innerHTML\s*=', line):
            if re.search(r'\.innerHTML\s*=\s*["\']', line):
                continue  # Static string literal
            smells.append({
                "type": "xss",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "innerHTML",
            })
        elif re.search(r'document\.write\s*\(', line):
            smells.append({
                "type": "xss",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "document_write",
            })
        elif re.search(r'dangerouslySetInnerHTML', line):
            smells.append({
                "type": "xss",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "dangerouslySetInnerHTML",
            })
    return smells


# ── High Security + Bug Detectors ────────────────────────────────────

def detect_eval_usage(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect eval() and Function() constructor usage."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        if re.search(r'\beval\s*\(', line):
            smells.append({
                "type": "eval_usage",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "eval",
            })
        elif re.search(r'\bnew\s+Function\s*\(', line):
            smells.append({
                "type": "eval_usage",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "Function_constructor",
            })
    return smells


def detect_insecure_random(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect Math.random() for security-sensitive operations."""
    smells = []
    for i, line in enumerate(lines):
        if re.search(r'Math\.random\s*\(', line):
            context = "\n".join(lines[max(0, i - 5):min(len(lines), i + 5)])
            if re.search(r'(?:token|password|key|secret|session|auth|salt|nonce|otp|uuid|id)', context, re.IGNORECASE):
                smells.append({
                    "type": "insecure_random",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "recommendation": "Use crypto.randomUUID() or crypto.getRandomValues()",
                })
    return smells


def detect_prototype_pollution(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect prototype pollution via __proto__ or Object.assign with user input."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        if re.search(r'__proto__', line):
            smells.append({
                "type": "prototype_pollution",
                "line": i + 1,
                "context": stripped[:120],
                "pattern": "__proto__",
            })
    return smells


def detect_exception_swallowing(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect empty catch blocks."""
    smells = []
    for i, line in enumerate(lines):
        if re.search(r'\bcatch\s*\(', line):
            brace_depth = 0
            found_opening = False
            catch_body_lines = []

            for j in range(i, min(len(lines), i + 20)):
                if '{' in lines[j]:
                    found_opening = True
                    brace_depth += lines[j].count('{')
                if '}' in lines[j]:
                    brace_depth -= lines[j].count('}')
                if found_opening:
                    catch_body_lines.append(lines[j])
                if found_opening and brace_depth == 0:
                    break

            non_empty = [
                l.strip() for l in catch_body_lines
                if l.strip() and not l.strip().startswith("//")
                   and l.strip() not in ['{', '}']
            ]
            if len(non_empty) == 0:
                smells.append({
                    "type": "exception_swallowing",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "pattern": "empty_catch",
                })
    return smells


def detect_unhandled_promise(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect promise chains without .catch() or missing await in try/catch."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        # .then() without .catch()
        if re.search(r'\.then\s*\(', line) and not re.search(r'\.catch\s*\(', line):
            # Check next few lines for .catch
            lookahead = "\n".join(lines[i:min(len(lines), i + 5)])
            if not re.search(r'\.catch\s*\(', lookahead):
                smells.append({
                    "type": "unhandled_promise",
                    "line": i + 1,
                    "context": stripped[:120],
                    "pattern": "then_without_catch",
                })
    return smells


# ── Medium Quality Detectors ─────────────────────────────────────────

def detect_god_functions(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect functions exceeding 100 lines."""
    smells = []
    # Match function declarations, arrow functions, and method definitions
    func_pattern = re.compile(
        r'^\s*(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[^=])\s*=>)'
    )
    method_pattern = re.compile(
        r'^\s*(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{'
    )

    for i, line in enumerate(lines):
        m = func_pattern.match(line) or method_pattern.match(line)
        if m:
            name = m.group(1) or (m.group(2) if m.lastindex and m.lastindex >= 2 else None) or "anonymous"
            # Find end by counting braces
            brace_depth = 0
            found_opening = False
            end_line = i

            for j in range(i, len(lines)):
                brace_depth += lines[j].count('{') - lines[j].count('}')
                if '{' in lines[j]:
                    found_opening = True
                if found_opening and brace_depth == 0:
                    end_line = j
                    break

            length = end_line - i + 1
            if length > 100:
                smells.append({
                    "type": "god_method",
                    "line": i + 1,
                    "context": f"Function {name} is {length} lines",
                    "method_name": name,
                    "length": length,
                })
    return smells


def detect_deep_nesting(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect deep brace nesting (>4 levels)."""
    smells = []
    max_reported = 0
    brace_depth = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        brace_depth += line.count('{') - line.count('}')
        if brace_depth > 4 and brace_depth > max_reported:
            max_reported = brace_depth
            smells.append({
                "type": "deep_nesting",
                "line": i + 1,
                "context": f"Nesting depth: {brace_depth}",
                "depth": brace_depth,
            })
        if brace_depth <= 1:
            max_reported = 0

    return smells


def detect_long_parameter_list(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect functions with more than 5 parameters."""
    smells = []
    func_pattern = re.compile(
        r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(|(\w+)\s*\()\s*([^)]*)\)'
    )

    for i, line in enumerate(lines):
        m = func_pattern.search(line)
        if m:
            name = m.group(1) or m.group(2) or m.group(3) or "anonymous"
            params_str = m.group(4).strip()
            if not params_str:
                continue
            params = [p.strip() for p in params_str.split(",") if p.strip()]
            if len(params) > 5:
                smells.append({
                    "type": "long_parameter_list",
                    "line": i + 1,
                    "context": f"Function {name} has {len(params)} parameters",
                    "method_name": name,
                    "param_count": len(params),
                })
    return smells


def detect_console_log(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect console.log left in production code."""
    # Skip test files
    basename = os.path.basename(path).lower()
    if any(t in basename for t in ['test', 'spec', '.test.', '.spec.']):
        return []

    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        if re.search(r'\bconsole\.(?:log|warn|error|debug|info)\s*\(', line):
            smells.append({
                "type": "console_log",
                "line": i + 1,
                "context": stripped[:120],
            })
    return smells


# ── Low Style Detectors ──────────────────────────────────────────────

def detect_var_usage(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect var declarations (should use let/const)."""
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        if re.match(r'\bvar\s+', stripped):
            smells.append({
                "type": "var_usage",
                "line": i + 1,
                "context": stripped[:120],
                "recommendation": "Use let or const instead of var",
            })
    return smells


def detect_any_type(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect explicit 'any' type annotations in TypeScript."""
    if not path.endswith((".ts", ".tsx")):
        return []
    smells = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        if re.search(r':\s*any\b', line):
            smells.append({
                "type": "any_type",
                "line": i + 1,
                "context": stripped[:120],
                "recommendation": "Use a specific type instead of any",
            })
    return smells


# ── JS/TS Detector Registry ─────────────────────────────────────────

JAVASCRIPT_DETECTORS = [
    # Critical -- Security
    create_detector("hardcoded_secret",          detect_hardcoded_secrets,          "critical", "security"),
    create_detector("sql_injection",             detect_sql_injection,              "critical", "security"),
    create_detector("command_injection",         detect_command_injection,          "critical", "security"),
    create_detector("xss",                       detect_xss,                       "critical", "security"),
    # High -- Security + Bugs
    create_detector("eval_usage",                detect_eval_usage,                "high",    "security"),
    create_detector("insecure_random",           detect_insecure_random,           "high",    "security"),
    create_detector("prototype_pollution",       detect_prototype_pollution,       "high",    "security"),
    create_detector("exception_swallowing",      detect_exception_swallowing,      "high",    "bug"),
    create_detector("unhandled_promise",         detect_unhandled_promise,         "high",    "bug"),
    # Medium -- Code Quality
    create_detector("god_method",                detect_god_functions,             "medium",  "quality"),
    create_detector("deep_nesting",              detect_deep_nesting,              "medium",  "quality"),
    create_detector("long_parameter_list",       detect_long_parameter_list,       "medium",  "quality"),
    create_detector("console_log",               detect_console_log,              "medium",  "quality"),
    # Low -- Style
    create_detector("var_usage",                 detect_var_usage,                 "low",     "style"),
    create_detector("any_type",                  detect_any_type,                  "low",     "style"),
]
