#!/usr/bin/env python3
"""
Dependency Mapper — Static Analysis Engine (Python)

Modes:
  python 1_scan_projects.py /path/to/single-repo
  python 1_scan_projects.py /path/to/parent-dir    (auto-discovers repos by .sln/.git)

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
import platform
import re
import sys
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────

SCAN_ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT_DIR = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "output")

os.makedirs(OUT_DIR, exist_ok=True)

_IS_WINDOWS = platform.system() == "Windows"
_MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB — skip files larger than this
_MAX_SCAN_DEPTH = 30  # max directory nesting depth


def safe_read_text(filepath: str, max_size: int = _MAX_FILE_SIZE) -> str | None:
    """Read a text file, returning None if too large or unreadable.

    Applies long-path normalisation on Windows and skips files exceeding
    *max_size* to prevent memory issues on very large repos.
    """
    norm_path = _fs_path(filepath)
    try:
        sz = Path(norm_path).stat().st_size
        if sz > max_size:
            return None
    except OSError:
        return None
    try:
        return Path(norm_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


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


# ─── Path normalisation (Windows compat) ────────────────────────────

def _strip_long_prefix(p: str) -> str:
    """Strip the Windows ``\\\\?\\`` extended-length prefix."""
    if p.startswith("\\\\?\\UNC\\"):
        return "\\\\" + p[8:]  # \\?\UNC\server\share → \\server\share
    if p.startswith("\\\\?\\"):
        return p[4:]           # \\?\C:\foo → C:\foo
    return p


def _fs_path(p: str) -> str:
    """Return a path suitable for filesystem I/O (scandir, stat, read).

    On Windows, adds the ``\\\\?\\`` extended-length prefix for paths
    that exceed the legacy 260-char MAX_PATH limit.  The prefix is
    *only* needed for direct OS calls — never for relpath / comparisons.
    """
    if sys.platform == "win32":
        abs_p = os.path.abspath(p)
        if len(abs_p) >= 260 and not abs_p.startswith("\\\\?\\"):
            if abs_p.startswith("\\\\"):
                return "\\\\?\\UNC\\" + abs_p[2:]  # \\server\share → \\?\UNC\server\share
            return "\\\\?\\" + abs_p
    return os.path.normpath(p) if p else p


def _normalize_path(p: str) -> str:
    """Return a clean, absolute, normalised path (no ``\\\\?\\`` prefix).

    Safe for relpath, comparisons, and storage.  Filesystem helpers
    like ``safe_read_text`` and ``find_files`` call ``_fs_path``
    internally when they need the long-path prefix.
    """
    if not p:
        return p
    cleaned = _strip_long_prefix(p)
    if os.path.isabs(cleaned):
        return os.path.normpath(cleaned)
    return os.path.normpath(os.path.abspath(cleaned))


def _relpath(path: str, start: str) -> str:
    """Compute os.path.relpath after stripping any ``\\\\?\\`` prefixes.

    Also normalises both sides with os.path.normcase so that drive
    letter case (``C:`` vs ``c:``) and separator style never cause a
    cross-mount ValueError on Windows.
    """
    clean_path = _strip_long_prefix(os.path.normpath(path))
    clean_start = _strip_long_prefix(os.path.normpath(start))
    try:
        return os.path.relpath(clean_path, clean_start)
    except ValueError:
        return clean_path


# ─── Find all files recursively ─────────────────────────────────────

SKIP_DIRS = {".git", "node_modules", "bin", "obj", ".vs", ".idea", "packages",
              "TestResults", "artifacts", "__pycache__", ".nuget"}


def find_files(
    directory: str,
    pattern: re.Pattern,
    results: list | None = None,
    _depth: int = 0,
) -> list[str]:
    """Recursively find files matching a regex pattern on the filename.

    Returns clean paths (no ``\\\\?\\`` prefix) that are safe for
    relpath comparisons.  Uses ``_fs_path`` internally for scandir
    to handle Windows long-path limits.

    Respects *_MAX_SCAN_DEPTH* to avoid excessively deep trees (common on
    Windows where junction/symlink loops and deeply nested ``node_modules``
    can cause MAX_PATH errors).
    """
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
        # Clean path for storage/comparison; _fs_path used only for scandir
        full = _normalize_path(entry.path)
        try:
            is_dir = entry.is_dir(follow_symlinks=False)
        except OSError:
            continue

        if is_dir:
            if entry.name in SKIP_DIRS:
                continue
            find_files(full, pattern, results, _depth + 1)
        elif pattern.search(entry.name):
            results.append(full)

    return results


# ─── Auto-discover repos ────────────────────────────────────────────

def discover_repos(scan_root: str) -> list[dict]:
    """Discover .NET repositories under scan_root."""
    scan_root = _normalize_path(scan_root)
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
        sub_dir = _normalize_path(os.path.join(scan_root, entry_name))
        try:
            if not os.path.isdir(sub_dir):
                continue
        except OSError:
            continue

        sub_csproj = find_files(sub_dir, re.compile(r"\.csproj$"))
        if not sub_csproj:
            continue

        sub_slns = [os.path.normpath(_relpath(s, sub_dir)) for s in find_files(sub_dir, re.compile(r"\.sln$"))]

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
        if len(os.path.normpath(_relpath(f, repo_root)).split(os.sep)) <= 2
    ]

    skip_tags = {"PropertyGroup", "Condition", "Project", "Import", "ItemGroup"}

    for pf in props_files:
        xml = safe_read_text(pf)
        if xml is None:
            continue
        for m in re.finditer(r"<(\w+)>([^<]+)</\1>", xml):
            tag_name, tag_val = m.group(1), m.group(2)
            if tag_name not in skip_tags and tag_name not in props:
                props[tag_name] = tag_val

    # Also look for Directory.Build.props / Directory.Packages.props
    for name in ("Directory.Build.props", "Directory.Packages.props"):
        dbp = os.path.join(repo_root, name)
        if os.path.isfile(dbp):
            xml = safe_read_text(dbp)
            if xml is None:
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

        import_path = import_path.replace("$(RepoGitHubPath)", repo_root + os.sep)
        import_path = import_path.replace("$(MSBuildThisFileDirectory)", file_dir + os.sep)
        import_path = import_path.replace("\\", os.sep).replace("/", os.sep)

        resolved = os.path.normpath(os.path.join(file_dir, import_path))
        if resolved in visited or not os.path.isfile(resolved):
            continue
        visited.add(resolved)

        props_xml = safe_read_text(resolved)
        if props_xml is None:
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
                ref_path = ref_path.replace("$(RepoGitHubPath)", repo_root + os.sep)
                ref_path = ref_path.replace("\\", os.sep).replace("/", os.sep)
                all_project_refs.append({"raw_path": ref_path, "resolve_from": props_dir})

    return {"package_refs": all_package_refs, "project_refs": all_project_refs}


# ─── Extract dependencies from a single repo ───────────────────────

def extract_dependencies_from_repo(repo: dict, global_scan_root: str) -> dict:
    """Extract all dependencies from a single repo."""
    repo_root = repo["root"]
    props = load_properties(repo_root)
    csproj_files = find_files(repo_root, re.compile(r"\.csproj$"))
    abs_root = _normalize_path(repo_root)

    package_deps = []
    project_refs = []
    project_meta = []

    for csproj_path in csproj_files:
        xml = safe_read_text(csproj_path)
        if xml is None:
            continue

        csproj_dir = os.path.dirname(csproj_path)
        proj_name = os.path.splitext(os.path.basename(csproj_path))[0]
        rel_path = _relpath(csproj_path, abs_root)
        global_rel_path = _relpath(csproj_path, global_scan_root)

        category = categorize_project(rel_path, proj_name, xml)

        # Extract target framework (check csproj first, then resolve $(Var) from props)
        tf_match = re.search(r'<TargetFramework(?:s)?>(.*?)</TargetFramework(?:s)?>', xml)
        target_framework = tf_match.group(1) if tf_match else "unknown"
        # Resolve property references like $(StockSharpTargets)
        if target_framework != "unknown":
            tf_var = re.match(r'^\$\((\w+)\)$', target_framework)
            if tf_var:
                target_framework = props.get(tf_var.group(1), target_framework)
        # Fallback: check props for TargetFramework/TargetFrameworks
        if target_framework == "unknown":
            target_framework = props.get("TargetFrameworks", props.get("TargetFramework", "unknown"))

        project_meta.append({
            "project": proj_name,
            "repo": repo["name"],
            "path": rel_path,
            "globalPath": global_rel_path,
            "category": category,
            "targetFramework": target_framework,
        })

        # Resolve inherited deps from .props imports
        inherited = resolve_imports(xml, csproj_dir, abs_root)

        # Direct PackageReferences
        direct_pkgs = parse_xml_elements(xml, "PackageReference")
        all_pkgs = inherited["package_refs"] + [
            {"name": p["attrs"].get("Include", ""), "version": p["attrs"].get("Version", "")}
            for p in direct_pkgs
        ]

        # Also check for packages.config (legacy NuGet format)
        pkgs_config_path = os.path.join(csproj_dir, "packages.config")
        pkgs_config_xml = safe_read_text(pkgs_config_path)
        uses_packages_config = False
        if pkgs_config_xml:
            uses_packages_config = True
            for pc in parse_xml_elements(pkgs_config_xml, "package"):
                pkg_id = pc["attrs"].get("id", "")
                if pkg_id:
                    all_pkgs.append({"name": pkg_id, "version": pc["attrs"].get("version", "")})

        # Record NuGet format in project meta
        project_meta[-1]["nugetFormat"] = "packages.config" if uses_packages_config else "PackageReference"

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
            p = p.replace("$(RepoGitHubPath)", abs_root + os.sep)
            p = p.replace("\\", os.sep).replace("/", os.sep)
            resolved = os.path.normpath(os.path.join(csproj_dir, p))
            all_refs.append(resolved)

        for resolved_ref in all_refs:
            if not resolved_ref:
                continue
            ref_name = os.path.splitext(os.path.basename(resolved_ref))[0]
            ref_rel_path = _relpath(resolved_ref, abs_root)
            ref_global_path = _relpath(resolved_ref, global_scan_root)
            resolved_ref_norm = os.path.normcase(_normalize_path(resolved_ref))
            abs_root_norm = os.path.normcase(abs_root)
            try:
                is_in_same_repo = os.path.commonpath([resolved_ref_norm, abs_root_norm]) == abs_root_norm
            except ValueError:
                # Different drives or otherwise incomparable paths are not in the same repo
                is_in_same_repo = False
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
    rp = rel_path.replace("\\", "/").lower()
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


# ─── Test project scanning ───────────────────────────────────────────

_TEST_METHOD_ATTRS = re.compile(
    r"^\s*\[(?:Test|TestMethod|Fact|Theory|TestCase)\b", re.MULTILINE
)
_TEST_CLASS_ATTRS = re.compile(
    r"^\s*\[(?:TestFixture|TestClass)\b", re.MULTILINE
)
_TEST_FRAMEWORK_PATTERNS = {
    "xUnit": re.compile(r"\b(?:global\s+)?using\s+Xunit\b"),
    "NUnit": re.compile(r"\b(?:global\s+)?using\s+NUnit\b"),
    "MSTest": re.compile(r"\b(?:global\s+)?using\s+Microsoft\.VisualStudio\.TestTools\b"),
}
# Fallback: detect framework from .csproj / .props PackageReference or Sdk includes
_CSPROJ_FRAMEWORK_PATTERNS = {
    "xUnit": re.compile(r"(?:xunit|xUnit)", re.IGNORECASE),
    "NUnit": re.compile(r"(?:NUnit)", re.IGNORECASE),
    "MSTest": re.compile(r"(?:MSTest|Microsoft\.NET\.Test\.Sdk)", re.IGNORECASE),
}


def scan_test_projects(
    all_project_meta: list[dict],
    all_project_refs: list[dict],
    scan_root: str,
    repos: list[dict],
) -> dict:
    """Scan test projects to count test methods/classes and determine coverage.

    Returns a dict suitable for writing to test-projects.json.
    """
    # Build category lookup
    cat_by_name = {pm["project"]: pm.get("category", "") for pm in all_project_meta}
    repo_by_name = {pm["project"]: pm.get("repo", "") for pm in all_project_meta}

    # Build project reference graph for coverage mapping
    # test_project → set of referenced projects
    test_refs: dict[str, set[str]] = {}
    for pr in all_project_refs:
        test_refs.setdefault(pr["project"], set()).add(pr["references"])

    # Build repo root lookup
    repo_roots = {r["name"]: r["root"] for r in repos}

    test_projects = []

    for pm in all_project_meta:
        proj_name = pm["project"]
        category = pm.get("category", "")
        repo_name = pm.get("repo", "")
        repo_root = repo_roots.get(repo_name, scan_root)
        # Use path (relative to repo root) preferably, globalPath is relative to scan_root
        proj_path = pm.get("path", "")
        if not proj_path:
            proj_path = pm.get("globalPath", "")

        if not proj_path:
            continue

        # Resolve full path to project directory
        if os.path.isabs(proj_path):
            proj_dir = os.path.dirname(proj_path)
        else:
            # Try relative to repo root first, fall back to scan root
            candidate = os.path.join(repo_root, proj_path)
            if not os.path.exists(candidate):
                candidate = os.path.join(scan_root, proj_path)
            proj_dir = os.path.dirname(candidate)

        if not os.path.isdir(proj_dir):
            continue

        # Only scan projects categorized as Test, or non-test projects
        # with Test-like .cs files (inline tests)
        is_test_category = category.lower() == "test"

        test_method_count = 0
        test_class_count = 0
        frameworks_found: set[str] = set()
        test_files: list[str] = []

        # Walk .cs files in project directory
        for root, dirs, files in os.walk(proj_dir):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in ("bin", "obj", "node_modules", "packages", ".git")]
            depth = root.replace(proj_dir, "").count(os.sep)
            if depth > 15:
                dirs.clear()
                continue

            for fname in files:
                if not fname.endswith(".cs"):
                    continue
                fpath = os.path.join(root, fname)
                content = safe_read_text(fpath)
                if not content:
                    continue

                # Check for framework using directives in all .cs files
                for fw_name, fw_pat in _TEST_FRAMEWORK_PATTERNS.items():
                    if fw_pat.search(content):
                        frameworks_found.add(fw_name)

                methods = len(_TEST_METHOD_ATTRS.findall(content))
                classes = len(_TEST_CLASS_ATTRS.findall(content))

                if methods > 0 or classes > 0:
                    test_method_count += methods
                    test_class_count += classes
                    rel_path = _relpath(fpath, repo_root)
                    test_files.append(rel_path)

        # Fallback: detect framework from .csproj and imported .props files
        if not frameworks_found and (is_test_category or test_method_count > 0):
            csproj_file = os.path.join(repo_root, proj_path) if not os.path.isabs(proj_path) else proj_path
            if not os.path.isfile(csproj_file):
                csproj_file = os.path.join(scan_root, proj_path)
            files_to_check = [csproj_file]
            csproj_content = safe_read_text(csproj_file) or ""
            # Find imported .props files
            for imp_match in re.finditer(r'<Import\s+Project="([^"]+)"', csproj_content):
                props_rel = imp_match.group(1).replace("\\", "/")
                props_path = os.path.normpath(os.path.join(os.path.dirname(csproj_file), props_rel))
                if os.path.isfile(props_path):
                    files_to_check.append(props_path)
            for check_file in files_to_check:
                check_content = safe_read_text(check_file) or "" if check_file != csproj_file else csproj_content
                for fw_name, fw_pat in _CSPROJ_FRAMEWORK_PATTERNS.items():
                    if fw_pat.search(check_content):
                        frameworks_found.add(fw_name)

        if is_test_category or test_method_count > 0:
            fw_list = sorted(frameworks_found)
            test_projects.append({
                "project": proj_name,
                "repo": repo_name,
                "category": category,
                "testFramework": fw_list[0] if fw_list else "unknown",
                "testFrameworks": fw_list,
                "testClassCount": test_class_count,
                "testMethodCount": test_method_count,
                "testFileCount": len(test_files),
                "files": test_files[:20],  # cap for output size
                "covers": sorted(test_refs.get(proj_name, set())),
            })

    # Build coverage map: which non-test projects are covered by test projects
    coverage: dict[str, dict] = {}
    for tp in test_projects:
        for covered_proj in tp.get("covers", []):
            if cat_by_name.get(covered_proj, "").lower() == "test":
                continue  # don't count test→test as coverage
            if covered_proj not in coverage or tp["testMethodCount"] > coverage[covered_proj].get("testMethodCount", 0):
                coverage[covered_proj] = {
                    "testProject": tp["project"],
                    "testFramework": tp["testFramework"],
                    "testMethodCount": tp["testMethodCount"],
                }

    # Find uncovered non-test projects
    non_test_projects = [pm["project"] for pm in all_project_meta
                         if pm.get("category", "").lower() != "test"]
    uncovered = sorted(p for p in non_test_projects if p not in coverage)

    total_test_methods = sum(tp["testMethodCount"] for tp in test_projects)
    total_test_classes = sum(tp["testClassCount"] for tp in test_projects)
    covered_count = len(coverage)

    return {
        "testProjects": test_projects,
        "coverage": coverage,
        "uncoveredProjects": uncovered,
        "summary": {
            "totalTestProjects": len(test_projects),
            "totalTestMethods": total_test_methods,
            "totalTestClasses": total_test_classes,
            "coveredProjects": covered_count,
            "uncoveredProjects": len(uncovered),
            "coverageRatio": f"{covered_count}/{len(non_test_projects)}" if non_test_projects else "0/0",
        },
    }


# ─── Project resolution for .cs files ────────────────────────────────

def build_file_to_project_map(project_meta: list[dict], repo_root: str) -> dict[str, str]:
    """Map csproj directory paths → project names for a repo.

    Keys are normalised with ``os.path.normcase`` so lookups are
    case-insensitive on Windows.
    """
    dir_to_project: dict[str, str] = {}
    abs_root = _normalize_path(repo_root)
    for pm in project_meta:
        csproj_path = os.path.join(abs_root, pm["path"])
        csproj_dir = os.path.normcase(os.path.dirname(_normalize_path(csproj_path)))
        dir_to_project[csproj_dir] = pm["project"]
    return dir_to_project


def resolve_project_for_file(filepath: str, dir_to_project: dict[str, str]) -> str | None:
    """Walk up directory tree to find owning project for a source file."""
    d = os.path.normcase(os.path.dirname(_normalize_path(filepath)))
    for _ in range(20):  # safety limit
        if d in dir_to_project:
            return dir_to_project[d]
        parent = os.path.normcase(os.path.dirname(d))
        if parent == d:
            break
        d = parent
    return None


# ─── Enhanced data access pattern discovery ──────────────────────────

# Direction values: "read", "write", "both", "expose", "consume", None
# endpoint_group: index of regex capture group containing the endpoint name (0 = no endpoint)
# endpoint_type: "table", "entity", "topic", "queue", "exchange", "route", "collection", "url", None

ENHANCED_DATA_PATTERNS = [
    # ── Database: SQL ──
    {"name": "SQL.Select",       "regex": re.compile(r"\bSELECT\b.+?\bFROM\s+\[?(\w{2,})\]?", re.IGNORECASE), "type": "database", "direction": "read",  "endpoint_group": 1, "endpoint_type": "table", "confidence": "high"},
    {"name": "SQL.Insert",       "regex": re.compile(r"\bINSERT\s+INTO\s+\[?(\w{2,})\]?", re.IGNORECASE),    "type": "database", "direction": "write", "endpoint_group": 1, "endpoint_type": "table", "confidence": "high"},
    {"name": "SQL.Update",       "regex": re.compile(r"\bUPDATE\s+\[?(\w{2,})\]?\s+SET\b", re.IGNORECASE),   "type": "database", "direction": "write", "endpoint_group": 1, "endpoint_type": "table", "confidence": "high"},
    {"name": "SQL.Delete",       "regex": re.compile(r"\bDELETE\s+FROM\s+\[?(\w{2,})\]?", re.IGNORECASE),    "type": "database", "direction": "write", "endpoint_group": 1, "endpoint_type": "table", "confidence": "high"},
    {"name": "SQL.CreateTable",  "regex": re.compile(r"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?\[?(\w{2,})\]?", re.IGNORECASE), "type": "database", "direction": "write", "endpoint_group": 1, "endpoint_type": "table", "confidence": "high"},

    # ── Database: EF / DbContext ──
    {"name": "DbContext",        "regex": re.compile(r":\s*DbContext\b"),                                    "type": "database", "direction": "both",  "endpoint_group": 0, "endpoint_type": None,    "confidence": "high"},
    {"name": "DbSet",            "regex": re.compile(r"DbSet<(\w+)>"),                                      "type": "database", "direction": "both",  "endpoint_group": 1, "endpoint_type": "entity", "confidence": "high"},
    {"name": "EntityFramework",  "regex": re.compile(r"\.UseSqlServer\(|\.UseNpgsql\(|\.UseSqlite\(|\.UseMySql\("), "type": "database", "direction": "both", "endpoint_group": 0, "endpoint_type": None, "confidence": "high"},
    {"name": "SqlConnection",    "regex": re.compile(r"new\s+SqlConnection\s*\("),                           "type": "database", "direction": "both",  "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},
    {"name": "SqlClient",        "regex": re.compile(r"Microsoft\.Data\.SqlClient|System\.Data\.SqlClient"), "type": "database", "direction": "both",  "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},

    # ── Database: Dapper ──
    {"name": "Dapper.Query",     "regex": re.compile(r"\.(Query|QueryAsync|QueryFirst|QuerySingle|QueryMultiple)\s*[<(]"), "type": "database", "direction": "read",  "endpoint_group": 0, "endpoint_type": None, "confidence": "high"},
    {"name": "Dapper.Execute",   "regex": re.compile(r"\.(Execute|ExecuteAsync|ExecuteScalar|ExecuteScalarAsync)\s*[<(]"), "type": "database", "direction": "write", "endpoint_group": 0, "endpoint_type": None, "confidence": "high"},

    # ── Database: MongoDB ──
    {"name": "MongoDB.Read",     "regex": re.compile(r"\.(Find|FindAsync|Aggregate|AggregateAsync|CountDocuments)\s*[<(]"), "type": "database", "direction": "read",  "endpoint_group": 0, "endpoint_type": None, "confidence": "medium"},
    {"name": "MongoDB.Write",    "regex": re.compile(r"\.(InsertOne|InsertMany|ReplaceOne|UpdateOne|UpdateMany|DeleteOne|DeleteMany)\s*[<(]"), "type": "database", "direction": "write", "endpoint_group": 0, "endpoint_type": None, "confidence": "medium"},
    {"name": "MongoDB.Collection", "regex": re.compile(r'GetCollection<(\w+)>\s*\(\s*"([^"]+)"'),           "type": "database", "direction": "both",  "endpoint_group": 2, "endpoint_type": "collection", "confidence": "high"},
    {"name": "MongoDB",          "regex": re.compile(r"MongoDB\.Driver|IMongoClient|IMongoDatabase"),       "type": "database", "direction": "both",  "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},

    # ── Messaging: Kafka ──
    {"name": "Kafka.Producer",   "regex": re.compile(r"IProducer\b|ProducerBuilder|\.Produce\s*\(|\.ProduceAsync\s*\("), "type": "messaging", "direction": "write", "endpoint_group": 0, "endpoint_type": None, "confidence": "high"},
    {"name": "Kafka.Consumer",   "regex": re.compile(r"IConsumer\b|ConsumerBuilder|\.Consume\s*\(|\.Subscribe\s*\("),    "type": "messaging", "direction": "read",  "endpoint_group": 0, "endpoint_type": None, "confidence": "high"},
    {"name": "Kafka.Topic",      "regex": re.compile(r'(?:Topic|topic|TopicName|topicName|Subscribe|Produce)\w*\s*[\(=:]\s*["\']([a-zA-Z][\w.-]+)["\']'), "type": "messaging", "direction": None, "endpoint_group": 1, "endpoint_type": "topic", "confidence": "medium"},
    {"name": "Kafka",            "regex": re.compile(r"Confluent\.Kafka"),                                   "type": "messaging", "direction": None,   "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},

    # ── Messaging: RabbitMQ ──
    {"name": "RabbitMQ.Publish",  "regex": re.compile(r"BasicPublish\s*\(|\.Publish\s*\(.*IModel"),          "type": "messaging", "direction": "write", "endpoint_group": 0, "endpoint_type": None,    "confidence": "high"},
    {"name": "RabbitMQ.Consume",  "regex": re.compile(r"BasicConsume\s*\(|\.Consume\s*\(.*IModel"),          "type": "messaging", "direction": "read",  "endpoint_group": 0, "endpoint_type": None,    "confidence": "high"},
    {"name": "RabbitMQ.Queue",    "regex": re.compile(r'QueueDeclare\s*\(\s*(?:queue:\s*)?"([^"]+)"'),       "type": "messaging", "direction": None,    "endpoint_group": 1, "endpoint_type": "queue",    "confidence": "high"},
    {"name": "RabbitMQ.Exchange", "regex": re.compile(r'ExchangeDeclare\s*\(\s*(?:exchange:\s*)?"([^"]+)"'), "type": "messaging", "direction": None,    "endpoint_group": 1, "endpoint_type": "exchange", "confidence": "high"},
    {"name": "RabbitMQ",         "regex": re.compile(r"RabbitMQ\.Client|IConnection.*RabbitMQ"),             "type": "messaging", "direction": None,    "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},

    # ── API: ASP.NET attributes / Minimal API ──
    {"name": "API.HttpGet",      "regex": re.compile(r'\[HttpGet\s*\(\s*"([^"]*)"\s*\)\]'),                  "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.HttpPost",     "regex": re.compile(r'\[HttpPost\s*\(\s*"([^"]*)"\s*\)\]'),                 "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.HttpPut",      "regex": re.compile(r'\[HttpPut\s*\(\s*"([^"]*)"\s*\)\]'),                  "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.HttpDelete",   "regex": re.compile(r'\[HttpDelete\s*\(\s*"([^"]*)"\s*\)\]'),               "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.HttpGet",      "regex": re.compile(r'\[HttpGet\]'),                                        "type": "api", "direction": "expose", "endpoint_group": 0, "endpoint_type": None,    "confidence": "high"},
    {"name": "API.HttpPost",     "regex": re.compile(r'\[HttpPost\]'),                                       "type": "api", "direction": "expose", "endpoint_group": 0, "endpoint_type": None,    "confidence": "high"},
    {"name": "API.HttpPut",      "regex": re.compile(r'\[HttpPut\]'),                                        "type": "api", "direction": "expose", "endpoint_group": 0, "endpoint_type": None,    "confidence": "high"},
    {"name": "API.HttpDelete",   "regex": re.compile(r'\[HttpDelete\]'),                                     "type": "api", "direction": "expose", "endpoint_group": 0, "endpoint_type": None,    "confidence": "high"},
    {"name": "API.Route",        "regex": re.compile(r'\[Route\s*\(\s*"([^"]*)"\s*\)\]'),                    "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.Controller",   "regex": re.compile(r":\s*(Controller|ControllerBase|ApiController)\b"),    "type": "api", "direction": "expose", "endpoint_group": 0, "endpoint_type": None,    "confidence": "high"},
    {"name": "API.MapGet",       "regex": re.compile(r'\.MapGet\s*\(\s*"([^"]*)"'),                          "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.MapPost",      "regex": re.compile(r'\.MapPost\s*\(\s*"([^"]*)"'),                         "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.MapPut",       "regex": re.compile(r'\.MapPut\s*\(\s*"([^"]*)"'),                          "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.MapDelete",    "regex": re.compile(r'\.MapDelete\s*\(\s*"([^"]*)"'),                       "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},
    {"name": "API.MapGroup",     "regex": re.compile(r'\.MapGroup\s*\(\s*"([^"]*)"'),                        "type": "api", "direction": "expose", "endpoint_group": 1, "endpoint_type": "route", "confidence": "high"},

    # ── API: gRPC ──
    {"name": "gRPC.Server",      "regex": re.compile(r"\.MapGrpcService<|ServerServiceDefinition|:\s*\w+Base\b.*ServerCallContext|ServerCallContext"), "type": "api", "direction": "expose", "endpoint_group": 0, "endpoint_type": None, "confidence": "high"},
    {"name": "gRPC.Client",      "regex": re.compile(r"GrpcChannel\.ForAddress|new\s+\w+\.?\w*Client\s*\(.*GrpcChannel|\.CreateGrpcService<"), "type": "api", "direction": "consume", "endpoint_group": 0, "endpoint_type": None, "confidence": "high"},
    {"name": "gRPC",             "regex": re.compile(r"Grpc\.Core|Grpc\.Net\.Client|Google\.Protobuf"),      "type": "api", "direction": None,      "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},

    # ── API: HTTP client (consuming APIs) ──
    {"name": "HttpClient.GetAsync",    "regex": re.compile(r'\.(GetAsync|GetStringAsync|GetStreamAsync)\s*\(\s*"([^"]*)"'), "type": "api", "direction": "consume", "endpoint_group": 2, "endpoint_type": "url", "confidence": "medium"},
    {"name": "HttpClient.PostAsync",   "regex": re.compile(r'\.(PostAsync|PostAsJsonAsync)\s*\(\s*"([^"]*)"'),              "type": "api", "direction": "consume", "endpoint_group": 2, "endpoint_type": "url", "confidence": "medium"},
    {"name": "HttpClient.PutAsync",    "regex": re.compile(r'\.(PutAsync|PutAsJsonAsync)\s*\(\s*"([^"]*)"'),                "type": "api", "direction": "consume", "endpoint_group": 2, "endpoint_type": "url", "confidence": "medium"},
    {"name": "HttpClient.DeleteAsync", "regex": re.compile(r'\.DeleteAsync\s*\(\s*"([^"]*)"'),                              "type": "api", "direction": "consume", "endpoint_group": 1, "endpoint_type": "url", "confidence": "medium"},
    {"name": "HttpClient.Injection",   "regex": re.compile(r"AddHttpClient[<(]"),                            "type": "api", "direction": "consume", "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},
    {"name": "HttpClient.New",         "regex": re.compile(r"new\s+HttpClient\s*\("),                        "type": "api", "direction": "consume", "endpoint_group": 0, "endpoint_type": None,    "confidence": "low"},
    {"name": "HttpClient.BaseAddress", "regex": re.compile(r'BaseAddress\s*=\s*new\s+Uri\s*\(\s*"([^"]+)"'), "type": "api", "direction": "consume", "endpoint_group": 1, "endpoint_type": "url",   "confidence": "medium"},
    {"name": "WebSocket",             "regex": re.compile(r"ClientWebSocket|WebSocketClient"),               "type": "api", "direction": "consume", "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},

    # ── Cache: Redis ──
    {"name": "Redis.Read",       "regex": re.compile(r"\.(StringGet|HashGet|Get|GetAsync|KeyExists)\s*\("),  "type": "cache", "direction": "read",  "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},
    {"name": "Redis.Write",      "regex": re.compile(r"\.(StringSet|HashSet|Set|SetAsync|KeyDelete)\s*\("),  "type": "cache", "direction": "write", "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},
    {"name": "Redis",            "regex": re.compile(r"StackExchange\.Redis|IConnectionMultiplexer|RedisConnection"), "type": "cache", "direction": None, "endpoint_group": 0, "endpoint_type": None, "confidence": "medium"},

    # ── Storage: File ──
    {"name": "File.Read",        "regex": re.compile(r"File\.(ReadAll\w+|OpenRead|ReadLines)\b"),            "type": "storage", "direction": "read",  "endpoint_group": 0, "endpoint_type": None,    "confidence": "medium"},
    {"name": "File.Write",       "regex": re.compile(r"File\.(WriteAll\w+|Create|OpenWrite|AppendAll\w+)\b"), "type": "storage", "direction": "write", "endpoint_group": 0, "endpoint_type": None,   "confidence": "medium"},

    # ── Kept existing patterns with direction ──
    {"name": "ConnectionString", "regex": re.compile(r"[Cc]onnection[Ss]tring"),                             "type": "config",    "direction": None,   "endpoint_group": 0, "endpoint_type": None,    "confidence": "low"},
    {"name": "Repository",       "regex": re.compile(r"class\s+\w*Repository\w*\b"),                         "type": "pattern",   "direction": "both", "endpoint_group": 0, "endpoint_type": None,    "confidence": "low"},
    {"name": "DataAccess",       "regex": re.compile(r"class\s+\w*DataAccess\w*\b"),                         "type": "pattern",   "direction": "both", "endpoint_group": 0, "endpoint_type": None,    "confidence": "low"},
    {"name": "FTP",              "regex": re.compile(r"FtpClient|FluentFTP"),                                 "type": "datasource", "direction": "both", "endpoint_group": 0, "endpoint_type": None,   "confidence": "medium"},
    {"name": "IMessageAdapter",  "regex": re.compile(r":\s*IMessageAdapter\b|class\s+\w+Adapter\b"),         "type": "connector", "direction": "both", "endpoint_group": 0, "endpoint_type": None,    "confidence": "low"},

    # ── WPF / UI ──
    {"name": "WPF.Window",      "regex": re.compile(r":\s*(Window|UserControl)\b"),                         "type": "ui", "direction": "expose",  "endpoint_group": 0, "endpoint_type": None, "confidence": "high"},
    {"name": "WPF.Binding",     "regex": re.compile(r"\{Binding\s|DataContext\s*="),                        "type": "ui", "direction": "consume", "endpoint_group": 0, "endpoint_type": None, "confidence": "medium"},
    {"name": "WPF.ViewModel",   "regex": re.compile(r":\s*(ViewModelBase|ObservableObject)\b|:\s*INotifyPropertyChanged\b|ObservableCollection<"), "type": "ui", "direction": "both", "endpoint_group": 0, "endpoint_type": None, "confidence": "medium"},
]


_SQL_KEYWORDS = {
    "IF", "ELSE", "BEGIN", "END", "SET", "WHERE", "AND", "OR", "NOT", "NULL",
    "AS", "ON", "IN", "IS", "BY", "GO", "USE", "ALL", "ANY", "TOP", "INTO",
    "JOIN", "LEFT", "RIGHT", "INNER", "OUTER", "CROSS", "FULL", "CASE", "WHEN",
    "THEN", "HAVING", "GROUP", "ORDER", "UNION", "WITH", "FROM", "SELECT",
    "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "INDEX", "TABLE",
    "VIEW", "EXEC", "DECLARE", "RETURN", "EXISTS", "BETWEEN", "LIKE", "LIMIT",
    "OFFSET", "VALUES", "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "CONSTRAINT",
    # Common false positives from prose/comments in SQL string literals
    "THE", "TO", "IT", "AN", "AT", "OF", "CTE", "CTE1", "CTE2",
    "T1", "T2", "T3", "TP", "COLLECTION", "TEST", "RESULT",
}


# ─── Business layer classification ────────────────────────────────────

BUSINESS_LAYERS = ["Presentation", "Engine", "Service", "DataAccess", "Infrastructure", "Unclassified"]

# Name-based signals (weight 3)
_LAYER_NAME_PATTERNS: dict[str, list[re.Pattern]] = {
    "Presentation": [re.compile(r"screen|view|window|wpf|desktop|shell|ui\b|forms|display", re.IGNORECASE)],
    "Engine":       [re.compile(r"pricer|pricing|calc|engine|compute|math|algo|valuation|model|solver|analytics", re.IGNORECASE)],
    "Service":      [re.compile(r"service|server|host|worker|gateway|api\b|web\b|grpc|handler|middleware", re.IGNORECASE)],
    "DataAccess":   [re.compile(r"data|repo|repository|storage|persist|dal\b|context|migration|store\b", re.IGNORECASE)],
    "Infrastructure": [re.compile(r"infra|common|shared|util|helper|logging|config|core|framework|base|extension|diagnostic", re.IGNORECASE)],
}

# NuGet package signals (weight 2)
_LAYER_NUGET_PATTERNS: dict[str, list[re.Pattern]] = {
    "Presentation": [re.compile(r"WPF|Wpf|MAUI|Maui|Xamarin\.Forms|Avalonia|MaterialDesign|MahApps|Prism\.Wpf|Caliburn", re.IGNORECASE)],
    "Engine":       [re.compile(r"MathNet|Accord|QLNet|MathJS|NumSharp", re.IGNORECASE)],
    "DataAccess":   [re.compile(r"EntityFramework|Dapper|Npgsql|MySql|MongoDB\.Driver|StackExchange\.Redis|NHibernate|Marten", re.IGNORECASE)],
    "Service":      [re.compile(r"Grpc|Swashbuckle|MediatR|MassTransit|NServiceBus|Rebus", re.IGNORECASE)],
}

# Category boost signals (weight 1)
_CATEGORY_TO_LAYER: dict[str, str] = {
    "DesktopApp": "Presentation",
    "WebApp": "Service",
    "Service": "Service",
    "Connector": "Infrastructure",
    "Tool": "Infrastructure",
}

_CONFIDENCE_THRESHOLD = 0.15


def classify_business_layer(
    proj_name: str,
    category: str,
    xml: str,
    packages: list[str],
    data_roles: dict[str, int],
    project_dir: str,
) -> dict:
    """Score a project across all business layers and return the winning layer with confidence.

    Returns: {"layer": str, "confidence": float, "signals": list[str]}
    """
    scores: dict[str, float] = {layer: 0.0 for layer in BUSINESS_LAYERS if layer != "Unclassified"}
    signals: list[str] = []

    # Signal 1: Name patterns (weight 3)
    for layer, patterns in _LAYER_NAME_PATTERNS.items():
        for pat in patterns:
            if pat.search(proj_name):
                scores[layer] += 3
                signals.append(f"name:{layer}")
                break

    # Signal 2: WPF content in .csproj XML (weight 4)
    if "<UseWPF>true</UseWPF>" in xml or "<UseWPF>True</UseWPF>" in xml:
        scores["Presentation"] += 4
        signals.append("wpf:csproj")
    if "<UseWindowsForms>" in xml:
        scores["Presentation"] += 3
        signals.append("winforms:csproj")

    # Check for .xaml files in project directory
    if project_dir and os.path.isdir(project_dir):
        try:
            has_xaml = any(
                entry.name.endswith(".xaml")
                for entry in os.scandir(project_dir)
                if entry.is_file()
            )
            if has_xaml:
                scores["Presentation"] += 4
                signals.append("wpf:xaml")
        except OSError:
            pass

    # Signal 3: NuGet packages (weight 2)
    pkg_str = " ".join(packages)
    for layer, patterns in _LAYER_NUGET_PATTERNS.items():
        for pat in patterns:
            if pat.search(pkg_str):
                scores[layer] += 2
                signals.append(f"nuget:{layer}")
                break

    # Signal 4: Technical category boost (weight 1)
    mapped = _CATEGORY_TO_LAYER.get(category)
    if mapped:
        scores[mapped] += 1
        signals.append(f"category:{mapped}")

    # Signal 5: Data pattern roles (weight 1)
    if data_roles:
        write_count = data_roles.get("write", 0) + data_roles.get("both", 0)
        read_count = data_roles.get("read", 0) + data_roles.get("both", 0)
        expose_count = data_roles.get("expose", 0)
        consume_count = data_roles.get("consume", 0)
        ui_count = data_roles.get("ui", 0)

        if write_count > 0 or read_count > 0:
            scores["DataAccess"] += 1
            signals.append("data:DataAccess")
        if expose_count > 0:
            scores["Service"] += 1
            signals.append("data:Service")
        if ui_count > 0:
            scores["Presentation"] += 1
            signals.append("data:Presentation")

    # Pick winner
    sorted_layers = sorted(scores.items(), key=lambda x: -x[1])
    winner_score = sorted_layers[0][1]
    runner_up_score = sorted_layers[1][1] if len(sorted_layers) > 1 else 0

    if winner_score == 0:
        return {"layer": "Unclassified", "confidence": 0.0, "signals": signals}

    confidence = (winner_score - runner_up_score) / winner_score
    if confidence < _CONFIDENCE_THRESHOLD:
        return {"layer": "Unclassified", "confidence": confidence, "signals": signals}

    return {"layer": sorted_layers[0][0], "confidence": round(confidence, 2), "signals": signals}


def classify_all_projects(
    all_project_meta: list[dict],
    all_package_deps: list[dict],
    data_findings: list[dict],
    overrides: dict[str, str],
) -> dict[str, dict]:
    """Classify all projects into business layers.

    Returns: {project_name: {"layer": ..., "confidence": ..., "signals": [...]}}
    """
    # Build per-project package lists
    pkgs_by_project: dict[str, list[str]] = {}
    for pd in all_package_deps:
        pkgs_by_project.setdefault(pd["project"], []).append(pd["package"])

    # Build per-project data roles from findings
    roles_by_project: dict[str, dict[str, int]] = {}
    for f in data_findings:
        proj = f.get("project")
        if not proj:
            continue
        if proj not in roles_by_project:
            roles_by_project[proj] = {}
        direction = f.get("direction") or "unknown"
        ftype = f.get("type", "")
        # Count UI-type patterns separately
        if ftype == "ui":
            roles_by_project[proj]["ui"] = roles_by_project[proj].get("ui", 0) + 1
        else:
            roles_by_project[proj][direction] = roles_by_project[proj].get(direction, 0) + 1

    # Read csproj XML for each project (needed for WPF detection)
    result: dict[str, dict] = {}
    for pm in all_project_meta:
        proj_name = pm["project"]

        # Check overrides first
        if proj_name in overrides:
            override_layer = overrides[proj_name]
            if override_layer in BUSINESS_LAYERS:
                result[proj_name] = {"layer": override_layer, "confidence": 1.0, "signals": ["override"]}
                continue
            else:
                print(f"  Warning: Unknown layer '{override_layer}' for override '{proj_name}', using auto-detection")

        # Read .csproj XML for WPF detection
        csproj_path = os.path.join(SCAN_ROOT, pm.get("globalPath", pm["path"]))
        xml = safe_read_text(csproj_path) or ""

        project_dir = os.path.dirname(csproj_path)
        packages = pkgs_by_project.get(proj_name, [])
        data_roles = roles_by_project.get(proj_name, {})

        classification = classify_business_layer(
            proj_name, pm["category"], xml, packages, data_roles, project_dir
        )
        result[proj_name] = classification

    return result


def discover_data_patterns(scan_root: str, repos: list[dict], project_meta: list[dict] | None = None) -> list[dict]:
    """Scan .cs files for data access patterns with direction and endpoint extraction."""
    findings = []
    abs_root = _normalize_path(scan_root)

    for repo in repos:
        # Build project resolution map for this repo
        repo_meta = [pm for pm in (project_meta or []) if pm.get("repo") == repo["name"]]
        dir_to_project = build_file_to_project_map(repo_meta, repo["root"])

        cs_files = find_files(repo["root"], re.compile(r"\.cs$"))

        for cs_file in cs_files:
            content = safe_read_text(cs_file)
            if content is None:
                continue

            lines = content.splitlines()
            rel_path = _relpath(cs_file, abs_root)
            project_name = resolve_project_for_file(cs_file, dir_to_project)

            for pat in ENHANCED_DATA_PATTERNS:
                for i, line in enumerate(lines):
                    match = pat["regex"].search(line)
                    if match:
                        # Extract endpoint name from capture group
                        endpoint = None
                        eg = pat["endpoint_group"]
                        if eg and eg > 0:
                            try:
                                endpoint = match.group(eg)
                            except IndexError:
                                pass
                            # Filter out SQL keywords and short names as table names
                            if endpoint and pat["endpoint_type"] == "table":
                                if len(endpoint) <= 3 or endpoint.upper() in _SQL_KEYWORDS:
                                    endpoint = None

                        finding = {
                            "file": rel_path,
                            "repo": repo["name"],
                            "line": i + 1,
                            "pattern": pat["name"],
                            "type": pat["type"],
                            "match": match.group(0)[:120],
                            "context": line.strip()[:200],
                            # New fields (additive)
                            "project": project_name,
                            "direction": pat["direction"],
                            "confidence": pat["confidence"],
                        }
                        if endpoint:
                            finding["endpoint"] = endpoint
                            finding["endpointType"] = pat["endpoint_type"]

                        findings.append(finding)

    return findings


# ─── Field-level traceability: XAML → ViewModel → Entity → DB column ──

# XAML regex patterns
_XAML_CLASS_RE        = re.compile(r'x:Class="(?:[\w.]+\.)?(\w+)"')
_XAML_BINDING_PATH_RE = re.compile(r'\{Binding\s+(?:Path=)?(\w[\w.]*)')
_XAML_BINDING_FULL_RE = re.compile(r'\{Binding\s+([^}]+)\}')
_XAML_DATA_CONTEXT_RE = re.compile(r'DataContext\s*=\s*"\{[^}]*?(?:Type|local:|vm:)(\w+)')
_XAML_DESIGN_CTX_RE   = re.compile(r'd:DataContext\s*=\s*"\{[^}]*?(?:Type|local:|vm:)(\w+)')

# ViewModel regex patterns
_VIEWMODEL_CLASS_RE   = re.compile(r'class\s+(\w+)\s*(?:<[^>]+>)?\s*:\s*[^{]*?(?:ViewModelBase|ObservableObject|INotifyPropertyChanged|BindableBase|ReactiveObject)')
_VIEWMODEL_BASE_RE    = re.compile(r':\s*[^{]*?(ViewModelBase|ObservableObject|INotifyPropertyChanged|BindableBase|ReactiveObject)')
_CS_AUTO_PROPERTY_RE  = re.compile(r'public\s+(?:virtual\s+|override\s+|new\s+)?([\w<>,\s?]+?)\s+(\w+)\s*\{\s*get\s*;')
_CS_PROP_CHANGED_RE   = re.compile(r'(?:OnPropertyChanged|SetProperty|RaisePropertyChanged|RaiseAndSetIfChanged)\s*\(')

# Entity / column mapping regex patterns
_TABLE_ATTR_RE   = re.compile(r'\[Table\s*\(\s*"([^"]+)"\s*\)\]')
_COLUMN_ATTR_RE  = re.compile(r'\[Column\s*\(\s*"([^"]+)"\s*\)\]')
_KEY_ATTR_RE     = re.compile(r'\[Key\]')
_ENTITY_CLASS_RE = re.compile(r'class\s+(\w+)')

# Fluent API regex patterns
_FLUENT_ENTITY_RE     = re.compile(r'\.Entity<(\w+)>\s*\(')
_FLUENT_TO_TABLE_RE   = re.compile(r'\.ToTable\s*\(\s*"([^"]+)"')
_FLUENT_PROPERTY_RE   = re.compile(r'\.Property\s*\(\s*\w+\s*=>\s*\w+\.(\w+)\s*\)')
_FLUENT_HAS_COLUMN_RE = re.compile(r'\.HasColumnName\s*\(\s*"([^"]+)"')

# SQL field extraction regex patterns
_SQL_SELECT_FIELDS_RE = re.compile(r'\bSELECT\s+(.*?)\bFROM\b', re.IGNORECASE | re.DOTALL)
_SQL_INSERT_FIELDS_RE = re.compile(r'\bINSERT\s+INTO\s+\[?\w+\]?\s*\(([^)]+)\)', re.IGNORECASE)
_SQL_UPDATE_SET_RE    = re.compile(r'\bSET\s+(.*?)(?:\bWHERE\b|$)', re.IGNORECASE | re.DOTALL)
_DAPPER_QUERY_TYPE_RE = re.compile(r'\.(Query|QueryAsync|QueryFirst|QuerySingle)<(\w+)>')


def discover_xaml_bindings(scan_root: str, repos: list[dict], project_meta: list[dict] | None = None) -> list[dict]:
    """Scan .xaml files for bindings, view types, and DataContext references."""
    views: list[dict] = []
    abs_root = _normalize_path(scan_root)

    for repo in repos:
        repo_meta = [pm for pm in (project_meta or []) if pm.get("repo") == repo["name"]]
        dir_to_project = build_file_to_project_map(repo_meta, repo["root"])
        xaml_files = find_files(repo["root"], re.compile(r"\.xaml$"))

        for xaml_file in xaml_files:
            content = safe_read_text(xaml_file)
            if content is None:
                continue

            rel_path = _relpath(xaml_file, abs_root)
            project_name = resolve_project_for_file(xaml_file, dir_to_project)

            # Extract x:Class
            view_type = None
            m = _XAML_CLASS_RE.search(content)
            if m:
                view_type = m.group(1)

            # Extract DataContext type
            data_context_type = None
            m = _XAML_DATA_CONTEXT_RE.search(content)
            if m:
                data_context_type = m.group(1)
            if not data_context_type:
                m = _XAML_DESIGN_CTX_RE.search(content)
                if m:
                    data_context_type = m.group(1)

            # Extract all binding paths
            bindings: list[dict] = []
            lines = content.splitlines()
            for i, line in enumerate(lines):
                for bm in _XAML_BINDING_PATH_RE.finditer(line):
                    binding_path = bm.group(1)
                    # Skip mode/converter/source keywords
                    if binding_path.lower() in ("mode", "converter", "source", "updatesourcetrigger",
                                                 "fallbackvalue", "stringformat", "elementname",
                                                 "relativesource", "targettype", "validationrules"):
                        continue
                    bindings.append({
                        "path": binding_path,
                        "line": i + 1,
                    })

            if view_type or bindings:
                views.append({
                    "file": rel_path,
                    "repo": repo["name"],
                    "project": project_name,
                    "viewType": view_type,
                    "dataContextType": data_context_type,
                    "bindings": bindings,
                })

    return views


def extract_viewmodel_properties(scan_root: str, repos: list[dict], project_meta: list[dict] | None = None) -> list[dict]:
    """Extract public properties from ViewModel classes."""
    viewmodels: list[dict] = []
    abs_root = _normalize_path(scan_root)

    for repo in repos:
        repo_meta = [pm for pm in (project_meta or []) if pm.get("repo") == repo["name"]]
        dir_to_project = build_file_to_project_map(repo_meta, repo["root"])
        cs_files = find_files(repo["root"], re.compile(r"\.cs$"))

        for cs_file in cs_files:
            content = safe_read_text(cs_file)
            if content is None:
                continue

            # Quick check: does this file contain a ViewModel class?
            if not _VIEWMODEL_CLASS_RE.search(content):
                continue

            rel_path = _relpath(cs_file, abs_root)
            project_name = resolve_project_for_file(cs_file, dir_to_project)
            lines = content.splitlines()

            current_class: str | None = None
            current_base: str = "unknown"
            properties: list[dict] = []

            for i, line in enumerate(lines):
                # Check for ViewModel class declaration
                cm = _VIEWMODEL_CLASS_RE.search(line)
                if cm:
                    # Save previous class if any
                    if current_class and properties:
                        viewmodels.append({
                            "file": rel_path,
                            "repo": repo["name"],
                            "project": project_name,
                            "className": current_class,
                            "baseClass": current_base,
                            "properties": properties,
                        })
                    current_class = cm.group(1)
                    bm = _VIEWMODEL_BASE_RE.search(line)
                    current_base = bm.group(1) if bm else "unknown"
                    properties = []
                    continue

                # Extract auto-properties if inside a ViewModel class
                if current_class:
                    pm_match = _CS_AUTO_PROPERTY_RE.search(line)
                    if pm_match:
                        prop_type = pm_match.group(1).strip()
                        prop_name = pm_match.group(2)
                        properties.append({
                            "propertyName": prop_name,
                            "propertyType": prop_type,
                            "line": i + 1,
                        })

            # Save last class
            if current_class and properties:
                viewmodels.append({
                    "file": rel_path,
                    "repo": repo["name"],
                    "project": project_name,
                    "className": current_class,
                    "baseClass": current_base,
                    "properties": properties,
                })

    return viewmodels


def extract_entity_properties(scan_root: str, repos: list[dict], data_findings: list[dict],
                               project_meta: list[dict] | None = None) -> list[dict]:
    """Extract entity class properties with column/table annotations."""
    # Build set of known entity names from DbSet findings
    known_entities: set[str] = set()
    for f in data_findings:
        if f.get("pattern") == "DbSet" and f.get("endpoint"):
            known_entities.add(f["endpoint"])

    if not known_entities:
        return []

    entities: list[dict] = []
    abs_root = _normalize_path(scan_root)

    for repo in repos:
        repo_meta = [pm for pm in (project_meta or []) if pm.get("repo") == repo["name"]]
        dir_to_project = build_file_to_project_map(repo_meta, repo["root"])
        cs_files = find_files(repo["root"], re.compile(r"\.cs$"))

        for cs_file in cs_files:
            content = safe_read_text(cs_file)
            if content is None:
                continue

            # Quick check: does any known entity name appear?
            if not any(ename in content for ename in known_entities):
                continue

            rel_path = _relpath(cs_file, abs_root)
            project_name = resolve_project_for_file(cs_file, dir_to_project)
            lines = content.splitlines()

            current_entity: str | None = None
            table_name: str | None = None
            properties: list[dict] = []
            pending_column: str | None = None
            pending_key: bool = False

            for i, line in enumerate(lines):
                stripped = line.strip()

                # Check for [Table("...")] attribute
                tm = _TABLE_ATTR_RE.search(stripped)
                if tm:
                    table_name = tm.group(1)
                    continue

                # Check for [Column("...")] attribute (applies to next property)
                cm = _COLUMN_ATTR_RE.search(stripped)
                if cm:
                    pending_column = cm.group(1)
                    continue

                # Check for [Key] attribute
                if _KEY_ATTR_RE.search(stripped):
                    pending_key = True
                    continue

                # Check for entity class declaration
                class_m = _ENTITY_CLASS_RE.search(stripped)
                if class_m and ("class " in stripped):
                    class_name = class_m.group(1)
                    if class_name in known_entities:
                        # Save previous entity if any
                        if current_entity and properties:
                            entities.append({
                                "file": rel_path,
                                "repo": repo["name"],
                                "project": project_name,
                                "className": current_entity,
                                "tableName": table_name,
                                "properties": properties,
                            })
                        current_entity = class_name
                        table_name = table_name  # carry over [Table] if declared just above
                        properties = []
                        pending_column = None
                        pending_key = False
                        continue

                # Extract properties if inside an entity class
                if current_entity:
                    pm_match = _CS_AUTO_PROPERTY_RE.search(stripped)
                    if pm_match:
                        prop_type = pm_match.group(1).strip()
                        prop_name = pm_match.group(2)
                        prop = {
                            "propertyName": prop_name,
                            "propertyType": prop_type,
                            "line": i + 1,
                            "columnName": pending_column or prop_name,  # convention fallback
                            "columnSource": "attribute" if pending_column else "convention",
                        }
                        if pending_key:
                            prop["isKey"] = True
                        properties.append(prop)
                        pending_column = None
                        pending_key = False

            # Save last entity
            if current_entity and properties:
                entities.append({
                    "file": rel_path,
                    "repo": repo["name"],
                    "project": project_name,
                    "className": current_entity,
                    "tableName": table_name,
                    "properties": properties,
                })

    return entities


def extract_fluent_api_mappings(scan_root: str, repos: list[dict],
                                 project_meta: list[dict] | None = None) -> list[dict]:
    """Extract EF Fluent API table/column mappings from DbContext configurations."""
    mappings: list[dict] = []
    abs_root = _normalize_path(scan_root)

    for repo in repos:
        repo_meta = [pm for pm in (project_meta or []) if pm.get("repo") == repo["name"]]
        dir_to_project = build_file_to_project_map(repo_meta, repo["root"])
        cs_files = find_files(repo["root"], re.compile(r"\.cs$"))

        for cs_file in cs_files:
            content = safe_read_text(cs_file)
            if content is None:
                continue

            # Quick check: file must contain OnModelCreating or ModelBuilder
            if "OnModelCreating" not in content and "ModelBuilder" not in content:
                continue

            rel_path = _relpath(cs_file, abs_root)
            project_name = resolve_project_for_file(cs_file, dir_to_project)
            lines = content.splitlines()

            current_entity: str | None = None
            entity_table: str | None = None
            column_maps: list[dict] = []

            for i, line in enumerate(lines):
                # Check for .Entity<TypeName>()
                em = _FLUENT_ENTITY_RE.search(line)
                if em:
                    # Save previous entity mappings
                    if current_entity and (entity_table or column_maps):
                        mappings.append({
                            "file": rel_path,
                            "repo": repo["name"],
                            "project": project_name,
                            "entityName": current_entity,
                            "tableName": entity_table,
                            "columnMappings": column_maps,
                        })
                    current_entity = em.group(1)
                    entity_table = None
                    column_maps = []

                # Check for .ToTable("TableName")
                tt = _FLUENT_TO_TABLE_RE.search(line)
                if tt and current_entity:
                    entity_table = tt.group(1)

                # Check for .Property(x => x.Prop).HasColumnName("col")
                prop_m = _FLUENT_PROPERTY_RE.search(line)
                if prop_m and current_entity:
                    prop_name = prop_m.group(1)
                    col_m = _FLUENT_HAS_COLUMN_RE.search(line)
                    if col_m:
                        column_maps.append({
                            "propertyName": prop_name,
                            "columnName": col_m.group(1),
                            "line": i + 1,
                        })
                    else:
                        # Check next line for split pattern
                        if i + 1 < len(lines):
                            next_line = lines[i + 1]
                            col_m2 = _FLUENT_HAS_COLUMN_RE.search(next_line)
                            if col_m2:
                                column_maps.append({
                                    "propertyName": prop_name,
                                    "columnName": col_m2.group(1),
                                    "line": i + 1,
                                })

            # Save last entity mappings
            if current_entity and (entity_table or column_maps):
                mappings.append({
                    "file": rel_path,
                    "repo": repo["name"],
                    "project": project_name,
                    "entityName": current_entity,
                    "tableName": entity_table,
                    "columnMappings": column_maps,
                })

    return mappings


def extract_sql_field_names(data_findings: list[dict]) -> list[dict]:
    """Extract column names from SQL strings in existing data findings context."""
    sql_fields: list[dict] = []

    for f in data_findings:
        context = f.get("context", "")
        if not context:
            continue

        # SELECT fields
        sel_m = _SQL_SELECT_FIELDS_RE.search(context)
        if sel_m:
            fields_str = sel_m.group(1).strip()
            if fields_str != "*":
                cols = [c.strip().split(".")[-1].strip("[] ") for c in fields_str.split(",")]
                cols = [c.split(" AS ")[-1].split(" as ")[-1].strip() for c in cols if c and c != "*"]
                cols = [c for c in cols if c and len(c) > 1 and c.upper() not in _SQL_KEYWORDS]
                if cols:
                    sql_fields.append({
                        "file": f.get("file", ""),
                        "line": f.get("line", 0),
                        "project": f.get("project"),
                        "type": "select",
                        "columns": cols,
                    })

        # INSERT fields
        ins_m = _SQL_INSERT_FIELDS_RE.search(context)
        if ins_m:
            cols = [c.strip().strip("[] ") for c in ins_m.group(1).split(",")]
            cols = [c for c in cols if c and len(c) > 1 and c.upper() not in _SQL_KEYWORDS]
            if cols:
                sql_fields.append({
                    "file": f.get("file", ""),
                    "line": f.get("line", 0),
                    "project": f.get("project"),
                    "type": "insert",
                    "columns": cols,
                })

        # Dapper Query<T> type parameter
        dq_m = _DAPPER_QUERY_TYPE_RE.search(context)
        if dq_m:
            sql_fields.append({
                "file": f.get("file", ""),
                "line": f.get("line", 0),
                "project": f.get("project"),
                "type": "dapper-query",
                "targetType": dq_m.group(2),
            })

    return sql_fields


def build_field_traceability(
    xaml_views: list[dict],
    viewmodels: list[dict],
    entities: list[dict],
    fluent_mappings: list[dict],
    sql_fields: list[dict],
    project_refs: list[dict],
    business_layers: dict[str, dict],
) -> dict:
    """Link XAML bindings → ViewModel properties → Entity properties → DB columns."""
    # Build lookup maps
    vm_by_class: dict[str, dict] = {}
    for vm in viewmodels:
        vm_by_class[vm["className"]] = vm

    entity_by_class: dict[str, dict] = {}
    for ent in entities:
        entity_by_class[ent["className"]] = ent

    # Build fluent API overrides: entity_name -> {prop_name: col_name, __table__: table_name}
    fluent_overrides: dict[str, dict] = {}
    for fm in fluent_mappings:
        ename = fm["entityName"]
        if ename not in fluent_overrides:
            fluent_overrides[ename] = {}
        if fm.get("tableName"):
            fluent_overrides[ename]["__table__"] = fm["tableName"]
        for cm in fm.get("columnMappings", []):
            fluent_overrides[ename][cm["propertyName"]] = cm["columnName"]

    # Build set of known entity type names for type matching
    known_entity_names: set[str] = set(entity_by_class.keys())

    # Generic type unwrapper
    _generic_re = re.compile(r'(?:ObservableCollection|List|IEnumerable|ICollection|IList|IReadOnlyList|IReadOnlyCollection)<(\w+)>')

    def unwrap_generic(type_str: str) -> str | None:
        m = _generic_re.search(type_str)
        return m.group(1) if m else None

    # Resolve table name for an entity
    def resolve_table(entity_name: str) -> str | None:
        # Priority: Fluent > [Table] attribute > DbSet property name (entity_name + "s" convention)
        fo = fluent_overrides.get(entity_name, {})
        if "__table__" in fo:
            return fo["__table__"]
        ent = entity_by_class.get(entity_name)
        if ent and ent.get("tableName"):
            return ent["tableName"]
        return entity_name + "s"  # EF convention

    # Resolve column name for entity property
    def resolve_column(entity_name: str, prop_name: str) -> tuple[str, str]:
        """Returns (column_name, source) where source is 'fluent-api', 'attribute', or 'convention'."""
        fo = fluent_overrides.get(entity_name, {})
        if prop_name in fo:
            return fo[prop_name], "fluent-api"
        ent = entity_by_class.get(entity_name)
        if ent:
            for prop in ent.get("properties", []):
                if prop["propertyName"] == prop_name:
                    return prop["columnName"], prop["columnSource"]
        return prop_name, "convention"

    field_chains: list[dict] = []
    chain_id = 0

    for view in xaml_views:
        view_type = view.get("viewType")
        dc_type = view.get("dataContextType")

        # Infer ViewModel name if not explicit
        vm_class_name = dc_type
        if not vm_class_name and view_type:
            # Convention: OrderWindow → OrderViewModel, OrderView → OrderViewModel
            for suffix in ("Window", "View", "Page", "Control", "UserControl"):
                if view_type.endswith(suffix):
                    vm_class_name = view_type[:-len(suffix)] + "ViewModel"
                    break
            if not vm_class_name:
                vm_class_name = view_type + "ViewModel"

        vm = vm_by_class.get(vm_class_name) if vm_class_name else None

        for binding in view.get("bindings", []):
            chain_id += 1
            binding_path = binding["path"]

            chain: dict = {
                "id": f"fc-{chain_id:03d}",
                "xamlBinding": {
                    "file": view["file"],
                    "project": view.get("project"),
                    "viewType": view_type,
                    "bindingPath": binding_path,
                    "dataContextType": dc_type,
                    "line": binding["line"],
                },
                "viewModelProperty": None,
                "entityProperty": None,
                "dbColumn": None,
                "chainCompleteness": "xaml-only",
                "confidence": "low",
            }

            # Link 1: XAML binding → ViewModel property
            vm_prop = None
            if vm:
                # Handle dotted paths (e.g., "Order.OrderId" — match first segment)
                match_name = binding_path.split(".")[0]
                for prop in vm.get("properties", []):
                    if prop["propertyName"] == match_name:
                        vm_prop = prop
                        break

            if vm_prop and vm:
                chain["viewModelProperty"] = {
                    "file": vm["file"],
                    "className": vm["className"],
                    "propertyName": vm_prop["propertyName"],
                    "propertyType": vm_prop["propertyType"],
                    "line": vm_prop["line"],
                }
                chain["chainCompleteness"] = "xaml-to-viewmodel"
                chain["confidence"] = "medium"

                # Link 2: ViewModel property → Entity
                prop_type = vm_prop["propertyType"]
                matched_entity_name: str | None = None

                # Direct type match
                if prop_type in known_entity_names:
                    matched_entity_name = prop_type
                else:
                    # Unwrap generics
                    inner = unwrap_generic(prop_type)
                    if inner and inner in known_entity_names:
                        matched_entity_name = inner

                # Find matching entity property by name
                entity_prop = None
                if matched_entity_name:
                    ent = entity_by_class.get(matched_entity_name)
                    if ent:
                        # Property name on dotted path (e.g., "Order.OrderId" → look for "OrderId" in Order entity)
                        if "." in binding_path:
                            sub_prop_name = binding_path.split(".", 1)[1].split(".")[0]
                        else:
                            sub_prop_name = binding_path
                        for ep in ent.get("properties", []):
                            if ep["propertyName"] == sub_prop_name:
                                entity_prop = ep
                                break
                else:
                    # No type match — try name match across all entities
                    prop_name = binding_path.split(".")[-1] if "." in binding_path else binding_path
                    for ename, ent in entity_by_class.items():
                        for ep in ent.get("properties", []):
                            if ep["propertyName"] == prop_name:
                                entity_prop = ep
                                matched_entity_name = ename
                                break
                        if entity_prop:
                            break

                if entity_prop and matched_entity_name:
                    chain["entityProperty"] = {
                        "file": entity_by_class[matched_entity_name]["file"],
                        "className": matched_entity_name,
                        "propertyName": entity_prop["propertyName"],
                        "propertyType": entity_prop["propertyType"],
                        "line": entity_prop["line"],
                    }
                    chain["chainCompleteness"] = "xaml-to-entity"
                    chain["confidence"] = "medium"

                    # Link 3: Entity property → DB column
                    col_name, col_source = resolve_column(matched_entity_name, entity_prop["propertyName"])
                    table = resolve_table(matched_entity_name)
                    fluent_file = None
                    fluent_line = None
                    for fm in fluent_mappings:
                        if fm["entityName"] == matched_entity_name:
                            fluent_file = fm["file"]
                            for cm in fm.get("columnMappings", []):
                                if cm["propertyName"] == entity_prop["propertyName"]:
                                    fluent_line = cm.get("line")
                                    break
                            break

                    chain["dbColumn"] = {
                        "table": table,
                        "column": col_name,
                        "source": col_source,
                        "file": fluent_file or entity_by_class[matched_entity_name]["file"],
                        "line": fluent_line or entity_prop["line"],
                    }
                    chain["chainCompleteness"] = "full"
                    chain["confidence"] = "high" if col_source != "convention" else "medium"

            elif not vm and vm_class_name:
                # No ViewModel found — try direct entity property name match
                prop_name = binding_path.split(".")[-1] if "." in binding_path else binding_path
                for ename, ent in entity_by_class.items():
                    for ep in ent.get("properties", []):
                        if ep["propertyName"] == prop_name:
                            chain["entityProperty"] = {
                                "file": ent["file"],
                                "className": ename,
                                "propertyName": ep["propertyName"],
                                "propertyType": ep["propertyType"],
                                "line": ep["line"],
                            }
                            col_name, col_source = resolve_column(ename, ep["propertyName"])
                            table = resolve_table(ename)
                            chain["dbColumn"] = {
                                "table": table,
                                "column": col_name,
                                "source": col_source,
                            }
                            chain["chainCompleteness"] = "xaml-to-entity"
                            chain["confidence"] = "low"
                            break
                    if chain["entityProperty"]:
                        break

            field_chains.append(chain)

    # Also add entity-to-column chains for entities not covered by XAML
    xaml_entity_names: set[str] = set()
    for ch in field_chains:
        if ch.get("entityProperty"):
            xaml_entity_names.add(ch["entityProperty"]["className"])

    for ename, ent in entity_by_class.items():
        for prop in ent.get("properties", []):
            chain_id += 1
            col_name, col_source = resolve_column(ename, prop["propertyName"])
            table = resolve_table(ename)
            field_chains.append({
                "id": f"fc-{chain_id:03d}",
                "xamlBinding": None,
                "viewModelProperty": None,
                "entityProperty": {
                    "file": ent["file"],
                    "className": ename,
                    "propertyName": prop["propertyName"],
                    "propertyType": prop["propertyType"],
                    "line": prop["line"],
                },
                "dbColumn": {
                    "table": table,
                    "column": col_name,
                    "source": col_source,
                },
                "chainCompleteness": "entity-to-column",
                "confidence": "high" if col_source != "convention" else "medium",
            })

    # Build summary
    completeness_counts: dict[str, int] = {}
    for ch in field_chains:
        comp = ch["chainCompleteness"]
        completeness_counts[comp] = completeness_counts.get(comp, 0) + 1

    full_count = completeness_counts.get("full", 0)
    partial_count = sum(v for k, v in completeness_counts.items() if k != "full")

    return {
        "fieldChains": field_chains,
        "summary": {
            "totalChains": len(field_chains),
            "fullChains": full_count,
            "partialChains": partial_count,
            "completenessBreakdown": completeness_counts,
        },
        "viewModels": viewmodels,
        "entities": entities,
        "xamlViews": xaml_views,
        "columnMappings": fluent_mappings,
        "sqlFields": sql_fields,
    }


# ─── UX inconsistency detection ──────────────────────────────────────

def detect_ux_inconsistencies(
    xaml_views: list[dict],
    viewmodel_classes: list[dict],
    entity_classes: list[dict],
    project_meta: list[dict],
) -> dict:
    """Detect MVVM binding inconsistencies between XAML views and ViewModels.

    Returns dict with 'issues' list and 'summary' counts.
    Issue types: missing_datacontext, missing_viewmodel, broken_binding,
                 orphan_viewmodel, mixed_patterns.
    """
    issues: list[dict] = []
    issue_id = 0

    # Build lookup maps
    vm_by_class: dict[str, dict] = {}
    for vm in viewmodel_classes:
        vm_by_class[vm["className"]] = vm

    # Map project → set of VM base classes used
    project_bases: dict[str, set] = {}
    for vm in viewmodel_classes:
        proj = vm.get("project") or ""
        if proj:
            project_bases.setdefault(proj, set()).add(vm.get("baseClass", "unknown"))

    # Track which VMs are referenced by views
    referenced_vms: set[str] = set()

    # Build project meta lookup
    pm_by_name = {pm["project"]: pm for pm in project_meta}

    for view in xaml_views:
        has_bindings = len(view.get("bindings", [])) > 0
        dc_type = view.get("dataContextType")
        view_type = view.get("viewType")
        project = view.get("project") or ""
        repo = view.get("repo") or ""
        file = view.get("file") or ""

        # Convention-based VM name: ViewName → ViewNameViewModel
        convention_vm = (view_type + "ViewModel") if view_type else None

        # Check for missing_datacontext:
        # View has bindings but no DataContext AND no convention-matched VM
        if has_bindings and not dc_type:
            convention_found = convention_vm and convention_vm in vm_by_class
            if not convention_found:
                issue_id += 1
                issues.append({
                    "id": f"ux-{issue_id:04d}",
                    "type": "missing_datacontext",
                    "severity": "warning",
                    "project": project,
                    "repo": repo,
                    "file": file,
                    "viewType": view_type,
                    "message": f"View '{view_type or file}' has {len(view['bindings'])} bindings but no DataContext and no convention-matched ViewModel",
                })

        # Resolve the target VM (explicit DataContext or convention)
        resolved_vm_name = dc_type
        if not resolved_vm_name and convention_vm and convention_vm in vm_by_class:
            resolved_vm_name = convention_vm

        if resolved_vm_name:
            referenced_vms.add(resolved_vm_name)

        # Check for missing_viewmodel:
        # DataContext references VM class that doesn't exist in scanned code
        if dc_type and dc_type not in vm_by_class:
            issue_id += 1
            issues.append({
                "id": f"ux-{issue_id:04d}",
                "type": "missing_viewmodel",
                "severity": "error",
                "project": project,
                "repo": repo,
                "file": file,
                "viewType": view_type,
                "className": dc_type,
                "message": f"DataContext references '{dc_type}' but this ViewModel class was not found in scanned code",
            })
            continue  # Can't check bindings if VM doesn't exist

        # Check for broken_binding:
        # Binding path's first segment doesn't match any property on the resolved VM
        if resolved_vm_name and resolved_vm_name in vm_by_class:
            vm = vm_by_class[resolved_vm_name]
            vm_props = {p["propertyName"] for p in vm.get("properties", [])}
            for binding in view.get("bindings", []):
                path = binding.get("path", "")
                first_segment = path.split(".")[0] if path else ""
                if first_segment and first_segment not in vm_props:
                    issue_id += 1
                    available = sorted(vm_props)[:10]
                    issues.append({
                        "id": f"ux-{issue_id:04d}",
                        "type": "broken_binding",
                        "severity": "error",
                        "project": project,
                        "repo": repo,
                        "file": file,
                        "viewType": view_type,
                        "className": resolved_vm_name,
                        "bindingPath": path,
                        "line": binding.get("line"),
                        "availableProperties": available,
                        "message": f"Binding path '{path}' not found on '{resolved_vm_name}' (first segment '{first_segment}' has no matching property)",
                    })

    # Check for orphan_viewmodel:
    # VM class not referenced by any XAML view (explicit or convention)
    for vm_name, vm in vm_by_class.items():
        if vm_name not in referenced_vms:
            issue_id += 1
            issues.append({
                "id": f"ux-{issue_id:04d}",
                "type": "orphan_viewmodel",
                "severity": "info",
                "project": vm.get("project") or "",
                "repo": vm.get("repo") or "",
                "file": vm.get("file") or "",
                "className": vm_name,
                "message": f"ViewModel '{vm_name}' is not referenced by any XAML view (explicit DataContext or naming convention)",
            })

    # Check for mixed_patterns:
    # Project uses >1 MVVM base class
    for proj, bases in project_bases.items():
        real_bases = bases - {"unknown"}
        if len(real_bases) > 1:
            issue_id += 1
            pm = pm_by_name.get(proj, {})
            issues.append({
                "id": f"ux-{issue_id:04d}",
                "type": "mixed_patterns",
                "severity": "info",
                "project": proj,
                "repo": pm.get("repo", ""),
                "file": "",
                "baseClasses": sorted(real_bases),
                "message": f"Project '{proj}' uses multiple MVVM base classes: {', '.join(sorted(real_bases))}",
            })

    # Build summary
    by_type: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    by_project: dict[str, int] = {}
    for iss in issues:
        by_type[iss["type"]] = by_type.get(iss["type"], 0) + 1
        by_severity[iss["severity"]] = by_severity.get(iss["severity"], 0) + 1
        by_project[iss["project"]] = by_project.get(iss["project"], 0) + 1

    return {
        "issues": issues,
        "summary": {
            "totalIssues": len(issues),
            "byType": by_type,
            "bySeverity": by_severity,
            "byProject": by_project,
        },
    }


# ─── Data flow graph builder ─────────────────────────────────────────

def build_data_flow_graph(findings: list[dict], project_meta: list[dict]) -> dict:
    """Build a data flow graph connecting projects through shared data infrastructure.

    Returns a dict with dataNodes, dataEdges, impliedDependencies, infrastructureGroups.
    """
    # Group findings by endpoint (only those with an extracted endpoint name)
    endpoint_findings: dict[str, list[dict]] = {}
    for f in findings:
        ep = f.get("endpoint")
        ep_type = f.get("endpointType")
        if ep and ep_type:
            key = f"{ep_type}:{ep}"
            endpoint_findings.setdefault(key, []).append(f)

    # Build data nodes and directional edges
    data_nodes: list[dict] = []
    data_edges: list[dict] = []

    # Map endpoint type to infrastructure category
    type_to_infra = {
        "table": "database", "entity": "database", "collection": "database",
        "topic": "messaging", "queue": "messaging", "exchange": "messaging",
        "route": "api", "url": "api",
    }

    for endpoint_key, ep_findings in endpoint_findings.items():
        ep_type, ep_name = endpoint_key.split(":", 1)
        infra = type_to_infra.get(ep_type, "other")

        writers: set[str] = set()
        readers: set[str] = set()
        exposers: set[str] = set()
        consumers: set[str] = set()
        both: set[str] = set()

        for f in ep_findings:
            proj = f.get("project")
            if not proj:
                continue
            direction = f.get("direction")
            if direction == "write":
                writers.add(proj)
            elif direction == "read":
                readers.add(proj)
            elif direction == "expose":
                exposers.add(proj)
            elif direction == "consume":
                consumers.add(proj)
            elif direction == "both":
                both.add(proj)

        node = {
            "id": endpoint_key,
            "name": ep_name,
            "type": ep_type,
            "infrastructure": infra,
            "writers": sorted(writers | both),
            "readers": sorted(readers | both),
        }
        if exposers:
            node["exposers"] = sorted(exposers)
        if consumers:
            node["consumers"] = sorted(consumers)
        data_nodes.append(node)

        # Build directional edges
        for proj in writers | both:
            data_edges.append({"from": proj, "to": endpoint_key, "direction": "write", "endpointType": ep_type})
        for proj in readers | both:
            data_edges.append({"from": endpoint_key, "to": proj, "direction": "read", "endpointType": ep_type})
        for proj in exposers:
            data_edges.append({"from": proj, "to": endpoint_key, "direction": "expose", "endpointType": ep_type})
        for proj in consumers:
            data_edges.append({"from": endpoint_key, "to": proj, "direction": "consume", "endpointType": ep_type})

    # Derive implied dependencies: if A writes to X and B reads from X => A → B
    implied_deps: list[dict] = []
    seen_implied: set[tuple[str, str, str]] = set()
    for node in data_nodes:
        all_writers = set(node["writers"])
        all_readers = set(node["readers"])
        all_exposers = set(node.get("exposers", []))
        all_consumers = set(node.get("consumers", []))

        # write → read dependencies
        for w in all_writers:
            for r in all_readers:
                if w != r:
                    key = (w, r, node["id"])
                    if key not in seen_implied:
                        seen_implied.add(key)
                        implied_deps.append({
                            "from": w, "to": r,
                            "via": node["name"], "viaType": node["infrastructure"],
                            "viaId": node["id"],
                        })

        # expose → consume dependencies
        for e in all_exposers:
            for c in all_consumers:
                if e != c:
                    key = (e, c, node["id"])
                    if key not in seen_implied:
                        seen_implied.add(key)
                        implied_deps.append({
                            "from": e, "to": c,
                            "via": node["name"], "viaType": node["infrastructure"],
                            "viaId": node["id"],
                        })

    # Infrastructure groups: direction-aware pattern usage even without specific endpoints
    infra_groups: dict[str, dict] = {}
    for f in findings:
        pattern = f["pattern"]
        ftype = f["type"]
        proj = f.get("project")
        direction = f.get("direction")
        if not proj:
            continue

        gkey = f"{pattern}:{ftype}"
        if gkey not in infra_groups:
            infra_groups[gkey] = {"pattern": pattern, "type": ftype, "projects": {}}

        if proj not in infra_groups[gkey]["projects"]:
            infra_groups[gkey]["projects"][proj] = {}

        if direction:
            infra_groups[gkey]["projects"][proj][direction] = (
                infra_groups[gkey]["projects"][proj].get(direction, 0) + 1
            )
        else:
            infra_groups[gkey]["projects"][proj]["unknown"] = (
                infra_groups[gkey]["projects"][proj].get("unknown", 0) + 1
            )

    return {
        "dataNodes": data_nodes,
        "dataEdges": data_edges,
        "impliedDependencies": implied_deps,
        "infrastructureGroups": list(infra_groups.values()),
    }


# ─── E2E path computation ────────────────────────────────────────────

def build_unified_graph(
    all_project_refs: list[dict],
    implied_deps: list[dict],
) -> dict[str, set[tuple[str, str]]]:
    """Build adjacency list combining project references and implied data dependencies.

    Returns: {project_name: set of (target_project, edge_type)}
    """
    adj: dict[str, set[tuple[str, str]]] = {}

    for ref in all_project_refs:
        src = ref["project"]
        dst = ref["references"]
        adj.setdefault(src, set()).add((dst, "project-reference"))

    for dep in implied_deps:
        src = dep["from"]
        dst = dep["to"]
        adj.setdefault(src, set()).add((dst, f"data-flow-{dep.get('viaType', 'unknown')}"))

    return adj


def find_data_endpoints_for_project(
    project_name: str,
    data_nodes: list[dict],
) -> list[dict]:
    """Find data endpoints (DB tables, entities, topics, etc.) that a project reads or writes."""
    endpoints = []
    for node in data_nodes:
        roles = []
        if project_name in node.get("writers", []):
            roles.append("write")
        if project_name in node.get("readers", []):
            roles.append("read")
        if project_name in node.get("exposers", []):
            roles.append("expose")
        if project_name in node.get("consumers", []):
            roles.append("consume")
        if roles:
            endpoints.append({
                "endpoint": node["id"],
                "name": node["name"],
                "type": node.get("infrastructure", node.get("type", "unknown")),
                "endpointType": node.get("type", "unknown"),
                "roles": roles,
            })
    return endpoints


def find_e2e_paths(
    business_layers: dict[str, dict],
    unified_graph: dict[str, set[tuple[str, str]]],
    data_nodes: list[dict],
    named_flows: list[dict],
    data_findings: list[dict] | None = None,
    max_depth: int = 8,
) -> list[dict]:
    """BFS from each Presentation project to find end-to-end flow paths.

    Terminal conditions (path is recorded when current project has):
    1. Named data endpoints from data_nodes (e.g., entity:Trades), OR
    2. DataAccess layer + data access patterns (e.g., DbContext, SQL) but no extracted endpoints

    Returns list of flow path dicts with source, path, data endpoints, etc.
    """
    presentation_projects = [
        name for name, info in business_layers.items()
        if info["layer"] == "Presentation"
    ]

    # Build named flow lookup (source -> flow info)
    named_flow_lookup: dict[str, dict] = {}
    for nf in named_flows:
        src = nf.get("source", "")
        if src:
            named_flow_lookup[src] = nf

    # Build set of projects that have data access patterns (for fallback terminal)
    data_access_projects: set[str] = set()
    if data_findings:
        data_types = {"database", "messaging", "cache", "storage"}
        for f in data_findings:
            proj = f.get("project")
            if proj and f.get("type") in data_types:
                data_access_projects.add(proj)

    all_paths: list[dict] = []

    for source in presentation_projects:
        # BFS
        queue: list[list[tuple[str, str]]] = [[(source, "start")]]
        visited: set[str] = {source}

        while queue:
            path = queue.pop(0)
            current_project = path[-1][0]

            if len(path) > max_depth:
                continue

            # Check if current project has data endpoints
            endpoints = find_data_endpoints_for_project(current_project, data_nodes)

            # Fallback: treat DataAccess-layer projects with data patterns as terminals
            is_data_terminal = False
            if not endpoints and len(path) >= 2:
                cur_layer = business_layers.get(current_project, {}).get("layer")
                if cur_layer == "DataAccess" and current_project in data_access_projects:
                    is_data_terminal = True

            # Record path if it reaches a data endpoint/terminal and has at least 2 steps
            if (endpoints or is_data_terminal) and len(path) >= 2:
                path_entries = []
                layers_crossed = []
                for proj, edge_type in path:
                    layer_info = business_layers.get(proj, {"layer": "Unclassified"})
                    entry = {
                        "project": proj,
                        "layer": layer_info["layer"],
                        "edgeType": edge_type,
                    }
                    path_entries.append(entry)
                    if layer_info["layer"] not in layers_crossed:
                        layers_crossed.append(layer_info["layer"])

                # Add data endpoint entries (or marker for DataAccess terminal)
                data_ep_ids = []
                if endpoints:
                    for ep in endpoints:
                        path_entries.append({
                            "endpoint": ep["endpoint"],
                            "type": ep["type"],
                            "edgeType": f"data-flow-{ep['roles'][0]}",
                        })
                        data_ep_ids.append(ep["endpoint"])
                elif is_data_terminal:
                    data_ep_ids.append(f"project:{current_project}")

                named = named_flow_lookup.get(source)
                flow_path = {
                    "source": {"project": source, "layer": "Presentation"},
                    "path": path_entries,
                    "pathLength": len(path),
                    "crossesLayers": layers_crossed,
                    "dataEndpoints": data_ep_ids,
                }
                if named:
                    flow_path["namedFlow"] = named.get("name", "")
                    flow_path["description"] = named.get("description", "")

                all_paths.append(flow_path)

            # Expand neighbors
            neighbors = unified_graph.get(current_project, set())
            for neighbor, edge_type in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [(neighbor, edge_type)])

    # Deduplicate and rank: shorter paths first, then by layer diversity
    all_paths.sort(key=lambda p: (p["pathLength"], -len(p["crossesLayers"])))

    return all_paths


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
    abs_root = _normalize_path(scan_root)
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
            rel_path = _relpath(f, abs_root)
            content = safe_read_text(f)
            if content is None:
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


# ─── NuGet health analysis ────────────────────────────────────────────

def build_nuget_health(
    package_deps: list[dict],
    project_meta: list[dict],
    repos: list[dict],
) -> dict:
    """Analyze NuGet package health: version conflicts, legacy formats, frameworks, CPM status.

    Returns dict with versionConflicts, legacyFormatProjects, targetFrameworks,
    mixedFrameworkRepos, centralPackageManagement, and summary.
    """
    # Build package → {versions: {version: [projects]}, consumers: set}
    pkg_versions: dict[str, dict[str, list[str]]] = {}
    for pd in package_deps:
        pkg = pd["package"]
        ver = pd["version"] or "unspecified"
        proj = f"{pd['repo']}/{pd['project']}"
        pkg_versions.setdefault(pkg, {}).setdefault(ver, []).append(proj)

    # Version conflicts: packages with >1 version
    version_conflicts = []
    for pkg, versions in sorted(pkg_versions.items()):
        if len(versions) > 1:
            proj_count = sum(len(projs) for projs in versions.values())
            version_conflicts.append({
                "package": pkg,
                "versions": versions,
                "versionCount": len(versions),
                "projectCount": proj_count,
            })
    version_conflicts.sort(key=lambda x: -x["projectCount"])

    # Legacy format projects (packages.config)
    legacy_projects = []
    for pm in project_meta:
        if pm.get("nugetFormat") == "packages.config":
            legacy_projects.append({
                "project": pm["project"],
                "repo": pm.get("repo", ""),
                "path": pm.get("path", ""),
            })

    # Target frameworks
    target_frameworks: dict[str, list[str]] = {}
    for pm in project_meta:
        tf = pm.get("targetFramework", "unknown")
        if tf == "unknown":
            continue
        # Handle multi-targeting (split on ';')
        for fw in tf.split(";"):
            fw = fw.strip()
            if fw:
                target_frameworks.setdefault(fw, []).append(pm["project"])

    # Mixed framework repos
    repo_frameworks: dict[str, set[str]] = {}
    for pm in project_meta:
        tf = pm.get("targetFramework", "unknown")
        if tf == "unknown":
            continue
        repo = pm.get("repo", "")
        if repo:
            for fw in tf.split(";"):
                fw = fw.strip()
                if fw:
                    repo_frameworks.setdefault(repo, set()).add(fw)
    mixed_framework_repos = {
        repo: sorted(fws)
        for repo, fws in repo_frameworks.items()
        if len(fws) > 1
    }

    # Central Package Management detection
    cpm_status: dict[str, bool] = {}
    for repo in repos:
        dpp_path = os.path.join(repo["root"], "Directory.Packages.props")
        dpp_content = safe_read_text(dpp_path)
        if dpp_content:
            has_cpm = bool(re.search(r'<ManagePackageVersionsCentrally>\s*true\s*</ManagePackageVersionsCentrally>',
                                     dpp_content, re.IGNORECASE))
            cpm_status[repo["name"]] = has_cpm
        else:
            cpm_status[repo["name"]] = False

    return {
        "versionConflicts": version_conflicts,
        "legacyFormatProjects": legacy_projects,
        "targetFrameworks": {fw: projs for fw, projs in sorted(target_frameworks.items())},
        "mixedFrameworkRepos": mixed_framework_repos,
        "centralPackageManagement": cpm_status,
        "summary": {
            "totalPackages": len(pkg_versions),
            "conflictCount": len(version_conflicts),
            "legacyCount": len(legacy_projects),
            "frameworkCount": len(target_frameworks),
            "cpmRepos": sum(1 for v in cpm_status.values() if v),
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
    global SCAN_ROOT
    SCAN_ROOT = _normalize_path(SCAN_ROOT)
    print(f"\n=== Dependency Mapper (Python) ===")
    print(f"Scan root: {SCAN_ROOT}")
    print(f"Output:    {OUT_DIR}\n")

    # Load business-map.json overrides (optional)
    business_map_path = os.path.join(SCAN_ROOT, "business-map.json")
    business_overrides: dict[str, str] = {}
    named_flows: list[dict] = []
    if os.path.isfile(business_map_path):
        try:
            bm = json.loads(safe_read_text(business_map_path) or "{}")
            business_overrides = bm.get("overrides", {})
            named_flows = bm.get("namedFlows", [])
            print(f"  Loaded business-map.json: {len(business_overrides)} overrides, {len(named_flows)} named flows")
        except (json.JSONDecodeError, OSError) as e:
            print(f"  Warning: Could not parse business-map.json: {e}")

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

    # Step 3: Discover data access patterns (enhanced with direction + endpoints)
    print("\nStep 2: Discovering data access patterns...")
    data_findings = discover_data_patterns(SCAN_ROOT, repos, all_project_meta)
    print(f"  Found {len(data_findings)} data access pattern matches")

    type_summary: dict[str, int] = {}
    for f in data_findings:
        type_summary[f["pattern"]] = type_summary.get(f["pattern"], 0) + 1

    for pat, count in sorted(type_summary.items(), key=lambda x: -x[1])[:15]:
        print(f"    {pat}: {count}")
    if len(type_summary) > 15:
        print(f"    ... and {len(type_summary) - 15} more patterns")

    # Direction summary
    dir_counts: dict[str, int] = {}
    for f in data_findings:
        d = f.get("direction") or "unclassified"
        dir_counts[d] = dir_counts.get(d, 0) + 1
    print(f"  Directions: {json.dumps(dir_counts)}")

    ep_count = sum(1 for f in data_findings if f.get("endpoint"))
    print(f"  Endpoints extracted: {ep_count}")

    Path(os.path.join(OUT_DIR, "data-sources.json")).write_text(
        json.dumps(data_findings, indent=2), encoding="utf-8"
    )

    # Step 3b: Build data flow graph
    print("\nStep 2b: Building data flow graph...")
    data_flow = build_data_flow_graph(data_findings, all_project_meta)
    Path(os.path.join(OUT_DIR, "data-flow.json")).write_text(
        json.dumps(data_flow, indent=2), encoding="utf-8"
    )
    print(f"  Data nodes: {len(data_flow['dataNodes'])}")
    print(f"  Data edges: {len(data_flow['dataEdges'])}")
    print(f"  Implied dependencies: {len(data_flow['impliedDependencies'])}")
    print(f"  Infrastructure groups: {len(data_flow['infrastructureGroups'])}")

    # Step 2c: Business layer classification
    print("\nStep 2c: Classifying business layers...")
    business_layers = classify_all_projects(
        all_project_meta, all_package_deps, data_findings, business_overrides
    )

    layer_counts: dict[str, int] = {}
    for info in business_layers.values():
        layer_counts[info["layer"]] = layer_counts.get(info["layer"], 0) + 1
    for layer, count in sorted(layer_counts.items(), key=lambda x: -x[1]):
        print(f"    {layer}: {count}")

    # Step 2d: E2E path computation
    print("\nStep 2d: Computing end-to-end flow paths...")
    unified_graph = build_unified_graph(all_project_refs, data_flow.get("impliedDependencies", []))
    flow_paths = find_e2e_paths(
        business_layers, unified_graph, data_flow.get("dataNodes", []), named_flows,
        data_findings=data_findings,
    )
    print(f"  Found {len(flow_paths)} end-to-end flow paths")

    # Build layer summary
    layer_summary: dict[str, dict] = {}
    for proj_name, info in business_layers.items():
        layer = info["layer"]
        if layer not in layer_summary:
            layer_summary[layer] = {"count": 0, "projects": []}
        layer_summary[layer]["count"] += 1
        layer_summary[layer]["projects"].append(proj_name)

    flow_paths_output = {
        "businessLayers": {
            name: {"layer": info["layer"], "confidence": info["confidence"], "signals": info["signals"]}
            for name, info in business_layers.items()
        },
        "flowPaths": flow_paths,
        "layerSummary": layer_summary,
    }
    Path(os.path.join(OUT_DIR, "flow-paths.json")).write_text(
        json.dumps(flow_paths_output, indent=2), encoding="utf-8"
    )
    print(f"  Wrote flow-paths.json")

    # Step 2e: Field-level traceability
    print("\nStep 2e: Building field-level traceability...")
    xaml_views = discover_xaml_bindings(SCAN_ROOT, repos, all_project_meta)
    print(f"  XAML views: {len(xaml_views)}, bindings: {sum(len(v.get('bindings', [])) for v in xaml_views)}")

    vm_data = extract_viewmodel_properties(SCAN_ROOT, repos, all_project_meta)
    print(f"  ViewModels: {len(vm_data)}, properties: {sum(len(v.get('properties', [])) for v in vm_data)}")

    entity_data = extract_entity_properties(SCAN_ROOT, repos, data_findings, all_project_meta)
    print(f"  Entities: {len(entity_data)}, properties: {sum(len(e.get('properties', [])) for e in entity_data)}")

    fluent_data = extract_fluent_api_mappings(SCAN_ROOT, repos, all_project_meta)
    print(f"  Fluent API mappings: {len(fluent_data)}")

    sql_field_data = extract_sql_field_names(data_findings)
    print(f"  SQL field extractions: {len(sql_field_data)}")

    field_trace = build_field_traceability(
        xaml_views, vm_data, entity_data, fluent_data, sql_field_data,
        all_project_refs, business_layers,
    )
    Path(os.path.join(OUT_DIR, "field-traceability.json")).write_text(
        json.dumps(field_trace, indent=2), encoding="utf-8"
    )
    ft_summary = field_trace.get("summary", {})
    print(f"  Field chains: {ft_summary.get('totalChains', 0)} (full: {ft_summary.get('fullChains', 0)}, partial: {ft_summary.get('partialChains', 0)})")
    if ft_summary.get("completenessBreakdown"):
        for level, count in sorted(ft_summary["completenessBreakdown"].items(), key=lambda x: -x[1]):
            print(f"    {level}: {count}")
    print(f"  Wrote field-traceability.json")

    # Step 2f: Detect UX inconsistencies
    ux_issues = detect_ux_inconsistencies(xaml_views, vm_data, entity_data, all_project_meta)
    Path(os.path.join(OUT_DIR, "ux-inconsistencies.json")).write_text(
        json.dumps(ux_issues, indent=2), encoding="utf-8"
    )
    ux_sum = ux_issues.get("summary", {})
    print(f"  UX inconsistencies: {ux_sum.get('totalIssues', 0)} (errors: {ux_sum.get('bySeverity', {}).get('error', 0)}, warnings: {ux_sum.get('bySeverity', {}).get('warning', 0)}, info: {ux_sum.get('bySeverity', {}).get('info', 0)})")
    print(f"  Wrote ux-inconsistencies.json")

    # Step 2g: Scan test projects
    print("\nStep 2g: Scanning test projects...")
    test_data = scan_test_projects(all_project_meta, all_project_refs, SCAN_ROOT, repos)
    Path(os.path.join(OUT_DIR, "test-projects.json")).write_text(
        json.dumps(test_data, indent=2), encoding="utf-8"
    )
    ts = test_data["summary"]
    print(f"  Test projects: {ts['totalTestProjects']}, methods: {ts['totalTestMethods']}, classes: {ts['totalTestClasses']}")
    print(f"  Coverage: {ts['coverageRatio']} projects covered")
    print(f"  Wrote test-projects.json")

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

    # Step 5: NuGet health analysis
    print("\nStep 5: Analyzing NuGet health...")
    nuget_health = build_nuget_health(all_package_deps, all_project_meta, repos)
    Path(os.path.join(OUT_DIR, "nuget-health.json")).write_text(
        json.dumps(nuget_health, indent=2), encoding="utf-8"
    )
    nh_sum = nuget_health["summary"]
    print(f"  Total packages: {nh_sum['totalPackages']}")
    print(f"  Version conflicts: {nh_sum['conflictCount']}")
    print(f"  Legacy (packages.config): {nh_sum['legacyCount']}")
    print(f"  Target frameworks: {nh_sum['frameworkCount']}")
    print(f"  CPM repos: {nh_sum['cpmRepos']}")
    print(f"  Wrote nuget-health.json")

    print("\n=== Analysis complete ===\n")


if __name__ == "__main__":
    main()
