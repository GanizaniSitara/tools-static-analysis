"""Triage decision loader and manager.

Manages triage decisions stored in <output-dir>/triage.json.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class TriageLoader:
    """Loads and manages triage decisions."""

    def __init__(self, triage_file: Path):
        """Initialize triage loader.

        Args:
            triage_file: Path to triage.json file
        """
        self.triage_file = triage_file
        self._cache: Optional[Dict[str, Any]] = None

    def _load_triage(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load triage decisions from file.

        Returns:
            Dictionary mapping project -> list of triage decisions
        """
        if self._cache is not None:
            return self._cache

        if not self.triage_file.exists():
            return {}

        try:
            with open(self.triage_file, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
                return self._cache
        except (json.JSONDecodeError, IOError):
            return {}

    def refresh(self):
        """Clear cache and reload from file."""
        self._cache = None

    def get_triage(self, project: str, file_path: str, line: int) -> Optional[Dict[str, Any]]:
        """Get triage decision for a specific finding.

        Args:
            project: Project name
            file_path: File path
            line: Line number

        Returns:
            Triage decision or None
        """
        triage_data = self._load_triage()
        project_triage = triage_data.get(project, [])

        for decision in project_triage:
            if (decision.get('file_path') == file_path and
                decision.get('line') == line):
                return decision

        return None

    def get_all_triage(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all triage decisions with optional status filter.

        Args:
            status_filter: Optional status to filter by
                (open, in_progress, resolved, wont_fix, false_positive)

        Returns:
            List of triage decisions
        """
        triage_data = self._load_triage()
        result = []

        for project, decisions in triage_data.items():
            for decision in decisions:
                if status_filter and decision.get('status') != status_filter:
                    continue
                result.append(decision)

        return result

    def update_triage(self, project: str, file_path: str, line: int,
                     status: str, assigned_to: Optional[str] = None,
                     notes: Optional[str] = None) -> bool:
        """Update or create a triage decision.

        Args:
            project: Project name
            file_path: File path
            line: Line number
            status: Triage status (open, in_progress, resolved, wont_fix, false_positive)
            assigned_to: Optional assignee
            notes: Optional notes

        Returns:
            True if successful
        """
        triage_data = self._load_triage()

        if project not in triage_data:
            triage_data[project] = []

        # Find existing decision
        existing = None
        for i, decision in enumerate(triage_data[project]):
            if (decision.get('file_path') == file_path and
                decision.get('line') == line):
                existing = i
                break

        # Create or update decision
        decision = {
            "project": project,
            "file_path": file_path,
            "line": line,
            "status": status,
            "updated_at": datetime.now().isoformat()
        }

        if assigned_to:
            decision["assigned_to"] = assigned_to
        if notes:
            decision["notes"] = notes

        if existing is not None:
            # Preserve smell_type if it exists
            old_smell = triage_data[project][existing].get('smell_type')
            if old_smell:
                decision["smell_type"] = old_smell
            triage_data[project][existing] = decision
        else:
            triage_data[project].append(decision)

        # Save to file
        try:
            # Create parent directory if needed
            self.triage_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.triage_file, 'w', encoding='utf-8') as f:
                json.dump(triage_data, f, indent=2)
            self._cache = triage_data
            return True
        except IOError:
            return False

    def delete_triage(self, project: str, file_path: str, line: int) -> bool:
        """Delete a triage decision.

        Args:
            project: Project name
            file_path: File path
            line: Line number

        Returns:
            True if successful
        """
        triage_data = self._load_triage()

        if project not in triage_data:
            return False

        # Find and remove decision
        original_len = len(triage_data[project])
        triage_data[project] = [
            d for d in triage_data[project]
            if not (d.get('file_path') == file_path and d.get('line') == line)
        ]

        if len(triage_data[project]) == original_len:
            return False  # Nothing removed

        # Save to file
        try:
            with open(self.triage_file, 'w', encoding='utf-8') as f:
                json.dump(triage_data, f, indent=2)
            self._cache = triage_data
            return True
        except IOError:
            return False
