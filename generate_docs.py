#!/usr/bin/env python3
"""
Dependency Mapper — Documentation Generator (Python)

Reads analysis outputs and generates structured markdown documentation.
Supports single-repo and multi-repo modes.
"""

import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

OUT_DIR = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "output")
DOCS_DIR = os.path.join(OUT_DIR, "docs")

# Load analysis data
graph = json.loads(Path(os.path.join(OUT_DIR, "graph.json")).read_text(encoding="utf-8"))
project_meta = json.loads(Path(os.path.join(OUT_DIR, "project-meta.json")).read_text(encoding="utf-8"))
data_findings = json.loads(Path(os.path.join(OUT_DIR, "data-sources.json")).read_text(encoding="utf-8"))
configs = json.loads(Path(os.path.join(OUT_DIR, "configs.json")).read_text(encoding="utf-8"))


# ─── Parse CSVs ──────────────────────────────────────────────────────

def read_csv(filepath: str) -> list[dict]:
    """Read a CSV file, handling quoted values with commas."""
    content = Path(filepath).read_text(encoding="utf-8")
    lines = content.strip().split("\n")
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
    parts = f["file"].replace("\\", "/").split("/")
    proj_dir = parts[1 if is_multi_repo else 0] if len(parts) > (1 if is_multi_repo else 0) else parts[0]
    data_by_project.setdefault(proj_dir, []).append(f)


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
    landscape_path = os.path.join(OUT_DIR, "diagrams", "landscape.mmd")
    if os.path.isfile(landscape_path):
        content = Path(landscape_path).read_text(encoding="utf-8")
        md += f"\n## Full Landscape\n\n```mermaid\n{content}\n```\n"

    core_path = os.path.join(OUT_DIR, "diagrams", "core-libraries.mmd")
    if os.path.isfile(core_path):
        content = Path(core_path).read_text(encoding="utf-8")
        md += f"\n## Core Library Hierarchy\n\n```mermaid\n{content}\n```\n"

    data_infra_path = os.path.join(OUT_DIR, "diagrams", "data-infrastructure.mmd")
    if os.path.isfile(data_infra_path):
        content = Path(data_infra_path).read_text(encoding="utf-8")
        md += f"\n## Data Infrastructure\n\n```mermaid\n{content}\n```\n"

    nuget_path = os.path.join(OUT_DIR, "diagrams", "nuget-groups.mmd")
    if os.path.isfile(nuget_path):
        content = Path(nuget_path).read_text(encoding="utf-8")
        md += f"\n## NuGet Package Groups\n\n```mermaid\n{content}\n```\n"

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


