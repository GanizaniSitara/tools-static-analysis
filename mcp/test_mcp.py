#!/usr/bin/env python3
"""Test script for MCP server modules.

Tests all core functionality without requiring fastmcp installation.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.config import get_config
from mcp.scan_loader import ScanLoader
from mcp.fix_loader import FixLoader
from mcp.triage_loader import TriageLoader


def test_config():
    """Test configuration loading."""
    print("=" * 60)
    print("Testing Configuration")
    print("=" * 60)

    config = get_config()
    print(f"✓ Project root: {config.project_root}")
    print(f"✓ Output dir: {config.output_dir}")
    print(f"✓ Companion port: {config.companion_port}")
    print(f"✓ Claude Code path: {config.claude_code_path}")
    print(f"✓ Fixes file: {config.fixes_file}")
    print()


def test_scan_loader():
    """Test scan loader functionality."""
    print("=" * 60)
    print("Testing Scan Loader")
    print("=" * 60)

    # Test with existing scan
    loader = ScanLoader('output-eshop-test')
    print(f"✓ Scan directory exists: {loader.exists()}")

    if loader.exists():
        summary = loader.get_summary()
        print(f"✓ Total files scanned: {summary.get('totalFilesScanned', 0)}")
        print(f"✓ Total smells: {summary.get('totalSmells', 0)}")
        print(f"✓ Severity counts: {summary.get('severityCounts', {})}")

        # Test finding queries
        findings = loader.get_all_findings({'severity': 'high'})
        print(f"✓ High severity findings: {len(findings)}")

        if findings:
            print(f"✓ First finding: {findings[0].get('smell_type', 'N/A')}")

        # Test metrics
        metrics = loader.get_project_metrics()
        print(f"✓ Projects with metrics: {len(metrics)}")

        # Test dependency graph
        graph = loader.get_dependency_graph()
        if 'nodes' in graph:
            print(f"✓ Dependency nodes: {len(graph['nodes'])}")
            print(f"✓ Dependency edges: {len(graph['edges'])}")

        # Test circular dependencies
        cycles = loader.find_circular_dependencies()
        print(f"✓ Circular dependencies found: {len(cycles)}")

    print()


def test_fix_loader():
    """Test fix loader functionality."""
    print("=" * 60)
    print("Testing Fix Loader")
    print("=" * 60)

    config = get_config()
    loader = FixLoader(str(config.project_root))

    fixes = loader.get_all_fixes()
    print(f"✓ Total fixes: {len(fixes)}")

    active_fixes = loader.list_active_fixes()
    print(f"✓ Active fixes: {len(active_fixes)}")

    if fixes:
        print(f"✓ First fix status: {fixes[0].get('status', 'N/A')}")
    else:
        print("  (No fixes in state file yet)")

    print()


def test_triage_loader():
    """Test triage loader functionality."""
    print("=" * 60)
    print("Testing Triage Loader")
    print("=" * 60)

    config = get_config()
    triage_file = config.get_triage_file('output-eshop-test')
    loader = TriageLoader(triage_file)

    triage_decisions = loader.get_all_triage()
    print(f"✓ Triage decisions: {len(triage_decisions)}")

    if triage_decisions:
        print(f"✓ First decision status: {triage_decisions[0].get('status', 'N/A')}")
    else:
        print("  (No triage decisions yet - this is normal)")

    print()


def main():
    """Run all tests."""
    print("\nMCP Server Module Tests")
    print("=" * 60)
    print()

    try:
        test_config()
        test_scan_loader()
        test_fix_loader()
        test_triage_loader()

        print("=" * 60)
        print("All tests passed!")
        print("=" * 60)
        print()
        print("Note: To run the full MCP server, install fastmcp:")
        print("  pip install fastmcp")
        print()
        print("Then start the server:")
        print("  python -m mcp.server")
        print()

        return 0

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
