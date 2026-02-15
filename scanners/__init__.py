"""Scanner plugin auto-discovery."""

from __future__ import annotations

import importlib
import os
import sys

from .base import LanguageScanner


def discover_scanners() -> list[LanguageScanner]:
    """Import all ``*_scanner.py`` modules in this directory and return
    instances of concrete :class:`LanguageScanner` subclasses.
    """
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    instances: list[LanguageScanner] = []

    for fname in sorted(os.listdir(pkg_dir)):
        if not fname.endswith("_scanner.py"):
            continue
        module_name = fname[:-3]  # strip .py
        full_module = f"scanners.{module_name}"
        try:
            mod = importlib.import_module(full_module)
        except Exception as exc:
            print(f"  Warning: could not import scanner {full_module}: {exc}")
            continue

        for attr_name in dir(mod):
            obj = getattr(mod, attr_name)
            if (
                isinstance(obj, type)
                and issubclass(obj, LanguageScanner)
                and obj is not LanguageScanner
                and getattr(obj, "name", "")
            ):
                instances.append(obj())

    return instances
