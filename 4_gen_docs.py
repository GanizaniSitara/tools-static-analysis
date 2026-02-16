#!/usr/bin/env python3
"""
Dependency Mapper — Documentation Generator (Python)

Reads analysis outputs and generates structured markdown documentation.
Supports single-repo and multi-repo modes.
"""

import glob
import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

OUT_DIR = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "output")
DOCS_DIR = os.path.join(OUT_DIR, "docs")


def _load_json(path: str, default=None):
    """Load a JSON file, returning *default* on any read/parse error."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        if default is None:
            raise
        print(f"  Warning: could not load {path}: {exc}")
        return default


def _read_text(path: str) -> str | None:
    """Read a text file, returning None on error."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


# Load analysis data
graph = _load_json(os.path.join(OUT_DIR, "graph.json"))
project_meta = _load_json(os.path.join(OUT_DIR, "project-meta.json"))
data_findings = _load_json(os.path.join(OUT_DIR, "data-sources.json"))
configs = _load_json(os.path.join(OUT_DIR, "configs.json"))

# Load optional data (may not exist on older runs)
data_flow: dict = _load_json(os.path.join(OUT_DIR, "data-flow.json"), {})
flow_paths_data: dict = _load_json(os.path.join(OUT_DIR, "flow-paths.json"), {})
field_trace_data: dict = _load_json(os.path.join(OUT_DIR, "field-traceability.json"), {})
repos_data: list = _load_json(os.path.join(OUT_DIR, "repos.json"), [])
refactoring_data: dict = _load_json(os.path.join(OUT_DIR, "refactoring-targets.json"), {})
ux_inconsistencies: dict = _load_json(os.path.join(OUT_DIR, "ux-inconsistencies.json"), {})
nuget_health: dict = _load_json(os.path.join(OUT_DIR, "nuget-health.json"), {})
test_data: dict = _load_json(os.path.join(OUT_DIR, "test-projects.json"), {})
external_tools_data: dict = _load_json(os.path.join(OUT_DIR, "external-tools.json"), {})

# Load all language scanner outputs (e.g. python-projects.json, java-projects.json)
language_data: dict[str, dict] = {}
for _lf in glob.glob(os.path.join(OUT_DIR, "*-projects.json")):
    _basename = os.path.basename(_lf)
    if _basename in ("project-meta.json", "test-projects.json"):
        continue
    _lang_name = _basename.replace("-projects.json", "")
    _ld = _load_json(_lf, {})
    if _ld.get("projects"):
        language_data[_lang_name] = _ld


# ─── Parse CSVs ──────────────────────────────────────────────────────

def read_csv(filepath: str) -> list[dict]:
    """Read a CSV file, handling quoted values with commas."""
    try:
        content = Path(filepath).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"  Warning: could not read CSV {filepath}: {exc}")
        return []
    lines = content.strip().splitlines()
    if not lines:
        return []

    headers = lines[0].split(",")
    rows = []

    for line in lines[1:]:
        if not line.strip():
            continue
        values = []
        current = ""
        in_quotes = False
        for ch in line:
            if ch == '"':
                in_quotes = not in_quotes
                continue
            if ch == "," and not in_quotes:
                values.append(current)
                current = ""
                continue
            current += ch
        values.append(current)

        row = {}
        for i, h in enumerate(headers):
            row[h] = values[i] if i < len(values) else ""
        rows.append(row)

    return rows


package_deps = read_csv(os.path.join(OUT_DIR, "dependencies.csv"))
project_refs_csv = read_csv(os.path.join(OUT_DIR, "project-refs.csv"))

# Determine repos
repos = sorted({p["repo"] for p in project_meta if p.get("repo")})
is_multi_repo = len(repos) > 1

# Create directory structure
dirs = ["", "applications", "libraries", "connectors", "data-sources", "diagrams"]
if is_multi_repo:
    for repo in repos:
        dirs.append(f"repos/{repo}")
for d in dirs:
    os.makedirs(os.path.join(DOCS_DIR, d), exist_ok=True)


# ─── Build lookup maps ──────────────────────────────────────────────

def sanitize_id(id_str: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", id_str)


projects_by_name: dict[str, dict] = {pm["project"]: pm for pm in project_meta}

deps_by_project: dict[str, list] = {}
for pd in package_deps:
    deps_by_project.setdefault(pd["project"], []).append(pd)

refs_by_project: dict[str, list] = {}
referenced_by: dict[str, list] = {}
for pr in project_refs_csv:
    refs_by_project.setdefault(pr["project"], []).append(pr)
    referenced_by.setdefault(pr["references"], []).append(pr["project"])

data_by_project: dict[str, list] = {}
for f in data_findings:
    parts = os.path.normpath(f["file"]).split(os.sep)
    proj_dir = parts[1 if is_multi_repo else 0] if len(parts) > (1 if is_multi_repo else 0) else parts[0]
    data_by_project.setdefault(proj_dir, []).append(f)


def compute_hotspot_metrics() -> list[dict]:
    """Compute coupling/complexity metrics for each project, sorted by hotspot score."""
    bl = flow_paths_data.get("businessLayers", {})
    metrics = []
    for pm in project_meta:
        project = pm["project"]
        fan_out = len(refs_by_project.get(project, []))
        fan_in = len(referenced_by.get(project, []))
        nuget_deps = len(deps_by_project.get(project, []))
        dp_list = data_by_project.get(project, [])
        data_pattern_count = len(dp_list)
        data_types = sorted({f["type"] for f in dp_list}) if dp_list else []
        cross_repo_out = sum(
            1 for r in refs_by_project.get(project, []) if r.get("crossRepo") == "true"
        )
        cross_repo_in = sum(
            1
            for src in referenced_by.get(project, [])
            for r in refs_by_project.get(src, [])
            if r.get("references") == project and r.get("crossRepo") == "true"
        )
        cross_repo_refs = cross_repo_out + cross_repo_in
        hotspot_score = (
            fan_out * 3 + fan_in * 2 + nuget_deps + data_pattern_count + cross_repo_refs * 4
        )
        layer_info = bl.get(project, {})
        entry = {
            "project": project,
            "category": pm["category"],
            "repo": pm.get("repo", ""),
            "path": pm.get("globalPath") or pm.get("path", ""),
            "layer": layer_info.get("layer", ""),
            "layer_confidence": layer_info.get("confidence", 0),
            "fan_out": fan_out,
            "fan_in": fan_in,
            "nuget_deps": nuget_deps,
            "data_patterns": data_pattern_count,
            "data_types": data_types,
            "cross_repo_refs": cross_repo_refs,
            "hotspot_score": hotspot_score,
        }
        smells = compute_smell_flags(entry)
        entry["smells"] = smells
        entry["explanation"] = compute_hotspot_explanation(entry, smells)

        # Risk score: discounts expected patterns (Library/Infrastructure fan-in)
        is_infra = pm["category"] == "Library" or layer_info.get("layer", "") == "Infrastructure"
        adjusted_fan_in = min(fan_in, 4) if is_infra else fan_in
        risk_score = (
            fan_out * 3 + adjusted_fan_in * 2 + data_pattern_count + cross_repo_refs * 4
        )
        risk_score += sum(10 for s in smells if s["level"] == "red")
        risk_score += sum(5 for s in smells if s["level"] == "yellow")
        risk_score -= sum(5 for s in smells if s["level"] == "green")
        risk_score = max(0, risk_score)
        entry["risk_score"] = risk_score

        metrics.append(entry)
    metrics.sort(key=lambda x: -x["risk_score"])
    return metrics


def compute_smell_flags(m: dict) -> list[dict]:
    """Return a list of smell flags for a hotspot metric dict."""
    flags = []
    cat = m.get("category", "")
    layer = m.get("layer", "")
    fan_in = m.get("fan_in", 0)
    fan_out = m.get("fan_out", 0)
    data_types = m.get("data_types", [])
    cross_repo = m.get("cross_repo_refs", 0)

    # Red flags
    if fan_in >= 3 and fan_out >= 5:
        flags.append({
            "id": "hub",
            "level": "red",
            "label": "Hub/God Object",
            "explanation": f"Fan-in {fan_in} + fan-out {fan_out}: heavily depended-upon AND heavily depending",
        })
    if cat in ("Application", "DesktopApp", "Test") and fan_in >= 3:
        flags.append({
            "id": "upstream_dep",
            "level": "red",
            "label": "Upstream Dependency",
            "explanation": f"{cat} with fan-in {fan_in}: app/test layer should not be reused by others",
        })

    # Yellow flags
    if len(data_types) >= 3:
        flags.append({
            "id": "mixed_concerns",
            "level": "yellow",
            "label": "Mixed Concerns",
            "explanation": f"{len(data_types)} data types ({', '.join(data_types)}): too many responsibilities",
        })
    if cross_repo >= 2:
        flags.append({
            "id": "cross_boundary",
            "level": "yellow",
            "label": "Cross-Boundary",
            "explanation": f"{cross_repo} cross-repo refs: heavy coupling across repo boundaries",
        })
    if cat != "Library" and layer != "Infrastructure" and fan_in >= 5:
        flags.append({
            "id": "widely_used_non_lib",
            "level": "yellow",
            "label": "Widely Used Non-Library",
            "explanation": f"{cat} with fan-in {fan_in}: may be mis-categorized infrastructure",
        })

    # Green flags
    if (cat == "Library" or layer == "Infrastructure") and fan_in >= 3:
        flags.append({
            "id": "stable_infra",
            "level": "green",
            "label": "Stable Infrastructure",
            "explanation": f"{cat}/{layer} with fan-in {fan_in}: expected healthy shared component",
        })

    return flags


def compute_hotspot_explanation(m: dict, flags: list[dict]) -> str:
    """Return a one-line human-readable summary of score drivers and smells."""
    parts = []
    red_flags = [f for f in flags if f["level"] == "red"]
    yellow_flags = [f for f in flags if f["level"] == "yellow"]
    green_flags = [f for f in flags if f["level"] == "green"]

    if red_flags:
        parts.append("Risk: " + "; ".join(f["label"] for f in red_flags))
    if yellow_flags:
        parts.append("Watch: " + "; ".join(f["label"] for f in yellow_flags))
    if green_flags:
        parts.append("OK: " + "; ".join(f["label"] for f in green_flags))

    drivers = []
    if m.get("fan_out", 0) >= 3:
        drivers.append(f"fan-out={m['fan_out']}")
    if m.get("fan_in", 0) >= 3:
        drivers.append(f"fan-in={m['fan_in']}")
    if m.get("cross_repo_refs", 0) > 0:
        drivers.append(f"cross-repo={m['cross_repo_refs']}")
    if drivers:
        parts.append("Drivers: " + ", ".join(drivers))

    return " | ".join(parts) if parts else "Low coupling"


def get_dir_for_category(cat: str) -> str:
    if cat == "Connector":
        return "connectors"
    if cat == "Library":
        return "libraries"
    return "applications"


# ─── Generate index.md ─────────────────────────────────────────────

def generate_index() -> str:
    categories = graph["summary"]["categories"]

    md = f"""# Dependency Map

## Overview

| Metric | Count |
|--------|-------|
| Repositories | {graph['summary'].get('totalRepos', 1)} |
| Total Projects | {graph['summary']['totalProjects']} |
| NuGet Packages | {graph['summary']['totalNuGetPackages']} |
| Project References | {graph['summary']['totalProjectRefs']} |
"""

    if graph["summary"].get("totalCrossRepoRefs", 0) > 0:
        md += f"| Cross-Repo References | {graph['summary']['totalCrossRepoRefs']} |\n"

    md += f"""| Data Access Findings | {graph['summary']['totalDataFindings']} |
| Config Files | {graph['summary']['totalConfigFiles']} |

"""

    if is_multi_repo and graph["summary"].get("repos"):
        md += "## Repositories\n\n| Repo | Projects | Categories |\n|------|----------|------------|\n"
        for repo_name, info in graph["summary"]["repos"].items():
            cats = ", ".join(f"{k}:{v}" for k, v in info["categories"].items())
            md += f"| **{repo_name}** | {info['projects']} | {cats} |\n"
        md += "\n"

    md += "## Project Categories\n\n| Category | Count |\n|----------|-------|\n"
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        md += f"| {cat} | {count} |\n"

    # Diagrams
    for diagram_name, heading in [
        ("landscape.mmd", "Full Landscape"),
        ("core-libraries.mmd", "Core Library Hierarchy"),
        ("data-infrastructure.mmd", "Data Infrastructure"),
        ("nuget-groups.mmd", "NuGet Package Groups"),
    ]:
        content = _read_text(os.path.join(OUT_DIR, "diagrams", diagram_name))
        if content:
            md += f"\n## {heading}\n\n```mermaid\n{content}\n```\n"

    # Navigation
    md += "\n## Navigation\n\n"

    if is_multi_repo:
        for repo in repos:
            repo_projects = [p for p in project_meta if p.get("repo") == repo]
            md += f"### {repo}\n"
            for cat in sorted({p["category"] for p in repo_projects}):
                cat_projects = [p for p in repo_projects if p["category"] == cat]
                links = ", ".join(f"[{p['project']}](repos/{repo}/{p['project']}.md)" for p in cat_projects[:10])
                md += f"**{cat}** ({len(cat_projects)}): {links}"
                if len(cat_projects) > 10:
                    md += f", ... +{len(cat_projects) - 10} more"
                md += "\n\n"
    else:
        for cat in sorted({p["category"] for p in project_meta}):
            cat_projects = [p for p in project_meta if p["category"] == cat]
            dir_name = get_dir_for_category(cat)
            md += f"### {cat} ({len(cat_projects)})\n"
            md += "\n".join(f"- [{p['project']}]({dir_name}/{p['project']}.md)" for p in cat_projects[:20])
            if len(cat_projects) > 20:
                md += f"\n- ... +{len(cat_projects) - 20} more"
            md += "\n\n"

    md += "- [Data Source Registry](data-sources/registry.md)\n\n"
    md += f"---\n\n*Generated: {date.today().isoformat()}*\n*Tool: Dependency Mapper (Static Analysis)*\n"

    return md


# ─── Generate per-project page ──────────────────────────────────────

def generate_project_page(pm: dict) -> str:
    project = pm["project"]
    repo = pm.get("repo", "")
    category = pm["category"]
    deps = deps_by_project.get(project, [])
    refs = refs_by_project.get(project, [])
    consumers = referenced_by.get(project, [])
    data_patterns = data_by_project.get(project, [])

    md = f"""# {project}

## Overview

| Property | Value |
|----------|-------|
| Category | {category} |
"""
    if repo:
        md += f"| Repository | {repo} |\n"

    md += f"""| Path | `{pm['path']}` |
| Project References | {len(refs)} |
| NuGet Dependencies | {len(deps)} |
| Consumers | {len(consumers)} |

"""

    # Dependency diagram
    if refs or consumers:
        md += "## Dependency Diagram\n\n```mermaid\ngraph TD\n"
        md += f'    {sanitize_id(project)}["<strong>{project}</strong>"]\n'
        for r in refs:
            ref_name = r["references"]
            is_cross = r.get("crossRepo") == "true"
            md += f'    {sanitize_id(ref_name)}["{ref_name}"]\n'
            arrow = " -.->" if is_cross else " -->"
            md += f"    {sanitize_id(project)}{arrow} {sanitize_id(ref_name)}\n"
        for c in consumers[:15]:
            md += f'    {sanitize_id(c)}["{c}"]\n'
            md += f"    {sanitize_id(c)} -.-> {sanitize_id(project)}\n"
        if len(consumers) > 15:
            md += f'    more_consumers["... +{len(consumers) - 15} more"]\n'
            md += f"    more_consumers -.-> {sanitize_id(project)}\n"
        md += "```\n\n"

    if refs:
        md += "## Project References\n"
        for r in refs:
            is_cross = r.get("crossRepo") == "true"
            md += f"- {r['references']}{' *(cross-repo)*' if is_cross else ''}\n"
        md += "\n"

    if consumers:
        md += "## Consumed By\n" + "\n".join(f"- {c}" for c in consumers) + "\n\n"

    external_pkgs = [d for d in deps if not d["package"].startswith(("StockSharp.", "Ecng."))]
    internal_pkgs = [d for d in deps if d["package"].startswith(("StockSharp.", "Ecng."))]

    if external_pkgs:
        md += "## External NuGet Packages\n| Package | Version |\n|---------|---------||\n"
        md += "\n".join(f"| {d['package']} | {d['version']} |" for d in external_pkgs)
        md += "\n\n"

    if internal_pkgs:
        md += "## Internal NuGet Packages\n| Package | Version |\n|---------|---------|\n"
        md += "\n".join(f"| {d['package']} | {d['version']} |" for d in internal_pkgs)
        md += "\n\n"

    if data_patterns:
        grouped: dict[str, list] = {}
        for dp in data_patterns:
            grouped.setdefault(dp["pattern"], []).append(dp)

        md += "## Data Access Patterns\n"
        for pattern, findings in grouped.items():
            md += f"### {pattern}\n| File | Line | Context |\n|------|------|---------||\n"
            for f in findings[:15]:
                ctx = f["context"][:70].replace("|", "\\|")
                md += f"| `{f['file']}` | {f['line']} | `{ctx}` |\n"
            if len(findings) > 15:
                md += f"\n*... and {len(findings) - 15} more*\n"
            md += "\n"

    back_path = "../../" if is_multi_repo else "../"
    md += f"\n---\n\n*[Back to Index]({back_path}index.md)*\n"
    return md


# ─── Generate data source registry ──────────────────────────────────

def generate_data_source_registry() -> str:
    by_type: dict[str, list] = {}
    for f in data_findings:
        by_type.setdefault(f["type"], []).append(f)

    md = "# Data Source Registry\n\n## Summary\n\n| Type | Occurrences |\n|------|-------------|\n"
    for type_name, findings in sorted(by_type.items(), key=lambda x: -len(x[1])):
        md += f"| {type_name} | {len(findings)} |\n"
    md += "\n"

    # Connection strings
    configs_with_conn = [c for c in configs if c.get("connectionStrings")]
    if configs_with_conn:
        md += "## Connection Strings Found\n\n| File | Repo | Connection Name | Value |\n|------|------|----------------|-------|\n"
        for c in configs_with_conn:
            for name, val in c["connectionStrings"].items():
                sanitized_val = str(val)[:80].replace("|", "\\|")
                md += f"| `{c['file']}` | {c.get('repo', '')} | {name} | `{sanitized_val}` |\n"
        md += "\n"

    for type_name, findings in sorted(by_type.items(), key=lambda x: -len(x[1])):
        by_pattern: dict[str, list] = {}
        for f in findings:
            by_pattern.setdefault(f["pattern"], []).append(f)

        md += f"## {type_name[0].upper()}{type_name[1:]}\n\n"
        for pattern, p_findings in sorted(by_pattern.items(), key=lambda x: -len(x[1])):
            by_repo: dict[str, list] = {}
            for f in p_findings:
                by_repo.setdefault(f.get("repo", "default"), []).append(f)

            md += f"### {pattern} ({len(p_findings)} occurrences)\n\n"
            md += "| Repo | File | Line | Context |\n|------|------|------|---------||\n"
            for f in p_findings[:25]:
                ctx = f["context"][:60].replace("|", "\\|")
                md += f"| {f.get('repo', '')} | `{f['file']}` | {f['line']} | `{ctx}` |\n"
            if len(p_findings) > 25:
                md += f"\n*... and {len(p_findings) - 25} more*\n"
            md += f"\n**Repos:** {', '.join(by_repo.keys())}\n\n"

    md += "\n---\n\n*[Back to Index](../index.md)*\n"
    return md


# ─── Generate viewer.html ────────────────────────────────────────

def _esc_html(text: str) -> str:
    """Escape HTML special characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _safe_json_for_script(data, **kwargs) -> str:
    """json.dumps() safe for embedding inside <script> tags.

    Replaces '</' with '<\\/' to prevent the HTML parser from seeing
    '</script>' (or any closing tag) inside string literals.
    """
    return json.dumps(data, **kwargs).replace("</", "<\\/")


def _hex_to_rgb(hex_color: str) -> str:
    """Convert #RRGGBB to 'R,G,B' for use in rgba()."""
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)}"


def _file_uri(path: str) -> str:
    """Convert a filesystem path to a file:/// URI (forward slashes)."""
    p = path.replace("\\", "/")
    if not p.startswith("/"):
        p = "/" + p  # e.g. C:/foo → /C:/foo for file:///C:/foo
    return "file://" + p


def _resolve_file_uri(rel_path: str, repo_name: str, repo_roots: dict[str, str]) -> str:
    """Resolve a relative file path (possibly repo-prefixed) to a file:/// URI."""
    root = repo_roots.get(repo_name, "")
    if not root or not rel_path:
        return ""
    rp = rel_path.replace("\\", "/")
    rr = root.replace("\\", "/")
    # Strip repo-name prefix if it duplicates the repo root tail
    repo_tail = rr.rstrip("/").rsplit("/", 1)[-1]
    if repo_tail and rp.startswith(repo_tail + "/"):
        rp = rp[len(repo_tail) + 1:]
    return _file_uri(rr + "/" + rp)


def _file_actions_html(path: str, line: int = 0, display: str = "") -> str:
    """Generate HTML for a file reference with IDE action icons."""
    if not path:
        return f'<span class="mono">{_esc_html(display or "")}</span>'
    disp = _esc_html(display or (f"{path}:{line}" if line else path))
    p = _esc_html(path)
    return (
        f'<span class="file-ref">'
        f'<span class="mono" style="color:#53565A;">{disp}</span>'
        f' <a href="#" class="file-action file-studio" data-path="{p}" data-line="{line}" title="Open in Visual Studio">Studio</a>'
        f' <a href="#" class="file-action file-code" data-path="{p}" data-line="{line}" title="Open in VS Code">Code</a>'
        f' <a href="#" class="file-action file-claude" data-path="{p}" data-line="{line}" title="Explore with Claude Code">Claude</a>'
        f' <a href="#" class="file-action file-view" data-path="{p}" data-line="{line}" title="View in browser">View</a>'
        f'</span>'
    )


