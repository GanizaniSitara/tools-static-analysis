"""C# code smell detectors for .NET projects."""

from __future__ import annotations
import os
import re
from pathlib import Path

from .base import create_detector

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
    # Values that are just key names / labels, not actual secrets
    keyname_pattern = re.compile(
        r'^(password|passwd|pwd|apikey|api_key|secret|secretkey|secret_key|connectionstring|'
        r'access_key|token|auth_token|private_key|username|user|host|server|database|port|'
        r'data source|initial catalog|integrated security|trusted_connection|'
        r'persist security info|multipleactiveresultsets|encrypt|trustservercertificate)$',
        re.IGNORECASE
    )
    # Methods that remove/mask/sanitize secrets — not storing them
    sanitizer_pattern = re.compile(
        r'\b(remove|strip|mask|redact|sanitize|hide|clear|blank|replace|obfuscate)\w*'
        r'(password|secret|credential|sensitive|connection)',
        re.IGNORECASE
    )
    # Detect if the file-level or method-level context is a sanitizer
    # Check the enclosing method name once per method scope
    method_sig_pattern = re.compile(
        r'\b(?:public|private|protected|internal|static)\s+\S+\s+(\w+)\s*\(',
    )

    # Build a line -> enclosing method name map (approximate)
    enclosing_method: dict[int, str] = {}
    current_method = ""
    brace_depth = 0
    for idx, ln in enumerate(lines):
        msig = method_sig_pattern.search(ln)
        if msig:
            current_method = msig.group(1)
        enclosing_method[idx] = current_method

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        for m in secret_pattern.finditer(line):
            value = m.group(2)
            if placeholder_pattern.search(value):
                continue
            # Skip if the "secret" value is just a key name (e.g. const string PASSWORD = "password")
            if keyname_pattern.match(value.strip()):
                continue
            # Skip if inside a method that removes/masks secrets
            method_name = enclosing_method.get(i, "")
            if method_name and sanitizer_pattern.search(method_name):
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
    """Detect use of weak cryptographic algorithms.

    MD5 and SHA1 are only flagged when used in a security-relevant context
    (passwords, signatures, tokens, certificates). Non-security uses like
    checksums, cache keys, ETags, and content hashing are not flagged.
    DES, TripleDES, and RC2 are always flagged (they are symmetric ciphers
    with no legitimate non-security use case).
    """
    smells = []
    # Symmetric ciphers — always weak, always flag
    always_weak = re.compile(r'\b(DES|TripleDES|RC2)\s*\.\s*Create\b')
    # Hash algorithms — weak only in security contexts
    weak_hash = re.compile(r'\b(MD5|SHA1)\s*\.\s*Create\b')
    # Method/variable names suggesting non-security hashing
    nonsecurity_context = re.compile(
        r'(checksum|HashString|content.?hash|cache.?key|etag|fingerprint|'
        r'dedup|bucket|GetMd5|CalcHash|file.?hash|Md5Hash)',
        re.IGNORECASE
    )
    # Method/variable names suggesting security usage
    security_context = re.compile(
        r'(password|credential|token|signature|sign|verify|cert|'
        r'hmac|encrypt|decrypt|auth|nonce|salt|pbkdf|derive.?key)',
        re.IGNORECASE
    )

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue

        # Always flag DES/TripleDES/RC2
        if always_weak.search(line):
            smells.append({
                "type": "weak_crypto",
                "line": i + 1,
                "context": stripped[:80],
            })
            continue

        # For MD5/SHA1, check surrounding context (5 lines before/after)
        if weak_hash.search(line):
            context_start = max(0, i - 5)
            context_end = min(len(lines), i + 6)
            context_text = "\n".join(lines[context_start:context_end])

            has_security = security_context.search(context_text)
            has_nonsecurity = nonsecurity_context.search(context_text)

            # Security context takes priority — always flag
            if has_security:
                smells.append({
                    "type": "weak_crypto",
                    "line": i + 1,
                    "context": stripped[:80],
                })
                continue
            # Clear non-security usage — skip
            if has_nonsecurity:
                continue
            # Ambiguous — flag but with lower confidence (still report it;
            # triage system lets users mark as accepted_risk if non-security)
            smells.append({
                "type": "weak_crypto",
                "line": i + 1,
                "context": stripped[:80],
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


# ─── Cross-Technology Call Detection ──────────────────────────────────

def detect_python_calls(path: str, content: str, lines: list[str]) -> list[dict]:
    """Detect C# code that invokes Python via process execution or interop libraries.

    Detects:
      - Process.Start / ProcessStartInfo launching python/python3
      - Python.NET (Python.Runtime, PythonEngine, PyObject, Py.GIL, using/import)
      - IronPython (IronPython.*, CreateEngine, Microsoft.Scripting)
      - Embedded script execution referencing .py files or python interpreters
    """
    smells = []

    # Pre-compiled patterns for efficiency
    # 1. Process-based invocation: Process.Start("python" ...) or FileName = "python"
    process_python = re.compile(
        r"""(?:Process\.Start|ProcessStartInfo)\s*\(?\s*["']python[3"]?["']"""
        r"""|FileName\s*=\s*["'](?:[^"']*[/\\])?python[3"]?(?:\.exe)?["']""",
        re.IGNORECASE,
    )

    # 2. Python.NET library usage
    pythonnet = re.compile(
        r"""\busing\s+Python\.Runtime\b"""
        r"""|\bPythonEngine\s*\."""
        r"""|\bPyObject\b"""
        r"""|\bPy\s*\.\s*GIL\b"""
        r"""|\bPyModule\b"""
        r"""|\bPyScope\b""",
    )

    # 3. IronPython
    ironpython = re.compile(
        r"""\bIronPython\b"""
        r"""|\bMicrosoft\.Scripting\b"""
        r"""|\bCreateEngine\s*\(\s*\)\s*.*[Pp]ython"""
        r"""|\bPython\.CreateRuntime\b""",
    )

    # 4. Generic script-engine invocation with a .py file reference
    # Matches .py at end of string or followed by space/quote (e.g., "script.py --args")
    py_script_ref = re.compile(
        r"""["'][^"']*\.py(?:\s|["'])""",
    )

    # Track which patterns we've already reported per line to avoid duplicates
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue

        mechanism = None

        if process_python.search(line):
            mechanism = "process_exec"
        elif pythonnet.search(line):
            mechanism = "python_net"
        elif ironpython.search(line):
            mechanism = "ironpython"
        elif py_script_ref.search(line):
            # Only flag .py file references if there's also a process/script context
            context_start = max(0, i - 5)
            context_end = min(len(lines), i + 6)
            nearby = ' '.join(lines[context_start:context_end])
            if re.search(r'\b(Process|Script|Execute|Run|Start|Invoke|Engine)\b', nearby):
                mechanism = "py_script_ref"

        if mechanism:
            smells.append({
                "type": "python_call",
                "line": i + 1,
                "context": line.strip()[:120],
                "mechanism": mechanism,
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
    # Medium — Interop / Cross-Technology
    {"name": "python_call",               "fn": detect_python_calls,              "severity": "medium",  "category": "interop"},
    # Low — Style/Noise
    {"name": "magic_number",              "fn": detect_magic_numbers,             "severity": "low",     "category": "style"},
    {"name": "missing_null_check",        "fn": detect_missing_null_checks,       "severity": "low",     "category": "style"},
    {"name": "mutable_shared_state",      "fn": detect_mutable_shared_state,      "severity": "low",     "category": "style"},
]


SEVERITY_WEIGHTS = {"critical": 15, "high": 8, "medium": 3, "low": 1}


# ─── C# Detector Registry ─────────────────────────────────────────────

CSHARP_DETECTORS = [
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
