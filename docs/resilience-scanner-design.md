# Resilience Scanner Design -- `6_scan_resilience.py`

## Purpose

Add a cross-cutting resilience analyzer that detects fault-tolerance gaps in .NET projects. Unlike `2_scan_smells.py` (which works per-file), this scanner correlates NuGet dependencies, DI registrations, and call sites across multiple files to produce a per-project resilience posture report.

## Pipeline Position

```
1_scan_projects.py  -->  2_scan_smells.py  -->  6_scan_resilience.py  -->  3_gen_diagrams.py  -->  4_gen_docs.py
                                                      ^
                                                      |
                                          Consumes: project-meta.json
                                                    data-sources.json
                                                    dependencies.csv
```

## What It Detects

### A. NuGet-Level Checks (from `dependencies.csv`)

| Check | Severity | Logic |
|-------|----------|-------|
| Missing Polly | high | Project has external calls in `data-sources.json` but no `Polly`, `Microsoft.Extensions.Http.Polly`, or `Microsoft.Extensions.Resilience` in `dependencies.csv` |
| Raw HttpClient | high | Project uses `new HttpClient()` (data-sources `HttpClient.New`) instead of IHttpClientFactory |
| No health checks | low | WebApp/Service project without `AspNetCore.Diagnostics.HealthChecks` or `Microsoft.Extensions.Diagnostics.HealthChecks` |

### B. DI/Startup Registration Checks (scan Startup.cs, Program.cs)

| Check | Severity | Logic |
|-------|----------|-------|
| AddHttpClient without policy | high | `AddHttpClient<T>()` without chained `.AddPolicyHandler` / `.AddTransientHttpErrorPolicy` / `.AddStandardResilienceHandler` (look forward 15 lines for fluent chaining) |
| Missing Polly v8 registration | medium | No `AddResiliencePipeline` / `AddResilienceHandler` in .NET 8+ projects |

### C. Call-Site Checks (scan .cs files)

| Detector Function | Severity | What It Finds |
|-------------------|----------|---------------|
| `detect_missing_cancellation_token` | high | `GetAsync`/`PostAsync`/`SaveChangesAsync`/`QueryAsync` etc. without `CancellationToken` in same statement (check current line + next 2 lines) |
| `detect_missing_timeout` | high | `new HttpClient()` without `.Timeout` set in next 10 lines |
| `detect_httpclient_no_policy` | high | `AddHttpClient<` in DI files without policy handler in next 15 lines |
| `detect_fire_and_forget` | medium | `_ = SomeAsync()` or unassigned `Task.Run()` without await |
| `detect_catch_all_no_retry` | medium | `catch (Exception)` within 20 lines of an external call, without retry keywords in catch body |
| `detect_connection_no_dispose` | medium | `new SqlConnection/HttpClient/NpgsqlConnection` not in `using` block |
| `detect_global_httpclient` | medium | `static [readonly] HttpClient` fields (DNS caching issue) |
| `detect_retry_without_backoff` | medium | `for/while` loop with retry/attempt variable, no `Task.Delay`/`Thread.Sleep`/`TimeSpan` in body |
| `detect_hardcoded_timeout` | low | `TimeSpan.FromSeconds(N)` in timeout context with literal number |

### D. Positive Patterns Detected (what IS in place)

| Pattern | Regex | Category Key |
|---------|-------|-------------|
| Polly retry | `\.RetryAsync\(` / `.WaitAndRetryAsync\(` / `RetryPolicy` | `retry` |
| Circuit breaker | `\.CircuitBreakerAsync\(` / `CircuitBreakerPolicy` | `circuitBreaker` |
| Timeout policy | `\.TimeoutAsync\(` / `TimeoutPolicy` | `timeout` |
| Bulkhead | `\.BulkheadAsync\(` / `BulkheadPolicy` | `bulkhead` |
| Fallback | `\.FallbackAsync\(` / `FallbackPolicy` | `fallback` |
| CancellationToken | `CancellationToken\s+\w+` in signatures | `cancellationToken` |
| Health checks | `IHealthCheck` / `AddHealthChecks` / `MapHealthChecks` | `healthCheck` |
| HttpClientFactory | `IHttpClientFactory` / `services.AddHttpClient` | `httpClientFactory` |
| Rate limiting | `RateLimiter` / `AddRateLimiter` | `rateLimiting` |
| Polly v8 | `AddResilienceHandler` / `ResiliencePipelineBuilder` / `AddStandardResilienceHandler` | `resiliencePipeline` |
| Policy handler | `AddPolicyHandler` / `AddTransientHttpErrorPolicy` | `policyHandler` |

## Detector Function Signatures

All detectors follow the same pattern as `2_scan_smells.py`:

```python
def detect_xyz(path: str, content: str, lines: list[str]) -> list[dict]:
    """Returns list of findings."""
    # Each finding: {"type": "detector_name", "line": N, "context": "code snippet"}
    # Severity and category are added by the registry loop.
```

## Detector Registry

