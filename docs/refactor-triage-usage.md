# Refactor Triage Usage Guide

## Overview

`refactor_triage.py` is a purpose-built refactoring analyzer that identifies the most valuable refactoring targets in .NET codebases. It scans C# source files for complexity metrics and code smells, then produces actionable recommendations optimized for AI-assisted refactoring with Claude Code.

## Usage

### Basic Usage

```bash
# Run analysis after analyze.py has completed
python refactor_triage.py /path/to/repos /path/to/output
```

### Example Workflow

```bash
# 1. Run the main analysis
python analyze.py /path/to/repos output-myproject

# 2. Run refactoring triage
python refactor_triage.py /path/to/repos output-myproject

# 3. Check the outputs
cat output-myproject/refactoring-report.md
```

## What It Detects

### Complexity Metrics

- **Line Count**: Skips files under 50 lines (not interesting for refactoring)
- **Cyclomatic Complexity**: Counts decision points (if, else, switch, loops, etc.)
- **Nesting Depth**: Maximum brace nesting depth
- **Method Count**: Total number of methods
- **Long Methods**: Methods exceeding 50 lines
- **God Methods**: Methods exceeding 100 lines

### Code Smells

1. **Exception Swallowing**: Catch blocks with empty body or just `// TODO`
2. **Sync-over-async**: `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` patterns
3. **Magic Numbers**: Hardcoded numeric literals in business logic
4. **Precision-unsafe Math**: `float` or `double` used for financial calculations
5. **Mutable Shared State**: Static mutable fields (not `readonly`, not `const`)
6. **Missing Null Checks**: Public methods without parameter validation
7. **God Methods**: Single method > 100 lines
8. **Deep Inheritance**: Classes with many base classes/interfaces

## Understanding the Outputs

### refactoring-targets.json

Machine-readable analysis with:
- **Summary**: Overall statistics
- **Projects**: Detailed metrics per project
- **claudeCodeTargets**: Pre-formatted prompts ready for Claude Code

#### Refactoring Value Score

The score formula prioritizes projects that are both complex and risky:

```
refactoring_value = (
    complexity_score * 2
    + smell_count * 3
    + (fan_in * fan_out) * 0.5
    + test_gap_penalty * 5
    - deprioritize_discount
)
```

Where:
- Higher score = more valuable to refactor
- Coupling danger multiplies fan-in × fan-out (not sum!)
- Projects without tests get +5 penalty
- UI/logging/test projects get -20 discount

### refactoring-report.md

Human-readable report with:
- **Executive Summary**: Totals and top smell types
- **Top 30 Projects**: Ranked by refactoring value
- **Financial Pricer Projects**: Special section for precision-critical code
- **Claude Code Session Plan**: Tiered approach (Critical, High, Medium)

## Claude Code Integration

The `claudeCodeTargets` section provides copy-paste prompts:

```json
{
  "tier1_critical": [
    {
      "project": "FinancialPricer.Core",
      "why": "Highest refactoring value: 234.5. 3 god methods, 5 precision-unsafe math patterns, no tests, fan-in=15.",
      "suggestedPrompt": "Review FinancialPricer.Core for refactoring. Focus on: precision-unsafe math (double used for financial calculations), 3 methods exceeding 100 lines, sync-over-async patterns. This project has 15 downstream dependents and no test coverage.",
      "estimatedEffort": "high",
      "files": ["src/PricerEngine/BlackScholes.cs", "src/PricerEngine/Greeks.cs"]
    }
  ]
}
```

## Configuration

### Exclusion Patterns

The script automatically excludes:
- Designer/generated files: `*.Designer.cs`, `*.generated.cs`
- Build outputs: `obj/`, `bin/`
- Migrations: `*/Migrations/*`

### Deprioritized Categories

These are still scanned but get -20 score discount:
- Test projects
- Sample/demo projects
- Localization projects
- Tool/utility projects
- Logging infrastructure
- UI base classes

### Financial Project Detection

Projects matching these patterns are flagged as precision-critical:
- Pricer, Pricing
- Financial, Calc
- Engine, Valuation
- Greeks, BlackScholes, MonteCarlo

## Performance

The script is optimized for large codebases:
- **Streaming**: Files are processed one at a time (no memory issues)
- **Skip large files**: Files > 2MB are skipped
- **Progress reporting**: Updates every 500 files
- **Regex-based**: No AST parsing (much faster)

Expected performance:
- 25GB codebase: ~5-10 minutes
- 1000 files: ~30 seconds

## Example Output

```
======================================================================
Refactoring Triage Analyzer
======================================================================
Scan root: /path/to/repos
Output dir: output-myproject

Scanning for C# files in: /path/to/repos
Found 12345 C# files to analyze
Loading existing analysis data...

Analyzing files...
  Progress: 500/12345 files analyzed
  Progress: 1000/12345 files analyzed
  ...

Analyzed 8901 files (skipped 3444 small/excluded files)
Files grouped into 234 projects

Generating outputs...
Saved: output-myproject/refactoring-targets.json
Saved: output-myproject/refactoring-report.md

======================================================================
Analysis complete!
  - 234 projects analyzed
  - 4567 total smells detected
  - Top project: FinancialPricer.Core (score: 409.0)
======================================================================
```

## Best Practices

1. **Run after analyze.py**: This script depends on `graph.json`, `project-meta.json`, etc.
2. **Review Tier 1 first**: Start with critical targets for maximum impact
3. **Use Claude Code prompts**: The suggested prompts are optimized for AI assistance
4. **Focus on financial code**: Precision-unsafe math in pricers is high priority
5. **Address test gaps**: Projects without tests are riskier to refactor

## Troubleshooting

### No projects analyzed

- Ensure `analyze.py` has run first
- Check that `project-meta.json` exists in output directory
- Verify C# files are present and > 50 lines

### Too many magic numbers

- This is expected in complex calculations
- Focus on god methods instead (they're already flagged)
- Magic numbers in expressions are legitimate targets for constants

### Missing smells

- Detection is heuristic-based (not perfect)
- Some patterns require full semantic analysis (not available)
- False negatives are acceptable for prioritization

## Integration with Existing Tools

This tool complements the existing pipeline:

```
analyze.py          → Extract dependencies, project refs
  ↓
refactor_triage.py  → Identify refactoring targets
  ↓
visualize.py        → Generate architecture diagrams
  ↓
generate_docs.py    → Create comprehensive documentation
```

Use together for best results:
- `analyze.py` provides architectural context (fan-in/fan-out)
- `refactor_triage.py` identifies code quality issues
- Combined view helps prioritize refactoring safely
