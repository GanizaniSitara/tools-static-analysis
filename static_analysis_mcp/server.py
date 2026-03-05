"""Static Analysis MCP Server.

Exposes static analysis functionality through MCP (Model Context Protocol)
for AI-powered code analysis and refactoring workflows.
"""

import sys
import os
import subprocess
import uuid
import logging
import requests
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastmcp import FastMCP

from .config import get_config
from .scan_loader import ScanLoader
from .fix_loader import FixLoader
from .triage_loader import TriageLoader

# Initialize FastMCP server
mcp = FastMCP("static-analysis-mcp")

# Global state
config = None
scan_loader = None
fix_loader = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Scan Management Tools (5 tools)
# =============================================================================

@mcp.tool()
def trigger_scan(
    repos: str,
    output_dir: str,
    level: str = "high",
    tools: str = "none"
) -> Dict[str, Any]:
    """Start a new analysis scan.

    Args:
        repos: Path to repository or solution to scan
        output_dir: Output directory for scan results
        level: Analysis level (critical|high|medium|low)
        tools: External tools to run (none|semgrep|bandit|all)

    Returns:
        Scan metadata with scan_id and status
    """
    scan_id = str(uuid.uuid4())

    # Build command
    cmd = [
        sys.executable,
        str(Path(__file__).parent.parent / 'run.py'),
        '--repos', repos,
        '--out', output_dir,
        '--level', level,
        '--tools', tools
    ]

    try:
        # Start subprocess (detached)
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )

        # Store scan metadata
        scan_meta = {
            'scan_id': scan_id,
            'status': 'running',
            'pid': proc.pid,
            'output_dir': output_dir,
            'repos': repos,
            'start_time': datetime.now().isoformat()
        }

        logger.info(f"Started scan {scan_id} with PID {proc.pid}")
        return scan_meta

    except Exception as e:
        logger.error(f"Failed to start scan: {e}")
        return {
            "isError": True,
            "message": f"Failed to start scan: {str(e)}"
        }


@mcp.tool()
def get_scan_summary(output_dir: str) -> Dict[str, Any]:
    """Get summary statistics for a completed scan.

    Args:
        output_dir: Path to scan output directory

    Returns:
        Summary with file counts, smell types, and severity breakdown
    """
    try:
        loader = ScanLoader(output_dir)
        if not loader.exists():
            return {
                "isError": True,
                "message": f"Output directory not found: {output_dir}"
            }

        return loader.get_summary()

    except Exception as e:
        logger.error(f"Failed to get scan summary: {e}")
        return {
            "isError": True,
            "message": f"Failed to get scan summary: {str(e)}"
        }