def generate_viewer_html() -> str:
    summary = graph["summary"]
    categories = summary["categories"]
    repo_count = summary.get("totalRepos", 1)
    repo_list = sorted({p["repo"] for p in project_meta if p.get("repo")})
    title = ", ".join(repo_list) if repo_list else "Project"

    # ── Collect two-level diagram tabs: overview + per-category ──
    diagrams_dir = os.path.join(OUT_DIR, "diagrams")
    diagram_tabs: list[dict] = []

    # Overview tab (category-level diagram)
    overview_path = os.path.join(diagrams_dir, "overview.mmd")
    if os.path.isfile(overview_path):
        content = Path(overview_path).read_text(encoding="utf-8")
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
        mmd_path = os.path.join(diagrams_dir, f"category-{cat_key}.mmd")
        if os.path.isfile(mmd_path):
            content = Path(mmd_path).read_text(encoding="utf-8")
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

    # ── Aggregate data sources by pattern ──
    pattern_summary: dict[str, dict] = {}
    for f in data_findings:
        p = f["pattern"]
        if p not in pattern_summary:
            pattern_summary[p] = {"type": f["type"], "count": 0, "projects": set()}
        pattern_summary[p]["count"] += 1
        parts = f["file"].replace("\\", "/").split("/")
        proj_dir = parts[1 if is_multi_repo else 0] if len(parts) > (1 if is_multi_repo else 0) else parts[0]
        pattern_summary[p]["projects"].add(proj_dir)

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
        (summary["totalProjects"], "Projects"),
        (summary["totalNuGetPackages"], "NuGet Packages"),
        (summary["totalProjectRefs"], "Project References"),
        (summary["totalDataFindings"], "Data Patterns"),
        (summary["totalConfigFiles"], "Config Files"),
    ]
    if repo_count > 1:
        stats_items.append((repo_count, f"Repos ({', '.join(repo_list)})"))

    stats_html = "\n".join(
        f'    <div class="stat"><span class="stat-value">{count}</span> {label}</div>'
        for count, label in stats_items
    )

    # Tab buttons
    all_tab_ids: list[tuple[str, str]] = []
    for dt in diagram_tabs:
        all_tab_ids.append((dt["id"], dt["label"]))
    if pattern_summary:
        all_tab_ids.append(("datasources", "Data Sources"))
    if conn_strings:
        all_tab_ids.append(("connstrings", "Connection Strings"))
    all_tab_ids.append(("allprojects", "All Projects"))

    tab_buttons = "\n".join(
        f'  <button class="tab-btn{" active" if i == 0 else ""}" data-tab="{tid}">{label}</button>'
        for i, (tid, label) in enumerate(all_tab_ids)
    )

    # Diagram panels
    diagram_panels = ""
    for i, dt in enumerate(diagram_tabs):
        active = " active" if i == 0 else ""
        warning_html = ""
        if dt.get("warning"):
            warning_html = f'\n      <div class="edge-filter-warning">{_esc_html(dt["warning"])}</div>'
        diagram_panels += f"""
  <section class="tab-panel{active}" id="panel-{dt['id']}">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> {dt['title']}
        <span class="zoom-controls">
          <button class="zoom-btn" onclick="zoomDiagram('mermaid-{dt['id']}', -0.2)" title="Zoom out">&#8722;</button>
          <button class="zoom-btn" onclick="zoomDiagram('mermaid-{dt['id']}', 0)" title="Reset zoom">Reset</button>
          <button class="zoom-btn" onclick="zoomDiagram('mermaid-{dt['id']}', 0.2)" title="Zoom in">&#43;</button>
        </span>
      </div>{warning_html}
      <div class="mermaid-wrap" id="mermaid-{dt['id']}">
        <span class="loading">Loading diagram...</span>
        <pre class="mermaid" style="display:none">
{_esc_html(dt['mermaid'])}
        </pre>
      </div>
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
        <table>
          <thead>
            <tr><th>Pattern</th><th>Type</th><th>Occurrences</th><th>Key Projects</th></tr>
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
            rows += f"""            <tr>
              <td class="mono">{_esc_html(cs['file'])}</td>
              <td>{_esc_html(cs['repo'])}</td>
              <td>{_esc_html(cs['name'])}</td>
              <td class="mono">{_esc_html(cs['value'])}</td>
            </tr>
"""
        connstrings_panel = f"""
  <section class="tab-panel" id="panel-connstrings">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> Connection Strings</div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Config File</th><th>Repo</th><th>Connection Name</th><th>Value</th></tr>
          </thead>
          <tbody>
{rows}          </tbody>
        </table>
      </div>
    </div>
  </section>
