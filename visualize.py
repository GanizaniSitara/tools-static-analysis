#!/usr/bin/env python3
"""
Dependency Mapper — Visualization Generator (Python)

Reads output/graph.json and generates Mermaid + GraphViz diagrams.
Supports single-repo and multi-repo modes.
"""

import html as html_mod
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


# ─── DrawIO generation ──────────────────────────────────────────────

_DIO_NW, _DIO_NH = 160, 36
_DIO_GX, _DIO_GY = 12, 8
_DIO_COLORS = {
    "library": ("#4A90D9", "#3570A8"), "connector": ("#E67E22", "#C56A1B"),
    "application": ("#E74C3C", "#C0392B"), "test": ("#9B59B6", "#7D3C98"),
    "tool": ("#F39C12", "#D4860B"), "webapp": ("#1ABC9C", "#16A085"),
    "service": ("#3498DB", "#2980B9"), "desktopapp": ("#E91E63", "#C2185B"),
    "datasource": ("#27AE60", "#1E8449"),
}


def _xesc(text: str) -> str:
    return html_mod.escape(str(text), quote=True)


def _dio_cols(n: int) -> int:
    if n <= 4: return max(1, n)
    if n <= 12: return 4
    if n <= 30: return 5
    if n <= 60: return 6
    if n <= 120: return 8
    return 10


def _build_drawio(diagram_id: str, outer_groups: list, edges: list, direction: str = "LR") -> str:
    """
    Build a DrawIO XML diagram.

    outer_groups: [{"label": str, "groups": [{"label": str, "fill": str, "stroke": str,
                     "nodes": [{"id": str, "label": str, "shape"?: str}]}]}]
    edges: [{"from": str, "to": str, "dashed": bool}]
    """
    NW, NH, GX, GY = _DIO_NW, _DIO_NH, _DIO_GX, _DIO_GY
    GP = {"l": 12, "t": 32, "r": 12, "b": 12}
    OP = {"l": 12, "t": 36, "r": 12, "b": 12}

    cell_id = [2]
    node_map = {}
    all_cells = []

    def nid():
        c = str(cell_id[0]); cell_id[0] += 1; return c

    def grid(n):
        c = _dio_cols(n)
        r = (n + c - 1) // c
        return c, r

    cx, cy = 0, 0

    for og in outer_groups:
        has_outer = bool(og["label"])
        og_id = nid()

        ig_layouts = []
        for ig in og["groups"]:
            if not ig["nodes"]:
                continue
            cols, rows = grid(len(ig["nodes"]))
            iw = GP["l"] + cols * (NW + GX) - GX + GP["r"]
            ih = GP["t"] + rows * (NH + GY) - GY + GP["b"]
            ig_layouts.append((ig, iw, ih, cols))

        if not ig_layouts:
            continue

        # Stack inner groups
        if direction == "LR":
            max_w = max(w for _, w, _, _ in ig_layouts)
            pos, iy = [], 0
            for item in ig_layouts:
                pos.append((*item, 0, iy))
                iy += item[2] + 15
            content_w, content_h = max_w, iy - 15
        else:
            max_h = max(h for _, _, h, _ in ig_layouts)
            pos, ix = [], 0
            for item in ig_layouts:
                pos.append((*item, ix, 0))
                ix += item[1] + 15
            content_w, content_h = ix - 15, max_h

        og_w = (OP["l"] + content_w + OP["r"]) if has_outer else content_w
        og_h = (OP["t"] + content_h + OP["b"]) if has_outer else content_h
        off_x = OP["l"] if has_outer else 0
        off_y = OP["t"] if has_outer else 0

        if has_outer:
            all_cells.append(("og", og_id, og["label"], cx, cy, og_w, og_h))

        for ig, iw, ih, cols, rx, ry in pos:
            ig_id = nid()
            parent = og_id if has_outer else "1"
            abs_x = off_x + rx + (0 if has_outer else cx)
            abs_y = off_y + ry + (0 if has_outer else cy)

            all_cells.append(("ig", ig_id, ig["label"], abs_x, abs_y, iw, ih,
                              ig["fill"], ig["stroke"], parent))

            for i, nd in enumerate(ig["nodes"]):
                nd_id = nid()
                node_map[nd["id"]] = nd_id
                row, col = divmod(i, cols)
                nx = GP["l"] + col * (NW + GX)
                ny = GP["t"] + row * (NH + GY)
                shape = nd.get("shape", "rounded=1")
                all_cells.append(("nd", nd_id, nd["label"], nx, ny, NW, NH,
                                  ig["fill"], ig["stroke"], ig_id, shape))

        if direction == "LR":
            cx += og_w + 40
        else:
            cy += og_h + 40

    # Build XML
    lines = []
    for c in all_cells:
        if c[0] == "og":
            _, cid, label, x, y, w, h = c
            s = "swimlane;startSize=30;fontSize=14;fontStyle=1;fillColor=#f5f5f5;strokeColor=#666666;rounded=1;shadow=1;"
            lines.append(f'        <mxCell id="{cid}" value="{_xesc(label)}" style="{s}" vertex="1" connectable="0" parent="1">')
            lines.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>')
            lines.append(f'        </mxCell>')
        elif c[0] == "ig":
            _, cid, label, x, y, w, h, fill, stroke, parent = c
            s = f'swimlane;startSize=26;fontSize=12;fontStyle=1;fillColor={fill}33;strokeColor={stroke};rounded=1;swimlaneLine=1;'
            lines.append(f'        <mxCell id="{cid}" value="{_xesc(label)}" style="{s}" vertex="1" connectable="0" parent="{parent}">')
            lines.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>')
            lines.append(f'        </mxCell>')
        elif c[0] == "nd":
            _, cid, label, x, y, w, h, fill, stroke, parent, shape = c
            s = f'{shape};whiteSpace=wrap;html=1;fontSize=10;fillColor={fill};fontColor=#ffffff;strokeColor={stroke};shadow=1;'
            lines.append(f'        <mxCell id="{cid}" value="{_xesc(label)}" style="{s}" vertex="1" parent="{parent}">')
            lines.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>')
            lines.append(f'        </mxCell>')

    for e in edges:
        src, tgt = node_map.get(e["from"]), node_map.get(e["to"])
        if not src or not tgt:
            continue
        eid = nid()
        dashed = e.get("dashed", False)
        ds = "dashed=1;dashPattern=8 4;" if dashed else ""
        sc = "#ff4444" if dashed else "#999999"
        s = f'html=1;rounded=1;curved=1;strokeColor={sc};strokeWidth=1;{ds}'
        lines.append(f'        <mxCell id="{eid}" style="{s}" edge="1" source="{src}" target="{tgt}" parent="1">')
        lines.append(f'          <mxGeometry relative="1" as="geometry"/>')
        lines.append(f'        </mxCell>')

    cells_xml = "\n".join(lines)
    return (
        '<mxfile host="dependency-mapper" type="device">\n'
        f'  <diagram id="{_xesc(diagram_id)}" name="{_xesc(diagram_id)}">\n'
        '    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" '
        'connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="8000" pageHeight="8000" '
        'math="0" shadow="0">\n'
        '      <root>\n'
        '        <mxCell id="0"/>\n'
        '        <mxCell id="1" parent="0"/>\n'
        f'{cells_xml}\n'
        '      </root>\n'
        '    </mxGraphModel>\n'
        '  </diagram>\n'
        '</mxfile>'
    )