@mcp.tool()
def list_recent_scans(project_root: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """List recent scan output directories.

    Args:
        project_root: Project root directory (defaults to config)
        limit: Maximum number of scans to return

    Returns:
        List of scan output directories with metadata
    """
    try:
        if project_root is None:
            project_root = str(config.project_root)

        root = Path(project_root)
        output_dirs = []

        # Find all output-* directories
        for item in root.iterdir():
            if item.is_dir() and item.name.startswith('output-'):
                refactoring_file = item / 'refactoring-targets.json'
                if refactoring_file.exists():
                    mtime = refactoring_file.stat().st_mtime
                    output_dirs.append({
                        'path': str(item),
                        'name': item.name,
                        'modified': datetime.fromtimestamp(mtime).isoformat()
                    })

        # Sort by modification time (newest first)
        output_dirs.sort(key=lambda x: x['modified'], reverse=True)

        return output_dirs[:limit]

    except Exception as e:
        logger.error(f"Failed to list scans: {e}")
        return []


@mcp.tool()
def get_scan_status(scan_id: str) -> Dict[str, Any]:
    """Check status of a running scan.

    Args:
        scan_id: Scan identifier returned by trigger_scan

    Returns:
        Scan status information
    """
    # Note: In a production system, you'd persist scan metadata
    # For now, return a simple status check
    return {
        "scan_id": scan_id,
        "status": "unknown",
        "message": "Scan status tracking not yet implemented. Use get_scan_summary to check results."
    }


@mcp.tool()
def get_viewer_url(output_dir: str, port: int = 8000) -> Dict[str, Any]:
    """Get URL for web viewer of scan results.

    Args:
        output_dir: Path to scan output directory
        port: HTTP server port

    Returns:
        Viewer URL and availability info
    """
    try:
        loader = ScanLoader(output_dir)
        if not loader.exists():
            return {
                "isError": True,
                "message": f"Output directory not found: {output_dir}"
            }

        viewer_file = Path(output_dir) / "docs" / "viewer.html"
        if not viewer_file.exists():
            return {
                "url": "",
                "output_dir": output_dir,
                "available": False,
                "message": "Viewer not generated. Run 5_gen_docs.py first."
            }

        return {
            "url": f"http://localhost:{port}/{output_dir}/docs/viewer.html",
            "output_dir": output_dir,
            "available": True,
            "message": f"Start run.py to serve the viewer on port {port}"
        }

    except Exception as e:
        logger.error(f"Failed to get viewer URL: {e}")
        return {
            "isError": True,
            "message": f"Failed to get viewer URL: {str(e)}"
        }


# =============================================================================
# Query Tools (7 tools)
# =============================================================================

@mcp.tool()
def query_findings(
    output_dir: str,
    severity: Optional[str] = None,
    category: Optional[str] = None,
    language: Optional[str] = None,
    project: Optional[str] = None,
    smell_type: Optional[str] = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Search code smells and findings with filters.

    Args:
        output_dir: Path to scan output directory
        severity: Filter by severity (critical|high|medium|low)
        category: Filter by category (security|bug|quality|style)
        language: Filter by language (csharp|java|python)
        project: Filter by project name
        smell_type: Filter by smell type
        limit: Maximum results to return

    Returns:
        List of findings with context
    """
    try:
        loader = ScanLoader(output_dir)
        if not loader.exists():
            return []

        filters = {}
        if severity:
            filters['severity'] = severity
        if category:
            filters['category'] = category
        if language:
            filters['language'] = language
        if project:
            filters['project'] = project
        if smell_type:
            filters['smell_type'] = smell_type

        findings = loader.get_all_findings(filters)
        return findings[:limit]

    except Exception as e:
        logger.error(f"Failed to query findings: {e}")
        return []


@mcp.tool()
def get_finding_details(
    output_dir: str,
    project: str,
    file_path: str,
    line: int
) -> Dict[str, Any]:
    """Get full context for a specific finding.

    Args:
        output_dir: Path to scan output directory
        project: Project name
        file_path: File path
        line: Line number

    Returns:
        Finding details with source code context
    """
    try:
        loader = ScanLoader(output_dir)
        finding = loader.get_finding_at(project, file_path, line)

        if not finding:
            return {
                "isError": True,
                "message": "Finding not found"
            }

        # Add surrounding code context
        source_code = loader.get_file_content(file_path, line - 5, line + 5)
        finding['source_code'] = source_code

        return finding

    except Exception as e:
        logger.error(f"Failed to get finding details: {e}")
        return {
            "isError": True,
            "message": f"Failed to get finding details: {str(e)}"
        }


@mcp.tool()
def query_dependencies(
    output_dir: str,
    project: Optional[str] = None,
    include_transitive: bool = False
) -> Dict[str, Any]:
    """Get project dependency graph.

    Args:
        output_dir: Path to scan output directory
        project: Optional project name to filter to
        include_transitive: Include transitive dependencies

    Returns:
        Dependency graph with nodes and edges
    """
    try:
        loader = ScanLoader(output_dir)
        graph = loader.get_dependency_graph()

        if 'isError' in graph:
            return graph

        if project:
            # Filter to specific project
            graph = loader.filter_graph(graph, project, include_transitive)

        return graph

    except Exception as e:
        logger.error(f"Failed to query dependencies: {e}")
        return {
            "isError": True,
            "message": f"Failed to query dependencies: {str(e)}"
        }


@mcp.tool()
def find_circular_dependencies(output_dir: str) -> List[Dict[str, Any]]:
    """Detect circular dependencies in project graph.

    Args:
        output_dir: Path to scan output directory

    Returns:
        List of circular dependency cycles with severity
    """
    try:
        loader = ScanLoader(output_dir)
        cycles = loader.find_circular_dependencies()
        return cycles

    except Exception as e:
        logger.error(f"Failed to find circular dependencies: {e}")
        return []


@mcp.tool()
def query_data_flows(
    output_dir: str,
    project: Optional[str] = None,
    flow_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get data flow analysis results.

    Args:
        output_dir: Path to scan output directory
        project: Optional project filter
        flow_type: Optional flow type filter

    Returns:
        List of data flows
    """
    try:
        loader = ScanLoader(output_dir)
        filters = {}
        if project:
            filters['project'] = project
        if flow_type:
            filters['flow_type'] = flow_type

        flows = loader.get_data_flows(filters)
        return flows

    except Exception as e:
        logger.error(f"Failed to query data flows: {e}")
        return []


@mcp.tool()
def get_project_metrics(
    output_dir: str,
    project: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get complexity metrics for projects.

    Args:
        output_dir: Path to scan output directory
        project: Optional project name filter

    Returns:
        List of project metrics (complexity, smells, etc.)
    """
    try:
        loader = ScanLoader(output_dir)
        metrics = loader.get_project_metrics(project)
        return metrics

    except Exception as e:
        logger.error(f"Failed to get project metrics: {e}")
        return []


@mcp.tool()
def search_code(
    output_dir: str,
    query: str,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Full-text search across finding descriptions and context.

    Args:
        output_dir: Path to scan output directory
        query: Search query string
        limit: Maximum results to return

    Returns:
        List of matching findings
    """
    try:
        loader = ScanLoader(output_dir)
        results = loader.search_code(query, limit)
        return results

    except Exception as e:
        logger.error(f"Failed to search code: {e}")
        return []


# =============================================================================
# Fix Workflow Tools (5 tools)
# =============================================================================

@mcp.tool()
def start_fix(
    smell_type: str,
    file_path: str,
    line: int,
    project: str,
    smell_description: str,
    editor: str = "claude"
) -> Dict[str, Any]:
    """Begin fix workflow via companion agent.

    Args:
        smell_type: Type of code smell
        file_path: Path to file with smell
        line: Line number
        project: Project name
        smell_description: Description of the smell
        editor: Editor to use (claude|opencode|copilot)

    Returns:
        Fix workflow state with fix_id
    """
    try:
        # Delegate to companion agent
        params = {
            'smell_type': smell_type,
            'path': file_path,
            'line': line,
            'project': project,
            'smell': smell_description,
            'editor': editor
        }

        companion_url = f'http://localhost:{config.companion_port}/_fix/start'
        response = requests.get(companion_url, params=params, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "isError": True,
                "message": f"Companion agent error: {response.text}"
            }

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to start fix: {e}")
        return {
            "isError": True,
            "message": f"Failed to connect to companion agent on port {config.companion_port}. Is it running?"
        }


@mcp.tool()
def get_fix_status(fix_id: str) -> Dict[str, Any]:
    """Get fix workflow status.

    Args:
        fix_id: Fix identifier from start_fix

    Returns:
        Fix state with status and progress
    """
    try:
        fix = fix_loader.get_fix(fix_id)

        if not fix:
            return {
                "isError": True,
                "message": f"Fix not found: {fix_id}"
            }

        return {
            "fix_id": fix_id,
            **fix
        }

    except Exception as e:
        logger.error(f"Failed to get fix status: {e}")
        return {
            "isError": True,
            "message": f"Failed to get fix status: {str(e)}"
        }


@mcp.tool()
def list_active_fixes(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """List in-progress fix workflows.

    Args:
        status: Optional status filter (checkout|branching|fixing|review|building|testing|submitting|done)

    Returns:
        List of fix workflows
    """
    try:
        if status:
            fixes = fix_loader.get_all_fixes(status)
        else:
            fixes = fix_loader.list_active_fixes()

        return fixes

    except Exception as e:
        logger.error(f"Failed to list fixes: {e}")
        return []


@mcp.tool()
def submit_fix(fix_id: str, message: Optional[str] = None) -> Dict[str, Any]:
    """Submit fix for review (create PR or patch).

    Args:
        fix_id: Fix identifier
        message: Optional commit/PR message

    Returns:
        Submission result with PR URL or patch path
    """
    try:
        # Delegate to companion agent
        params = {'fix_id': fix_id}
        if message:
            params['message'] = message

        companion_url = f'http://localhost:{config.companion_port}/_fix/submit'
        response = requests.get(companion_url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "isError": True,
                "message": f"Companion agent error: {response.text}"
            }

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to submit fix: {e}")
        return {
            "isError": True,
            "message": f"Failed to connect to companion agent: {str(e)}"
        }


@mcp.tool()
def cancel_fix(fix_id: str) -> Dict[str, Any]:
    """Cancel/abandon a fix workflow.

    Args:
        fix_id: Fix identifier

    Returns:
        Cancellation result
    """
    try:
        # Delegate to companion agent
        params = {'fix_id': fix_id}

        companion_url = f'http://localhost:{config.companion_port}/_fix/cancel'
        response = requests.get(companion_url, params=params, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "isError": True,
                "message": f"Companion agent error: {response.text}"
            }

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to cancel fix: {e}")
        return {
            "isError": True,
            "message": f"Failed to connect to companion agent: {str(e)}"
        }


# =============================================================================
# Configuration Tools (4 tools)
# =============================================================================

@mcp.tool()
def get_server_config() -> Dict[str, Any]:
    """Get current configuration settings.

    Returns:
        Configuration dictionary
    """
    try:
        return {
            "project_root": str(config.project_root),
            "output_dir": config.output_dir,
            "companion_port": config.companion_port,
            "server_port": config.server_port,
            "claude_code_path": config.claude_code_path,
            "copilot_enabled": config.copilot_enabled,
            "copilot_model": config.copilot_model,
            "enable_wsl_tools": config.enable_wsl_tools
        }

    except Exception as e:
        logger.error(f"Failed to get config: {e}")
        return {
            "isError": True,
            "message": f"Failed to get config: {str(e)}"
        }


@mcp.tool()
def list_prompts() -> List[Dict[str, Any]]:
    """List available AI prompt templates.

    Returns:
        List of prompt templates with names and descriptions
    """
    try:
        prompts_dir = config.get_prompts_dir()
        default_prompts_file = prompts_dir / "default_prompts.yaml"

        if not default_prompts_file.exists():
            return []

        with open(default_prompts_file, 'r', encoding='utf-8') as f:
            prompts_data = yaml.safe_load(f) or {}

        prompts = []
        for name, data in prompts_data.items():
            if isinstance(data, dict):
                prompts.append({
                    "name": name,
                    "description": data.get('description', ''),
                    "template": data.get('template', ''),
                    "variables": data.get('variables', [])
                })

        return prompts

    except Exception as e:
        logger.error(f"Failed to list prompts: {e}")
        return []


@mcp.tool()
def get_prompt_for_finding(
    smell_type: str,
    file_path: str,
    context: str
) -> Dict[str, Any]:
    """Get tailored AI prompt for a specific finding.

    Args:
        smell_type: Type of code smell
        file_path: Path to file
        context: Code context

    Returns:
        Formatted prompt for AI tool
    """
    try:
        prompts = list_prompts()

        # Find matching prompt template
        template = None
        for prompt in prompts:
            if smell_type.lower() in prompt['name'].lower():
                template = prompt['template']
                break

        if not template:
            # Use generic template
            template = config.claude_prompt

        # Format prompt with context
        prompt_text = template.format(
            smell_type=smell_type,
            file_path=file_path,
            context=context
        ) if '{' in template else template

        return {
            "prompt": prompt_text,
            "smell_type": smell_type,
            "template_used": "specific" if template != config.claude_prompt else "generic"
        }

    except Exception as e:
        logger.error(f"Failed to get prompt: {e}")
        return {
            "isError": True,
            "message": f"Failed to get prompt: {str(e)}"
        }


@mcp.tool()
def update_triage_status(
    output_dir: str,
    project: str,
    file_path: str,
    line: int,
    status: str,
    assigned_to: Optional[str] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """Update triage status for a finding.

    Args:
        output_dir: Path to scan output directory
        project: Project name
        file_path: File path
        line: Line number
        status: Triage status (open|in_progress|resolved|wont_fix|false_positive)
        assigned_to: Optional assignee
        notes: Optional notes

    Returns:
        Update result
    """
    try:
        triage_file = config.get_triage_file(output_dir)
        triage_loader = TriageLoader(triage_file)

        success = triage_loader.update_triage(
            project, file_path, line, status, assigned_to, notes
        )

        if success:
            return {
                "success": True,
                "project": project,
                "file_path": file_path,
                "line": line,
                "status": status
            }
        else:
            return {
                "isError": True,
                "message": "Failed to update triage status"
            }

    except Exception as e:
        logger.error(f"Failed to update triage: {e}")
        return {
            "isError": True,
            "message": f"Failed to update triage: {str(e)}"
        }


# =============================================================================
# Server Initialization
# =============================================================================

def initialize_server():
    """Initialize server on startup."""
    global config, scan_loader, fix_loader

    from .config import get_config as load_config
    config = load_config()
    fix_loader = FixLoader(str(config.project_root))

    logger.info("Static Analysis MCP server initialized")
    logger.info(f"Project root: {config.project_root}")
    logger.info(f"Default output dir: {config.default_output_dir}")
    logger.info(f"Companion port: {config.companion_port}")


def main():
    """Entry point for MCP server."""
    initialize_server()

    # Auto-detect transport
    if "--http" in sys.argv:
        port_idx = sys.argv.index("--http") + 1
        port = int(sys.argv[port_idx]) if port_idx < len(sys.argv) else 8080
        logger.info(f"Starting HTTP transport on port {port}")
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    else:
        logger.info("Starting stdio transport (Claude Desktop)")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
