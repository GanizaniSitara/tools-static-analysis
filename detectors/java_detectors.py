"""Java code smell detectors for Java projects."""

from __future__ import annotations
import os
import re
from pathlib import Path

from .base import create_detector

# ─── Critical Security Detectors ──────────────────────────────────────

def detect_hardcoded_secrets(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect hardcoded passwords, API keys, and connection strings in Java code."""
    smells = []

    # Patterns for hardcoded secrets
    patterns = [
        # Password assignments
        (r'(?:password|passwd|pwd)\s*=\s*"([^"]{8,})"', "password"),
        (r"(?:password|passwd|pwd)\s*=\s*'([^']{8,})'", "password"),
        # API keys and tokens
        (r'(?:api_?key|apikey|token|secret)\s*=\s*"([^"]{16,})"', "api_key"),
        (r"(?:api_?key|apikey|token|secret)\s*=\s*'([^']{16,})'", "api_key"),
        # Connection strings with credentials
        (r'jdbc:(?:mysql|postgresql|oracle|sqlserver)://[^:]+:[^@]+@', "connection_string"),
        # AWS/cloud credentials
        (r'(?:aws|azure|gcp).*(?:key|secret|token)\s*=\s*"[A-Za-z0-9+/]{20,}"', "cloud_credential"),
    ]

    for i, line in enumerate(lines):
        # Skip comments
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        for pattern, secret_type in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Filter false positives
                # Skip if it's a constant name (e.g., private static final String PASSWORD = "password")
                if re.search(r'(?:private|public|protected)\s+static\s+final\s+\w+\s+\w+\s*=\s*"(?:password|key|token)"', line, re.IGNORECASE):
                    continue
                # Skip if it's clearly a placeholder or example
                if re.search(r'(?:example|placeholder|test|demo|sample)', line, re.IGNORECASE):
                    continue
                # Skip if value is too short or generic
                if re.search(r'=\s*"(?:password|12345|admin|test|null|empty)"\s*', line, re.IGNORECASE):
                    continue

                smells.append({
                    "type": "hardcoded_secret",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "secret_type": secret_type,
                })
                break  # Only report once per line

    return smells


def detect_sql_injection(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect SQL injection via string concatenation in Java."""
    smells = []

    for i, line in enumerate(lines):
        # Skip comments
        if line.strip().startswith("//") or line.strip().startswith("/*"):
            continue

        # Check for string concatenation in SQL contexts
        # Pattern: executeQuery( ... + var + ... )
        if re.search(r'\b(?:executeQuery|executeUpdate|execute|createQuery)\s*\([^)]*\+', line):
            # Exclude safe patterns
            if "PreparedStatement" in content[max(0, i-10):min(len(content), i+10)]:
                # If PreparedStatement is nearby, it's likely safe
                continue
            if re.search(r'\.setString\(|\.setInt\(|\.setLong\(', content):
                # If parameterized queries are used, likely safe
                continue

            smells.append({
                "type": "sql_injection",
                "line": i + 1,
                "context": line.strip()[:120],
                "pattern": "string_concatenation",
            })
        # Direct Statement usage (not PreparedStatement)
        elif re.search(r'\bStatement\s+\w+\s*=', line) and "PreparedStatement" not in line:
            smells.append({
                "type": "sql_injection",
                "line": i + 1,
                "context": line.strip()[:120],
                "pattern": "raw_statement",
            })

    return smells


def detect_insecure_deserialization(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect insecure deserialization via ObjectInputStream.readObject()."""
    smells = []

    for i, line in enumerate(lines):
        # Look for readObject() calls
        if "readObject()" in line or "ObjectInputStream" in line:
            # Check if there's validation nearby (instanceof check)
            context_start = max(0, i - 5)
            context_end = min(len(lines), i + 10)
            context_lines = lines[context_start:context_end]
            context_text = "\n".join(context_lines)

            # If there's an instanceof check nearby, it's likely safe
            if re.search(r'\binstanceof\b', context_text):
                continue
            # If there's a whitelist check, likely safe
            if re.search(r'(?:whitelist|allowed|valid).*class', context_text, re.IGNORECASE):
                continue

            if "readObject()" in line:
                smells.append({
                    "type": "insecure_deserialization",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "pattern": "readObject_without_validation",
                })
            elif "new ObjectInputStream" in line:
                smells.append({
                    "type": "insecure_deserialization",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "pattern": "ObjectInputStream_usage",
                })

    return smells


def detect_command_injection(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect command injection via Runtime.exec() or ProcessBuilder."""
    smells = []

    for i, line in enumerate(lines):
        # Skip comments
        if line.strip().startswith("//") or line.strip().startswith("/*"):
            continue

        # Runtime.exec() with string concatenation or variables
        if re.search(r'Runtime\.getRuntime\(\)\.exec\s*\(', line):
            # Check if it uses variables or concatenation
            if "+" in line or re.search(r'exec\s*\(\s*\w+', line):
                # Filter: if command is from a hardcoded enum or validated list, it's safer
                context = "\n".join(lines[max(0, i-10):min(len(lines), i+5)])
                if re.search(r'(?:enum|switch|case)\s+\w+', context):
                    continue

                smells.append({
                    "type": "command_injection",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "mechanism": "Runtime.exec",
                })

        # ProcessBuilder with variables
        elif re.search(r'new ProcessBuilder\s*\([^)]*\w+', line):
            # If it's a variable (not a string literal), check for validation
            if re.search(r'new ProcessBuilder\s*\(\s*"[^"]+"\s*\)', line):
                # Pure string literal, likely safe
                continue

            smells.append({
                "type": "command_injection",
                "line": i + 1,
                "context": line.strip()[:120],
                "mechanism": "ProcessBuilder",
            })

        # ProcessBuilder.command() with concatenation
        elif re.search(r'\.command\s*\([^)]*\+', line):
            smells.append({
                "type": "command_injection",
                "line": i + 1,
                "context": line.strip()[:120],
                "mechanism": "ProcessBuilder.command",
            })

    return smells


# ─── High Security + Bug Detectors ────────────────────────────────────

def detect_weak_crypto(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect weak cryptographic algorithms (MD5, SHA1, DES)."""
    smells = []

    weak_algos = {
        "MD5": r'\b(?:MD5|MessageDigest\.getInstance\s*\(\s*"MD5"\s*\))',
        "SHA1": r'\b(?:SHA-?1|MessageDigest\.getInstance\s*\(\s*"SHA-?1"\s*\))',
        "DES": r'\b(?:DES|Cipher\.getInstance\s*\(\s*"DES)',
    }

    for i, line in enumerate(lines):
        # Skip comments
        if line.strip().startswith("//") or line.strip().startswith("/*"):
            continue

        for algo, pattern in weak_algos.items():
            if re.search(pattern, line):
                # Context-aware: check if it's used for security or just checksums
                context_start = max(0, i - 10)
                context_end = min(len(lines), i + 10)
                context_text = "\n".join(lines[context_start:context_end])

                # If it's clearly for file integrity/checksum, less critical
                if re.search(r'(?:checksum|hash|digest|integrity|etag|fingerprint)', context_text, re.IGNORECASE):
                    # Still report but note it's for integrity, not encryption
                    pass

                # If it's for password hashing or encryption, critical
                is_security_context = re.search(r'(?:password|encrypt|decrypt|key|token|auth|secret)', context_text, re.IGNORECASE)

                smells.append({
                    "type": "weak_crypto",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "algorithm": algo,
                    "security_context": is_security_context is not None,
                })
                break

    return smells


def detect_open_redirect(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect open redirect via response.sendRedirect() with user input."""
    smells = []

    for i, line in enumerate(lines):
        if "sendRedirect(" in line:
            # Check if the parameter is a variable (not a string literal)
            if re.search(r'sendRedirect\s*\(\s*"[^"]+"\s*\)', line):
                # Pure string literal, likely safe
                continue

            # Check if there's validation nearby
            context = "\n".join(lines[max(0, i-10):min(len(lines), i+5)])
            if re.search(r'(?:startsWith|contains|matches|whitelist)', context):
                # Some validation present, less risky
                continue

            smells.append({
                "type": "open_redirect",
                "line": i + 1,
                "context": line.strip()[:120],
                "pattern": "sendRedirect_with_variable",
            })

    return smells


def detect_xss(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect XSS via PrintWriter.write() without escaping."""
    smells = []

    for i, line in enumerate(lines):
        # Look for PrintWriter output methods
        if re.search(r'\.(?:write|print|println)\s*\([^)]*\w+', line):
            # Check if it's writing user input
            context = "\n".join(lines[max(0, i-10):min(len(lines), i+5)])

            # Look for escaping/encoding nearby
            if re.search(r'(?:escape|encode|sanitize|HTMLUtils|StringEscapeUtils)', context, re.IGNORECASE):
                continue

            # Check if it's writing a variable (potential user input)
            if re.search(r'\.(?:write|print|println)\s*\(\s*"[^"]*"\s*\)', line):
                # Pure string literal, likely safe
                continue

            smells.append({
                "type": "xss",
                "line": i + 1,
                "context": line.strip()[:120],
                "pattern": "unescaped_output",
            })

    return smells


def detect_insecure_random(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect java.util.Random usage for security-critical operations."""
    smells = []

    for i, line in enumerate(lines):
        if re.search(r'\bnew Random\s*\(', line) or re.search(r'Random\s+\w+\s*=', line):
            # Check context for security usage
            context = "\n".join(lines[max(0, i-10):min(len(lines), i+10)])

            # If it's used for security tokens, passwords, keys, etc., it's critical
            is_security = re.search(r'(?:token|password|key|secret|session|auth|salt|nonce)', context, re.IGNORECASE)

            if is_security:
                smells.append({
                    "type": "insecure_random",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "recommendation": "Use SecureRandom instead",
                })

    return smells


def detect_exception_swallowing(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect catch blocks with empty body or just comments."""
    smells = []

    for i, line in enumerate(lines):
        if re.search(r'\bcatch\s*\(', line):
            # Find the catch block body
            start = i
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

            # Check if body is empty or only comments
            non_empty_lines = [
                l.strip() for l in catch_body_lines
                if l.strip() and not l.strip().startswith("//")
                   and not l.strip().startswith("/*")
                   and not l.strip().startswith("*")
                   and l.strip() not in ['{', '}']
            ]

            if len(non_empty_lines) == 0:
                smells.append({
                    "type": "exception_swallowing",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "pattern": "empty_catch",
                })

    return smells


def detect_sync_over_async(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect sync-over-async patterns (blocking on async operations)."""
    smells = []

    for i, line in enumerate(lines):
        # CompletableFuture.get() - blocks the thread
        if re.search(r'CompletableFuture.*\.get\s*\(', line):
            smells.append({
                "type": "sync_over_async",
                "line": i + 1,
                "context": line.strip()[:120],
                "pattern": "CompletableFuture.get",
            })
        # Future.get() without timeout
        elif re.search(r'Future<.*>.*\.get\s*\(\s*\)', line):
            smells.append({
                "type": "sync_over_async",
                "line": i + 1,
                "context": line.strip()[:120],
                "pattern": "Future.get_without_timeout",
            })
        # .join() on CompletableFuture
        elif re.search(r'CompletableFuture.*\.join\s*\(', line):
            smells.append({
                "type": "sync_over_async",
                "line": i + 1,
                "context": line.strip()[:120],
                "pattern": "CompletableFuture.join",
            })

    return smells


# ─── Medium Quality Detectors ─────────────────────────────────────────

def detect_god_methods(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect methods exceeding 100 lines."""
    smells = []

    # Pattern for Java method signatures
    method_pattern = r'^\s*(?:public|private|protected|static|final|synchronized|native|abstract)+\s+(?:[\w<>[\]]+\s+)+(\w+)\s*\('

    for i, line in enumerate(lines):
        match = re.search(method_pattern, line)
        if match:
            method_name = match.group(1)
            start_line = i + 1

            # Find the end of the method (approximate by counting braces)
            brace_depth = 0
            found_opening = False
            end_line = start_line

            for j in range(i, len(lines)):
                if '{' in lines[j]:
                    found_opening = True
                    brace_depth += lines[j].count('{')
                if '}' in lines[j]:
                    brace_depth -= lines[j].count('}')
                    if found_opening and brace_depth == 0:
                        end_line = j + 1
                        break

            method_length = end_line - start_line
            if method_length > 100:
                smells.append({
                    "type": "god_method",
                    "line": start_line,
                    "context": f"Method {method_name} is {method_length} lines",
                    "method_name": method_name,
                    "length": method_length,
                })

    return smells


def detect_deep_nesting(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect deep nesting (>4 levels) within methods."""
    smells = []

    current_depth = 0
    max_depth_in_method = 0
    method_start_line = 0
    in_method = False

    for i, line in enumerate(lines):
        # Detect method start
        if re.search(r'^\s*(?:public|private|protected|static|final|synchronized)+\s+(?:[\w<>[\]]+\s+)+\w+\s*\(', line):
            in_method = True
            method_start_line = i + 1
            current_depth = 0
            max_depth_in_method = 0

        if in_method:
            # Count braces
            current_depth += line.count('{') - line.count('}')
            max_depth_in_method = max(max_depth_in_method, current_depth)

            # Method ended
            if current_depth <= 0 and '{' in lines[method_start_line - 1:i + 1]:
                in_method = False
                if max_depth_in_method > 4:
                    smells.append({
                        "type": "deep_nesting",
                        "line": method_start_line,
                        "context": f"Nesting depth: {max_depth_in_method}",
                        "depth": max_depth_in_method,
                    })

    return smells


def detect_long_parameter_list(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect methods with more than 5 parameters."""
    smells = []

    # Pattern for method signatures
    method_pattern = r'^\s*(?:public|private|protected|static|final|synchronized)+\s+(?:[\w<>[\]]+\s+)+(\w+)\s*\(([^)]*)\)'

    for i, line in enumerate(lines):
        match = re.search(method_pattern, line)
        if match:
            method_name = match.group(1)
            params = match.group(2).strip()

            if params:
                # Count parameters (split by comma, but be careful with generics)
                # Simple heuristic: count commas that aren't inside angle brackets
                param_count = 1
                in_generics = 0
                for char in params:
                    if char == '<':
                        in_generics += 1
                    elif char == '>':
                        in_generics -= 1
                    elif char == ',' and in_generics == 0:
                        param_count += 1

                if param_count > 5:
                    smells.append({
                        "type": "long_parameter_list",
                        "line": i + 1,
                        "context": f"Method {method_name} has {param_count} parameters",
                        "method_name": method_name,
                        "param_count": param_count,
                    })

    return smells


def detect_precision_unsafe_math(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect float/double usage in financial calculations."""
    smells = []

    # Check if file is financial domain
    is_financial = any(re.search(r'(?:price|money|currency|payment|amount|balance|financial)', content, re.IGNORECASE))

    if not is_financial:
        return smells

    for i, line in enumerate(lines):
        # float or double variable declarations in financial context
        if re.search(r'\b(?:float|double)\s+\w+(?:Price|Amount|Balance|Total|Cost|Fee)', line, re.IGNORECASE):
            smells.append({
                "type": "precision_unsafe_math",
                "line": i + 1,
                "context": line.strip()[:120],
                "recommendation": "Use BigDecimal for financial calculations",
            })
        # Arithmetic operations on float/double in financial methods
        elif re.search(r'(?:float|double)\s+\w+\s*=.*[\+\-\*/]', line):
            context = "\n".join(lines[max(0, i-5):min(len(lines), i+5)])
            if re.search(r'(?:price|money|currency|payment|amount)', context, re.IGNORECASE):
                smells.append({
                    "type": "precision_unsafe_math",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "recommendation": "Use BigDecimal for financial calculations",
                })

    return smells


def detect_deep_inheritance(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect classes implementing more than 5 interfaces."""
    smells = []

    for i, line in enumerate(lines):
        # Match class declarations with implements clause
        match = re.search(r'class\s+(\w+).*\bimplements\s+([^{]+)', line)
        if match:
            class_name = match.group(1)
            implements_clause = match.group(2).strip()

            # Count interfaces (split by comma, handle generics)
            interface_count = 1
            in_generics = 0
            for char in implements_clause:
                if char == '<':
                    in_generics += 1
                elif char == '>':
                    in_generics -= 1
                elif char == ',' and in_generics == 0:
                    interface_count += 1

            if interface_count > 5:
                smells.append({
                    "type": "deep_inheritance",
                    "line": i + 1,
                    "context": f"Class {class_name} implements {interface_count} interfaces",
                    "class_name": class_name,
                    "interface_count": interface_count,
                })

    return smells


# ─── Low Style Detectors ──────────────────────────────────────────────

def detect_python_calls(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect Java code calling Python scripts via ProcessBuilder."""
    smells = []

    for i, line in enumerate(lines):
        # Look for ProcessBuilder with python/python3
        if re.search(r'ProcessBuilder.*(?:python|python3|py)', line, re.IGNORECASE):
            mechanism = "ProcessBuilder"
        elif re.search(r'Runtime.*exec.*(?:python|python3|py)', line, re.IGNORECASE):
            mechanism = "Runtime.exec"
        else:
            continue

        smells.append({
            "type": "python_call",
            "line": i + 1,
            "context": line.strip()[:120],
            "mechanism": mechanism,
        })

    return smells


def detect_magic_numbers(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect hardcoded numeric literals (excluding common constants)."""
    smells = []

    # Exclude common values
    exclude_values = {0, 1, -1, 2, 10, 100, 1000, 24, 60, 365}

    for i, line in enumerate(lines):
        # Skip comments and strings
        if line.strip().startswith("//") or line.strip().startswith("/*"):
            continue

        # Find numeric literals (not in strings)
        # Pattern: numbers not preceded by " or '
        matches = re.finditer(r'(?<!["\'])\b(\d+(?:\.\d+)?)\b(?!["\'])', line)

        for match in matches:
            try:
                value = float(match.group(1))
                if value in exclude_values:
                    continue
                # Skip if it's part of a constant declaration
                if re.search(r'(?:static\s+)?final\s+', line):
                    continue
                # Skip if in array/collection initialization
                if re.search(r'[{\[]', line[:match.start()]):
                    continue

                smells.append({
                    "type": "magic_number",
                    "line": i + 1,
                    "context": line.strip()[:120],
                    "value": value,
                })
            except ValueError:
                pass

    return smells


def detect_missing_null_checks(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect public methods without null validation on parameters."""
    smells = []

    # Find public method signatures
    method_pattern = r'^\s*public\s+(?:static\s+)?[\w<>[\]]+\s+(\w+)\s*\(([^)]+)\)'

    for i, line in enumerate(lines):
        match = re.search(method_pattern, line)
        if match:
            method_name = match.group(1)
            params = match.group(2).strip()

            if not params or params == "":
                continue

            # Check method body for null checks
            # Look ahead 10 lines for Objects.requireNonNull or if (param == null)
            check_lines = lines[i+1:min(len(lines), i+15)]
            check_text = "\n".join(check_lines)

            has_null_check = re.search(r'(?:requireNonNull|== null|!= null|Objects\.isNull|@NotNull|@Nonnull)', check_text)

            if not has_null_check:
                # Extract parameter names
                param_names = []
                for p in params.split(','):
                    parts = p.strip().split()
                    if len(parts) >= 2:
                        param_names.append(parts[-1])

                if param_names:
                    smells.append({
                        "type": "missing_null_check",
                        "line": i + 1,
                        "context": f"Public method {method_name} may need null checks",
                        "method_name": method_name,
                        "parameters": param_names,
                    })

    return smells


def detect_mutable_shared_state(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect static mutable fields without synchronization."""
    smells = []

    for i, line in enumerate(lines):
        # Look for static non-final fields
        if re.search(r'\bstatic\s+(?!final\b)\w+', line):
            # Check if it's a collection or array (mutable)
            if re.search(r'(?:List|Set|Map|HashMap|ArrayList|HashSet|array|\[\])', line):
                # Check for synchronization nearby
                context = "\n".join(lines[max(0, i-5):min(len(lines), i+10)])
                has_sync = re.search(r'(?:synchronized|volatile|Atomic|Concurrent)', context)

                if not has_sync:
                    smells.append({
                        "type": "mutable_shared_state",
                        "line": i + 1,
                        "context": line.strip()[:120],
                        "recommendation": "Consider making final or adding synchronization",
                    })

    return smells


# ─── Java Detector Registry ───────────────────────────────────────────

JAVA_DETECTORS = [
    # Critical — Security
    create_detector("hardcoded_secret",          detect_hardcoded_secrets,          "critical", "security"),
    create_detector("sql_injection",             detect_sql_injection,              "critical", "security"),
    create_detector("insecure_deserialization",  detect_insecure_deserialization,   "critical", "security"),
    create_detector("command_injection",         detect_command_injection,          "critical", "security"),
    # High — Security + Bugs
    create_detector("weak_crypto",               detect_weak_crypto,               "high",    "security"),
    create_detector("open_redirect",             detect_open_redirect,             "high",    "security"),
    create_detector("xss",                       detect_xss,                       "high",    "security"),
    create_detector("insecure_random",           detect_insecure_random,           "high",    "security"),
    create_detector("exception_swallowing",      detect_exception_swallowing,      "high",    "bug"),
    create_detector("sync_over_async",           detect_sync_over_async,           "high",    "bug"),
    # Medium — Code Quality
    create_detector("god_method",                detect_god_methods,               "medium",  "quality"),
    create_detector("deep_nesting",              detect_deep_nesting,              "medium",  "quality"),
    create_detector("long_parameter_list",       detect_long_parameter_list,       "medium",  "quality"),
    create_detector("precision_unsafe_math",     detect_precision_unsafe_math,     "medium",  "quality"),
    create_detector("deep_inheritance",          detect_deep_inheritance,          "medium",  "quality"),
    # Medium — Interop / Cross-Technology
    create_detector("python_call",               detect_python_calls,              "medium",  "interop"),
    # Low — Style/Noise
    create_detector("magic_number",              detect_magic_numbers,             "low",     "style"),
    create_detector("missing_null_check",        detect_missing_null_checks,       "low",     "style"),
    create_detector("mutable_shared_state",      detect_mutable_shared_state,      "low",     "style"),
]
