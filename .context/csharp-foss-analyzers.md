# FOSS C# Static Analysis Tools

## Official Microsoft Tools

### 1. Roslyn Analyzers (Built into .NET SDK)
- **License:** MIT
- **What:** Official C# compiler platform with extensible analyzers
- **Requires:** .NET SDK installed
- **Rules:** 100+ code quality & security rules
- **Usage:**
  ```bash
  dotnet build /p:RunAnalyzers=true /p:EnforceCodeStyleInBuild=true
  ```

### 2. FxCop Analyzers (now .NET Code Analysis)
- **License:** MIT
- **What:** Microsoft's official code quality analyzers
- **Included in:** .NET 5+ SDK
- **Categories:** Design, Performance, Security, Reliability
- **Docs:** https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview

## Third-Party FOSS

### 3. Roslynator ⭐ Most Popular
- **License:** Apache 2.0
- **Rules:** 500+ analyzers & refactorings
- **GitHub:** https://github.com/dotnet/roslynator
- **Install:** `dotnet tool install -g roslynator.dotnet.cli`
- **Usage:**
  ```bash
  roslynator analyze Solution.sln --output roslynator.json
  ```

### 4. SonarAnalyzer.CSharp
- **License:** LGPL v3
- **Rules:** 600+ quality & security rules
- **GitHub:** https://github.com/SonarSource/sonar-dotnet
- **Integrates with:** SonarQube, SonarCloud

### 5. SecurityCodeScan
- **License:** LGPL 3.0
- **Focus:** Security vulnerabilities (SQL injection, XSS, crypto issues)
- **GitHub:** https://github.com/security-code-scan/security-code-scan
- **Rules:** 30+ security-specific analyzers
- **Integration:** Works as Roslyn analyzer or standalone

### 6. StyleCop.Analyzers
- **License:** Apache 2.0
- **Focus:** Code style & consistency
- **GitHub:** https://github.com/DotNetAnalyzers/StyleCopAnalyzers
- **Rules:** 200+ style rules

## Current Implementation vs FOSS Tools

### Our Custom Regex-Based Scanner (2_scan_smells.py)

**Pros:**
- ✅ **Zero dependencies** - pure Python stdlib
- ✅ **Cross-platform** - works without .NET SDK
- ✅ **Fast** - no compilation needed
- ✅ **Customizable** - easy to tweak patterns
- ✅ **Portable** - runs anywhere Python runs

**Cons:**
- ❌ **Limited accuracy** - regex can't do semantic analysis
- ❌ **Fewer rules** - 18 detectors vs 500+
- ❌ **No AST analysis** - can miss complex patterns
- ❌ **False positives** - pattern matching limitations

### Using Roslyn/Roslynator

**Pros:**
- ✅ **Accurate** - full Abstract Syntax Tree (AST) analysis
- ✅ **Comprehensive** - 500+ rules
- ✅ **Well-maintained** - Microsoft/community supported
- ✅ **Deep analysis** - understands code semantics
- ✅ **Industry standard** - used by Visual Studio, VS Code

**Cons:**
- ❌ **Requires .NET SDK** - users must install it
- ❌ **Slower** - needs to compile/analyze solutions
- ❌ **Platform dependency** - .NET runtime required
- ❌ **Integration complexity** - call .NET tools from Python

## Recommendation: Hybrid Approach

**Keep both approaches:**

1. **Baseline Scanner (always runs):** Our regex-based `2_scan_smells.py`
   - No dependencies required
   - Fast, lightweight scanning
   - Catches common issues

2. **Enhanced Scanner (optional):** Add Roslynator to `3_external_tools.py`
   - Runs if .NET SDK is installed
   - Comprehensive rule coverage
   - Deep semantic analysis

**Integration Example:**

```python
# In 3_external_tools.py, add:

def run_roslynator(repos_root: str) -> dict:
    """Run Roslynator analyzer if available."""
    if not shutil.which("roslynator"):
        return {"skipped": "roslynator not found"}

    findings = []
    for solution in glob.glob(f"{repos_root}/**/*.sln", recursive=True):
        result = subprocess.run(
            ["roslynator", "analyze", solution, "--output", "json"],
            capture_output=True,
            text=True
        )
        # Parse JSON output and convert to our format
        findings.extend(parse_roslynator_json(result.stdout))

    return {"findings": findings, "tool": "roslynator"}
```

This gives users the **best of both worlds:**
- Works out-of-the-box with no setup
- Enhanced analysis if they install .NET SDK + Roslynator

## Implementation Priority

1. **High:** Add Roslynator integration to 3_external_tools.py
2. **Medium:** Add SecurityCodeScan for security-focused analysis
3. **Low:** Consider SonarAnalyzer if users request SonarQube integration

## Resources

- Roslyn SDK: https://github.com/dotnet/roslyn
- Roslyn Analyzer Tutorial: https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/
- List of all .NET analyzers: https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/
