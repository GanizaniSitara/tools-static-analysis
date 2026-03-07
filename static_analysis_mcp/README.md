# Static Analysis MCP Server

An MCP (Model Context Protocol) server that exposes static analysis functionality for AI-powered code analysis and refactoring workflows.

## Installation

```bash
# Install dependencies (requires Python 3.8+)
pip install -r mcp/requirements.txt
```

## Usage

### Stdio Mode (Claude Desktop)

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "static-analysis": {
      "command": "python",
      "args": [
        "/home/user/dependency-mapper-python/mcp/server.py"
      ]
    }
  }
}
```

### HTTP Mode (Testing)

```bash
# Start server on port 8080
python -m mcp.server --http 8080

# Test with MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8080/sse
```

## Available Tools (30 total)

### Scan Management (5 tools)

- `trigger_scan` - Start a new analysis scan
- `get_scan_summary` - Get scan statistics
- `list_recent_scans` - List recent scan outputs
- `get_scan_status` - Check scan progress
- `get_viewer_url` - Get web viewer URL

### Query Tools (7 tools)

- `query_findings` - Search code smells with filters
- `get_finding_details` - Get full context for a finding
- `query_dependencies` - Get dependency graph
- `find_circular_dependencies` - Detect circular dependencies
- `query_data_flows` - Get data flow analysis
- `get_project_metrics` - Get complexity metrics
- `search_code` - Full-text search across findings

### Fix Workflow (5 tools)

- `start_fix` - Begin fix workflow
- `get_fix_status` - Check fix progress
- `list_active_fixes` - List in-progress fixes
- `submit_fix` - Submit fix for review
- `cancel_fix` - Abandon fix workflow

### Configuration (4 tools)

- `get_config` - Get current settings
- `list_prompts` - List AI prompt templates
- `get_prompt_for_finding` - Get tailored prompt
- `update_triage_status` - Update finding status

### Health Check & Setup (2 NEW tools)

**Proactive companion server management:**
- `check_companion_health` - Check if companion is running, get setup instructions if not
- `get_companion_setup_info` - Get comprehensive setup information with commands and links

**Returns structured responses with:**
- Step-by-step setup instructions
- Clickable links to quickstart HTML
- Copy-paste commands
- Troubleshooting tips
- Call-to-action buttons

### Intelligent Fix Recommendations (7 tools)

**Answer "What should I fix first?":**
- `recommend_fixes_priority` - Get prioritized list of fixes ranked by impact, effort, and blast radius

**Rich Context Assembly:**
- `get_rich_fix_context` - Assemble comprehensive context (dependencies, similar patterns, metrics, test coverage)
- `find_similar_smells` - Find all instances of a smell type for batch fixing
- `estimate_fix_effort` - Estimate effort required (trivial|low|medium|high)

**Learning Support:**
- `get_fix_template` - Get pre-built fix patterns and guidance
- `get_educational_resources` - Get YouTube videos and docs to learn about the smell type
- `start_fix_with_context` - Enhanced fix workflow with rich context + educational resources + CONFIDENCE CHECK

**Key Features:**
- **Smart Prioritization**: Ranks fixes by severity, security, blast radius, and effort
- **Batch Fix Opportunities**: Identifies similar patterns across the codebase
- **Educational Resources**: Curated YouTube videos and documentation for 15+ smell types
- **Confidence Check**: AI agents assess understanding before proposing fixes, preventing guessing
- **Rich Context**: Dependencies, similar patterns, complexity metrics, and test coverage

## Configuration

The server loads configuration from `config.yaml` and environment variables:

- `OUTPUT_DIR` - Default output directory (default: `output-unified`)
- `COMPANION_PORT` - Companion agent port (default: `3000`)
- `SERVER_PORT` - HTTP server port (default: `8000`)

## Example Workflows

### Basic Workflow

```python
# 1. Trigger a scan
scan = trigger_scan(
    repos="/path/to/repo",
    output_dir="output-test",
    level="high"
)

# 2. Get summary
summary = get_scan_summary("output-test")
print(f"Found {summary['totalSmells']} smells")

# 3. Query findings
findings = query_findings(
    output_dir="output-test",
    severity="critical",
    category="security",
    limit=10
)

