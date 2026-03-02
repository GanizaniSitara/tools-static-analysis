# Security and Code Quality Detectors

## Overview

`2_scan_smells.py` contains 19 detectors organized into four severity tiers and five
categories. Each detector scans C# source files line-by-line using regex pattern matching
with context-aware false positive suppression.

### Severity Tiers

| Tier | Weight | Detectors | Purpose |
|------|--------|-----------|---------|
| Critical | 15 | 4 | Security vulnerabilities that must be fixed |
| High | 8 | 6 | Security issues + bug patterns |
| Medium | 3 | 6 | Code quality + cross-technology concerns |
| Low | 1 | 3 | Style and hygiene |

### Categories

| Category | What it covers |
|----------|---------------|
| `security` | OWASP-aligned vulnerability detection |
| `bug` | Patterns that cause runtime failures |
| `quality` | Maintainability and complexity issues |
| `interop` | Cross-technology boundary risks |
| `style` | Code hygiene and conventions |

### Severity Filtering

The `--level` flag controls which tiers run. Each level includes all tiers above it:

- `--level critical`: Security only (4 detectors)
- `--level high`: Critical + High (10 detectors) -- **default**
- `--level medium`: High + Medium (16 detectors)
- `--level low`: All 19 detectors

---

## Critical Severity -- Security

### hardcoded_secret

**What it detects**: Hardcoded passwords, API keys, secrets, and connection strings
assigned as string literals in C# source.

**Pattern**: Variable names matching `password|passwd|pwd|apikey|api_key|secret|secretkey|
secret_key|connectionstring|access_key|token|auth_token|private_key` with a string value
of 8+ characters.

**False positive suppression**:

| Filter | What it excludes | Why |
|--------|-----------------|-----|
| Test files | Files with `test`, `spec`, `mock`, `fake`, `stub`, `sample` in the name | Test data is not production secrets |
| Dev config | `appsettings.development` files | Development placeholders |
| Placeholders | Values containing `{...}`, `<...>`, `${...}`, `your_`, `example`, `placeholder`, `changeme`, `xxx`, `todo`, `replace` | Template values, not real secrets |
| Key-name values | Values that are themselves key names: `password`, `pwd`, `token`, `connectionstring`, `data source`, etc. | Constants used for parsing (e.g., `const string PASSWORD = "password"` in a connection string parser) |
| Sanitizer methods | Findings inside methods named `Remove/Mask/Redact/Strip/Sanitize/Hide/Clear/Blank/Replace/Obfuscate` + `Password/Secret/Credential/Sensitive/Connection` | Code that removes or masks secrets, not stores them |
| Comments | Lines starting with `//`, `/*`, `*` | Code comments |

**Real-world example of false positive eliminated**:
```csharp
// This was flagged before -- RemovePassword blanks the password from
// an in-memory connection string. It doesn't store secrets.
public static string RemovePassword(string connectionString)
{
    const string PWD = "pwd";           // key name, not a secret
    const string PASSWORD = "password"; // key name, not a secret
    ...
}
```

The detector now skips this because (a) `"password"` is a key-name value, and (b) the
enclosing method `RemovePassword` matches the sanitizer pattern.

---

### sql_injection

**What it detects**: String concatenation or interpolation used to build SQL queries.

**Pattern**: Lines containing SQL keywords (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `EXEC`,
`EXECUTE`, `DROP`, `ALTER`) combined with string concatenation (`"..." + variable`) or
string interpolation (`$"...{variable}..."`).

**False positive suppression**:

| Filter | What it excludes | Why |
|--------|-----------------|-----|
| Parameterized queries | Lines with `@param`, `.Parameters`, `.AddWithValue` | Already using safe parameterization |
| EF Core safe methods | `FromSqlRaw`, `FromSqlInterpolated` calls | EF Core handles parameterization |
| Comments | Lines starting with `//`, `/*`, `*` | Code comments |

---

### insecure_deserialization

**What it detects**: Use of known-dangerous deserializers that can execute arbitrary code.

