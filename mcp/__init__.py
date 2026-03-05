"""Static Analysis MCP Server.

An MCP (Model Context Protocol) server that exposes static analysis tools
for AI-powered code analysis and refactoring workflows.
"""

__version__ = "0.1.0"

def main():
    """Entry point for MCP server."""
    from .server import main as server_main
    return server_main()

__all__ = ["main"]
