#!/usr/bin/env python3
"""Test script for enhanced MCP tools.

Tests the 7 new intelligent fix recommendation tools.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from static_analysis_mcp.scan_loader import ScanLoader
from static_analysis_mcp.educational_resources import get_educational_resources


def test_scan_loader_enhancements():
    """Test new scan_loader methods."""
    print("=" * 60)
    print("Testing ScanLoader Enhancements")
    print("=" * 60)

    # Use output-unified as test data
    test_dir = "output-unified"
    loader = ScanLoader(test_dir)

    if not loader.exists():
        print(f"❌ Test directory {test_dir} not found")
        return False

    print(f"✓ Loader initialized for {test_dir}\n")

    # Test 1: get_prioritized_findings
    print("Test 1: get_prioritized_findings")
    print("-" * 40)
    try:
        findings = loader.get_prioritized_findings(limit=5)
        print(f"✓ Found {len(findings)} prioritized findings")

        if findings:
            top = findings[0]
            print(f"  Top priority: {top.get('smell_type', 'N/A')}")
            print(f"  Severity: {top.get('severity', 'N/A')}")
            print(f"  Priority score: {top.get('priority_score', 0):.2f}")
            print(f"  Effort: {top.get('effort_estimate', 'N/A')}")
            print(f"  Blast radius: {top.get('blast_radius', 'N/A')}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print()

    # Test 2: get_rich_context
    print("Test 2: get_rich_context")
    print("-" * 40)
    try:
        # Get any finding for testing
        all_findings = loader.get_all_findings()
        if all_findings:
            f = all_findings[0]
            context = loader.get_rich_context(
                f['project'],
                f['path'],
                f['line']
            )

            if 'isError' not in context:
                print(f"✓ Rich context assembled")
                print(f"  Finding: {context['finding'].get('smell_type', 'N/A')}")
                print(f"  Source lines: {len(context['source_code'].get('full', '').split(chr(10)))}")
                print(f"  Related findings: {len(context.get('related_findings', []))}")
                print(f"  Similar patterns: {len(context.get('similar_patterns', []))}")
                print(f"  Language: {context['fix_guidance'].get('language', 'N/A')}")
            else:
                print(f"❌ Error: {context.get('message', 'Unknown error')}")
        else:
            print("  (No findings to test with)")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print()

    # Test 3: find_similar_smells
    print("Test 3: find_similar_smells")
    print("-" * 40)
    try:
        all_findings = loader.get_all_findings()
        if all_findings:
            # Pick a common smell type
            smell_type = all_findings[0]['smell_type']
            similar = loader.find_similar_smells(smell_type, group_by="file", limit=10)

            print(f"✓ Found similar smells: {smell_type}")
            print(f"  Results: {len(similar)} groups")

            if similar and isinstance(similar, list) and len(similar) > 0:
                if isinstance(similar[0], dict):
                    if 'count' in similar[0]:
                        total = sum(s.get('count', 0) for s in similar)
                        print(f"  Total instances: {total}")
        else:
            print("  (No findings to test with)")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print()

    # Test 4: effort estimation
    print("Test 4: _estimate_effort")
    print("-" * 40)
    try:
        all_findings = loader.get_all_findings()
        if all_findings:
            for i, f in enumerate(all_findings[:3]):
                effort = loader._estimate_effort(f)
                print(f"  Finding {i+1}: {f.get('smell_type', 'N/A')} - {effort}")
        else:
            print("  (No findings to test with)")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print()
    return True


def test_educational_resources():
    """Test educational resources module."""
    print("=" * 60)
    print("Testing Educational Resources")
    print("=" * 60)

    # Test common smell types
    smell_types = [
        'sql_injection',
        'exception_swallowing',
        'sync_over_async',
        'command_injection',
        'hardcoded_secret',
        'magic_number',
        'unknown_smell_type'  # Should fallback to generic
    ]

    for smell_type in smell_types:
        try:
            resources = get_educational_resources(smell_type)

            videos = resources.get('educational_videos', [])
            docs = resources.get('documentation_links', [])
            has_specific = resources.get('has_resources', False)

            status = "✓ Specific" if has_specific else "○ Generic"
            print(f"{status} {smell_type:30s} - {len(videos)} videos, {len(docs)} docs")

        except Exception as e:
            print(f"❌ {smell_type:30s} - Error: {e}")
            return False

    print()

    # Test a specific resource in detail
    print("Detail test: sql_injection")
    print("-" * 40)
    try:
        resources = get_educational_resources('sql_injection')

        print(f"Has specific resources: {resources['has_resources']}")
        print(f"Videos ({len(resources['educational_videos'])}):")
        for i, video in enumerate(resources['educational_videos'], 1):
            print(f"  {i}. {video['title']}")
            print(f"     Channel: {video['channel']}, Duration: {video.get('duration', 'N/A')}")
            print(f"     URL: {video['url']}")

        print(f"\nDocumentation ({len(resources['documentation_links'])}):")
        for i, doc in enumerate(resources['documentation_links'], 1):
            print(f"  {i}. {doc}")

        if resources.get('related_topics'):
            print(f"\nRelated topics: {', '.join(resources['related_topics'][:5])}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print()
    return True


def test_integration():
    """Test integration of all components."""
    print("=" * 60)
    print("Testing Integration: Complete Workflow")
    print("=" * 60)

    try:
        test_dir = "output-unified"
        loader = ScanLoader(test_dir)

        if not loader.exists():
            print(f"❌ Test directory {test_dir} not found")
            return False

        # 1. Get prioritized findings
        print("Step 1: Get priority recommendations")
        findings = loader.get_prioritized_findings(limit=3)
        print(f"  ✓ Top 3 priorities retrieved")

        if not findings:
            print("  (No findings available for integration test)")
            return True

        top_finding = findings[0]
        print(f"  Top: {top_finding.get('smell_type', 'N/A')} (score: {top_finding.get('priority_score', 0):.2f})")

        # 2. Get rich context
        print("\nStep 2: Assemble rich context")
        context = loader.get_rich_context(
            top_finding['project'],
            top_finding['path'],
            top_finding['line']
        )

        if 'isError' in context:
            print(f"  ❌ Context error: {context.get('message', 'Unknown')}")
            return False

        print(f"  ✓ Context assembled")
        print(f"    - Dependencies: {context['dependencies'].get('fan_in', 0)} incoming")
        print(f"    - Related findings: {len(context.get('related_findings', []))}")
        print(f"    - Triage status: {context['triage'].get('status', 'N/A')}")

        # 3. Get educational resources
        print("\nStep 3: Get educational resources")
        smell_type = top_finding.get('smell_type', '')
        resources = get_educational_resources(smell_type)

        print(f"  ✓ Resources retrieved")
        print(f"    - Videos: {len(resources.get('educational_videos', []))}")
        print(f"    - Docs: {len(resources.get('documentation_links', []))}")
        print(f"    - Has specific resources: {resources.get('has_resources', False)}")

        # 4. Find similar for batch opportunities
        print("\nStep 4: Find similar smells for batch fixing")
        similar = loader.find_similar_smells(smell_type, group_by="pattern", limit=10)

        if isinstance(similar, list) and len(similar) > 0:
            if isinstance(similar[0], dict) and 'count' in similar[0]:
                total = sum(s.get('count', 0) for s in similar)
                print(f"  ✓ Found {total} total instances in {len(similar)} patterns")
                print(f"    - Batch fix opportunity: {'Yes' if total > 3 else 'No'}")

        print("\n✓ Integration test completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print(" ENHANCED MCP SERVER TEST SUITE")
    print("=" * 60)
    print()

    results = []

    # Test 1: ScanLoader enhancements
    results.append(("ScanLoader", test_scan_loader_enhancements()))

    # Test 2: Educational resources
    results.append(("Educational Resources", test_educational_resources()))

    # Test 3: Integration
    results.append(("Integration", test_integration()))

    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status:8s} {name}")

    print()

    all_passed = all(r[1] for r in results)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