def generate_landscape_drawio() -> str:
    skip_types = {"localization", "sample"}
    outer_groups = []

    if is_multi_repo:
        for repo in repos:
            rn = [n for n in project_nodes if n.get("repo") == repo and n["type"] not in skip_types]
            if not rn:
                continue
            cats: dict[str, list] = {}
            for n in rn:
                cats.setdefault(n["type"], []).append(n)
            inner = []
            for cat, nodes in cats.items():
                fill, stroke = _DIO_COLORS.get(cat, ("#95A5A6", "#7F8C8D"))
                inner.append({"label": cat[0].upper() + cat[1:], "fill": fill, "stroke": stroke,
                              "nodes": [{"id": n["id"], "label": short_name(n)} for n in nodes]})
            outer_groups.append({"label": repo, "groups": inner})
    else:
        cats: dict[str, list] = {}
        for n in project_nodes:
            if n["type"] in skip_types:
                continue
            cats.setdefault(n["type"], []).append(n)
        inner = []
        for cat, nodes in cats.items():
            fill, stroke = _DIO_COLORS.get(cat, ("#95A5A6", "#7F8C8D"))
            inner.append({"label": cat[0].upper() + cat[1:] + "s", "fill": fill, "stroke": stroke,
                          "nodes": [{"id": n["id"], "label": short_name(n)} for n in nodes]})
        outer_groups.append({"label": "", "groups": inner})

    node_ids = set()
    for og in outer_groups:
        for ig in og["groups"]:
            for nd in ig["nodes"]:
                node_ids.add(nd["id"])

    edges = [{"from": e["from"], "to": e["to"], "dashed": e["type"] == "cross-repo-reference"}
             for e in deduped_refs if e["from"] in node_ids and e["to"] in node_ids]

    return _build_drawio("landscape", outer_groups, edges, "LR")


