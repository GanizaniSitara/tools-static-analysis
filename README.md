# tools-static-analysis

Static analysis pipeline for .NET codebases. Scan → visualize → review in browser → point Claude Code at specific repos.

## Usage

```bash
# 1. Analyze dependencies, data patterns, field traceability, UX consistency, NuGet health
python3 analyze.py /path/to/repos output-myproject

# 2. Scan C# source for code smells and refactoring targets
python3 refactor_triage.py /path/to/repos output-myproject

# 3. Generate Mermaid/GraphViz diagrams
python3 visualize.py output-myproject

# 4. Generate viewer.html, markdown docs, and AI context files
python3 generate_docs.py output-myproject
```

Steps 1-3 can run in any order. Step 4 reads from the output directory, so run it last.

## Outputs (in `output-myproject/`)

| File | Producer | Description |
|------|----------|-------------|
| `graph.json` | analyze.py | Dependency graph (nodes + edges) |
| `project-meta.json` | analyze.py | Per-project metadata (category, targetFramework, nugetFormat) |
| `data-sources.json` | analyze.py | Data access patterns (SQL, HTTP, messaging) |
| `data-flow.json` | analyze.py | Data flow graph with implied dependencies |
| `flow-paths.json` | analyze.py | End-to-end flow paths (Presentation → Data) |
| `field-traceability.json` | analyze.py | XAML → ViewModel → Entity → DB column chains |
| `ux-inconsistencies.json` | analyze.py | MVVM binding issues (broken bindings, orphan VMs) |
| `nuget-health.json` | analyze.py | Version conflicts, legacy formats, framework analysis |
| `refactoring-targets.json` | refactor_triage.py | Code smells, complexity, Claude Code prompts |
| `viewer.html` | generate_docs.py | Interactive browser viewer with all tabs |
| `docs/ai-context/` | generate_docs.py | Per-project markdown for AI coding agents |
