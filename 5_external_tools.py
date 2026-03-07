#!/usr/bin/env python3
"""
External Tools Runner — integrates semgrep, bandit, detect-secrets, and radon.

Usage:
    python3 5_external_tools.py <repos> <out> --tools semgrep,bandit,detect-secrets,radon
    python3 5_external_tools.py <repos> <out> --tools all
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

KNOWN_TOOLS = ["semgrep", "bandit", "detect-secrets", "radon"]
MAX_FINDINGS_PER_TOOL = 500
SUBPROCESS_TIMEOUT = 300  # 5 minutes per tool


def _get_tool_version(tool_name: str) -> str:
    """Get installed version string for a tool."""
    try:
        result = subprocess.run(
            [tool_name, "--version"],
            capture_output=True, text=True, timeout=15,
        )
        out = (result.stdout or result.stderr or "").strip()
        # Take first line, cap length
        return out.splitlines()[0][:120] if out else "unknown"
    except Exception:
        return "unknown"


# ── Tool runners ─────────────────────────────────────────────────────


def run_semgrep(scan_root: str) -> dict:
    """Run semgrep and return parsed findings."""
    result = subprocess.run(
        ["semgrep", "scan", "--json", "--config", "auto", "--quiet",
         "--max-target-bytes", "1000000", scan_root],
        capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
    )
    data = json.loads(result.stdout)
    severity_map = {"ERROR": "critical", "WARNING": "high", "INFO": "medium"}
    findings = []
    for r in data.get("results", []):
        extra = r.get("extra", {})
        raw_sev = extra.get("severity", "INFO")
        sev = severity_map.get(raw_sev, "medium")
        findings.append({
            "tool": "semgrep",
            "ruleId": r.get("check_id", ""),
            "severity": sev,
            "category": "security",
            "message": extra.get("message", ""),
            "file": r.get("path", ""),
            "line": r.get("start", {}).get("line", 0),
            "context": (extra.get("lines", "") or "").strip()[:200],
        })
    return {
        "tool": "semgrep",
        "version": _get_tool_version("semgrep"),
        "status": "success",
        "findingCount": len(findings),
        "findings": findings[:MAX_FINDINGS_PER_TOOL],
        "truncated": len(findings) > MAX_FINDINGS_PER_TOOL,
    }


def run_bandit(scan_root: str) -> dict:
    """Run bandit and return parsed findings."""
    result = subprocess.run(
        ["bandit", "-r", scan_root, "-f", "json", "--quiet"],
        capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
    )
    # bandit exits non-zero when it finds issues, so parse stdout regardless
    data = json.loads(result.stdout) if result.stdout.strip() else {}
    findings = []
    for r in data.get("results", []):
        sev = r.get("issue_severity", "LOW").upper()
        conf = r.get("issue_confidence", "LOW").upper()
        if sev == "HIGH" and conf == "HIGH":
            mapped = "critical"
        elif sev == "HIGH":
            mapped = "high"
        elif sev == "MEDIUM":
            mapped = "medium"
        else:
            mapped = "low"
        findings.append({
            "tool": "bandit",
            "ruleId": r.get("test_id", ""),
            "severity": mapped,
            "category": "security",
            "message": r.get("test_name", ""),
            "file": r.get("filename", ""),
            "line": r.get("line_number", 0),
            "context": (r.get("code", "") or "").strip()[:200],
        })
    return {
        "tool": "bandit",
        "version": _get_tool_version("bandit"),
        "status": "success",
        "findingCount": len(findings),
        "findings": findings[:MAX_FINDINGS_PER_TOOL],
        "truncated": len(findings) > MAX_FINDINGS_PER_TOOL,
    }


def run_detect_secrets(scan_root: str) -> dict:
    """Run detect-secrets and return parsed findings."""
    result = subprocess.run(
        ["detect-secrets", "scan", scan_root],
        capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
    )
    data = json.loads(result.stdout) if result.stdout.strip() else {}
    findings = []
    for filepath, secrets in data.get("results", {}).items():
        for s in secrets:
            findings.append({
                "tool": "detect-secrets",
                "ruleId": s.get("type", ""),
                "severity": "critical",
                "category": "security",
                "message": f"Potential secret: {s.get('type', 'unknown')}",
                "file": filepath,
                "line": s.get("line_number", 0),
                "context": "",
            })
    return {
        "tool": "detect-secrets",
        "version": _get_tool_version("detect-secrets"),
        "status": "success",
        "findingCount": len(findings),
        "findings": findings[:MAX_FINDINGS_PER_TOOL],
        "truncated": len(findings) > MAX_FINDINGS_PER_TOOL,
    }


def run_radon(scan_root: str) -> dict:
    """Run radon CC and MI, return parsed findings."""
    findings = []

    # Cyclomatic complexity — only grade C or worse
    try:
        cc_result = subprocess.run(
            ["radon", "cc", "-j", "-n", "C", scan_root],
            capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
        )
        cc_data = json.loads(cc_result.stdout) if cc_result.stdout.strip() else {}
        grade_severity = {"C": "medium", "D": "high", "E": "critical", "F": "critical"}
        for filepath, blocks in cc_data.items():
            for block in blocks:
                grade = block.get("rank", "A")
                if grade not in grade_severity:
                    continue
                findings.append({
                    "tool": "radon",
                    "ruleId": f"cc-grade-{grade}",
                    "severity": grade_severity[grade],
                    "category": "quality",
                    "message": f"Cyclomatic complexity grade {grade} ({block.get('complexity', '?')}): {block.get('type', '')} {block.get('name', '')}",
                    "file": filepath,
                    "line": block.get("lineno", 0),
                    "context": f"{block.get('type', '')} {block.get('name', '')} — complexity {block.get('complexity', '?')}",
                })
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
        print(f"  Warning: radon cc failed: {exc}")

    # Maintainability index
    try:
        mi_result = subprocess.run(
            ["radon", "mi", "-j", scan_root],
            capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
        )
        mi_data = json.loads(mi_result.stdout) if mi_result.stdout.strip() else {}
        mi_severity = {"C": "medium", "D": "high", "E": "critical", "F": "critical"}
        for filepath, info in mi_data.items():
            grade = info.get("rank", "A") if isinstance(info, dict) else "A"
            if grade not in mi_severity:
                continue
            findings.append({
                "tool": "radon",
                "ruleId": f"mi-grade-{grade}",
                "severity": mi_severity[grade],
                "category": "quality",
                "message": f"Maintainability index grade {grade}: {filepath}",
                "file": filepath,
                "line": 1,
                "context": f"MI grade {grade}",
            })
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
        print(f"  Warning: radon mi failed: {exc}")

    return {
        "tool": "radon",
        "version": _get_tool_version("radon"),
        "status": "success",
        "findingCount": len(findings),
        "findings": findings[:MAX_FINDINGS_PER_TOOL],
        "truncated": len(findings) > MAX_FINDINGS_PER_TOOL,
    }


TOOL_RUNNERS = {
    "semgrep": run_semgrep,
    "bandit": run_bandit,
    "detect-secrets": run_detect_secrets,
    "radon": run_radon,
}


# ── Main ─────────────────────────────────────────────────────────────


def resolve_tool_list(tools_arg: str) -> list[str]:
    """Parse --tools value into a list of tool names."""
    val = tools_arg.strip().lower()
    if val in ("all", "*"):
        return list(KNOWN_TOOLS)
    if val in ("none", ""):
        return []
    return [t.strip() for t in val.split(",") if t.strip()]


def main():
    parser = argparse.ArgumentParser(description="Run external analysis tools.")
    parser.add_argument("repos", help="Directory to scan")
    parser.add_argument("out", help="Output directory")
    parser.add_argument("--tools", default="all",
                        help="Comma-separated list of tools, or all/none")
    args = parser.parse_args()

    scan_root = os.path.abspath(args.repos)
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    requested = resolve_tool_list(args.tools)
    if not requested:
        print("  No tools requested, skipping.")
        return

    unknown = [t for t in requested if t not in KNOWN_TOOLS]
    if unknown:
        print(f"  Warning: unknown tools ignored: {', '.join(unknown)}")
        requested = [t for t in requested if t in KNOWN_TOOLS]

    print(f"  Tools requested: {', '.join(requested)}")

    tools_executed = []
    tools_skipped = {}
    tools_results = {}

    for tool_name in requested:
        # Check availability
        exe = tool_name
        if not shutil.which(exe):
            reason = f"not found in PATH"
            tools_skipped[tool_name] = reason
            print(f"  {tool_name}: skipped — {reason}")
            continue

        # Run the tool
        print(f"  {tool_name}: running...")
        try:
            result = TOOL_RUNNERS[tool_name](scan_root)
            tools_executed.append(tool_name)
            tools_results[tool_name] = result
            count = result.get("findingCount", 0)
            trunc = " (truncated)" if result.get("truncated") else ""
            print(f"  {tool_name}: {count} findings{trunc}")
        except subprocess.TimeoutExpired:
            tools_skipped[tool_name] = "timed out"
            print(f"  {tool_name}: skipped — timed out after {SUBPROCESS_TIMEOUT}s")
        except json.JSONDecodeError as exc:
            tools_skipped[tool_name] = f"invalid JSON output: {exc}"
            print(f"  {tool_name}: skipped — could not parse output")
        except OSError as exc:
            tools_skipped[tool_name] = str(exc)
            print(f"  {tool_name}: skipped — {exc}")
        except Exception as exc:
            tools_skipped[tool_name] = str(exc)
            print(f"  {tool_name}: skipped — unexpected error: {exc}")

    # Build summary
    all_findings = []
    for tr in tools_results.values():
        all_findings.extend(tr.get("findings", []))

    by_severity = {}
    by_tool = {}
    by_category = {}
    for f in all_findings:
        sev = f.get("severity", "unknown")
        by_severity[sev] = by_severity.get(sev, 0) + 1
        t = f.get("tool", "unknown")
        by_tool[t] = by_tool.get(t, 0) + 1
        cat = f.get("category", "other")
        by_category[cat] = by_category.get(cat, 0) + 1

    output = {
        "generated": datetime.now().isoformat(),
        "scanRoot": scan_root,
        "toolsRequested": requested,
        "toolsExecuted": tools_executed,
        "toolsSkipped": tools_skipped,
        "summary": {
            "totalFindings": len(all_findings),
            "findingsBySeverity": by_severity,
            "findingsByTool": by_tool,
            "findingsByCategory": by_category,
        },
        "tools": tools_results,
    }

    out_path = os.path.join(out_dir, "external-tools.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"  Wrote {out_path} ({len(all_findings)} total findings)")


if __name__ == "__main__":
    main()
