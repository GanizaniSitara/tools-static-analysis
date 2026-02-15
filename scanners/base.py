"""Base class for language-specific scanners."""

from __future__ import annotations

import os


class LanguageScanner:
    """Base class for language-specific scanners.

    Subclasses must set ``name``, ``display_name``, ``file_extensions``
    and implement ``detect()`` and ``scan()``.
    """

    name: str = ""  # e.g. "python", "java"
    display_name: str = ""  # e.g. "Python", "Java"
    file_extensions: tuple[str, ...] = ()  # e.g. (".py",)

    def detect(self, repo_path: str) -> bool:
        """Return True if *repo_path* contains projects of this language."""
        raise NotImplementedError

    def scan(self, repo_path: str, repo_name: str) -> dict:
        """Scan a repo and return language-specific project data.

        Must return a dict with at least ``projects`` (list) and
        ``summary`` (dict) keys plus a top-level ``displayName``.
        """
        raise NotImplementedError

    def output_filename(self) -> str:
        """JSON output filename, e.g. ``python-projects.json``."""
        return f"{self.name}-projects.json"

    # ── Helpers available to subclasses ──

    @staticmethod
    def _walk_files(root: str, extensions: tuple[str, ...],
                    max_depth: int = 20,
                    exclude_dirs: set[str] | None = None) -> list[str]:
        """Walk *root* and return files matching *extensions*."""
        if exclude_dirs is None:
            exclude_dirs = {"node_modules", ".git", "__pycache__", ".tox",
                            ".mypy_cache", ".pytest_cache", "venv", ".venv",
                            "env", ".env", "bin", "obj", "dist", "build"}
        results: list[str] = []
        root = os.path.normpath(root)
        for dirpath, dirnames, filenames in os.walk(root):
            depth = dirpath.replace(root, "").count(os.sep)
            if depth > max_depth:
                dirnames.clear()
                continue
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
            for fname in filenames:
                if any(fname.endswith(ext) for ext in extensions):
                    results.append(os.path.join(dirpath, fname))
        return results

    @staticmethod
    def _safe_read(filepath: str, max_size: int = 2 * 1024 * 1024) -> str | None:
        """Read a text file, returning None if too large or unreadable."""
        try:
            sz = os.path.getsize(filepath)
            if sz > max_size:
                return None
            with open(filepath, encoding="utf-8", errors="replace") as f:
                return f.read()
        except OSError:
            return None