**Dangerous types flagged**:
- `BinaryFormatter` -- [CA2300/CA2301](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2300)
- `SoapFormatter` -- Same class of vulnerability
- `NetDataContractSerializer` -- Type-name based deserialization
- `LosFormatter` -- Legacy ASP.NET formatter
- `TypeNameHandling` set to `All`, `Auto`, `Objects`, or `Arrays` (Newtonsoft.Json)

**False positive suppression**: `TypeNameHandling` is only flagged if not set to `None`.

---

### command_injection

**What it detects**: `Process.Start` or `ProcessStartInfo` with dynamically constructed
arguments (string concatenation or interpolation).

**Pattern**: Process API call on the same line as `+` concatenation or `$"...{...}"` interpolation.

---

## High Severity -- Security

### weak_crypto

**What it detects**: Weak cryptographic algorithms: MD5, SHA1, DES, TripleDES, RC2.

**Context-aware detection** (added to address ArmorCode comparison feedback):

| Algorithm | Detection Rule |
|-----------|---------------|
| DES, TripleDES, RC2 | **Always flagged** -- these are symmetric ciphers with no legitimate non-security use case |
| MD5, SHA1 | **Context-dependent** -- examines 5 lines before and after the usage |

For MD5/SHA1, the detector checks surrounding context:

| Context Found | Result | Rationale |
|--------------|--------|-----------|
| Security keywords (`password`, `token`, `sign`, `verify`, `encrypt`, `cert`, `hmac`, `auth`, `nonce`, `salt`) | **Flagged** | Weak hash in security context is a vulnerability |
| Non-security keywords (`checksum`, `etag`, `cache`, `fingerprint`, `dedup`, `GetMd5Hash`, `CalcHash`) | **Suppressed** | MD5 for content hashing is acceptable |
| Neither | **Flagged** (ambiguous) | Triage system lets user mark as `accepted_risk` |

**Real-world example of false positive eliminated**:
```csharp
// MD5 used for string hashing (cache keys) -- NOT a security issue
public static string GetMd5Hash(string input)
{
    using var md5 = MD5.Create();  // was flagged, now suppressed
    byte[] data = md5.ComputeHash(Encoding.UTF8.GetBytes(input));
    return BitConverter.ToString(data).Replace("-", "");
}
```

---

### open_redirect

**What it detects**: `Redirect()` calls where user-controlled input (`returnUrl`,
`redirectUrl`, `Request.*`) flows into the redirect target.

**Suppressed** if `LocalRedirect()` or `Url.IsLocalUrl()` validation is present.

---

### xss

**What it detects**: Three cross-site scripting vectors:

1. `Html.Raw()` with non-static input (should use HtmlEncoder)
2. `Response.Write()` with non-static input
3. `[HttpPost/Put/Delete]` actions missing `[ValidateAntiForgeryToken]`

**Suppressed** if the argument is a static string literal (e.g., `Html.Raw("<br>")`).

---

### insecure_random

**What it detects**: `new Random()` used in security-sensitive contexts.

**Context-aware**: Only flags if surrounding 5 lines contain security keywords
(`token`, `password`, `secret`, `key`, `nonce`, `salt`, `otp`, `auth`, `crypto`, `session`).
Non-security usage (game logic, UI randomization) is not flagged.

---

### exception_swallowing

**What it detects**: Empty or TODO-only catch blocks that silently swallow exceptions.

