#!/usr/bin/env python3
"""
Resilience Scanner -- Cross-Cutting Fault-Tolerance Analysis

Scans .NET C# source files to identify resilience gaps:
  - Missing retry policies on external calls (HTTP, DB, messaging)
  - Missing timeouts and CancellationToken propagation
  - Missing circuit breakers, bulkheads, rate limiting
  - Fire-and-forget async calls, unprotected connections
  - Cross-references NuGet dependencies + data-source patterns + source code

Consumes output from 1_scan_projects.py:
  - project-meta.json, data-sources.json, dependencies.csv

Usage:
  python 6_scan_resilience.py /path/to/repos [output-dir]

Outputs:
  - resilience-findings.json (machine-readable)
  - resilience-report.md (human-readable)
"""

import argparse
import csv
import json
import os
import platform
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Resilience Scanner")
parser.add_argument("scan_root", help="Directory containing repos to scan")
parser.add_argument("out_dir", nargs="?", default="output", help="Output directory")
_args = parser.parse_args()

SCAN_ROOT = os.path.abspath(_args.scan_root)
OUT_DIR = os.path.abspath(_args.out_dir)

_MAX_FILE_SIZE = 2 * 1024 * 1024
_MAX_SCAN_DEPTH = 30
_PROGRESS_INTERVAL = 500

EXCLUDE_PATTERNS = [
    r"\.(Designer|generated|AssemblyInfo)\.cs$",
    r"[\\/](obj|bin|node_modules|packages)[\\/]",
    r"[\\/]Migrations[\\/]",
]

SKIP_DIRS = {".git", "node_modules", "bin", "obj", ".vs", ".idea", "packages",
             "TestResults", "artifacts", "__pycache__", ".nuget"}

RESILIENCE_PACKAGES = {
    "polly", "polly.core", "polly.extensions.http",
    "microsoft.extensions.http.polly",
    "microsoft.extensions.resilience",
    "microsoft.extensions.http.resilience",
    "polly.contrib.waitandretry", "polly.contrib.simmy",
}
HEALTH_CHECK_PACKAGES = {
    "microsoft.extensions.diagnostics.healthchecks",
    "aspnetcore.diagnostics.healthchecks",
    "aspnetcore.healthchecks.ui",
    "microsoft.extensions.diagnostics.healthchecks.abstractions",
}
HTTP_FACTORY_PACKAGES = {"microsoft.extensions.http"}
EXTERNAL_CALL_TYPES = {"api", "database", "messaging", "cache"}


# ─── Path Utilities ──────────────────────────────────────────────────

def _strip_long_prefix(p: str) -> str:
    if p.startswith("\\\\?\\UNC\\"):
        return "\\\\" + p[8:]
    if p.startswith("\\\\?\\"):
        return p[4:]
    return p


def _fs_path(p: str) -> str:
    if sys.platform == "win32":
        abs_p = os.path.abspath(p)
        if len(abs_p) >= 260 and not abs_p.startswith("\\\\?\\"):
            if abs_p.startswith("\\\\"):
                return "\\\\?\\UNC\\" + abs_p[2:]
            return "\\\\?\\" + abs_p
    return os.path.normpath(p) if p else p


def _normalize_path(p: str) -> str:
    if not p:
        return p
    cleaned = _strip_long_prefix(p)
    if os.path.isabs(cleaned):
        return os.path.normpath(cleaned)
    return os.path.normpath(os.path.abspath(cleaned))


def _relpath(path: str, start: str) -> str:
    clean_path = _strip_long_prefix(os.path.normpath(path))
    clean_start = _strip_long_prefix(os.path.normpath(start))
    try:
        return os.path.relpath(clean_path, clean_start)
    except ValueError:
        return clean_path