def generate_viewer_html() -> str:
    summary = graph["summary"]
    categories = summary["categories"]
    repo_count = summary.get("totalRepos", 1)
    repo_list = sorted({p["repo"] for p in project_meta if p.get("repo")})
    if len(repo_list) > 1:
        title = f"{len(repo_list)} Repositories"
    elif repo_list:
        title = repo_list[0]
    else:
        title = "Project"

    # ── Collect two-level diagram tabs: overview + per-category ──
    diagrams_dir = os.path.join(OUT_DIR, "diagrams")
    diagram_tabs: list[dict] = []

    # Overview tab (category-level diagram)
    overview_path = os.path.join(diagrams_dir, "overview.mmd")
    content = _read_text(overview_path)
    if content:
        diagram_tabs.append({
            "id": "overview",
            "label": "Overview",
            "title": "Category Overview",
            "mermaid": content,
        })

    # Per-category tabs ordered by project count descending
    skip_cats = {"Localization", "Sample"}
    cat_counts = sorted(categories.items(), key=lambda x: -x[1])
    for cat_name, count in cat_counts:
        if cat_name in skip_cats:
            continue
        cat_key = cat_name.lower()
        content = _read_text(os.path.join(diagrams_dir, f"category-{cat_key}.mmd"))
        if content:
            # Check for edge filter metadata comment
            edge_filter_warning = ""
            for line in content.splitlines():
                if line.startswith("%% EDGE_FILTER:"):
                    parts = dict(kv.split("=") for kv in line[len("%% EDGE_FILTER:"):].strip().split())
                    hidden = int(parts.get("hidden", 0))
                    min_count = int(parts.get("min_count", 1))
                    total = int(parts.get("total", 0))
                    shown = int(parts.get("shown", 0))
                    edge_filter_warning = (
                        f"Showing {shown} of {total} edges (hiding {hidden} edges "
                        f"with fewer than {min_count} references to stay within rendering limits)"
                    )
                    break
            diagram_tabs.append({
                "id": f"cat_{sanitize_id(cat_key)}",
                "label": f"{cat_name} ({count})",
                "title": f"{cat_name} Projects ({count})",
                "mermaid": content,
                "warning": edge_filter_warning,
            })

    # ── Named diagram tabs (Data Flow, Business Layers, E2E, Field Trace) ──
    for mmd_name, tab_id, tab_label, tab_title in [
        ("data-flow.mmd", "dataflow", "Data Flow",
         "Data Flow — Projects Connected Through Data Infrastructure"),
        ("business-layers.mmd", "businesslayers", "Business Layers",
         "Business Layer Classification — Presentation / Engine / Service / DataAccess"),
        ("e2e-flows.mmd", "e2eflowsdiagram", "E2E Flows Diagram",
         "End-to-End Flow Paths — Screen to Pricer to Data"),
        ("field-traceability.mmd", "fieldtracediagram", "Field Trace Diagram",
         "Field Traceability — XAML Binding to Database Column"),
    ]:
        content = _read_text(os.path.join(diagrams_dir, mmd_name))
        if content and "no_data" not in content:
            diagram_tabs.append({
                "id": tab_id,
                "label": tab_label,
                "title": tab_title,
                "mermaid": content,
            })

    # ── Aggregate data sources by pattern ──
    pattern_summary: dict[str, dict] = {}
    for f in data_findings:
        p = f["pattern"]
        if p not in pattern_summary:
            pattern_summary[p] = {"type": f["type"], "count": 0, "projects": set()}
        pattern_summary[p]["count"] += 1
        proj = f.get("project") or ""
        if not proj:
            parts = os.path.normpath(f["file"]).split(os.sep)
            proj = parts[1 if is_multi_repo else 0] if len(parts) > (1 if is_multi_repo else 0) else parts[0]
        pattern_summary[p]["projects"].add(proj)

    # ── Connection strings ──
    conn_strings: list[dict] = []
    for c in configs:
        if c.get("connectionStrings"):
            for name, val in c["connectionStrings"].items():
                conn_strings.append({
                    "file": c["file"],
                    "repo": c.get("repo", ""),
                    "name": name,
                    "value": str(val)[:80],
                })

    # ── Build HTML ──
    # Stats bar
    stats_items = [
        (summary["totalProjects"], "Projects", "allprojects"),
        (summary["totalNuGetPackages"], "NuGet Packages", "allprojects"),
        (summary["totalProjectRefs"], "Project References", "allprojects"),
        (summary["totalDataFindings"], "Data Patterns", "datasources"),
        (summary["totalConfigFiles"], "Config Files", "connstrings"),
    ]
    if repo_count > 1:
        stats_items.append((repo_count, "Repos", "repos"))

    stats_html = "\n".join(
        f'    <div class="stat stat-link" onclick="activateTab(\'{tab}\')">'
        f'<span class="stat-value">{count}</span> {label}</div>'
        for count, label, tab in stats_items
    )

    # ── Implied dependencies from data flow ──
    implied_deps = data_flow.get("impliedDependencies", [])

    # ── Hotspot metrics ──
    hotspot_metrics = compute_hotspot_metrics()
    hotspot_json = _safe_json_for_script(hotspot_metrics)
    # Summary card data
    top_hotspot = hotspot_metrics[0] if hotspot_metrics else None
    most_referenced = max(hotspot_metrics, key=lambda m: m["fan_in"]) if hotspot_metrics else None
    most_cross_repo = max(hotspot_metrics, key=lambda m: m["cross_repo_refs"]) if hotspot_metrics else None

    # ── Code quality data ──
    refactoring_projects = refactoring_data.get("projects", [])
    refactoring_summary = refactoring_data.get("summary", {})
    claude_targets = refactoring_data.get("claudeCodeTargets", {})
    # Cap at 200 projects; include trimmed files[] for click-through evidence
    cq_projects_trimmed = []
    for _rp in refactoring_projects[:200]:
        entry = {
            k: v for k, v in _rp.items()
            if k in ("project", "repo", "category", "layer", "refactoring_value_score",
                     "smell_count", "top_smells", "total_lines", "total_files",
                     "has_tests", "complexity_score", "fan_in", "fan_out")
        }
        # Include trimmed files with smell evidence (max 50 files, 20 smells each)
        raw_files = _rp.get("files", [])
        trimmed_files = []
        for rf in sorted(raw_files, key=lambda f: -f.get("smell_count", 0))[:50]:
            smells = rf.get("smells", [])[:20]
            trimmed_smells = [{"type": s.get("type", ""), "line": s.get("line", 0),
                               "context": (s.get("context") or "")[:100],
                               "severity": s.get("severity", ""),
                               "category": s.get("category", "")} for s in smells]
            if trimmed_smells:
                trimmed_files.append({"file": rf.get("path", rf.get("file", "")),
                                      "smellCount": rf.get("smell_count", len(trimmed_smells)),
                                      "smells": trimmed_smells})
        if trimmed_files:
            entry["files"] = trimmed_files
        cq_projects_trimmed.append(entry)
    cq_embedded = _safe_json_for_script({
        "projects": cq_projects_trimmed,
        "summary": refactoring_summary,
        "claudeCodeTargets": claude_targets,
    })

    # ── Repo root lookup for file:// links ──
    repos_root_lookup = {r["name"]: r.get("root", "") for r in repos_data} if repos_data else {}
    repos_roots_json = _safe_json_for_script(repos_root_lookup)

    # ── UX inconsistency data ──
    ux_issues = ux_inconsistencies.get("issues", [])
    ux_summary = ux_inconsistencies.get("summary", {})
    ux_embedded = _safe_json_for_script({"issues": ux_issues, "summary": ux_summary})

    # ── External tools data ──
    _ext_all_findings = []
    for _et in external_tools_data.get("tools", {}).values():
        _ext_all_findings.extend(_et.get("findings", []))
    ext_tools_embedded = _safe_json_for_script({
        "findings": _ext_all_findings,
        "summary": external_tools_data.get("summary", {}),
        "toolsExecuted": external_tools_data.get("toolsExecuted", []),
        "toolsSkipped": external_tools_data.get("toolsSkipped", {}),
    })

    # ── NuGet health data ──
    nh_conflicts = nuget_health.get("versionConflicts", [])
    nh_legacy = nuget_health.get("legacyFormatProjects", [])
    nh_frameworks = nuget_health.get("targetFrameworks", {})
    nh_mixed_repos = nuget_health.get("mixedFrameworkRepos", {})
    nh_cpm = nuget_health.get("centralPackageManagement", {})
    nh_summary = nuget_health.get("summary", {})

    # Tab buttons
    all_tab_ids: list[tuple[str, str]] = []
    for dt in diagram_tabs:
        all_tab_ids.append((dt["id"], dt["label"]))
    if pattern_summary:
        all_tab_ids.append(("datasources", "Data Sources"))
    if implied_deps:
        all_tab_ids.append(("implieddeps", "Implied Dependencies"))
    if conn_strings:
        all_tab_ids.append(("connstrings", "Connection Strings"))
    if flow_paths_data.get("flowPaths"):
        all_tab_ids.append(("e2eflows", "E2E Flows"))
    if field_trace_data.get("fieldChains"):
        all_tab_ids.append(("fieldtrace", "Field Traceability"))
    if refactoring_projects:
        all_tab_ids.append(("codequality", "Code Quality"))
    # Security tab: show if any security-category smells exist (built-in or external tools)
    _has_security_findings = any(
        s.get("category") == "security"
        for _rp in refactoring_projects
        for _rf in _rp.get("files", [])
        for s in _rf.get("smells", [])
    ) or any(
        f.get("category") == "security"
        for _et in external_tools_data.get("tools", {}).values()
        for f in _et.get("findings", [])
    )
    if _has_security_findings:
        all_tab_ids.append(("security", "Security"))
    if ux_issues:
        all_tab_ids.append(("uxconsistency", "UX Consistency"))
    all_tab_ids.append(("hotspots", "Hotspots"))
    if nh_conflicts or nh_legacy:
        all_tab_ids.append(("nugethealth", "NuGet Health"))
    if test_data.get("testProjects"):
        all_tab_ids.append(("tests", "Tests"))
    # External Tools tab: show if any tool produced findings
    _ext_tools = external_tools_data.get("tools", {})
    _has_ext_findings = any(t.get("findingCount", 0) > 0 for t in _ext_tools.values())
    if _has_ext_findings:
        all_tab_ids.append(("externaltools", "External Tools"))
    # Dynamic language tabs
    for _lang_key, _lang_d in sorted(language_data.items()):
        _display = _lang_d.get("displayName", _lang_key.title())
        all_tab_ids.append((_lang_key, _display))
    if repo_count > 1:
        all_tab_ids.append(("repos", "Repos"))
    all_tab_ids.append(("allprojects", "All Projects"))

    tab_buttons = "\n".join(
        f'  <button class="tab-btn{" active" if i == 0 else ""}" data-tab="{tid}">{label}</button>'
        for i, (tid, label) in enumerate(all_tab_ids)
    )

    # Diagram panels
    legend_html = """
        <div class="diagram-legend">
          <div class="legend-title">Legend</div>
          <div class="legend-item"><span class="legend-icon">&#9632;</span> <strong>Boxes</strong> = project categories (number = project count)</div>
          <div class="legend-item"><span class="legend-icon">&#8594;</span> <strong>Arrows</strong> = cross-category references (number = reference count)</div>
          <div class="legend-item" style="margin-top:0.4rem;"><span class="legend-icon">&#9755;</span> Click <strong>arrow</strong> &rarr; see which projects reference each other</div>
          <div class="legend-item"><span class="legend-icon">&#9755;</span> Click <strong>box</strong> &rarr; jump to that category&#39;s detail tab</div>
        </div>"""
    category_detail_legend_html = """
        <div class="diagram-legend">
          <div class="legend-title">Legend</div>
          <div class="legend-item"><span class="legend-icon">&#9632;</span> <strong>Boxes</strong> in the colored rectangle are individual projects in this category</div>
          <div class="legend-item"><span class="legend-icon">&#9899;</span> <strong>Outside pills</strong> (e.g. &ldquo;Library (5)&rdquo;) = other categories with cross-category dependencies. The number is how many projects in that category connect to this diagram. Dashed arrows show which projects link.</div>
          <div class="legend-item"><span class="legend-icon">&#8594;</span> <strong>Solid arrow</strong> = direct project reference within this category</div>
          <div class="legend-item" style="margin-top:0.4rem;"><span class="legend-icon">&#9755;</span> Click <strong>pill</strong> &rarr; see the underlying project references</div>
          <div class="legend-item"><span class="legend-icon">&#9755;</span> Click <strong>arrow</strong> &rarr; see the actual references</div>
        </div>"""
    diagram_panels = ""
    for i, dt in enumerate(diagram_tabs):
        active = " active" if i == 0 else ""
        warning_html = ""
        if dt.get("warning"):
            warning_html = f'\n      <div class="edge-filter-warning">{_esc_html(dt["warning"])}</div>'
        if dt["id"] == "overview":
            side_legend = legend_html
        elif dt["id"].startswith("cat_"):
            side_legend = category_detail_legend_html
        else:
            side_legend = ""
        diagram_body = f"""
      <div class="diagram-with-legend">
        <div class="mermaid-wrap" id="mermaid-{dt['id']}">
          <span class="loading">Loading diagram...</span>
          <pre class="mermaid" style="display:none">
{_esc_html(dt['mermaid'])}
          </pre>
        </div>
        <div class="diagram-sidebar">
          {side_legend}
          <div class="edge-detail-panel" id="edgeDetail-{dt['id']}"></div>
        </div>
      </div>"""
        diagram_panels += f"""
  <section class="tab-panel{active}" id="panel-{dt['id']}">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> {dt['title']}
        <span class="zoom-controls">
          <button class="zoom-btn" onclick="zoomDiagram('mermaid-{dt['id']}', -0.2)" title="Zoom out">&#8722;</button>
          <button class="zoom-btn" onclick="zoomDiagram('mermaid-{dt['id']}', 0)" title="Reset zoom">Reset</button>
          <button class="zoom-btn" onclick="zoomDiagram('mermaid-{dt['id']}', 0.2)" title="Zoom in">&#43;</button>
        </span>
      </div>{warning_html}{diagram_body}
    </div>
  </section>
"""

    # Mermaid container map for JS
    mermaid_map_entries = ", ".join(
        f"'{dt['id']}': 'mermaid-{dt['id']}'" for dt in diagram_tabs
    )

    # Data sources panel
    datasources_panel = ""
    if pattern_summary:
        type_tag_class = {
            "database": "tag-db", "messaging": "tag-messaging",
            "api": "tag-api", "cache": "tag-cache", "config": "tag-config",
        }
        rows = ""
        for pattern, info in sorted(pattern_summary.items(), key=lambda x: -x[1]["count"]):
            tag_cls = type_tag_class.get(info["type"], "tag-config")
            type_label = info["type"].capitalize()
            projects_str = _esc_html(", ".join(sorted(info["projects"])[:5]))
            if len(info["projects"]) > 5:
                projects_str += f", ... +{len(info['projects']) - 5} more"
            rows += f"""            <tr>
              <td><strong>{_esc_html(pattern)}</strong></td>
              <td><span class="tag {tag_cls}">{type_label}</span></td>
              <td>{info['count']}</td>
              <td>{projects_str}</td>
            </tr>
"""
        datasources_panel = f"""
  <section class="tab-panel" id="panel-datasources">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Data Access Patterns</div>
      <div class="table-wrap">
        <table id="datasourcesTable">
          <thead>
            <tr><th data-sort-type="text" title="Code pattern or API detected (e.g. DbContext, HttpClient)">Pattern</th><th data-sort-type="text" title="Data access type: Database, API, Cache, Messaging, or Config">Type</th><th data-sort-type="num" title="Total times this pattern was found across all files">Occurrences</th><th data-sort-type="text" title="Projects where this pattern was found">Key Projects</th></tr>
          </thead>
          <tbody>
{rows}          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # Connection strings panel
    connstrings_panel = ""
    if conn_strings:
        rows = ""
        for cs in conn_strings:
            cs_file = cs['file']
            cs_repo = cs.get('repo', '')
            if cs_file:
                file_cell = _file_actions_html(cs_file)
            else:
                file_cell = _esc_html(cs_file)
            rows += f"""            <tr>
              <td class="mono">{file_cell}</td>
              <td>{_esc_html(cs_repo)}</td>
              <td>{_esc_html(cs['name'])}</td>
              <td class="mono">{_esc_html(cs['value'])}</td>
            </tr>
"""
        connstrings_panel = f"""
  <section class="tab-panel" id="panel-connstrings">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Connection Strings</div>
      <div class="table-wrap">
        <table id="connstringsTable">
          <thead>
            <tr><th data-sort-type="text" title="Configuration file path (appsettings.json, web.config, etc.)">Config File</th><th data-sort-type="text" title="Repository containing this config file">Repo</th><th data-sort-type="text" title="Name/key of the connection string entry">Connection Name</th><th data-sort-type="text" title="Connection string value (truncated to 80 characters)">Value</th></tr>
          </thead>
          <tbody>
{rows}          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # Implied dependencies panel
    implieddeps_panel = ""
    if implied_deps:
        infra_tag_class = {
            "database": "tag-db", "messaging": "tag-messaging", "api": "tag-api",
        }
        rows = ""
        for dep in implied_deps:
            tag_cls = infra_tag_class.get(dep.get("viaType", ""), "tag-config")
            via_label = _esc_html(dep.get("viaType", ""))
            rows += f"""            <tr>
              <td><strong>{_esc_html(dep['from'])}</strong></td>
              <td><strong>{_esc_html(dep['to'])}</strong></td>
              <td>{_esc_html(dep.get('via', ''))}</td>
              <td><span class="tag {tag_cls}">{via_label}</span></td>
              <td>writes &#8594; reads</td>
            </tr>
"""
        implieddeps_panel = f"""
  <section class="tab-panel" id="panel-implieddeps">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Implied Data Dependencies ({len(implied_deps)})</div>
      <p style="color:#53565A;font-size:0.85rem;margin-bottom:0.75rem;">
        Cross-project dependencies derived through shared data infrastructure.
        Project A writes to a data node, Project B reads from it &mdash; implying a data dependency A &rarr; B.
      </p>
      <div class="table-wrap">
        <table id="impliedDepsTable">
          <thead>
            <tr><th data-sort-type="text" title="Source project that writes to the shared endpoint">From</th><th data-sort-type="text" title="Target project that reads from the shared endpoint">To</th><th data-sort-type="text" title="Shared data endpoint creating the implicit dependency">Via (Endpoint)</th><th data-sort-type="text" title="Infrastructure type: Database, Messaging, API, Cache">Infrastructure</th><th data-sort-type="none" title="Direction of data flow: writes &#8594; reads">Relationship</th></tr>
          </thead>
          <tbody>
{rows}          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # E2E Flows panel
    e2eflows_panel = ""
    if flow_paths_data.get("flowPaths"):
        bl = flow_paths_data.get("businessLayers", {})
        fps = flow_paths_data.get("flowPaths", [])
        layer_sum = flow_paths_data.get("layerSummary", {})

        # Layer badges
        layer_colors = {
            "Presentation": "#621244", "Engine": "#36749D", "Service": "#008BCD",
            "DataAccess": "#005587", "Infrastructure": "#80276C", "Unclassified": "#53565A",
        }
        badges_html = ""
        for layer in ["Presentation", "Engine", "Service", "DataAccess", "Infrastructure", "Unclassified"]:
            info = layer_sum.get(layer, {})
            count = info.get("count", 0)
            if count == 0:
                continue
            color = layer_colors.get(layer, "#53565A")
            badges_html += (
                f'<span style="display:inline-block;padding:0.2rem 0.6rem;border-radius:12px;'
                f'background:rgba({_hex_to_rgb(color)},0.15);color:{color};font-size:0.78rem;'
                f'font-weight:600;margin-right:0.4rem;margin-bottom:0.3rem;">'
                f'{_esc_html(layer)}: {count}</span>'
            )

        # Flow paths table rows
        flow_rows = ""
        for i, fp in enumerate(fps[:100]):
            source = fp.get("source", {}).get("project", "?")
            layers_crossed = ", ".join(fp.get("crossesLayers", []))
            depth = fp.get("pathLength", 0)
            # Build short path chain
            chain_parts = []
            for step in fp.get("path", []):
                if "project" in step:
                    chain_parts.append(_esc_html(step["project"]))
                elif "endpoint" in step:
                    ep = step["endpoint"]
                    chain_parts.append(f'<em>{_esc_html(ep)}</em>')
            chain = " &rarr; ".join(chain_parts)
            named = _esc_html(fp.get("namedFlow", ""))

            flow_rows += f"""            <tr class="flow-row" data-flow-idx="{i}" data-search="{_esc_html(source.lower() + ' ' + layers_crossed.lower() + ' ' + named.lower())}">
              <td><strong>{_esc_html(source)}</strong></td>
              <td>{_esc_html(layers_crossed)}</td>
              <td style="text-align:center">{depth}</td>
              <td style="font-size:0.78rem">{chain}</td>
              <td>{named}</td>
            </tr>
"""

        e2eflows_panel = f"""
  <section class="tab-panel" id="panel-e2eflows">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> End-to-End Flow Paths ({len(fps)})</div>
      <p style="color:#53565A;font-size:0.85rem;margin-bottom:0.75rem;">
        Traces from UI screens through engines/services down to data endpoints.
        Click a row to see the full path detail with inline diagram.
      </p>
      <div style="margin-bottom:0.75rem;">{badges_html}</div>
      <input type="text" id="flowSearchInput" placeholder="Search flows..." style="
        width:100%;max-width:400px;padding:0.4rem 0.7rem;border-radius:6px;
        border:1px solid #E1E1E1;background:#FFFFFF;color:#000000;
        font-size:0.85rem;margin-bottom:0.75rem;outline:none;
      ">
      <div class="table-wrap">
        <table id="flowPathsTable">
          <thead>
            <tr><th data-sort-type="text" title="Starting UI screen or entry point of the flow">Source Screen</th><th data-sort-type="text" title="Business layers traversed by this flow">Layers Crossed</th><th data-sort-type="num" title="Number of project hops from source to deepest dependency">Depth</th><th data-sort-type="none" title="Visual chain of projects in this end-to-end flow">Path Chain</th><th data-sort-type="text" title="Named business flow grouping related paths">Named Flow</th></tr>
          </thead>
          <tbody id="flowPathsBody">
{flow_rows}          </tbody>
        </table>
      </div>
      <div id="flowDetailContainer" style="margin-top:1rem;display:none;">
        <div class="card" style="border-color:#005587;">
          <div class="card-title"><span class="icon">&#9670;</span> Flow Detail
            <button onclick="document.getElementById('flowDetailContainer').style.display='none'" style="margin-left:auto;background:none;border:1px solid #E1E1E1;color:#53565A;border-radius:4px;cursor:pointer;padding:0.1rem 0.5rem;font-size:0.8rem;">Close</button>
          </div>
          <div id="flowDetailContent"></div>
          <div class="mermaid-wrap" id="flowDetailMermaid" style="margin-top:0.75rem;"></div>
        </div>
      </div>
    </div>
  </section>
"""

    # Field Traceability panel
    fieldtrace_panel = ""
    if field_trace_data.get("fieldChains"):
        ft_chains = field_trace_data["fieldChains"]
        ft_summary = field_trace_data.get("summary", {})
        ft_breakdown = ft_summary.get("completenessBreakdown", {})

        # Summary badges
        badge_colors = {
            "full": ("#009639", "Full"),
            "xaml-to-entity": ("#9E8700", "XAML→Entity"),
            "xaml-to-viewmodel": ("#789D4A", "XAML→VM"),
            "entity-to-column": ("#005587", "Entity→DB"),
            "viewmodel-to-column": ("#80276C", "VM→DB"),
            "xaml-only": ("#53565A", "XAML Only"),
        }
        ft_badges_html = ""
        for level, (color, label) in badge_colors.items():
            count = ft_breakdown.get(level, 0)
            if count == 0:
                continue
            ft_badges_html += (
                f'<span class="ft-badge" data-filter="{level}" style="display:inline-block;padding:0.2rem 0.6rem;'
                f'border-radius:12px;background:rgba({_hex_to_rgb(color)},0.15);color:{color};'
                f'font-size:0.78rem;font-weight:600;margin-right:0.4rem;margin-bottom:0.3rem;cursor:pointer;">'
                f'{_esc_html(label)}: {count}</span>'
            )

        # Table rows
        ft_rows = ""
        for i, ch in enumerate(ft_chains[:500]):
            xaml = ch.get("xamlBinding") or {}
            vm = ch.get("viewModelProperty") or {}
            ent = ch.get("entityProperty") or {}
            db = ch.get("dbColumn") or {}
            comp = ch.get("chainCompleteness", "")
            conf = ch.get("confidence", "low")

            view_type = _esc_html(xaml.get("viewType", ""))
            binding_path = _esc_html(xaml.get("bindingPath", ""))
            vm_class = _esc_html(vm.get("className", ""))
            vm_prop = _esc_html(vm.get("propertyName", ""))
            ent_class = _esc_html(ent.get("className", ""))
            db_col = ""
            if db:
                table = _esc_html(db.get("table", ""))
                col = _esc_html(db.get("column", ""))
                db_col = f"{table}.{col}" if table and col else ""

            comp_color = {"full": "#009639", "xaml-to-entity": "#9E8700", "xaml-to-viewmodel": "#789D4A",
                         "entity-to-column": "#005587", "viewmodel-to-column": "#80276C", "xaml-only": "#53565A"}.get(comp, "#53565A")
            comp_label = badge_colors.get(comp, ("#53565A", comp))[1]

            search_text = f"{view_type} {binding_path} {vm_class} {vm_prop} {ent_class} {db_col} {comp}".lower()

            ft_rows += f"""            <tr class="ft-row" data-ft-idx="{i}" data-completeness="{comp}" data-search="{_esc_html(search_text)}">
              <td>{view_type}</td>
              <td><strong>{binding_path}</strong></td>
              <td>{vm_class}</td>
              <td>{vm_prop}</td>
              <td>{ent_class}</td>
              <td class="mono">{db_col}</td>
              <td><span style="color:{comp_color};font-size:0.75rem;font-weight:600;">{_esc_html(comp_label)}</span></td>
            </tr>
