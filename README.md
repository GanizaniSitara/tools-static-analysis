# tools-static-analysis

Static analysis pipeline for .NET codebases. Scan → visualize → review in browser → point Claude Code at specific repos.

## Usage

```bash
# 1. Scan .csproj/.xaml/.config — dependencies, refs, data patterns, traceability, UX, NuGet health
python3 1_scan_projects.py /path/to/repos output-myproject

# 2. Scan .cs source — code smells, security detectors, complexity, refactoring targets
python3 2_scan_smells.py /path/to/repos output-myproject --level high

# 3. Generate Mermaid/GraphViz diagrams from graph.json
python3 3_gen_diagrams.py output-myproject

# 4. Generate viewer.html, markdown docs, and AI context files
python3 4_gen_docs.py output-myproject
```

Steps 1-2 scan source and can run in parallel. Step 3 needs graph.json from step 1. Step 4 reads all outputs, so run it last.

### Severity levels (`--level`)

The smell scanner supports log-level-style verbosity via `--level critical|high|medium|low` (default: `high`). Each level includes all levels above it.

| Level | What runs | Typical use |
|-------|-----------|-------------|
| `critical` | Security only (hardcoded secrets, SQL injection, insecure deserialization, command injection) | CI gate for must-fix vulnerabilities |
| `high` | Critical + high-severity security (weak crypto, open redirect, XSS, insecure random) + bugs (exception swallowing, sync-over-async) | **Default** — actionable findings without noise |
| `medium` | High + code quality (god methods, deep nesting, long parameter lists) | Sprint planning |
| `low` | All detectors including style (magic numbers, missing null checks, mutable shared state) | Full audit |

The `run.py` pipeline also accepts `--level`:

```bash
python3 run.py /path/to/repos output-myproject --level medium
```

### Serve-only mode (`--serve-only`)

If you've already run the pipeline and just want the web server (with IDE integration endpoints for the Claude/VS Code/View buttons), use `--serve-only` to skip the scan steps:

```bash
python3 run.py dummy output-myproject 8001 --serve-only
```

This starts the custom HTTP server immediately on existing output — no re-scanning. A plain `python -m http.server` serves the viewer but the file action buttons (open in Claude Code, VS Code, Visual Studio, view source) require `run.py`'s server.

## Outputs (in `output-myproject/`)

| File | Producer | Description |
|------|----------|-------------|
| `graph.json` | 1_scan_projects | Dependency graph (nodes + edges) |
| `project-meta.json` | 1_scan_projects | Per-project metadata (category, targetFramework, nugetFormat) |
| `data-sources.json` | 1_scan_projects | Data access patterns (SQL, HTTP, messaging) |
| `data-flow.json` | 1_scan_projects | Data flow graph with implied dependencies |
| `flow-paths.json` | 1_scan_projects | End-to-end flow paths (Presentation → Data) |
| `field-traceability.json` | 1_scan_projects | XAML → ViewModel → Entity → DB column chains |
| `ux-inconsistencies.json` | 1_scan_projects | MVVM binding issues (broken bindings, orphan VMs) |
| `nuget-health.json` | 1_scan_projects | Version conflicts, legacy formats, framework analysis |
| `refactoring-targets.json` | 2_scan_smells | Code smells, security findings, complexity, Claude Code prompts |
| `viewer.html` | 4_gen_docs | Interactive browser viewer with all tabs (incl. Security tab) |
| `docs/ai-context/` | 4_gen_docs | Per-project markdown for AI coding agents |
