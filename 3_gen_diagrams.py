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


def _load_json(path: str, default=None):
    """Load a JSON file, returning *default* on any read/parse error."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        if default is None:
            raise
        print(f"  Warning: could not load {path}: {exc}")
        return default


graph = _load_json(os.path.join(OUT_DIR, "graph.json"))

# ─── Heat-map: load refactoring scores ──────────────────────────────

_rt_path = os.path.join(OUT_DIR, "refactoring-targets.json")
_score_map: dict[str, float] = {}  # node_id (repo/project) → refactoring_value_score
if os.path.isfile(_rt_path):
    _rt = _load_json(_rt_path, {})
    for _p in _rt.get("projects", []):
        _key = f"{_p['repo']}/{_p['project']}" if _p.get("repo") else _p.get("project", "")
        if _key:
            _score_map[_key] = _p.get("refactoring_value_score", 0)

# ─── Helpers ────────────────────────────────────────────────────────

ALL_TYPES = {
    "library", "connector", "sample", "application", "test", "tool",
    "localization", "webapp", "service", "desktopapp",
}

project_nodes = [n for n in graph["nodes"] if n.get("type") in ALL_TYPES]

# Compute max refactoring score per category for overview heat-map
_cat_max_score: dict[str, float] = {}
for _n in project_nodes:
    _ncat = _n.get("type", "")
    _nscore = _score_map.get(_n["id"], 0)
    if _nscore > _cat_max_score.get(_ncat, 0):
        _cat_max_score[_ncat] = _nscore

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


def _node_colour(node_id: str) -> "str | None":
    """Return Mermaid fill colour based on project refactoring score, or None for default."""
    score = _score_map.get(node_id, 0)
    if score > 100:  return "#D0002B"   # red   — high risk
    if score > 50:   return "#E87722"   # amber — medium
    if score > 10:   return "#9E8700"   # yellow — low-medium
    return None                          # default — clean


def _category_colour(category: str) -> "str | None":
    """Return colour based on max project refactoring score in the category."""
    score = _cat_max_score.get(category, 0)
    if score > 100:  return "#D0002B"
    if score > 50:   return "#E87722"
    if score > 10:   return "#9E8700"
    return None


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

    # Heat-map: colour nodes by refactoring score
    for nid in node_ids:
        colour = _node_colour(nid)
        if colour:
            lines.append(f"  style {sanitize_id(nid)} fill:{colour},color:#fff")

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

    # Heat-map: colour category nodes by max project refactoring score
    for cat in cat_counts:
        colour = _category_colour(cat)
        if colour:
            lines.append(f"  style {sanitize_id(cat)} fill:{colour},color:#fff")

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

    data_flow = _load_json(data_flow_path, {})
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


# ─── Mermaid: Business Layers ──────────────────────────────────────

def generate_business_layer_mermaid() -> str:
    """Generate a Mermaid diagram showing business layer summary with aggregated cross-layer edges."""
    flow_paths_path = os.path.join(OUT_DIR, "flow-paths.json")
    if not os.path.isfile(flow_paths_path):
        return "graph TD\n    no_data[No business layer data available]"

    flow_data = _load_json(flow_paths_path, {})
    layers_data = flow_data.get("businessLayers", {})
    layer_summary = flow_data.get("layerSummary", {})

    if not layers_data:
        return "graph TD\n    no_data[No business layer classifications found]"

    lines = ["graph TD"]

    # Define layer order for top-down display
    layer_order = ["Presentation", "Engine", "Service", "DataAccess", "Infrastructure", "Unclassified"]

    # Emit layer nodes
    for layer in layer_order:
        info = layer_summary.get(layer, {})
        count = info.get("count", 0)
        if count == 0:
            continue
        nid = sanitize_id(f"layer_{layer}")
        lines.append(f'    {nid}["{layer} ({count})"]')

    # Build node-to-layer lookup
    node_layer: dict[str, str] = {}
    for name, info in layers_data.items():
        node_layer[name] = info.get("layer", "Unclassified")

    # Aggregate cross-layer edges from project references
    layer_edges: dict[tuple[str, str], int] = {}
    for e in deduped_refs:
        from_id = e["from"]
        to_id = e["to"]
        # Extract project name from "repo/project" format
        from_name = from_id.split("/")[-1] if "/" in from_id else from_id
        to_name = to_id.split("/")[-1] if "/" in to_id else to_id
        from_layer = node_layer.get(from_name)
        to_layer = node_layer.get(to_name)
        if from_layer and to_layer and from_layer != to_layer:
            key = (from_layer, to_layer)
            layer_edges[key] = layer_edges.get(key, 0) + 1

    # Emit edges
    for (from_layer, to_layer), count in sorted(layer_edges.items(), key=lambda x: -x[1]):
        from_id = sanitize_id(f"layer_{from_layer}")
        to_id = sanitize_id(f"layer_{to_layer}")
        lines.append(f"    {from_id} -->|{count} refs| {to_id}")

    return "\n".join(lines)


def _group_by_prefix(names: list[str], max_nodes: int = 8) -> list[dict]:
    """Group project names by semantic category. Returns individual nodes if few, grouped otherwise.

    Each result: {"id": str, "label": str, "members": list[str]}
    Aims to produce at most `max_nodes` groups for compact diagrams.
    """
    if len(names) <= max_nodes:
        return [{"id": sanitize_id(n), "label": n, "members": [n]} for n in sorted(names)]

    # Extract semantic category: strip leading numbers, take the category word
    # e.g. "01_Strategies.HistorySMA" -> "Strategies"
    #      "02_Chart_ActiveOrders" -> "Chart"
    #      "BusinessEntities" -> "BusinessEntities"
    import re
    def _category(name: str) -> str:
        # Strip leading digits and underscores: "01_Strategies.HistorySMA" -> "Strategies.HistorySMA"
        stripped = re.sub(r"^\d+_", "", name)
        # Take first segment before . or _
        for sep in (".", "_"):
            if sep in stripped:
                return stripped.split(sep)[0]
        return stripped

    groups: dict[str, list[str]] = {}
    for name in names:
        cat = _category(name)
        groups.setdefault(cat, []).append(name)

    # If still too many groups, merge the smallest ones into "Other"
    if len(groups) > max_nodes:
        sorted_groups = sorted(groups.items(), key=lambda x: -len(x[1]))
        kept = dict(sorted_groups[:max_nodes - 1])
        other_members = []
        for cat, members in sorted_groups[max_nodes - 1:]:
            other_members.extend(members)
        if other_members:
            kept["Other"] = other_members
        groups = kept

    result = []
    for cat, members in sorted(groups.items(), key=lambda x: -len(x[1])):
        if len(members) == 1:
            result.append({"id": sanitize_id(members[0]), "label": members[0], "members": members})
        else:
            gid = sanitize_id(f"grp_{cat}")
            result.append({"id": gid, "label": f"{cat} ({len(members)})", "members": members})
    return result


def generate_e2e_flows_mermaid() -> str:
    """Generate aggregated E2E flows diagram showing projects grouped by business layer.

    Groups projects by name prefix within each layer to keep the diagram compact
    and vertically oriented regardless of project count.
    """
    flow_paths_path = os.path.join(OUT_DIR, "flow-paths.json")
    if not os.path.isfile(flow_paths_path):
        return "graph TD\n    no_data[No flow path data available]"

    flow_data = _load_json(flow_paths_path, {})
    flow_paths = flow_data.get("flowPaths", [])
    layers_data = flow_data.get("businessLayers", {})

    if not flow_paths:
        return "graph TD\n    no_data[No end-to-end flow paths found]"

    # Collect all projects and endpoints on flow paths
    projects_on_paths: set[str] = set()
    endpoints_on_paths: set[str] = set()
    for fp in flow_paths:
        for step in fp.get("path", []):
            if "project" in step:
                projects_on_paths.add(step["project"])
            elif "endpoint" in step:
                endpoints_on_paths.add(step["endpoint"])

    # Group projects by layer
    layer_projects: dict[str, list[str]] = {}
    for proj in projects_on_paths:
        layer = layers_data.get(proj, {}).get("layer", "Unclassified")
        layer_projects.setdefault(layer, []).append(proj)

    # Build project-to-group-id mapping for edge routing
    proj_to_node: dict[str, str] = {}  # project name -> mermaid node id

    lines = ["graph TD"]

    # Emit layer subgraphs with grouped nodes
    layer_order = ["Presentation", "Engine", "Service", "DataAccess", "Infrastructure", "Unclassified"]
    for layer in layer_order:
        projs = layer_projects.get(layer, [])
        if not projs:
            continue
        lid = sanitize_id(f"sg_{layer}")
        grouped = _group_by_prefix(projs)
        lines.append(f'    subgraph {lid}["{layer} ({len(projs)})"]')
        for g in grouped:
            lines.append(f'        {g["id"]}["{g["label"]}"]')
            for member in g["members"]:
                proj_to_node[member] = g["id"]
        lines.append("    end")

    # Emit data endpoint nodes (limit to 10)
    ep_to_node: dict[str, str] = {}
    if endpoints_on_paths:
        lines.append('    subgraph sg_Data["Data Endpoints"]')
        for ep in sorted(list(endpoints_on_paths)[:10]):
            eid = sanitize_id(ep)
            ep_name = ep.split(":", 1)[-1] if ":" in ep else ep
            ep_to_node[ep] = eid
            if ep.startswith("entity:") or ep.startswith("table:") or ep.startswith("collection:"):
                lines.append(f'        {eid}[("{ep_name}")]')
            elif ep.startswith("topic:") or ep.startswith("queue:") or ep.startswith("exchange:"):
                lines.append(f'        {eid}{{{{"{ep_name}"}}}}')
            elif ep.startswith("route:") or ep.startswith("url:"):
                lines.append(f'        {eid}(["{ep_name}"])')
            else:
                lines.append(f'        {eid}["{ep_name}"]')
        lines.append("    end")

    # Collect edges using group ids (deduplicated)
    edge_set: set[tuple[str, str]] = set()
    for fp in flow_paths:
        path = fp.get("path", [])
        for i in range(len(path) - 1):
            step = path[i]
            next_step = path[i + 1]

            from_id = None
            to_id = None

            if "project" in step:
                from_id = proj_to_node.get(step["project"])
            elif "endpoint" in step:
                from_id = ep_to_node.get(step["endpoint"])

            if "project" in next_step:
                to_id = proj_to_node.get(next_step["project"])
            elif "endpoint" in next_step:
                to_id = ep_to_node.get(next_step["endpoint"])

            if from_id and to_id and from_id != to_id:
                edge_key = (from_id, to_id)
                if edge_key not in edge_set:
                    edge_set.add(edge_key)
                    lines.append(f"    {from_id} --> {to_id}")

    return "\n".join(lines)


def generate_field_traceability_mermaid() -> str:
    """Generate a Mermaid diagram showing field-level traceability chains.

    Top-down layered diagram: XAML View → ViewModel → Entity → DB Column.
    Limited to top 20 most-complete chains for readability.
    """
    ft_path = os.path.join(OUT_DIR, "field-traceability.json")
    if not os.path.isfile(ft_path):
        return "graph TD\n    no_data[No field traceability data available]"

    ft_data = _load_json(ft_path, {})
    chains = ft_data.get("fieldChains", [])

    if not chains:
        return "graph TD\n    no_data[No field traceability chains found]"

    # Prioritize: full > xaml-to-entity > xaml-to-viewmodel > entity-to-column > xaml-only
    completeness_rank = {
        "full": 0, "xaml-to-entity": 1, "xaml-to-viewmodel": 2,
        "viewmodel-to-column": 3, "entity-to-column": 4, "xaml-only": 5,
    }
    sorted_chains = sorted(chains, key=lambda c: completeness_rank.get(c.get("chainCompleteness", ""), 9))
    top_chains = sorted_chains[:20]

    lines = ["graph TD"]

    # Collect unique nodes per layer
    xaml_nodes: dict[str, str] = {}  # node_id -> label
    vm_nodes: dict[str, str] = {}
    entity_nodes: dict[str, str] = {}
    db_nodes: dict[str, str] = {}
    edges: list[tuple[str, str, bool]] = []  # (from, to, is_partial)

    for ch in top_chains:
        comp = ch.get("chainCompleteness", "")
        conf = ch.get("confidence", "low")
        is_partial = conf == "low"

        xaml = ch.get("xamlBinding")
        vm_prop = ch.get("viewModelProperty")
        entity = ch.get("entityProperty")
        db = ch.get("dbColumn")

        xaml_id = None
        vm_id = None
        ent_id = None
        db_id = None

        if xaml:
            vt = xaml.get("viewType") or "UnknownView"
            bp = xaml.get("bindingPath", "?")
            xaml_id = sanitize_id(f"xaml_{vt}_{bp}")
            xaml_nodes[xaml_id] = f"{vt}\\n{bp}"

        if vm_prop:
            cn = vm_prop.get("className", "?")
            pn = vm_prop.get("propertyName", "?")
            pt = vm_prop.get("propertyType", "")
            vm_id = sanitize_id(f"vm_{cn}_{pn}")
            vm_nodes[vm_id] = f"{cn}\\n{pn}: {pt}"

        if entity:
            cn = entity.get("className", "?")
            pn = entity.get("propertyName", "?")
            pt = entity.get("propertyType", "")
            ent_id = sanitize_id(f"ent_{cn}_{pn}")
            entity_nodes[ent_id] = f"{cn}\\n{pn}: {pt}"

        if db:
            tbl = db.get("table", "?")
            col = db.get("column", "?")
            db_id = sanitize_id(f"db_{tbl}_{col}")
            db_nodes[db_id] = f"{tbl}\\n{col}"

        # Build edges for the chain
        if xaml_id and vm_id:
            edges.append((xaml_id, vm_id, is_partial))
        if vm_id and ent_id:
            edges.append((vm_id, ent_id, is_partial))
        elif xaml_id and ent_id and not vm_id:
            edges.append((xaml_id, ent_id, True))
        if ent_id and db_id:
            edges.append((ent_id, db_id, is_partial))

    # Emit subgraphs
    if xaml_nodes:
        lines.append('    subgraph XAML["XAML Views"]')
        for nid, label in xaml_nodes.items():
            lines.append(f'        {nid}["{label}"]')
        lines.append("    end")

    if vm_nodes:
        lines.append('    subgraph VM["ViewModels"]')
        for nid, label in vm_nodes.items():
            lines.append(f'        {nid}["{label}"]')
        lines.append("    end")

    if entity_nodes:
        lines.append('    subgraph Entity["Entities"]')
        for nid, label in entity_nodes.items():
            lines.append(f'        {nid}["{label}"]')
        lines.append("    end")

    if db_nodes:
        lines.append('    subgraph DB["Database Columns"]')
        for nid, label in db_nodes.items():
            lines.append(f'        {nid}[("{label}")]')
        lines.append("    end")

    # Emit edges (deduplicated)
    seen_edges: set[tuple[str, str]] = set()
    for from_id, to_id, partial in edges:
        key = (from_id, to_id)
        if key not in seen_edges:
            seen_edges.add(key)
            arrow = " -.->" if partial else " -->"
            lines.append(f"    {from_id}{arrow} {to_id}")

    return "\n".join(lines)


def generate_flow_path_mermaid(flow_path: dict) -> str:
    """Generate a Mermaid diagram for a single flow path."""
    path = flow_path.get("path", [])
    if not path:
        return "graph TD\n    empty[Empty path]"

    lines = ["graph TD"]

    prev_id = None
    for step in path:
        if "project" in step:
            nid = sanitize_id(step["project"])
            layer = step.get("layer", "")
            label = f"{step['project']}\\n({layer})"
            # Use rectangle for screens
            if layer == "Presentation":
                lines.append(f'    {nid}["{label}"]')
            else:
                lines.append(f'    {nid}["{label}"]')
        elif "endpoint" in step:
            nid = sanitize_id(step["endpoint"])
            ep_name = step["endpoint"].split(":", 1)[-1] if ":" in step["endpoint"] else step["endpoint"]
            ep_type = step.get("type", "")
            if ep_type == "database":
                lines.append(f'    {nid}[("{ep_name}")]')
            elif ep_type == "messaging":
                lines.append(f'    {nid}{{{{"{ep_name}"}}}}')
            elif ep_type == "api":
                lines.append(f'    {nid}(["{ep_name}"])')
            else:
                lines.append(f'    {nid}["{ep_name}"]')
        else:
            continue

        if prev_id:
            edge_type = step.get("edgeType", "")
            if "data-flow" in edge_type:
                lines.append(f"    {prev_id} ==> {nid}")
            else:
                lines.append(f"    {prev_id} --> {nid}")
        prev_id = nid

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
        "business-layers.mmd": generate_business_layer_mermaid(),
        "e2e-flows.mmd": generate_e2e_flows_mermaid(),
        "field-traceability.mmd": generate_field_traceability_mermaid(),
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

    # Individual flow path diagrams (top 10)
    flow_paths_path = os.path.join(OUT_DIR, "flow-paths.json")
    if os.path.isfile(flow_paths_path):
        flow_data = _load_json(flow_paths_path, {})
        flow_paths = flow_data.get("flowPaths", [])
        for i, fp in enumerate(flow_paths[:10]):
            content = generate_flow_path_mermaid(fp)
            filename = f"flow-path-{i}.mmd"
            Path(os.path.join(DIAGRAMS_DIR, filename)).write_text(content, encoding="utf-8")
        if flow_paths:
            print(f"  Wrote {min(10, len(flow_paths))} flow-path-*.mmd files")

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
