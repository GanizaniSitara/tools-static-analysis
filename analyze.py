#!/usr/bin/env python3
"""
Dependency Mapper — Static Analysis Engine (Python)

Modes:
  python analyze.py /path/to/single-repo
  python analyze.py /path/to/parent-dir    (auto-discovers repos by .sln/.git)

Extracts:
  1. NuGet package dependencies (from .csproj + .props)
  2. Project-to-project references (including cross-repo)
  3. Data access patterns (DbContext, SqlConnection, HttpClient, etc.)
  4. Configuration / connection strings

Outputs: output/dependencies.csv, output/project-refs.csv,
         output/data-sources.json, output/configs.json,
         output/graph.json, output/repos.json
"""

import json
import os
import re
import sys
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────

SCAN_ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT_DIR = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "output")

os.makedirs(OUT_DIR, exist_ok=True)


# ─── XML helpers (no external deps — regex-based for .csproj/.props) ──

def parse_xml_elements(xml: str, tag: str) -> list[dict]:
    """Parse XML elements by tag name using regex. Returns list of {attrs, inner}."""
    results = []
    pattern = re.compile(
        rf"<{tag}\b([^>]*?)\s*/>|<{tag}\b([^>]*?)>([\s\S]*?)</{tag}>",
        re.IGNORECASE,
    )
    for m in pattern.finditer(xml):
        attr_str = m.group(1) or m.group(2) or ""
        inner = m.group(3) or ""
        attrs = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', attr_str))
        results.append({"attrs": attrs, "inner": inner})
    return results


# ─── Find all files recursively ─────────────────────────────────────

SKIP_DIRS = {".git", "node_modules", "bin", "obj"}


def find_files(directory: str, pattern: re.Pattern, results: list | None = None) -> list[str]:
    """Recursively find files matching a regex pattern on the filename."""
    if results is None:
        results = []
    if not os.path.exists(directory):
        return results
    try:
        entries = os.scandir(directory)
    except PermissionError:
        return results

    for entry in entries:
        full = entry.path
        try:
            is_dir = entry.is_dir(follow_symlinks=True)
        except OSError:
            continue

        if is_dir:
            if entry.name in SKIP_DIRS:
                continue
            find_files(full, pattern, results)
        elif pattern.search(entry.name):
            results.append(full)

    return results


# ─── Auto-discover repos ────────────────────────────────────────────

def discover_repos(scan_root: str) -> list[dict]:
    """Discover .NET repositories under scan_root."""
    sln_files = find_files(scan_root, re.compile(r"\.sln$"))
    csproj_files = find_files(scan_root, re.compile(r"\.csproj$"))

    if not csproj_files:
        print("  No .csproj files found. Nothing to analyze.")
        sys.exit(0)

    # Check if the root itself has .sln files directly
    root_slns = [f for f in os.listdir(scan_root) if f.endswith(".sln")]
    if root_slns:
        return [{"name": os.path.basename(scan_root), "root": scan_root, "solutions": root_slns}]

    # Multi-repo mode: look for repos in subdirectories
    repos = []
    seen = set()

    for entry_name in sorted(os.listdir(scan_root)):
        if entry_name.startswith("."):
            continue
        sub_dir = os.path.join(scan_root, entry_name)
        try:
            if not os.path.isdir(sub_dir):
                continue
        except OSError:
            continue

        sub_csproj = find_files(sub_dir, re.compile(r"\.csproj$"))
        if not sub_csproj:
            continue

        sub_slns = [os.path.relpath(s, sub_dir) for s in find_files(sub_dir, re.compile(r"\.sln$"))]

        if sub_dir not in seen:
            repos.append({"name": entry_name, "root": sub_dir, "solutions": sub_slns})
            seen.add(sub_dir)

    # If no subdirectory repos found but we have csproj files, treat root as single repo
    if not repos:
        return [{"name": os.path.basename(scan_root), "root": scan_root, "solutions": []}]

    return repos


# ─── Resolve MSBuild properties ─────────────────────────────────────

