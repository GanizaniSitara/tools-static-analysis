"""Base class for security platform integrations."""

from __future__ import annotations

import json
import os
from datetime import datetime


class SecurityIntegration:
    """Base class for security platform adapters.

    Each integration can:
    - **export**: Push local findings to the external platform
    - **import_findings**: Pull findings from the external platform
    - **test_connection**: Verify API connectivity

    Subclasses must set ``name`` and ``display_name`` and implement
    at least ``export_findings()`` and ``import_findings()``.
    """

    name: str = ""            # e.g. "armorcode", "sonarqube"
    display_name: str = ""    # e.g. "ArmorCode", "SonarQube"

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self._demo_mode = not self._has_credentials()

    def _has_credentials(self) -> bool:
        """Return True if required credentials are present in config."""
        return False

    def test_connection(self) -> dict:
        """Test connectivity to the platform.

        Returns dict with keys: connected (bool), message (str), demo (bool).
        """
        return {"connected": False, "message": "Not implemented", "demo": True}

    def export_findings(self, findings: list[dict], metadata: dict | None = None) -> dict:
        """Push local findings to the external platform.

        Args:
            findings: List of normalized findings (tool, ruleId, severity, etc.)
            metadata: Optional scan metadata (scanRoot, generated, etc.)

        Returns dict with: status, findingsExported (int), platform, details.
        """
        raise NotImplementedError

    def import_findings(self, **kwargs) -> dict:
        """Pull findings from the external platform.

        Returns dict matching the external-tools.json schema:
            tool, version, status, findingCount, findings[], truncated.
        """
        raise NotImplementedError

    @property
    def is_demo(self) -> bool:
        return self._demo_mode

    @staticmethod
    def _normalize_severity(raw: str) -> str:
        """Map various severity strings to our standard set."""
        raw = raw.strip().lower()
        mapping = {
            "critical": "critical", "crit": "critical", "very-high": "critical",
            "high": "high", "major": "high",
            "medium": "medium", "moderate": "medium", "med": "medium",
            "low": "low", "minor": "low", "info": "low",
            "informational": "low",
        }
        return mapping.get(raw, "medium")

    @staticmethod
    def _timestamp() -> str:
        return datetime.now().isoformat()
