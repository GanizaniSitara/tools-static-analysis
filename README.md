# tools-static-analysis

Static analysis pipeline for .NET codebases. Scan â†’ visualize â†’ review in browser â†’ point Claude Code at specific repos.

## Prerequisites

Python 3.10+ with no additional packages required â€” the core pipeline uses only the standard library.

### Optional: external analysis tools

For deeper security and quality coverage, install any combination of:

```bash
pip install semgrep bandit detect-secrets radon
```

These are entirely optional. The pipeline works without them and skips any that aren't installed.

## Quick start

### 0. Download demo datasets (optional)

If you want sample repositories for demos or validation runs, use the bootstrap helper:

```text
python bootstrap-demo-datasets.py --list
python bootstrap-demo-datasets.py --all
python bootstrap-demo-datasets.py --csharp
python bootstrap-demo-datasets.py --java
python bootstrap-demo-datasets.py --csharp eshop --java spring-petclinic
```

See [BOOTSTRAP_README.md](BOOTSTRAP_README.md) for the full dataset guide.

### 1. Run the analysis pipeline

The simplest way to run everything is via `run.py`:

```bash
# Core pipeline only (no external tools)
python3 run.py /path/to/repos output-myproject

# Core pipeline + all available external tools
python3 run.py /path/to/repos output-myproject --tools all

# Core pipeline + specific tools only
python3 run.py /path/to/repos output-myproject --tools semgrep,bandit
```

This runs all steps in order and starts a web server on port 8000 with IDE integration (Claude Code, VS Code, Visual Studio, view source buttons).

### 2. Validate the viewer as a user

For a realistic manual test on Windows:

```powershell
python bootstrap-demo-datasets.py --all --output C:/demo-projects
python run.py C:/demo-projects output-demo-all 8021
```

Then open:

```text
http://127.0.0.1:8021/viewer.html
```

Recommended manual checks:

- multi-repo runs should start on the `Repos` tab
- the header selector should read `Folder`, not appear as an unlabeled pill control
- the folder dropdown should show `Choose folder...`, explicit repo names, and `All Folders`
- choosing a repo from the dropdown should always return to `Overview`, even after prior repo switches
- changing repo should clear tab-local search, severity, triage, and detail-panel state before applying the new repo context
- `Focus` buttons in the `Repos` tab should behave the same way as the dropdown
- editor launch actions use the local `run.py` server by default; if you want the standalone companion, start `node companion/server.js`

Windows note:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python run.py C:/demo-projects output-demo-all 8021
```

Use the UTF-8 environment variables above if redirected output fails with a `UnicodeEncodeError`.

## Running individual steps

```bash
# 1. Scan .csproj/.xaml/.config â€” dependencies, refs, data patterns, traceability, UX, NuGet health
python3 1_scan_projects.py /path/to/repos output-myproject

# 2. Scan .cs source â€” code smells, security detectors, complexity, refactoring targets
python3 2_scan_smells.py /path/to/repos output-myproject --level high

# 3. (Optional) Run external tools â€” semgrep, bandit, detect-secrets, radon
python3 5_external_tools.py /path/to/repos output-myproject --tools all

# 4. Generate Mermaid/GraphViz diagrams from graph.json
python3 3_gen_diagrams.py output-myproject

# 5. Generate viewer.html, markdown docs, and AI context files
python3 4_gen_docs.py output-myproject
```

Steps 1-2 scan source and can run in parallel. Step 3 (external tools) can run any time after steps 1-2. Step 4 needs graph.json from step 1. Step 5 reads all outputs (including `external-tools.json` if present), so run it last.

### Severity levels (`--level`)

The smell scanner supports log-level-style verbosity via `--level critical|high|medium|low` (default: `high`). Each level includes all levels above it.

| Level | What runs | Typical use |
|-------|-----------|-------------|
| `critical` | Security only (hardcoded secrets, SQL injection, insecure deserialization, command injection) | CI gate for must-fix vulnerabilities |
| `high` | Critical + high-severity security (weak crypto, open redirect, XSS, insecure random) + bugs (exception swallowing, sync-over-async) | **Default** â€” actionable findings without noise |
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

This starts the custom HTTP server immediately on existing output â€” no re-scanning. A plain `python -m http.server` serves the viewer but the file action buttons (open in Claude Code, VS Code, Visual Studio, view source) require `run.py`'s server.

In multi-repo runs, the initial landing tab is `Repos`. Use the folder dropdown or the `Focus` buttons there to move into `Overview`.

### External tools (`--tools`)

Off by default. Pass `--tools all` to run every installed tool, or a comma-separated list for specific ones. Tools not found in PATH are skipped with a warning.

| Tool | What it checks | Category |
|------|---------------|----------|
| `semgrep` | Pattern-based security and correctness rules | security |
| `bandit` | Python security linter | security |
| `detect-secrets` | Hardcoded secrets and credentials | security |
| `radon` | Cyclomatic complexity and maintainability index | quality |

Findings appear in an **External Tools** tab in the viewer, and security-category findings are also merged into the **Security** tab. Output is written to `external-tools.json`.

## Outputs (in `output-myproject/`)

| File | Producer | Description |
|------|----------|-------------|
| `graph.json` | 1_scan_projects | Dependency graph (nodes + edges) |
| `project-meta.json` | 1_scan_projects | Per-project metadata (category, targetFramework, nugetFormat) |
| `data-sources.json` | 1_scan_projects | Data access patterns (SQL, HTTP, messaging) |
| `data-flow.json` | 1_scan_projects | Data flow graph with implied dependencies |
| `flow-paths.json` | 1_scan_projects | End-to-end flow paths (Presentation â†’ Data) |
| `field-traceability.json` | 1_scan_projects | XAML â†’ ViewModel â†’ Entity â†’ DB column chains |
| `ux-inconsistencies.json` | 1_scan_projects | MVVM binding issues (broken bindings, orphan VMs) |
| `nuget-health.json` | 1_scan_projects | Version conflicts, legacy formats, framework analysis |
| `refactoring-targets.json` | 2_scan_smells | Code smells, security findings, complexity, Claude Code prompts |
| `external-tools.json` | 5_external_tools | External tool findings (semgrep, bandit, detect-secrets, radon) |
| `viewer.html` | 4_gen_docs | Interactive browser viewer with all tabs (incl. Security tab) |
| `docs/ai-context/` | 4_gen_docs | Per-project markdown for AI coding agents |