def load_properties(repo_root: str) -> dict[str, str]:
    """Load MSBuild properties from .props files."""
    props = {}

    # Scan for .props files at repo root (max 2 levels deep)
    props_files = [
        f for f in find_files(repo_root, re.compile(r"\.props$", re.IGNORECASE))
        if len(os.path.relpath(f, repo_root).replace("\\", "/").split("/")) <= 2
    ]

    skip_tags = {"PropertyGroup", "Condition", "Project", "Import", "ItemGroup"}

    for pf in props_files:
        try:
            xml = Path(pf).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in re.finditer(r"<(\w+)>([^<]+)</\1>", xml):
            tag_name, tag_val = m.group(1), m.group(2)
            if tag_name not in skip_tags and tag_name not in props:
                props[tag_name] = tag_val

    # Also look for Directory.Build.props / Directory.Packages.props
    for name in ("Directory.Build.props", "Directory.Packages.props"):
        dbp = os.path.join(repo_root, name)
        if os.path.isfile(dbp):
            try:
                xml = Path(dbp).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in re.finditer(r"<(\w+)>([^<]+)</\1>", xml):
                if m.group(1) not in props:
                    props[m.group(1)] = m.group(2)

    return props


def resolve_version(version: str, props: dict[str, str]) -> str:
    """Resolve $(VarName) references in version strings."""
    if not version:
        return ""
    m = re.match(r"^\$\((\w+)\)$", version)
    if m and m.group(1) in props:
        return props[m.group(1)]
    return version


# ─── Resolve .props imports (recursive) ────────────────────────────

def resolve_imports(
    xml_content: str,
    file_dir: str,
    repo_root: str,
    visited: set | None = None,
) -> dict:
    """Recursively resolve Import elements in .csproj/.props files."""
    if visited is None:
        visited = set()

    all_package_refs = []
    all_project_refs = []

    imports = parse_xml_elements(xml_content, "Import")
    for imp in imports:
        import_path = imp["attrs"].get("Project", "")
        if not import_path:
            continue

        # Skip SDK imports and unresolvable conditional imports
        if "$(" in import_path and "RepoGitHubPath" not in import_path and "MSBuildThisFileDirectory" not in import_path:
            continue

        import_path = import_path.replace("$(RepoGitHubPath)", repo_root + "/")
        import_path = import_path.replace("$(MSBuildThisFileDirectory)", file_dir + "/")
        import_path = import_path.replace("\\", "/")

        resolved = os.path.normpath(os.path.join(file_dir, import_path))
        if resolved in visited or not os.path.isfile(resolved):
            continue
        visited.add(resolved)

        try:
            props_xml = Path(resolved).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        props_dir = os.path.dirname(resolved)

        # Recurse into imported file
        sub = resolve_imports(props_xml, props_dir, repo_root, visited)
        all_package_refs.extend(sub["package_refs"])
        all_project_refs.extend(sub["project_refs"])

        # Parse PackageReferences in imported file
        for p in parse_xml_elements(props_xml, "PackageReference"):
            if p["attrs"].get("Include"):
                all_package_refs.append({
                    "name": p["attrs"]["Include"],
                    "version": p["attrs"].get("Version", ""),
                })

        # Parse ProjectReferences in imported file
        for pr in parse_xml_elements(props_xml, "ProjectReference"):
            if pr["attrs"].get("Include"):
                ref_path = pr["attrs"]["Include"]
                ref_path = ref_path.replace("$(RepoGitHubPath)", repo_root + "/")
                ref_path = ref_path.replace("\\", "/")
                all_project_refs.append({"raw_path": ref_path, "resolve_from": props_dir})

    return {"package_refs": all_package_refs, "project_refs": all_project_refs}


# ─── Extract dependencies from a single repo ───────────────────────

