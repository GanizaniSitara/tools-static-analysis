# Pipeline Overview

## What This Tool Does

This is a static analysis pipeline for .NET solutions. It scans C# source code, project
files, and configuration files to produce an interactive browser-based report covering:

- Dependency graphs and project relationships
- Security vulnerabilities (OWASP-aligned)
- Code quality metrics and refactoring targets
- Resilience posture (fault tolerance gaps)
- Data flow and field traceability
- UX consistency (MVVM binding issues)
- NuGet health (version conflicts, legacy formats)

The output is a single `viewer.html` file with no external dependencies -- open it in any
browser to explore all findings interactively.

## Pipeline Steps

```
Step 1                 Step 2               Step 6              Step 3           Step 4
1_scan_projects.py --> 2_scan_smells.py --> 6_scan_resilience --> 3_gen_diagrams --> 4_gen_docs.py
       |                    |                    |                    |                |
       v                    v                    v                    v                v
  graph.json          refactoring-         resilience-          diagrams/        viewer.html
  project-meta.json   targets.json         findings.json        *.mmd            docs/
  data-sources.json   triage.json                               *.dot            ai-context/
  data-flow.json      refactoring-
  flow-paths.json     report.md
  field-trace.json
  ux-inconsistencies.json
  nuget-health.json

                     Optional:
                     5_external_tools.py --> external-tools.json
```

### Step 1: Scan Projects (`1_scan_projects.py`)

**Input**: Directory tree containing .NET repositories

**Scans**: `.csproj`, `.xaml`, `.config`, `.json`, `.props`, `.targets` files

**Produces**:
- `graph.json` -- Dependency graph (project nodes + reference edges)
- `project-meta.json` -- Per-project metadata (category, target framework, NuGet format)
- `data-sources.json` -- Data access patterns (SQL, HTTP, messaging, file I/O)
- `data-flow.json` -- Data flow graph with implied dependencies
- `flow-paths.json` -- End-to-end flow paths (Presentation to Data)
- `field-traceability.json` -- XAML binding to ViewModel to Entity to DB column chains
- `ux-inconsistencies.json` -- MVVM binding issues (broken bindings, orphan ViewModels)
- `nuget-health.json` -- Version conflicts, legacy formats, framework analysis
- `dependencies.csv` -- Flat list of NuGet dependencies per project
- `repos.json` -- Repository metadata (roots, names)

### Step 2: Scan Smells (`2_scan_smells.py`)

**Input**: Same directory tree + output from Step 1

**Scans**: `.cs` source files

**Produces**:
- `refactoring-targets.json` -- Per-project, per-file findings with severity, category,
  complexity metrics, refactoring value scores, and Claude Code prompt templates
- `triage.json` -- Persistent finding dispositions (see [triage-system.md](triage-system.md))
- `refactoring-report.md` -- Human-readable markdown report

**Detectors**: 19 detectors across 4 severity tiers. See [security-detectors.md](security-detectors.md)
for the complete list with false positive suppression logic.

**Severity filtering**: `--level critical|high|medium|low` (default: `high`)

### Step 3: Generate Diagrams (`3_gen_diagrams.py`)

**Input**: `graph.json` from Step 1

**Produces**:
- `diagrams/*.mmd` -- Mermaid diagrams (overview, per-category, data flow, business layers,
  E2E flows, field traceability)
- `diagrams/*.dot` -- GraphViz diagrams (landscape view)
- `all-diagrams.md` -- Combined markdown with all diagrams

### Step 4: Generate Docs (`4_gen_docs.py`)

**Input**: All JSON outputs from Steps 1-3 + optional external tools output

**Produces**:
- `viewer.html` -- Interactive HTML viewer with all panels, filters, and triage controls
- `docs/` -- Per-project markdown documentation
- `docs/ai-context/` -- AI-optimized context files for each project

### Step 5: External Tools (`5_external_tools.py`) -- Optional

**Input**: Same directory tree

**Runs**: Any combination of `semgrep`, `bandit`, `detect-secrets`, `radon` (if installed)

**Produces**: `external-tools.json` -- Merged findings from all tools. Security findings
also appear in the Security tab of `viewer.html`.

### Step 6: Resilience Scanner (`6_scan_resilience.py`)

**Input**: Same directory tree + output from Step 1

**Scans**: `.cs` source files for fault tolerance patterns

**Produces**:
- `resilience-findings.json` -- Per-project resilience scores, findings, positive patterns
- `resilience-report.md` -- Human-readable report

See [resilience-scanner-design.md](resilience-scanner-design.md) for full detector documentation.

