# Project Rules

## Git Discipline
- **Commit after every meaningful change.** Every feature, fix, or refactor gets its own commit BEFORE moving on.
- Never let working changes accumulate without a commit.
- If a change might need to be rolled back, it absolutely must be committed first.
- Use descriptive commit messages summarizing the what and why.
- **Never commit plan/design .md files.** Plans live in conversation context only, not in the repo.
- **Always raise PRs to GanizaniSitara/tools-static-analysis** (origin), not the fork. Push to `fork` remote, PR into `origin/main`.

## Testing Pipeline
- **Always test on all three repos before raising a PR:** eShop, StockSharp, OrchardCore
- Run the full pipeline: `1_scan_projects.py` → `2_scan_smells.py` → `3_gen_diagrams.py` → `4_gen_docs.py`
- Verify: no errors, sensible output counts, viewer.html JS syntax check passes
- JS syntax check: extract `<script>` blocks and run `node --check`

## Code Style
- **Never use emojis** in code, HTML, documentation, or any generated output

## Project Overview
- Static analysis tool for .NET solutions: `1_scan_projects.py` → `2_scan_smells.py` → `3_gen_diagrams.py` → `4_gen_docs.py`
- `1_scan_projects.py`: Scans .csproj/.xaml/.config files — dependencies, project refs, data patterns, field traceability, UX consistency, NuGet health
- `2_scan_smells.py`: Scans .cs source files for complexity metrics and code smells, generates refactoring targets
- `3_gen_diagrams.py`: Generates Mermaid (.mmd) and GraphViz (.dot) diagrams from graph.json
- `4_gen_docs.py`: Generates markdown docs, `viewer.html` (interactive HTML viewer), and AI context files
- Output directories: `output-{name}/` with JSON, CSV, diagrams/, docs/, viewer.html