def extract_dependencies_from_repo(repo: dict, global_scan_root: str) -> dict:
    """Extract all dependencies from a single repo."""
    repo_root = repo["root"]
    props = load_properties(repo_root)
    csproj_files = find_files(repo_root, re.compile(r"\.csproj$"))
    abs_root = os.path.abspath(repo_root)

    package_deps = []
    project_refs = []
    project_meta = []

    for csproj_path in csproj_files:
        try:
            xml = Path(csproj_path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        csproj_dir = os.path.dirname(csproj_path)
        proj_name = os.path.splitext(os.path.basename(csproj_path))[0]
        rel_path = os.path.relpath(csproj_path, abs_root)
        global_rel_path = os.path.relpath(csproj_path, global_scan_root)

        category = categorize_project(rel_path, proj_name, xml)
        project_meta.append({
            "project": proj_name,
            "repo": repo["name"],
            "path": rel_path,
            "globalPath": global_rel_path,
            "category": category,
        })

        # Resolve inherited deps from .props imports
        inherited = resolve_imports(xml, csproj_dir, abs_root)

        # Direct PackageReferences
        direct_pkgs = parse_xml_elements(xml, "PackageReference")
        all_pkgs = inherited["package_refs"] + [
            {"name": p["attrs"].get("Include", ""), "version": p["attrs"].get("Version", "")}
            for p in direct_pkgs
        ]

        for pkg in all_pkgs:
            if pkg["name"]:
                package_deps.append({
                    "project": proj_name,
                    "repo": repo["name"],
                    "package": pkg["name"],
                    "version": resolve_version(pkg["version"], props),
                })

        # Direct ProjectReferences
        direct_refs = parse_xml_elements(xml, "ProjectReference")

        all_refs = []
        # From inherited imports
        for r in inherited["project_refs"]:
            resolved = os.path.normpath(os.path.join(r["resolve_from"], r["raw_path"]))
            all_refs.append(resolved)
        # From direct refs
        for r in direct_refs:
            p = r["attrs"].get("Include", "")
            p = p.replace("$(RepoGitHubPath)", abs_root + "/")
            p = p.replace("\\", "/")
            resolved = os.path.normpath(os.path.join(csproj_dir, p))
            all_refs.append(resolved)

        for resolved_ref in all_refs:
            if not resolved_ref:
                continue
            ref_name = os.path.splitext(os.path.basename(resolved_ref))[0]
            ref_rel_path = os.path.relpath(resolved_ref, abs_root)
            ref_global_path = os.path.relpath(resolved_ref, global_scan_root)
            is_in_same_repo = resolved_ref.startswith(abs_root)
            project_refs.append({
                "project": proj_name,
                "repo": repo["name"],
                "references": ref_name,
                "referencePath": ref_rel_path,
                "referenceGlobalPath": ref_global_path,
                "crossRepo": not is_in_same_repo,
            })

    return {
        "package_deps": package_deps,
        "project_refs": project_refs,
        "project_meta": project_meta,
        "props": props,
    }


# ─── Generic project categorization ─────────────────────────────────

def categorize_project(rel_path: str, proj_name: str, xml: str) -> str:
    """Categorize a project based on its path, name, and csproj content."""
    rp = rel_path.lower()
    pn = proj_name.lower()

    # Test projects
    if (
        "test" in rp
        or pn.endswith(".tests")
        or pn.endswith(".test")
        or pn.startswith("test.")
        or pn.startswith("tests.")
        or "Microsoft.NET.Test.Sdk" in xml
        or "xunit" in xml
        or "MSTest" in xml
    ):
        return "Test"

    # Sample/example projects
    if (
        rp.startswith("samples/")
        or rp.startswith("examples/")
        or rp.startswith("demo/")
        or "sample" in pn
        or "example" in pn
        or "demo" in pn
    ):
        return "Sample"

    # Tools / generators / utilities
    if any(kw in pn for kw in ("generator", "extractor", "tool", "cli", "console")):
        return "Tool"

    # Web applications
    if (
        "Microsoft.NET.Sdk.Web" in xml
        or ".web" in pn
        or ".api" in pn
        or "webapp" in pn
        or "webapi" in pn
        or "blazor" in pn
    ):
        return "WebApp"

    # Worker / background services
    if (
        "Microsoft.NET.Sdk.Worker" in xml
        or "worker" in pn
        or "service" in pn
        or "job" in pn
        or "hosted" in pn
    ):
        return "Service"

    # WPF / Windows apps
    if (
        "<UseWPF>" in xml
        or "<UseWindowsForms>" in xml
        or "WinExe" in xml
        or "desktop" in pn
        or "wpf" in pn
    ):
        return "DesktopApp"

    # Localization
    if "localization" in rp or pn.startswith("localization"):
        return "Localization"

    # Connectors / adapters
    if rp.startswith("connectors/") or "connector" in pn or "adapter" in pn:
        return "Connector"

    # Library (netstandard or no output type)
    if "netstandard" in xml or ("<OutputType>" not in xml and "Sdk.Web" not in xml):
        return "Library"

    return "Application"


# ─── Data access pattern discovery ──────────────────────────────────

DATA_PATTERNS = [
    {"name": "DbContext",            "regex": re.compile(r":\s*DbContext\b"),                                "type": "database"},
    {"name": "SqlConnection",        "regex": re.compile(r"new\s+SqlConnection\s*\("),                      "type": "database"},
    {"name": "SqlClient",            "regex": re.compile(r"Microsoft\.Data\.SqlClient|System\.Data\.SqlClient"), "type": "database"},
    {"name": "HttpClient.Injection", "regex": re.compile(r"AddHttpClient[<(]"),                              "type": "api"},
    {"name": "HttpClient.New",       "regex": re.compile(r"new\s+HttpClient\s*\("),                          "type": "api"},
    {"name": "HttpClient.BaseAddress", "regex": re.compile(r'BaseAddress\s*=\s*new\s+Uri\s*\(\s*"([^"]+)"'), "type": "api"},
    {"name": "WebSocket",            "regex": re.compile(r"WebSocket|ClientWebSocket"),                      "type": "api"},
    {"name": "ConnectionString",     "regex": re.compile(r"[Cc]onnection[Ss]tring"),                         "type": "config"},
    {"name": "Repository",           "regex": re.compile(r"class\s+\w*Repository\w*\b"),                     "type": "pattern"},
    {"name": "DataAccess",           "regex": re.compile(r"class\s+\w*DataAccess\w*\b"),                     "type": "pattern"},
    {"name": "gRPC",                 "regex": re.compile(r"Grpc\.Core|Grpc\.Net|\.Protos?\b"),               "type": "api"},
    {"name": "RabbitMQ",             "regex": re.compile(r"RabbitMQ|IModel|IConnection.*RabbitMQ"),           "type": "messaging"},
    {"name": "Kafka",                "regex": re.compile(r"Confluent\.Kafka|IProducer|IConsumer.*Kafka"),     "type": "messaging"},
    {"name": "Redis",                "regex": re.compile(r"StackExchange\.Redis|IConnectionMultiplexer|RedisConnection"), "type": "cache"},
    {"name": "MongoDB",              "regex": re.compile(r"MongoDB\.Driver|IMongoClient|MongoCollection"),   "type": "database"},
    {"name": "EntityFramework",      "regex": re.compile(r"\.UseSqlServer\(|\.UseNpgsql\(|\.UseSqlite\(|\.UseMySql\("), "type": "database"},
    {"name": "Dapper",               "regex": re.compile(r"\.Query[<(]|\.Execute\("),                        "type": "database"},
    {"name": "FTP",                  "regex": re.compile(r"FtpClient|FluentFTP"),                            "type": "datasource"},
    {"name": "FileStorage",          "regex": re.compile(r"File\.(ReadAll|WriteAll|Open|Create)\b"),         "type": "storage"},
    {"name": "IMessageAdapter",      "regex": re.compile(r":\s*IMessageAdapter\b|class\s+\w+Adapter\b"),    "type": "connector"},
]


def discover_data_patterns(scan_root: str, repos: list[dict]) -> list[dict]:
    """Scan .cs files for data access patterns."""
    findings = []
    abs_root = os.path.abspath(scan_root)

    for repo in repos:
        cs_files = find_files(repo["root"], re.compile(r"\.cs$"))

        for cs_file in cs_files:
            try:
                content = Path(cs_file).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            lines = content.split("\n")
            rel_path = os.path.relpath(cs_file, abs_root)

            for pat in DATA_PATTERNS:
                for i, line in enumerate(lines):
                    match = pat["regex"].search(line)
                    if match:
                        findings.append({
                            "file": rel_path,
                            "repo": repo["name"],
                            "line": i + 1,
                            "pattern": pat["name"],
                            "type": pat["type"],
                            "match": match.group(0)[:120],
                            "context": line.strip()[:200],
                        })

    return findings


# ─── Configuration extraction ───────────────────────────────────────

def extract_json_paths(obj, key: str):
    """Recursively search for a key in a JSON object."""
    if not isinstance(obj, dict):
        return None
    if key in obj:
        return obj[key]
    for v in obj.values():
        result = extract_json_paths(v, key)
        if result is not None:
            return result
    return None


def extract_configs(scan_root: str, repos: list[dict]) -> list[dict]:
    """Extract configuration files and connection strings."""
    abs_root = os.path.abspath(scan_root)
    configs = []

    config_patterns = [
        re.compile(r"appsettings.*\.json$", re.IGNORECASE),
        re.compile(r"web\.config$", re.IGNORECASE),
        re.compile(r"app\.config$", re.IGNORECASE),
        re.compile(r"launchSettings\.json$", re.IGNORECASE),
    ]

    for repo in repos:
        config_files = []
        for pat in config_patterns:
            config_files.extend(find_files(repo["root"], pat))

        for f in config_files:
            rel_path = os.path.relpath(f, abs_root)
            try:
                content = Path(f).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            if f.endswith(".json"):
                try:
                    data = json.loads(content)
                    conn_strings = (
                        extract_json_paths(data, "ConnectionStrings")
                        or extract_json_paths(data, "connectionStrings")
                        or {}
                    )
                    urls = (
                        extract_json_paths(data, "Urls")
                        or extract_json_paths(data, "urls")
                        or {}
                    )
                    configs.append({
                        "file": rel_path,
                        "repo": repo["name"],
                        "type": "json",
                        "connectionStrings": conn_strings,
                        "urls": urls,
                        "raw": content[:2000] + ("..." if len(content) > 2000 else ""),
                    })
                except json.JSONDecodeError:
                    configs.append({
                        "file": rel_path,
                        "repo": repo["name"],
                        "type": "json-parse-error",
                        "raw": content[:500],
                    })
            else:
                # XML config files
                conn_strings = {}
                for m in re.finditer(r'<add\s+name="([^"]*)"[^>]*connectionString="([^"]*)"', content, re.IGNORECASE):
                    conn_strings[m.group(1)] = m.group(2)

                endpoints = [
                    m.group(1) for m in re.finditer(r'<endpoint\s+[^>]*address="([^"]*)"', content, re.IGNORECASE)
                ]

                configs.append({
                    "file": rel_path,
                    "repo": repo["name"],
                    "type": "xml",
                    "connectionStrings": conn_strings,
                    "endpoints": endpoints,
                    "raw": content[:2000] + ("..." if len(content) > 2000 else ""),
                })

    return configs


# ─── Build dependency graph ─────────────────────────────────────────

def build_graph(
    package_deps: list[dict],
    project_refs: list[dict],
    project_meta: list[dict],
    data_findings: list[dict],
    configs: list[dict],
) -> dict:
    """Build the full dependency graph as a JSON-serialisable dict."""
    nodes = {}
    edges = []

    # Project nodes
    for pm in project_meta:
        node_id = f"{pm['repo']}/{pm['project']}" if pm.get("repo") else pm["project"]
        nodes[node_id] = {
            "id": node_id,
            "project": pm["project"],
            "repo": pm.get("repo", ""),
            "type": pm["category"].lower(),
            "path": pm["path"],
            "globalPath": pm["globalPath"],
            "description": f"{pm['category']}: {pm['project']} ({pm.get('repo', '')})",
        }

    # NuGet package nodes
    nuget_packages: dict[str, dict] = {}
    for pd in package_deps:
        pkg_id = pd["package"]
        if pkg_id not in nuget_packages:
            nuget_packages[pkg_id] = {"versions": set(), "consumers": set()}
        nuget_packages[pkg_id]["versions"].add(pd["version"])
        nuget_packages[pkg_id]["consumers"].add(f"{pd['repo']}/{pd['project']}")

    for pkg_name, info in nuget_packages.items():
        nodes[f"nuget:{pkg_name}"] = {
            "id": f"nuget:{pkg_name}",
            "type": "nuget-package",
            "versions": sorted(info["versions"]),
            "consumers": sorted(info["consumers"]),
            "description": f"NuGet: {pkg_name} ({', '.join(sorted(info['versions']))})",
        }

    # Project reference edges
    # Build a lookup for project meta by project name
    meta_by_name = {}
    for pm in project_meta:
        meta_by_name[pm["project"]] = pm

    for pr in project_refs:
        from_id = f"{pr['repo']}/{pr['project']}"
        target = meta_by_name.get(pr["references"])
        to_id = f"{target['repo']}/{target['project']}" if target else pr["references"]
        edges.append({
            "from": from_id,
            "to": to_id,
            "type": "cross-repo-reference" if pr["crossRepo"] else "project-reference",
        })

    # NuGet dependency edges
    for pd in package_deps:
        edges.append({
            "from": f"{pd['repo']}/{pd['project']}",
            "to": f"nuget:{pd['package']}",
            "type": "nuget-dependency",
        })

    # Data source nodes
    datasource_map: dict[str, dict] = {}
    for f in data_findings:
        if f["type"] in ("connector", "api", "database", "messaging", "cache"):
            key = f"{f['type']}:{f['pattern']}:{f['repo']}"
            if key not in datasource_map:
                datasource_map[key] = {
                    "type": f["type"],
                    "pattern": f["pattern"],
                    "repo": f["repo"],
                    "occurrences": [],
                }
            datasource_map[key]["occurrences"].append({
                "file": f["file"],
                "line": f["line"],
                "context": f["context"],
            })

    for ds in datasource_map.values():
        node_id = f"datasource:{ds['repo']}:{ds['pattern']}"
        if node_id not in nodes:
            nodes[node_id] = {
                "id": node_id,
                "type": "datasource",
                "subtype": ds["type"],
                "pattern": ds["pattern"],
                "repo": ds["repo"],
                "occurrences": len(ds["occurrences"]),
                "description": f"{ds['pattern']} in {ds['repo']} ({len(ds['occurrences'])} occurrences)",
            }

    # Repo summary
    repo_summary: dict[str, dict] = {}
    for pm in project_meta:
        repo_name = pm.get("repo", "default")
        if repo_name not in repo_summary:
            repo_summary[repo_name] = {"projects": 0, "categories": {}}
        repo_summary[repo_name]["projects"] += 1
        cat = pm["category"]
        repo_summary[repo_name]["categories"][cat] = repo_summary[repo_name]["categories"].get(cat, 0) + 1

    # Category summary
    cat_counts: dict[str, int] = {}
    for pm in project_meta:
        cat_counts[pm["category"]] = cat_counts.get(pm["category"], 0) + 1

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "summary": {
            "totalRepos": len(repo_summary),
            "totalProjects": len(project_meta),
            "totalNuGetPackages": len(nuget_packages),
            "totalProjectRefs": len(project_refs),
            "totalCrossRepoRefs": sum(1 for r in project_refs if r["crossRepo"]),
            "totalDataFindings": len(data_findings),
            "totalConfigFiles": len(configs),
            "repos": repo_summary,
            "categories": cat_counts,
        },
    }