## Running the Pipeline

### All-in-one (recommended)

```bash
python3 run.py /path/to/repos output-myproject
```

This runs all steps in order and starts a web server on port 8000 with IDE integration.

### With external tools

```bash
python3 run.py /path/to/repos output-myproject --tools all
```

### Individual steps

```bash
python3 1_scan_projects.py /path/to/repos output-myproject
python3 2_scan_smells.py /path/to/repos output-myproject --level high
python3 6_scan_resilience.py /path/to/repos output-myproject
python3 3_gen_diagrams.py output-myproject
python3 4_gen_docs.py output-myproject
```

Steps 1, 2, and 6 scan source and can run in parallel. Step 3 needs `graph.json` from
Step 1. Step 4 reads all outputs, so run it last.

## Output Directory Structure

```
output-myproject/
  graph.json                    # Dependency graph
  project-meta.json             # Project metadata
  data-sources.json             # Data access patterns
  data-flow.json                # Data flow graph
  flow-paths.json               # E2E flow paths
  field-traceability.json       # XAML-to-DB field chains
  ux-inconsistencies.json       # MVVM binding issues
  nuget-health.json             # NuGet version/format analysis
  dependencies.csv              # Flat NuGet dependency list
  repos.json                    # Repository metadata
  refactoring-targets.json      # Code smells + security findings
  triage.json                   # Persistent triage dispositions
  refactoring-report.md         # Human-readable smell report
  resilience-findings.json      # Resilience posture per project
  resilience-report.md          # Human-readable resilience report
  external-tools.json           # External tool findings (if run)
  viewer.html                   # Interactive browser viewer
  diagrams/
    overview.mmd                # Category-level Mermaid diagram
    category-*.mmd              # Per-category Mermaid diagrams
    data-flow.mmd               # Data flow diagram
    business-layers.mmd         # Business layer classification
    e2e-flows.mmd               # End-to-end flow paths
    field-traceability.mmd      # Field trace diagram
    landscape.dot               # GraphViz landscape view
    all-diagrams.md             # Combined markdown
  docs/
    index.md                    # Documentation index
    *.md                        # Per-project documentation
    ai-context/
      *.md                      # AI-optimized project context files
```

## Viewer Panels

The `viewer.html` interactive report contains these panels:

| Panel | Data Source | What It Shows |
|-------|-----------|---------------|
| All Projects | `graph.json`, `project-meta.json` | Sortable project table with category, framework, dependencies |
| Diagrams | `diagrams/*.mmd` | Interactive Mermaid diagrams with pan/zoom |
| Data Sources | `data-sources.json` | Data access patterns by type (SQL, HTTP, messaging) |
| Connection Strings | `configs.json` | Database connection strings found in config files |
| Code Quality | `refactoring-targets.json`, `triage.json` | Code smells with severity filtering, triage controls, refactoring targets |
| Security | `refactoring-targets.json`, `external-tools.json` | Security findings with triage status, severity filtering |
| Resilience | `resilience-findings.json` | Resilience scores, external call analysis, policy detection |
| Hotspots | computed from `graph.json` | Coupling-based hotspot detection |
| External Tools | `external-tools.json` | Semgrep, Bandit, detect-secrets, Radon findings |
| NuGet Health | `nuget-health.json` | Version conflicts, outdated packages, framework analysis |
| UX Consistency | `ux-inconsistencies.json` | MVVM binding issues |

Each panel supports:
- Global search (top search bar filters across all panels)
- Repository filter (multi-repo scans show a repo selector)
- Severity filtering (click severity badges to filter)
- Sortable columns (click column headers)
- Expandable detail rows (click project rows for file-level details)

## What This Tool Does NOT Do

- **Does not modify source code.** This is a read-only analysis tool. All code changes
  happen through your IDE or AI coding assistant.
- **Does not replace security scanners like ArmorCode.** The built-in detectors use regex
  pattern matching, not dataflow analysis. They catch common patterns but may miss complex
  vulnerabilities. Use this tool for rapid triage and prioritization; use dedicated SAST
  tools for depth.
- **Does not require .NET SDK.** The tool is pure Python (standard library only). It reads
  source files as text, not compiled binaries.
- **Does not phone home.** No telemetry, no network calls. All analysis runs locally.
  The viewer is a self-contained HTML file with inline CSS and JavaScript.

## Prerequisites

- Python 3.10+
- No pip packages required for the core pipeline
- Optional: `semgrep`, `bandit`, `detect-secrets`, `radon` for external tool integration
- Optional: Node.js (for `node --check` JS syntax verification during development)
