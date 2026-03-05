"""Fix workflow state loader.

Loads and manages fix workflow state from .companion-fixes.json.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class FixLoader:
    """Loads and queries fix workflow state."""

    def __init__(self, project_root: str):
        """Initialize fix loader.

        Args:
            project_root: Path to project root directory
        """
        self.project_root = Path(project_root)
        self.fixes_file = self.project_root / ".companion-fixes.json"
        self._cache: Optional[Dict[str, Any]] = None

    def _load_fixes(self) -> Dict[str, Any]:
        """Load fixes from file.

        Returns:
            Dictionary of fix states keyed by fix ID
        """
        if self._cache is not None:
            return self._cache

        if not self.fixes_file.exists():
            return {}

        try:
            with open(self.fixes_file, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
                return self._cache
        except (json.JSONDecodeError, IOError):
            return {}

    def refresh(self):
        """Clear cache and reload from file."""
        self._cache = None

    def get_fix(self, fix_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific fix by ID.

        Args:
            fix_id: Fix identifier

        Returns:
            Fix data or None
        """
        fixes = self._load_fixes()
        return fixes.get(fix_id)

    def get_all_fixes(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all fixes with optional status filter.

        Args:
            status_filter: Optional status to filter by
                (checkout, branching, fixing, review, building, testing, submitting, done,
                 failed, build_failed, test_failed)

        Returns:
            List of fix states
        """
        fixes = self._load_fixes()
        result = []

        for fix_id, fix_data in fixes.items():
            if status_filter and fix_data.get('status') != status_filter:
                continue

            result.append({
                "fix_id": fix_id,
                **fix_data
            })

        return result

    def list_active_fixes(self) -> List[Dict[str, Any]]:
        """Get all active (non-terminal) fixes.

        Returns:
            List of active fix states
        """
        terminal_states = {'done', 'failed', 'build_failed', 'test_failed'}
        fixes = self._load_fixes()
        result = []

        for fix_id, fix_data in fixes.items():
            status = fix_data.get('status', '')
            if status not in terminal_states:
                result.append({
                    "fix_id": fix_id,
                    **fix_data
                })

        return result

    def save_fix(self, fix_id: str, fix_data: Dict[str, Any]) -> bool:
        """Save a fix state to file.

        Args:
            fix_id: Fix identifier
            fix_data: Fix state data

        Returns:
            True if successful
        """
        fixes = self._load_fixes()
        fixes[fix_id] = fix_data

        try:
            with open(self.fixes_file, 'w', encoding='utf-8') as f:
                json.dump(fixes, f, indent=2)
            self._cache = fixes
            return True
        except IOError:
            return False

    def delete_fix(self, fix_id: str) -> bool:
        """Delete a fix from state.

        Args:
            fix_id: Fix identifier

        Returns:
            True if successful
        """
        fixes = self._load_fixes()
        if fix_id not in fixes:
            return False

        del fixes[fix_id]

        try:
            with open(self.fixes_file, 'w', encoding='utf-8') as f:
                json.dump(fixes, f, indent=2)
            self._cache = fixes
            return True
        except IOError:
            return False