# ─── Write CSV ───────────────────────────────────────────────────────

def write_csv(filepath: str, rows: list[dict], columns: list[str]):
    """Write a list of dicts to a CSV file."""
    def escape(val: str) -> str:
        val = str(val).replace('"', '""')
        if "," in val or '"' in val or "\n" in val:
            return f'"{val}"'
        return val

    lines = [",".join(columns)]
    for row in rows:
        lines.append(",".join(escape(row.get(c, "")) for c in columns))

    Path(filepath).write_text("\n".join(lines), encoding="utf-8")


# ─── Main ───────────────────────────────────────────────────────────

def main():
    print(f"\n=== Dependency Mapper (Python) ===")
    print(f"Scan root: {SCAN_ROOT}")
    print(f"Output:    {OUT_DIR}\n")

    # Step 0: Discover repos
    print("Step 0: Discovering repositories...")
    repos = discover_repos(SCAN_ROOT)
    print(f"  Found {len(repos)} repo(s):")
    for r in repos:
        sln_info = f" ({len(r['solutions'])} .sln)" if r["solutions"] else ""
        print(f"    - {r['name']}{sln_info}: {r['root']}")

    Path(os.path.join(OUT_DIR, "repos.json")).write_text(
        json.dumps(repos, indent=2), encoding="utf-8"
    )

    # Step 1 & 2: Extract dependencies from each repo
    print("\nStep 1: Extracting NuGet dependencies and project references...")
    all_package_deps = []
    all_project_refs = []
    all_project_meta = []

    for repo in repos:
        result = extract_dependencies_from_repo(repo, SCAN_ROOT)
        all_package_deps.extend(result["package_deps"])
        all_project_refs.extend(result["project_refs"])
        all_project_meta.extend(result["project_meta"])
        pm = result["project_meta"]
        pd = result["package_deps"]
        pr = result["project_refs"]
        print(f"  {repo['name']}: {len(pm)} projects, {len(pd)} NuGet refs, {len(pr)} project refs")

    print(f"  Total: {len(all_package_deps)} NuGet refs, {len(all_project_refs)} project refs across {len(all_project_meta)} projects")

    write_csv(
        os.path.join(OUT_DIR, "dependencies.csv"),
        all_package_deps,
        ["repo", "project", "package", "version"],
    )
    write_csv(
        os.path.join(OUT_DIR, "project-refs.csv"),
        all_project_refs,
        ["repo", "project", "references", "referencePath", "crossRepo"],
    )
    Path(os.path.join(OUT_DIR, "project-meta.json")).write_text(
        json.dumps(all_project_meta, indent=2), encoding="utf-8"
    )

    # Step 3: Discover data access patterns
    print("\nStep 2: Discovering data access patterns...")
    data_findings = discover_data_patterns(SCAN_ROOT, repos)
    print(f"  Found {len(data_findings)} data access pattern matches")

    type_summary: dict[str, int] = {}
    for f in data_findings:
        type_summary[f["pattern"]] = type_summary.get(f["pattern"], 0) + 1

    for pat, count in sorted(type_summary.items(), key=lambda x: -x[1])[:15]:
        print(f"    {pat}: {count}")
    if len(type_summary) > 15:
        print(f"    ... and {len(type_summary) - 15} more patterns")

    Path(os.path.join(OUT_DIR, "data-sources.json")).write_text(
        json.dumps(data_findings, indent=2), encoding="utf-8"
    )

    # Step 4: Extract configs
    print("\nStep 3: Extracting configuration files...")
    configs = extract_configs(SCAN_ROOT, repos)
    print(f"  Found {len(configs)} configuration files")

    for c in configs:
        conn = c.get("connectionStrings", {})
        if conn:
            print(f"    {c['file']}: {', '.join(conn.keys())}")

    Path(os.path.join(OUT_DIR, "configs.json")).write_text(
        json.dumps(configs, indent=2), encoding="utf-8"
    )

    # Step 5: Build graph
    print("\nStep 4: Building dependency graph...")
    graph = build_graph(all_package_deps, all_project_refs, all_project_meta, data_findings, configs)
    Path(os.path.join(OUT_DIR, "graph.json")).write_text(
        json.dumps(graph, indent=2), encoding="utf-8"
    )
    print(f"  Graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")

    if graph["summary"]["totalRepos"] > 1:
        print(f"  Repos: {graph['summary']['totalRepos']}")
        for repo_name, info in graph["summary"]["repos"].items():
            print(f"    {repo_name}: {info['projects']} projects — {json.dumps(info['categories'])}")

    print(f"  Categories: {json.dumps(graph['summary']['categories'])}")
    if graph["summary"]["totalCrossRepoRefs"] > 0:
        print(f"  Cross-repo references: {graph['summary']['totalCrossRepoRefs']}")

    print("\n=== Analysis complete ===\n")


if __name__ == "__main__":
    main()
