# Project Rules

## Git Discipline
- **Commit after every meaningful change.** Every feature, fix, or refactor gets its own commit BEFORE moving on.
- Never let working changes accumulate without a commit.
- If a change might need to be rolled back, it absolutely must be committed first.
- Use descriptive commit messages summarizing the what and why.

## Project Overview
- Static analysis tool for .NET solutions: `1_scan_projects.py` → `2_scan_smells.py` → `3_gen_diagrams.py` → `4_gen_docs.py`
- `1_scan_projects.py`: Scans .csproj/.xaml/.config files — dependencies, project refs, data patterns, field traceability, UX consistency, NuGet health
- `2_scan_smells.py`: Scans .cs source files for complexity metrics and code smells, generates refactoring targets
- `3_gen_diagrams.py`: Generates Mermaid (.mmd) and GraphViz (.dot) diagrams from graph.json
- `4_gen_docs.py`: Generates markdown docs, `viewer.html` (interactive HTML viewer), and AI context files
- Output directories: `output-{name}/` with JSON, CSV, diagrams/, docs/, viewer.html
