# Finding Triage System

## Purpose

The triage system provides a persistent workflow for reviewing, categorizing, and tracking
static analysis findings across scan runs. It answers the workflow question: once the tool
reports findings, how do you systematically work through them, mark false positives, confirm
real issues, and carry those decisions forward when the code changes and the scanner re-runs?

## How It Works

```
Scan run N                          Scan run N+1
-----------                         ------------
2_scan_smells.py                    2_scan_smells.py
   |                                   |
   v                                   v
Detect findings                     Detect findings
   |                                   |
   v                                   v
Load triage.json ----+         Load triage.json ----+
   |                 |            |                  |
   v                 |            v                  |
Match findings       |         Match findings        |
to dispositions      |         to dispositions       |
   |                 |            |                  |
   v                 |            v                  |
Save updated         |         Save updated          |
triage.json     <----+         triage.json      <----+
   |                              |
   v                              v
viewer.html                    viewer.html
(review + export)              (review + export)
```

Each scan run:
1. Runs all detectors, producing findings with `findingId` and `triageStatus`
2. Loads the existing `triage.json` from the output directory
3. Matches current findings to prior dispositions (exact match, then fuzzy match)
4. Saves the updated `triage.json` -- new findings get `unreviewed`, existing ones keep their status
5. Generates `viewer.html` with triage controls embedded

## Finding IDs

Every finding gets a deterministic ID:

```
{smell_type}::{relative_file_path}:{line_number}
```

Examples:
```
hardcoded_secret::StockSharp/Algo/Connector.cs:42
sql_injection::src/Data/UserRepository.cs:156
weak_crypto::Crypto/HashService.cs:23
```

The path is normalized (backslashes converted to forward slashes) and relative to the scan root.

## Matching Logic

When a new scan runs, the triage system matches findings to prior dispositions in two passes:

### Pass 1: Exact Match

If the finding ID (type + path + line) exactly matches an existing disposition, the
triage status carries forward. This handles the common case where code hasn't changed.

### Pass 2: Fuzzy Match

If no exact match is found, the system looks for a prior disposition with:
- Same smell type
- Same file path
- Line number within +/-5 lines of the current finding
- Identical context string (the code snippet)

This handles the common case where a few lines were inserted above a finding, shifting
its line number. The disposition is migrated to the new finding ID.

### New Findings

Findings that match neither pass are added as `unreviewed`.

### Stale Dispositions

Dispositions that exist in `triage.json` but don't match any current finding are counted
as "stale" in the scan output. They remain in `triage.json` (not deleted) because the
finding might reappear in a future scan. Manual cleanup is the user's choice.

## Triage Statuses

| Status | Meaning | Effect on Workflow |
|--------|---------|-------------------|
| `unreviewed` | Not yet examined | Default for new findings. Filters highlight these for review. |
| `confirmed` | Real issue, needs fixing | Stays visible. Use to prioritize fix backlog. |
| `false_positive` | Scanner was wrong | Can be filtered out in the viewer. Suppressed in future runs. |
| `accepted_risk` | Real finding, but risk accepted | Documented. Stays visible with rationale in the reason field. |
| `fixed` | Issue has been resolved | Can be filtered out. If it reappears (regression), fuzzy match may re-apply. |

## triage.json Schema

```json
{
  "version": 1,
  "generated": "2026-02-28",
  "dispositions": {
    "hardcoded_secret::src/Config.cs:42": {
      "status": "false_positive",
      "reason": "Connection string key name constant used for parsing, not an actual secret",
      "decidedBy": "jsmith",
      "date": "2026-02-28",
      "context": "const string PASSWORD = \"password\";"
    },
    "weak_crypto::src/Hashing/Md5Helper.cs:15": {
      "status": "accepted_risk",
      "reason": "MD5 used for content checksums only, not for security",
      "decidedBy": "security-team",
      "date": "2026-02-27",
      "context": "using var md5 = MD5.Create();"
    },
    "sql_injection::src/Data/UserRepo.cs:89": {
      "status": "confirmed",
      "reason": "User input flows directly into SQL -- needs parameterization",
      "decidedBy": "",
      "date": "2026-02-28",
      "context": "var q = \"SELECT * FROM Users WHERE Name = '\" + name + \"'\";"
    }
  }
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `version` | int | Schema version (currently `1`) |
| `generated` | string | ISO date of last save |
| `dispositions` | object | Map of finding ID to disposition |
| `dispositions.*.status` | string | One of: `unreviewed`, `confirmed`, `false_positive`, `accepted_risk`, `fixed` |
| `dispositions.*.reason` | string | Free-text explanation for the triage decision |
| `dispositions.*.decidedBy` | string | Person or team who made the decision |
| `dispositions.*.date` | string | ISO date when the decision was made |
| `dispositions.*.context` | string | Code snippet from the finding (for fuzzy matching) |

## Viewer UI

The viewer (`viewer.html`) provides triage controls in two places:

### Code Quality Panel

- **Triaged summary card**: Shows `X/Y` findings triaged (non-unreviewed count / total)
- **Triage filter dropdown**: Filter the table by triage status (All, Unreviewed, Confirmed, False Positive, Accepted Risk, Fixed)
- **Per-finding controls**: Each finding row in the expanded detail table has:
  - A status dropdown (change triage status)
  - A reason text field (explain the decision)
- **Export Triage button**: Downloads the current `triage.json` with all in-session changes

### Security Panel

- **Triage badge**: Each security finding row shows its current triage status
- **Triage filter dropdown**: Filter security findings by triage status

### Export Workflow

Changes made in the viewer are held in browser memory until exported:

1. Expand a project row to see its findings
2. Change the triage dropdown for a finding (e.g., from "Unreviewed" to "False Positive")
3. Type a reason in the text field
4. The "Export Triage" button highlights to indicate unsaved changes
5. Click "Export Triage" to download `triage.json`
6. Copy the downloaded file to your output directory (replacing the existing one)
7. Next scan run picks up the updated dispositions automatically

## Integration with refactoring-targets.json

The scan output includes triage data on every finding:

```json
{
  "projects": [{
    "project": "MyProject",
    "files": [{
      "path": "src/Service.cs",
      "smells": [{
        "type": "hardcoded_secret",
        "line": 42,
        "context": "private string apiKey = \"sk-...\";",
        "severity": "critical",
        "category": "security",
        "findingId": "hardcoded_secret::src/Service.cs:42",
        "triageStatus": "unreviewed"
      }]
    }]
  }],
  "summary": {
    "triageCounts": {
      "unreviewed": 45,
      "confirmed": 12,
      "false_positive": 8,
      "accepted_risk": 3,
      "fixed": 2
    }
  }
}
```

## Console Output

The scan reports triage progress on every run:

```
Applying triage dispositions...
  Triage: 52 matched, 3 new, 1 stale

======================================================================
Analysis complete!
  - 45 projects analyzed
  - 70 total smells detected
  - 25/70 findings triaged
  - 8 marked as false positive
  - Top project: Ordering.API (score: 142.0)
======================================================================
```

## Relationship to ArmorCode / Other Tools

This triage system is self-contained and does not replace external security tools like
ArmorCode. The design supports two usage patterns:

1. **Standalone triage**: Use the viewer UI to review and categorize findings directly.
   Export `triage.json` and check it into source control alongside the output.

2. **Pre-filter for external tools**: Run the scanner, triage obvious false positives
   locally, then feed the confirmed/unreviewed findings to ArmorCode or similar platforms
   for deeper analysis. The `refactoring-targets.json` output includes `triageStatus` on
   every finding, making it straightforward to filter programmatically.
