"""Scan result loader and query interface.

Loads and caches scan results from JSON files in output directories.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class ScanLoader:
    """Loads and queries scan results from output directories."""

    def __init__(self, output_dir: str):
        """Initialize scan loader.

        Args:
            output_dir: Path to scan output directory
        """
        self.output_dir = Path(output_dir)
        self._cache: Dict[str, Any] = {}

    def _load_json(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load and cache a JSON file from output directory.

        Args:
            filename: Name of JSON file to load

        Returns:
            Parsed JSON data or None if file doesn't exist
        """
        if filename in self._cache:
            return self._cache[filename]

        file_path = self.output_dir / filename
        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache[filename] = data
                return data
        except (json.JSONDecodeError, IOError):
            return None

    def exists(self) -> bool:
        """Check if output directory exists.

        Returns:
            True if directory exists
        """
        return self.output_dir.exists() and self.output_dir.is_dir()

    def get_summary(self) -> Dict[str, Any]:
        """Get scan summary statistics.

        Returns:
            Summary data from refactoring-targets.json
        """
        data = self._load_json('refactoring-targets.json')
        if not data:
            return {
                "isError": True,
                "message": f"Scan results not found in {self.output_dir}"
            }

        summary = data.get('summary', {})
        return {
            "generated": data.get('generated', ''),
            "scanRoot": data.get('scanRoot', ''),
            "totalFilesScanned": summary.get('totalFilesScanned', 0),
            "totalFilesWithSmells": summary.get('totalFilesWithSmells', 0),
            "totalSmells": summary.get('totalSmells', 0),
            "topSmellTypes": summary.get('topSmellTypes', []),
            "severityCounts": summary.get('severityCounts', {}),
            "categoryCounts": summary.get('categoryCounts', {}),
            "level": summary.get('level', 'unknown')
        }

    def get_all_findings(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all findings with optional filters.

        Args:
            filters: Optional filter dict with keys:
                - severity: Filter by severity (critical|high|medium|low)
                - category: Filter by category (security|bug|quality|style)
                - language: Filter by language (csharp|java|python)
                - project: Filter by project name
                - smell_type: Filter by smell type

        Returns:
            List of findings
        """
        data = self._load_json('refactoring-targets.json')
        if not data:
            return []

        findings = []
        projects = data.get('projects', [])

        for project_data in projects:
            project = project_data.get('project', '')
            repo = project_data.get('repo', '')

            for file_data in project_data.get('files', []):
                file_path = file_data.get('path', '')

                for smell in file_data.get('smells', []):
                    # Apply filters
                    if filters:
                        if 'severity' in filters and smell.get('severity') != filters['severity']:
                            continue
                        if 'category' in filters and smell.get('category') != filters['category']:
                            continue
                        if 'project' in filters and project != filters['project']:
                            continue
                        if 'smell_type' in filters and smell.get('type') != filters['smell_type']:
                            continue
                        # Language filter (based on file extension)
                        if 'language' in filters:
                            ext = Path(file_path).suffix.lower()
                            lang_map = {'.cs': 'csharp', '.java': 'java', '.py': 'python'}
                            if lang_map.get(ext) != filters['language']:
                                continue

                    finding = {
                        "project": project,
                        "repo": repo,
                        "path": file_path,
                        "line": smell.get('line', 0),
                        "smell_type": smell.get('type', ''),
                        "severity": smell.get('severity', ''),
                        "category": smell.get('category', ''),
                        "description": smell.get('description', ''),
                        "context": smell.get('context', '')
                    }
                    findings.append(finding)

        return findings

    def get_finding_at(self, project: str, file_path: str, line: int) -> Optional[Dict[str, Any]]:
        """Get a specific finding by location.

        Args:
            project: Project name
            file_path: File path
            line: Line number

        Returns:
            Finding data or None
        """
        findings = self.get_all_findings({
            'project': project
        })

        for finding in findings:
            if finding['path'] == file_path and finding['line'] == line:
                return finding

        return None

    def get_file_content(self, file_path: str, start_line: int, end_line: int) -> str:
        """Get source code content from a file (if available).

        Args:
            file_path: Path to source file
            start_line: Start line number (1-indexed)
            end_line: End line number (1-indexed)

        Returns:
            Source code snippet or empty string
        """
        # Try to find the file in the scan root
        data = self._load_json('refactoring-targets.json')
        if not data:
            return ""

        scan_root = Path(data.get('scanRoot', ''))
        full_path = scan_root / file_path

        if not full_path.exists():
            return ""

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Convert to 0-indexed
                start_idx = max(0, start_line - 1)
                end_idx = min(len(lines), end_line)
                return ''.join(lines[start_idx:end_idx])
        except (IOError, UnicodeDecodeError):
            return ""

    def get_dependency_graph(self) -> Dict[str, Any]:
        """Get project dependency graph.

        Returns:
            Graph data with nodes and edges
        """
        data = self._load_json('graph.json')
        if not data:
            return {
                "isError": True,
                "message": "Dependency graph not found"
            }

        return {
            "nodes": data.get('nodes', []),
            "edges": data.get('edges', [])
        }

    def filter_graph(self, graph: Dict[str, Any], project: str,
                    include_transitive: bool = False) -> Dict[str, Any]:
        """Filter graph to a specific project and its dependencies.

        Args:
            graph: Full dependency graph
            project: Project name to filter to
            include_transitive: Include transitive dependencies

        Returns:
            Filtered graph
        """
        nodes = graph.get('nodes', [])
        edges = graph.get('edges', [])

        # Find project node
        project_nodes = [n for n in nodes if n.get('project') == project]
        if not project_nodes:
            return {"nodes": [], "edges": []}

        # Get direct dependencies
        project_ids = {n['id'] for n in project_nodes}
        direct_edges = [e for e in edges if e['source'] in project_ids]
        connected_ids = project_ids | {e['target'] for e in direct_edges}

        if include_transitive:
            # Add transitive dependencies
            changed = True
            while changed:
                changed = False
                for edge in edges:
                    if edge['source'] in connected_ids and edge['target'] not in connected_ids:
                        connected_ids.add(edge['target'])
                        changed = True

        filtered_nodes = [n for n in nodes if n['id'] in connected_ids]
        filtered_edges = [e for e in edges
                         if e['source'] in connected_ids and e['target'] in connected_ids]

        return {
            "nodes": filtered_nodes,
            "edges": filtered_edges
        }

    def find_circular_dependencies(self) -> List[Dict[str, Any]]:
        """Detect circular dependencies in the graph.

        Returns:
            List of circular dependency cycles
        """
        graph = self.get_dependency_graph()
        if 'isError' in graph:
            return []

        nodes = {n['id']: n for n in graph.get('nodes', [])}
        edges = graph.get('edges', [])

        # Build adjacency list
        adj: Dict[str, List[str]] = {}
        for node_id in nodes:
            adj[node_id] = []
        for edge in edges:
            # Handle both 'source' and 'from' key names
            source = edge.get('source') or edge.get('from')
            target = edge.get('target') or edge.get('to')
            if source and target and source in adj:
                adj[source].append(target)

        # DFS to detect cycles
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path[:])
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append({
                        "cycle": [nodes[n]['project'] for n in cycle if n in nodes],
                        "severity": "high" if len(cycle) <= 3 else "medium",
                        "description": f"Circular dependency detected: {' -> '.join([nodes[n]['project'] for n in cycle if n in nodes])}"
                    })

            path.pop()
            rec_stack.remove(node)

        for node_id in nodes:
            if node_id not in visited:
                dfs(node_id, [])

        return cycles

    def get_data_flows(self, filters: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Get data flow analysis results.

        Args:
            filters: Optional filters (project, flow_type)

        Returns:
            List of data flows
        """
        data = self._load_json('data-flow.json')
        if not data:
            return []

        flows = data.get('flows', [])

        if filters:
            if 'project' in filters:
                flows = [f for f in flows if f.get('project') == filters['project']]
            if 'flow_type' in filters:
                flows = [f for f in flows if f.get('type') == filters['flow_type']]

        return flows

    def get_project_metrics(self, project: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get complexity metrics for projects.

        Args:
            project: Optional project name filter

        Returns:
            List of project metrics
        """
        data = self._load_json('refactoring-targets.json')
        if not data:
            return []

        projects = data.get('projects', [])

        if project:
            projects = [p for p in projects if p.get('project') == project]

        # Extract key metrics
        metrics = []
        for proj in projects:
            metrics.append({
                "project": proj.get('project', ''),
                "repo": proj.get('repo', ''),
                "category": proj.get('category', ''),
                "layer": proj.get('layer', ''),
                "fan_in": proj.get('fan_in', 0),
                "fan_out": proj.get('fan_out', 0),
                "has_tests": proj.get('has_tests', False),
                "total_files": proj.get('total_files', 0),
                "total_lines": proj.get('total_lines', 0),
                "complexity_score": proj.get('complexity_score', 0),
                "smell_count": proj.get('smell_count', 0),
                "top_smells": proj.get('top_smells', [])
            })

        return metrics

    def search_code(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search for code patterns in findings.

        Args:
            query: Search query (substring match)
            limit: Maximum results

        Returns:
            List of matching findings
        """
        findings = self.get_all_findings()
        results = []

        query_lower = query.lower()

        for finding in findings:
            # Search in description and context
            desc = finding.get('description', '').lower()
            context = finding.get('context', '').lower()

            if query_lower in desc or query_lower in context:
                results.append({
                    "file_path": finding['path'],
                    "line": finding['line'],
                    "content": finding.get('description', ''),
                    "project": finding['project'],
                    "match_context": finding.get('context', '')
                })

                if len(results) >= limit:
                    break

        return results
