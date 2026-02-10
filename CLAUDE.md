# Project Rules

## Git Discipline
- **Commit after every meaningful change.** Every feature, fix, or refactor gets its own commit BEFORE moving on.
- Never let working changes accumulate without a commit.
- If a change might need to be rolled back, it absolutely must be committed first.
- Use descriptive commit messages summarizing the what and why.

## Project Overview
- Static analysis tool for .NET solutions: `analyze.py` -> `visualize.py` -> `generate_docs.py`
- `analyze.py`: Scans .csproj files, extracts dependencies, project refs, data patterns
- `visualize.py`: Generates Mermaid (.mmd) and GraphViz (.dot) diagrams
- `generate_docs.py`: Generates markdown docs and `viewer.html` (interactive HTML viewer)
- Output directories: `output-{name}/` with JSON, CSV, diagrams/, docs/, viewer.html
