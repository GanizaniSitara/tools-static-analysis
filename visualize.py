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


# ─── Mermaid: Category overview ───────────────────────────────────────

def generate_category_overview_mermaid() -> str:
    """One node per category with count, edges between categories with aggregated counts."""
    skip_types = {"localization", "sample"}
    lines = ["graph LR"]

    # Build node-id -> type lookup
    node_type: dict[str, str] = {}
    for n in project_nodes:
        if n["type"] not in skip_types:
            node_type[n["id"]] = n["type"]

    # Count projects per category
    cat_counts: dict[str, int] = {}
    for n in project_nodes:
        if n["type"] in skip_types:
            continue
        cat_counts[n["type"]] = cat_counts.get(n["type"], 0) + 1

    # Aggregate edges between categories
    cat_edges: dict[tuple[str, str], int] = {}
    for e in deduped_refs:
        from_type = node_type.get(e["from"])
        to_type = node_type.get(e["to"])
        if from_type and to_type and from_type != to_type:
            key = (from_type, to_type)
            cat_edges[key] = cat_edges.get(key, 0) + 1

    # Emit nodes
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        label = cat[0].upper() + cat[1:]
        lines.append(f'    {sanitize_id(cat)}["{label} ({count})"]')

    # Emit edges
    for (from_cat, to_cat), count in sorted(cat_edges.items(), key=lambda x: -x[1]):
        lines.append(f'    {sanitize_id(from_cat)} -->|{count}| {sanitize_id(to_cat)}')

    return "\n".join(lines)


# ─── Mermaid: Category detail ────────────────────────────────────────

MAX_NODES = 50


def generate_category_detail_mermaid(category: str) -> str:
    """Per-category detail diagram. Full nodes if ≤MAX_NODES, prefix-grouped otherwise."""
    skip_types = {"localization", "sample"}

    cat_nodes = [n for n in project_nodes if n["type"] == category]
    cat_ids = {n["id"] for n in cat_nodes}

    # Build lookup of all non-skipped node ids to their type
    node_type: dict[str, str] = {}
    for n in project_nodes:
        if n["type"] not in skip_types:
            node_type[n["id"]] = n["type"]

    if len(cat_nodes) <= MAX_NODES:
        return _category_detail_full(category, cat_nodes, cat_ids, node_type)
    else:
        return _category_detail_grouped(category, cat_nodes, cat_ids, node_type)


def _category_detail_full(category: str, cat_nodes: list, cat_ids: set, node_type: dict) -> str:
    """Render individual project nodes for small categories."""
    lines = ["graph LR"]

    # Category subgraph
    cat_label = category[0].upper() + category[1:]
    lines.append(f'    subgraph {sanitize_id(category)}["{cat_label}"]')
    for n in cat_nodes:
        lines.append(f'        {sanitize_id(n["id"])}["{short_name(n)}"]')
    lines.append("    end")

    # Collect external nodes (nodes in other categories referenced by or referencing this category)
    external_cats: dict[str, set] = {}  # other_cat -> set of node ids
    for e in deduped_refs:
        if e["from"] in cat_ids and e["to"] not in cat_ids:
            to_type = node_type.get(e["to"])
            if to_type:
                external_cats.setdefault(to_type, set()).add(e["to"])
        elif e["to"] in cat_ids and e["from"] not in cat_ids:
            from_type = node_type.get(e["from"])
            if from_type:
                external_cats.setdefault(from_type, set()).add(e["from"])

    # Add external category group nodes
    for ext_cat, ext_ids in external_cats.items():
        ext_label = ext_cat[0].upper() + ext_cat[1:]
        ext_node_id = f"ext_{sanitize_id(ext_cat)}"
        lines.append(f'    {ext_node_id}(["{ext_label} ({len(ext_ids)})"])')

    # Intra-category edges
    for e in deduped_refs:
        if e["from"] in cat_ids and e["to"] in cat_ids:
            style = " -.->" if e["type"] == "cross-repo-reference" else " -->"
            lines.append(f"    {sanitize_id(e['from'])}{style} {sanitize_id(e['to'])}")

    # Edges to/from external category groups (deduplicated)
    seen_ext_edges: set[tuple[str, str]] = set()
    for e in deduped_refs:
        if e["from"] in cat_ids and e["to"] not in cat_ids:
            to_type = node_type.get(e["to"])
            if to_type:
                edge_key = (sanitize_id(e["from"]), f"ext_{sanitize_id(to_type)}")
                if edge_key not in seen_ext_edges:
                    seen_ext_edges.add(edge_key)
                    lines.append(f"    {edge_key[0]} -.-> {edge_key[1]}")
        elif e["to"] in cat_ids and e["from"] not in cat_ids:
            from_type = node_type.get(e["from"])
            if from_type:
                edge_key = (f"ext_{sanitize_id(from_type)}", sanitize_id(e["to"]))
                if edge_key not in seen_ext_edges:
                    seen_ext_edges.add(edge_key)
                    lines.append(f"    {edge_key[0]} -.-> {edge_key[1]}")

    return "\n".join(lines)


