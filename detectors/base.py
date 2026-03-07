"""Base classes and utilities for code smell detectors."""

from __future__ import annotations
from typing import Callable

# Type alias for detector functions
# Signature: detect(file_path: str, content: str, lines: list[str]) -> list[dict]
DetectorFunction = Callable[[str, str, list[str]], list[dict]]


def create_detector(
    name: str,
    fn: DetectorFunction,
    severity: str,
    category: str
) -> dict:
    """Factory function for creating detector registry entries.

    Args:
        name: Detector identifier (e.g., "hardcoded_secret")
        fn: Detector function that returns list of smell dicts
        severity: One of "critical", "high", "medium", "low"
        category: One of "security", "bug", "quality", "interop", "style"

    Returns:
        Dictionary with detector metadata for registry
    """
    return {
        "name": name,
        "fn": fn,
        "severity": severity,
        "category": category,
    }
