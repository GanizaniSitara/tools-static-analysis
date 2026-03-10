"""Multi-language code smell detector registry."""

from __future__ import annotations

from .csharp_detectors import CSHARP_DETECTORS
from .java_detectors import JAVA_DETECTORS
from .python_detectors import PYTHON_DETECTORS
from .javascript_detectors import JAVASCRIPT_DETECTORS

# Language-specific detector registries
# Each language has its own list of detector dictionaries
DETECTOR_REGISTRY: dict[str, list[dict]] = {
    "csharp": CSHARP_DETECTORS,
    "java": JAVA_DETECTORS,
    "python": PYTHON_DETECTORS,
    "javascript": JAVASCRIPT_DETECTORS,
    "typescript": JAVASCRIPT_DETECTORS,  # same detectors for TS
}

# Severity ordering for filtering
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEVERITY_WEIGHTS = {"critical": 15, "high": 8, "medium": 3, "low": 1}


def get_detectors(language: str, severity_filter: str = "low") -> list[dict]:
    """Get detectors for a language, filtered by minimum severity level.

    Args:
        language: Language identifier ("csharp", "java", etc.)
        severity_filter: Minimum severity level ("critical", "high", "medium", "low")
                        Default "low" includes all detectors.

    Returns:
        List of detector dictionaries filtered by severity
    """
    detectors = DETECTOR_REGISTRY.get(language, [])

    if severity_filter == "low":
        # Include all detectors
        return detectors

    # Filter by severity level
    max_severity_order = SEVERITY_ORDER.get(severity_filter, 3)
    filtered = [
        d for d in detectors
        if SEVERITY_ORDER.get(d["severity"], 3) <= max_severity_order
    ]

    return filtered


def get_all_detector_names(language: str) -> list[str]:
    """Get all detector names for a language.

    Args:
        language: Language identifier ("csharp", "java", etc.)

    Returns:
        List of detector names (e.g., ["hardcoded_secret", "sql_injection", ...])
    """
    detectors = DETECTOR_REGISTRY.get(language, [])
    return [d["name"] for d in detectors]


def get_supported_languages() -> list[str]:
    """Get list of supported languages.

    Returns:
        List of language identifiers (e.g., ["csharp", "java"])
    """
    return list(DETECTOR_REGISTRY.keys())