def _category_detail_grouped(category: str, cat_nodes: list, cat_ids: set, node_type: dict) -> str:
    """Group projects by name prefix (first 2 dot-segments) for large categories."""
    lines = ["graph LR"]

    # Group by prefix
    groups: dict[str, list] = {}
    for n in cat_nodes:
        name = short_name(n)
        parts = name.split(".")
        prefix = ".".join(parts[:2]) if len(parts) >= 2 else name
        groups.setdefault(prefix, []).append(n)

    # Build group id -> group key, and node id -> group key
    node_to_group: dict[str, str] = {}
    for prefix, nodes in groups.items():
        for n in nodes:
            node_to_group[n["id"]] = prefix

    # Emit group nodes
    cat_label = category[0].upper() + category[1:]
    lines.append(f'    subgraph {sanitize_id(category)}["{cat_label}"]')
    for prefix, nodes in sorted(groups.items(), key=lambda x: -len(x[1])):
        gid = sanitize_id(f"grp_{prefix}")
        if len(nodes) == 1:
            label = short_name(nodes[0])
        else:
            label = f"{prefix} ({len(nodes)})"
        lines.append(f'        {gid}["{label}"]')
    lines.append("    end")

    # Collect external categories
    external_cats: dict[str, set] = {}
    for e in deduped_refs:
        if e["from"] in cat_ids and e["to"] not in cat_ids:
            to_type = node_type.get(e["to"])
            if to_type:
                external_cats.setdefault(to_type, set()).add(e["to"])
        elif e["to"] in cat_ids and e["from"] not in cat_ids:
            from_type = node_type.get(e["from"])
            if from_type:
                external_cats.setdefault(from_type, set()).add(e["from"])

    for ext_cat, ext_ids in external_cats.items():
        ext_label = ext_cat[0].upper() + ext_cat[1:]
        ext_node_id = f"ext_{sanitize_id(ext_cat)}"
        lines.append(f'    {ext_node_id}(["{ext_label} ({len(ext_ids)})"])')

    # Aggregate intra-category edges between groups
    group_edges: dict[tuple[str, str], int] = {}
    for e in deduped_refs:
        if e["from"] in cat_ids and e["to"] in cat_ids:
            from_grp = node_to_group.get(e["from"])
            to_grp = node_to_group.get(e["to"])
            if from_grp and to_grp and from_grp != to_grp:
                key = (from_grp, to_grp)
                group_edges[key] = group_edges.get(key, 0) + 1

    # Aggregate edges to/from external category groups
    ext_edges_out: dict[tuple[str, str], int] = {}
    ext_edges_in: dict[tuple[str, str], int] = {}
    for e in deduped_refs:
        if e["from"] in cat_ids and e["to"] not in cat_ids:
            to_type = node_type.get(e["to"])
            from_grp = node_to_group.get(e["from"])
            if to_type and from_grp:
                key = (from_grp, to_type)
                ext_edges_out[key] = ext_edges_out.get(key, 0) + 1
        elif e["to"] in cat_ids and e["from"] not in cat_ids:
            from_type = node_type.get(e["from"])
            to_grp = node_to_group.get(e["to"])
            if from_type and to_grp:
                key = (from_type, to_grp)
                ext_edges_in[key] = ext_edges_in.get(key, 0) + 1

    # Determine minimum edge count to stay under Mermaid's 500-edge limit
    all_edge_counts = (
        list(group_edges.values())
        + list(ext_edges_out.values())
        + list(ext_edges_in.values())
    )
    MAX_EDGES = 400
    min_count = 1
    total_edges = len(all_edge_counts)
    if total_edges > MAX_EDGES:
        min_count = 2
        while sum(1 for c in all_edge_counts if c >= min_count) > MAX_EDGES:
            min_count += 1
        shown = sum(1 for c in all_edge_counts if c >= min_count)
        hidden = total_edges - shown
        lines.insert(0, f"%% EDGE_FILTER: total={total_edges} shown={shown} hidden={hidden} min_count={min_count}")

    for (from_grp, to_grp), count in sorted(group_edges.items(), key=lambda x: -x[1]):
        if count < min_count:
            continue
        from_id = sanitize_id(f"grp_{from_grp}")
        to_id = sanitize_id(f"grp_{to_grp}")
        lines.append(f"    {from_id} -->|{count}| {to_id}")

    for (from_grp, to_type), count in ext_edges_out.items():
        if count < min_count:
            continue
        from_id = sanitize_id(f"grp_{from_grp}")
        to_id = f"ext_{sanitize_id(to_type)}"
        lines.append(f"    {from_id} -.->|{count}| {to_id}")

    for (from_type, to_grp), count in ext_edges_in.items():
        if count < min_count:
            continue
        from_id = f"ext_{sanitize_id(from_type)}"
        to_id = sanitize_id(f"grp_{to_grp}")
        lines.append(f"    {from_id} -.->|{count}| {to_id}")

    return "\n".join(lines)


