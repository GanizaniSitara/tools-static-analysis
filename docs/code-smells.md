# Code Smells, Complexity Metrics, and Refactoring Targets

## Purpose

`2_scan_smells.py` scans every `.cs` file in the target repositories and produces:

1. **Complexity metrics** per file (cyclomatic complexity, nesting depth, method count)
2. **Smell findings** per file (19 detectors across security, bugs, quality, interop, style)
3. **Refactoring value scores** per project (weighted combination of complexity, smells, coupling, test gaps)
4. **Prioritized refactoring targets** with ready-to-use Claude Code prompts
5. **Triage state** persisted across scan runs (see [triage-system.md](triage-system.md))

## Complexity Metrics

Three metrics are computed for every scanned `.cs` file:

### Cyclomatic Complexity

Counts decision points in the file:

| Counted | Why |
|---------|-----|
| `if` | Branch |
| `else` | Branch |
| `switch` / `case` | Branch |
| `while` / `for` / `foreach` | Loop |
| `catch` | Exception path |
| `? :` (ternary) | Inline branch |
| `&&` / `\|\|` | Short-circuit evaluation |

Higher values mean more execution paths and harder-to-test code.

### Maximum Nesting Depth

Tracks the deepest level of brace nesting within the file, accounting for string
literals and character literals to avoid false positives from braces inside strings.

- Threshold: depth > 4 within a method triggers the `deep_nesting` detector
- The method's own brace level is subtracted (so `if { if { if { if { if {` = depth 5)

### Method Count and Long Methods

- **Method count**: Total method declarations found via pattern matching on access
  modifiers and signatures
- **Long methods**: Methods exceeding 50 lines (approximate, brace-based calculation)
- **God methods**: Subset of long methods exceeding 100 lines (flagged as a smell)

### Complexity Score Formula

Per file:

```
complexity_score = cyclomatic + (nesting_depth * 3) + (long_methods_count * 5)
```

The weights reflect that deep nesting and oversized methods are harder to address than
simple branching. A file with cyclomatic complexity 20, nesting depth 6, and 2 long
methods scores `20 + 18 + 10 = 48`.

## Refactoring Value Score

Projects are ranked by a composite score that combines code quality signals with
architectural importance:

```
score = (complexity_score * 2)
      + weighted_smell_score
      + (fan_in * fan_out) * 0.5
      + test_gap_penalty * 5
      - deprioritize_discount
```

### Score Components

| Component | Formula | Weight | Rationale |
|-----------|---------|--------|-----------|
| Complexity | Sum of all file complexity scores | x2 | Primary factor -- complex code needs the most attention |
| Smell severity | Sum of severity weights per finding | x1 | Critical=15, High=8, Medium=3, Low=1 per finding |
| Coupling | fan_in * fan_out | x0.5 | High coupling = changes ripple further |
| Test gap | 5 if no test project references this project | +5 | Untested complex code is higher risk |
| Deprioritize | -20 if category is test/sample/tool/localization | -20 | Reduce noise from non-production code |

### Severity Weights

| Severity | Points per Finding | Example |
|----------|-------------------|---------|
| Critical | 15 | One hardcoded secret = 15 pts |
| High | 8 | One sync-over-async = 8 pts |
| Medium | 3 | One god method = 3 pts |
| Low | 1 | One magic number = 1 pt |

A single critical security finding (15 pts) outweighs five low-severity style issues
(5 pts), keeping the ranking focused on what matters.

### Fan-In / Fan-Out

Loaded from `graph.json` (produced by `1_scan_projects.py`):

- **Fan-in**: Number of other projects that depend on this project
- **Fan-out**: Number of projects this project depends on
- **Coupling factor**: `fan_in * fan_out * 0.5`

A project with fan_in=8 and fan_out=3 adds `8 * 3 * 0.5 = 12` to its score. Changes
to highly coupled projects carry more risk.

### Test Gap Detection

The scanner checks whether the project has associated test projects:

1. **Preferred**: Reads `test-projects.json` if available
2. **Fallback**: Scans `graph.json` edges for projects with `"test"` in their category
   that reference this project

