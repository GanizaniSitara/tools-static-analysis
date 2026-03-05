#!/usr/bin/env python3
"""Migration script to extract SMELL_PROMPTS from 2_scan_smells.py to YAML."""

import re
import yaml
from pathlib import Path

# Read 2_scan_smells.py and extract SMELL_PROMPTS
with open("2_scan_smells.py", "r") as f:
    content = f.read()

# Extract the SMELL_PROMPTS dictionary
match = re.search(r'SMELL_PROMPTS = \{(.*?)\n\}', content, re.DOTALL)
if not match:
    print("ERROR: Could not find SMELL_PROMPTS in 2_scan_smells.py")
    exit(1)

prompts_dict_str = "{" + match.group(1) + "\n}"

# Safely evaluate the dictionary (using exec since it contains multiline strings)
SMELL_PROMPTS = {}
exec(f"SMELL_PROMPTS = {prompts_dict_str}")

# Convert to YAML structure with base/csharp/java variants
yaml_structure = {
    "version": 1,
    "prompts": {}
}

# For each detector, create base prompt (from existing C# prompts)
# and add language-specific variants where syntax differs
for detector_name, base_prompt in SMELL_PROMPTS.items():
    yaml_structure["prompts"][detector_name] = {
        "base": base_prompt
    }

    # Add C#-specific prompts (same as base for now, but explicitly labeled)
    yaml_structure["prompts"][detector_name]["csharp"] = base_prompt

    # Add Java-specific prompts (modify C# prompts for Java syntax)
    java_prompt = base_prompt

    # Replace C#-specific syntax with Java equivalents
    replacements = {
        # SQL Injection
        "@param, SqlParameter, or EF Core interpolated SQL": "PreparedStatement with ? placeholders or JPA criteria queries",
        # Deserialization
        "BinaryFormatter, SoapFormatter, TypeNameHandling.All": "ObjectInputStream.readObject() without validation",
        "System.Text.Json, JsonSerializer with safe settings, or a custom binder": "Jackson with safe settings or custom deserializer",
        # Command Injection
        "Process.Start with string concatenation": "Runtime.exec() or ProcessBuilder with user input",
        "an argument array (no shell), input validation, or allowlisting": "ProcessBuilder with array arguments, input validation, or allowlisting",
        # Weak Crypto
        "MD5, SHA1, DES, TripleDES, RC2": "MD5, SHA1, DES",
        "SHA-256/SHA-512 (hashing), AES-256 (encryption), or PBKDF2/Argon2 (passwords)": "SHA-256/SHA-512 (hashing), AES-256 (encryption), or PBKDF2/BCrypt (passwords)",
        # Open Redirect
        "LocalRedirect(), add Url.IsLocalUrl() validation, or use an allowlist": "validation with startsWith() or URL whitelist checking",
        # XSS
        "Html.Raw with user input, Response.Write, or missing [ValidateAntiForgeryToken]": "PrintWriter.write() without encoding or missing CSRF protection",
        "encode via HtmlEncoder or use Razor's default encoding": "encode via StringEscapeUtils or use JSTL <c:out>",
        "add [ValidateAntiForgeryToken] to the POST action": "add CSRF token validation to POST endpoints",
        # Insecure Random
        "System.Random": "java.util.Random",
        "RandomNumberGenerator (System.Security.Cryptography)": "SecureRandom (java.security.SecureRandom)",
        # Exception Swallowing
        "ILogger, rethrow with throw;": "Logger, rethrow with throw",
        # Sync over Async
        ".Result, .Wait(), or .GetAwaiter().GetResult()": "CompletableFuture.get(), Future.get(), or .join()",
        "add async/await up the call chain": "use CompletableFuture composition or make method return Future",
        # God Methods
        "method exceeds 100 lines": "method exceeds 100 lines",
        # Deep Nesting
        "nesting depth": "nesting depth",
        # Long Parameter List
        "more than 5 parameters": "more than 5 parameters",
        # Precision Unsafe Math
        "float or double": "float or double",
        "decimal type": "BigDecimal",
        # Deep Inheritance
        "class implements >5 interfaces or extends >5 classes": "class implements >5 interfaces",
        # Python Calls
        "Process.Start.*python": "ProcessBuilder or Runtime.exec with python",
        # Magic Numbers
        "const or static readonly": "static final",
        # Missing Null Checks
        "ArgumentNullException or Guard.NotNull": "Objects.requireNonNull or validation",
        # Mutable Shared State
        "static mutable": "static mutable",
        "readonly": "final",
        "lock or Interlocked": "synchronized or java.util.concurrent.atomic",
    }

    for csharp_text, java_text in replacements.items():
        java_prompt = java_prompt.replace(csharp_text, java_text)

    yaml_structure["prompts"][detector_name]["java"] = java_prompt

# Write to YAML
output_path = Path("prompts/default_prompts.yaml")
with open(output_path, "w") as f:
    yaml.safe_dump(yaml_structure, f, default_flow_style=False, allow_unicode=True, width=120)

print(f"✓ Migrated {len(SMELL_PROMPTS)} prompts to {output_path}")
print(f"  Total prompt variants: {len(SMELL_PROMPTS) * 3} (base + csharp + java)")
