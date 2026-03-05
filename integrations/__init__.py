"""Security platform integration discovery and registry."""

from __future__ import annotations

import importlib
import os

from .base import SecurityIntegration

KNOWN_INTEGRATIONS = ["armorcode", "sonarqube"]


def discover_integrations(config: dict | None = None) -> dict[str, SecurityIntegration]:
    """Import all integration modules and return instances keyed by name.

    Scans this directory for modules matching known integration names
    and instantiates each adapter with the provided config section.
    """
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    registry: dict[str, SecurityIntegration] = {}

    for fname in sorted(os.listdir(pkg_dir)):
        if not fname.endswith(".py") or fname.startswith("_"):
            continue
        module_name = fname[:-3]
        if module_name == "base":
            continue
        full_module = f"integrations.{module_name}"
        try:
            mod = importlib.import_module(full_module)
        except Exception as exc:
            print(f"  Warning: could not import integration {full_module}: {exc}")
            continue

        for attr_name in dir(mod):
            obj = getattr(mod, attr_name)
            if (
                isinstance(obj, type)
                and issubclass(obj, SecurityIntegration)
                and obj is not SecurityIntegration
                and getattr(obj, "name", "")
            ):
                # Pass the integration-specific config section
                section = (config or {}).get(obj.name, {})
                registry[obj.name] = obj(section)

    return registry