def safe_read_text(filepath: str, max_size: int = _MAX_FILE_SIZE) -> str | None:
    norm_path = _fs_path(filepath)
    try:
        if Path(norm_path).stat().st_size > max_size:
            return None
    except OSError:
        return None
    try:
        return Path(norm_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


# ─── File Discovery ──────────────────────────────────────────────────

def find_cs_files(directory: str, results: list | None = None, _depth: int = 0) -> list[str]:
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
            if not any(re.search(pat, full) for pat in EXCLUDE_PATTERNS):
                results.append(full)
    return results


# ─── Load Existing Analysis Data ─────────────────────────────────────

def load_json(path: str, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        if default is None:
            print(f"  Warning: could not load {path}: {exc}")
            return {}
        return default


def load_dependencies(out_dir: str) -> dict[str, set[str]]:
    """Load dependencies.csv into {project: set(lowercase_package_names)}."""
    result: dict[str, set[str]] = defaultdict(set)
    csv_path = os.path.join(out_dir, "dependencies.csv")
    if not os.path.isfile(csv_path):
        print("  Warning: dependencies.csv not found")
        return result
    try:
        with open(csv_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                proj = row.get("project", "")
                pkg = row.get("package", "")
                if proj and pkg:
                    result[proj].add(pkg.lower())
    except (OSError, csv.Error) as exc:
        print(f"  Warning: could not load dependencies.csv: {exc}")
    return result


def load_data_sources(out_dir: str) -> dict[str, list[dict]]:
    """Load data-sources.json grouped by project."""
    result: dict[str, list[dict]] = defaultdict(list)
    raw = load_json(os.path.join(out_dir, "data-sources.json"), [])
    items = raw if isinstance(raw, list) else raw.get("findings", raw.get("patterns", []))
    for finding in items:
        proj = finding.get("project", "")
        ds_type = finding.get("type", "")
        if proj and ds_type in EXTERNAL_CALL_TYPES:
            result[proj].append(finding)
    return result


def find_project_for_file(filepath: str, project_meta: list, scan_root: str) -> str | None:
    filepath = _normalize_path(filepath)
    for pm in sorted(project_meta, key=lambda p: len(p.get("globalPath") or p.get("path", "")), reverse=True):
        proj_path = pm.get("globalPath") or pm.get("path", "")
        if not proj_path:
            continue
        if not os.path.isabs(proj_path):
            proj_path = os.path.join(scan_root, proj_path)
        proj_dir = os.path.dirname(_normalize_path(proj_path))
        try:
            if not _relpath(filepath, proj_dir).startswith(".."):
                return pm.get("project")
        except ValueError:
            continue
    return None


def infer_project_from_path(filepath: str, scan_root: str) -> str:
    norm_path = _normalize_path(filepath)
    norm_root = _normalize_path(scan_root)
    current = os.path.dirname(norm_path)
    while current and current != norm_root and len(current) >= len(norm_root):
        try:
            for entry in os.scandir(_fs_path(current)):
                if entry.name.endswith(".csproj") and entry.is_file():
                    return os.path.splitext(entry.name)[0]
        except OSError:
            pass
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    try:
        parts = _relpath(filepath, scan_root).replace("\\", "/").split("/")
        if len(parts) > 1:
            return parts[0]
    except ValueError:
        pass
    return "_unknown"


# ─── Positive Resilience Pattern Detection ────────────────────────────

POSITIVE_PATTERNS = [
    {"name": "polly_retry",           "regex": re.compile(r'\.RetryAsync\s*\(|\.WaitAndRetryAsync\s*\(|\.Retry\s*\(|RetryPolicy|AddRetryPolicy'),           "category": "retry"},
    {"name": "polly_circuit_breaker", "regex": re.compile(r'\.CircuitBreakerAsync\s*\(|\.AdvancedCircuitBreakerAsync\s*\(|CircuitBreakerPolicy'),             "category": "circuitBreaker"},
    {"name": "polly_timeout",         "regex": re.compile(r'\.TimeoutAsync\s*\(|TimeoutPolicy|Policy\.Timeout'),                                             "category": "timeout"},
    {"name": "polly_bulkhead",        "regex": re.compile(r'\.BulkheadAsync\s*\(|BulkheadPolicy'),                                                           "category": "bulkhead"},
    {"name": "polly_fallback",        "regex": re.compile(r'\.FallbackAsync\s*\(|FallbackPolicy'),                                                           "category": "fallback"},
    {"name": "cancellation_token",    "regex": re.compile(r'CancellationToken\s+\w+'),                                                                       "category": "cancellationToken"},
    {"name": "health_check",          "regex": re.compile(r'IHealthCheck\b|\.MapHealthChecks\s*\(|\.AddHealthChecks\s*\('),                                   "category": "healthCheck"},
    {"name": "http_client_factory",   "regex": re.compile(r'IHttpClientFactory\b|services\.AddHttpClient|builder\.Services\.AddHttpClient'),                  "category": "httpClientFactory"},
    {"name": "rate_limiting",         "regex": re.compile(r'RateLimiter\b|TokenBucketRateLimiter|FixedWindowRateLimiter|SlidingWindowRateLimiter|\.AddRateLimiter\s*\('), "category": "rateLimiting"},
    {"name": "polly_v8_resilience",   "regex": re.compile(r'\.AddResilienceHandler\s*\(|ResiliencePipelineBuilder\b|\.AddResiliencePipeline\s*\(|\.AddStandardResilienceHandler\s*\('), "category": "resiliencePipeline"},
    {"name": "policy_handler",        "regex": re.compile(r'\.AddPolicyHandler\s*\(|\.AddTransientHttpErrorPolicy\s*\('),                                     "category": "policyHandler"},
]


def scan_positive_patterns(content: str) -> dict[str, int]:
    """Count resilience patterns present in a file."""
    counts: dict[str, int] = {}
    for pat in POSITIVE_PATTERNS:
        n = len(pat["regex"].findall(content))
        if n:
            counts[pat["category"]] = counts.get(pat["category"], 0) + n
    return counts


# ─── Resilience Weakness Detectors ────────────────────────────────────

_RE_ASYNC_HTTP = re.compile(
    r'\.\s*(GetAsync|PostAsync|PutAsync|DeleteAsync|SendAsync|'
    r'GetStringAsync|GetStreamAsync|GetByteArrayAsync|'
    r'PostAsJsonAsync|PutAsJsonAsync|PatchAsync)\s*\('
)
_RE_ASYNC_DB = re.compile(
    r'\.\s*(SaveChangesAsync|ExecuteAsync|QueryAsync|'
    r'QueryFirstAsync|QuerySingleAsync|QueryMultipleAsync|'
    r'ExecuteScalarAsync|ExecuteReaderAsync|'
    r'FindAsync|ToListAsync|FirstOrDefaultAsync|'
    r'SingleOrDefaultAsync|AnyAsync|CountAsync)\s*\('
)


def _is_comment(line: str) -> bool:
    s = line.strip()
    return s.startswith("//") or s.startswith("/*") or s.startswith("*")


def detect_missing_cancellation_token(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if _RE_ASYNC_HTTP.search(line) or _RE_ASYNC_DB.search(line):
            window = "\n".join(lines[i:min(i + 3, len(lines))])
            if "CancellationToken" not in window and "cancellationToken" not in window:
                findings.append({"type": "missing_cancellation_token", "line": i + 1,
                                 "context": line.strip()[:200]})
    return findings


def detect_missing_timeout(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if re.search(r'new\s+HttpClient\s*\(', line):
            scope = "\n".join(lines[i:min(i + 10, len(lines))])
            if ".Timeout" not in scope and "TimeoutPolicy" not in scope:
                findings.append({"type": "missing_timeout", "line": i + 1,
                                 "context": line.strip()[:200]})
    return findings


def detect_httpclient_no_policy(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    basename = os.path.basename(path).lower()
    is_di_file = any(kw in basename for kw in [
        "startup", "program", "serviceregistration", "diregistration",
        "serviceextension", "dependencyinjection", "hostbuilder",
        "serviceconfig", "servicecollection",
    ])
    if not is_di_file and "AddHttpClient" not in content:
        return findings
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if re.search(r'\.AddHttpClient\s*[<(]', line):
            scope = "\n".join(lines[i:min(i + 15, len(lines))])
            if not any(p in scope for p in [
                "AddPolicyHandler", "AddTransientHttpErrorPolicy",
                "AddStandardResilienceHandler", "AddResilienceHandler",
            ]):
                findings.append({"type": "httpclient_no_policy", "line": i + 1,
                                 "context": line.strip()[:200]})
    return findings


def detect_fire_and_forget(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if re.search(r'_\s*=\s*\w+.*Async\s*\(', line):
            findings.append({"type": "fire_and_forget", "line": i + 1,
                             "context": line.strip()[:200]})
        elif re.search(r'(?<!await\s)Task\.Run\s*\(', line) and "await" not in line:
            if not re.search(r'(var|Task|=)\s+\w+\s*=\s*Task\.Run', line):
                findings.append({"type": "fire_and_forget", "line": i + 1,
                                 "context": line.strip()[:200]})
    return findings


def detect_catch_all_no_retry(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if re.search(r'catch\s*\(\s*Exception\b', line):
            pre = "\n".join(lines[max(0, i - 20):i])
            has_ext = bool(_RE_ASYNC_HTTP.search(pre) or _RE_ASYNC_DB.search(pre)
                           or re.search(r'HttpClient|SqlConnection|IDbConnection', pre))
            if has_ext:
                post = "\n".join(lines[i:min(i + 10, len(lines))])
                if not any(kw in post for kw in ["retry", "Retry", "attempt", "backoff",
                                                  "Backoff", "Polly", "policy", "Policy"]):
                    findings.append({"type": "catch_all_no_retry", "line": i + 1,
                                     "context": line.strip()[:200]})
    return findings


def detect_connection_no_dispose(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if re.search(r'new\s+(SqlConnection|HttpClient|NpgsqlConnection|MySqlConnection)\s*\(', line):
            prev = lines[i - 1].strip() if i > 0 else ""
            if "using" not in line and "using" not in prev:
                findings.append({"type": "connection_no_dispose", "line": i + 1,
                                 "context": line.strip()[:200]})
    return findings


def detect_global_httpclient(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if re.search(r'static\s+(?:readonly\s+)?HttpClient\s+\w+', line):
            findings.append({"type": "global_httpclient", "line": i + 1,
                             "context": line.strip()[:200]})
    return findings


def detect_retry_without_backoff(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if re.search(r'(for|while)\s*\(.*\b(retry|attempt|tries|retryCount)\b', line):
            body = "\n".join(lines[i:min(i + 15, len(lines))])
            if not any(kw in body for kw in ["Task.Delay", "Thread.Sleep",
                                              "backoff", "Backoff", "TimeSpan"]):
                findings.append({"type": "retry_without_backoff", "line": i + 1,
                                 "context": line.strip()[:200]})
    return findings


def detect_hardcoded_timeout(path: str, content: str, lines: list[str]) -> list[dict]:
    findings = []
    for i, line in enumerate(lines):
        if _is_comment(line):
            continue
        if re.search(r'TimeSpan\.From(Seconds|Minutes|Milliseconds|Hours)\s*\(\s*\d+\s*\)', line):
            if any(kw in line for kw in ["Timeout", "timeout", "TimeoutPolicy", "WaitAndRetry"]):
                findings.append({"type": "hardcoded_timeout", "line": i + 1,
                                 "context": line.strip()[:200]})
    return findings


# ─── Detector Registry ───────────────────────────────────────────────

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

SEVERITY_WEIGHTS = {"critical": 15, "high": 8, "medium": 3, "low": 1}


# ─── LLM Prompt Templates ────────────────────────────────────────────

RESILIENCE_PROMPTS = {
    "missing_cancellation_token": (
        "RESILIENCE FINDING: Async external call without CancellationToken.\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this missing CancellationToken. Do NOT review the rest of the file.\n"
        "1. Add CancellationToken parameter to the method signature if not present.\n"
        "2. Pass it to the external call.\n"
        "3. If this is a controller action, use HttpContext.RequestAborted.\n"
        "4. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "missing_timeout": (
        "RESILIENCE FINDING: HttpClient instantiated without timeout.\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this missing timeout. Do NOT review the rest of the file.\n"
        "1. Set HttpClient.Timeout to a sensible value (e.g., 30 seconds).\n"
        "2. Consider using IHttpClientFactory with a TimeoutPolicy instead.\n"
        "3. Show the minimal code change needed -- do not refactor surrounding code."
    ),
    "httpclient_no_policy": (
        "RESILIENCE FINDING: AddHttpClient registration without resilience policy.\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this missing policy handler. Do NOT review the rest of the file.\n"
        "1. Add .AddTransientHttpErrorPolicy() with retry + circuit breaker, OR\n"
        "2. Use .AddStandardResilienceHandler() for .NET 8+, OR\n"
        "3. Add .AddPolicyHandler() with a custom Polly policy.\n"
        "4. Show the minimal code change needed."
    ),
    "fire_and_forget": (
        "RESILIENCE FINDING: Fire-and-forget async call (lost exceptions).\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this fire-and-forget pattern. Do NOT review the rest of the file.\n"
        "1. If truly fire-and-forget, add error handling (ContinueWith to log).\n"
        "2. Otherwise, await the task and handle errors properly.\n"
        "3. Consider a background task queue (IHostedService, Channel<T>).\n"
        "4. Show the minimal code change needed."
    ),
    "catch_all_no_retry": (
        "RESILIENCE FINDING: catch(Exception) around external call without retry.\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this catch block. Do NOT review the rest of the file.\n"
        "1. Distinguish transient errors (timeout, 503) from permanent (404, validation).\n"
        "2. Add Polly WaitAndRetryAsync for transient errors.\n"
        "3. Show the minimal code change needed."
    ),
    "connection_no_dispose": (
        "RESILIENCE FINDING: Connection created without using/dispose.\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this missing dispose. Do NOT review the rest of the file.\n"
        "1. Wrap in a using statement or using declaration.\n"
        "2. For HttpClient, consider IHttpClientFactory instead.\n"
        "3. Show the minimal code change needed."
    ),
    "global_httpclient": (
        "RESILIENCE FINDING: Static HttpClient field (DNS caching issue).\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this static HttpClient. Do NOT review the rest of the file.\n"
        "1. Replace with IHttpClientFactory injection via DI.\n"
        "2. If static is intentional, set PooledConnectionLifetime.\n"
        "3. Show the minimal code change needed."
    ),
    "retry_without_backoff": (
        "RESILIENCE FINDING: Manual retry loop without delay/backoff.\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this retry loop. Do NOT review the rest of the file.\n"
        "1. Add exponential backoff (Task.Delay with increasing intervals).\n"
        "2. Better: replace with Polly WaitAndRetryAsync.\n"
        "3. Show the minimal code change needed."
    ),
    "hardcoded_timeout": (
        "RESILIENCE FINDING: Hardcoded timeout value.\n"
        "File: {file} (line {line})\nContext: {context}\n\n"
        "TASK: Evaluate ONLY this hardcoded timeout. Do NOT review the rest of the file.\n"
        "1. Extract to IConfiguration or appsettings.json.\n"
        "2. Use a named constant if config is overkill.\n"
        "3. Show the minimal code change needed."
    ),
    "missing_polly": (
        "RESILIENCE FINDING: Project makes external calls but has no resilience library.\n"
        "Project: {project}\nExternal call types: {context}\n\n"
        "TASK: Add Polly-based resilience to this project.\n"
        "1. Install Microsoft.Extensions.Http.Polly (or .Resilience for .NET 8+).\n"
        "2. Register HttpClient with AddTransientHttpErrorPolicy or AddStandardResilienceHandler.\n"
        "3. Configure retry (3 attempts, exponential backoff), circuit breaker, timeout.\n"
        "4. Show the DI registration code needed."
    ),
    "missing_health_checks": (
        "RESILIENCE FINDING: Web/service project without health checks.\n"
        "Project: {project}\n\n"
        "TASK: Add health check endpoints.\n"
        "1. Install Microsoft.Extensions.Diagnostics.HealthChecks.\n"
        "2. Add builder.Services.AddHealthChecks() with dependency checks.\n"
        "3. Map endpoints: /health and /ready.\n"
        "4. Show the registration code needed."
    ),
}


# ─── NuGet Cross-Reference ───────────────────────────────────────────

def check_nuget_resilience(project: str, packages: set[str],
                           data_sources: list[dict], category: str) -> list[dict]:
    findings = []
    if not data_sources:
        return findings
    has_polly = bool(packages & RESILIENCE_PACKAGES)
    ext_types = {ds.get("type") for ds in data_sources}
    if not has_polly and ("api" in ext_types or "messaging" in ext_types):
        findings.append({
            "type": "missing_polly", "severity": "high", "line": 0,
            "context": f"External calls: {', '.join(sorted(ext_types))}. No Polly/resilience NuGet.",
            "suggestion": "Add Microsoft.Extensions.Http.Polly or Microsoft.Extensions.Resilience",
        })
    if not (packages & HEALTH_CHECK_PACKAGES) and category.lower() in {"webapp", "service", "webapi"}:
        findings.append({
            "type": "missing_health_checks", "severity": "low", "line": 0,
            "context": f"Project category: {category}. No health check package.",
            "suggestion": "Add Microsoft.Extensions.Diagnostics.HealthChecks",
        })
    return findings


# ─── File Analysis ────────────────────────────────────────────────────

def analyze_file_resilience(filepath: str, scan_root: str) -> dict | None:
    content = safe_read_text(filepath)
    if content is None:
        return None
    lines = content.split("\n")
    findings = []
    for det in RESILIENCE_DETECTORS:
        for f in det["fn"](filepath, content, lines):
            f["severity"] = det["severity"]
            f["category"] = det["category"]
            findings.append(f)
    positive = scan_positive_patterns(content)
    if not findings and not positive:
        return None
    return {"path": _relpath(filepath, scan_root), "lines": len(lines),
            "findings": findings, "positivePatterns": positive}


# ─── Scoring ─────────────────────────────────────────────────────────

def compute_resilience_score(ext_count: int, positive: dict[str, int],
                             findings: list[dict], has_polly: bool,
                             has_health: bool, has_http_factory: bool) -> float:
    if ext_count == 0:
        return 100.0
    ratio = min(1.0, sum(positive.values()) / max(1, ext_count))
    score = ratio * 60
    if has_polly:        score += 15
    if has_http_factory: score += 10
    if has_health:       score += 5
    if positive.get("cancellationToken", 0) > 0: score += 5
    if positive.get("circuitBreaker", 0) > 0:    score += 5
    for f in findings:
        sev = f.get("severity", "low")
        score -= {"high": 5, "medium": 2, "low": 1}.get(sev, 0)
    return max(0.0, min(100.0, score))


# ─── Main Analysis ───────────────────────────────────────────────────

def analyze_all(scan_root: str, out_dir: str) -> dict:
    print("Loading existing analysis data...")
    project_meta = load_json(os.path.join(out_dir, "project-meta.json"), [])
    data_sources = load_data_sources(out_dir)
    dependencies = load_dependencies(out_dir)
    flow_paths = load_json(os.path.join(out_dir, "flow-paths.json"), {})

    pm_lookup: dict[str, dict] = {}
    for pm in project_meta:
        name = pm.get("project", "")
        if name:
            pm_lookup[name] = pm
    bl = flow_paths.get("businessLayers", {})

    print(f"  {len(project_meta)} projects in metadata")
    print(f"  {len(data_sources)} projects with external call patterns")
    print(f"  {len(dependencies)} projects with NuGet dependencies")

    print(f"\nScanning for C# files in: {scan_root}")
    cs_files = find_cs_files(scan_root)
    print(f"Found {len(cs_files)} C# files to analyze")

    project_files: dict[str, list[dict]] = defaultdict(list)
    analyzed = 0
    print("\nAnalyzing files for resilience patterns...")
    for i, fp in enumerate(cs_files):
        if (i + 1) % _PROGRESS_INTERVAL == 0:
            print(f"  Progress: {i + 1}/{len(cs_files)} files")
        fd = analyze_file_resilience(fp, scan_root)
        if fd is None:
            continue
        analyzed += 1
        proj = find_project_for_file(fp, project_meta, scan_root)
        if not proj:
            proj = infer_project_from_path(fp, scan_root)
        project_files[proj].append(fd)
    print(f"\n{analyzed} files had resilience findings or positive patterns")

    # Build per-project results
    projects = []
    all_keys = set(project_files.keys()) | set(data_sources.keys())
    for proj in sorted(all_keys):
        files = project_files.get(proj, [])
        ds = data_sources.get(proj, [])
        pkgs = dependencies.get(proj, set())
        meta = pm_lookup.get(proj, {})
        cat = meta.get("category", "unknown")
        repo = meta.get("repo", "")
        layer = bl.get(proj, {}).get("layer", "")

        all_findings = []
        for f in files:
            for finding in f["findings"]:
                finding["file"] = f["path"]
                all_findings.append(finding)
        all_findings.extend(check_nuget_resilience(proj, pkgs, ds, cat))

        total_pos: dict[str, int] = defaultdict(int)
        for f in files:
            for k, v in f.get("positivePatterns", {}).items():
                total_pos[k] += v

        has_polly = bool(pkgs & RESILIENCE_PACKAGES)
        has_health = bool(pkgs & HEALTH_CHECK_PACKAGES)
        has_hf = bool(pkgs & HTTP_FACTORY_PACKAGES) or total_pos.get("httpClientFactory", 0) > 0
        ext_by_type: dict[str, int] = defaultdict(int)
        for d in ds:
            ext_by_type[d.get("type", "unknown")] += 1

        score = compute_resilience_score(len(ds), dict(total_pos), all_findings,
                                          has_polly, has_health, has_hf)
        projects.append({
            "project": proj, "repo": repo, "category": cat, "layer": layer,
            "resilienceScore": round(score, 1),
            "externalCallCount": len(ds),
            "protectedCallCount": sum(1 for f in files if f.get("positivePatterns")),
            "pollyPackages": sorted(pkgs & (RESILIENCE_PACKAGES | HEALTH_CHECK_PACKAGES | HTTP_FACTORY_PACKAGES)),
            "resiliencePatterns": dict(total_pos),
            "externalCallsByType": dict(ext_by_type),
            "findings": all_findings,
            "findingCount": len(all_findings),
            "policySummary": {
                "retry": total_pos.get("retry", 0) > 0 or total_pos.get("policyHandler", 0) > 0,
                "circuitBreaker": total_pos.get("circuitBreaker", 0) > 0,
                "timeout": total_pos.get("timeout", 0) > 0,
                "bulkhead": total_pos.get("bulkhead", 0) > 0,
                "fallback": total_pos.get("fallback", 0) > 0,
            },
        })

    projects.sort(key=lambda x: x["resilienceScore"])

    ext_proj = [p for p in projects if p["externalCallCount"] > 0]
    sev_counts: dict[str, int] = defaultdict(int)
    type_counts: dict[str, int] = defaultdict(int)
    for p in projects:
        for f in p["findings"]:
            sev_counts[f.get("severity", "low")] += 1
            type_counts[f.get("type", "unknown")] += 1

    avg = sum(p["resilienceScore"] for p in ext_proj) / len(ext_proj) if ext_proj else 0
    return {
        "generated": date.today().isoformat(),
        "scanRoot": scan_root,
        "summary": {
            "totalProjects": len(projects),
            "projectsWithExternalCalls": len(ext_proj),
            "projectsWithPolly": sum(1 for p in projects if p["pollyPackages"]),
            "avgResilienceScore": round(avg, 1),
            "totalFindings": sum(p["findingCount"] for p in projects),
            "findingsBySeverity": dict(sev_counts),
            "findingsByType": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
        },
        "projects": projects,
        "resiliencePrompts": RESILIENCE_PROMPTS,
    }


# ─── Markdown Report ─────────────────────────────────────────────────

def generate_markdown_report(data: dict, output_path: str):
    projects = data["projects"]
    s = data["summary"]
    md = [
        "# Resilience Analysis Report", "",
        f"**Generated:** {data['generated']}",
        f"**Scan Root:** {data['scanRoot']}", "",
        "## Executive Summary", "",
        f"- **Total Projects:** {s['totalProjects']}",
        f"- **Projects with External Calls:** {s['projectsWithExternalCalls']}",
        f"- **Projects with Polly/Resilience NuGet:** {s['projectsWithPolly']}",
        f"- **Average Resilience Score:** {s['avgResilienceScore']}/100",
        f"- **Total Findings:** {s['totalFindings']}", "",
    ]
    sev = s.get("findingsBySeverity", {})
    if sev:
        md += ["### Findings by Severity", ""]
        for k in ["high", "medium", "low"]:
            if sev.get(k, 0):
                md.append(f"- **{k.title()}:** {sev[k]}")
        md.append("")
    by_type = s.get("findingsByType", {})
    if by_type:
        md += ["### Findings by Type", ""]
        for t, c in list(by_type.items())[:15]:
            md.append(f"- **{t}:** {c}")
        md.append("")

    ext = [p for p in projects if p["externalCallCount"] > 0]
    if ext:
        md += [
            "## Projects Ranked by Resilience Score", "",
            "| # | Project | Repo | Score | Ext Calls | Findings | Polly |",
            "|---|---------|------|-------|-----------|----------|-------|",
        ]
        for i, p in enumerate(ext[:40], 1):
            md.append(f"| {i} | {p['project']} | {p['repo']} | {p['resilienceScore']} | "
                      f"{p['externalCallCount']} | {p['findingCount']} | "
                      f"{'Yes' if p['pollyPackages'] else 'No'} |")
        md.append("")

    if ext:
        md += ["## Detailed Analysis (Top 20)", ""]
        for i, p in enumerate(ext[:20], 1):
            sc = p["resilienceScore"]
            grade = "POOR" if sc < 40 else ("FAIR" if sc < 70 else "GOOD")
            md += [
                f"### {i}. {p['project']} -- {grade} ({sc}/100)", "",
                f"- **Repo:** {p['repo']}",
                f"- **Category:** {p['category']}",
                f"- **External Calls:** {p['externalCallCount']}",
                f"- **Polly Packages:** {', '.join(p['pollyPackages']) or 'None'}",
            ]
            active = [k for k, v in p.get("policySummary", {}).items() if v]
            md.append(f"- **Active Policies:** {', '.join(active) or 'None'}")
            if p["findings"]:
                md += ["", "**Findings:**", ""]
                for f in p["findings"][:10]:
                    loc = f"{f.get('file', '')}:{f.get('line', '')}" if f.get("file") else ""
                    md.append(f"- [{f['severity'].upper()}] **{f['type']}** {'at ' + loc if loc else ''}")
                if len(p["findings"]) > 10:
                    md.append(f"- ... and {len(p['findings']) - 10} more")
            md.append("")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    Path(output_path).write_text("\n".join(md), encoding="utf-8")
    print(f"Saved: {output_path}")


# ─── Entry Point ─────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Resilience Scanner")
    print("=" * 70)
    print(f"Scan root: {SCAN_ROOT}")
    print(f"Output dir: {OUT_DIR}")
    print()
    os.makedirs(OUT_DIR, exist_ok=True)

    result = analyze_all(SCAN_ROOT, OUT_DIR)

    print("\nGenerating outputs...")
    json_path = os.path.join(OUT_DIR, "resilience-findings.json")
    md_path = os.path.join(OUT_DIR, "resilience-report.md")
    Path(json_path).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved: {json_path}")
    generate_markdown_report(result, md_path)

    s = result["summary"]
    print("\n" + "=" * 70)
    print("Resilience analysis complete!")
    print(f"  - {s['totalProjects']} projects analyzed")
    print(f"  - {s['projectsWithExternalCalls']} projects with external calls")
    print(f"  - {s['projectsWithPolly']} projects with Polly/resilience packages")
    print(f"  - {s['totalFindings']} total findings")
    print(f"  - Average resilience score: {s['avgResilienceScore']}/100")
    print("=" * 70)


if __name__ == "__main__":
    main()