**How it works**: After finding `catch (...)`, scans up to 20 lines for the closing brace.
Flags if the catch body contains zero meaningful statements (whitespace, braces, and
single TODO comments don't count).

---

### sync_over_async

**What it detects**: Three sync-over-async anti-patterns:
- `.Result` -- synchronous wait on a Task
- `.Wait()` -- synchronous wait on a Task
- `.GetAwaiter().GetResult()` -- synchronous unwrap

These patterns risk deadlocks in ASP.NET and UI thread contexts.

---

## Medium Severity -- Code Quality

### god_method

**What it detects**: Methods exceeding 100 lines. Calculates method length by tracking
brace depth from the method signature to the matching closing brace.

---

### deep_nesting

**What it detects**: Methods with nesting depth exceeding 4 levels. Tracks maximum brace
depth within each method body.

---

### long_parameter_list

**What it detects**: Methods with more than 5 parameters. Handles multi-line parameter
lists by collecting lines until the closing parenthesis.

---

### precision_unsafe_math

**What it detects**: `float` or `double` variables used near financial keywords (`price`,
`amount`, `value`, `rate`, `margin`, `pnl`, `profit`, `loss`, `cost`, `premium`, `strike`,
`notional`). These should typically use `decimal` for precision.

**Context-aware**: Only flags if financial keywords appear within 3 lines.

---

### deep_inheritance

**What it detects**: Classes with more than 3 base types/interfaces. Counts the
comma-separated items after the `:` in a class declaration.

---

### python_call (Interop)

**What it detects**: C# code invoking Python through four mechanisms:

| Mechanism | Pattern |
|-----------|---------|
| Process execution | `Process.Start("python")`, `FileName = "python3.exe"` |
| Python.NET | `using Python.Runtime`, `PythonEngine`, `PyObject`, `Py.GIL` |
| IronPython | `IronPython`, `Microsoft.Scripting`, `Python.CreateRuntime` |
| Script file references | String literals containing `.py` files (only if process context nearby) |

---

## Low Severity -- Style

### magic_number

**What it detects**: Hardcoded numeric literals in logic (conditions, returns, arithmetic).

**Excluded numbers**: 0, 1, -1, 2, 10, 100, 1000, 60, 24, 365, 1024, 0.0, 1.0, 0.5, 2.0
(common time/size/boolean constants).

**Excluded contexts**: const declarations, enum values, attributes, switch cases, test
assertions, collection initializers, simple variable declarations.

---

### missing_null_check

**What it detects**: Public method parameters (reference types) without null validation
in the first 10 lines of the method body.

**Excluded types**: Value types (`int`, `long`, `bool`, `DateTime`, `decimal`, `double`,
`float`, `byte`, `char`, `short`, `Guid`, `TimeSpan`, `DateTimeOffset`, `CancellationToken`).

**Excluded if**: Parameter has `[NotNull]`, `[Required]`, or `[NonNull]` annotations.

---

### mutable_shared_state

**What it detects**: Static non-readonly, non-const fields (potential thread-safety issues).

**Excluded types**: Thread-safe types (`ILogger`, `IOptions`, `IConfiguration`,
`IServiceProvider`, `IMemoryCache`, `ConcurrentDictionary`, `ConcurrentBag`,
`ConcurrentQueue`, `ConcurrentStack`, `ImmutableArray`, `ImmutableList`,
`ImmutableDictionary`, `Lazy`).

---

## File Exclusions

Before any detector runs, the scanner excludes files matching:

| Pattern | What it skips |
|---------|--------------|
| `*.Designer.cs`, `*.generated.cs`, `AssemblyInfo.cs` | Auto-generated code |
| `obj/`, `bin/`, `node_modules/`, `packages/` | Build output and dependencies |
| `Migrations/` | EF Core migrations (auto-generated) |
| Files < 50 lines | Too small to contain meaningful findings |
| Files > 2 MB | Likely generated or binary-like |

---

## LLM Prompt Templates

Every detector has a corresponding prompt template in `SMELL_PROMPTS`. These are used by
the viewer's Claude Code integration -- clicking the "Claude" button on a finding passes
the prompt with `{file}`, `{line}`, `{context}`, and `{project}` substituted.

Each prompt:
1. Names the specific finding type
2. Provides file/line/context
3. Instructs the LLM to evaluate ONLY this specific finding
4. Lists 3-4 numbered investigation/fix steps
5. Ends with "Show the minimal code change needed -- do not refactor surrounding code"

This keeps AI-assisted reviews focused and avoids scope creep into unrelated code.

---

## Scoring

Projects are ranked by a refactoring value score:

```
score = (complexity_score * 2)
      + weighted_smell_score
      + (fan_in * fan_out) * 0.5
      + test_gap_penalty * 5
      - deprioritize_discount
```

Where `weighted_smell_score` sums severity weights per finding:
- Critical: 15 points each
- High: 8 points each
- Medium: 3 points each
- Low: 1 point each

This means a single critical security finding (15 pts) outweighs five low-severity style
issues (5 pts), focusing attention where it matters most.
