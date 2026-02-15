"""Python language scanner — discovers Python projects and collects metadata."""

from __future__ import annotations

import configparser
import os
import re

from .base import LanguageScanner

# Marker files that indicate a Python project root
_PROJECT_MARKERS = ("pyproject.toml", "setup.py", "setup.cfg")
_DEP_FILES = ("requirements.txt", "Pipfile")

# Framework detection patterns (applied to dependency names)
_FRAMEWORKS: dict[str, str] = {
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "starlette": "Starlette",
    "tornado": "Tornado",
    "aiohttp": "aiohttp",
    "bottle": "Bottle",
    "pyramid": "Pyramid",
    "sanic": "Sanic",
    "celery": "Celery",
    "airflow": "Airflow",
    "scrapy": "Scrapy",
    "streamlit": "Streamlit",
    "gradio": "Gradio",
}

_TEST_FRAMEWORKS: dict[str, str] = {
    "pytest": "pytest",
    "unittest": "unittest",
    "nose": "nose",
    "nose2": "nose2",
    "tox": "tox",
}


class PythonScanner(LanguageScanner):
    name = "python"
    display_name = "Python"
    file_extensions = (".py",)

    def detect(self, repo_path: str) -> bool:
        """Return True if repo contains Python project indicators."""
        for marker in _PROJECT_MARKERS + _DEP_FILES:
            if os.path.isfile(os.path.join(repo_path, marker)):
                return True
        # Fallback: check for .py files at top level or one level down
        for entry in os.listdir(repo_path):
            if entry.endswith(".py"):
                return True
            sub = os.path.join(repo_path, entry)
            if os.path.isdir(sub) and os.path.isfile(os.path.join(sub, "__init__.py")):
                return True
        return False

    def scan(self, repo_path: str, repo_name: str) -> dict:
        """Scan a repo and return Python project data."""
        projects: list[dict] = []
        seen_roots: set[str] = set()

        # 1. Find project roots via marker files
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in {
                "node_modules", ".git", "__pycache__", ".tox", ".mypy_cache",
                ".pytest_cache", "venv", ".venv", "env", ".env",
                "bin", "obj", "dist", "build", ".eggs", "*.egg-info",
            }]
            depth = root.replace(repo_path, "").count(os.sep)
            if depth > 10:
                dirs.clear()
                continue

            has_marker = any(f in files for f in _PROJECT_MARKERS)
            has_dep = any(f in files for f in _DEP_FILES)
            has_init = "__init__.py" in files and root != repo_path

            if has_marker or has_dep or (has_init and depth <= 2):
                norm = os.path.normpath(root)
                # Skip if this is nested inside an already-found project
                skip = False
                for sr in seen_roots:
                    if norm.startswith(sr + os.sep):
                        skip = True
                        break
                if skip:
                    continue
                seen_roots.add(norm)

                proj = self._analyze_project(root, repo_path, repo_name)
                if proj:
                    projects.append(proj)

        # If nothing found at all, treat repo root as a project if it has .py files
        if not projects:
            py_files = self._walk_files(repo_path, (".py",), max_depth=3)
            if py_files:
                proj = self._analyze_project(repo_path, repo_path, repo_name)
                if proj:
                    projects.append(proj)

        # Build summary
        total_files = sum(p.get("fileCount", 0) for p in projects)
        total_lines = sum(p.get("lineCount", 0) for p in projects)
        fw_counts: dict[str, int] = {}
        cat_counts: dict[str, int] = {}
        for p in projects:
            fw = p.get("framework", "")
            if fw:
                fw_counts[fw] = fw_counts.get(fw, 0) + 1
            cat = p.get("category", "")
            if cat:
                cat_counts[cat] = cat_counts.get(cat, 0) + 1

        return {
            "displayName": self.display_name,
            "projects": projects,
            "summary": {
                "totalProjects": len(projects),
                "totalFiles": total_files,
                "totalLines": total_lines,
                "frameworks": fw_counts,
                "categories": cat_counts,
            },
        }

    def _analyze_project(self, proj_root: str, repo_root: str, repo_name: str) -> dict | None:
        """Analyze a single Python project directory."""
        rel_root = os.path.relpath(proj_root, repo_root)
        name = os.path.basename(proj_root) if proj_root != repo_root else repo_name

        # Count .py files and lines
        py_files = self._walk_files(proj_root, (".py",), max_depth=15)
        if not py_files:
            return None

        line_count = 0
        for fpath in py_files:
            content = self._safe_read(fpath)
            if content:
                line_count += content.count("\n") + 1

        # Parse dependencies
        deps = self._parse_dependencies(proj_root)

        # Detect frameworks
        dep_names_lower = {d.lower() for d in deps}
        detected_fw = ""
        for key, fw_name in _FRAMEWORKS.items():
            if key in dep_names_lower:
                detected_fw = fw_name
                break

        # Detect test framework
        has_tests = False
        test_fw = ""
        for key, tfw_name in _TEST_FRAMEWORKS.items():
            if key in dep_names_lower:
                has_tests = True
                test_fw = tfw_name
                break
        # Also check for test directories
        if not has_tests:
            for d in ("tests", "test"):
                test_dir = os.path.join(proj_root, d)
                if os.path.isdir(test_dir):
                    test_files = self._walk_files(test_dir, (".py",), max_depth=5)
                    if test_files:
                        has_tests = True
                        test_fw = "pytest"  # assume pytest by default
                        break

        # Detect Python version
        python_version = self._detect_python_version(proj_root)

        # Categorize
        category = self._categorize(proj_root, name, deps, detected_fw)

        return {
            "name": name,
            "repo": repo_name,
            "root": rel_root if rel_root != "." else "",
            "category": category,
            "framework": detected_fw,
            "pythonVersion": python_version,
            "dependencies": sorted(deps)[:50],
            "fileCount": len(py_files),
            "lineCount": line_count,
            "hasTests": has_tests,
            "testFramework": test_fw,
        }

    def _parse_dependencies(self, proj_root: str) -> list[str]:
        """Parse dependencies from requirements.txt, pyproject.toml, or Pipfile."""
        deps: list[str] = []

        # requirements.txt
        req_path = os.path.join(proj_root, "requirements.txt")
        if os.path.isfile(req_path):
            content = self._safe_read(req_path)
            if content:
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith("-"):
                        continue
                    # Extract package name (before version specifier)
                    pkg = re.split(r"[>=<!\[;]", line)[0].strip()
                    if pkg:
                        deps.append(pkg)

        # pyproject.toml (basic parsing without toml library)
        pyproj_path = os.path.join(proj_root, "pyproject.toml")
        if os.path.isfile(pyproj_path):
            content = self._safe_read(pyproj_path)
            if content:
                # Look for dependencies = [...] or install_requires
                in_deps = False
                for line in content.splitlines():
                    stripped = line.strip()
                    if re.match(r"^dependencies\s*=\s*\[", stripped):
                        in_deps = True
                        # Check for inline deps on same line
                        bracket_content = re.search(r"\[(.+)\]", stripped)
                        if bracket_content:
                            for dep in bracket_content.group(1).split(","):
                                dep = dep.strip().strip('"').strip("'")
                                pkg = re.split(r"[>=<!\[;]", dep)[0].strip()
                                if pkg:
                                    deps.append(pkg)
                            in_deps = False
                        continue
                    if in_deps:
                        if "]" in stripped:
                            in_deps = False
                            continue
                        dep = stripped.strip('",').strip("',").strip()
                        if dep:
                            pkg = re.split(r"[>=<!\[;]", dep)[0].strip()
                            if pkg:
                                deps.append(pkg)

        # setup.py (basic regex extraction)
        setup_path = os.path.join(proj_root, "setup.py")
        if os.path.isfile(setup_path) and not deps:
            content = self._safe_read(setup_path)
            if content:
                # Look for install_requires=[...]
                match = re.search(
                    r"install_requires\s*=\s*\[(.*?)\]", content, re.DOTALL
                )
                if match:
                    for dep_str in match.group(1).split(","):
                        dep = dep_str.strip().strip('"').strip("'")
                        pkg = re.split(r"[>=<!\[;]", dep)[0].strip()
                        if pkg:
                            deps.append(pkg)

        # Pipfile
        pipfile_path = os.path.join(proj_root, "Pipfile")
        if os.path.isfile(pipfile_path) and not deps:
            content = self._safe_read(pipfile_path)
            if content:
                in_packages = False
                for line in content.splitlines():
                    stripped = line.strip()
                    if stripped == "[packages]":
                        in_packages = True
                        continue
                    if stripped.startswith("["):
                        in_packages = False
                        continue
                    if in_packages and "=" in stripped:
                        pkg = stripped.split("=")[0].strip().strip('"')
                        if pkg:
                            deps.append(pkg)

        # Deduplicate preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for d in deps:
            dl = d.lower()
            if dl not in seen:
                seen.add(dl)
                unique.append(d)
        return unique

    def _detect_python_version(self, proj_root: str) -> str:
        """Try to detect the Python version from project config."""
        # Check pyproject.toml for requires-python
        pyproj = os.path.join(proj_root, "pyproject.toml")
        if os.path.isfile(pyproj):
            content = self._safe_read(pyproj)
            if content:
                match = re.search(r'requires-python\s*=\s*"([^"]+)"', content)
                if match:
                    return match.group(1)

        # Check .python-version file
        pv_file = os.path.join(proj_root, ".python-version")
        if os.path.isfile(pv_file):
            content = self._safe_read(pv_file)
            if content:
                return content.strip().splitlines()[0].strip()

        # Check setup.cfg
        setup_cfg = os.path.join(proj_root, "setup.cfg")
        if os.path.isfile(setup_cfg):
            content = self._safe_read(setup_cfg)
            if content:
                match = re.search(r"python_requires\s*=\s*(.+)", content)
                if match:
                    return match.group(1).strip()

        return ""

    def _categorize(self, proj_root: str, name: str, deps: list[str],
                    framework: str) -> str:
        """Categorize the Python project."""
        name_lower = name.lower()
        dep_lower = {d.lower() for d in deps}

        if framework in ("Django", "Flask", "FastAPI", "Starlette", "Tornado",
                         "aiohttp", "Bottle", "Pyramid", "Sanic"):
            return "WebApp"

        if framework in ("Celery", "Airflow"):
            return "Worker"

        if framework in ("Scrapy",):
            return "Tool"

        if framework in ("Streamlit", "Gradio"):
            return "WebApp"

        # Check for setup.py/pyproject.toml with package build config
        if os.path.isfile(os.path.join(proj_root, "setup.py")) or \
           os.path.isfile(os.path.join(proj_root, "pyproject.toml")):
            # Check for console_scripts
            pyproj = os.path.join(proj_root, "pyproject.toml")
            if os.path.isfile(pyproj):
                content = self._safe_read(pyproj)
                if content and "console_scripts" in content:
                    return "Tool"

            setup = os.path.join(proj_root, "setup.py")
            if os.path.isfile(setup):
                content = self._safe_read(setup)
                if content and "console_scripts" in content:
                    return "Tool"

        # Test project
        if "pytest" in dep_lower or "unittest" in dep_lower or \
           name_lower.startswith("test") or name_lower.endswith("tests"):
            return "Test"

        # Default
        if os.path.isfile(os.path.join(proj_root, "setup.py")) or \
           os.path.isfile(os.path.join(proj_root, "pyproject.toml")):
            return "Library"

        return "Application"
