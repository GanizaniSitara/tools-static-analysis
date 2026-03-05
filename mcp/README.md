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

## Available Tools (21 total)

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

## Configuration

The server loads configuration from `config.yaml` and environment variables:

- `OUTPUT_DIR` - Default output directory (default: `output-unified`)
- `COMPANION_PORT` - Companion agent port (default: `3000`)
- `SERVER_PORT` - HTTP server port (default: `8000`)

## Example Workflow

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

## Architecture

```
mcp/
├── server.py          # Main FastMCP server with 21 tools
├── config.py          # Configuration management
├── models.py          # Pydantic response models
├── scan_loader.py     # Load scan results from JSON
├── fix_loader.py      # Load fix workflow state
├── triage_loader.py   # Manage triage decisions
└── requirements.txt   # Dependencies
```

## Data Sources

- Scan results: `<output-dir>/*.json`
- Fix state: `.companion-fixes.json`
- Triage decisions: `<output-dir>/triage.json`
- Prompts: `prompts/default_prompts.yaml`

All data is loaded from local JSON files - no external APIs or databases.