```python
RESILIENCE_DETECTORS = [
    {"name": "missing_cancellation_token", "fn": detect_missing_cancellation_token, "severity": "high",   "category": "resilience"},
    {"name": "missing_timeout",            "fn": detect_missing_timeout,            "severity": "high",   "category": "resilience"},
    {"name": "httpclient_no_policy",       "fn": detect_httpclient_no_policy,       "severity": "high",   "category": "resilience"},
    {"name": "fire_and_forget",            "fn": detect_fire_and_forget,            "severity": "medium", "category": "resilience"},
    {"name": "catch_all_no_retry",         "fn": detect_catch_all_no_retry,         "severity": "medium", "category": "resilience"},
    {"name": "connection_no_dispose",      "fn": detect_connection_no_dispose,      "severity": "medium", "category": "resilience"},
    {"name": "global_httpclient",          "fn": detect_global_httpclient,          "severity": "medium", "category": "resilience"},
    {"name": "retry_without_backoff",      "fn": detect_retry_without_backoff,      "severity": "medium", "category": "resilience"},
    {"name": "hardcoded_timeout",          "fn": detect_hardcoded_timeout,          "severity": "low",    "category": "resilience"},
]
```

## Resilience Scoring (per project)

```python
def compute_resilience_score(external_call_count, positive_patterns, findings, has_polly, has_health, has_http_factory):
    if external_call_count == 0:
        return 100.0  # nothing to protect

    # Base: ratio of positive patterns to external calls (0-60 points)
    protection_count = sum(positive_patterns.values())
    score = min(1.0, protection_count / max(1, external_call_count)) * 60

    # Bonuses (up to 40 points)
    if has_polly:           score += 15
    if has_http_factory:    score += 10
    if has_health:          score += 5
    if cancellationToken:   score += 5
    if circuitBreaker:      score += 5

    # Penalties
    for finding in findings:
        if finding.severity == "high":   score -= 5
        if finding.severity == "medium": score -= 2
        if finding.severity == "low":    score -= 1

    return clamp(0, 100, score)
```

Color coding: green (>70), yellow (40-70), red (<40).

## Output: `resilience-findings.json`

```json
{
  "generated": "2026-02-26",
  "scanRoot": "/path/to/repos",
  "summary": {
    "totalProjects": 45,
    "projectsWithExternalCalls": 18,
    "projectsWithPolly": 5,
    "avgResilienceScore": 34.2,
    "totalFindings": 156,
    "findingsBySeverity": {"high": 45, "medium": 78, "low": 33},
    "findingsByType": {"missing_cancellation_token": 45, "httpclient_no_policy": 12, "...": "..."}
  },
  "projects": [
    {
      "project": "Ordering.API",
      "repo": "eShop",
      "category": "WebApp",
      "layer": "Service",
      "resilienceScore": 67.0,
      "externalCallCount": 12,
      "protectedCallCount": 8,
      "pollyPackages": ["Polly", "Microsoft.Extensions.Http.Polly"],
      "resiliencePatterns": {
        "retry": 3, "circuitBreaker": 1, "timeout": 0,
        "bulkhead": 0, "fallback": 0, "cancellationToken": 8,
        "healthCheck": 1, "httpClientFactory": 1, "rateLimiting": 0
      },
      "externalCallsByType": {"api": 8, "database": 3, "messaging": 1},
      "findings": [
        {
          "type": "missing_cancellation_token",
          "severity": "high",
          "file": "Services/CatalogService.cs",
          "line": 42,
          "context": "await _httpClient.GetAsync(url);",
          "suggestion": "Pass CancellationToken to enable caller-driven timeout/cancellation"
        }
      ],
      "findingCount": 5,
      "policySummary": {"retry": true, "circuitBreaker": false, "timeout": true, "bulkhead": false, "fallback": false}
    }
  ],
  "resiliencePrompts": {
    "missing_cancellation_token": "RESILIENCE FINDING: Async external call without CancellationToken.\nFile: {file} (line {line})\n...",
    "...": "..."
  }
}
```

Projects are sorted by `resilienceScore` ascending (worst first).

## Output: `resilience-report.md`

Human-readable markdown with:
- Executive summary (total projects, external calls, Polly adoption, avg score)
- Findings by severity and type
- Table: all projects ranked by resilience score
- Top 20 detailed analysis with findings per project

## LLM Prompt Templates (`RESILIENCE_PROMPTS`)

One per detector type, same `{file}`, `{line}`, `{context}`, `{project}` pattern as `SMELL_PROMPTS` in `2_scan_smells.py`. Each prompt:
- Names the specific finding
- Provides file/line/context
- Says "Evaluate ONLY this finding. Do NOT review the rest of the file."
- Gives 3-4 numbered fix steps
- Ends with "Show the minimal code change needed -- do not refactor surrounding code."

Template keys: `missing_cancellation_token`, `missing_timeout`, `httpclient_no_policy`, `fire_and_forget`, `catch_all_no_retry`, `connection_no_dispose`, `global_httpclient`, `retry_without_backoff`, `hardcoded_timeout`, `missing_polly`, `missing_health_checks`.

