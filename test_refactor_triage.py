#!/usr/bin/env python3
"""Tests for refactor_triage.py project inference and fallback logic."""

import os
import sys
import tempfile
import unittest

# refactor_triage.py runs module-level code (SCAN_ROOT, OUT_DIR, os.makedirs) on import,
# so we inject a harmless argv and import only the helpers we need.
sys.argv = ["refactor_triage.py", tempfile.gettempdir()]

# Now safe to import
from refactor_triage import (  # noqa: E402
    _normalize_path,
    infer_project_from_path,
    find_project_for_file,
)


class TestInferProjectFromPath(unittest.TestCase):
    """Test directory-based project name inference."""

    def test_finds_csproj_in_same_directory(self):
        """When a .csproj is in the same directory as the file, use its name."""
        with tempfile.TemporaryDirectory() as td:
            # Create structure: td/MyProject/MyProject.csproj, MyProject/File.cs
            proj_dir = os.path.join(td, "MyProject")
            os.makedirs(proj_dir)
            csproj_path = os.path.join(proj_dir, "MyProject.csproj")
            cs_file = os.path.join(proj_dir, "File.cs")
            
            open(csproj_path, "w").close()
            open(cs_file, "w").close()
            
            result = infer_project_from_path(cs_file, td)
            self.assertEqual(result, "MyProject")

    def test_finds_csproj_in_parent_directory(self):
        """Walk up to find a .csproj in a parent directory."""
        with tempfile.TemporaryDirectory() as td:
            # Create structure: td/MyProject/MyProject.csproj, MyProject/src/File.cs
            proj_dir = os.path.join(td, "MyProject")
            src_dir = os.path.join(proj_dir, "src")
            os.makedirs(src_dir)
            csproj_path = os.path.join(proj_dir, "MyProject.csproj")
            cs_file = os.path.join(src_dir, "File.cs")
            
            open(csproj_path, "w").close()
            open(cs_file, "w").close()
            
            result = infer_project_from_path(cs_file, td)
            self.assertEqual(result, "MyProject")

    def test_stops_at_scan_root(self):
        """Don't walk above scan_root when looking for .csproj."""
        with tempfile.TemporaryDirectory() as td:
            # Create structure: td/Parent.csproj, td/SubDir/File.cs
            parent_csproj = os.path.join(td, "Parent.csproj")
            sub_dir = os.path.join(td, "SubDir")
            os.makedirs(sub_dir)
            cs_file = os.path.join(sub_dir, "File.cs")
            
            open(parent_csproj, "w").close()
            open(cs_file, "w").close()
            
            # Set scan_root to SubDir, so it should NOT find Parent.csproj
            result = infer_project_from_path(cs_file, sub_dir)
            # Should fall back to directory name
            self.assertEqual(result, "_unknown")

    def test_fallback_to_top_level_directory(self):
        """If no .csproj found, use top-level directory name relative to scan root."""
        with tempfile.TemporaryDirectory() as td:
            # Create structure: td/MyFolder/src/File.cs (no .csproj)
            folder_dir = os.path.join(td, "MyFolder")
            src_dir = os.path.join(folder_dir, "src")
            os.makedirs(src_dir)
            cs_file = os.path.join(src_dir, "File.cs")
            
            open(cs_file, "w").close()
            
            result = infer_project_from_path(cs_file, td)
            self.assertEqual(result, "MyFolder")

    def test_fallback_to_unknown_when_no_structure(self):
        """Return _unknown when file is directly under scan root and no .csproj."""
        with tempfile.TemporaryDirectory() as td:
            cs_file = os.path.join(td, "File.cs")
            open(cs_file, "w").close()
            
            result = infer_project_from_path(cs_file, td)
            self.assertEqual(result, "_unknown")

    def test_prefers_nearest_csproj(self):
        """If multiple .csproj files exist in the walk-up, prefer the nearest one."""
        with tempfile.TemporaryDirectory() as td:
            # Create: td/Outer/Outer.csproj, td/Outer/Inner/Inner.csproj, td/Outer/Inner/File.cs
            outer_dir = os.path.join(td, "Outer")
            inner_dir = os.path.join(outer_dir, "Inner")
            os.makedirs(inner_dir)
            
            outer_csproj = os.path.join(outer_dir, "Outer.csproj")
            inner_csproj = os.path.join(inner_dir, "Inner.csproj")
            cs_file = os.path.join(inner_dir, "File.cs")
            
            open(outer_csproj, "w").close()
            open(inner_csproj, "w").close()
            open(cs_file, "w").close()
            
            result = infer_project_from_path(cs_file, td)
            # Should find Inner.csproj first (nearest)
            self.assertEqual(result, "Inner")


class TestFindProjectForFileWithFallback(unittest.TestCase):
    """Test the integration of find_project_for_file with the fallback."""

    def test_returns_none_when_project_meta_empty(self):
        """find_project_for_file returns None when project_meta is empty."""
        with tempfile.TemporaryDirectory() as td:
            cs_file = os.path.join(td, "File.cs")
            open(cs_file, "w").close()
            
            result = find_project_for_file(cs_file, [], td)
            self.assertIsNone(result)

    def test_matches_project_from_meta_when_available(self):
        """find_project_for_file finds a match when project-meta.json has valid entries."""
        with tempfile.TemporaryDirectory() as td:
            proj_dir = os.path.join(td, "MyProject")
            os.makedirs(proj_dir)
            csproj_path = os.path.join(proj_dir, "MyProject.csproj")
            cs_file = os.path.join(proj_dir, "File.cs")
            
            open(csproj_path, "w").close()
            open(cs_file, "w").close()
            
            project_meta = [
                {
                    "project": "MyProject",
                    "path": "MyProject/MyProject.csproj",
                    "globalPath": csproj_path,
                }
            ]
            
            result = find_project_for_file(cs_file, project_meta, td)
            self.assertEqual(result, "MyProject")


if __name__ == "__main__":
    unittest.main()