def generate_core_library_drawio() -> str:
    core_nodes = [n for n in project_nodes if n["type"] == "library"]
    core_ids = {n["id"] for n in core_nodes}
    fill, stroke = _DIO_COLORS["library"]

    outer_groups = []
    if is_multi_repo:
        for repo in repos:
            rn = [n for n in core_nodes if n.get("repo") == repo]
            if not rn:
                continue
            outer_groups.append({"label": repo, "groups": [
                {"label": "Libraries", "fill": fill, "stroke": stroke,
                 "nodes": [{"id": n["id"], "label": short_name(n)} for n in rn]}
            ]})
    else:
        outer_groups.append({"label": "", "groups": [
            {"label": "Libraries", "fill": fill, "stroke": stroke,
             "nodes": [{"id": n["id"], "label": short_name(n)} for n in core_nodes]}
        ]})

    edges = [{"from": e["from"], "to": e["to"], "dashed": e["type"] == "cross-repo-reference"}
             for e in deduped_refs if e["from"] in core_ids and e["to"] in core_ids]

    return _build_drawio("core-libraries", outer_groups, edges, "TD")


def generate_data_infra_drawio() -> str:
    service_types = {"webapp", "service", "application", "desktopapp"}
    svc_nodes = [n for n in project_nodes if n["type"] in service_types]
    db_nodes = [n for n in graph["nodes"]
                if n.get("type") == "datasource" and n.get("subtype") in ("database", "messaging", "cache")]

    outer_groups = []
    if is_multi_repo:
        for repo in repos:
            rn = [n for n in svc_nodes if n.get("repo") == repo]
            if not rn:
                continue
            cats: dict[str, list] = {}
            for n in rn:
                cats.setdefault(n["type"], []).append(n)
            inner = []
            for cat, nodes in cats.items():
                fill, stroke = _DIO_COLORS.get(cat, ("#95A5A6", "#7F8C8D"))
                inner.append({"label": cat[0].upper() + cat[1:], "fill": fill, "stroke": stroke,
                              "nodes": [{"id": n["id"], "label": short_name(n)} for n in nodes]})
            outer_groups.append({"label": repo, "groups": inner})
    else:
        inner = []
        for n in svc_nodes:
            fill, stroke = _DIO_COLORS.get(n["type"], ("#95A5A6", "#7F8C8D"))
            inner.append({"label": n["type"][0].upper() + n["type"][1:], "fill": fill, "stroke": stroke,
                          "nodes": [{"id": n["id"], "label": short_name(n)}]})
        outer_groups.append({"label": "Applications", "groups": inner})

    if db_nodes:
        fill, stroke = _DIO_COLORS["datasource"]
        outer_groups.append({"label": "Data Sources", "groups": [
            {"label": "External", "fill": fill, "stroke": stroke,
             "nodes": [{"id": n["id"], "label": n.get("pattern", n["id"]), "shape": "ellipse"}
                       for n in db_nodes]}
        ]})

    return _build_drawio("data-infrastructure", outer_groups, [], "LR")


def generate_nuget_drawio() -> str:
    nuget_nodes = [n for n in graph["nodes"] if n.get("type") == "nuget-package"]
    groups_map: dict[str, list] = {}
    for n in nuget_nodes:
        prefix = n["id"].replace("nuget:", "").split(".")[0]
        groups_map.setdefault(prefix, []).append(n)

    notable = sorted(groups_map.items(), key=lambda x: -len(x[1]))[:15]
    palette = [
        ("#3498DB", "#2980B9"), ("#E74C3C", "#C0392B"), ("#2ECC71", "#27AE60"),
        ("#9B59B6", "#7D3C98"), ("#F39C12", "#D4860B"), ("#1ABC9C", "#16A085"),
        ("#E67E22", "#C56A1B"), ("#E91E63", "#C2185B"), ("#00BCD4", "#0097A7"),
        ("#795548", "#5D4037"), ("#607D8B", "#455A64"), ("#FF5722", "#E64A19"),
        ("#4A90D9", "#3570A8"), ("#CDDC39", "#AFB42B"), ("#FF9800", "#F57C00"),
    ]

    inner_groups = []
    for i, (prefix, pkgs) in enumerate(notable):
        fill, stroke = palette[i % len(palette)]
        nodes = []
        for pkg in pkgs[:8]:
            name = pkg["id"].replace("nuget:", "")
            vers = ", ".join(pkg.get("versions", []))
            nodes.append({"id": pkg["id"], "label": name + (f"\n{vers}" if vers else "")})
        if len(pkgs) > 8:
            nodes.append({"id": f"more_{prefix}", "label": f"... +{len(pkgs) - 8} more"})
        inner_groups.append({"label": prefix, "fill": fill, "stroke": stroke, "nodes": nodes})

    return _build_drawio("nuget-groups", [{"label": "", "groups": inner_groups}], [], "LR")


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

    # DrawIO files
    drawio_files = {
        "landscape.drawio": generate_landscape_drawio(),
        "core-libraries.drawio": generate_core_library_drawio(),
        "data-infrastructure.drawio": generate_data_infra_drawio(),
        "nuget-groups.drawio": generate_nuget_drawio(),
    }

    for filename, content in drawio_files.items():
        Path(os.path.join(DIAGRAMS_DIR, filename)).write_text(content, encoding="utf-8")
        print(f"  Wrote {filename}")

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