# ─── Mermaid: Data Flow ────────────────────────────────────────────

def generate_data_flow_mermaid() -> str:
    """Generate a Mermaid diagram showing projects connected through data infrastructure.

    Uses distinct shapes: [( )] for DB, {{ }} for messaging, ([ ]) for API routes.
    Thick arrows (==>) for writes, dashed arrows (-.->) for reads.
    """
    data_flow_path = os.path.join(OUT_DIR, "data-flow.json")
    if not os.path.isfile(data_flow_path):
        return "graph LR\n    no_data[No data flow information available]"

    data_flow = json.loads(Path(data_flow_path).read_text(encoding="utf-8"))
    data_nodes = data_flow.get("dataNodes", [])
    data_edges = data_flow.get("dataEdges", [])

    if not data_nodes:
        return "graph LR\n    no_data[No data flow nodes detected]"

    # Filter to nodes that have at least one writer/reader/exposer/consumer
    active_nodes = [
        n for n in data_nodes
        if n.get("writers") or n.get("readers") or n.get("exposers") or n.get("consumers")
    ]

    if not active_nodes:
        return "graph LR\n    no_data[No active data flow connections]"

    # Collect all project names involved
    all_projects: set[str] = set()
    for n in active_nodes:
        all_projects.update(n.get("writers", []))
        all_projects.update(n.get("readers", []))
        all_projects.update(n.get("exposers", []))
        all_projects.update(n.get("consumers", []))

    # Group data nodes by infrastructure type
    db_nodes = [n for n in active_nodes if n["infrastructure"] == "database"]
    msg_nodes = [n for n in active_nodes if n["infrastructure"] == "messaging"]
    api_nodes = [n for n in active_nodes if n["infrastructure"] == "api"]

    # Limit nodes to prevent oversized diagrams
    MAX_DATA_NODES = 30
    MAX_PROJECTS = 40

    def top_nodes(nodes: list, limit: int) -> list:
        """Return top N nodes sorted by connection count."""
        return sorted(
            nodes,
            key=lambda n: len(n.get("writers", [])) + len(n.get("readers", []))
                        + len(n.get("exposers", [])) + len(n.get("consumers", [])),
            reverse=True,
        )[:limit]

    total = len(db_nodes) + len(msg_nodes) + len(api_nodes)
    if total > MAX_DATA_NODES:
        ratio = MAX_DATA_NODES / max(total, 1)
        db_nodes = top_nodes(db_nodes, max(1, int(len(db_nodes) * ratio)))
        msg_nodes = top_nodes(msg_nodes, max(1, int(len(msg_nodes) * ratio)))
        api_nodes = top_nodes(api_nodes, max(1, int(len(api_nodes) * ratio)))

    shown_node_ids = {n["id"] for n in db_nodes + msg_nodes + api_nodes}

    # Recalculate projects from shown nodes only
    all_projects = set()
    for n in db_nodes + msg_nodes + api_nodes:
        all_projects.update(n.get("writers", []))
        all_projects.update(n.get("readers", []))
        all_projects.update(n.get("exposers", []))
        all_projects.update(n.get("consumers", []))

    # Limit projects if too many
    if len(all_projects) > MAX_PROJECTS:
        # Keep projects with most connections
        proj_counts: dict[str, int] = {}
        for n in db_nodes + msg_nodes + api_nodes:
            for p in n.get("writers", []) + n.get("readers", []) + n.get("exposers", []) + n.get("consumers", []):
                proj_counts[p] = proj_counts.get(p, 0) + 1
        all_projects = set(sorted(proj_counts, key=lambda p: -proj_counts[p])[:MAX_PROJECTS])

    lines = ["graph LR"]

    # Project nodes subgraph
    lines.append('    subgraph Projects["Services & Projects"]')
    for proj in sorted(all_projects):
        lines.append(f'        {sanitize_id(proj)}["{proj}"]')
    lines.append("    end")

    # Database subgraph
    if db_nodes:
        lines.append('    subgraph Database["Database / Storage"]')
        for n in db_nodes:
            nid = sanitize_id(n["id"])
            label = n["name"]
            # [( )] = cylinder shape for databases
            lines.append(f'        {nid}[("{label}")]')
        lines.append("    end")

    # Messaging subgraph
    if msg_nodes:
        lines.append('    subgraph Messaging["Message Queues / Topics"]')
        for n in msg_nodes:
            nid = sanitize_id(n["id"])
            label = n["name"]
            # {{ }} = hexagon shape for messaging
            lines.append(f'        {nid}{{{{"{label}"}}}}')
        lines.append("    end")

    # API subgraph
    if api_nodes:
        lines.append('    subgraph APIs["API Routes"]')
        for n in api_nodes:
            nid = sanitize_id(n["id"])
            label = n["name"]
            # ([ ]) = stadium shape for API routes
            lines.append(f'        {nid}(["{label}"])')
        lines.append("    end")

    # Edges: thick (==>) for write/expose, dashed (-.->) for read/consume
    edge_set: set[str] = set()
    for n in db_nodes + msg_nodes + api_nodes:
        nid = sanitize_id(n["id"])
        for proj in n.get("writers", []):
            if proj in all_projects:
                edge_key = f"{sanitize_id(proj)}==>|write|{nid}"
                if edge_key not in edge_set:
                    edge_set.add(edge_key)
                    lines.append(f"    {sanitize_id(proj)} ==>|write| {nid}")
        for proj in n.get("readers", []):
            if proj in all_projects:
                edge_key = f"{nid}-.->|read|{sanitize_id(proj)}"
                if edge_key not in edge_set:
                    edge_set.add(edge_key)
                    lines.append(f"    {nid} -.->|read| {sanitize_id(proj)}")
        for proj in n.get("exposers", []):
            if proj in all_projects:
                edge_key = f"{sanitize_id(proj)}==>|expose|{nid}"
                if edge_key not in edge_set:
                    edge_set.add(edge_key)
                    lines.append(f"    {sanitize_id(proj)} ==>|expose| {nid}")
        for proj in n.get("consumers", []):
            if proj in all_projects:
                edge_key = f"{nid}-.->|consume|{sanitize_id(proj)}"
                if edge_key not in edge_set:
                    edge_set.add(edge_key)
                    lines.append(f"    {nid} -.->|consume| {sanitize_id(proj)}")

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
        "data-flow.mmd": generate_data_flow_mermaid(),
        "nuget-groups.mmd": generate_nuget_mermaid(),
    }

    for filename, content in mermaid_files.items():
        Path(os.path.join(DIAGRAMS_DIR, filename)).write_text(content, encoding="utf-8")
        print(f"  Wrote {filename}")

    # Category overview + per-category detail diagrams
    overview = generate_category_overview_mermaid()
    Path(os.path.join(DIAGRAMS_DIR, "overview.mmd")).write_text(overview, encoding="utf-8")
    print("  Wrote overview.mmd")

    skip_types = {"localization", "sample"}
    category_types = sorted({n["type"] for n in project_nodes if n["type"] not in skip_types})
    for cat in category_types:
        detail = generate_category_detail_mermaid(cat)
        filename = f"category-{cat}.mmd"
        Path(os.path.join(DIAGRAMS_DIR, filename)).write_text(detail, encoding="utf-8")
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
