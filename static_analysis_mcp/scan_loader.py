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

    def _load_triage(self) -> Dict[str, Any]:
        """Load triage status data.

        Returns:
            Triage data dictionary or empty dict if not found
        """
        data = self._load_json('triage.json')
        return data or {}

    def _get_triage_status(self, finding: Dict[str, Any], triage: Dict[str, Any]) -> Dict[str, Any]:
        """Get triage status for a finding.

        Args:
            finding: Finding dictionary
            triage: Triage data

        Returns:
            Triage status dict
        """
        key = f"{finding['project']}:{finding['path']}:{finding['line']}"
        entry = triage.get(key, {})

        return {
            "status": entry.get('status', 'open'),
            "assigned_to": entry.get('assigned_to'),
            "notes": entry.get('notes'),
            "updated_at": entry.get('updated_at')
        }

    def _get_fan_in(self, project_id: str, graph: Dict[str, Any]) -> int:
        """Get fan-in (incoming dependencies) for a project.

        Args:
            project_id: Project identifier
            graph: Dependency graph

        Returns:
            Number of incoming dependencies
        """
        edges = graph.get('edges', [])
        return len([e for e in edges if e.get('target') == project_id or e.get('to') == project_id])

    def _get_project_dependencies(self, project_id: str, graph: Dict[str, Any]) -> Dict[str, Any]:
        """Get dependency information for a project.

        Args:
            project_id: Project identifier
            graph: Dependency graph

        Returns:
            Dependency information
        """
        nodes = {n['id']: n for n in graph.get('nodes', [])}
        edges = graph.get('edges', [])

        # Find fan-in and fan-out
        fan_in = len([e for e in edges if (e.get('target') == project_id or e.get('to') == project_id)])
        fan_out = len([e for e in edges if (e.get('source') == project_id or e.get('from') == project_id)])

        # Get dependent modules (those that depend on this project)
        dependent_ids = [e.get('source') or e.get('from') for e in edges
                        if (e.get('target') == project_id or e.get('to') == project_id)]
        dependent_modules = [nodes[nid].get('project', '') for nid in dependent_ids if nid in nodes]

        return {
            "fan_in": fan_in,
            "fan_out": fan_out,
            "dependent_modules": dependent_modules,
            "blast_radius": "high" if fan_in > 5 else "medium" if fan_in > 2 else "low"
        }

    def _get_file_metrics(self, file_path: str, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get complexity metrics for a file from project metrics.

        Args:
            file_path: File path
            metrics: Project metrics list

        Returns:
            File metrics dictionary
        """
        # For now, return simplified metrics
        # In a real implementation, we'd parse file-level metrics from the scan
        return {
            "cyclomatic": 5,  # Default placeholder
            "nesting_depth": 3,
            "method_count": 0,
            "lines_of_code": 0
        }

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension.

        Args:
            file_path: File path

        Returns:
            Language identifier
        """
        ext = Path(file_path).suffix.lower()
        lang_map = {
            '.cs': 'csharp',
            '.java': 'java',
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c'
        }
        return lang_map.get(ext, 'unknown')

    def _estimate_effort(self, finding: Dict[str, Any]) -> str:
        """Estimate effort required to fix a finding.

        Args:
            finding: Finding dictionary

        Returns:
            Effort estimate (trivial|low|medium|high)
        """
        # Simple heuristic based on severity and complexity
        severity = finding.get('severity', 'low')
        smell_type = finding.get('smell_type', '')

        # Security issues often require more careful changes
        if finding.get('category') == 'security':
            if severity in ['critical', 'high']:
                return 'medium'
            return 'low'

        # Complex refactoring smells
        if smell_type in ['god_method', 'god_class', 'feature_envy']:
            return 'high'

        # Simple fixes
        if smell_type in ['magic_number', 'hardcoded_string']:
            return 'trivial'

        # Default based on severity
        effort_map = {
            'critical': 'medium',
            'high': 'medium',
            'medium': 'low',
            'low': 'trivial'
        }
        return effort_map.get(severity, 'low')

    def _extract_pattern(self, context: str) -> str:
        """Extract a pattern key from code context.

        Args:
            context: Code context string

        Returns:
            Pattern key for grouping
        """
        # Simple pattern extraction - normalize whitespace and extract core pattern
        if not context:
            return "unknown"

        # Remove extra whitespace
        normalized = ' '.join(context.split())

        # Truncate to first 50 chars for pattern matching
        pattern = normalized[:50] if len(normalized) > 50 else normalized

        return pattern

    def get_prioritized_findings(
        self,
        filters: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get findings sorted by priority score.

        Priority considers:
        - Severity (critical > high > medium > low)
        - Security category (weighted higher)
        - Blast radius (dependencies affected)
        - Effort estimate (lower effort = higher priority)
        - Triage status (in_progress on top, resolved filtered out)

        Args:
            filters: Optional filter dict (severity, category, project, etc.)
            limit: Maximum results to return

        Returns:
            List of findings with priority scores and rankings
        """
        findings = self.get_all_findings(filters)

        # Load dependency graph for blast radius
        graph = self.get_dependency_graph()
        if 'isError' in graph:
            graph = {"nodes": [], "edges": []}

        # Load triage to skip resolved
        triage = self._load_triage()

        scored_findings = []
        for finding in findings:
            # Check triage status first
            triage_status = self._get_triage_status(finding, triage)
            if triage_status['status'] in ['resolved', 'wont_fix', 'false_positive']:
                continue  # Skip resolved/closed findings

            # Calculate priority score
            score = self._calculate_priority_score(finding, graph, triage)
            finding['priority_score'] = score
            finding['priority_rank'] = 0  # Will be set after sorting

            # Add contextual information
            project_id = f"{finding['repo']}/{finding['project']}"
            deps = self._get_project_dependencies(project_id, graph)
            finding['blast_radius'] = deps['blast_radius']
            finding['effort_estimate'] = self._estimate_effort(finding)
            finding['has_tests'] = False  # TODO: Get from project metrics

            scored_findings.append(finding)

        # Sort by score descending
        scored_findings.sort(key=lambda x: x['priority_score'], reverse=True)

        # Add ranks
        for i, f in enumerate(scored_findings):
            f['priority_rank'] = i + 1

        return scored_findings[:limit]

    def _calculate_priority_score(
        self,
        finding: Dict,
        graph: Dict,
        triage: Dict
    ) -> float:
        """Calculate priority score for a finding.

        Args:
            finding: Finding dictionary
            graph: Dependency graph
            triage: Triage data

        Returns:
            Priority score (higher = more important)
        """
        # Severity weights
        severity_map = {'critical': 10, 'high': 7, 'medium': 4, 'low': 1}
        severity_weight = severity_map.get(finding.get('severity', 'low'), 1)

        # Security bonus
        security_bonus = 5 if finding.get('category') == 'security' else 0

        # Blast radius from dependency graph
        project_id = f"{finding['repo']}/{finding['project']}"
        fan_in = self._get_fan_in(project_id, graph)

        # Effort estimate (lower is better, so negative)
        effort_map = {'trivial': 1, 'low': 2, 'medium': 4, 'high': 8}
        effort = effort_map.get(self._estimate_effort(finding), 2)

        # Triage priority boost
        triage_status = self._get_triage_status(finding, triage)
        if triage_status['status'] == 'in_progress':
            return 1000  # Top priority - already being worked on

        score = (
            severity_weight * 10 +
            security_bonus +
            fan_in * 2 +
            -effort * 0.5
        )

        return score

    def get_rich_context(
        self,
        project: str,
        file_path: str,
        line: int
    ) -> Dict[str, Any]:
        """Assemble rich context for fixing a finding.

        Includes:
        - Finding details
        - Source code with context
        - Related findings in same file
        - Similar patterns in codebase
        - Dependency information
        - Complexity metrics
        - Triage status
        - Fix guidance

        Args:
            project: Project name
            file_path: File path
            line: Line number

        Returns:
            Rich context dictionary
        """
        finding = self.get_finding_at(project, file_path, line)

        if not finding:
            return {"isError": True, "message": "Finding not found"}

        # 1. Source code with more context
        source_code = self.get_file_content(file_path, line - 10, line + 10)

        # 2. Related findings in same file
        all_findings = self.get_all_findings({'project': project})
        related = [f for f in all_findings
                  if f['path'] == file_path and f['line'] != line]

        # 3. Similar patterns in codebase
        similar = self.find_similar_smells(
            finding['smell_type'],
            group_by="file",
            limit=5
        )

        # 4. Dependencies
        graph = self.get_dependency_graph()
        if 'isError' in graph:
            graph = {"nodes": [], "edges": []}

        project_id = f"{finding['repo']}/{project}"
        deps = self._get_project_dependencies(project_id, graph)

        # 5. Complexity metrics
        metrics = self.get_project_metrics(project)
        file_metrics = self._get_file_metrics(file_path, metrics)

        # 6. Triage status
        triage = self._load_triage()
        triage_status = self._get_triage_status(finding, triage)

        # 7. Test coverage info
        project_metrics = metrics[0] if metrics else {}
        test_coverage = {
            "project_has_tests": project_metrics.get('has_tests', False),
            "file_has_tests": False  # TODO: File-level test detection
        }

        return {
            "finding": finding,
            "source_code": {
                "full": source_code,
                "target_line": line,
                "before": source_code.split('\n')[:10] if source_code else [],
                "after": source_code.split('\n')[10:] if source_code else []
            },
            "related_findings": related,
            "similar_patterns": similar[:3] if isinstance(similar, list) else [],
            "dependencies": deps,
            "complexity": file_metrics,
            "test_coverage": test_coverage,
            "triage": triage_status,
            "fix_guidance": {
                "prompt_template": finding['smell_type'],
                "language": self._detect_language(file_path),
                "estimated_effort": self._estimate_effort(finding)
            }
        }

    def find_similar_smells(
        self,
        smell_type: str,
        group_by: str = "pattern",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Find all instances of a smell type.

        Args:
            smell_type: Type of code smell
            group_by: Grouping strategy ("pattern", "file", "project")
            limit: Maximum results

        Returns:
            List of findings or grouped results
        """
        findings = self.get_all_findings({'smell_type': smell_type})

        if group_by == "pattern":
            # Group by similar code patterns
            patterns = {}
            for f in findings:
                context = f.get('context', '')
                pattern_key = self._extract_pattern(context)

                if pattern_key not in patterns:
                    patterns[pattern_key] = {
                        "pattern": context[:100] if context else pattern_key,
                        "count": 0,
                        "instances": []
                    }

                patterns[pattern_key]['count'] += 1
                patterns[pattern_key]['instances'].append({
                    "file": f['path'],
                    "line": f['line'],
                    "project": f['project'],
                    "context": f.get('context', '')
                })

            result = list(patterns.values())
            # Sort by count descending
            result.sort(key=lambda x: x['count'], reverse=True)
            return result

        elif group_by == "file":
            # Group by file
            files = {}
            for f in findings:
                file_key = f['path']
                if file_key not in files:
                    files[file_key] = {
                        "file": file_key,
                        "project": f['project'],
                        "count": 0,
                        "instances": []
                    }

                files[file_key]['count'] += 1
                files[file_key]['instances'].append({
                    "line": f['line'],
                    "context": f.get('context', '')
                })

            result = list(files.values())
            result.sort(key=lambda x: x['count'], reverse=True)
            return result

        elif group_by == "project":
            # Group by project
            projects = {}
            for f in findings:
                project_key = f['project']
                if project_key not in projects:
                    projects[project_key] = {
                        "project": project_key,
                        "count": 0,
                        "instances": []
                    }

                projects[project_key]['count'] += 1
                projects[project_key]['instances'].append({
                    "file": f['path'],
                    "line": f['line'],
                    "context": f.get('context', '')
                })

            result = list(projects.values())
            result.sort(key=lambda x: x['count'], reverse=True)
            return result

        # Default: return list of findings
        return findings[:limit]
