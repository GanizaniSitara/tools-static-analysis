# tools-static-analysis

Static analysis pipeline for .NET codebases. Scan → visualize → review in browser → point Claude Code at specific repos.

## Usage

```bash
# 1. Scan .csproj/.xaml/.config — dependencies, refs, data patterns, traceability, UX, NuGet health
python3 1_scan_projects.py /path/to/repos output-myproject

# 2. Scan .cs source — code smells, complexity, refactoring targets
python3 2_scan_smells.py /path/to/repos output-myproject

# 3. Generate Mermaid/GraphViz diagrams from graph.json
python3 3_gen_diagrams.py output-myproject

# 4. Generate viewer.html, markdown docs, and AI context files
python3 4_gen_docs.py output-myproject
```

Steps 1-2 scan source and can run in parallel. Step 3 needs graph.json from step 1. Step 4 reads all outputs, so run it last.

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
| `refactoring-targets.json` | 2_scan_smells | Code smells, complexity, Claude Code prompts |
| `viewer.html` | 4_gen_docs | Interactive browser viewer with all tabs |
| `docs/ai-context/` | 4_gen_docs | Per-project markdown for AI coding agents |