## Script Structure

```
6_scan_resilience.py (~700-900 lines)

# ─── Config / CLI ───
#   argparse: scan_root, out_dir (same pattern as 2_scan_smells.py)

# ─── Path Utilities ───
#   _strip_long_prefix, _fs_path, _normalize_path, _relpath, safe_read_text
#   (copied from 2_scan_smells.py lines 84-140)

# ─── File Discovery ───
#   find_cs_files (copied from 2_scan_smells.py lines 149-186)

# ─── Load Existing Analysis ───
#   load_json(path, default)
#   load_dependencies(out_dir) -> {project: set(packages)}  -- reads dependencies.csv
#   load_data_sources(out_dir) -> {project: [findings]}     -- reads data-sources.json
#   load_project_meta(out_dir) -> [projects]                -- reads project-meta.json
#   find_project_for_file / infer_project_from_path         -- (from 2_scan_smells.py)

# ─── Positive Pattern Detection ───
#   POSITIVE_PATTERNS list of {name, regex, category}
#   scan_positive_patterns(content) -> {category: count}

# ─── Weakness Detectors ───
#   _RE_ASYNC_HTTP_CALL, _RE_ASYNC_DB_CALL (compiled regexes)
#   detect_missing_cancellation_token(path, content, lines)
#   detect_missing_timeout(path, content, lines)
#   detect_httpclient_no_policy(path, content, lines)
#   detect_fire_and_forget(path, content, lines)
#   detect_catch_all_no_retry(path, content, lines)
#   detect_connection_no_dispose(path, content, lines)
#   detect_global_httpclient(path, content, lines)
#   detect_retry_without_backoff(path, content, lines)
#   detect_hardcoded_timeout(path, content, lines)

# ─── Detector Registry ───
#   RESILIENCE_DETECTORS = [{name, fn, severity, category}, ...]
#   SEVERITY_WEIGHTS = {critical: 15, high: 8, medium: 3, low: 1}

# ─── LLM Prompt Templates ───
#   RESILIENCE_PROMPTS = {type: template_string, ...}

# ─── NuGet Cross-Reference ───
#   check_nuget_resilience(project, packages, data_sources, category)
#     -> findings for missing_polly, missing_health_checks

# ─── File Analysis ───
#   analyze_file_resilience(filepath, scan_root)
#     -> {path, lines, findings, positivePatterns}

# ─── Scoring ───
#   compute_resilience_score(external_call_count, positive_patterns, findings, ...)

# ─── Main Analysis ───
#   analyze_all(scan_root, out_dir) -> full result dict

# ─── Output ───
#   generate_markdown_report(data, output_path)
#   save_json_output(data, output_path)

# ─── Entry Point ───
#   main() -> load, analyze, output, print summary
```

## Integration Points

### `run.py` (1 line addition after line 559)

```python
# After step 2 (scan smells), before step 3 (diagrams):
print("\n--- Scanning resilience ---")
run("6_scan_resilience.py", repos, out)
```

### `4_gen_docs.py` -- Resilience tab in viewer.html

1. **Load JSON** (~line 94): `resilience_data = _load_json(os.path.join(OUT_DIR, "resilience-findings.json"), {})`
2. **Register tab** (~line 895): `if resilience_data.get("projects"): all_tab_ids.append(("resilience", "Resilience"))`
3. **Embed JSON**: `window._resilienceData = {resilience_embedded};`
4. **Panel HTML**: Summary cards + sortable table (Project | Score | External Calls | Protected | Findings | Top Issue) + expandable detail rows
5. **JS IIFE**: Render function following the Code Quality tab pattern (~line 3886)

## Reusable Code from Existing Scripts

| Function | Source | Lines |
|----------|--------|-------|
| `_strip_long_prefix` | `2_scan_smells.py` | 84-90 |
| `_fs_path` | `2_scan_smells.py` | 93-105 |
| `_normalize_path` | `2_scan_smells.py` | 108-115 |
| `_relpath` | `2_scan_smells.py` | 118-125 |
| `safe_read_text` | `2_scan_smells.py` | 128-140 |
| `find_cs_files` | `2_scan_smells.py` | 149-186 |
| `load_json` | `2_scan_smells.py` | 1238-1246 |
| `find_project_for_file` | `2_scan_smells.py` | 1300-1332 |
| `infer_project_from_path` | `2_scan_smells.py` | 1335-1369 |
| `save_json_output` | `2_scan_smells.py` | 1652-1665 |

## Verification Checklist

1. Run full pipeline on eShop, StockSharp, OrchardCore
2. Verify `resilience-findings.json` written with sensible data
3. Verify `resilience-report.md` is readable
4. Verify viewer.html Resilience tab renders: extract `<script>` blocks, `node --check`
5. No regressions in existing tabs
6. Unit tests still pass: `python3 -m unittest test_scan_projects test_scan_smells`
