#!/usr/bin/env python3
"""Security platform integrations — ArmorCode and SonarQube.

Connects the local static-analysis pipeline to external security platforms.
Runs in demo mode (realistic mock data) when API credentials are not configured,
so the full workflow can be demonstrated without platform access.

Usage:
    python3 6_security_integrations.py <out> --platforms armorcode,sonarqube
    python3 6_security_integrations.py <out> --platforms all
    python3 6_security_integrations.py <out> --platforms all --export external-tools.json
"""

import argparse
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from integrations import KNOWN_INTEGRATIONS, discover_integrations


def _load_local_findings(out_dir: str, filename: str) -> tuple[list[dict], dict]:
    """Load findings from a local JSON file for export to platforms.

    Returns (findings_list, metadata_dict).
    """
    path = os.path.join(out_dir, filename)
    if not os.path.isfile(path):
        return [], {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"  Warning: could not load {filename}: {exc}")
        return [], {}

    # external-tools.json has findings nested under tools
    all_findings: list[dict] = []
    if "tools" in data:
        for tool_result in data["tools"].values():
            all_findings.extend(tool_result.get("findings", []))
    elif "findings" in data:
        all_findings = data["findings"]

    metadata = {
        "generated": data.get("generated", ""),
        "scanRoot": data.get("scanRoot", ""),
    }
    return all_findings, metadata


def _load_smell_findings(out_dir: str) -> list[dict]:
    """Load smell findings from refactoring-targets.json and normalize them."""
    path = os.path.join(out_dir, "refactoring-targets.json")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    findings: list[dict] = []
    for project in data.get("projects", []):
        for file_entry in project.get("files", []):
            for smell in file_entry.get("smells", []):
                findings.append({
                    "tool": "scan-smells",
                    "ruleId": smell.get("type", ""),
                    "severity": smell.get("severity", "medium"),
                    "category": smell.get("category", "quality"),
                    "message": smell.get("context", smell.get("type", "")),
                    "file": file_entry.get("path", file_entry.get("file", "")),
                    "line": smell.get("line", 0),
                    "context": smell.get("context", "")[:200],
                })
    return findings


def resolve_platform_list(platforms_arg: str) -> list[str]:
    """Parse --platforms value into a list of platform names."""
    val = platforms_arg.strip().lower()
    if val in ("all", "*"):
        return list(KNOWN_INTEGRATIONS)
    if val in ("none", ""):
        return []
    return [p.strip() for p in val.split(",") if p.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="Security platform integrations (ArmorCode, SonarQube)."
    )
    parser.add_argument("out", help="Output directory (same as pipeline output)")
    parser.add_argument(
        "--platforms", default="all",
        help=f"Comma-separated platforms, or all/none (available: {', '.join(KNOWN_INTEGRATIONS)})"
    )
    parser.add_argument(
        "--export", default="",
        help="Also export local findings to platforms (specify source JSON filename, e.g. external-tools.json)"
    )
    parser.add_argument(
        "--config", default="",
        help="Path to integration config YAML (default: config.yaml in repo root)"
    )
    args = parser.parse_args()

    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    # Load integration config
    config = _load_integration_config(args.config)

    requested = resolve_platform_list(args.platforms)
    if not requested:
        print("  No platforms requested, skipping.")
        return

    unknown = [p for p in requested if p not in KNOWN_INTEGRATIONS]
    if unknown:
        print(f"  Warning: unknown platforms ignored: {', '.join(unknown)}")
        requested = [p for p in requested if p in KNOWN_INTEGRATIONS]

    print(f"  Platforms requested: {', '.join(requested)}")

    # Discover and instantiate integrations
    registry = discover_integrations(config)

    results: dict[str, dict] = {}
    all_imported_findings: list[dict] = []

    for platform_name in requested:
        if platform_name not in registry:
            print(f"  {platform_name}: adapter not found, skipping")
            continue

        adapter = registry[platform_name]
        mode_label = " (demo)" if adapter.is_demo else ""
        print(f"  {adapter.display_name}{mode_label}: connecting...")

        # Test connection
        conn = adapter.test_connection()
        if conn.get("demo"):
            print(f"  {adapter.display_name}: {conn['message']}")
        elif conn.get("connected"):
            print(f"  {adapter.display_name}: {conn['message']}")
        else:
            print(f"  {adapter.display_name}: {conn['message']}")

        # Import findings from platform
        print(f"  {adapter.display_name}: importing findings...")
        import_result = adapter.import_findings()
        count = import_result.get("findingCount", 0)
        results[platform_name] = import_result
        all_imported_findings.extend(import_result.get("findings", []))

        # Show per-project breakdown if available
        per_project = import_result.get("projects", {})
        if per_project and len(per_project) > 1:
            print(f"  {adapter.display_name}: {count} findings from {len(per_project)} projects:")
            for pk, pr in per_project.items():
                print(f"    {pk}: {pr.get('findingCount', 0)} findings ({pr.get('status', '?')})")
        else:
            print(f"  {adapter.display_name}: {count} findings imported")

        # Export local findings if requested
        if args.export:
            local_findings, metadata = _load_local_findings(out_dir, args.export)
            # Also include smell findings
            local_findings.extend(_load_smell_findings(out_dir))
            if local_findings:
                print(f"  {adapter.display_name}: exporting {len(local_findings)} local findings...")
                export_result = adapter.export_findings(local_findings, metadata)
                results[platform_name]["export"] = export_result
                exported = export_result.get("findingsExported", 0)
                print(f"  {adapter.display_name}: {exported} findings exported ({export_result.get('status', 'unknown')})")
            else:
                print(f"  {adapter.display_name}: no local findings to export")

    # Build aggregated output
    by_severity: dict[str, int] = {}
    by_tool: dict[str, int] = {}
    by_category: dict[str, int] = {}
    for f in all_imported_findings:
        sev = f.get("severity", "unknown")
        by_severity[sev] = by_severity.get(sev, 0) + 1
        t = f.get("tool", "unknown")
        by_tool[t] = by_tool.get(t, 0) + 1
        cat = f.get("category", "other")
        by_category[cat] = by_category.get(cat, 0) + 1

    output = {
        "generated": datetime.now().isoformat(),
        "platformsRequested": requested,
        "platformsExecuted": list(results.keys()),
        "summary": {
            "totalFindings": len(all_imported_findings),
            "findingsBySeverity": by_severity,
            "findingsByTool": by_tool,
            "findingsByCategory": by_category,
        },
        "platforms": results,
    }

    out_path = os.path.join(out_dir, "security-integrations.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"  Wrote {out_path} ({len(all_imported_findings)} total findings)")


def _load_integration_config(config_path: str) -> dict:
    """Load integration config from YAML file."""
    if not config_path:
        config_path = os.path.join(SCRIPT_DIR, "config.yaml")
    if not os.path.isfile(config_path):
        return {}
    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        # Extract the integrations section
        return data.get("integrations", {})
    except ImportError:
        # Fall back to reading just the integrations keys manually
        return {}
    except Exception:
        return {}


if __name__ == "__main__":
    main()
