#!/usr/bin/env python3
"""
Dependency Mapper — Visualization Generator (Python)

Reads output/graph.json and generates Mermaid + GraphViz diagrams.
Supports single-repo and multi-repo modes.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

OUT_DIR = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "output")
DIAGRAMS_DIR = os.path.join(OUT_DIR, "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

graph = json.loads(Path(os.path.join(OUT_DIR, "graph.json")).read_text(encoding="utf-8"))

# ─── Helpers ────────────────────────────────────────────────────────

ALL_TYPES = {
    "library", "connector", "sample", "application", "test", "tool",
    "localization", "webapp", "service", "desktopapp",
}

project_nodes = [n for n in graph["nodes"] if n.get("type") in ALL_TYPES]

# Deduplicate project ref edges
unique_project_refs: dict[str, dict] = {}
for e in graph["edges"]:
    if e["type"] in ("project-reference", "cross-repo-reference"):
        key = f"{e['from']}->{e['to']}"
        unique_project_refs[key] = e
deduped_refs = list(unique_project_refs.values())

# Determine if multi-repo
repos = sorted({n.get("repo", "") for n in project_nodes if n.get("repo")})
is_multi_repo = len(repos) > 1


def sanitize_id(id_str: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", id_str)


def short_name(node: dict) -> str:
    return node.get("project") or node["id"].split("/")[-1]


# ─── Mermaid: Full Landscape ────────────────────────────────────────

def generate_landscape_mermaid() -> str:
    lines = ["graph LR"]
    skip_types = {"localization", "sample"}

    if is_multi_repo:
        for repo in repos:
            repo_nodes = [n for n in project_nodes if n.get("repo") == repo and n["type"] not in skip_types]
            if not repo_nodes:
                continue
            lines.append(f'    subgraph {sanitize_id(repo)}["{repo}"]')

            categories: dict[str, list] = {}
            for n in repo_nodes:
                categories.setdefault(n["type"], []).append(n)

            for cat, nodes in categories.items():
                lines.append(f'        subgraph {sanitize_id(repo + "_" + cat)}["{cat}"]')
                for n in nodes:
                    lines.append(f'            {sanitize_id(n["id"])}["{short_name(n)}"]')
                lines.append("        end")
            lines.append("    end")
    else:
        categories: dict[str, list] = {}
        for n in project_nodes:
            if n["type"] in skip_types:
                continue
            categories.setdefault(n["type"], []).append(n)

        for cat, nodes in categories.items():
            label = cat[0].upper() + cat[1:] + "s"
            lines.append(f"    subgraph {label}")
            for n in nodes:
                lines.append(f'        {sanitize_id(n["id"])}["{short_name(n)}"]')
            lines.append("    end")

    # Edges
    node_ids = {n["id"] for n in project_nodes if n["type"] not in skip_types}
    for e in deduped_refs:
        if e["from"] in node_ids and e["to"] in node_ids:
            style = " -.->" if e["type"] == "cross-repo-reference" else " -->"
            lines.append(f"    {sanitize_id(e['from'])}{style} {sanitize_id(e['to'])}")

    return "\n".join(lines)


# ─── Mermaid: Core libraries ────────────────────────────────────────

def generate_core_library_mermaid() -> str:
    core_nodes = [n for n in project_nodes if n["type"] == "library"]
    core_ids = {n["id"] for n in core_nodes}

    lines = ["graph TD"]

    if is_multi_repo:
        for repo in repos:
            repo_nodes = [n for n in core_nodes if n.get("repo") == repo]
            if not repo_nodes:
                continue
            lines.append(f'    subgraph {sanitize_id(repo)}["{repo}"]')
            for n in repo_nodes:
                lines.append(f'        {sanitize_id(n["id"])}["{short_name(n)}"]')
            lines.append("    end")
    else:
        for n in core_nodes:
            lines.append(f'    {sanitize_id(n["id"])}["{short_name(n)}"]')

    for e in deduped_refs:
        if e["from"] in core_ids and e["to"] in core_ids:
            style = " -.->" if e["type"] == "cross-repo-reference" else " -->"
            lines.append(f"    {sanitize_id(e['from'])}{style} {sanitize_id(e['to'])}")

    return "\n".join(lines)


# ─── Mermaid: Data infrastructure ───────────────────────────────────

def generate_data_infra_mermaid() -> str:
    service_types = {"webapp", "service", "application", "desktopapp"}
    service_nodes = [n for n in project_nodes if n["type"] in service_types]
    db_nodes = [
        n for n in graph["nodes"]
        if n.get("type") == "datasource" and n.get("subtype") in ("database", "messaging", "cache")
    ]

    lines = ["graph LR"]

    if is_multi_repo:
        for repo in repos:
            rn = [n for n in service_nodes if n.get("repo") == repo]
            if not rn:
                continue
            lines.append(f'    subgraph {sanitize_id(repo)}["{repo}"]')
            for n in rn:
                lines.append(f'        {sanitize_id(n["id"])}["{short_name(n)}"]')
            lines.append("    end")
    else:
        lines.append("    subgraph Applications")
        for n in service_nodes:
            lines.append(f'        {sanitize_id(n["id"])}["{short_name(n)}"]')
        lines.append("    end")

    if db_nodes:
        lines.append("    subgraph DataSources")
        for n in db_nodes:
            lines.append(f'        {sanitize_id(n["id"])}[("{n["pattern"]}")]')
        lines.append("    end")

    return "\n".join(lines)


# ─── Mermaid: NuGet package groups ──────────────────────────────────

def generate_nuget_mermaid() -> str:
    nuget_nodes = [n for n in graph["nodes"] if n.get("type") == "nuget-package"]

    nuget_groups: dict[str, list] = {}
    for n in nuget_nodes:
        name = n["id"].replace("nuget:", "")
        prefix = name.split(".")[0]
        nuget_groups.setdefault(prefix, []).append(n)

    lines = ["graph LR"]

    notable = sorted(nuget_groups.items(), key=lambda x: -len(x[1]))[:15]
    for prefix, pkgs in notable:
        lines.append(f'    subgraph {sanitize_id(prefix)}["{prefix}"]')
        for pkg in pkgs[:8]:
            short_pkg = pkg["id"].replace("nuget:", "")
            versions = ", ".join(pkg.get("versions", []))
            lines.append(f'        {sanitize_id(pkg["id"])}["{short_pkg}<br/>{versions}"]')
        if len(pkgs) > 8:
            lines.append(f'        {sanitize_id(prefix + "_more")}["... +{len(pkgs) - 8} more"]')
        lines.append("    end")

    return "\n".join(lines)


# ─── GraphViz DOT: Full landscape ───────────────────────────────────

def generate_landscape_dot() -> str:
    lines = [
        "digraph dependencies {",
        "    rankdir=LR;",
        '    node [shape=box, style=filled, fontname="Helvetica"];',
        '    edge [color="#666666"];',
        "",
    ]

    skip_types = {"localization", "sample"}
    colors = {
        "library": "#4A90D9", "connector": "#E67E22", "sample": "#2ECC71",
        "application": "#E74C3C", "test": "#9B59B6", "tool": "#F39C12",
        "webapp": "#1ABC9C", "service": "#3498DB", "desktopapp": "#E91E63",
    }

    cluster_idx = 0

    if is_multi_repo:
        for repo in repos:
            lines.append(f"    subgraph cluster_{cluster_idx} {{")
            cluster_idx += 1
            lines.append(f'        label="{repo}";')
            lines.append('        style=filled; color="#DDDDDD";')

            repo_nodes = [n for n in project_nodes if n.get("repo") == repo and n["type"] not in skip_types]
            categories: dict[str, list] = {}
            for n in repo_nodes:
                categories.setdefault(n["type"], []).append(n)

            for cat, nodes in categories.items():
                color = colors.get(cat, "#95A5A6")
                lines.append(f"        subgraph cluster_{cluster_idx} {{")
                cluster_idx += 1
                lines.append(f'            label="{cat}";')
                lines.append('            style=filled; color="#EEEEEE";')
                for n in nodes:
                    lines.append(f'            {sanitize_id(n["id"])} [label="{short_name(n)}", fillcolor="{color}", fontcolor="white"];')
                lines.append("        }")
            lines.append("    }")
    else:
        categories: dict[str, list] = {}
        for n in project_nodes:
            if n["type"] in skip_types:
                continue
            categories.setdefault(n["type"], []).append(n)

        for cat, nodes in categories.items():
            color = colors.get(cat, "#95A5A6")
            lines.append(f"    subgraph cluster_{cluster_idx} {{")
            cluster_idx += 1
            lines.append(f'        label="{cat}s"; style=filled; color="#EEEEEE";')
            for n in nodes:
                lines.append(f'        {sanitize_id(n["id"])} [label="{short_name(n)}", fillcolor="{color}", fontcolor="white"];')
            lines.append("    }")

    node_ids = {n["id"] for n in project_nodes if n["type"] not in skip_types}
    for e in deduped_refs:
        if e["from"] in node_ids and e["to"] in node_ids:
            style = ' [style=dashed, color="red"]' if e["type"] == "cross-repo-reference" else ""
            lines.append(f"    {sanitize_id(e['from'])} -> {sanitize_id(e['to'])}{style};")

    lines.append("}")
    return "\n".join(lines)


# ─── Write all outputs ──────────────────────────────────────────────

def main():
    print("=== Generating Visualizations (Python) ===\n")

    mermaid_files = {
        "landscape.mmd": generate_landscape_mermaid(),
        "core-libraries.mmd": generate_core_library_mermaid(),
        "data-infrastructure.mmd": generate_data_infra_mermaid(),
        "nuget-groups.mmd": generate_nuget_mermaid(),
    }

    for filename, content in mermaid_files.items():
        Path(os.path.join(DIAGRAMS_DIR, filename)).write_text(content, encoding="utf-8")
        print(f"  Wrote {filename}")

    dot_files = {
        "landscape.dot": generate_landscape_dot(),
    }

    for filename, content in dot_files.items():
        Path(os.path.join(DIAGRAMS_DIR, filename)).write_text(content, encoding="utf-8")
        print(f"  Wrote {filename}")

    # Try rendering with dot
    if shutil.which("dot"):
        print("\n  Rendering PNGs with GraphViz...")
        for filename in dot_files:
            dot_path = os.path.join(DIAGRAMS_DIR, filename)
            try:
                subprocess.run(
                    ["dot", "-Tpng", dot_path, "-o", dot_path.replace(".dot", ".png")],
                    capture_output=True, check=True,
                )
                subprocess.run(
                    ["dot", "-Tsvg", dot_path, "-o", dot_path.replace(".dot", ".svg")],
                    capture_output=True, check=True,
                )
                print(f"    Rendered {filename}")
            except subprocess.CalledProcessError:
                pass

    # Combined markdown
    sections = []
    for filename, content in mermaid_files.items():
        title = filename.replace(".mmd", "").replace("-", " ")
        sections.append(f"## {title}\n\n```mermaid\n{content}\n```\n")

    mermaid_md = "# Dependency Visualizations\n\n" + "\n".join(sections)
    Path(os.path.join(DIAGRAMS_DIR, "all-diagrams.md")).write_text(mermaid_md, encoding="utf-8")
    print("  Wrote all-diagrams.md")

    print("\n=== Visualization complete ===\n")


if __name__ == "__main__":
    main()