"""

        fieldtrace_panel = f"""
  <section class="tab-panel" id="panel-fieldtrace">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Field-Level Traceability ({ft_summary.get('totalChains', 0)} chains)</div>
      <p style="color:#53565A;font-size:0.85rem;margin-bottom:0.75rem;">
        Traces XAML bindings through ViewModel properties and entity classes to database columns.
        Click a row to see the full chain detail. Click a badge to filter by completeness level.
      </p>
      <div style="margin-bottom:0.75rem;">{ft_badges_html}</div>
      <input type="text" id="ftSearchInput" placeholder="Search fields..." style="
        width:100%;max-width:400px;padding:0.4rem 0.7rem;border-radius:6px;
        border:1px solid #E1E1E1;background:#FFFFFF;color:#000000;
        font-size:0.85rem;margin-bottom:0.75rem;outline:none;
      ">
      <div class="ft-layout">
        <div class="table-wrap" style="flex:1;min-width:0;">
          <table id="fieldTraceTable">
            <thead>
              <tr><th data-sort-type="text" title="XAML view/page file where the binding is defined">XAML View</th><th data-sort-type="text" title="Data binding path expression in the XAML markup">Binding Path</th><th data-sort-type="text" title="ViewModel class the XAML view binds to">ViewModel</th><th data-sort-type="text" title="Property on the ViewModel the binding resolves to">VM Property</th><th data-sort-type="text" title="Entity/model class that maps to a database table">Entity</th><th data-sort-type="text" title="Database table and column that stores this field">DB Table.Column</th><th data-sort-type="text" title="How complete the trace chain is (Full &#8594; XAML Only)">Completeness</th></tr>
            </thead>
            <tbody id="ftBody">
{ft_rows}            </tbody>
          </table>
        </div>
        <div class="ft-sidebar" id="ftDetailContainer" style="display:none;">
          <div style="border:1px solid #009639;border-radius:8px;padding:0.8rem;background:#FFFFFF;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;padding-bottom:0.5rem;border-bottom:1px solid #E1E1E1;">
              <strong style="font-size:0.85rem;color:#022D5E;">Field Chain Detail</strong>
              <button onclick="document.getElementById('ftDetailContainer').style.display='none'" style="background:none;border:1px solid #E1E1E1;color:#53565A;border-radius:4px;cursor:pointer;padding:0.1rem 0.5rem;font-size:0.8rem;">Close</button>
            </div>
            <div id="ftDetailContent"></div>
            <div class="mermaid-wrap" id="ftDetailMermaid" style="margin-top:0.75rem;"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

    # Category distribution panel (pie chart via Mermaid)
    cat_chart_mermaid = "pie title Project Categories\n"
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        cat_chart_mermaid += f'    "{cat}" : {count}\n'

    # Category map for JS-side category detection on Overview edges
    def _js_str(s: str) -> str:
        """Escape a string for safe embedding in a JS single-quoted literal."""
        return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r").replace("</", "<\\/")
    cat_map_entries = ", ".join(
        f"'{_js_str(cat_name)} ({count})': {{key:'{_js_str(cat_name.lower())}', name:'{_js_str(cat_name)}', count:{count}, tabId:'cat_{sanitize_id(cat_name.lower())}'}}"
        for cat_name, count in categories.items()
        if cat_name not in {"Localization", "Sample"}
    )

    # Repos panel
    repos_panel = ""
    if repo_count > 1:
        summary_repos = summary.get("repos", {})
        repos_lookup = {r["name"]: r for r in repos_data} if repos_data else {}
        repos_rows = ""
        for repo_name in sorted(summary_repos.keys()):
            info = summary_repos[repo_name]
            rd = repos_lookup.get(repo_name, {})
            proj_count = info.get("projects", 0)
            solutions = rd.get("solutions", [])
            sol_count = len(solutions)
            cats = ", ".join(sorted(info.get("categories", {}).keys()))
            root_path_raw = rd.get("root", "")
            root_path = _esc_html(root_path_raw)
            root_path_link = _file_actions_html(root_path_raw) if root_path_raw else root_path
            repos_rows += f"""            <tr>
              <td><strong>{_esc_html(repo_name)}</strong></td>
              <td>{proj_count}</td>
              <td>{sol_count}</td>
              <td>{_esc_html(cats)}</td>
              <td>{root_path_link}</td>
            </tr>
"""
        repos_panel = f"""
  <section class="tab-panel" id="panel-repos">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Repositories ({repo_count})</div>
      <div class="table-wrap">
        <table id="reposTable">
          <thead>
            <tr>
              <th data-sort-type="text" title="Repository name">Repo Name</th>
              <th data-sort-type="num" title="Number of .csproj projects in this repository">Projects</th>
              <th data-sort-type="num" title="Number of .sln solution files found">Solutions</th>
              <th data-sort-type="text" title="Functional categories of projects in this repo">Categories</th>
              <th data-sort-type="text" title="Root filesystem path of this repository">Root Path</th>
            </tr>
          </thead>
          <tbody>
{repos_rows}          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # All projects panel
    all_projects_panel = f"""
  <section class="tab-panel" id="panel-allprojects">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> All Projects</div>
      <div class="table-wrap">
        <table id="projectsTable">
          <thead>
            <tr>
              <th data-sort-type="text" title="Project name (.csproj)">Project</th>
              <th data-sort-type="text" title="Source repository this project belongs to">Repo</th>
              <th data-sort-type="text" title="Functional category (Application, Library, Service, etc.)">Category</th>
              <th data-sort-type="text" title="Architectural layer (Presentation, Engine, DataAccess, etc.)">Business Layer</th>
              <th data-sort-type="num" title="Other projects this project references via ProjectReference">Project Refs</th>
              <th data-sort-type="num" title="NuGet packages this project depends on via PackageReference">NuGet Deps</th>
              <th data-sort-type="text" title="Relative file path to the .csproj file">Path</th>
            </tr>
          </thead>
          <tbody id="projectsBody">
            <tr><td colspan="7" style="text-align:center;color:#53565A;padding:2rem;">Loading project data...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # ── Code Quality panel ──
    codequality_panel = ""
    if refactoring_projects:
        cq_total_smells = refactoring_summary.get("totalSmells", 0)
        cq_top_smell_types = refactoring_summary.get("topSmellTypes", [])
        cq_top_smell_name = cq_top_smell_types[0]["smell"] if cq_top_smell_types else "—"
        cq_top_smell_count = cq_top_smell_types[0]["count"] if cq_top_smell_types else 0
        cq_top_project = max(refactoring_projects, key=lambda p: p.get("smell_count", 0)) if refactoring_projects else {}
        cq_top_proj_name = _esc_html(cq_top_project.get("project", "—"))
        cq_top_proj_smells = cq_top_project.get("smell_count", 0)
        cq_files_scanned = refactoring_summary.get("totalFilesScanned", 0)
        cq_files_with = refactoring_summary.get("totalFilesWithSmells", 0)
        cq_files_ratio = f"{cq_files_with}/{cq_files_scanned}" if cq_files_scanned else "—"

        # Severity counts for summary cards
        cq_sev_counts = refactoring_summary.get("severityCounts", {})
        cq_critical_count = cq_sev_counts.get("critical", 0)
        cq_high_count = cq_sev_counts.get("high", 0)
        cq_medium_count = cq_sev_counts.get("medium", 0)
        cq_low_count = cq_sev_counts.get("low", 0)
        cq_scan_level = _esc_html(refactoring_summary.get("level", "high"))

        # Smell type badges
        cq_badge_html = ""
        for st in cq_top_smell_types:
            cq_badge_html += f'<button type="button" class="cq-badge" data-smell="{_esc_html(st["smell"])}">{_esc_html(st["smell"])}: {st["count"]}</button>\n        '

        # Severity filter badges
        cq_sev_badge_colors = {"critical": "#D0002B", "high": "#E87722", "medium": "#9E8700", "low": "#53565A"}
        cq_sev_badges_html = ""
        for sev in ["critical", "high", "medium", "low"]:
            cnt = cq_sev_counts.get(sev, 0)
            if cnt:
                c = cq_sev_badge_colors[sev]
                cq_sev_badges_html += f'<button type="button" class="cq-sev-badge" data-severity="{sev}" style="background:rgba({_hex_to_rgb(c)},0.15);color:{c};">{sev.title()}: {cnt}</button>\n        '

        # Refactoring targets (tier details)
        cq_tier_html = ""
        for tier_key, tier_label in [("tier1_critical", "Tier 1 Critical"), ("tier2_high", "Tier 2 High"), ("tier3_medium", "Tier 3 Medium")]:
            tier_items = claude_targets.get(tier_key, [])
            if not tier_items:
                continue
            items_html = ""
            for t in tier_items:
                files_list = ", ".join(t.get("files", [])[:5])
                if len(t.get("files", [])) > 5:
                    files_list += f" +{len(t['files']) - 5} more"
                effort_color = "#D0002B" if "large" in t.get("estimatedEffort", "").lower() else "#9E8700" if "medium" in t.get("estimatedEffort", "").lower() else "#009639"
                items_html += f"""<div style="margin-bottom:1rem;padding:0.75rem;background:#FAFAFA;border:1px solid #E1E1E1;border-radius:6px;">
              <div style="font-weight:700;">{_esc_html(t.get('project', ''))}</div>
              <div style="font-size:0.82rem;color:#53565A;margin:0.3rem 0;">{_esc_html(t.get('why', ''))}</div>
              <pre style="background:#F5F5F5;padding:0.5rem;border-radius:4px;font-size:0.78rem;overflow-x:auto;cursor:pointer;position:relative;" onclick="navigator.clipboard.writeText(this.textContent).then(function(){{var el=event.target.closest('pre');el.style.outline='2px solid #009639';setTimeout(function(){{el.style.outline='none';}},600);}})">{_esc_html(t.get('suggestedPrompt', ''))}</pre>
              <div style="display:flex;gap:0.5rem;align-items:center;margin-top:0.3rem;">
                <span style="display:inline-block;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:600;background:rgba({_hex_to_rgb(effort_color)},0.15);color:{effort_color};">{_esc_html(t.get('estimatedEffort', ''))}</span>
                <span style="font-size:0.75rem;color:#53565A;">Files: {_esc_html(files_list)}</span>
              </div>
            </div>
"""
            cq_tier_html += f"""<details style="margin-bottom:0.5rem;">
          <summary style="cursor:pointer;font-weight:600;padding:0.4rem 0;">{tier_label} ({len(tier_items)})</summary>
          <div style="padding:0.5rem 0;">
            {items_html}
          </div>
        </details>
"""

        codequality_panel = f"""
  <section class="tab-panel" id="panel-codequality">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Code Quality Analysis <span style="font-size:0.72rem;font-weight:400;color:#53565A;margin-left:0.5rem;">Level: {cq_scan_level}</span></div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
        <div style="flex:1;min-width:140px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Total Smells</div>
          <div style="font-size:1.1rem;font-weight:700;color:#D0002B;margin-top:0.2rem;">{cq_total_smells}</div>
        </div>
        <div style="flex:1;min-width:140px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#D0002B;text-transform:uppercase;letter-spacing:0.04em;">Critical</div>
          <div style="font-size:1.1rem;font-weight:700;color:#D0002B;margin-top:0.2rem;">{cq_critical_count}</div>
        </div>
        <div style="flex:1;min-width:140px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#E87722;text-transform:uppercase;letter-spacing:0.04em;">High</div>
          <div style="font-size:1.1rem;font-weight:700;color:#E87722;margin-top:0.2rem;">{cq_high_count}</div>
        </div>
        <div style="flex:1;min-width:140px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#9E8700;text-transform:uppercase;letter-spacing:0.04em;">Medium</div>
          <div style="font-size:1.1rem;font-weight:700;color:#9E8700;margin-top:0.2rem;">{cq_medium_count}</div>
        </div>
        <div style="flex:1;min-width:140px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Low</div>
          <div style="font-size:1.1rem;font-weight:700;color:#53565A;margin-top:0.2rem;">{cq_low_count}</div>
        </div>
      </div>
      <div id="cqFilterBar" style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;margin-bottom:0.75rem;">
        {cq_sev_badges_html}
        <span style="color:#E1E1E1;">|</span>
        {cq_badge_html}
        <select id="cqCategoryFilter" class="hs-dropdown"><option value="">All Categories</option></select>
        <select id="cqTestsFilter" class="hs-dropdown"><option value="">All</option><option value="true">Has Tests</option><option value="false">No Tests</option></select>
      </div>
      <div class="table-wrap">
        <table id="cqTable">
          <thead>
            <tr>
              <th data-sort-type="text" title="Project name">Project</th>
              <th data-sort-type="text" title="Project category">Category</th>
              <th data-sort-type="num" title="Refactoring value score">Score</th>
              <th data-sort-type="num" title="Number of code smells">Smells</th>
              <th data-sort-type="text" title="Most frequent smell type">Top Smell</th>
              <th data-sort-type="num" title="Total lines of code">Lines</th>
              <th data-sort-type="num" title="Complexity score">Complexity</th>
              <th data-sort-type="text" title="Whether the project has tests">Has Tests</th>
            </tr>
          </thead>
          <tbody id="cqBody">
          </tbody>
        </table>
      </div>
      {f'<div style="margin-top:1.5rem;"><div class="card-title"><span class="icon">&#9670;</span> Refactoring Targets</div>{cq_tier_html}</div>' if cq_tier_html else ''}
    </div>
  </section>
"""

    # ── Security panel ──
    security_panel = ""
    if _has_security_findings:
        # Count security findings by severity (built-in + external tools)
        _sec_critical = 0
        _sec_high = 0
        _sec_total = 0
        for _rp in refactoring_projects:
            for _rf in _rp.get("files", []):
                for _s in _rf.get("smells", []):
                    if _s.get("category") == "security":
                        _sec_total += 1
                        if _s.get("severity") == "critical":
                            _sec_critical += 1
                        elif _s.get("severity") == "high":
                            _sec_high += 1
        for _et in external_tools_data.get("tools", {}).values():
            for _ef in _et.get("findings", []):
                if _ef.get("category") == "security":
                    _sec_total += 1
                    if _ef.get("severity") == "critical":
                        _sec_critical += 1
                    elif _ef.get("severity") == "high":
                        _sec_high += 1

        security_panel = f"""
  <section class="tab-panel" id="panel-security">
    <div class="card">
      <div class="card-title"><span class="icon" style="color:#D0002B;">&#9888;</span> Security Findings</div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
        <div style="flex:1;min-width:180px;background:#FFF5F5;border:1px solid #FCA5A5;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#D0002B;text-transform:uppercase;letter-spacing:0.04em;">Critical</div>
          <div style="font-size:1.1rem;font-weight:700;color:#D0002B;margin-top:0.2rem;">{_sec_critical}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#FFF7ED;border:1px solid #FDBA74;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#E87722;text-transform:uppercase;letter-spacing:0.04em;">High</div>
          <div style="font-size:1.1rem;font-weight:700;color:#E87722;margin-top:0.2rem;">{_sec_high}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Total Security</div>
          <div style="font-size:1.1rem;font-weight:700;color:#53565A;margin-top:0.2rem;">{_sec_total}</div>
        </div>
      </div>
      <div class="table-wrap">
        <table id="securityTable">
          <thead>
            <tr>
              <th data-sort-type="text">File</th>
              <th data-sort-type="num">Line</th>
              <th data-sort-type="text">Detector</th>
              <th data-sort-type="text">Severity</th>
              <th data-sort-type="text">Context</th>
            </tr>
          </thead>
          <tbody id="securityBody">
          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # ── UX Consistency panel ──
    uxconsistency_panel = ""
    if ux_issues:
        ux_by_severity = ux_summary.get("bySeverity", {})
        ux_by_type = ux_summary.get("byType", {})
        ux_total = ux_summary.get("totalIssues", len(ux_issues))

        ux_severity_badges = ""
        sev_colors = {"error": "#D0002B", "warning": "#9E8700", "info": "#53565A"}
        for sev in ["error", "warning", "info"]:
            cnt = ux_by_severity.get(sev, 0)
            if cnt:
                c = sev_colors.get(sev, "#53565A")
                ux_severity_badges += f'<button type="button" class="ux-badge" data-severity="{sev}" style="background:rgba({_hex_to_rgb(c)},0.15);color:{c};">{sev.title()}: {cnt}</button>\n        '

        ux_type_badges = ""
        for typ, cnt in sorted(ux_by_type.items(), key=lambda x: -x[1]):
            ux_type_badges += f'<button type="button" class="ux-badge" data-type="{_esc_html(typ)}">{_esc_html(typ)}: {cnt}</button>\n        '

        uxconsistency_panel = f"""
  <section class="tab-panel" id="panel-uxconsistency">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> UX Consistency Analysis</div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Total Issues</div>
          <div style="font-size:1.1rem;font-weight:700;color:#D0002B;margin-top:0.2rem;">{ux_total}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Errors</div>
          <div style="font-size:1.1rem;font-weight:700;color:#D0002B;margin-top:0.2rem;">{ux_by_severity.get('error', 0)}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Warnings</div>
          <div style="font-size:1.1rem;font-weight:700;color:#9E8700;margin-top:0.2rem;">{ux_by_severity.get('warning', 0)}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Info</div>
          <div style="font-size:1.1rem;font-weight:700;color:#53565A;margin-top:0.2rem;">{ux_by_severity.get('info', 0)}</div>
        </div>
      </div>
      <div id="uxFilterBar" style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;margin-bottom:0.75rem;">
        {ux_severity_badges}
        {ux_type_badges}
      </div>
      <div class="table-wrap">
        <table id="uxTable">
          <thead>
            <tr>
              <th data-sort-type="text" title="Issue severity">Severity</th>
              <th data-sort-type="text" title="Issue type">Type</th>
              <th data-sort-type="text" title="Project name">Project</th>
              <th data-sort-type="text" title="Source file">File</th>
              <th data-sort-type="text" title="View or class involved">View/Class</th>
              <th data-sort-type="text" title="Issue description">Message</th>
            </tr>
          </thead>
          <tbody id="uxBody">
          </tbody>
        </table>
      </div>
      <div id="uxDetailSidebar" style="display:none;margin-top:1rem;padding:1rem;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;">
      </div>
    </div>
  </section>
"""

    # ── NuGet Health panel ──
    nugethealth_panel = ""
    if nh_conflicts or nh_legacy:
        # Build conflict table rows server-side
        nh_conflict_rows = ""
        for vc in nh_conflicts:
            pkg = _esc_html(vc.get("package", ""))
            ver_count = vc.get("versionCount", 0)
            proj_count = vc.get("projectCount", 0)
            versions_detail = ""
            for ver, projs in sorted(vc.get("versions", {}).items()):
                proj_list = ", ".join(_esc_html(p) for p in projs[:10])
                if len(projs) > 10:
                    proj_list += f" +{len(projs) - 10} more"
                versions_detail += f"<div style='margin:0.3rem 0;'><strong>{_esc_html(ver)}</strong>: {proj_list}</div>"
            nh_conflict_rows += f"""<tr>
              <td><strong>{pkg}</strong></td>
              <td style="text-align:center">{ver_count}</td>
              <td style="text-align:center">{proj_count}</td>
              <td><details><summary style="cursor:pointer;font-size:0.82rem;">Show versions</summary><div style="padding:0.4rem 0;font-size:0.8rem;">{versions_detail}</div></details></td>
            </tr>
"""

        # Build legacy table rows
        nh_legacy_rows = ""
        for lp in nh_legacy:
            nh_legacy_rows += f"""<tr>
              <td>{_esc_html(lp.get('project', ''))}</td>
              <td>{_esc_html(lp.get('repo', ''))}</td>
              <td class="mono">{_esc_html(lp.get('path', ''))}</td>
              <td><span style="display:inline-block;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:600;background:rgba(158,135,0,0.15);color:#9E8700;">packages.config</span></td>
            </tr>
"""

        # Build framework badges
        nh_fw_html = ""
        for fw, projs in sorted(nh_frameworks.items()):
            fw_lower = fw.lower()
            if "net8" in fw_lower or "net9" in fw_lower or "net10" in fw_lower:
                fw_color = "#009639"
            elif "net4" in fw_lower or "net3" in fw_lower:
                fw_color = "#9E8700"
            elif "netstandard" in fw_lower:
                fw_color = "#005587"
            else:
                fw_color = "#53565A"
            nh_fw_html += f'<span style="display:inline-block;padding:0.2rem 0.6rem;border-radius:12px;font-size:0.78rem;font-weight:600;background:rgba({_hex_to_rgb(fw_color)},0.15);color:{fw_color};margin:0.2rem;">{_esc_html(fw)}: {len(projs)}</span>\n'

        # Mixed framework repos
        nh_mixed_html = ""
        if nh_mixed_repos:
            nh_mixed_html = '<div style="margin-top:0.5rem;"><strong>Mixed-Framework Repos:</strong><ul style="margin:0.3rem 0;padding-left:1.2rem;">'
            for repo, fws in sorted(nh_mixed_repos.items()):
                nh_mixed_html += f'<li style="font-size:0.85rem;">{_esc_html(repo)}: {", ".join(_esc_html(f) for f in fws)}</li>'
            nh_mixed_html += '</ul></div>'

        # CPM status badges
        nh_cpm_html = ""
        if nh_cpm:
            for repo, enabled in sorted(nh_cpm.items()):
                icon = "&#10003;" if enabled else "&#10007;"
                color = "#009639" if enabled else "#D0002B"
                nh_cpm_html += f'<span style="display:inline-block;padding:0.2rem 0.6rem;border-radius:12px;font-size:0.78rem;font-weight:600;background:rgba({_hex_to_rgb(color)},0.15);color:{color};margin:0.2rem;">{icon} {_esc_html(repo)}</span>\n'

        nugethealth_panel = f"""
  <section class="tab-panel" id="panel-nugethealth">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> NuGet Health</div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Version Conflicts</div>
          <div style="font-size:1.1rem;font-weight:700;color:#D0002B;margin-top:0.2rem;">{nh_summary.get('conflictCount', len(nh_conflicts))}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Legacy Projects</div>
          <div style="font-size:1.1rem;font-weight:700;color:#9E8700;margin-top:0.2rem;">{nh_summary.get('legacyCount', len(nh_legacy))}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Frameworks</div>
          <div style="font-size:1.1rem;font-weight:700;color:#005587;margin-top:0.2rem;">{nh_summary.get('frameworkCount', len(nh_frameworks))}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">CPM Repos</div>
          <div style="font-size:1.1rem;font-weight:700;color:#009639;margin-top:0.2rem;">{nh_summary.get('cpmRepos', sum(1 for v in nh_cpm.values() if v))}</div>
        </div>
      </div>
      {"<h3 style='margin:1rem 0 0.5rem;'>Version Conflicts</h3>" + '<div class="table-wrap"><table id="nhConflictsTable"><thead><tr><th data-sort-type="text">Package</th><th data-sort-type="num">Versions</th><th data-sort-type="num">Projects</th><th data-sort-type="none">Details</th></tr></thead><tbody>' + nh_conflict_rows + '</tbody></table></div>' if nh_conflict_rows else ''}
      {"<h3 style='margin:1rem 0 0.5rem;'>Legacy Format Projects</h3>" + '<div class="table-wrap"><table id="nhLegacyTable"><thead><tr><th data-sort-type="text">Project</th><th data-sort-type="text">Repo</th><th data-sort-type="text">Path</th><th data-sort-type="none">Format</th></tr></thead><tbody>' + nh_legacy_rows + '</tbody></table></div>' if nh_legacy_rows else ''}
      {"<h3 style='margin:1rem 0 0.5rem;'>Target Frameworks</h3><div style='display:flex;flex-wrap:wrap;gap:0.3rem;'>" + nh_fw_html + "</div>" + nh_mixed_html if nh_fw_html else ''}
      {"<h3 style='margin:1rem 0 0.5rem;'>Central Package Management</h3><div style='display:flex;flex-wrap:wrap;gap:0.3rem;'>" + nh_cpm_html + "</div>" if nh_cpm_html else ''}
    </div>
  </section>
"""

    # Hotspots panel
    hs_top_name = _esc_html(top_hotspot["project"]) if top_hotspot else "—"
    hs_top_score = top_hotspot["hotspot_score"] if top_hotspot else 0
    hs_ref_name = _esc_html(most_referenced["project"]) if most_referenced else "—"
    hs_ref_val = most_referenced["fan_in"] if most_referenced else 0
    hs_xr_name = _esc_html(most_cross_repo["project"]) if most_cross_repo else "—"
    hs_xr_val = most_cross_repo["cross_repo_refs"] if most_cross_repo else 0
    hotspots_panel = f"""
  <section class="tab-panel" id="panel-hotspots">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Hotspot Analysis</div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Top Hotspot</div>
          <div style="font-size:1.1rem;font-weight:700;color:#D0002B;margin-top:0.2rem;">{hs_top_name}</div>
          <div style="font-size:0.8rem;color:#53565A;">Score: {hs_top_score}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Most Referenced</div>
          <div style="font-size:1.1rem;font-weight:700;color:#005587;margin-top:0.2rem;">{hs_ref_name}</div>
          <div style="font-size:0.8rem;color:#53565A;">Fan-in: {hs_ref_val}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Most Cross-Repo</div>
          <div style="font-size:1.1rem;font-weight:700;color:#789D4A;margin-top:0.2rem;">{hs_xr_name}</div>
          <div style="font-size:0.8rem;color:#53565A;">Cross-repo refs: {hs_xr_val}</div>
        </div>
      </div>
      <p style="color:#53565A;font-size:0.85rem;margin-bottom:0.75rem;">
        Projects ranked by coupling complexity &mdash; where AI help has most impact.
        Score = Fan-Out&times;3 + Fan-In&times;2 + NuGet + Data&nbsp;Patterns + Cross-Repo&times;4
      </p>
      <div id="hsFilterBar" style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;margin-bottom:0.75rem;">
        <button type="button" class="hs-badge" data-filter="red">Risk: 0</button>
        <button type="button" class="hs-badge" data-filter="yellow">Watch: 0</button>
        <button type="button" class="hs-badge" data-filter="green">Stable: 0</button>
        <button type="button" class="hs-badge" data-filter="none">None: 0</button>
        <select id="hsCategoryFilter" class="hs-dropdown"><option value="">All Categories</option></select>
        <select id="hsLayerFilter" class="hs-dropdown"><option value="">All Layers</option></select>
      </div>
      <div class="table-wrap">
        <table id="hotspotsTable">
          <thead>
            <tr>
              <th data-sort-type="text" title="Project name (.csproj)">Project</th>
              <th data-sort-type="text" title="Functional category (Application, Library, Service, etc.)">Category</th>
              <th data-sort-type="text" title="Business layer with confidence indicator">Layer</th>
              <th data-sort-type="num" title="Projects this one depends on (outgoing references)">Fan-Out</th>
              <th data-sort-type="num" title="Projects that depend on this one (incoming references)">Fan-In</th>
              <th data-sort-type="num" title="Distinct NuGet packages referenced">NuGet</th>
              <th data-sort-type="num" title="Data access patterns found (SQL, ORM, HTTP, etc.)">Data Patterns</th>
              <th data-sort-type="num" title="References crossing repository boundaries">Cross-Repo</th>
              <th data-sort-type="num" title="Raw weighted coupling score: Fan-Out&#215;3 + Fan-In&#215;2 + NuGet + Data Patterns + Cross-Repo&#215;4">Score</th>
              <th data-sort-type="num" title="Risk-adjusted score: discounts expected patterns (Library fan-in) and factors in code smells">Risk Score</th>
              <th data-sort-type="risk" title="Risk level based on hotspot score and code smells">Risk</th>
            </tr>
          </thead>
          <tbody id="hotspotsBody">
          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # ── Tests panel ──
    tests_panel = ""
    test_projects_list = test_data.get("testProjects", [])
    test_summary = test_data.get("summary", {})
    if test_projects_list:
        t_total = test_summary.get("totalTestProjects", 0)
        t_methods = test_summary.get("totalTestMethods", 0)
        t_coverage = test_summary.get("coverageRatio", "0/0")
        # Detect frameworks
        fw_counts: dict[str, int] = {}
        for tp in test_projects_list:
            fw = tp.get("testFramework", "unknown")
            fw_counts[fw] = fw_counts.get(fw, 0) + 1
        fw_str = ", ".join(f"{fw}: {cnt}" for fw, cnt in sorted(fw_counts.items(), key=lambda x: -x[1]))

        # Test project rows
        test_rows = ""
        for tp in sorted(test_projects_list, key=lambda t: -t.get("testMethodCount", 0)):
            covers = ", ".join(tp.get("covers", [])[:5])
            if len(tp.get("covers", [])) > 5:
                covers += f" +{len(tp['covers']) - 5} more"
            fw_color = {"xUnit": "#005587", "NUnit": "#009639", "MSTest": "#80276C"}.get(tp.get("testFramework", ""), "#53565A")
            test_rows += f"""            <tr>
              <td><strong>{_esc_html(tp.get('project', ''))}</strong></td>
              <td>{_esc_html(tp.get('repo', ''))}</td>
              <td><span style="display:inline-block;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:600;background:rgba({_hex_to_rgb(fw_color)},0.15);color:{fw_color};">{_esc_html(tp.get('testFramework', ''))}</span></td>
              <td style="text-align:center">{tp.get('testClassCount', 0)}</td>
              <td style="text-align:center">{tp.get('testMethodCount', 0)}</td>
              <td style="font-size:0.82rem;">{_esc_html(covers)}</td>
            </tr>
"""

        # Uncovered projects
        uncovered = test_data.get("uncoveredProjects", [])
        uncovered_html = ""
        if uncovered:
            uncovered_badges = "".join(
                f'<span style="display:inline-block;padding:0.15rem 0.5rem;margin:0.15rem;border-radius:4px;font-size:0.78rem;background:rgba(208,0,43,0.1);color:#D0002B;">{_esc_html(p)}</span>'
                for p in uncovered[:50]
            )
            if len(uncovered) > 50:
                uncovered_badges += f'<span style="color:#53565A;font-size:0.8rem;margin-left:0.3rem;">+{len(uncovered) - 50} more</span>'
            uncovered_html = f'<div style="margin-top:1rem;"><h3 style="margin:0 0 0.5rem;color:#022D5E;font-size:0.95rem;">Uncovered Projects ({len(uncovered)})</h3><div style="display:flex;flex-wrap:wrap;gap:0.2rem;">{uncovered_badges}</div></div>'

        tests_panel = f"""
  <section class="tab-panel" id="panel-tests">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Test Coverage</div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Test Projects</div>
          <div style="font-size:1.1rem;font-weight:700;color:#005587;margin-top:0.2rem;">{t_total}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Test Methods</div>
          <div style="font-size:1.1rem;font-weight:700;color:#009639;margin-top:0.2rem;">{t_methods}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Coverage Ratio</div>
          <div style="font-size:1.1rem;font-weight:700;color:#9E8700;margin-top:0.2rem;">{_esc_html(t_coverage)}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Frameworks</div>
          <div style="font-size:0.88rem;font-weight:600;color:#53565A;margin-top:0.2rem;">{_esc_html(fw_str)}</div>
        </div>
      </div>
      <div class="table-wrap">
        <table id="testsTable">
          <thead>
            <tr>
              <th data-sort-type="text" title="Test project name">Test Project</th>
              <th data-sort-type="text" title="Repository">Repo</th>
              <th data-sort-type="text" title="Testing framework">Framework</th>
              <th data-sort-type="num" title="Number of test classes">Classes</th>
              <th data-sort-type="num" title="Number of test methods">Methods</th>
              <th data-sort-type="text" title="Projects covered by this test project">Covers</th>
            </tr>
          </thead>
          <tbody>
{test_rows}          </tbody>
        </table>
      </div>
      {uncovered_html}
    </div>
  </section>
"""

    # ── Language panels (dynamic, from scanner plugins) ──
    language_panels = ""
    for _lk, _ld in sorted(language_data.items()):
        _ldisp = _ld.get("displayName", _lk.title())
        _lprojs = _ld.get("projects", [])
        _lsum = _ld.get("summary", {})
        _lfiles = _lsum.get("totalFiles", 0)
        _llines = _lsum.get("totalLines", 0)
        _lfws = _lsum.get("frameworks", {})
        _lcats = _lsum.get("categories", {})

        # Framework badges
        _fw_badge_html = ""
        _fw_colors = {"Django": "#0C4B33", "Flask": "#000000", "FastAPI": "#009485",
                      "pytest": "#009639", "Celery": "#37822E", "Airflow": "#017CEE"}
        for fw, cnt in sorted(_lfws.items(), key=lambda x: -x[1]):
            _fwc = _fw_colors.get(fw, "#005587")
            _fw_badge_html += f'<span style="display:inline-block;padding:0.15rem 0.5rem;border-radius:12px;font-size:0.78rem;font-weight:600;background:rgba({_hex_to_rgb(_fwc)},0.15);color:{_fwc};margin:0.15rem;">{_esc_html(fw)}: {cnt}</span>\n'

        # Table rows
        _lang_rows = ""
        for _lp in sorted(_lprojs, key=lambda p: -(p.get("lineCount", 0))):
            _dep_list = ", ".join(_lp.get("dependencies", [])[:8])
            if len(_lp.get("dependencies", [])) > 8:
                _dep_list += f" +{len(_lp['dependencies']) - 8} more"
            _cat_lower = (_lp.get("category") or "").lower()
            _tag_class = f"tag-{_cat_lower}" if _cat_lower else "tag-unclassified"
            _lang_rows += f"""            <tr>
              <td><strong>{_esc_html(_lp.get('name', ''))}</strong></td>
              <td>{_esc_html(_lp.get('repo', ''))}</td>
              <td><span class="tag {_tag_class}">{_esc_html(_lp.get('category', ''))}</span></td>
              <td>{_esc_html(_lp.get('framework', '') or '—')}</td>
              <td style="text-align:center">{_lp.get('fileCount', 0)}</td>
              <td style="text-align:center">{_lp.get('lineCount', 0):,}</td>
              <td style="font-size:0.8rem;"><details><summary style="cursor:pointer;font-size:0.8rem;">{len(_lp.get('dependencies', []))} deps</summary><div style="padding:0.3rem 0;font-size:0.78rem;">{_esc_html(_dep_list)}</div></details></td>
              <td style="text-align:center">{'<span style="color:#009639">&#10003;</span>' if _lp.get('hasTests') else '<span style="color:#D0002B">&#10007;</span>'}</td>
            </tr>
"""

        language_panels += f"""
  <section class="tab-panel" id="panel-{_lk}">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> {_esc_html(_ldisp)} Projects ({len(_lprojs)})</div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Projects</div>
          <div style="font-size:1.1rem;font-weight:700;color:#005587;margin-top:0.2rem;">{len(_lprojs)}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Total Files</div>
          <div style="font-size:1.1rem;font-weight:700;color:#009639;margin-top:0.2rem;">{_lfiles:,}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Total Lines</div>
          <div style="font-size:1.1rem;font-weight:700;color:#9E8700;margin-top:0.2rem;">{_llines:,}</div>
        </div>
        <div style="flex:1;min-width:180px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Frameworks</div>
          <div style="display:flex;flex-wrap:wrap;gap:0.2rem;margin-top:0.2rem;">{_fw_badge_html or '<span style="color:#53565A;">—</span>'}</div>
        </div>
      </div>
      <div class="table-wrap">
        <table id="{_lk}Table">
          <thead>
            <tr>
              <th data-sort-type="text" title="Project name">Project</th>
              <th data-sort-type="text" title="Repository">Repo</th>
              <th data-sort-type="text" title="Project category">Category</th>
              <th data-sort-type="text" title="Detected framework">Framework</th>
              <th data-sort-type="num" title="Number of source files">Files</th>
              <th data-sort-type="num" title="Lines of code">Lines</th>
              <th data-sort-type="num" title="Dependencies">Deps</th>
              <th data-sort-type="text" title="Has test suite">Tests</th>
            </tr>
          </thead>
          <tbody>
{_lang_rows}          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # ── External Tools panel ──
    externaltools_panel = ""
    if _has_ext_findings:
        _ext_summary = external_tools_data.get("summary", {})
        _ext_total = _ext_summary.get("totalFindings", 0)
        _ext_by_sev = _ext_summary.get("findingsBySeverity", {})
        _ext_by_tool = _ext_summary.get("findingsByTool", {})
        _ext_skipped = external_tools_data.get("toolsSkipped", {})

        # Severity summary cards
        _ext_crit = _ext_by_sev.get("critical", 0)
        _ext_high = _ext_by_sev.get("high", 0)
        _ext_med = _ext_by_sev.get("medium", 0)
        _ext_low = _ext_by_sev.get("low", 0)

        # Tool badges
        _ext_tool_badges = ""
        _tool_colors = {"semgrep": "#4B11A8", "bandit": "#D0002B", "detect-secrets": "#9E8700", "radon": "#005587"}
        for _tn, _tc in sorted(_ext_by_tool.items(), key=lambda x: -x[1]):
            _tcolor = _tool_colors.get(_tn, "#53565A")
            _ext_tool_badges += f'<button type="button" class="ext-tool-badge" data-tool="{_esc_html(_tn)}" style="display:inline-block;padding:0.15rem 0.5rem;border-radius:12px;font-size:0.78rem;font-weight:600;background:rgba({_hex_to_rgb(_tcolor)},0.15);color:{_tcolor};margin:0.15rem;border:none;cursor:pointer;">{_esc_html(_tn)}: {_tc}</button>\n'

        # Skipped tools notice
        _skip_notice = ""
        if _ext_skipped:
            _skip_items = ", ".join(f"{k} ({v})" for k, v in _ext_skipped.items())
            _skip_notice = f'<div style="margin-bottom:0.75rem;padding:0.5rem 0.75rem;background:#FFF7ED;border:1px solid #FDBA74;border-radius:6px;font-size:0.82rem;color:#9E8700;">Skipped: {_esc_html(_skip_items)}</div>'

        externaltools_panel = f"""
  <section class="tab-panel" id="panel-externaltools">
    <div class="card">
      <div class="card-title"><span class="icon" style="color:#4B11A8;">&#9881;</span> External Tool Findings</div>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
        <div style="flex:1;min-width:140px;background:#FFF5F5;border:1px solid #FCA5A5;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#D0002B;text-transform:uppercase;letter-spacing:0.04em;">Critical</div>
          <div style="font-size:1.1rem;font-weight:700;color:#D0002B;margin-top:0.2rem;">{_ext_crit}</div>
        </div>
        <div style="flex:1;min-width:140px;background:#FFF7ED;border:1px solid #FDBA74;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#E87722;text-transform:uppercase;letter-spacing:0.04em;">High</div>
          <div style="font-size:1.1rem;font-weight:700;color:#E87722;margin-top:0.2rem;">{_ext_high}</div>
        </div>
        <div style="flex:1;min-width:140px;background:#FFFDE7;border:1px solid #FFF176;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#9E8700;text-transform:uppercase;letter-spacing:0.04em;">Medium</div>
          <div style="font-size:1.1rem;font-weight:700;color:#9E8700;margin-top:0.2rem;">{_ext_med}</div>
        </div>
        <div style="flex:1;min-width:140px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Low</div>
          <div style="font-size:1.1rem;font-weight:700;color:#53565A;margin-top:0.2rem;">{_ext_low}</div>
        </div>
        <div style="flex:1;min-width:140px;background:#F5F5F5;border:1px solid #E1E1E1;border-radius:8px;padding:0.75rem 1rem;">
          <div style="font-size:0.72rem;color:#53565A;text-transform:uppercase;letter-spacing:0.04em;">Total</div>
          <div style="font-size:1.1rem;font-weight:700;color:#53565A;margin-top:0.2rem;">{_ext_total}</div>
        </div>
      </div>
      <div style="margin-bottom:0.75rem;">{_ext_tool_badges}</div>
      {_skip_notice}
      <div class="table-wrap">
        <table id="extToolsTable">
          <thead>
            <tr>
              <th data-sort-type="text">Tool</th>
              <th data-sort-type="text">File</th>
              <th data-sort-type="num">Line</th>
              <th data-sort-type="text">Rule</th>
              <th data-sort-type="text">Severity</th>
              <th data-sort-type="text">Category</th>
              <th data-sort-type="text">Message</th>
            </tr>
          </thead>
          <tbody id="extToolsBody">
          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc_html(title)} — Dependency Map</title>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{ startOnLoad: false, theme: 'default', securityLevel: 'loose', maxTextSize: 200000, maxEdges: 600 }});
  window.mermaidAPI = mermaid;