# 4. Start fix workflow
fix = start_fix(
    smell_type=findings[0]['smell_type'],
    file_path=findings[0]['path'],
    line=findings[0]['line'],
    project=findings[0]['project'],
    smell_description=findings[0]['description']
)

# 5. Update triage status
update_triage_status(
    output_dir="output-test",
    project=findings[0]['project'],
    file_path=findings[0]['path'],
    line=findings[0]['line'],
    status="in_progress"
)
```

### NEW: Intelligent Fix Workflow with Learning Support

```python
# 1. Get prioritized recommendations - "What should I fix first?"
recommendations = recommend_fixes_priority(
    output_dir="output-test",
    category="security",
    limit=5
)

# Top priority: Critical SQL injection with high blast radius
top_fix = recommendations[0]
print(f"Priority #{top_fix['priority_rank']}: {top_fix['smell_type']}")
print(f"Reason: {top_fix['reason']}")
print(f"Effort: {top_fix['effort_estimate']}")
print(f"Similar instances: {top_fix['similar_count']}")

# 2. Get rich context for comprehensive understanding
context = get_rich_fix_context(
    output_dir="output-test",
    project=top_fix['project'],
    file_path=top_fix['path'],
    line=top_fix['line']
)

print(f"Dependencies: {context['dependencies']['fan_in']} modules depend on this")
print(f"Related issues in file: {len(context['related_findings'])}")
print(f"Similar patterns found: {len(context['similar_patterns'])}")

# 3. Check if there are batch fix opportunities
similar = find_similar_smells(
    output_dir="output-test",
    smell_type=top_fix['smell_type'],
    group_by="pattern"
)

print(f"Found {similar['total_instances']} instances in {len(similar['groups'])} patterns")

# 4. Get educational resources before fixing
resources = get_educational_resources(
    smell_type=top_fix['smell_type'],
    language="csharp"
)

if not resources['has_resources']:
    print("No specific resources, but generic learning links available")
else:
    print(f"Educational videos: {len(resources['educational_videos'])}")
    for video in resources['educational_videos']:
        print(f"  - {video['title']} ({video['channel']})")

# 5. Start enhanced fix workflow with CONFIDENCE CHECK
fix = start_fix_with_context(
    smell_type=top_fix['smell_type'],
    file_path=top_fix['path'],
    line=top_fix['line'],
    project=top_fix['project'],
    output_dir="output-test",
    editor="claude"
)

# The AI agent will:
# - Receive rich context (dependencies, similar patterns, metrics)
# - See educational resources (videos + docs)
# - Be asked to assess confidence before proposing fix
# - Either learn first OR propose fix directly based on confidence

print(f"Fix started: {fix['fix_id']}")
print(f"Context provided: {fix['context_provided']}")
print(f"Educational resources: {fix['educational_resources']}")
print(f"Recommendation: {fix.get('recommendation', 'N/A')}")
```

## Architecture

```
static_analysis_mcp/
├── server.py                    # Main FastMCP server with 28 tools (21 original + 7 new)
├── config.py                    # Configuration management
├── models.py                    # Pydantic response models
├── scan_loader.py               # Load scan results + intelligent recommendations
├── fix_loader.py                # Load fix workflow state
├── triage_loader.py             # Manage triage decisions
├── educational_resources.py     # NEW: Curated learning resources (YouTube + docs)
└── requirements.txt             # Dependencies
```

### New Enhancements

**scan_loader.py** now includes:
- `get_prioritized_findings()` - Smart prioritization algorithm
- `get_rich_context()` - Rich context assembly for AI agents
- `find_similar_smells()` - Pattern matching for batch fixes
- Helper methods for effort estimation, blast radius calculation

**educational_resources.py** (NEW):
- Curated YouTube videos for 15+ smell types
- Official documentation links (OWASP, Microsoft, etc.)
- Fallback to generic search for uncurated types
- 200+ lines of educational content mapping

## Data Sources

- Scan results: `<output-dir>/*.json`
- Fix state: `.companion-fixes.json`
- Triage decisions: `<output-dir>/triage.json`
- Prompts: `prompts/default_prompts.yaml`

All data is loaded from local JSON files - no external APIs or databases.
