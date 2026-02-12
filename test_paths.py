#!/usr/bin/env python3
"""Tests for Windows path normalisation in find_files / discover_repos."""

import os
import sys
import tempfile
import unittest

# analyze.py runs module-level code (SCAN_ROOT, OUT_DIR, os.makedirs) on import,
# so we inject a harmless argv and import only the helpers we need.
sys.argv = ["analyze.py", tempfile.gettempdir()]

# Now safe to import
from analyze import _normalize_path, find_files, discover_repos  # noqa: E402


class TestNormalizePath(unittest.TestCase):
    """Ensure _normalize_path converts backslashes and handles long paths."""

    def test_backslash_replaced(self):
        self.assertEqual(_normalize_path(r"C:\Users\dev\repo"), "C:/Users/dev/repo")

    def test_double_backslash_replaced(self):
        result = _normalize_path("C:\\\\foo\\\\bar")
        self.assertNotIn("\\", result)

    def test_forward_slash_unchanged(self):
        self.assertEqual(_normalize_path("/home/user/repo"), "/home/user/repo")

    def test_mixed_slashes(self):
        result = _normalize_path("C:\\repos/sub\\dir")
        self.assertNotIn("\\", result)

    def test_empty_string(self):
        self.assertEqual(_normalize_path(""), "")


class TestFindFilesNormalized(unittest.TestCase):
    """Ensure find_files returns forward-slash paths."""

    def test_results_have_no_backslashes(self):
        import re
        with tempfile.TemporaryDirectory() as td:
            # Create a nested structure
            nested = os.path.join(td, "a", "b")
            os.makedirs(nested)
            open(os.path.join(nested, "hello.csproj"), "w").close()

            results = find_files(td, re.compile(r"\.csproj$"))
            self.assertEqual(len(results), 1)
            self.assertNotIn("\\", results[0])
            self.assertTrue(results[0].endswith("hello.csproj"))


class TestDiscoverReposNormalized(unittest.TestCase):
    """Ensure discover_repos returns forward-slash root paths."""

    def test_root_has_sln(self):
        with tempfile.TemporaryDirectory() as td:
            # Create .sln and .csproj so discover_repos doesn't sys.exit
            open(os.path.join(td, "My.sln"), "w").close()
            nested = os.path.join(td, "src")
            os.makedirs(nested)
            open(os.path.join(nested, "App.csproj"), "w").close()

            repos = discover_repos(td)
            self.assertEqual(len(repos), 1)
            self.assertNotIn("\\", repos[0]["root"])

    def test_multi_repo_mode(self):
        with tempfile.TemporaryDirectory() as td:
            for name in ("RepoA", "RepoB"):
                d = os.path.join(td, name)
                os.makedirs(d)
                open(os.path.join(d, f"{name}.csproj"), "w").close()

            repos = discover_repos(td)
            self.assertEqual(len(repos), 2)
            for r in repos:
                self.assertNotIn("\\", r["root"])
                for sln in r["solutions"]:
                    self.assertNotIn("\\", sln)


if __name__ == "__main__":
    unittest.main()
