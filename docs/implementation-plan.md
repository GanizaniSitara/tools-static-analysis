# Implementation Plan: Code Smell Visualization, NuGet Modernization & UX Inconsistency Detection

**Date**: 2026-02-14
**Scope**: Enhancements to the static analysis scanning pipeline
**Target**: 25GB .NET financial pricer codebase (~10K+ C# files, WPF desktop apps, pricer engines, data access layers)

---

## Overview

Three features that extend what the scanner detects and surfaces when analyzing the target codebase. All three build on data that the pipeline **already partially collects** but doesn't fully exploit.

| # | Feature | Key Insight | Effort |
|---|---------|-------------|--------|
| 1 | Code Smell Visualization | `refactoring-targets.json` exists with full smell data but viewer ignores it entirely | Medium |
| 2 | NuGet Modernization Analysis | `analyze.py` already collects versions, `packages.config`, `.props` — just needs comparison/flagging logic | Low |
| 3 | UX Inconsistency Detection | `discover_xaml_bindings()` and `extract_viewmodel_properties()` already run — need cross-referencing | Medium |

### Architecture Principle

All three features follow the same pattern:

```
analyze.py (or refactor_triage.py)    generate_docs.py
         |                                  |
    scan target codebase              load JSON, render tab
    produce JSON output               inject into viewer.html
         |                                  |
    {feature}-data.json  ──────────>  "Feature" tab in viewer
```

**No changes to `visualize.py`**. All viewer rendering goes through `generate_docs.py` → `viewer.html`. The Mermaid diagrams in `visualize.py` are for dependency/flow visualization only and are not touched by this plan.

---

## Feature 1: Code Smell Visualization in Viewer

### Problem

`refactor_triage.py` produces `refactoring-targets.json` with per-project smell data (god methods, sync-over-async, precision-unsafe math, exception swallowing, etc.) and a tiered refactoring plan. But `generate_docs.py` never reads this file. The viewer has no "Code Quality" tab. All the refactoring intelligence is invisible unless you manually open the JSON.

### What Already Exists

- `refactor_triage.py` outputs `refactoring-targets.json` to the same `OUT_DIR` as all other pipeline outputs
- The JSON contains:
  - `summary.totalSmells`, `summary.topSmellTypes` — aggregate stats
  - `projects[].smell_count`, `projects[].top_smells`, `projects[].refactoring_value_score` — per-project
  - `projects[].files[].smells[]` — per-file smell instances with type, line number, context
  - `claudeCodeTargets.tier1_critical`, `tier2_high`, `tier3_medium` — prioritized refactoring targets with suggested prompts
- `generate_docs.py` already loads multiple JSON files from the output directory and renders them as viewer tabs

### Implementation Steps

#### Step 1: Load refactoring data in `generate_docs.py`

In `generate_docs.py`, in the `generate_viewer()` function (around where it loads `graph.json`, `data-flow.json`, etc.), add:

```python
refactoring_data = _load_json(os.path.join(OUT_DIR, "refactoring-targets.json"), {})
refactoring_projects = refactoring_data.get("projects", [])
refactoring_summary = refactoring_data.get("summary", {})
claude_targets = refactoring_data.get("claudeCodeTargets", {})
```

#### Step 2: Add "Code Quality" tab button

In the `all_tab_ids` list where tabs are registered:

```python
if refactoring_projects:
    all_tab_ids.append(("codequality", "Code Quality"))
```

#### Step 3: Build the tab panel HTML

Create a new panel with three sections:

**Section A — Summary cards** (same pattern as existing hotspot summary cards):
- Total smells count
- Top 5 smell types with counts
- Files scanned / files with smells ratio
- Top project by refactoring value score

**Section B — Project table** (sortable, same pattern as "All Projects" table):

| Column | Source |
|--------|--------|
| Project | `projects[].project` |
| Category | `projects[].category` |
| Score | `projects[].refactoring_value_score` |
| Smells | `projects[].smell_count` |
| Top Smell | `projects[].top_smells[0]` |
| Lines | `projects[].total_lines` |
| God Methods | count from `files[].smells[]` where type=god_method |
| Has Tests | `projects[].has_tests` |

Color-code rows: red for tier 1 (score > 100), yellow for tier 2 (> 50), default for tier 3.

**Section C — Refactoring session plan**:
- Render `claudeCodeTargets` tiers as collapsible sections
- Each target shows: project name, why, suggested prompt (in a copyable code block), estimated effort, key files list
- This is the actionable output for AI-assisted refactoring sessions

#### Step 4: Inject refactoring data into JavaScript

Same pattern as existing data injection — serialize as JSON into a `<script>` block:

```python
refactoring_json = json.dumps({
    "summary": refactoring_summary,
    "projects": [
        {
            "project": p["project"],
            "category": p.get("category", ""),
            "refactoring_value_score": p["refactoring_value_score"],
            "smell_count": p["smell_count"],
            "top_smells": p.get("top_smells", []),
            "total_lines": p.get("total_lines", 0),
            "total_files": p.get("total_files", 0),
            "has_tests": p.get("has_tests", False),
            "complexity_score": p.get("complexity_score", 0),
        }
        for p in refactoring_projects[:100]  # cap for performance
    ],
    "targets": claude_targets,
}, indent=None)
```

Add to the `<script>` section: `window._refactoringData = {refactoring_json};`

Then build the table and session plan from `window._refactoringData` in JavaScript, same as the hotspot and allprojects tabs do.

### Files to Modify

- `generate_docs.py` — load refactoring JSON, add tab, render panel, inject JS data

### Dependencies

- `refactor_triage.py` must have been run before `generate_docs.py`
- If `refactoring-targets.json` doesn't exist, skip the tab gracefully (no crash)

---

## Feature 2: NuGet Modernization Analysis

### Problem

The 25GB financial codebase almost certainly has NuGet hygiene issues: version conflicts (project A uses Newtonsoft 12.x, project B uses 13.x), legacy `packages.config` projects that haven't migrated to `PackageReference`, mixed target frameworks (`net48` alongside `net8.0`), and no Central Package Management. `analyze.py` **already collects all the raw data** but never compares or flags it.

### What Already Exists

- `analyze.py` extracts `PackageReference` from `.csproj` files (modern SDK-style)
- `analyze.py` reads `packages.config` (legacy format) — see the `pkgs_config_path` code in `extract_dependencies_from_repo()`
- `analyze.py` reads `Directory.Build.props` and `Directory.Packages.props` in `load_properties()`
- `build_graph()` aggregates NuGet packages with version sets: `nuget_packages[pkg_id]["versions"]` is a `set` — version conflicts are already detectable by checking `len(versions) > 1`
- `.csproj` XML content is already read into memory (the `xml` variable in `extract_dependencies_from_repo`) — `<TargetFramework>` is right there but never extracted

### Implementation Steps

#### Step 1: Extract target framework from `.csproj`

In `analyze.py`, in `extract_dependencies_from_repo()`, after reading the `.csproj` XML, extract the target framework:

```python
# After reading xml for each csproj
tf_match = re.search(r'<TargetFramework(?:s)?>(.*?)</TargetFramework(?:s)?>', xml)
target_framework = tf_match.group(1) if tf_match else "unknown"
```

Add `"targetFramework": target_framework` to the `project_meta` dict for each project.

#### Step 2: Detect `packages.config` projects

Already detected (the code reads it). Just need to flag it in the metadata:

```python
uses_packages_config = os.path.isfile(pkgs_config_path) and pkgs_config_xml is not None
```

Add `"nugetFormat": "packages.config" if uses_packages_config else "PackageReference"` to `project_meta`.

#### Step 3: Detect Central Package Management

In `load_properties()`, the code already reads `Directory.Packages.props`. Check for the CPM property:

```python
uses_cpm = False
dbp_path = os.path.join(repo_root, "Directory.Packages.props")
if os.path.isfile(dbp_path):
    dbp_xml = safe_read_text(dbp_path) or ""
    if "ManagePackageVersionsCentrally" in dbp_xml and "true" in dbp_xml.lower():
        uses_cpm = True
```

#### Step 4: Build NuGet health report

New function in `analyze.py`, called after `build_graph()`:

```python
def build_nuget_health(package_deps, project_meta, repos):
    """Analyze NuGet package health across the scanned codebase."""
    
    # 1. Version conflicts
    pkg_versions = {}  # {package_name: {version: [projects]}}
    for pd in package_deps:
        pkg = pd["package"]
        ver = pd["version"]
        if pkg not in pkg_versions:
            pkg_versions[pkg] = {}
        if ver not in pkg_versions[pkg]:
            pkg_versions[pkg][ver] = []
        pkg_versions[pkg][ver].append(pd["project"])
    
    conflicts = []
    for pkg, versions in pkg_versions.items():
        if len(versions) > 1:
            conflicts.append({
                "package": pkg,
                "versions": {v: projs for v, projs in versions.items()},
                "versionCount": len(versions),
                "projectCount": sum(len(p) for p in versions.values()),
            })
    conflicts.sort(key=lambda c: -c["projectCount"])
    
    # 2. Legacy format projects
    legacy_projects = [
        pm["project"] for pm in project_meta
        if pm.get("nugetFormat") == "packages.config"
    ]
    
    # 3. Target framework summary
    framework_groups = {}  # {framework: [projects]}
    for pm in project_meta:
        tf = pm.get("targetFramework", "unknown")
        # Handle multi-targeting (e.g., "net48;net8.0")
        for f in tf.split(";"):
            f = f.strip()
            if f not in framework_groups:
                framework_groups[f] = []
            framework_groups[f].append(pm["project"])
    
    # 4. CPM status per repo
    cpm_status = {}
    for repo in repos:
        dbp = os.path.join(repo["root"], "Directory.Packages.props")
        if os.path.isfile(dbp):
            xml = safe_read_text(dbp) or ""
            cpm_status[repo["name"]] = "ManagePackageVersionsCentrally" in xml
        else:
            cpm_status[repo["name"]] = False
    
    return {
        "versionConflicts": conflicts,
        "legacyFormatProjects": legacy_projects,
        "targetFrameworks": framework_groups,
        "centralPackageManagement": cpm_status,
        "totalPackages": len(pkg_versions),
        "conflictCount": len(conflicts),
        "legacyCount": len(legacy_projects),
    }
```

#### Step 5: Save output

In `main()` of `analyze.py`, after `build_graph()`:

```python
nuget_health = build_nuget_health(all_package_deps, all_project_meta, repos)
Path(os.path.join(OUT_DIR, "nuget-health.json")).write_text(
    json.dumps(nuget_health, indent=2), encoding="utf-8"
)
print(f"  NuGet health: {nuget_health['conflictCount']} version conflicts, "
      f"{nuget_health['legacyCount']} legacy format projects")
```

#### Step 6: Add "NuGet Health" tab to viewer

In `generate_docs.py`, load `nuget-health.json` and add a tab with:

- **Version conflict table** — sortable by package name, version count, project count. Click a row to expand and see which projects use which version.
- **Legacy projects list** — projects still on `packages.config`, with a "Migrate to PackageReference" recommendation.
- **Target framework summary** — group projects by framework, flag `net48`/`netstandard2.0` alongside `net8.0` as migration candidates.
- **CPM status** — per-repo badge: ✅ using Central Package Management or ❌ not using it.

### Files to Modify

- `analyze.py` — extract `targetFramework`, `nugetFormat`, add `build_nuget_health()`, save `nuget-health.json`
- `generate_docs.py` — load `nuget-health.json`, add "NuGet Health" tab with table + summary

### Dependencies

- None beyond existing `analyze.py` run. All data is already read during the scan.

---

## Feature 3: UX Inconsistency Detection

### Problem

The financial pricer codebase has WPF desktop applications. `analyze.py` already scans XAML files (`discover_xaml_bindings()`) and ViewModel classes (`extract_viewmodel_properties()`) and traces field-level chains (XAML → ViewModel → Entity → DB). But it only reports **what exists** — it never checks for **what's broken or inconsistent** across the UI layer. Broken bindings, orphan ViewModels, and inconsistent patterns are invisible.

### What Already Exists

- `discover_xaml_bindings()` returns a list of views with:
  - `viewType` (x:Class), `dataContextType`, `bindings[].path`, `bindings[].line`
- `extract_viewmodel_properties()` returns a list of ViewModel classes with:
  - `className`, `properties[].propertyName`, `properties[].propertyType`
- `build_field_chains()` already does partial cross-referencing (XAML binding → ViewModel property matching) but only for traceability, not error detection
- The XAML pattern detection (`WPF.Window`, `WPF.Binding`, `WPF.ViewModel`) in `ENHANCED_DATA_PATTERNS` identifies which projects have UI code

### Implementation Steps

#### Step 1: Add `detect_ux_inconsistencies()` in `analyze.py`

This runs **after** `discover_xaml_bindings()` and `extract_viewmodel_properties()` have completed, cross-referencing their outputs:

```python
def detect_ux_inconsistencies(
    xaml_views: list[dict],
    viewmodel_classes: list[dict],
    entity_classes: list[dict],
    project_meta: list[dict],
) -> dict:
    """Cross-reference XAML bindings with ViewModel properties to find inconsistencies
    in the scanned target codebase."""
    
    issues = []
    
    # Build lookup: ViewModel className -> properties
    vm_lookup = {}
    for vm in viewmodel_classes:
        vm_lookup[vm["className"]] = {
            "file": vm["file"],
            "project": vm.get("project"),
            "properties": {p["propertyName"] for p in vm["properties"]},
            "property_details": vm["properties"],
        }
    
    # Track which ViewModels are referenced by views
    referenced_vms = set()
    
    for view in xaml_views:
        dc_type = view.get("dataContextType")
        view_type = view.get("viewType")
        bindings = view.get("bindings", [])
        
        # Issue 1: View with bindings but no DataContext declared
        if bindings and not dc_type:
            issues.append({
                "type": "missing_datacontext",
                "severity": "warning",
                "file": view["file"],
                "project": view.get("project"),
                "viewType": view_type,
                "bindingCount": len(bindings),
                "message": f"View '{view_type}' has {len(bindings)} bindings but no DataContext type declared",
            })
            continue
        
        if dc_type:
            referenced_vms.add(dc_type)
        
        # Issue 2: DataContext references a ViewModel that doesn't exist
        if dc_type and dc_type not in vm_lookup:
            issues.append({
                "type": "missing_viewmodel",
                "severity": "error",
                "file": view["file"],
                "project": view.get("project"),
                "viewType": view_type,
                "dataContextType": dc_type,
                "message": f"View '{view_type}' references ViewModel '{dc_type}' which was not found",
            })
            continue
        
        # Issue 3: Broken bindings — binding path doesn't match any ViewModel property
        if dc_type and dc_type in vm_lookup:
            vm_props = vm_lookup[dc_type]["properties"]
            for binding in bindings:
                prop_name = binding["path"].split(".")[0]  # handle dotted paths
                if prop_name not in vm_props:
                    issues.append({
                        "type": "broken_binding",
                        "severity": "error",
                        "file": view["file"],
                        "project": view.get("project"),
                        "viewType": view_type,
                        "bindingPath": binding["path"],
                        "line": binding["line"],
                        "dataContextType": dc_type,
                        "availableProperties": sorted(vm_props)[:10],
                        "message": f"Binding '{binding['path']}' in '{view_type}' has no matching property in '{dc_type}'",
                    })
    
    # Issue 4: Orphan ViewModels — ViewModel classes with no XAML view referencing them
    for vm_name, vm_info in vm_lookup.items():
        if vm_name not in referenced_vms:
            issues.append({
                "type": "orphan_viewmodel",
                "severity": "info",
                "file": vm_info["file"],
                "project": vm_info.get("project"),
                "className": vm_name,
                "propertyCount": len(vm_info["properties"]),
                "message": f"ViewModel '{vm_name}' has no XAML view referencing it as DataContext",
            })
    
    # Issue 5: Mixed property notification patterns within a single project
    # (ViewModelBase vs ObservableObject vs INotifyPropertyChanged vs ReactiveObject)
    # This requires extracting the base class from the ViewModel class declaration
    # regex match — extend extract_viewmodel_properties() to also return the base class name
    # For now, this is a TODO placeholder
    
    # Build summary
    by_type = {}
    for issue in issues:
        t = issue["type"]
        by_type[t] = by_type.get(t, 0) + 1
    
    by_severity = {}
    for issue in issues:
        s = issue["severity"]
        by_severity[s] = by_severity.get(s, 0) + 1
    
    by_project = {}
    for issue in issues:
        p = issue.get("project", "_unknown")
        by_project[p] = by_project.get(p, 0) + 1
    
    return {
        "issues": issues,
        "summary": {
            "totalIssues": len(issues),
            "byType": by_type,
            "bySeverity": by_severity,
            "byProject": by_project,
            "viewsScanned": len(xaml_views),
            "viewModelsScanned": len(viewmodel_classes),
        },
    }
```

#### Step 2: Call it from `analyze.py` main

Currently `discover_xaml_bindings()` and `extract_viewmodel_properties()` are called inside `build_field_chains()` and their results aren't returned to `main()`. Refactor:

- Call `discover_xaml_bindings()` and `extract_viewmodel_properties()` separately in `main()` before `build_field_chains()`
- Pass the results to both `build_field_chains()` and `detect_ux_inconsistencies()`
- This avoids re-scanning — those functions scan `.xaml` and `.cs` files which is the expensive part. Call them once, use the results twice.

```python
# In main(), after data pattern discovery:
print("\nStep N: Scanning XAML bindings and ViewModels...")
xaml_views = discover_xaml_bindings(SCAN_ROOT, repos, all_project_meta)
viewmodel_classes = extract_viewmodel_properties(SCAN_ROOT, repos, all_project_meta)
entity_classes = extract_entity_properties(SCAN_ROOT, repos, data_findings, all_project_meta)

# Existing field chain building — pass pre-computed data instead of re-scanning
field_chains = build_field_chains_from_data(xaml_views, viewmodel_classes, entity_classes, ...)

# NEW: cross-reference for inconsistencies
print("\nStep N+1: Detecting UX inconsistencies...")
ux_issues = detect_ux_inconsistencies(xaml_views, viewmodel_classes, entity_classes, all_project_meta)
Path(os.path.join(OUT_DIR, "ux-inconsistencies.json")).write_text(
    json.dumps(ux_issues, indent=2), encoding="utf-8"
)
print(f"  UX issues: {ux_issues['summary']['totalIssues']} "
      f"({ux_issues['summary']['bySeverity'].get('error', 0)} errors, "
      f"{ux_issues['summary']['bySeverity'].get('warning', 0)} warnings)")
```

#### Step 3: Add "UX Consistency" tab to viewer

In `generate_docs.py`, load `ux-inconsistencies.json` and add a tab:

**Section A — Summary**:
- Error/Warning/Info counts as colored badges
- Views scanned vs ViewModels scanned
- Projects with most issues

**Section B — Issue table** (sortable, filterable):

| Column | Source |
|--------|--------|
| Severity | `issues[].severity` — rendered as colored dot (🔴 error, 🟡 warning, 🔵 info) |
| Type | `issues[].type` — human-readable label |
| Project | `issues[].project` |
| File | `issues[].file` |
| Message | `issues[].message` |
| Line | `issues[].line` (where applicable) |

Add filter buttons: "Errors only", "Warnings+", "All" — same pattern as the hotspot risk badges.

**Section C — Broken binding detail**:
When clicking a broken_binding row, show:
- The XAML file and line
- The binding path that failed
- The DataContext ViewModel class
- The list of available properties on that ViewModel (so the developer can see what the correct binding should be)

### Files to Modify

- `analyze.py` — add `detect_ux_inconsistencies()`, refactor `build_field_chains()` to accept pre-scanned data, save `ux-inconsistencies.json`
- `generate_docs.py` — load `ux-inconsistencies.json`, add "UX Consistency" tab

### Dependencies

- Only runs on repos that have WPF/XAML content (skip gracefully if no `.xaml` files found)
- Requires `analyze.py` to have run (uses same scan pass)

### Limitations / Known Gaps

- **Regex-based**: Cannot resolve dynamic DataContext assignments (set in code-behind, DI, or at runtime)
- **Single-file ViewModel detection**: If a ViewModel is defined across partial classes, properties from the other partial won't be found
- **No converter awareness**: Bindings using `IValueConverter` may look "broken" because the binding path targets a different type
- **Inheritance blind**: If ViewModel inherits properties from a base class in a different file, those won't be in the property list
- **Confidence**: Mark broken_binding issues with a `confidence` field — "high" if DataContext is explicitly declared, "medium" if inferred from naming convention

---

## Execution Order

```
Phase 1 (Quick Win):
  Feature 2 — NuGet Modernization
  - Modify: analyze.py, generate_docs.py
  - Low effort, all data already collected
  - Adds nuget-health.json output + viewer tab
  - Immediately useful: version conflicts surface real build/runtime issues

Phase 2 (High Impact):
  Feature 1 — Code Smell Visualization
  - Modify: generate_docs.py only
  - Medium effort, data pipeline fully exists
  - Wires refactoring-targets.json into viewer
  - Makes the refactoring triage output actionable in the viewer

Phase 3 (Deep Analysis):
  Feature 3 — UX Inconsistency Detection
  - Modify: analyze.py, generate_docs.py
  - Medium effort, requires refactoring build_field_chains() internals
  - Cross-references XAML and ViewModel data
  - Most valuable for WPF-heavy financial pricer apps
```

## Files Modified Per Feature

| Feature | `analyze.py` | `refactor_triage.py` | `generate_docs.py` | `visualize.py` |
|---------|:---:|:---:|:---:|:---:|
| 1 — Code Smell Viz | — | — | ✅ | — |
| 2 — NuGet Health | ✅ | — | ✅ | — |
| 3 — UX Inconsistency | ✅ | — | ✅ | — |

## Output Files Summary

After all three features, the output directory will contain:

```
output-{name}/
├── (existing files)
├── refactoring-targets.json    # Already exists from refactor_triage.py
├── refactoring-report.md       # Already exists from refactor_triage.py
├── nuget-health.json           # NEW — version conflicts, legacy format, frameworks
├── ux-inconsistencies.json     # NEW — broken bindings, orphan VMs, missing DataContexts
└── viewer.html                 # UPDATED — 3 new tabs: "Code Quality", "NuGet Health", "UX Consistency"
```

## Testing Strategy

For each feature, test against the existing test repos:

| Test Repo | Projects | Why |
|-----------|----------|-----|
| **eShop** | 24 | API routes, no WPF — tests graceful skip of UX detection |
| **OrchardCore** | 230 | Large, many NuGet deps — stress tests version conflict detection |
| **StockSharp** | 140 | Has WPF UI + financial patterns — tests all 3 features |
| **Target codebase** | ~200+ | The real 25GB pricer codebase — final validation |

For each test repo:
1. Run full pipeline: `analyze.py` → `refactor_triage.py` → `generate_docs.py`
2. Verify new JSON outputs exist and are valid
3. Serve viewer, check new tabs render correctly
4. Spot-check: do flagged issues look legitimate?