"""

    # Category distribution panel (pie chart via Mermaid)
    cat_chart_mermaid = "pie title Project Categories\n"
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        cat_chart_mermaid += f'    "{cat}" : {count}\n'

    # All projects panel
    all_projects_panel = f"""
  <section class="tab-panel" id="panel-allprojects">
    <div class="card">
      <div class="card-title"><span class="icon">&#9670;</span> All Projects</div>
      <div class="table-wrap">
        <table id="projectsTable">
          <thead>
            <tr>
              <th>Project</th>
              <th>Repo</th>
              <th>Category</th>
              <th>Project Refs</th>
              <th>NuGet Deps</th>
              <th>Path</th>
            </tr>
          </thead>
          <tbody id="projectsBody">
            <tr><td colspan="6" style="text-align:center;color:#64748b;padding:2rem;">Loading project data...</td></tr>
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
    background: #0f172a; color: #e2e8f0; line-height: 1.6; min-height: 100vh;
  }}
  a {{ color: #3b82f6; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .header {{
    background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
    border-bottom: 1px solid #334155; padding: 1.5rem 2rem 1rem;
  }}
  .header-top {{
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;
  }}
  .header h1 {{ font-size: 1.6rem; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; }}
  .header h1 span {{ color: #3b82f6; }}
  .search-box {{ position: relative; width: 280px; }}
  .search-box input {{
    width: 100%; padding: 0.5rem 0.75rem 0.5rem 2.2rem; border-radius: 6px;
    border: 1px solid #334155; background: #1e293b; color: #e2e8f0;
    font-size: 0.875rem; outline: none; transition: border-color .2s;
  }}
  .search-box input::placeholder {{ color: #64748b; }}
  .search-box input:focus {{ border-color: #3b82f6; }}
  .search-box .search-icon {{
    position: absolute; left: 0.65rem; top: 50%; transform: translateY(-50%);
    color: #64748b; font-size: 0.85rem; pointer-events: none;
  }}
  .stats-row {{ display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; margin-bottom: 0.75rem; }}
  .stat {{ display: flex; align-items: center; gap: 0.4rem; font-size: 0.8rem; color: #94a3b8; }}
  .stat-value {{ font-weight: 700; font-size: 1rem; color: #3b82f6; }}
  .tabs {{
    display: flex; flex-wrap: wrap; gap: 0.25rem; padding: 0 2rem;
    background: #0f172a; border-bottom: 1px solid #334155;
  }}
  .tab-btn {{
    padding: 0.6rem 1rem; background: transparent; border: none; color: #94a3b8;
    font-size: 0.82rem; font-weight: 500; cursor: pointer;
    border-bottom: 2px solid transparent; transition: color .2s, border-color .2s; white-space: nowrap;
  }}
  .tab-btn:hover {{ color: #e2e8f0; }}
  .tab-btn.active {{ color: #3b82f6; border-bottom-color: #3b82f6; }}
  .content {{ padding: 1.5rem 2rem 3rem; }}
  .tab-panel {{ display: none; }}
  .tab-panel.active {{ display: block; }}
  .card {{
    background: #1e293b; border: 1px solid #334155; border-radius: 10px;
    padding: 1.25rem 1.5rem; margin-bottom: 1.25rem;
  }}
  .card-title {{
    font-size: 1.05rem; font-weight: 600; color: #f1f5f9; margin-bottom: 0.75rem;
    display: flex; align-items: center; gap: 0.5rem;
  }}
  .card-title .icon {{ color: #3b82f6; }}
  .card-title {{ justify-content: flex-start; }}
  .zoom-controls {{ margin-left: auto; display: flex; gap: 0.25rem; }}
  .zoom-btn {{
    background: #0f172a; border: 1px solid #334155; color: #94a3b8; border-radius: 4px;
    padding: 0.15rem 0.5rem; font-size: 0.75rem; cursor: pointer; line-height: 1.2;
  }}
  .zoom-btn:hover {{ color: #e2e8f0; border-color: #3b82f6; }}
  .edge-filter-warning {{
    background: #fef3c7; color: #92400e; border: 1px solid #f59e0b; border-radius: 6px;
    padding: 0.5rem 0.75rem; margin: 0.5rem 0; font-size: 0.85rem;
  }}
  .mermaid-wrap {{
    background: #f8fafc; border-radius: 8px; padding: 1rem; overflow: auto;
    min-height: 120px; max-height: 80vh;
  }}
  .mermaid-wrap .loading {{ color: #64748b; font-size: 0.9rem; text-align: center; }}
  .mermaid-wrap svg {{ max-width: none !important; height: auto; transform-origin: top left; }}
  .flowchart-link {{ transition: stroke 0.15s, stroke-width 0.15s, opacity 0.15s; }}
  .edge-hover-target {{ stroke: transparent; stroke-width: 15px; fill: none; cursor: pointer; pointer-events: stroke; }}
  .flowchart-link.edge-highlight {{ stroke: #3b82f6 !important; stroke-width: 3px !important; }}
  .edgePaths:has(.flowchart-link:hover) .flowchart-link:not(:hover) {{ opacity: 0.15; }}
  .edge-tooltip {{
    position: fixed; background: #1e293b; color: #e2e8f0; border: 1px solid #3b82f6;
    border-radius: 6px; padding: 0.4rem 0.7rem; font-size: 0.8rem; pointer-events: none;
    z-index: 1000; white-space: nowrap; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    display: none;
  }}
  .edge-tooltip .edge-from {{ color: #60a5fa; }}
  .edge-tooltip .edge-to {{ color: #34d399; }}
  .edge-tooltip .edge-arrow {{ color: #94a3b8; margin: 0 0.3rem; }}
  .edge-detail-panel {{
    position: fixed; right: 1rem; top: 50%; transform: translateY(-50%);
    background: #1e293b; border: 1px solid #334155; border-radius: 10px;
    padding: 1.2rem; width: 380px; max-height: 70vh; overflow-y: auto;
    z-index: 999; box-shadow: 0 8px 32px rgba(0,0,0,0.5); display: none;
    font-size: 0.85rem; color: #e2e8f0;
  }}
  .edge-detail-panel .detail-header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 0.8rem; padding-bottom: 0.6rem; border-bottom: 1px solid #334155;
  }}
  .edge-detail-panel .detail-header h3 {{ font-size: 0.95rem; font-weight: 600; margin: 0; }}
  .edge-detail-panel .detail-close {{
    background: none; border: 1px solid #475569; color: #94a3b8; border-radius: 4px;
    cursor: pointer; padding: 0.1rem 0.5rem; font-size: 0.8rem;
  }}
  .edge-detail-panel .detail-close:hover {{ color: #e2e8f0; border-color: #64748b; }}
  .edge-detail-panel .detail-section {{ margin-bottom: 0.8rem; }}
  .edge-detail-panel .detail-section h4 {{
    font-size: 0.75rem; text-transform: uppercase; color: #64748b; letter-spacing: 0.04em;
    margin-bottom: 0.3rem;
  }}
  .edge-detail-panel .detail-flow {{
    display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; margin-bottom: 0.3rem;
  }}
  .edge-detail-panel .detail-flow .from {{ color: #60a5fa; font-weight: 600; }}
  .edge-detail-panel .detail-flow .to {{ color: #34d399; font-weight: 600; }}
  .edge-detail-panel .detail-flow .arrow {{ color: #94a3b8; }}
  .edge-detail-panel .detail-list {{ list-style: none; padding: 0; }}
  .edge-detail-panel .detail-list li {{
    padding: 0.25rem 0; border-bottom: 1px solid #1e293b; color: #cbd5e1; font-size: 0.8rem;
  }}
  .edge-detail-panel .detail-list li:last-child {{ border-bottom: none; }}
  .edge-detail-panel .detail-empty {{ color: #64748b; font-style: italic; font-size: 0.8rem; }}
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
  thead th {{
    background: #1a2438; color: #94a3b8; font-weight: 600; text-transform: uppercase;
    font-size: 0.72rem; letter-spacing: 0.04em; padding: 0.6rem 0.75rem; text-align: left;
    border-bottom: 1px solid #334155; position: sticky; top: 0; z-index: 1;
  }}
  tbody td {{ padding: 0.55rem 0.75rem; border-bottom: 1px solid #1e293b; color: #cbd5e1; }}
  tbody tr:hover {{ background: rgba(59,130,246,0.06); }}
  .tag {{
    display: inline-block; padding: 0.15rem 0.55rem; border-radius: 4px;
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em;
  }}
  .tag-webapp      {{ background: rgba(26,188,156,.15); color: #1ABC9C; }}
  .tag-library     {{ background: rgba(74,144,217,.15); color: #4A90D9; }}
  .tag-application {{ background: rgba(231,76,60,.15);  color: #E74C3C; }}
  .tag-service     {{ background: rgba(52,152,219,.15); color: #3498DB; }}
  .tag-tool        {{ background: rgba(243,156,18,.15); color: #F39C12; }}
  .tag-test        {{ background: rgba(155,89,182,.15); color: #9B59B6; }}
  .tag-connector   {{ background: rgba(230,126,34,.15); color: #E67E22; }}
  .tag-desktopapp  {{ background: rgba(233,30,99,.15);  color: #E91E63; }}
  .tag-db       {{ background: rgba(74,144,217,.15);  color: #4A90D9; }}
  .tag-messaging{{ background: rgba(231,76,60,.15);   color: #E74C3C; }}
  .tag-api      {{ background: rgba(52,152,219,.15);  color: #3498DB; }}
  .tag-cache    {{ background: rgba(243,156,18,.15);  color: #F39C12; }}
  .tag-config   {{ background: rgba(155,89,182,.15);  color: #9B59B6; }}
  .mono {{ font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: 0.78rem; color: #64748b; }}
  .footer {{
    text-align: center; padding: 1.5rem 2rem; color: #475569;
    font-size: 0.78rem; font-style: italic; border-top: 1px solid #334155;
  }}
  @media (max-width: 768px) {{
    .header {{ padding: 1rem; }}
    .content {{ padding: 1rem; }}
    .tabs {{ padding: 0 1rem; }}
    .search-box {{ width: 100%; }}
  }}
</style>
</head>
<body>
<div class="edge-tooltip" id="edgeTooltip"></div>
<div class="edge-detail-panel" id="edgeDetailPanel"></div>

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
  </div>
</header>

<nav class="tabs" id="tabNav">
{tab_buttons}
</nav>

<main class="content">
{diagram_panels}
{datasources_panel}
{connstrings_panel}
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
      if (ep) showEdgeDetail(ep.from, ep.to);
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

function showEdgeDetail(fromName, toName) {{
  var panel = document.getElementById('edgeDetailPanel');
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
    html += '<div style="font-size:0.75rem;color:#94a3b8;margin-top:0.2rem;">';
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
      var cross = r.crossRepo === 'True' ? ' <span style="color:#f59e0b;">(cross-repo)</span>' : '';
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
      html += '<li>' + escHtmlGlobal(d.package) + ' <span style="color:#94a3b8">' + escHtmlGlobal(d.version) + '</span></li>';
    }});
    if (sharedPkgs.length > 15) html += '<li style="color:#64748b">... and ' + (sharedPkgs.length - 15) + ' more</li>';
    html += '</ul>';
  }} else {{
    html += '<div class="detail-empty">No shared NuGet packages</div>';
  }}
  html += '</div>';

  // Data patterns
  var totalFromPatterns = fromDataPatterns.length;
  var totalToPatterns = toDataPatterns.length;
  html += '<div class="detail-section"><h4>Data Patterns</h4>';
  html += '<div style="font-size:0.78rem;color:#cbd5e1;margin-bottom:0.3rem;">'
    + '<span class="from" style="color:#60a5fa">' + escHtmlGlobal(fromName) + '</span>: ' + totalFromPatterns + ' patterns, '
    + '<span class="to" style="color:#34d399">' + escHtmlGlobal(toName) + '</span>: ' + totalToPatterns + ' patterns</div>';
  var sharedKeys = Object.keys(sharedPatternNames);
  if (sharedKeys.length > 0) {{
    html += '<ul class="detail-list">';
    sharedKeys.forEach(function (p) {{
      html += '<li>' + escHtmlGlobal(p) + ' <span style="color:#94a3b8">(' + sharedPatternNames[p] + ' matches in target)</span></li>';
    }});
    html += '</ul>';
  }} else {{
    html += '<div class="detail-empty">No shared data patterns</div>';
  }}
  html += '</div>';

  panel.innerHTML = html;
  panel.style.display = 'block';
  var closeBtn = document.getElementById('detailCloseBtn');
  if (closeBtn) closeBtn.addEventListener('click', function () {{ panel.style.display = 'none'; }});
}}

function escHtmlGlobal(s) {{
  var d = document.createElement('div');
  d.textContent = s || '';
  return d.innerHTML;
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

  function escHtml(s) {{
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
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

  // Global project data for edge detail lookups
  window._projData = {{ meta: [], refs: [], deps: [], dataSources: [] }};

  // Load All Projects data
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
    meta.forEach(function (p) {{
      var tr = document.createElement('tr');
      tr.setAttribute('data-search', (p.project + ' ' + (p.repo||'') + ' ' + p.category + ' ' + (p.globalPath||p.path||'')).toLowerCase());
      tr.innerHTML =
        '<td><strong>' + escHtml(p.project) + '</strong></td>' +
        '<td>' + escHtml(p.repo || '') + '</td>' +
        '<td>' + tagHTML(p.category) + '</td>' +
        '<td style="text-align:center">' + (refCounts[p.project] || 0) + '</td>' +
        '<td style="text-align:center">' + (depCounts[p.project] || 0) + '</td>' +
        '<td class="mono">' + escHtml(p.globalPath || p.path || '') + '</td>';
      tbody.appendChild(tr);
    }});
  }}).catch(function (err) {{
    console.error('Failed to load project data:', err);
    var tbody = document.getElementById('projectsBody');
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#ef4444;padding:2rem;">Failed to load project data.</td></tr>';
  }});

  // Search
  var searchInput = document.getElementById('searchInput');
  searchInput.addEventListener('input', function () {{
    var query = searchInput.value.trim().toLowerCase();
    if (query.length > 0) activateTab('allprojects');
    var rows = document.querySelectorAll('#projectsBody tr[data-search]');
    rows.forEach(function (row) {{
      var text = row.getAttribute('data-search') || '';
      row.style.display = (!query || text.indexOf(query) !== -1) ? '' : 'none';
    }});
  }});
}})();
</script>
</body>
</html>"""

    return html


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

    print(f"\n=== Documentation complete ({page_count} pages) ===\n")


if __name__ == "__main__":
    main()