</script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ font-size: 15px; scroll-behavior: smooth; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: #FFFFFF; color: #000000; line-height: 1.6; min-height: 100vh;
  }}
  a {{ color: #005587; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .header {{
    background: linear-gradient(135deg, #022D5E 0%, #005587 100%);
    border-bottom: 1px solid #E1E1E1; padding: 1.5rem 2rem 1rem;
  }}
  .header-top {{
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;
  }}
  .header h1 {{ font-size: 1.6rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em; }}
  .header h1 span {{ color: #FFFFFF; }}
  .search-box {{ position: relative; width: 280px; }}
  .search-box input {{
    width: 100%; padding: 0.5rem 0.75rem 0.5rem 2.2rem; border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.15); color: #FFFFFF;
    font-size: 0.875rem; outline: none; transition: border-color .2s;
  }}
  .search-box input::placeholder {{ color: rgba(255,255,255,0.6); }}
  .search-box input:focus {{ border-color: #FFFFFF; }}
  .search-box .search-icon {{
    position: absolute; left: 0.65rem; top: 50%; transform: translateY(-50%);
    color: rgba(255,255,255,0.6); font-size: 0.85rem; pointer-events: none;
  }}
  .stats-row {{ display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; margin-bottom: 0.75rem; }}
  .stat {{ display: flex; align-items: center; gap: 0.4rem; font-size: 0.8rem; color: rgba(255,255,255,0.7); }}
  .stat-value {{ font-weight: 700; font-size: 1rem; color: #FFFFFF; }}
  .stat-link {{ cursor: pointer; padding: 0.25rem 0.6rem; border-radius: 6px; transition: background .15s; }}
  .stat-link:hover {{ background: rgba(255,255,255,0.15); }}
  .tabs {{
    display: flex; flex-wrap: wrap; gap: 0.25rem; padding: 0 2rem;
    background: #FFFFFF; border-bottom: 1px solid #E1E1E1;
  }}
  .tab-btn {{
    padding: 0.6rem 1rem; background: transparent; border: none; color: #53565A;
    font-size: 0.82rem; font-weight: 500; cursor: pointer;
    border-bottom: 2px solid transparent; transition: color .2s, border-color .2s; white-space: nowrap;
  }}
  .tab-btn:hover {{ color: #000000; }}
  .tab-btn.active {{ color: #005587; border-bottom-color: #005587; }}
  .content {{ padding: 1.5rem 2rem 3rem; }}
  .tab-panel {{ display: none; }}
  .tab-panel.active {{ display: block; }}
  .card {{
    background: #FFFFFF; border: 1px solid #E1E1E1; border-radius: 10px;
    padding: 1.25rem 1.5rem; margin-bottom: 1.25rem;
  }}
  .card-title {{
    font-size: 1.05rem; font-weight: 600; color: #022D5E; margin-bottom: 0.75rem;
    display: flex; align-items: center; gap: 0.5rem;
  }}
  .card-title .icon {{ color: #005587; }}
  .card-title {{ justify-content: flex-start; }}
  .zoom-controls {{ margin-left: auto; display: flex; gap: 0.25rem; }}
  .zoom-btn {{
    background: #FFFFFF; border: 1px solid #E1E1E1; color: #53565A; border-radius: 4px;
    padding: 0.15rem 0.5rem; font-size: 0.75rem; cursor: pointer; line-height: 1.2;
  }}
  .zoom-btn:hover {{ color: #000000; border-color: #005587; }}
  .edge-filter-warning {{
    background: #FFF8E1; color: #9E8700; border: 1px solid #FFD100; border-radius: 6px;
    padding: 0.5rem 0.75rem; margin: 0.5rem 0; font-size: 0.85rem;
  }}
  .diagram-with-legend {{ display:flex; gap:1rem; align-items:flex-start; }}
  .diagram-with-legend .mermaid-wrap {{ flex:1; min-width:0; }}
  .diagram-sidebar {{ width:320px; flex-shrink:0; display:flex; flex-direction:column; gap:0.75rem; }}
  .diagram-legend {{ width:100%; background:#FFFFFF; border:1px solid #E1E1E1; border-radius:8px; padding:0.6rem 0.8rem; font-size:0.78rem; color:#333333; }}
  .diagram-legend .legend-title {{ font-weight:600; color:#022D5E; margin-bottom:0.4rem; font-size:0.82rem; }}
  .diagram-legend .legend-item {{ margin-bottom:0.3rem; line-height:1.35; }}
  .diagram-legend .legend-icon {{ display:inline-block; width:1.1rem; color:#005587; text-align:center; }}
  .cat-nav-btn {{ background:#F5F5F5; border:1px solid #E1E1E1; color:#022D5E; border-radius:6px; padding:0.3rem 0.7rem; font-size:0.8rem; cursor:pointer; }}
  .cat-nav-btn:hover {{ background:#E1E1E1; }}
  .mermaid-wrap {{
    background: #f8fafc; border-radius: 8px; padding: 1rem; overflow: auto;
    min-height: 120px; max-height: 80vh;
  }}
  .mermaid-wrap .loading {{ color: #53565A; font-size: 0.9rem; text-align: center; }}
  .mermaid-wrap svg {{ max-width: none !important; height: auto; transform-origin: top left; }}
  .flowchart-link {{ transition: stroke 0.15s, stroke-width 0.15s, opacity 0.15s; }}
  .edge-hover-target {{ stroke: transparent; stroke-width: 15px; fill: none; cursor: pointer; pointer-events: stroke; }}
  .flowchart-link.edge-highlight {{ stroke: #005587 !important; stroke-width: 3px !important; }}
  .edgePaths:has(.flowchart-link:hover) .flowchart-link:not(:hover) {{ opacity: 0.15; }}
  .edge-tooltip {{
    position: fixed; background: #FFFFFF; color: #000000; border: 1px solid #005587;
    border-radius: 6px; padding: 0.4rem 0.7rem; font-size: 0.8rem; pointer-events: none;
    z-index: 1000; white-space: nowrap; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    display: none;
  }}
  .edge-tooltip .edge-from {{ color: #005587; }}
  .edge-tooltip .edge-to {{ color: #00897B; }}
  .edge-tooltip .edge-arrow {{ color: #53565A; margin: 0 0.3rem; }}
  .edge-detail-panel {{
    display: none; margin-top: 0.75rem;
    background: #FFFFFF; border: 1px solid #E1E1E1; border-radius: 10px;
    padding: 1.2rem; width: 100%; max-height: 70vh; overflow-y: auto;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    font-size: 0.85rem; color: #000000;
  }}
  .edge-detail-panel .detail-header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 0.8rem; padding-bottom: 0.6rem; border-bottom: 1px solid #E1E1E1;
  }}
  .edge-detail-panel .detail-header h3 {{ font-size: 0.95rem; font-weight: 600; margin: 0; }}
  .edge-detail-panel .detail-close {{
    background: none; border: 1px solid #E1E1E1; color: #53565A; border-radius: 4px;
    cursor: pointer; padding: 0.1rem 0.5rem; font-size: 0.8rem;
  }}
  .edge-detail-panel .detail-close:hover {{ color: #000000; border-color: #53565A; }}
  .edge-detail-panel .detail-section {{ margin-bottom: 0.8rem; }}
  .edge-detail-panel .detail-section h4 {{
    font-size: 0.75rem; text-transform: uppercase; color: #53565A; letter-spacing: 0.04em;
    margin-bottom: 0.3rem;
  }}
  .edge-detail-panel .detail-flow {{
    display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; margin-bottom: 0.3rem;
  }}
  .edge-detail-panel .detail-flow .from {{ color: #005587; font-weight: 600; }}
  .edge-detail-panel .detail-flow .to {{ color: #00897B; font-weight: 600; }}
  .edge-detail-panel .detail-flow .arrow {{ color: #53565A; }}
  .edge-detail-panel .detail-list {{ list-style: none; padding: 0; }}
  .edge-detail-panel .detail-list li {{
    padding: 0.25rem 0; border-bottom: 1px solid #F5F5F5; color: #333333; font-size: 0.8rem;
  }}
  .edge-detail-panel .detail-list li:last-child {{ border-bottom: none; }}
  .edge-detail-panel .detail-empty {{ color: #53565A; font-style: italic; font-size: 0.8rem; }}
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
  thead th {{
    background: #F5F5F5; color: #53565A; font-weight: 600; text-transform: uppercase;
    font-size: 0.72rem; letter-spacing: 0.04em; padding: 0.6rem 0.75rem; text-align: left;
    border-bottom: 1px solid #E1E1E1; position: sticky; top: 0; z-index: 1;
  }}
  tbody td {{ padding: 0.55rem 0.75rem; border-bottom: 1px solid #F5F5F5; color: #333333; }}
  tbody tr:hover {{ background: rgba(0,85,135,0.04); }}
  thead th[data-sort-type]:not([data-sort-type="none"]) {{ cursor: pointer; user-select: none; }}
  thead th[data-sort-type]:not([data-sort-type="none"]):hover {{ background: #EAEAEA; }}
  .sort-indicator {{ font-size: 0.65em; margin-left: 3px; color: #005587; }}
  .hs-badge {{
    display:inline-block; padding:0.2rem 0.6rem; border-radius:12px;
    font-size:0.78rem; font-weight:600; cursor:pointer; transition: outline .15s;
  }}
  .hs-badge[data-filter="red"]    {{ background:rgba(208,0,43,0.15); color:#D0002B; }}
  .hs-badge[data-filter="yellow"] {{ background:rgba(158,135,0,0.15); color:#9E8700; }}
  .hs-badge[data-filter="green"]  {{ background:rgba(0,150,57,0.15); color:#009639; }}
  .hs-badge[data-filter="none"]   {{ background:rgba(83,86,90,0.15); color:#53565A; }}
  .hs-badge-active {{ outline:2px solid currentColor; }}
  .cq-badge {{
    display:inline-block; padding:0.2rem 0.6rem; border-radius:12px;
    font-size:0.78rem; font-weight:600; cursor:pointer; transition: outline .15s;
    background:rgba(0,85,135,0.15); color:#005587;
  }}
  .cq-badge-active {{ outline:2px solid currentColor; }}
  .cq-sev-badge {{
    display:inline-block; padding:0.2rem 0.6rem; border-radius:12px;
    font-size:0.78rem; font-weight:600; cursor:pointer; transition: outline .15s;
    border:none;
  }}
  .cq-sev-badge-active {{ outline:2px solid currentColor; }}
  .ux-badge {{
    display:inline-block; padding:0.2rem 0.6rem; border-radius:12px;
    font-size:0.78rem; font-weight:600; cursor:pointer; transition: outline .15s;
  }}
  .ux-badge-active {{ outline:2px solid currentColor; }}
  .hs-dropdown {{
    padding:0.35rem 0.6rem; border-radius:6px; border:1px solid #E1E1E1;
    background:#FFFFFF; color:#333333; font-size:0.82rem; outline:none;
    cursor:pointer; transition:border-color .2s;
  }}
  .hs-dropdown:hover {{ border-color:#005587; }}
  .hs-dropdown:focus {{ border-color:#005587; box-shadow:0 0 0 2px rgba(0,85,135,0.15); }}
  .tag {{
    display: inline-block; padding: 0.15rem 0.55rem; border-radius: 4px;
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em;
  }}
  .tag-webapp      {{ background: rgba(0,137,123,.15); color: #00897B; }}
  .tag-library     {{ background: rgba(0,85,135,.15); color: #005587; }}
  .tag-application {{ background: rgba(98,18,68,.15);  color: #621244; }}
  .tag-service     {{ background: rgba(0,139,205,.15); color: #008BCD; }}
  .tag-tool        {{ background: rgba(120,157,74,.15); color: #789D4A; }}
  .tag-test        {{ background: rgba(128,39,108,.15); color: #80276C; }}
  .tag-connector   {{ background: rgba(54,116,157,.15); color: #36749D; }}
  .tag-desktopapp  {{ background: rgba(0,191,179,.15);  color: #00BFB3; }}
  .tag-db       {{ background: rgba(0,85,135,.15);  color: #005587; }}
  .tag-messaging{{ background: rgba(98,18,68,.15);   color: #621244; }}
  .tag-api      {{ background: rgba(0,139,205,.15);  color: #008BCD; }}
  .tag-cache    {{ background: rgba(120,157,74,.15);  color: #789D4A; }}
  .tag-config   {{ background: rgba(128,39,108,.15);  color: #80276C; }}
  .tag-presentation  {{ background: rgba(98,18,68,.15);  color: #621244; }}
  .tag-engine        {{ background: rgba(54,116,157,.15);  color: #36749D; }}
  .tag-dataaccess    {{ background: rgba(0,85,135,.15); color: #005587; }}
  .tag-infrastructure {{ background: rgba(128,39,108,.15); color: #80276C; }}
  .tag-unclassified  {{ background: rgba(83,86,90,.15); color: #53565A; }}
  .ft-layout {{ display:flex; gap:1rem; align-items:flex-start; }}
  .ft-sidebar {{ width:360px; flex-shrink:0; position:sticky; top:1rem; max-height:85vh; overflow-y:auto; }}
  .flow-row {{ cursor: pointer; }}
  .flow-row:hover {{ background: rgba(0,85,135,0.08) !important; }}
  .ft-row {{ cursor: pointer; }}
  .ft-row:hover {{ background: rgba(0,137,123,0.06) !important; }}
  .flow-step {{ display: inline-flex; align-items: center; gap: 0.3rem; margin: 0.2rem 0; }}
  .flow-arrow {{ color: #53565A; margin: 0 0.2rem; }}
  .mono {{ font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: 0.78rem; color: #53565A; }}
  .file-ref {{ display:inline; white-space:nowrap; }}
  .file-action {{ display:inline-block; padding:0.1rem 0.35rem; border-radius:3px; font-size:0.6rem; font-weight:700; cursor:pointer; text-decoration:none; margin-left:0.2rem; vertical-align:middle; line-height:1.2; }}
  .file-studio {{ background:#68217a; color:#fff !important; }}
  .file-studio:hover {{ background:#4e1a5c; }}
  .file-code {{ background:#0078d4; color:#fff !important; }}
  .file-code:hover {{ background:#005a9e; }}
  .file-claude {{ background:#da7756; color:#fff !important; }}
  .file-claude:hover {{ background:#b85e3f; }}
  .file-view {{ background:#e8e8e8; color:#333 !important; }}
  .file-view:hover {{ background:#d0d0d0; }}
  .footer {{
    text-align: center; padding: 1.5rem 2rem; color: #53565A;
    font-size: 0.78rem; font-style: italic; border-top: 1px solid #E1E1E1;
  }}
  @media (max-width: 768px) {{
    .header {{ padding: 1rem; }}
    .content {{ padding: 1rem; }}
    .tabs {{ padding: 0 1rem; }}
    .search-box {{ width: 100%; }}
    .diagram-with-legend {{ flex-direction:column; }}
    .diagram-sidebar {{ width:100%; }}
    .diagram-legend {{ width:100%; }}
    .ft-layout {{ flex-direction:column; }}
    .ft-sidebar {{ width:100%; position:static; max-height:none; }}
  }}
</style>
</head>
<body>
<div class="edge-tooltip" id="edgeTooltip"></div>

<div id="helpModal" style="display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.5);align-items:center;justify-content:center;" onclick="if(event.target===this)this.style.display='none'">
  <div style="background:#FFFFFF;border-radius:12px;max-width:720px;width:90%;max-height:85vh;overflow-y:auto;padding:2rem;position:relative;box-shadow:0 8px 32px rgba(0,0,0,0.25);">
    <button onclick="document.getElementById('helpModal').style.display='none'" style="position:absolute;top:1rem;right:1rem;background:none;border:1px solid #E1E1E1;color:#53565A;border-radius:4px;cursor:pointer;padding:0.2rem 0.6rem;font-size:0.85rem;">&#10005;</button>
    <h2 style="color:#022D5E;margin-bottom:1rem;">Dependency Map — Help</h2>

    <h3 style="color:#005587;margin:1rem 0 0.5rem;">Diagram Tabs</h3>
    <p style="font-size:0.88rem;color:#333;line-height:1.6;">
      <strong>Overview</strong> — category-level dependency graph. Click boxes to jump to category detail; click arrows to see project-level references.<br>
      <strong>Category tabs</strong> (Library, Service, etc.) — project-level dependency diagrams within each category.
    </p>

    <h3 style="color:#005587;margin:1rem 0 0.5rem;">Data Tabs</h3>
    <p style="font-size:0.88rem;color:#333;line-height:1.6;">
      <strong>Data Sources</strong> — discovered data access patterns (SQL, EF, HTTP, messaging).<br>
      <strong>Implied Dependencies</strong> — projects connected through shared data infrastructure (same DB table, queue, etc.).<br>
      <strong>Connection Strings</strong> — configuration file connection strings found across repos.<br>
      <strong>E2E Flows</strong> — end-to-end paths from UI screens through business layers to data access.<br>
      <strong>Field Traceability</strong> — traces XAML bindings through ViewModels and Entities to database columns.
    </p>

    <h3 style="color:#005587;margin:1rem 0 0.5rem;">Analysis Tabs</h3>
    <p style="font-size:0.88rem;color:#333;line-height:1.6;">
      <strong>Code Quality</strong> — refactoring triage based on code smell and security detection. Scores use severity-weighted smells (critical=15, high=8, medium=3, low=1).<br>
      <em>Severity tiers:</em> Critical (hardcoded secrets, SQL injection, insecure deserialization, command injection), High (weak crypto, open redirect, XSS, insecure random, exception swallowing, sync-over-async), Medium (god methods, deep nesting, long parameter lists), Low (magic numbers, missing null checks, mutable shared state).<br>
      <em>Refactoring Value Score</em> = Complexity&times;2 + WeightedSmells + (Fan-In&times;Fan-Out)&times;0.5 + TestGap&times;5 &minus; CategoryDiscount.<br>
      <strong>Security</strong> — dedicated view of security-category findings (critical + high severity). Shows file, line, detector, severity, and context with direct file navigation.
    </p>
    <p style="font-size:0.88rem;color:#333;line-height:1.6;">
      <strong>UX Consistency</strong> — detects XAML/WPF binding issues including broken bindings, missing DataContext, and inconsistent naming.<br>
      <em>Severity levels:</em> Error (broken bindings that will fail at runtime), Warning (likely issues), Info (style suggestions).
    </p>
    <p style="font-size:0.88rem;color:#333;line-height:1.6;">
      <strong>Hotspots</strong> — projects ranked by coupling complexity where AI-assisted refactoring has the most impact.<br>
      <em>Hotspot Score</em> = Fan-Out&times;3 + Fan-In&times;2 + NuGet + DataPatterns + CrossRepo&times;4.<br>
      <em>Risk Score</em> adjusts for expected patterns (Library fan-in) and factors in code smell flags.
    </p>
    <p style="font-size:0.88rem;color:#333;line-height:1.6;">
      <strong>NuGet Health</strong> — version conflicts (same package, different versions), legacy format projects (packages.config), target framework distribution, and Central Package Management status.
    </p>

    <h3 style="color:#005587;margin:1rem 0 0.5rem;">Other Tabs</h3>
    <p style="font-size:0.88rem;color:#333;line-height:1.6;">
      <strong>Tests</strong> — test project detection with method counts, framework identification, and coverage mapping.<br>
      <strong>Language tabs</strong> (Python, etc.) — auto-detected non-.NET projects with framework detection, dependency parsing, and line counts.<br>
      <strong>Repos</strong> — repository summary with project counts and categories.<br>
      <strong>All Projects</strong> — searchable/sortable table of every .csproj project found.
    </p>

    <h3 style="color:#005587;margin:1rem 0 0.5rem;">Tips</h3>
    <p style="font-size:0.88rem;color:#333;line-height:1.6;">
      Use the search box to filter any active tab. Click stat cards in the header to jump to the relevant tab. Click the AI Context link to browse per-project context files for feeding to AI assistants.
    </p>
  </div>
</div>

<header class="header">
  <div class="header-top">
    <h1><span>{_esc_html(title)}</span> Dependency Map</h1>
    <div class="search-box">
      <span class="search-icon">&#128269;</span>
      <input type="text" id="searchInput" placeholder="Search projects..." autocomplete="off">
    </div>
  </div>
  <div class="stats-row">
{stats_html}
    <a href="docs/ai-context/index.html" target="_blank" class="stat stat-link" style="text-decoration:none;" title="Open AI-ready codebase overview and per-project context files">
      <span class="stat-value">AI</span> Context
    </a>
    <a href="#" id="helpLink" style="color:rgba(255,255,255,0.85);font-size:0.82rem;font-weight:600;padding:0.25rem 0.6rem;border-radius:6px;transition:background .15s;text-decoration:none;" onmouseover="this.style.background='rgba(255,255,255,0.15)'" onmouseout="this.style.background='none'" onclick="event.preventDefault();document.getElementById('helpModal').style.display='flex';">? Help</a>
  </div>
</header>

<nav class="tabs" id="tabNav">
{tab_buttons}
</nav>

<main class="content">
{diagram_panels}
{datasources_panel}
{implieddeps_panel}
{connstrings_panel}
{e2eflows_panel}
{fieldtrace_panel}
{codequality_panel}
{security_panel}
{uxconsistency_panel}
{hotspots_panel}
{nugethealth_panel}
{tests_panel}
{externaltools_panel}
{language_panels}
{repos_panel}
{all_projects_panel}
</main>

<footer class="footer">
  Generated by Dependency Mapper (Python) &mdash; {date.today().isoformat()}
</footer>

<script>
var diagramZoomLevels = {{}};

function attachEdgeTooltips(svg) {{
  var tooltip = document.getElementById('edgeTooltip');
  if (!tooltip) return;

  // Build node ID -> display name lookup from rendered nodes
  var nodeNames = {{}};
  svg.querySelectorAll('.node').forEach(function (n) {{
    var match = n.id.match(/^flowchart-(.+)-\\d+$/);
    if (match) {{
      nodeNames[match[1]] = n.textContent.trim();
    }}
  }});

  // Get sorted node keys longest-first for greedy matching
  var nodeKeys = Object.keys(nodeNames).sort(function (a, b) {{ return b.length - a.length; }});

  function resolveEdgeEndpoints(edgeId) {{
    var inner = edgeId.replace(/^L_/, '').replace(/_\\d+$/, '');
    for (var i = 0; i < nodeKeys.length; i++) {{
      var key = nodeKeys[i];
      if (inner.indexOf(key) === 0) {{
        var rest = inner.substring(key.length + 1);
        if (nodeNames[rest] !== undefined) {{
          return {{ from: nodeNames[key], to: nodeNames[rest] }};
        }}
      }}
    }}
    return null;
  }}

  // For each edge path, create a wider invisible hover target and attach events
  var edgePaths = svg.querySelector('.edgePaths');
  if (!edgePaths) return;

  svg.querySelectorAll('.flowchart-link').forEach(function (edge) {{
    if (!edge.id) return;

    // Clone the path as a wider invisible hover target
    var hitArea = edge.cloneNode(false);
    hitArea.removeAttribute('id');
    hitArea.removeAttribute('marker-end');
    hitArea.setAttribute('class', 'edge-hover-target');
    hitArea.removeAttribute('style');
    edge.parentNode.insertBefore(hitArea, edge);

    function showTip(e) {{
      var ep = resolveEdgeEndpoints(edge.id);
      if (!ep) return;
      tooltip.innerHTML = '<span class="edge-from">' + ep.from + '</span>'
        + '<span class="edge-arrow"> &#8594; </span>'
        + '<span class="edge-to">' + ep.to + '</span>';
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 12) + 'px';
      tooltip.style.top = (e.clientY - 10) + 'px';
      edge.classList.add('edge-highlight');
      // Dim other edges
      svg.querySelectorAll('.flowchart-link').forEach(function (other) {{
        if (other !== edge) other.style.opacity = '0.15';
      }});
    }}

    function moveTip(e) {{
      tooltip.style.left = (e.clientX + 12) + 'px';
      tooltip.style.top = (e.clientY - 10) + 'px';
    }}

    function hideTip() {{
      tooltip.style.display = 'none';
      edge.classList.remove('edge-highlight');
      svg.querySelectorAll('.flowchart-link').forEach(function (other) {{
        other.style.opacity = '';
      }});
    }}

    function onClick(e) {{
      e.stopPropagation();
      var ep = resolveEdgeEndpoints(edge.id);
      if (!ep) return;
      var fromCat = parseCategoryLabel(ep.from);
      var toCat = parseCategoryLabel(ep.to);
      if (fromCat && toCat) {{ showCategoryEdgeDetail(ep.from, ep.to, fromCat, toCat); return; }}
      var meta = (window._projData || {{}}).meta || [];
      var fromIsProject = meta.some(function (m) {{ return m.project === ep.from; }});
      var toIsProject = meta.some(function (m) {{ return m.project === ep.to; }});
      if (fromIsProject && toCat) {{ showProjectCategoryDetail(ep.from, toCat, true); return; }}
      if (toIsProject && fromCat) {{ showProjectCategoryDetail(ep.to, fromCat, false); return; }}
      if (fromIsProject && toIsProject) {{ showEdgeDetail(ep.from, ep.to); }}
      else {{ showDataFlowDetail(ep.from, ep.to, fromIsProject, toIsProject); }}
    }}

    hitArea.addEventListener('mouseenter', showTip);
    hitArea.addEventListener('mousemove', moveTip);
    hitArea.addEventListener('mouseleave', hideTip);
    hitArea.addEventListener('click', onClick);
    edge.addEventListener('mouseenter', showTip);
    edge.addEventListener('mousemove', moveTip);
    edge.addEventListener('mouseleave', hideTip);
    edge.addEventListener('click', onClick);
  }});
}}

function attachCategoryNodeClicks(svg) {{
  svg.querySelectorAll('.node').forEach(function (node) {{
    var textEl = node.querySelector('span, foreignObject div, text');
    if (!textEl) return;
    var label = textEl.textContent.trim();
    var catInfo = parseCategoryLabel(label);
    if (!catInfo) return;
    node.style.cursor = 'pointer';
    node.setAttribute('title', catInfo.name + ': ' + catInfo.count + ' projects in this category that connect to projects in this diagram. Click to see details.');
    node.addEventListener('click', function (e) {{
      e.stopPropagation();
      showPillDetail(catInfo, svg);
    }});
  }});
}}

function showPillDetail(catInfo, svg) {{
  var panel = document.querySelector('.tab-panel.active .edge-detail-panel');
  if (!panel) return;
  var d = window._projData || {{}};
  var meta = d.meta || [];
  var refs = d.refs || [];

  // Find the current diagram's tab panel to determine which category we're viewing
  var activeTab = document.querySelector('.tab-panel.active');
  var tabId = activeTab ? activeTab.id.replace('panel-', '') : '';
  var currentCatKey = tabId.replace('cat_', '');

  // Find projects in the pill's category and in the current category
  var pillProjects = {{}};
  var currentProjects = {{}};
  meta.forEach(function (m) {{
    if (m.category && m.category.toLowerCase() === catInfo.key) pillProjects[m.project] = m;
    if (m.category && m.category.toLowerCase() === currentCatKey) currentProjects[m.project] = m;
  }});

  // Find references between current category and pill category
  var outgoing = refs.filter(function (r) {{ return currentProjects[r.project] && pillProjects[r.references]; }});
  var incoming = refs.filter(function (r) {{ return pillProjects[r.project] && currentProjects[r.references]; }});

  var html = '<div class="detail-header"><h3>' + escHtmlGlobal(catInfo.name) + ' (' + catInfo.count + ' projects)</h3>'
    + '<button class="detail-close">Close</button></div>';

  html += '<div class="detail-section" style="color:#53565A;font-size:0.8rem;margin-bottom:0.6rem;">'
    + 'This pill represents <strong>' + catInfo.count + '</strong> ' + escHtmlGlobal(catInfo.name)
    + ' projects that have cross-category dependencies with the projects in this diagram.</div>';

  // Outgoing refs (current -> pill)
  if (outgoing.length > 0) {{
    html += '<div class="detail-section"><h4>Depends on ' + escHtmlGlobal(catInfo.name) + ' (' + outgoing.length + ')</h4>';
    html += '<ul class="detail-list">';
    var shown = outgoing.slice(0, 20);
    shown.forEach(function (r) {{
      html += '<li><span style="color:#005587">' + escHtmlGlobal(r.project) + '</span>'
        + ' <span style="color:#53565A">&#8594;</span> '
        + '<span style="color:#00897B">' + escHtmlGlobal(r.references) + '</span></li>';
    }});
    if (outgoing.length > 20) html += '<li style="color:#53565A">... and ' + (outgoing.length - 20) + ' more</li>';
    html += '</ul></div>';
  }}

  // Incoming refs (pill -> current)
  if (incoming.length > 0) {{
    html += '<div class="detail-section"><h4>Referenced by ' + escHtmlGlobal(catInfo.name) + ' (' + incoming.length + ')</h4>';
    html += '<ul class="detail-list">';
    var shown2 = incoming.slice(0, 20);
    shown2.forEach(function (r) {{
      html += '<li><span style="color:#005587">' + escHtmlGlobal(r.project) + '</span>'
        + ' <span style="color:#53565A">&#8594;</span> '
        + '<span style="color:#00897B">' + escHtmlGlobal(r.references) + '</span></li>';
    }});
    if (incoming.length > 20) html += '<li style="color:#53565A">... and ' + (incoming.length - 20) + ' more</li>';
    html += '</ul></div>';
  }}

  if (outgoing.length === 0 && incoming.length === 0) {{
    html += '<div class="detail-section"><div class="detail-empty">No direct project references found</div></div>';
  }}

  // Navigation button
  html += '<div class="detail-section" style="margin-top:0.5rem;">';
  html += '<button class="cat-nav-btn" data-tab="' + catInfo.tabId + '">Explore ' + escHtmlGlobal(catInfo.name) + ' tab</button>';
  html += '</div>';

  panel.innerHTML = html;
  panel.style.display = 'block';
  var closeBtn = panel.querySelector('.detail-close');
  if (closeBtn) closeBtn.addEventListener('click', function () {{ panel.style.display = 'none'; }});
  panel.querySelectorAll('.cat-nav-btn').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      panel.style.display = 'none';
      var tabBtn = document.querySelector('.tab-btn[data-tab="' + btn.dataset.tab + '"]');
      if (tabBtn) tabBtn.click();
    }});
  }});
}}

function showEdgeDetail(fromName, toName) {{
  var panel = document.querySelector('.tab-panel.active .edge-detail-panel');
  if (!panel) return;
  var d = window._projData || {{}};
  var refs = d.refs || [], deps = d.deps || [], meta = d.meta || [], dataSrc = d.dataSources || [];

  // Find meta for both projects (match by short name — the display name)
  var fromMeta = meta.find(function (m) {{ return m.project === fromName; }});
  var toMeta = meta.find(function (m) {{ return m.project === toName; }});

  // Find direct references between these projects
  var directRefs = refs.filter(function (r) {{
    return (r.project === fromName && r.references === toName) ||
           (r.project === toName && r.references === fromName);
  }});

  // Find NuGet packages used by the source project
  var fromDeps = deps.filter(function (d) {{ return d.project === fromName; }});
  var toDeps = deps.filter(function (d) {{ return d.project === toName; }});
  // Find shared NuGet packages
  var toPackages = {{}};
  toDeps.forEach(function (d) {{ toPackages[d.package] = d.version; }});
  var sharedPkgs = fromDeps.filter(function (d) {{ return toPackages[d.package]; }});

  // Find data patterns for both projects
  // Project path is like "src/Foo/Foo.csproj" — directory is everything up to the last "/"
  var fromPath = fromMeta ? (fromMeta.globalPath || fromMeta.path || '') : '';
  var toPath = toMeta ? (toMeta.globalPath || toMeta.path || '') : '';
  var fromDir = fromPath.substring(0, fromPath.lastIndexOf('/'));
  var toDir = toPath.substring(0, toPath.lastIndexOf('/'));
  var fromDataPatterns = fromDir ? dataSrc.filter(function (ds) {{ return ds.file && ds.file.indexOf(fromDir + '/') === 0; }}) : [];
  var toDataPatterns = toDir ? dataSrc.filter(function (ds) {{ return ds.file && ds.file.indexOf(toDir + '/') === 0; }}) : [];

  // Find shared data pattern types
  var fromPatternTypes = {{}};
  fromDataPatterns.forEach(function (p) {{ fromPatternTypes[p.pattern] = true; }});
  var sharedPatterns = toDataPatterns.filter(function (p) {{ return fromPatternTypes[p.pattern]; }});
  // Unique shared pattern names
  var sharedPatternNames = {{}};
  sharedPatterns.forEach(function (p) {{ sharedPatternNames[p.pattern] = (sharedPatternNames[p.pattern] || 0) + 1; }});

  // Build HTML
  var html = '<div class="detail-header"><h3>Dependency Detail</h3>'
    + '<button class="detail-close" id="detailCloseBtn">Close</button></div>';

  // Flow
  html += '<div class="detail-section"><div class="detail-flow">'
    + '<span class="from">' + escHtmlGlobal(fromName) + '</span>'
    + '<span class="arrow">&#8594;</span>'
    + '<span class="to">' + escHtmlGlobal(toName) + '</span>'
    + '</div>';
  if (fromMeta || toMeta) {{
    html += '<div style="font-size:0.75rem;color:#53565A;margin-top:0.2rem;">';
    if (fromMeta) html += escHtmlGlobal(fromMeta.category);
    html += ' &#8594; ';
    if (toMeta) html += escHtmlGlobal(toMeta.category);
    html += '</div>';
  }}
  html += '</div>';

  // Project references
  html += '<div class="detail-section"><h4>Project References</h4>';
  if (directRefs.length > 0) {{
    html += '<ul class="detail-list">';
    directRefs.forEach(function (r) {{
      var cross = r.crossRepo === 'True' ? ' <span style="color:#789D4A;">(cross-repo)</span>' : '';
      html += '<li>' + escHtmlGlobal(r.project) + ' &#8594; ' + escHtmlGlobal(r.references) + cross + '</li>';
    }});
    html += '</ul>';
  }} else {{
    html += '<div class="detail-empty">No direct project references found</div>';
  }}
  html += '</div>';

  // Shared NuGet packages
  html += '<div class="detail-section"><h4>Shared NuGet Packages (' + sharedPkgs.length + ')</h4>';
  if (sharedPkgs.length > 0) {{
    html += '<ul class="detail-list">';
    sharedPkgs.slice(0, 15).forEach(function (d) {{
      html += '<li>' + escHtmlGlobal(d.package) + ' <span style="color:#53565A">' + escHtmlGlobal(d.version) + '</span></li>';
    }});
    if (sharedPkgs.length > 15) html += '<li style="color:#53565A">... and ' + (sharedPkgs.length - 15) + ' more</li>';
    html += '</ul>';
  }} else {{
    html += '<div class="detail-empty">No shared NuGet packages</div>';
  }}
  html += '</div>';

  // Data patterns
  var totalFromPatterns = fromDataPatterns.length;
  var totalToPatterns = toDataPatterns.length;
  html += '<div class="detail-section"><h4>Data Patterns</h4>';
  html += '<div style="font-size:0.78rem;color:#333333;margin-bottom:0.3rem;">'
    + '<span class="from" style="color:#005587">' + escHtmlGlobal(fromName) + '</span>: ' + totalFromPatterns + ' patterns, '
    + '<span class="to" style="color:#00897B">' + escHtmlGlobal(toName) + '</span>: ' + totalToPatterns + ' patterns</div>';
  var sharedKeys = Object.keys(sharedPatternNames);
  if (sharedKeys.length > 0) {{
    html += '<ul class="detail-list">';
    sharedKeys.forEach(function (p) {{
      html += '<li>' + escHtmlGlobal(p) + ' <span style="color:#53565A">(' + sharedPatternNames[p] + ' matches in target)</span></li>';
    }});
    html += '</ul>';
  }} else {{
    html += '<div class="detail-empty">No shared data patterns</div>';
  }}
  html += '</div>';

  // Data Flow section (from data-flow.json)
  var df = window._dataFlow || {{}};
  var dfNodes = df.dataNodes || [];
  var dfImplied = df.impliedDependencies || [];

  // Find data nodes that both projects connect to
  var sharedDataNodes = dfNodes.filter(function (n) {{
    var allFrom = (n.writers || []).concat(n.readers || []).concat(n.exposers || []).concat(n.consumers || []);
    var allTo = (n.writers || []).concat(n.readers || []).concat(n.exposers || []).concat(n.consumers || []);
    var fromConnected = allFrom.indexOf(fromName) !== -1;
    var toConnected = allTo.indexOf(toName) !== -1;
    return fromConnected && toConnected;
  }});

  // Find implied dependencies between these projects
  var relevantImplied = dfImplied.filter(function (d) {{
    return (d.from === fromName && d.to === toName) || (d.from === toName && d.to === fromName);
  }});

  html += '<div class="detail-section"><h4>Data Flow</h4>';
  if (sharedDataNodes.length > 0 || relevantImplied.length > 0) {{
    if (sharedDataNodes.length > 0) {{
      html += '<div style="font-size:0.78rem;color:#333333;margin-bottom:0.3rem;">Shared data infrastructure:</div>';
      html += '<ul class="detail-list">';
      sharedDataNodes.slice(0, 10).forEach(function (n) {{
        var fromRole = [];
        var toRole = [];
        if ((n.writers || []).indexOf(fromName) !== -1) fromRole.push('writes');
        if ((n.readers || []).indexOf(fromName) !== -1) fromRole.push('reads');
        if ((n.exposers || []).indexOf(fromName) !== -1) fromRole.push('exposes');
        if ((n.consumers || []).indexOf(fromName) !== -1) fromRole.push('consumes');
        if ((n.writers || []).indexOf(toName) !== -1) toRole.push('writes');
        if ((n.readers || []).indexOf(toName) !== -1) toRole.push('reads');
        if ((n.exposers || []).indexOf(toName) !== -1) toRole.push('exposes');
        if ((n.consumers || []).indexOf(toName) !== -1) toRole.push('consumes');
        var infraLabel = n.infrastructure || n.type || '';
        html += '<li><strong>' + escHtmlGlobal(n.name) + '</strong> <span style="color:#53565A">(' + infraLabel + ')</span><br/>'
          + '<span style="color:#005587">' + escHtmlGlobal(fromName) + '</span>: ' + fromRole.join(', ') + ' &mdash; '
          + '<span style="color:#00897B">' + escHtmlGlobal(toName) + '</span>: ' + toRole.join(', ')
          + '</li>';
      }});
      if (sharedDataNodes.length > 10) html += '<li style="color:#53565A">... and ' + (sharedDataNodes.length - 10) + ' more</li>';
      html += '</ul>';
    }}
    if (relevantImplied.length > 0) {{
      html += '<div style="font-size:0.78rem;color:#789D4A;margin-top:0.3rem;">&#9888; Implied data dependencies:</div>';
      html += '<ul class="detail-list">';
      relevantImplied.forEach(function (d) {{
        html += '<li>' + escHtmlGlobal(d.from) + ' &#8594; ' + escHtmlGlobal(d.to) + ' via <strong>' + escHtmlGlobal(d.via) + '</strong> (' + escHtmlGlobal(d.viaType) + ')</li>';
      }});
      html += '</ul>';
    }}
  }} else {{
    html += '<div class="detail-empty">No shared data flow connections</div>';
  }}
  html += '</div>';

  panel.innerHTML = html;
  panel.style.display = 'block';
  var closeBtn = panel.querySelector('.detail-close');
  if (closeBtn) closeBtn.addEventListener('click', function () {{ panel.style.display = 'none'; }});
}}

function showDataFlowDetail(fromName, toName, fromIsProject, toIsProject) {{
  var panel = document.querySelector('.tab-panel.active .edge-detail-panel');
  if (!panel) return;
  var df = window._dataFlow || {{}};
  var nodes = df.dataNodes || [];
  var implied = df.impliedDependencies || [];

  // Determine which is the project and which is the data node
  var projectName = fromIsProject ? fromName : toName;
  var dataName = fromIsProject ? toName : fromName;

  // Find matching data node (match by name since Mermaid shows display names)
  var dataNode = nodes.find(function (n) {{ return n.name === dataName; }});

  var html = '<div class="detail-header"><h3>Data Flow Detail</h3>'
    + '<button class="detail-close" id="detailCloseBtn">Close</button></div>';

  // Edge direction
  html += '<div class="detail-section"><div class="detail-flow">'
    + '<span class="' + (fromIsProject ? 'from' : 'to') + '">' + escHtmlGlobal(fromName) + '</span>'
    + '<span class="arrow">&#8594;</span>'
    + '<span class="' + (toIsProject ? 'from' : 'to') + '">' + escHtmlGlobal(toName) + '</span>'
    + '</div></div>';

  if (dataNode) {{
    // Data node info
    html += '<div class="detail-section"><h4>' + escHtmlGlobal(dataNode.type) + ': ' + escHtmlGlobal(dataNode.name) + '</h4>';
    html += '<div style="font-size:0.78rem;color:#53565A;margin-bottom:0.4rem;">Infrastructure: ' + escHtmlGlobal(dataNode.infrastructure) + '</div>';

    // Writers
    var writers = dataNode.writers || [];
    if (writers.length > 0) {{
      html += '<div style="margin-bottom:0.3rem;"><strong style="color:#789D4A;font-size:0.78rem;">&#9654; Writers:</strong> ';
      html += writers.map(function (w) {{
        var style = w === projectName ? 'color:#005587;font-weight:600' : 'color:#333333';
        return '<span style="' + style + '">' + escHtmlGlobal(w) + '</span>';
      }}).join(', ');
      html += '</div>';
    }}

    // Readers
    var readers = dataNode.readers || [];
    if (readers.length > 0) {{
      html += '<div style="margin-bottom:0.3rem;"><strong style="color:#005587;font-size:0.78rem;">&#9664; Readers:</strong> ';
      html += readers.map(function (r) {{
        var style = r === projectName ? 'color:#005587;font-weight:600' : 'color:#333333';
        return '<span style="' + style + '">' + escHtmlGlobal(r) + '</span>';
      }}).join(', ');
      html += '</div>';
    }}

    // Exposers
    var exposers = dataNode.exposers || [];
    if (exposers.length > 0) {{
      html += '<div style="margin-bottom:0.3rem;"><strong style="color:#00897B;font-size:0.78rem;">&#9650; Exposes:</strong> ';
      html += exposers.map(function (x) {{
        var style = x === projectName ? 'color:#005587;font-weight:600' : 'color:#333333';
        return '<span style="' + style + '">' + escHtmlGlobal(x) + '</span>';
      }}).join(', ');
      html += '</div>';
    }}

    // Consumers
    var consumers = dataNode.consumers || [];
    if (consumers.length > 0) {{
      html += '<div style="margin-bottom:0.3rem;"><strong style="color:#80276C;font-size:0.78rem;">&#9660; Consumers:</strong> ';
      html += consumers.map(function (c) {{
        var style = c === projectName ? 'color:#005587;font-weight:600' : 'color:#333333';
        return '<span style="' + style + '">' + escHtmlGlobal(c) + '</span>';
      }}).join(', ');
      html += '</div>';
    }}
    html += '</div>';

    // Implied dependencies through this node
    var nodeImplied = implied.filter(function (d) {{ return d.via === dataNode.name; }});
    if (nodeImplied.length > 0) {{
      html += '<div class="detail-section"><h4>Implied Dependencies</h4>';
      html += '<ul class="detail-list">';
      nodeImplied.forEach(function (d) {{
        html += '<li>' + escHtmlGlobal(d.from) + ' &#8594; ' + escHtmlGlobal(d.to)
          + ' <span style="color:#53565A">(' + escHtmlGlobal(d.viaType) + ')</span></li>';
      }});
      html += '</ul></div>';
    }}
  }} else {{
    html += '<div class="detail-section"><div class="detail-empty">Data node details not available</div></div>';
  }}

  panel.innerHTML = html;
  panel.style.display = 'block';
  var closeBtn = panel.querySelector('.detail-close');
  if (closeBtn) closeBtn.addEventListener('click', function () {{ panel.style.display = 'none'; }});
}}

function showCategoryEdgeDetail(fromLabel, toLabel, fromCat, toCat) {{
  var panel = document.querySelector('.tab-panel.active .edge-detail-panel');
  if (!panel) return;
  var d = window._projData || {{}};
  var meta = d.meta || [];
  var refs = d.refs || [];

  // Find projects in each category
  var fromProjects = {{}};
  var toProjects = {{}};
  meta.forEach(function (m) {{
    if (m.category && m.category.toLowerCase() === fromCat.key) fromProjects[m.project] = true;
    if (m.category && m.category.toLowerCase() === toCat.key) toProjects[m.project] = true;
  }});

  // Filter refs: from-category projects referencing to-category projects
  var crossRefs = refs.filter(function (r) {{
    return fromProjects[r.project] && toProjects[r.references];
  }});

  var html = '<div class="detail-header"><h3>Cross-Category References</h3>'
    + '<button class="detail-close" id="detailCloseBtn">Close</button></div>';

  // Summary flow
  html += '<div class="detail-section"><div class="detail-flow">'
    + '<span class="from">' + escHtmlGlobal(fromCat.name) + '</span>'
    + '<span class="arrow">&#8594;</span>'
    + '<span class="to">' + escHtmlGlobal(toCat.name) + '</span>'
    + '</div>';
  html += '<div style="color:#53565A;font-size:0.78rem;margin-top:0.3rem;">'
    + crossRefs.length + ' project reference' + (crossRefs.length !== 1 ? 's' : '')
    + ' from ' + escHtmlGlobal(fromCat.name) + ' (' + Object.keys(fromProjects).length + ' projects)'
    + ' to ' + escHtmlGlobal(toCat.name) + ' (' + Object.keys(toProjects).length + ' projects)'
    + '</div></div>';

  // Sample references (capped at 20)
  if (crossRefs.length > 0) {{
    html += '<div class="detail-section"><h4>References' + (crossRefs.length > 20 ? ' (showing 20 of ' + crossRefs.length + ')' : '') + '</h4>';
    html += '<ul class="detail-list">';
    var shown = crossRefs.slice(0, 20);
    shown.forEach(function (r) {{
      html += '<li><span style="color:#005587">' + escHtmlGlobal(r.project) + '</span>'
        + ' <span style="color:#53565A">&#8594;</span> '
        + '<span style="color:#00897B">' + escHtmlGlobal(r.references) + '</span></li>';
    }});
    html += '</ul></div>';
  }} else {{
    html += '<div class="detail-section"><div class="detail-empty">No direct project references found in this direction</div></div>';
  }}

  // Navigation buttons
  html += '<div class="detail-section" style="display:flex;gap:0.5rem;margin-top:0.5rem;">';
  html += '<button class="cat-nav-btn" data-tab="' + fromCat.tabId + '">Explore ' + escHtmlGlobal(fromCat.name) + '</button>';
  html += '<button class="cat-nav-btn" data-tab="' + toCat.tabId + '">Explore ' + escHtmlGlobal(toCat.name) + '</button>';
  html += '</div>';

  panel.innerHTML = html;
  panel.style.display = 'block';
  var closeBtn = panel.querySelector('.detail-close');
  if (closeBtn) closeBtn.addEventListener('click', function () {{ panel.style.display = 'none'; }});
  panel.querySelectorAll('.cat-nav-btn').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      panel.style.display = 'none';
      var tabBtn = document.querySelector('.tab-btn[data-tab="' + btn.dataset.tab + '"]');
      if (tabBtn) tabBtn.click();
    }});
  }});
}}

function showProjectCategoryDetail(projectName, catInfo, isOutgoing) {{
  var panel = document.querySelector('.tab-panel.active .edge-detail-panel');
  if (!panel) return;
  var d = window._projData || {{}};
  var meta = d.meta || [];
  var refs = d.refs || [];

  // Find projects in the target category
  var catProjects = {{}};
  meta.forEach(function (m) {{
    if (m.category && m.category.toLowerCase() === catInfo.key) catProjects[m.project] = true;
  }});

  // Filter refs between this project and projects in the target category
  var matchedRefs;
  if (isOutgoing) {{
    matchedRefs = refs.filter(function (r) {{
      return r.project === projectName && catProjects[r.references];
    }});
  }} else {{
    matchedRefs = refs.filter(function (r) {{
      return catProjects[r.project] && r.references === projectName;
    }});
  }}

  var html = '<div class="detail-header"><h3>Project / Category References</h3>'
    + '<button class="detail-close" id="detailCloseBtn">Close</button></div>';

  // Flow direction
  html += '<div class="detail-section"><div class="detail-flow">';
  if (isOutgoing) {{
    html += '<span class="from">' + escHtmlGlobal(projectName) + '</span>'
      + '<span class="arrow">&#8594;</span>'
      + '<span class="to">' + escHtmlGlobal(catInfo.name) + '</span>';
  }} else {{
    html += '<span class="from">' + escHtmlGlobal(catInfo.name) + '</span>'
      + '<span class="arrow">&#8594;</span>'
      + '<span class="to">' + escHtmlGlobal(projectName) + '</span>';
  }}
  html += '</div>';
  html += '<div style="color:#53565A;font-size:0.78rem;margin-top:0.3rem;">'
    + matchedRefs.length + ' reference' + (matchedRefs.length !== 1 ? 's' : '')
    + '</div></div>';

  // List actual referenced projects
  if (matchedRefs.length > 0) {{
    html += '<div class="detail-section"><h4>References' + (matchedRefs.length > 20 ? ' (showing 20 of ' + matchedRefs.length + ')' : '') + '</h4>';
    html += '<ul class="detail-list">';
    matchedRefs.slice(0, 20).forEach(function (r) {{
      html += '<li><span style="color:#005587">' + escHtmlGlobal(r.project) + '</span>'
        + ' <span style="color:#53565A">&#8594;</span> '
        + '<span style="color:#00897B">' + escHtmlGlobal(r.references) + '</span></li>';
    }});
    html += '</ul></div>';
  }} else {{
    html += '<div class="detail-section"><div class="detail-empty">No direct project references found</div></div>';
  }}

  // Navigation button
  html += '<div class="detail-section" style="margin-top:0.5rem;">';
  html += '<button class="cat-nav-btn" data-tab="' + catInfo.tabId + '">Explore ' + escHtmlGlobal(catInfo.name) + '</button>';
  html += '</div>';

  panel.innerHTML = html;
  panel.style.display = 'block';
  var closeBtn = panel.querySelector('.detail-close');
  if (closeBtn) closeBtn.addEventListener('click', function () {{ panel.style.display = 'none'; }});
  panel.querySelectorAll('.cat-nav-btn').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      panel.style.display = 'none';
      var tabBtn = document.querySelector('.tab-btn[data-tab="' + btn.dataset.tab + '"]');
      if (tabBtn) tabBtn.click();
    }});
  }});
}}

function escHtmlGlobal(s) {{
  var d = document.createElement('div');
  d.textContent = s || '';
  return d.innerHTML;
}}

// ── File path resolution ──
function _resolveFilePath(repoRoot, relFile) {{
  if (!repoRoot || !relFile) return '';
  var rf = relFile.replace(/\\\\/g, '/');
  var rr = repoRoot.replace(/\\\\/g, '/');
  var repoTail = rr.split('/').pop();
  if (repoTail && rf.indexOf(repoTail + '/') === 0) {{
    rf = rf.substring(repoTail.length + 1);
  }}
  return rr + '/' + rf;
}}
function _resolveFromRoots(filePath) {{
  if (!filePath) return '';
  var fp = filePath.replace(/\\\\/g, '/');
  // Already an absolute path — return as-is
  if (fp.charAt(0) === '/' || /^[A-Za-z]:/.test(fp)) return fp;
  var roots = window._repoRoots || {{}};
  var firstSeg = fp.split('/')[0];
  if (roots[firstSeg]) return _resolveFilePath(roots[firstSeg], fp);
  for (var rn in roots) {{
    if (roots.hasOwnProperty(rn)) return _resolveFilePath(roots[rn], fp);
  }}
  return fp;
}}
// Global helper: generate file action icons HTML
function fileActionsHtml(filePath, line, style) {{
  if (!filePath) return '';
  var display = escHtmlGlobal(filePath || '') + (line ? ':' + line : '');
  var dp = escHtmlGlobal(filePath);
  var dl = line || 0;
  return '<span class="file-ref">' +
    '<span class="mono" style="' + (style || 'color:#53565A;') + '">' + display + '</span>' +
    ' <a href="#" class="file-action file-studio" data-path="' + dp + '" data-line="' + dl + '" title="Open in Visual Studio">Studio</a>' +
    ' <a href="#" class="file-action file-code" data-path="' + dp + '" data-line="' + dl + '" title="Open in VS Code">Code</a>' +
    ' <a href="#" class="file-action file-claude" data-path="' + dp + '" data-line="' + dl + '" title="Explore with Claude Code">Claude</a>' +
    ' <a href="#" class="file-action file-view" data-path="' + dp + '" data-line="' + dl + '" title="View in browser">View</a>' +
    '</span>';
}}
function showToast(msg, isLong) {{
  var t = document.getElementById('pathToast');
  if (!t) {{
    t = document.createElement('div');
    t.id = 'pathToast';
    t.style.cssText = 'position:fixed;bottom:1.5rem;left:50%;transform:translateX(-50%);background:#022D5E;color:#fff;padding:0.5rem 1.2rem;border-radius:8px;font-size:0.82rem;font-family:monospace;z-index:10000;opacity:0;transition:opacity 0.3s;pointer-events:none;max-width:80vw;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;';
    document.body.appendChild(t);
  }}
  t.textContent = msg;
  t.style.opacity = '1';
  clearTimeout(t._tid);
  t._tid = setTimeout(function() {{ t.style.opacity = '0'; }}, isLong ? 5000 : 2000);
}}
function _openViaServer(editor, resolved, line) {{
  var url = '/_open?editor=' + editor + '&path=' + encodeURIComponent(resolved) + '&line=' + (line || 0);
  fetch(url).then(function(r) {{ return r.json(); }}).then(function(d) {{
    if (d.error) showToast(d.error, true);
    else showToast('Opening ' + editor + '...', false);
  }}).catch(function() {{
    showToast('Server not available — are you using run.py?', true);
  }});
}}
// Delegated click handler for file action icons
document.addEventListener('click', function(e) {{
  var action = e.target.closest('.file-action');
  if (!action) return;
  e.preventDefault();
  var path = action.getAttribute('data-path');
  var line = parseInt(action.getAttribute('data-line') || '0', 10);
  if (!path) return;
  var resolved = _resolveFromRoots(path);
  if (action.classList.contains('file-studio')) {{
    _openViaServer('studio', resolved, line);
  }} else if (action.classList.contains('file-code')) {{
    // VS Code: try client-side URI first, fall back to server
    var vsUri = 'vscode://file/' + encodeURI(resolved.replace(/\\\\/g, '/'));
    if (line) vsUri += ':' + line;
    window.location.href = vsUri;
  }} else if (action.classList.contains('file-claude')) {{
    _openViaServer('claude', resolved, line);
  }} else if (action.classList.contains('file-view')) {{
    var viewUrl = '/_view?path=' + encodeURIComponent(resolved) + '&line=' + (line || 0);
    window.open(viewUrl, '_blank');
  }}
}});

function parseCategoryLabel(label) {{
  var catMap = window._categoryMap || {{}};
  if (catMap[label]) return catMap[label];
  var m = label.match(/^([\\w][\\w\\s]*?)\\s*\\((\\d+)\\)$/);
  if (!m) return null;
  var name = m[1];
  var keys = Object.keys(catMap);
  for (var i = 0; i < keys.length; i++) {{
    if (catMap[keys[i]].key === name.toLowerCase()) return catMap[keys[i]];
  }}
  return null;
}}

function zoomDiagram(containerId, delta) {{
  if (delta === 0) {{ diagramZoomLevels[containerId] = 1; }}
  else {{ diagramZoomLevels[containerId] = Math.max(0.2, Math.min(3, (diagramZoomLevels[containerId] || 1) + delta)); }}
  var container = document.getElementById(containerId);
  if (!container) return;
  var svg = container.querySelector('svg');
  if (!svg) return;
  var scale = diagramZoomLevels[containerId];
  svg.style.transform = 'scale(' + scale + ')';
}}

function initSortableTable(table) {{
  if (!table) return;
  var headers = table.querySelectorAll('thead th[data-sort-type]');
  if (headers.length === 0) return;
  var tbody = table.querySelector('tbody');
  if (!tbody) return;
  var originalOrder = null;

  headers.forEach(function (th, colIdx) {{
    var sortType = th.getAttribute('data-sort-type');
    if (sortType === 'none') return;
    th.style.cursor = 'pointer';
    th.addEventListener('click', function () {{
      // Capture original order on first sort
      if (!originalOrder) {{
        originalOrder = Array.from(tbody.querySelectorAll('tr'));
      }}
      // Determine next state: none -> asc -> desc -> none
      var currentDir = th.getAttribute('data-sort-dir') || 'none';
      var nextDir = currentDir === 'none' ? 'asc' : currentDir === 'asc' ? 'desc' : 'none';

      // Clear all other headers
      headers.forEach(function (h) {{
        h.setAttribute('data-sort-dir', 'none');
        var ind = h.querySelector('.sort-indicator');
        if (ind) ind.remove();
      }});

      if (nextDir === 'none') {{
        // Restore original order
        th.setAttribute('data-sort-dir', 'none');
        originalOrder.forEach(function (row) {{ tbody.appendChild(row); }});
        return;
      }}

      th.setAttribute('data-sort-dir', nextDir);
      var indicator = document.createElement('span');
      indicator.className = 'sort-indicator';
      indicator.textContent = nextDir === 'asc' ? '\u25B2' : '\u25BC';
      th.appendChild(indicator);

      var rows = Array.from(tbody.querySelectorAll('tr'));
      rows.sort(function (a, b) {{
        var aCell = a.children[colIdx];
        var bCell = b.children[colIdx];
        if (!aCell || !bCell) return 0;
        var aVal = (aCell.textContent || '').trim();
        var bVal = (bCell.textContent || '').trim();
        var cmp;
        if (sortType === 'risk') {{
          var riskLevelWeight = {{ red: 300, yellow: 200, green: 100, none: 0 }};
          var aRisk = a.getAttribute('data-risk-level') || 'none';
          var bRisk = b.getAttribute('data-risk-level') || 'none';
          cmp = (riskLevelWeight[aRisk] || 0) - (riskLevelWeight[bRisk] || 0);
          if (cmp === 0) {{
            // Secondary sort: count of dots (more smells = higher)
            var aDots = aCell.querySelectorAll('span[style*="border-radius"]').length;
            var bDots = bCell.querySelectorAll('span[style*="border-radius"]').length;
            cmp = aDots - bDots;
          }}
        }} else if (sortType === 'num') {{
          cmp = (parseFloat(aVal) || 0) - (parseFloat(bVal) || 0);
        }} else {{
          cmp = aVal.localeCompare(bVal, undefined, {{ numeric: true, sensitivity: 'base' }});
        }}
        return nextDir === 'desc' ? -cmp : cmp;
      }});
      rows.forEach(function (row) {{ tbody.appendChild(row); }});
    }});
  }});
}}

(function () {{
  'use strict';

  var categoryClass = {{
    'webapp': 'tag-webapp', 'library': 'tag-library', 'application': 'tag-application',
    'service': 'tag-service', 'tool': 'tag-tool', 'test': 'tag-test',
    'connector': 'tag-connector', 'desktopapp': 'tag-desktopapp'
  }};

  function tagHTML(category) {{
    var lower = (category || '').toLowerCase();
    var cls = categoryClass[lower] || 'tag-service';
    return '<span class="tag ' + cls + '">' + escHtml(category) + '</span>';
  }}

  var layerClass = {{
    'presentation': 'tag-presentation', 'engine': 'tag-connector',
    'service': 'tag-service', 'dataaccess': 'tag-dataaccess',
    'infrastructure': 'tag-infrastructure', 'unclassified': 'tag-unclassified'
  }};

  function layerTagHTML(layer, confidence) {{
    if (!layer) return '';
    var lower = layer.toLowerCase();
    var cls = layerClass[lower] || 'tag-unclassified';
    var confColor = confidence >= 0.7 ? '#009639' : confidence >= 0.4 ? '#9E8700' : '#D0002B';
    var confDot = '<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:' + confColor + ';margin-left:4px;" title="Confidence: ' + (confidence * 100).toFixed(0) + '%"></span>';
    return '<span class="tag ' + cls + '">' + escHtml(layer) + confDot + '</span>';
  }}

  function escHtml(s) {{
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }}

  function catDir(cat) {{
    if (cat === 'Connector') return 'connectors';
    if (cat === 'Library') return 'libraries';
    return 'applications';
  }}

  function parseCSV(text) {{
    var lines = text.trim().split('\\n');
    if (lines.length === 0) return [];
    var headers = lines[0].split(',');
    var rows = [];
    for (var i = 1; i < lines.length; i++) {{
      var vals = lines[i].split(',');
      var obj = {{}};
      headers.forEach(function (h, idx) {{ obj[h.trim()] = (vals[idx] || '').trim(); }});
      rows.push(obj);
    }}
    return rows;
  }}

  var tabButtons = document.querySelectorAll('.tab-btn');
  var tabPanels  = document.querySelectorAll('.tab-panel');
  var renderedTabs = {{}};

  function activateTab(tabId) {{
    tabButtons.forEach(function (b) {{ b.classList.toggle('active', b.dataset.tab === tabId); }});
    tabPanels.forEach(function (p)  {{ p.classList.toggle('active', p.id === 'panel-' + tabId); }});
    lazyRenderMermaid(tabId);
  }}
  window.activateTab = activateTab;

  tabButtons.forEach(function (btn) {{
    btn.addEventListener('click', function () {{ activateTab(btn.dataset.tab); }});
  }});

  var mermaidContainers = {{ {mermaid_map_entries} }};

  function lazyRenderMermaid(tabId) {{
    var containerId = mermaidContainers[tabId];
    if (!containerId || renderedTabs[tabId]) return;

    function doRender() {{
      var container = document.getElementById(containerId);
      if (!container) return;
      var pre = container.querySelector('pre.mermaid');
      if (!pre) return;
      renderedTabs[tabId] = true;
      var loading = container.querySelector('.loading');
      pre.style.display = '';
      if (loading) loading.style.display = 'none';
      window.mermaidAPI.run({{ nodes: [pre] }}).then(function () {{
        // Fix SVG sizing: use natural viewBox width instead of 100%
        var svg = container.querySelector('svg');
        if (svg) {{
          var vb = svg.getAttribute('viewBox');
          if (vb) {{
            var parts = vb.split(' ');
            var naturalWidth = parseFloat(parts[2]);
            var naturalHeight = parseFloat(parts[3]);
            svg.style.width = naturalWidth + 'px';
            svg.style.height = naturalHeight + 'px';
            svg.style.maxWidth = 'none';
            svg.removeAttribute('width');
          }}
          attachEdgeTooltips(svg);
          attachCategoryNodeClicks(svg);
        }}
      }}).catch(function (err) {{
        console.error('Mermaid render error for ' + tabId + ':', err);
        if (loading) {{ loading.textContent = 'Diagram rendering failed.'; loading.style.display = ''; }}
      }});
    }}

    if (window.mermaidAPI) {{ doRender(); }}
    else {{
      var interval = setInterval(function () {{
        if (window.mermaidAPI) {{ clearInterval(interval); doRender(); }}
      }}, 150);
    }}
  }}

  // Render first tab on load
  var firstTab = document.querySelector('.tab-btn');
  if (firstTab) lazyRenderMermaid(firstTab.dataset.tab);

  // Init sorting on static tables
  initSortableTable(document.getElementById('datasourcesTable'));
  initSortableTable(document.getElementById('connstringsTable'));
  initSortableTable(document.getElementById('impliedDepsTable'));
  initSortableTable(document.getElementById('flowPathsTable'));
  initSortableTable(document.getElementById('fieldTraceTable'));
  initSortableTable(document.getElementById('reposTable'));

  // Global project data for edge detail lookups
  window._projData = {{ meta: [], refs: [], deps: [], dataSources: [] }};
  window._dataFlow = {{ dataNodes: [], dataEdges: [], impliedDependencies: [], infrastructureGroups: [] }};
  window._categoryMap = {{ {cat_map_entries} }};
  window._hotspotData = {hotspot_json};
  window._codeQualityData = {cq_embedded};
  window._uxData = {ux_embedded};
  window._repoRoots = {repos_roots_json};
  window._externalToolsData = {ext_tools_embedded};
  window._isMultiRepo = {str(is_multi_repo).lower()};

  // Load data-flow.json for edge detail panel
  fetch('data-flow.json').then(function (r) {{ return r.json(); }}).then(function (df) {{
    window._dataFlow = df;
  }}).catch(function () {{ /* data-flow.json may not exist on older runs */ }});

  // Load field-traceability.json
  window._fieldTrace = {{ fieldChains: [], summary: {{}} }};
  fetch('field-traceability.json').then(function (r) {{ return r.json(); }}).then(function (ft) {{
    window._fieldTrace = ft;
  }}).catch(function () {{ /* field-traceability.json may not exist */ }});

  // Load flow-paths.json for E2E flows tab, then load All Projects data
  window._flowData = {{ businessLayers: {{}}, flowPaths: [], layerSummary: {{}} }};
  fetch('flow-paths.json').then(function (r) {{ return r.json(); }}).then(function (fd) {{
    window._flowData = fd;
  }}).catch(function () {{ /* flow-paths.json may not exist */ }}).finally(function () {{

  // Load All Projects data (after flow-paths.json)
  Promise.all([
    fetch('project-meta.json').then(function (r) {{ return r.json(); }}),
    fetch('project-refs.csv').then(function (r) {{ return r.text(); }}),
    fetch('dependencies.csv').then(function (r) {{ return r.text(); }}),
    fetch('data-sources.json').then(function (r) {{ return r.json(); }}).catch(function () {{ return []; }})
  ]).then(function (results) {{
    var meta = results[0], refs = parseCSV(results[1]), deps = parseCSV(results[2]), dataSrc = results[3];
    window._projData = {{ meta: meta, refs: refs, deps: deps, dataSources: dataSrc }};
    var refCounts = {{}}, depCounts = {{}};
    refs.forEach(function (r) {{ refCounts[r.project] = (refCounts[r.project] || 0) + 1; }});
    deps.forEach(function (d) {{ depCounts[d.project] = (depCounts[d.project] || 0) + 1; }});
    var tbody = document.getElementById('projectsBody');
    tbody.innerHTML = '';
    var bl = (window._flowData || {{}}).businessLayers || {{}};
    meta.forEach(function (p) {{
      var tr = document.createElement('tr');
      var layerInfo = bl[p.project] || {{}};
      var layerName = layerInfo.layer || '';
      var layerConf = layerInfo.confidence || 0;
      tr.setAttribute('data-search', (p.project + ' ' + (p.repo||'') + ' ' + p.category + ' ' + layerName + ' ' + (p.globalPath||p.path||'')).toLowerCase());
      var docPath = window._isMultiRepo
        ? 'docs/repos/' + encodeURIComponent(p.repo || 'unknown') + '/' + encodeURIComponent(p.project) + '.md'
        : 'docs/' + catDir(p.category) + '/' + encodeURIComponent(p.project) + '.md';
      tr.innerHTML =
        '<td><strong><a href="' + docPath + '" target="_blank" title="Open project docs">' + escHtml(p.project) + '</a></strong></td>' +
        '<td>' + escHtml(p.repo || '') + '</td>' +
        '<td>' + tagHTML(p.category) + '</td>' +
        '<td>' + layerTagHTML(layerName, layerConf) + '</td>' +
        '<td style="text-align:center">' + (refCounts[p.project] || 0) + '</td>' +
        '<td style="text-align:center">' + (depCounts[p.project] || 0) + '</td>' +
        (function() {{ var fp = p.globalPath || p.path || ''; return fp ? '<td>' + fileActionsHtml(fp, 0) + '</td>' : '<td class="mono"></td>'; }})();
      tbody.appendChild(tr);
    }});
    initSortableTable(document.getElementById('projectsTable'));
  }}).catch(function (err) {{
    console.error('Failed to load project data:', err);
    var tbody = document.getElementById('projectsBody');
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:#D0002B;padding:2rem;">Failed to load project data.</td></tr>';
  }});

  }}); // end finally for flow-paths.json

  // Populate hotspots table from embedded data
  (function () {{
    var data = window._hotspotData || [];
    var tbody = document.getElementById('hotspotsBody');
    if (!tbody || data.length === 0) return;
    var total = data.length;
    var topThird = Math.ceil(total / 3);
    var midThird = Math.ceil(total * 2 / 3);
    data.forEach(function (m, idx) {{
      var tr = document.createElement('tr');
      var scoreColor, scoreBg;
      if (idx < topThird) {{ scoreColor = '#D0002B'; scoreBg = 'rgba(208,0,43,0.08)'; }}
      else if (idx < midThird) {{ scoreColor = '#9E8700'; scoreBg = 'rgba(158,135,0,0.06)'; }}
      else {{ scoreColor = '#009639'; scoreBg = 'rgba(0,150,57,0.06)'; }}
      tr.setAttribute('data-search', (m.project + ' ' + m.category + ' ' + (m.layer || '') + ' ' + (m.repo || '')).toLowerCase());
      tr.setAttribute('data-category', (m.category || '').toLowerCase());
      tr.setAttribute('data-layer', (m.layer || '').toLowerCase());
      // Build risk cell & determine highest risk level
      var riskDots = '';
      var riskLabels = '';
      var smellColors = {{ red: '#D0002B', yellow: '#9E8700', green: '#009639' }};
      var riskPriority = {{ red: 3, yellow: 2, green: 1 }};
      var highestRisk = 'none';
      var highestPri = 0;
      (m.smells || []).forEach(function (s) {{
        var c = smellColors[s.level] || '#53565A';
        riskDots += '<span title="' + escHtml(s.explanation) + '" style="display:inline-block;width:10px;height:10px;border-radius:50%;background:' + c + ';margin-right:3px;cursor:help;"></span>';
        riskLabels += '<div style="font-size:0.7rem;color:' + c + ';line-height:1.3;" title="' + escHtml(s.explanation) + '">' + escHtml(s.label) + '</div>';
        var pri = riskPriority[s.level] || 0;
        if (pri > highestPri) {{ highestPri = pri; highestRisk = s.level; }}
      }});
      tr.setAttribute('data-risk-level', highestRisk);
      var riskCell = (m.smells || []).length > 0
        ? '<div style="display:flex;align-items:center;gap:6px;justify-content:center;"><div>' + riskDots + '</div><div style="text-align:left;">' + riskLabels + '</div></div>'
        : '&mdash;';
      tr.innerHTML =
        '<td><strong>' + escHtml(m.project) + '</strong></td>' +
        '<td>' + tagHTML(m.category) + '</td>' +
        '<td>' + layerTagHTML(m.layer || '', m.layer_confidence || 0) + '</td>' +
        '<td style="text-align:center">' + m.fan_out + '</td>' +
        '<td style="text-align:center">' + m.fan_in + '</td>' +
        '<td style="text-align:center">' + m.nuget_deps + '</td>' +
        '<td style="text-align:center">' + m.data_patterns + '</td>' +
        '<td style="text-align:center">' + m.cross_repo_refs + '</td>' +
        '<td style="text-align:center;font-weight:700;color:' + scoreColor + ';background:' + scoreBg + '">' + m.hotspot_score + '</td>' +
        '<td style="text-align:center;font-weight:700;color:' + scoreColor + '">' + (m.risk_score || 0) + '</td>' +
        '<td>' + riskCell + '</td>';
      tbody.appendChild(tr);
    }});
    initSortableTable(document.getElementById('hotspotsTable'));

    // Populate badge counts
    var riskCounts = {{ red: 0, yellow: 0, green: 0, none: 0 }};
    var categories = {{}};
    var layers = {{}};
    var hsRows = document.querySelectorAll('#hotspotsBody tr');
    hsRows.forEach(function (row) {{
      var rl = row.getAttribute('data-risk-level') || 'none';
      riskCounts[rl] = (riskCounts[rl] || 0) + 1;
      var cat = row.getAttribute('data-category') || '';
      if (cat) categories[cat] = true;
      var lay = row.getAttribute('data-layer') || '';
      if (lay) layers[lay] = true;
    }});
    document.querySelectorAll('.hs-badge').forEach(function (b) {{
      var f = b.getAttribute('data-filter');
      var labels = {{ red: 'Risk', yellow: 'Watch', green: 'Stable', none: 'None' }};
      b.textContent = (labels[f] || f) + ': ' + (riskCounts[f] || 0);
    }});

    // Populate category dropdown
    var catSelect = document.getElementById('hsCategoryFilter');
    if (catSelect) {{
      Object.keys(categories).sort().forEach(function (c) {{
        var opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c.charAt(0).toUpperCase() + c.slice(1);
        catSelect.appendChild(opt);
      }});
    }}

    // Populate layer dropdown
    var laySelect = document.getElementById('hsLayerFilter');
    if (laySelect) {{
      Object.keys(layers).sort().forEach(function (l) {{
        var opt = document.createElement('option');
        opt.value = l;
        opt.textContent = l.charAt(0).toUpperCase() + l.slice(1);
        laySelect.appendChild(opt);
      }});
    }}

    // Badge click handlers
    document.querySelectorAll('.hs-badge').forEach(function (badge) {{
      badge.addEventListener('click', function () {{
        var isActive = badge.classList.contains('hs-badge-active');
        document.querySelectorAll('.hs-badge').forEach(function (b) {{ b.classList.remove('hs-badge-active'); }});
        if (!isActive) {{
          badge.classList.add('hs-badge-active');
        }}
        applyHotspotFilters();
      }});
    }});

    // Dropdown change handlers
    if (catSelect) catSelect.addEventListener('change', function () {{ applyHotspotFilters(); }});
    if (laySelect) laySelect.addEventListener('change', function () {{ applyHotspotFilters(); }});
  }})();

  // ── Code Quality IIFE ──
  (function () {{
    var cqData = window._codeQualityData || {{}};
    var projects = cqData.projects || [];
    var repoRoots = window._repoRoots || {{}};
    var tbody = document.getElementById('cqBody');
    if (!tbody || projects.length === 0) return;

    var sevColors = {{ critical: '#D0002B', high: '#E87722', medium: '#9E8700', low: '#53565A' }};

    function sevBadge(sev) {{
      var c = sevColors[sev] || '#53565A';
      return '<span style="display:inline-block;padding:0.1rem 0.4rem;border-radius:4px;font-size:0.65rem;font-weight:600;background:rgba(' + hexToRgb(c) + ',0.15);color:' + c + ';">' + escHtml(sev || '') + '</span>';
    }}

    function buildFileDetail(p) {{
      var files = p.files || [];
      if (files.length === 0) return '<div style="padding:0.5rem;color:#53565A;font-style:italic;">No file-level data available</div>';
      var root = repoRoots[p.repo || ''] || '';
      var h = '<table style="width:100%;font-size:0.8rem;border-collapse:collapse;margin:0.3rem 0;">';
      h += '<thead><tr style="background:#F5F5F5;"><th style="padding:0.3rem 0.5rem;text-align:left;color:#53565A;font-size:0.7rem;">File</th><th style="padding:0.3rem 0.5rem;text-align:left;color:#53565A;font-size:0.7rem;">Line</th><th style="padding:0.3rem 0.5rem;text-align:left;color:#53565A;font-size:0.7rem;">Severity</th><th style="padding:0.3rem 0.5rem;text-align:left;color:#53565A;font-size:0.7rem;">Smell</th><th style="padding:0.3rem 0.5rem;text-align:left;color:#53565A;font-size:0.7rem;">Context</th></tr></thead><tbody>';
      files.forEach(function(f) {{
        var fname = f.file ? f.file.split(/[\\/\\\\]/).pop() : '?';
        var fPath = f.file || '';
        (f.smells || []).forEach(function(s) {{
          var sc = sevColors[s.severity] || '#53565A';
          var fActions = fPath ? fileActionsHtml(fPath, s.line || 0, 'font-size:0.75rem;color:#005587;') : escHtml(fname);
          h += '<tr style="border-bottom:1px solid #F5F5F5;">';
          h += '<td style="padding:0.25rem 0.5rem;">' + fActions + '</td>';
          h += '<td style="padding:0.25rem 0.5rem;text-align:center;">' + (s.line || '') + '</td>';
          h += '<td style="padding:0.25rem 0.5rem;">' + sevBadge(s.severity) + '</td>';
          h += '<td style="padding:0.25rem 0.5rem;"><span style="display:inline-block;padding:0.1rem 0.4rem;border-radius:4px;font-size:0.7rem;font-weight:600;background:rgba(' + hexToRgb(sc) + ',0.15);color:' + sc + ';">' + escHtml(s.type) + '</span></td>';
          h += '<td style="padding:0.25rem 0.5rem;color:#53565A;font-size:0.78rem;">' + escHtml(s.context || '') + '</td>';
          h += '</tr>';
        }});
      }});
      h += '</tbody></table>';
      return h;
    }}

    var categories = {{}};
    projects.forEach(function (p) {{
      var tr = document.createElement('tr');
      var score = p.refactoring_value_score || 0;
      var scoreColor = score > 100 ? '#D0002B' : score > 50 ? '#9E8700' : '#009639';
      var topSmell = (p.top_smells && p.top_smells.length > 0) ? p.top_smells[0] : '';
      var smellList = (p.top_smells || []).join(',');
      var hasFiles = p.files && p.files.length > 0;
      // Collect severity set for this project
      var sevSet = {{}};
      (p.files || []).forEach(function(f) {{ (f.smells || []).forEach(function(s) {{ if (s.severity) sevSet[s.severity] = true; }}); }});
      var sevList = Object.keys(sevSet).join(',');
      tr.setAttribute('data-search', (p.project + ' ' + (p.category || '') + ' ' + (p.repo || '') + ' ' + smellList).toLowerCase());
      tr.setAttribute('data-category', (p.category || '').toLowerCase());
      tr.setAttribute('data-has-tests', p.has_tests ? 'true' : 'false');
      tr.setAttribute('data-smells', smellList.toLowerCase());
      tr.setAttribute('data-severities', sevList.toLowerCase());
      if (hasFiles) tr.style.cursor = 'pointer';
      tr.innerHTML =
        '<td><strong>' + (hasFiles ? '<span style="color:#005587;margin-right:0.3rem;">&#9654;</span>' : '') + escHtml(p.project || '') + '</strong></td>' +
        '<td>' + tagHTML(p.category || '') + '</td>' +
        '<td style="text-align:center;font-weight:700;color:' + scoreColor + '">' + score + '</td>' +
        '<td style="text-align:center">' + (p.smell_count || 0) + '</td>' +
        '<td>' + escHtml(topSmell) + '</td>' +
        '<td style="text-align:center">' + (p.total_lines || 0).toLocaleString() + '</td>' +
        '<td style="text-align:center">' + (p.complexity_score || 0) + '</td>' +
        '<td style="text-align:center">' + (p.has_tests ? '<span style="color:#009639">&#10003;</span>' : '<span style="color:#D0002B">&#10007;</span>') + '</td>';
      tbody.appendChild(tr);

      // Expandable detail row
      if (hasFiles) {{
        var detailTr = document.createElement('tr');
        detailTr.className = 'cq-detail-row';
        detailTr.style.display = 'none';
        var detailTd = document.createElement('td');
        detailTd.colSpan = 8;
        detailTd.style.padding = '0 0.5rem 0.75rem 1.5rem';
        detailTd.style.background = '#FAFAFA';
        detailTr.appendChild(detailTd);
        tbody.appendChild(detailTr);

        tr.addEventListener('click', function () {{
          var showing = detailTr.style.display !== 'none';
          // Collapse any open detail rows
          document.querySelectorAll('.cq-detail-row').forEach(function(dr) {{ dr.style.display = 'none'; }});
          document.querySelectorAll('#cqBody tr[data-search] span').forEach(function(s) {{
            if (s.textContent === '\u25BC') s.textContent = '\u25B6';
          }});
          if (!showing) {{
            if (!detailTd.innerHTML) detailTd.innerHTML = buildFileDetail(p);
            detailTr.style.display = '';
            var arrow = tr.querySelector('td:first-child span');
            if (arrow) arrow.textContent = '\u25BC';
          }}
        }});
      }}

      var cat = (p.category || '').toLowerCase();
      if (cat) categories[cat] = true;
    }});
    initSortableTable(document.getElementById('cqTable'));

    // Populate category dropdown
    var cqCatSelect = document.getElementById('cqCategoryFilter');
    if (cqCatSelect) {{
      Object.keys(categories).sort().forEach(function (c) {{
        var opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c.charAt(0).toUpperCase() + c.slice(1);
        cqCatSelect.appendChild(opt);
      }});
    }}

    // Smell badge click handlers
    document.querySelectorAll('.cq-badge').forEach(function (badge) {{
      badge.addEventListener('click', function () {{
        var isActive = badge.classList.contains('cq-badge-active');
        document.querySelectorAll('.cq-badge').forEach(function (b) {{ b.classList.remove('cq-badge-active'); }});
        if (!isActive) badge.classList.add('cq-badge-active');
        applyCqFilters();
      }});
    }});

    // Severity badge click handlers
    document.querySelectorAll('.cq-sev-badge').forEach(function (badge) {{
      badge.addEventListener('click', function () {{
        var isActive = badge.classList.contains('cq-sev-badge-active');
        document.querySelectorAll('.cq-sev-badge').forEach(function (b) {{ b.classList.remove('cq-sev-badge-active'); }});
        if (!isActive) badge.classList.add('cq-sev-badge-active');
        applyCqFilters();
      }});
    }});

    // Dropdown handlers
    if (cqCatSelect) cqCatSelect.addEventListener('change', function () {{ applyCqFilters(); }});
    var cqTestSelect = document.getElementById('cqTestsFilter');
    if (cqTestSelect) cqTestSelect.addEventListener('change', function () {{ applyCqFilters(); }});
  }})();

  function applyCqFilters() {{
    var activeBadge = document.querySelector('.cq-badge.cq-badge-active');
    var smellFilter = activeBadge ? activeBadge.getAttribute('data-smell').toLowerCase() : '';
    var activeSevBadge = document.querySelector('.cq-sev-badge.cq-sev-badge-active');
    var sevFilter = activeSevBadge ? activeSevBadge.getAttribute('data-severity').toLowerCase() : '';
    var catFilter = (document.getElementById('cqCategoryFilter') || {{}}).value || '';
    var testFilter = (document.getElementById('cqTestsFilter') || {{}}).value || '';
    var searchQuery = (document.getElementById('searchInput') || {{}}).value || '';
    searchQuery = searchQuery.trim().toLowerCase();

    // Collapse all detail rows on filter
    document.querySelectorAll('.cq-detail-row').forEach(function(dr) {{ dr.style.display = 'none'; }});
    document.querySelectorAll('#cqBody tr[data-search] span').forEach(function(s) {{
      if (s.textContent === '\u25BC') s.textContent = '\u25B6';
    }});
    var rows = document.querySelectorAll('#cqBody tr[data-search]');
    rows.forEach(function (row) {{
      var show = true;
      if (smellFilter) {{
        var smells = row.getAttribute('data-smells') || '';
        if (smells.indexOf(smellFilter) === -1) show = false;
      }}
      if (sevFilter) {{
        var rowSevs = row.getAttribute('data-severities') || '';
        if (rowSevs.indexOf(sevFilter) === -1) show = false;
      }}
      if (catFilter && row.getAttribute('data-category') !== catFilter) show = false;
      if (testFilter && row.getAttribute('data-has-tests') !== testFilter) show = false;
      if (searchQuery) {{
        var text = row.getAttribute('data-search') || '';
        if (text.indexOf(searchQuery) === -1) show = false;
      }}
      row.style.display = show ? '' : 'none';
    }});
  }}

  // ── Security IIFE ──
  (function () {{
    var cqData = window._codeQualityData || {{}};
    var projects = cqData.projects || [];
    var repoRoots = window._repoRoots || {{}};
    var extData = window._externalToolsData || {{}};
    var tbody = document.getElementById('securityBody');
    if (!tbody) return;

    var sevColors = {{ critical: '#D0002B', high: '#E87722', medium: '#9E8700', low: '#53565A' }};
    var secFindings = [];
    projects.forEach(function (p) {{
      (p.files || []).forEach(function (f) {{
        (f.smells || []).forEach(function (s) {{
          if (s.category === 'security') {{
            secFindings.push({{ project: p.project, repo: p.repo || '', file: f.file || '', line: s.line || 0, type: s.type || '', severity: s.severity || '', context: s.context || '' }});
          }}
        }});
      }});
    }});
    // Merge external tool security findings
    (extData.findings || []).forEach(function (ef) {{
      if (ef.category === 'security') {{
        secFindings.push({{ project: '', repo: '', file: ef.file || '', line: ef.line || 0, type: '[' + (ef.tool || '') + '] ' + (ef.ruleId || ''), severity: ef.severity || '', context: ef.message || '' }});
      }}
    }});
    // Sort: critical first, then high
    var sevOrder = {{ critical: 0, high: 1, medium: 2, low: 3 }};
    secFindings.sort(function (a, b) {{ return (sevOrder[a.severity] || 9) - (sevOrder[b.severity] || 9); }});
    secFindings.forEach(function (sf) {{
      var tr = document.createElement('tr');
      var c = sevColors[sf.severity] || '#53565A';
      var fActions = sf.file ? fileActionsHtml(sf.file, sf.line, 'font-size:0.8rem;color:#005587;') : escHtml(sf.file);
      tr.setAttribute('data-search', (sf.project + ' ' + sf.file + ' ' + sf.type + ' ' + sf.context).toLowerCase());
      tr.style.borderLeft = '3px solid ' + c;
      tr.innerHTML =
        '<td style="padding:0.4rem 0.5rem;">' + fActions + '</td>' +
        '<td style="padding:0.4rem 0.5rem;text-align:center;">' + sf.line + '</td>' +
        '<td style="padding:0.4rem 0.5rem;">' + escHtml(sf.type) + '</td>' +
        '<td style="padding:0.4rem 0.5rem;"><span style="display:inline-block;padding:0.1rem 0.4rem;border-radius:4px;font-size:0.7rem;font-weight:600;background:rgba(' + hexToRgb(c) + ',0.15);color:' + c + ';">' + escHtml(sf.severity) + '</span></td>' +
        '<td style="padding:0.4rem 0.5rem;color:#53565A;font-size:0.82rem;">' + escHtml(sf.context) + '</td>';
      tbody.appendChild(tr);
    }});
    initSortableTable(document.getElementById('securityTable'));
  }})();

  // ── External Tools IIFE ──
  (function () {{
    var extData = window._externalToolsData || {{}};
    var findings = extData.findings || [];
    var tbody = document.getElementById('extToolsBody');
    if (!tbody || findings.length === 0) return;

    var sevColors = {{ critical: '#D0002B', high: '#E87722', medium: '#9E8700', low: '#53565A' }};
    var sevOrder = {{ critical: 0, high: 1, medium: 2, low: 3 }};
    findings.sort(function (a, b) {{ return (sevOrder[a.severity] || 9) - (sevOrder[b.severity] || 9); }});
    findings.forEach(function (f) {{
      var tr = document.createElement('tr');
      var c = sevColors[f.severity] || '#53565A';
      var fActions = f.file ? fileActionsHtml(f.file, f.line, 'font-size:0.8rem;color:#005587;') : escHtml(f.file || '');
      tr.setAttribute('data-search', ((f.tool || '') + ' ' + (f.file || '') + ' ' + (f.ruleId || '') + ' ' + (f.message || '')).toLowerCase());
      tr.setAttribute('data-tool', f.tool || '');
      tr.style.borderLeft = '3px solid ' + c;
      tr.innerHTML =
        '<td style="padding:0.4rem 0.5rem;font-weight:600;">' + escHtml(f.tool || '') + '</td>' +
        '<td style="padding:0.4rem 0.5rem;">' + fActions + '</td>' +
        '<td style="padding:0.4rem 0.5rem;text-align:center;">' + (f.line || 0) + '</td>' +
        '<td style="padding:0.4rem 0.5rem;font-size:0.8rem;">' + escHtml(f.ruleId || '') + '</td>' +
        '<td style="padding:0.4rem 0.5rem;"><span style="display:inline-block;padding:0.1rem 0.4rem;border-radius:4px;font-size:0.7rem;font-weight:600;background:rgba(' + hexToRgb(c) + ',0.15);color:' + c + ';">' + escHtml(f.severity || '') + '</span></td>' +
        '<td style="padding:0.4rem 0.5rem;">' + escHtml(f.category || '') + '</td>' +
        '<td style="padding:0.4rem 0.5rem;color:#53565A;font-size:0.82rem;">' + escHtml(f.message || '') + '</td>';
      tbody.appendChild(tr);
    }});
    initSortableTable(document.getElementById('extToolsTable'));

    // Tool badge filtering
    var badges = document.querySelectorAll('.ext-tool-badge');
    var activeTool = null;
    badges.forEach(function (badge) {{
      badge.addEventListener('click', function () {{
        var toolName = badge.getAttribute('data-tool');
        if (activeTool === toolName) {{
          activeTool = null;
          badges.forEach(function (b) {{ b.style.opacity = '1'; }});
        }} else {{
          activeTool = toolName;
          badges.forEach(function (b) {{ b.style.opacity = b.getAttribute('data-tool') === toolName ? '1' : '0.4'; }});
        }}
        var rows = tbody.querySelectorAll('tr');
        rows.forEach(function (row) {{
          if (!activeTool || row.getAttribute('data-tool') === activeTool) {{
            row.style.display = '';
          }} else {{
            row.style.display = 'none';
          }}
        }});
      }});
    }});
  }})();

  // ── UX Consistency IIFE ──
  (function () {{
    var uxData = window._uxData || {{}};
    var issues = uxData.issues || [];
    var tbody = document.getElementById('uxBody');
    if (!tbody || issues.length === 0) return;
    var sevColors = {{ error: '#D0002B', warning: '#9E8700', info: '#53565A' }};
    issues.forEach(function (iss) {{
      var tr = document.createElement('tr');
      var c = sevColors[iss.severity] || '#53565A';
      tr.setAttribute('data-search', (iss.project + ' ' + iss.type + ' ' + (iss.file || '') + ' ' + iss.message).toLowerCase());
      tr.setAttribute('data-severity', iss.severity || '');
      tr.setAttribute('data-type', iss.type || '');
      var viewClass = iss.viewType || iss.className || '';
      tr.innerHTML =
        '<td><span style="display:inline-block;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:600;background:rgba(' + hexToRgb(c) + ',0.15);color:' + c + ';">' + escHtml(iss.severity || '') + '</span></td>' +
        '<td>' + escHtml(iss.type || '') + '</td>' +
        '<td><strong>' + escHtml(iss.project || '') + '</strong></td>' +
        '<td class="mono" style="font-size:0.75rem;">' + escHtml(iss.file || '') + '</td>' +
        '<td>' + escHtml(viewClass) + '</td>' +
        '<td>' + escHtml(iss.message || '') + '</td>';
      // Store available properties for detail sidebar
      if (iss.availableProperties) {{
        tr.setAttribute('data-available-props', JSON.stringify(iss.availableProperties));
      }}
      tr.style.cursor = 'pointer';
      tr.addEventListener('click', (function(issue) {{ return function () {{
        var sidebar = document.getElementById('uxDetailSidebar');
        if (!sidebar) return;
        var repoRoots = window._repoRoots || {{}};
        var root = repoRoots[issue.repo || ''] || '';
        var h = '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">';
        h += '<strong style="color:#022D5E;font-size:0.95rem;">' + escHtml(issue.type || '') + '</strong>';
        var sc = sevColors[issue.severity] || '#53565A';
        h += '<span style="padding:0.15rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:600;background:rgba(' + hexToRgb(sc) + ',0.15);color:' + sc + ';">' + escHtml(issue.severity || '') + '</span></div>';
        h += '<div style="margin:0.4rem 0;font-size:0.88rem;">' + escHtml(issue.message || '') + '</div>';
        if (issue.file) {{
          h += '<div style="margin:0.3rem 0;"><span style="color:#53565A;font-size:0.75rem;text-transform:uppercase;">File:</span> ';
          h += fileActionsHtml(issue.file, issue.line, 'color:#005587;font-size:0.85rem;');
          h += '</div>';
        }}
        if (issue.bindingPath) {{
          h += '<div style="margin:0.3rem 0;"><span style="color:#53565A;font-size:0.75rem;text-transform:uppercase;">Binding Path:</span> <code style="background:#F5F5F5;padding:0.1rem 0.4rem;border-radius:3px;">' + escHtml(issue.bindingPath) + '</code></div>';
        }}
        if (issue.resolvedViewModel) {{
          h += '<div style="margin:0.3rem 0;"><span style="color:#53565A;font-size:0.75rem;text-transform:uppercase;">ViewModel:</span> <strong>' + escHtml(issue.resolvedViewModel) + '</strong></div>';
        }}
        var props = tr.getAttribute('data-available-props');
        if (props) {{
          try {{
            var propList = JSON.parse(props);
            // Fuzzy match suggestion
            if (issue.bindingPath && propList.length > 0) {{
              var bp = (issue.bindingPath || '').toLowerCase();
              var suggestions = propList.filter(function(p) {{
                var pl = p.toLowerCase();
                return pl.indexOf(bp) !== -1 || bp.indexOf(pl) !== -1 ||
                  (bp.length > 2 && pl.indexOf(bp.substring(0,3)) !== -1);
              }});
              if (suggestions.length > 0 && suggestions.length < propList.length) {{
                h += '<div style="margin:0.5rem 0;padding:0.5rem;background:#E8F5E9;border-radius:6px;"><strong style="color:#009639;">Did you mean?</strong> ' + suggestions.map(function(s) {{ return '<code style="background:#FFFFFF;padding:0.1rem 0.4rem;border-radius:3px;">' + escHtml(s) + '</code>'; }}).join(', ') + '</div>';
              }}
            }}
            h += '<div style="margin-top:0.5rem;"><strong>Available VM Properties:</strong><ul style="margin:0.3rem 0;padding-left:1.2rem;">' +
              propList.map(function(p) {{ return '<li style="font-size:0.85rem;">' + escHtml(p) + '</li>'; }}).join('') + '</ul></div>';
          }} catch(e) {{ /* skip */ }}
        }}
        sidebar.innerHTML = h;
        sidebar.style.display = 'block';
      }}; }})(iss));
      tbody.appendChild(tr);
    }});
    initSortableTable(document.getElementById('uxTable'));

    // Badge click handlers
    document.querySelectorAll('.ux-badge').forEach(function (badge) {{
      badge.addEventListener('click', function () {{
        var isActive = badge.classList.contains('ux-badge-active');
        document.querySelectorAll('.ux-badge').forEach(function (b) {{ b.classList.remove('ux-badge-active'); }});
        if (!isActive) badge.classList.add('ux-badge-active');
        applyUxFilters();
      }});
    }});
  }})();

  function applyUxFilters() {{
    var activeBadge = document.querySelector('.ux-badge.ux-badge-active');
    var sevFilter = activeBadge ? activeBadge.getAttribute('data-severity') || '' : '';
    var typeFilter = activeBadge ? activeBadge.getAttribute('data-type') || '' : '';
    var searchQuery = (document.getElementById('searchInput') || {{}}).value || '';
    searchQuery = searchQuery.trim().toLowerCase();

    var rows = document.querySelectorAll('#uxBody tr[data-search]');
    rows.forEach(function (row) {{
      var show = true;
      if (sevFilter && row.getAttribute('data-severity') !== sevFilter) show = false;
      if (typeFilter && row.getAttribute('data-type') !== typeFilter) show = false;
      if (searchQuery) {{
        var text = row.getAttribute('data-search') || '';
        if (text.indexOf(searchQuery) === -1) show = false;
      }}
      row.style.display = show ? '' : 'none';
    }});
  }}

  // ── NuGet Health sorting init ──
  initSortableTable(document.getElementById('nhConflictsTable'));
  initSortableTable(document.getElementById('nhLegacyTable'));

  // ── Tests table sorting init ──
  initSortableTable(document.getElementById('testsTable'));

  // ── Language panel table sorting init ──
  {chr(10).join(f"  initSortableTable(document.getElementById('{lk}Table'));" for lk in sorted(language_data.keys()))}

  // hexToRgb helper for UX badges
  function hexToRgb(hex) {{
    var h = hex.replace('#', '');
    return parseInt(h.substring(0,2),16) + ',' + parseInt(h.substring(2,4),16) + ',' + parseInt(h.substring(4,6),16);
  }}

  // Shared hotspot filter function
  function applyHotspotFilters() {{
    var activeBadge = document.querySelector('.hs-badge.hs-badge-active');
    var riskFilter = activeBadge ? activeBadge.getAttribute('data-filter') : '';
    var catFilter = (document.getElementById('hsCategoryFilter') || {{}}).value || '';
    var layFilter = (document.getElementById('hsLayerFilter') || {{}}).value || '';
    var searchQuery = (document.getElementById('searchInput') || {{}}).value || '';
    searchQuery = searchQuery.trim().toLowerCase();

    var rows = document.querySelectorAll('#hotspotsBody tr[data-search]');
    rows.forEach(function (row) {{
      var show = true;
      if (riskFilter && row.getAttribute('data-risk-level') !== riskFilter) show = false;
      if (catFilter && row.getAttribute('data-category') !== catFilter) show = false;
      if (layFilter && row.getAttribute('data-layer') !== layFilter) show = false;
      if (searchQuery) {{
        var text = row.getAttribute('data-search') || '';
        if (text.indexOf(searchQuery) === -1) show = false;
      }}
      row.style.display = show ? '' : 'none';
    }});
  }}

  // Search
  var searchInput = document.getElementById('searchInput');
  searchInput.addEventListener('input', function () {{
    var query = searchInput.value.trim().toLowerCase();
    var rows = document.querySelectorAll('#projectsBody tr[data-search]');
    rows.forEach(function (row) {{
      var text = row.getAttribute('data-search') || '';
      row.style.display = (!query || text.indexOf(query) !== -1) ? '' : 'none';
    }});
    applyHotspotFilters();
    applyCqFilters();
    applyUxFilters();
  }});

  // Flow paths search
  var flowSearchInput = document.getElementById('flowSearchInput');
  if (flowSearchInput) {{
    flowSearchInput.addEventListener('input', function () {{
      var query = flowSearchInput.value.trim().toLowerCase();
      var rows = document.querySelectorAll('#flowPathsBody .flow-row');
      rows.forEach(function (row) {{
        var text = row.getAttribute('data-search') || '';
        row.style.display = (!query || text.indexOf(query) !== -1) ? '' : 'none';
      }});
    }});
  }}

  // Flow path click-to-expand
  var flowBody = document.getElementById('flowPathsBody');
  if (flowBody) {{
    flowBody.addEventListener('click', function (e) {{
      var row = e.target.closest('.flow-row');
      if (!row) return;
      var idx = parseInt(row.getAttribute('data-flow-idx'), 10);
      showFlowDetail(idx);
    }});
  }}

  function showFlowDetail(idx) {{
    var fd = window._flowData || {{}};
    var paths = fd.flowPaths || [];
    if (idx < 0 || idx >= paths.length) return;
    var fp = paths[idx];
    var container = document.getElementById('flowDetailContainer');
    var content = document.getElementById('flowDetailContent');
    var mermaidDiv = document.getElementById('flowDetailMermaid');
    if (!container || !content) return;

    // Build step-by-step detail
    var html = '<div style="margin-bottom:0.5rem;">';
    if (fp.namedFlow) {{
      html += '<strong style="color:#005587;">' + escHtml(fp.namedFlow) + '</strong><br/>';
    }}
    if (fp.description) {{
      html += '<span style="color:#53565A;font-size:0.85rem;">' + escHtml(fp.description) + '</span><br/>';
    }}
    html += '<span style="color:#53565A;font-size:0.8rem;">Depth: ' + fp.pathLength + ' | Layers: ' + (fp.crossesLayers || []).join(' &rarr; ') + '</span>';
    html += '</div>';

    // Step-by-step chain with layer badges
    html += '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.3rem;">';
    var bl = fd.businessLayers || {{}};
    (fp.path || []).forEach(function (step, i) {{
      if (i > 0) html += '<span class="flow-arrow">&rarr;</span>';
      if (step.project) {{
        var li = bl[step.project] || {{}};
        html += '<span class="flow-step">' + layerTagHTML(li.layer || step.layer || '', li.confidence || 0) + ' <strong>' + escHtml(step.project) + '</strong></span>';
      }} else if (step.endpoint) {{
        var epName = step.endpoint.indexOf(':') !== -1 ? step.endpoint.split(':').slice(1).join(':') : step.endpoint;
        var epType = step.type || '';
        html += '<span class="flow-step"><span class="tag tag-db">' + escHtml(epType) + '</span> <em>' + escHtml(epName) + '</em></span>';
      }}
    }});
    html += '</div>';
    content.innerHTML = html;

    // Render inline Mermaid diagram for this path
    if (mermaidDiv && window.mermaidAPI) {{
      var mermaidSrc = buildFlowPathMermaid(fp, bl);
      mermaidDiv.innerHTML = '<pre class="mermaid">' + escHtml(mermaidSrc) + '</pre>';
      var pre = mermaidDiv.querySelector('pre.mermaid');
      if (pre) {{
        window.mermaidAPI.run({{ nodes: [pre] }}).then(function () {{
          var svg = mermaidDiv.querySelector('svg');
          if (svg) {{
            var vb = svg.getAttribute('viewBox');
            if (vb) {{
              var parts = vb.split(' ');
              svg.style.width = parseFloat(parts[2]) + 'px';
              svg.style.height = parseFloat(parts[3]) + 'px';
              svg.style.maxWidth = 'none';
              svg.removeAttribute('width');
            }}
          }}
        }}).catch(function (err) {{ console.error('Flow mermaid error:', err); }});
      }}
    }}

    container.style.display = 'block';
  }}

  function buildFlowPathMermaid(fp, bl) {{
    var lines = ['graph TD'];
    var prevId = null;
    (fp.path || []).forEach(function (step) {{
      var nid, label;
      if (step.project) {{
        nid = step.project.replace(/[^a-zA-Z0-9_]/g, '_');
        var layer = (bl[step.project] || {{}}).layer || step.layer || '';
        label = step.project + '\\n(' + layer + ')';
        lines.push('    ' + nid + '["' + label + '"]');
      }} else if (step.endpoint) {{
        nid = step.endpoint.replace(/[^a-zA-Z0-9_]/g, '_');
        var epName = step.endpoint.indexOf(':') !== -1 ? step.endpoint.split(':').slice(1).join(':') : step.endpoint;
        var etype = step.type || '';
        if (etype === 'database') {{
          lines.push('    ' + nid + '[("' + epName + '")]');
        }} else if (etype === 'messaging') {{
          lines.push('    ' + nid + '{{{"' + epName + '"}}}');
        }} else {{
          lines.push('    ' + nid + '(["' + epName + '"])');
        }}
      }} else {{ return; }}
      if (prevId) {{
        var edgeType = step.edgeType || '';
        if (edgeType.indexOf('data-flow') !== -1) {{
          lines.push('    ' + prevId + ' ==> ' + nid);
        }} else {{
          lines.push('    ' + prevId + ' --> ' + nid);
        }}
      }}
      prevId = nid;
    }});
    return lines.join('\\n');
  }}

  // Field traceability search
  var ftSearchInput = document.getElementById('ftSearchInput');
  if (ftSearchInput) {{
    ftSearchInput.addEventListener('input', function () {{
      var query = ftSearchInput.value.trim().toLowerCase();
      var rows = document.querySelectorAll('#ftBody .ft-row');
      rows.forEach(function (row) {{
        var text = row.getAttribute('data-search') || '';
        row.style.display = (!query || text.indexOf(query) !== -1) ? '' : 'none';
      }});
    }});
  }}

  // Field traceability badge click-to-filter
  document.querySelectorAll('.ft-badge').forEach(function (badge) {{
    badge.addEventListener('click', function () {{
      var filter = badge.getAttribute('data-filter');
      var rows = document.querySelectorAll('#ftBody .ft-row');
      var allVisible = true;
      rows.forEach(function (row) {{
        if (row.getAttribute('data-completeness') !== filter && row.style.display === 'none') {{
          allVisible = false;
        }}
      }});
      // Toggle: if already filtered to this level, show all; otherwise filter
      var isFiltered = badge.classList.contains('ft-badge-active');
      document.querySelectorAll('.ft-badge').forEach(function (b) {{ b.classList.remove('ft-badge-active'); b.style.outline = ''; }});
      if (isFiltered) {{
        rows.forEach(function (row) {{ row.style.display = ''; }});
      }} else {{
        badge.classList.add('ft-badge-active');
        badge.style.outline = '2px solid ' + badge.style.color;
        rows.forEach(function (row) {{
          row.style.display = row.getAttribute('data-completeness') === filter ? '' : 'none';
        }});
      }}
    }});
  }});

  // Field traceability click-to-expand
  var ftBody = document.getElementById('ftBody');
  if (ftBody) {{
    ftBody.addEventListener('click', function (e) {{
      var row = e.target.closest('.ft-row');
      if (!row) return;
      var idx = parseInt(row.getAttribute('data-ft-idx'), 10);
      showFieldChainDetail(idx);
    }});
  }}

  function showFieldChainDetail(idx) {{
    var ft = window._fieldTrace || {{}};
    var chains = ft.fieldChains || [];
    if (idx < 0 || idx >= chains.length) return;
    var ch = chains[idx];
    var container = document.getElementById('ftDetailContainer');
    var content = document.getElementById('ftDetailContent');
    var mermaidDiv = document.getElementById('ftDetailMermaid');
    if (!container || !content) return;

    var xaml = ch.xamlBinding || {{}};
    var vm = ch.viewModelProperty || {{}};
    var ent = ch.entityProperty || {{}};
    var db = ch.dbColumn || {{}};

    var html = '<div style="margin-bottom:0.5rem;">';
    html += '<span style="color:#53565A;font-size:0.8rem;">Chain ID: ' + escHtml(ch.id || '') + ' | Completeness: <strong style="color:#009639;">' + escHtml(ch.chainCompleteness || '') + '</strong> | Confidence: ' + escHtml(ch.confidence || '') + '</span>';
    html += '</div>';

    // Step-by-step chain (vertical layout for sidebar)
    html += '<div style="display:flex;flex-direction:column;gap:0.3rem;margin-bottom:0.75rem;">';
    if (xaml.viewType) {{
      html += '<div style="background:#FFFFFF;border:1px solid #621244;border-radius:6px;padding:0.4rem 0.6rem;">';
      html += '<div style="font-size:0.7rem;color:#621244;text-transform:uppercase;">XAML View</div>';
      html += '<strong style="font-size:0.82rem;word-break:break-all;">' + escHtml(xaml.viewType) + '</strong>';
      html += '<div class="mono" style="font-size:0.72rem;">' + escHtml(xaml.bindingPath || '') + '</div>';
      html += '<div>' + fileActionsHtml(xaml.file, xaml.line) + '</div>';
      html += '</div>';
      html += '<div style="text-align:center;color:#53565A;font-size:0.9rem;">&darr;</div>';
    }}
    if (vm.className) {{
      html += '<div style="background:#FFFFFF;border:1px solid #36749D;border-radius:6px;padding:0.4rem 0.6rem;">';
      html += '<div style="font-size:0.7rem;color:#36749D;text-transform:uppercase;">ViewModel</div>';
      html += '<strong style="font-size:0.82rem;word-break:break-all;">' + escHtml(vm.className) + '</strong>';
      html += '<div style="font-size:0.78rem;">' + escHtml(vm.propertyName || '') + ': ' + escHtml(vm.propertyType || '') + '</div>';
      html += '<div>' + fileActionsHtml(vm.file, vm.line) + '</div>';
      html += '</div>';
      html += '<div style="text-align:center;color:#53565A;font-size:0.9rem;">&darr;</div>';
    }}
    if (ent.className) {{
      html += '<div style="background:#FFFFFF;border:1px solid #005587;border-radius:6px;padding:0.4rem 0.6rem;">';
      html += '<div style="font-size:0.7rem;color:#005587;text-transform:uppercase;">Entity</div>';
      html += '<strong style="font-size:0.82rem;word-break:break-all;">' + escHtml(ent.className) + '</strong>';
      html += '<div style="font-size:0.78rem;">' + escHtml(ent.propertyName || '') + ': ' + escHtml(ent.propertyType || '') + '</div>';
      html += '<div>' + fileActionsHtml(ent.file, ent.line) + '</div>';
      html += '</div>';
      html += '<div style="text-align:center;color:#53565A;font-size:0.9rem;">&darr;</div>';
    }}
    if (db.table) {{
      html += '<div style="background:#FFFFFF;border:1px solid #009639;border-radius:6px;padding:0.4rem 0.6rem;">';
      html += '<div style="font-size:0.7rem;color:#009639;text-transform:uppercase;">DB Column</div>';
      html += '<strong style="font-size:0.82rem;">' + escHtml(db.table) + '.' + escHtml(db.column || '') + '</strong>';
      html += '<div style="font-size:0.78rem;">Source: ' + escHtml(db.source || '') + '</div>';
      if (db.file) html += '<div>' + fileActionsHtml(db.file, db.line) + '</div>';
      html += '</div>';
    }}
    html += '</div>';

    content.innerHTML = html;

    // Render inline Mermaid for this chain
    if (mermaidDiv && window.mermaidAPI) {{
      var mSrc = buildFieldChainMermaid(ch);
      mermaidDiv.innerHTML = '<pre class="mermaid">' + escHtml(mSrc) + '</pre>';
      var pre = mermaidDiv.querySelector('pre.mermaid');
      if (pre) {{
        window.mermaidAPI.run({{ nodes: [pre] }}).then(function () {{
          var svg = mermaidDiv.querySelector('svg');
          if (svg) {{
            var vb = svg.getAttribute('viewBox');
            if (vb) {{
              var parts = vb.split(' ');
              svg.style.width = parseFloat(parts[2]) + 'px';
              svg.style.height = parseFloat(parts[3]) + 'px';
              svg.style.maxWidth = 'none';
              svg.removeAttribute('width');
            }}
          }}
        }}).catch(function (err) {{ console.error('Field chain mermaid error:', err); }});
      }}
    }}

    container.style.display = 'block';
  }}

  function buildFieldChainMermaid(ch) {{
    var lines = ['graph LR'];
    var prevId = null;

    var xaml = ch.xamlBinding || {{}};
    var vm = ch.viewModelProperty || {{}};
    var ent = ch.entityProperty || {{}};
    var db = ch.dbColumn || {{}};

    if (xaml.viewType) {{
      var xid = (xaml.viewType + '_' + (xaml.bindingPath || '')).replace(/[^a-zA-Z0-9_]/g, '_');
      lines.push('    ' + xid + '["' + xaml.viewType + '\\n' + (xaml.bindingPath || '') + '"]');
      prevId = xid;
    }}
    if (vm.className) {{
      var vid = (vm.className + '_' + (vm.propertyName || '')).replace(/[^a-zA-Z0-9_]/g, '_');
      lines.push('    ' + vid + '["' + vm.className + '\\n' + (vm.propertyName || '') + ': ' + (vm.propertyType || '') + '"]');
      if (prevId) lines.push('    ' + prevId + ' --> ' + vid);
      prevId = vid;
    }}
    if (ent.className) {{
      var eid = (ent.className + '_' + (ent.propertyName || '')).replace(/[^a-zA-Z0-9_]/g, '_');
      lines.push('    ' + eid + '["' + ent.className + '\\n' + (ent.propertyName || '') + ': ' + (ent.propertyType || '') + '"]');
      if (prevId) lines.push('    ' + prevId + ' --> ' + eid);
      prevId = eid;
    }}
    if (db.table) {{
      var did = (db.table + '_' + (db.column || '')).replace(/[^a-zA-Z0-9_]/g, '_');
      lines.push('    ' + did + '[("' + db.table + '\\n' + (db.column || '') + '")]');
      if (prevId) lines.push('    ' + prevId + ' --> ' + did);
    }}

    return lines.join('\\n');
  }}
}})();
</script>
</body>
</html>"""

    return html


# ─── AI Context Export ──────────────────────────────────────────────

def _write_codebase_overview(ai_dir: str, metrics: list[dict]) -> None:
    """Write CODEBASE_OVERVIEW.md with architecture summary."""
    summary = graph["summary"]
    categories = summary["categories"]

    md = f"""# Codebase Overview

> Auto-generated context for AI coding agents. Feed this file to Claude/OpenCode for architecture awareness.

## Architecture Summary

| Metric | Value |
|--------|-------|
| Repositories | {summary.get('totalRepos', 1)} |
| Projects | {summary['totalProjects']} |
| NuGet Packages | {summary['totalNuGetPackages']} |
| Project References | {summary['totalProjectRefs']} |
| Cross-Repo References | {summary.get('totalCrossRepoRefs', 0)} |
| Data Access Findings | {summary['totalDataFindings']} |
| Config Files | {summary['totalConfigFiles']} |

## Categories

| Category | Count | Description |
|----------|-------|-------------|
"""
    cat_descriptions = {
        "Application": "Standalone executable applications",
        "WebApp": "Web-facing applications and APIs",
        "Library": "Shared libraries consumed by other projects",
        "Connector": "Integration connectors to external systems",
        "Service": "Background services and daemons",
        "Tool": "Developer and build tools",
        "Test": "Test projects",
        "DesktopApp": "Desktop GUI applications",
        "Localization": "Localization/translation resources",
        "Sample": "Sample and example projects",
    }
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        desc = cat_descriptions.get(cat, "Project category")
        md += f"| {cat} | {count} | {desc} |\n"

    # Infrastructure patterns
    type_counts: dict[str, int] = {}
    for f in data_findings:
        type_counts[f["type"]] = type_counts.get(f["type"], 0) + 1
    if type_counts:
        md += "\n## Infrastructure Patterns\n\n| Type | Occurrences |\n|------|-------------|\n"
        for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
            md += f"| {t} | {c} |\n"

    # Cross-repo dependencies
    cross_refs = [r for r in project_refs_csv if r.get("crossRepo") == "true"]
    if cross_refs:
        md += "\n## Cross-Repo Dependencies\n\n| From | To | From Repo | To Repo |\n|------|----|-----------|---------|\n"
        seen = set()
        for r in cross_refs:
            key = (r["project"], r["references"])
            if key in seen:
                continue
            seen.add(key)
            from_meta = projects_by_name.get(r["project"], {})
            to_meta = projects_by_name.get(r["references"], {})
            md += f"| {r['project']} | {r['references']} | {from_meta.get('repo', '')} | {to_meta.get('repo', '')} |\n"
            if len(seen) >= 50:
                md += f"\n*... and {len(cross_refs) - 50} more cross-repo references*\n"
                break

    # Top 10 hotspots
    md += "\n## Top 10 Hotspots\n\n"
    md += "| Rank | Project | Category | Score | Key Factors |\n"
    md += "|------|---------|----------|-------|-------------|\n"
    for i, m in enumerate(metrics[:10]):
        factors = []
        if m["fan_out"] >= 5:
            factors.append(f"fan-out:{m['fan_out']}")
        if m["fan_in"] >= 5:
            factors.append(f"fan-in:{m['fan_in']}")
        if m["cross_repo_refs"] > 0:
            factors.append(f"cross-repo:{m['cross_repo_refs']}")
        if m["data_patterns"] >= 3:
            factors.append(f"data:{m['data_patterns']}")
        if m["nuget_deps"] >= 10:
            factors.append(f"nuget:{m['nuget_deps']}")
        md += f"| {i + 1} | {m['project']} | {m['category']} | {m['hotspot_score']} | {', '.join(factors) or 'moderate coupling'} |\n"

    # Code Quality Summary
    if refactoring_data.get("summary"):
        rs = refactoring_data["summary"]
        md += "\n## Code Quality Summary\n\n"
        md += f"| Metric | Value |\n|--------|-------|\n"
        md += f"| Total Smells | {rs.get('totalSmells', 0)} |\n"
        md += f"| Files Scanned | {rs.get('totalFilesScanned', 0)} |\n"
        md += f"| Files With Smells | {rs.get('totalFilesWithSmells', 0)} |\n"
        top_types = rs.get("topSmellTypes", [])
        if top_types:
            md += "\n**Top Smell Types:**\n\n"
            for st in top_types[:10]:
                md += f"- {st['smell']}: {st['count']}\n"
            md += "\n"

    # UX Consistency Summary
    ux_sum = ux_inconsistencies.get("summary", {})
    if ux_sum.get("totalIssues"):
        md += "\n## UX Consistency Summary\n\n"
        md += "| Metric | Value |\n|--------|-------|\n"
        md += f"| Total Issues | {ux_sum.get('totalIssues', 0)} |\n"
        by_sev = ux_sum.get("bySeverity", {})
        md += f"| Errors | {by_sev.get('error', 0)} |\n"
        md += f"| Warnings | {by_sev.get('warning', 0)} |\n"
        md += f"| Info | {by_sev.get('info', 0)} |\n"
        by_type = ux_sum.get("byType", {})
        if by_type:
            md += "\n**Top Issue Types:**\n\n"
            for typ, cnt in sorted(by_type.items(), key=lambda x: -x[1])[:10]:
                md += f"- {typ}: {cnt}\n"
            md += "\n"

    # NuGet Health Summary
    nh_sum = nuget_health.get("summary", {})
    if nh_sum:
        md += "\n## NuGet Health Summary\n\n"
        md += "| Metric | Value |\n|--------|-------|\n"
        md += f"| Version Conflicts | {nh_sum.get('conflictCount', 0)} |\n"
        md += f"| Legacy Projects | {nh_sum.get('legacyCount', 0)} |\n"
        md += f"| Frameworks | {nh_sum.get('frameworkCount', 0)} |\n"
        md += f"| Total Packages | {nh_sum.get('totalPackages', 0)} |\n"
        md += f"| CPM Repos | {nh_sum.get('cpmRepos', 0)} |\n\n"

    # Test Coverage Summary
    t_sum = test_data.get("summary", {})
    if t_sum.get("totalTestProjects"):
        md += "\n## Test Coverage Summary\n\n"
        md += "| Metric | Value |\n|--------|-------|\n"
        md += f"| Test Projects | {t_sum.get('totalTestProjects', 0)} |\n"
        md += f"| Test Methods | {t_sum.get('totalTestMethods', 0)} |\n"
        md += f"| Test Classes | {t_sum.get('totalTestClasses', 0)} |\n"
        md += f"| Coverage Ratio | {t_sum.get('coverageRatio', '0/0')} |\n"
        md += f"| Uncovered Projects | {t_sum.get('uncoveredProjects', 0)} |\n\n"

    # Language scanner summaries
    for _lk, _ld in sorted(language_data.items()):
        _ldisp = _ld.get("displayName", _lk.title())
        _lsum = _ld.get("summary", {})
        md += f"\n## {_ldisp} Projects Summary\n\n"
        md += "| Metric | Value |\n|--------|-------|\n"
        md += f"| Projects | {_lsum.get('totalProjects', 0)} |\n"
        md += f"| Files | {_lsum.get('totalFiles', 0)} |\n"
        md += f"| Lines | {_lsum.get('totalLines', 0)} |\n"
        fws = _lsum.get("frameworks", {})
        if fws:
            md += f"| Frameworks | {', '.join(f'{fw}: {cnt}' for fw, cnt in sorted(fws.items(), key=lambda x: -x[1]))} |\n"
        cats = _lsum.get("categories", {})
        if cats:
            md += f"| Categories | {', '.join(f'{cat}: {cnt}' for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]))} |\n"
        md += "\n"

    md += f"\n---\n*Generated: {date.today().isoformat()}*\n"
    Path(os.path.join(ai_dir, "CODEBASE_OVERVIEW.md")).write_text(md, encoding="utf-8")


def _write_project_context(ai_dir: str, pm: dict, metrics_by_name: dict[str, dict],
                           bl: dict, data_nodes: list) -> None:
    """Write per-project AI context markdown file."""
    project = pm["project"]
    m = metrics_by_name.get(project, {})
    deps = deps_by_project.get(project, [])
    refs = refs_by_project.get(project, [])
    consumers = referenced_by.get(project, [])
    dp_list = data_by_project.get(project, [])
    layer_info = bl.get(project, {})

    md = f"# {project}\n\n"
    md += "## Metadata\n\n"
    md += f"| Property | Value |\n|----------|-------|\n"
    md += f"| Category | {pm['category']} |\n"
    if pm.get("repo"):
        md += f"| Repository | {pm['repo']} |\n"
    md += f"| Path | `{pm.get('globalPath') or pm.get('path', '')}` |\n"
    if layer_info.get("layer"):
        md += f"| Business Layer | {layer_info['layer']} (confidence: {layer_info.get('confidence', 0):.0%}) |\n"

    # Infer what this project does from data patterns
    if dp_list:
        types_used = sorted({f["type"] for f in dp_list})
        patterns_used = sorted({f["pattern"] for f in dp_list})
        md += f"\n## What This Project Does\n\n"
        md += f"Data access types: {', '.join(types_used)}\n\n"
        md += f"Patterns found: {', '.join(patterns_used[:10])}\n\n"

    # Dependencies out
    if refs:
        md += "## Dependencies (Outgoing)\n\n"
        for r in refs:
            cross = " *(cross-repo)*" if r.get("crossRepo") == "true" else ""
            md += f"- {r['references']}{cross}\n"
        md += "\n"

    # Consumers in
    if consumers:
        md += "## Consumers (Incoming)\n\n"
        for c in consumers[:30]:
            md += f"- {c}\n"
        if len(consumers) > 30:
            md += f"- *... +{len(consumers) - 30} more*\n"
        md += "\n"

    # NuGet packages
    external_pkgs = [d for d in deps if not d["package"].startswith(("StockSharp.", "Ecng."))]
    internal_pkgs = [d for d in deps if d["package"].startswith(("StockSharp.", "Ecng."))]
    if external_pkgs:
        md += "## External NuGet Packages\n\n"
        for d in external_pkgs:
            md += f"- {d['package']} ({d['version']})\n"
        md += "\n"
    if internal_pkgs:
        md += "## Internal NuGet Packages\n\n"
        for d in internal_pkgs:
            md += f"- {d['package']} ({d['version']})\n"
        md += "\n"

    # Data access patterns with file:line
    if dp_list:
        grouped: dict[str, list] = {}
        for dp in dp_list:
            grouped.setdefault(dp["pattern"], []).append(dp)
        md += "## Data Access Patterns\n\n"
        for pattern, findings in grouped.items():
            md += f"### {pattern}\n\n"
            for f in findings[:10]:
                md += f"- `{f['file']}:{f['line']}` — {f['context'][:80]}\n"
            if len(findings) > 10:
                md += f"- *... +{len(findings) - 10} more*\n"
            md += "\n"

    # Hotspot metrics
    if m:
        md += "## Hotspot Metrics\n\n"
        md += "| Metric | Value |\n|--------|-------|\n"
        md += f"| Fan-Out | {m.get('fan_out', 0)} |\n"
        md += f"| Fan-In | {m.get('fan_in', 0)} |\n"
        md += f"| NuGet Deps | {m.get('nuget_deps', 0)} |\n"
        md += f"| Data Patterns | {m.get('data_patterns', 0)} |\n"
        md += f"| Cross-Repo Refs | {m.get('cross_repo_refs', 0)} |\n"
        md += f"| **Hotspot Score** | **{m.get('hotspot_score', 0)}** |\n\n"

    # Code Quality Metrics (from refactoring triage)
    refactoring_by_name = {rp["project"]: rp for rp in refactoring_data.get("projects", [])}
    rp = refactoring_by_name.get(project)
    if rp:
        md += "## Code Quality Metrics\n\n"
        md += "| Metric | Value |\n|--------|-------|\n"
        md += f"| Refactoring Score | {rp.get('refactoring_value_score', 0)} |\n"
        md += f"| Smell Count | {rp.get('smell_count', 0)} |\n"
        md += f"| Has Tests | {'Yes' if rp.get('has_tests') else 'No'} |\n"
        top_smells = rp.get("top_smells", [])
        if top_smells:
            md += f"| Top Smells | {', '.join(top_smells[:5])} |\n"
        md += "\n"

        # Smell Locations (per-file details, capped at 30)
        rp_files = rp.get("files", [])
        smell_entries = []
        for rf in rp_files:
            for sm in rf.get("smells", []):
                smell_entries.append((rf.get("file", ""), sm))
                if len(smell_entries) >= 30:
                    break
            if len(smell_entries) >= 30:
                break
        if smell_entries:
            md += "### Smell Locations\n\n"
            for sf, sm in smell_entries:
                fname = os.path.basename(sf) if sf else "unknown"
                line = sm.get("line", "?")
                stype = sm.get("type", "unknown")
                ctx = (sm.get("context") or "")[:80]
                md += f"- `{fname}:{line}` — {stype}: {ctx}\n"
            total_smells_in_files = sum(len(rf.get("smells", [])) for rf in rp_files)
            if total_smells_in_files > 30:
                md += f"- *... +{total_smells_in_files - 30} more smell locations*\n"
            md += "\n"

    # UX Consistency Issues for this project
    project_ux_issues = [i for i in ux_inconsistencies.get("issues", []) if i.get("project") == project]
    if project_ux_issues:
        md += "## UX Consistency Issues\n\n"
        for iss in project_ux_issues[:20]:
            sev = iss.get("severity", "info")
            iss_type = iss.get("type", "")
            msg = iss.get("message", "")
            iss_file = iss.get("file", "")
            md += f"- [{sev}] {iss_type}: {msg}"
            if iss_file:
                md += f" — {iss_file}"
            md += "\n"
            if iss.get("availableProperties"):
                md += f"  - Available properties: {', '.join(iss['availableProperties'][:10])}\n"
        if len(project_ux_issues) > 20:
            md += f"- *... +{len(project_ux_issues) - 20} more issues*\n"
        md += "\n"

    # NuGet Health for this project
    nh_project_data = {}
    for fw_name, fw_projs in nuget_health.get("targetFrameworks", {}).items():
        if project in fw_projs:
            nh_project_data["targetFramework"] = fw_name
            break
    # Check legacy format
    for lp in nuget_health.get("legacyFormatProjects", []):
        if lp.get("project") == project:
            nh_project_data["nugetFormat"] = "packages.config (legacy)"
            break
    else:
        nh_project_data["nugetFormat"] = "PackageReference"
    # Check version conflicts involving this project
    project_conflicts = []
    for vc in nuget_health.get("versionConflicts", []):
        for ver, projs in vc.get("versions", {}).items():
            if project in projs:
                project_conflicts.append(f"{vc['package']} ({ver})")
                break
    if nh_project_data.get("targetFramework") or project_conflicts:
        md += "## NuGet Health\n\n"
        md += "| Property | Value |\n|----------|-------|\n"
        if nh_project_data.get("targetFramework"):
            md += f"| Target Framework | {nh_project_data['targetFramework']} |\n"
        md += f"| NuGet Format | {nh_project_data.get('nugetFormat', 'PackageReference')} |\n"
        if project_conflicts:
            md += f"\n**Version Conflicts:** {', '.join(project_conflicts)}\n"
        md += "\n"

    # Test Coverage for this project
    test_cov = test_data.get("coverage", {}).get(project)
    if test_cov:
        md += "## Test Coverage\n\n"
        md += "| Property | Value |\n|----------|-------|\n"
        md += f"| Test Project | {test_cov.get('testProject', '')} |\n"
        md += f"| Framework | {test_cov.get('testFramework', '')} |\n"
        md += f"| Test Methods | {test_cov.get('testMethodCount', 0)} |\n\n"
    elif project not in (tp["project"] for tp in test_data.get("testProjects", [])):
        # This is a non-test project with no test coverage
        if test_data.get("testProjects"):
            md += "## Test Coverage\n\n**No test project found covering this project.**\n\n"

    # Related projects: shared data nodes
    related = set()
    for dn in data_nodes:
        all_connected = set(dn.get("writers", []) + dn.get("readers", []) +
                           dn.get("exposers", []) + dn.get("consumers", []))
        if project in all_connected:
            related.update(all_connected - {project})

    # Related projects: 3+ shared NuGet packages
    my_pkgs = {d["package"] for d in deps}
    if len(my_pkgs) >= 3:
        for other_pm in project_meta:
            if other_pm["project"] == project:
                continue
            other_pkgs = {d["package"] for d in deps_by_project.get(other_pm["project"], [])}
            if len(my_pkgs & other_pkgs) >= 3:
                related.add(other_pm["project"])

    if related:
        md += "## Related Projects\n\n"
        for r in sorted(related)[:20]:
            md += f"- {r}\n"
        if len(related) > 20:
            md += f"- *... +{len(related) - 20} more*\n"
        md += "\n"

    md += f"\n---\n*Generated: {date.today().isoformat()}*\n"
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', project)
    Path(os.path.join(ai_dir, f"{safe_name}.md")).write_text(md, encoding="utf-8")


def _write_hotspots_report(ai_dir: str, metrics: list[dict]) -> None:
    """Write HOTSPOTS.md with ranked hotspots, reasons, and suggestions."""
    md = """# Hotspot Analysis Report

> Projects ranked by coupling complexity. Higher scores indicate projects where
> AI-assisted refactoring, testing, or documentation would have the most impact.

## Scoring Formula

`Score = Fan-Out×3 + Fan-In×2 + NuGet + Data Patterns + Cross-Repo×4`

## Ranked Hotspots

"""
    for i, m in enumerate(metrics):
        if m["hotspot_score"] == 0:
            continue
        md += f"### {i + 1}. {m['project']} (Score: {m['hotspot_score']})\n\n"
        md += f"- **Category:** {m['category']}\n"
        if m.get("layer"):
            md += f"- **Layer:** {m['layer']}\n"
        if m.get("repo"):
            md += f"- **Repo:** {m['repo']}\n"
        md += f"- Fan-Out: {m['fan_out']} | Fan-In: {m['fan_in']} | "
        md += f"NuGet: {m['nuget_deps']} | Data: {m['data_patterns']} | "
        md += f"Cross-Repo: {m['cross_repo_refs']}\n\n"

        # Why it's a hotspot
        reasons = []
        if m["fan_out"] >= 5:
            reasons.append(f"High fan-out ({m['fan_out']} outgoing refs) — tightly coupled to many projects")
        if m["fan_in"] >= 5:
            reasons.append(f"High fan-in ({m['fan_in']} consumers) — many projects depend on this")
        if m["cross_repo_refs"] > 0:
            reasons.append(f"Cross-repo coupling ({m['cross_repo_refs']} cross-repo refs) — changes ripple across repos")
        if m["data_patterns"] >= 3:
            reasons.append(f"Heavy data access ({m['data_patterns']} patterns, types: {', '.join(m.get('data_types', []))})")
        if m["nuget_deps"] >= 10:
            reasons.append(f"Many NuGet dependencies ({m['nuget_deps']}) — large dependency surface")
        if reasons:
            md += "**Why it's a hotspot:**\n"
            for r in reasons:
                md += f"- {r}\n"
            md += "\n"

        # Suggested focus
        suggestions = []
        if m["fan_out"] >= 8:
            suggestions.append("Consider splitting responsibilities — this project depends on too many others")
        if m["fan_in"] >= 10:
            suggestions.append("Extract stable interfaces — many consumers means changes here are risky")
        if m["cross_repo_refs"] >= 3:
            suggestions.append("Define clear API contracts for cross-repo boundaries")
        if m["data_patterns"] >= 5:
            suggestions.append("Add integration tests for data access patterns")
        if m["nuget_deps"] >= 15:
            suggestions.append("Audit NuGet dependencies for consolidation opportunities")
        if m["fan_out"] >= 3 and m["fan_in"] >= 3:
            suggestions.append("Good candidate for comprehensive unit test coverage")
        if suggestions:
            md += "**Suggested focus:**\n"
            for s in suggestions:
                md += f"- {s}\n"
            md += "\n"

        md += "---\n\n"

    # Category coupling summary
    cat_stats: dict[str, dict] = {}
    for m in metrics:
        cat = m["category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"count": 0, "total_score": 0, "total_fan_out": 0,
                              "total_fan_in": 0, "total_cross_repo": 0}
        cat_stats[cat]["count"] += 1
        cat_stats[cat]["total_score"] += m["hotspot_score"]
        cat_stats[cat]["total_fan_out"] += m["fan_out"]
        cat_stats[cat]["total_fan_in"] += m["fan_in"]
        cat_stats[cat]["total_cross_repo"] += m["cross_repo_refs"]

    md += "## Category Coupling Summary\n\n"
    md += "| Category | Projects | Avg Score | Total Fan-Out | Total Fan-In | Cross-Repo |\n"
    md += "|----------|----------|-----------|---------------|--------------|------------|\n"
    for cat, s in sorted(cat_stats.items(), key=lambda x: -x[1]["total_score"]):
        avg = s["total_score"] / s["count"] if s["count"] else 0
        md += (f"| {cat} | {s['count']} | {avg:.1f} | {s['total_fan_out']} | "
               f"{s['total_fan_in']} | {s['total_cross_repo']} |\n")

    md += f"\n---\n*Generated: {date.today().isoformat()}*\n"
    Path(os.path.join(ai_dir, "HOTSPOTS.md")).write_text(md, encoding="utf-8")


def _write_ai_context_index(ai_dir: str) -> None:
    """Write an index.html in the ai-context directory listing all .md files."""
    md_files = sorted(
        f for f in os.listdir(ai_dir) if f.endswith(".md")
    )
    overview_files = [f for f in md_files if f == "CODEBASE_OVERVIEW.md"]
    hotspot_files = [f for f in md_files if f == "HOTSPOTS.md"]
    project_files = [f for f in md_files if f not in ("CODEBASE_OVERVIEW.md", "HOTSPOTS.md")]

    rows = ""
    for f in overview_files + hotspot_files:
        rows += f'    <li style="margin:0.3rem 0;"><a href="{f}" style="color:#005587;font-weight:600;">{f}</a></li>\n'
    if project_files:
        rows += '    <li style="margin:0.8rem 0 0.3rem;font-weight:600;color:#022D5E;list-style:none;">Per-Project Context Files</li>\n'
        for f in project_files:
            label = f.replace(".md", "")
            rows += f'    <li style="margin:0.2rem 0;"><a href="{f}" style="color:#005587;">{label}</a></li>\n'

    title = repos[0] if len(repos) == 1 else f"{len(repos)} Repositories"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>AI Context — {_esc_html(title)}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 700px; margin: 2rem auto; padding: 0 1rem; color: #000; }}
  h1 {{ color: #022D5E; font-size: 1.4rem; border-bottom: 2px solid #005587; padding-bottom: 0.5rem; }}
  ul {{ padding-left: 1.2rem; }}
  a {{ text-decoration: none; }} a:hover {{ text-decoration: underline; }}
  .count {{ color: #53565A; font-size: 0.85rem; }}
</style></head>
<body>
  <h1>AI Context Files</h1>
  <p class="count">{len(md_files)} files generated for {_esc_html(title)}</p>
  <ul>
{rows}  </ul>
  <p style="margin-top:2rem;color:#53565A;font-size:0.78rem;font-style:italic;">Generated by Dependency Mapper — {date.today().isoformat()}</p>
</body></html>"""
    Path(os.path.join(ai_dir, "index.html")).write_text(html, encoding="utf-8")


def generate_ai_context() -> int:
    """Generate AI-ready markdown context files. Returns count of files written."""
    ai_dir = os.path.join(DOCS_DIR, "ai-context")
    os.makedirs(ai_dir, exist_ok=True)

    metrics = compute_hotspot_metrics()
    metrics_by_name = {m["project"]: m for m in metrics}
    bl = flow_paths_data.get("businessLayers", {})
    data_nodes = data_flow.get("dataNodes", [])

    _write_codebase_overview(ai_dir, metrics)
    _write_hotspots_report(ai_dir, metrics)

    for pm in project_meta:
        _write_project_context(ai_dir, pm, metrics_by_name, bl, data_nodes)

    _write_ai_context_index(ai_dir)

    return len(project_meta) + 2  # project files + overview + hotspots


# ─── Main ───────────────────────────────────────────────────────────

def main():
    print("=== Generating Documentation (Python) ===\n")

    # Index
    Path(os.path.join(DOCS_DIR, "index.md")).write_text(generate_index(), encoding="utf-8")
    print("  Wrote index.md")

    # Per-project pages
    page_count = 0
    for pm in project_meta:
        page = generate_project_page(pm)

        if is_multi_repo:
            out_dir = os.path.join(DOCS_DIR, "repos", pm.get("repo", "unknown"))
        else:
            out_dir = os.path.join(DOCS_DIR, get_dir_for_category(pm["category"]))

        os.makedirs(out_dir, exist_ok=True)
        Path(os.path.join(out_dir, f"{pm['project']}.md")).write_text(page, encoding="utf-8")
        page_count += 1

    print(f"  Wrote {page_count} project pages")

    # Data source registry
    Path(os.path.join(DOCS_DIR, "data-sources", "registry.md")).write_text(
        generate_data_source_registry(), encoding="utf-8"
    )
    print("  Wrote data-sources/registry.md")

    # Copy diagrams
    diagrams_src = os.path.join(OUT_DIR, "diagrams")
    diagrams_dst = os.path.join(DOCS_DIR, "diagrams")
    if os.path.isdir(diagrams_src):
        for f in os.listdir(diagrams_src):
            shutil.copy2(os.path.join(diagrams_src, f), os.path.join(diagrams_dst, f))
        print("  Copied diagrams/")

    # Viewer HTML
    Path(os.path.join(OUT_DIR, "viewer.html")).write_text(generate_viewer_html(), encoding="utf-8")
    print("  Wrote viewer.html")

    # AI context export
    ai_count = generate_ai_context()
    print(f"  Wrote {ai_count} AI context files to docs/ai-context/")

    print(f"\n=== Documentation complete ({page_count} pages) ===\n")


if __name__ == "__main__":
    main()