Projects with no detected test coverage get a +5 penalty.

### Deprioritization

Certain project categories and namespaces are discounted by 20 points:

**Categories**: `test`, `sample`, `localization`, `tool`

**Namespace patterns**:
- `*.Logging.*`, `*.Logger`
- `*.UI.Controls.*`, `*.UI.Infrastructure.*`
- `*.Xaml.*`, `*.Resources.*`

This prevents test harnesses and infrastructure projects from dominating the ranking.

### Financial Project Detection

Projects matching financial patterns get special attention:

```
Pricer, Pricing, Financial, Calc, Engine, Valuation,
Greeks, BlackScholes, MonteCarlo
```

These are flagged in the report and their `precision_unsafe_math` findings
(float/double instead of decimal) are highlighted.

## Tiered Refactoring Targets

Projects are sorted by score and assigned to tiers:

| Tier | Score Range | Effort | Included in Report |
|------|------------|--------|-------------------|
| Tier 1: Critical | > 100 | High | Up to 5 projects with full details |
| Tier 2: High | 50 -- 100 | Medium | Abbreviated list |
| Tier 3: Medium | 20 -- 50 | Low | Abbreviated list |
| Below threshold | < 20 | -- | Not included |

Each target includes:
- **Why**: Summary of what drives the score (e.g., "12 god_method, 8 sync_over_async,
  no test coverage, fan-in=8")
- **Suggested prompt**: Ready-to-paste Claude Code prompt for the refactoring session
- **Estimated effort**: High / Medium / Low
- **Key files**: Top 5 files by complexity

## File Exclusions

Before any detector runs, the scanner skips:

| What | Pattern | Why |
|------|---------|-----|
| Auto-generated | `*.Designer.cs`, `*.generated.cs`, `AssemblyInfo.cs` | No value in refactoring generated code |
| Build output | `obj/`, `bin/`, `node_modules/`, `packages/` | Not source code |
| Migrations | `Migrations/` | EF Core auto-generated |
| Tiny files | < 50 lines | Too small for meaningful analysis |
| Huge files | > 2 MB | Likely generated or binary-like |
| Deep paths | > 30 directory levels | Avoids pathological directory structures |

Additionally, these directories are skipped during traversal:
`.git`, `node_modules`, `bin`, `obj`, `packages`, `.vs`, `.idea`, `TestResults`,
`Debug`, `Release`, `publish`

## refactoring-targets.json Schema

The complete output structure:

```json
{
  "generated": "2026-02-28",
  "scanRoot": "/path/to/repos",
  "summary": {
    "totalFilesScanned": 1234,
    "totalFilesWithSmells": 456,
    "totalSmells": 2345,
    "topSmellTypes": [
      {"smell": "god_method", "count": 234}
    ],
    "topProjectsByScore": ["ProjectA", "ProjectB"],
    "severityCounts": {
      "critical": 45,
      "high": 234,
      "medium": 567,
      "low": 1234
    },
    "categoryCounts": {
      "security": 279,
      "bug": 234,
      "quality": 567,
      "interop": 45,
      "style": 1234
    },
    "triageCounts": {
      "unreviewed": 1500,
      "confirmed": 500,
      "false_positive": 100,
      "accepted_risk": 150,
      "fixed": 95
    },
    "level": "high"
  },
  "projects": [
    {
      "project": "Ordering.API",
      "repo": "eShop",
      "category": "core",
      "layer": "application",
      "fan_in": 5,
      "fan_out": 3,
      "has_tests": true,
      "total_files": 45,
      "total_lines": 12345,
      "complexity_score": 456,
      "smell_count": 67,
      "top_smells": ["god_method", "deep_nesting", "sync_over_async"],
      "refactoring_value_score": 234.5,
      "files": [
        {
          "path": "src/Services/OrderService.cs",
          "lines": 342,
          "cyclomatic": 28,
          "nesting_depth": 5,
          "method_count": 12,
          "long_methods": 2,
          "complexity_score": 58,
          "smell_count": 8,
          "smells": [
            {
              "type": "god_method",
              "line": 120,
              "context": "public async Task ProcessOrder(Order order, ...) {",
              "severity": "medium",
              "category": "quality",
              "findingId": "god_method::src/Services/OrderService.cs:120",
              "triageStatus": "unreviewed",
              "length": 145
            }
          ]
        }
      ]
    }
  ],
  "claudeCodeTargets": {
    "tier1_critical": [
      {
        "project": "Ordering.API",
        "why": "Refactoring value: 234.5. 12 god_method, 8 sync_over_async. No test coverage. Fan-in=8.",
        "suggestedPrompt": "Review Ordering.API for refactoring...",
        "estimatedEffort": "high",
        "files": ["src/Services/OrderService.cs"]
      }
    ],
    "tier2_high": [],
    "tier3_medium": []
  },
  "smellPrompts": {
    "hardcoded_secret": "SECURITY FINDING: Hardcoded secret detected...",
    "god_method": "CODE QUALITY: Method exceeds 100 lines..."
  }
}
```

### Smell Object Fields

Every finding in `files[].smells[]` has:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Detector name (e.g., `god_method`, `sql_injection`) |
| `line` | int | Line number in the source file |
| `context` | string | Code snippet (80-120 chars) showing the flagged line |
| `severity` | string | `critical`, `high`, `medium`, or `low` |
| `category` | string | `security`, `bug`, `quality`, `interop`, or `style` |
| `findingId` | string | Stable ID: `{type}::{normalized_path}:{line}` |
| `triageStatus` | string | `unreviewed`, `confirmed`, `false_positive`, `accepted_risk`, `fixed` |

Some detectors add extra fields:
- `god_method`: `length` (line count)
- `python_call`: `mechanism` (process_exec, python_net, ironpython, py_script_ref)
- `magic_number`: `value` (the numeric literal)
- `missing_null_check`: `parameter` (the parameter name)

## refactoring-report.md Structure

The markdown report contains:

1. **Header and metadata** -- title, date, scan root
2. **Executive summary** -- file counts, smell counts, top 10 smell types
3. **Top 30 projects by refactoring value** -- per project:
   - Score, category, layer, fan-in/fan-out, test coverage
   - Total files, lines, complexity
   - Top 5 smell types with counts
   - Top 3 files by complexity
4. **Financial projects** (if detected) -- precision-unsafe math highlights
5. **Claude Code session plan** -- tiered targets with ready-to-paste prompts

## LLM Prompt Templates

Every detector has a corresponding prompt in `smellPrompts`. These drive the Claude Code
integration in `viewer.html` -- clicking the "Claude" button on a finding substitutes
`{file}`, `{line}`, `{context}`, and `{project}` into the template and opens Claude Code
with that prompt.

Each prompt follows a strict structure:

1. **Category label** and finding type (e.g., "SECURITY FINDING: Potential SQL injection")
2. **File, line, context** substituted from the finding
3. **Scope instruction**: "Evaluate ONLY this finding. Do NOT review the rest of the file."
4. **Numbered investigation/fix steps** (3-4 steps, detector-specific)
5. **Closing**: "Show the minimal code change needed -- do not refactor surrounding code."

This keeps AI-assisted reviews narrow and prevents scope creep. The full prompt text for
all 19 detectors is embedded in `refactoring-targets.json` under `smellPrompts`.

### Prompt Categories

| Category | Detectors | Prompt Focus |
|----------|-----------|-------------|
| Security | hardcoded_secret, sql_injection, insecure_deserialization, command_injection, weak_crypto, open_redirect, xss, insecure_random | Confirm vulnerability is real, propose specific secure alternative |
| Bug | exception_swallowing, sync_over_async | Identify root cause, propose safe fix |
| Quality | god_method, deep_nesting, long_parameter_list, precision_unsafe_math, deep_inheritance | Propose refactoring strategy |
| Interop | python_call | Document purpose, assess error handling, evaluate integration approach |
| Style | magic_number, missing_null_check, mutable_shared_state | Extract constant, add guard, add synchronization |
