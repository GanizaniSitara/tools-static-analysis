"""JavaScript/TypeScript language scanner — discovers JS/TS projects and collects metadata."""

from __future__ import annotations

import json
import os
import re

from .base import LanguageScanner

# Marker files that indicate a JS/TS project root
_PROJECT_MARKERS = ("package.json",)

# Framework detection patterns (applied to dependency names)
_FRAMEWORKS: dict[str, str] = {
    "next": "Next.js",
    "react": "React",
    "@angular/core": "Angular",
    "vue": "Vue",
    "nuxt": "Nuxt",
    "svelte": "Svelte",
    "@sveltejs/kit": "SvelteKit",
    "astro": "Astro",
    "@remix-run/react": "Remix",
    "gatsby": "Gatsby",
    "express": "Express",
    "@nestjs/core": "NestJS",
    "fastify": "Fastify",
    "koa": "Koa",
    "@hapi/hapi": "Hapi",
    "electron": "Electron",
    "react-native": "React Native",
    "@ionic/angular": "Ionic",
    "ember-source": "Ember",
    "preact": "Preact",
    "solid-js": "Solid",
    "qwik": "Qwik",
}

_TEST_FRAMEWORKS: dict[str, str] = {
    "jest": "Jest",
    "mocha": "Mocha",
    "vitest": "Vitest",
    "cypress": "Cypress",
    "@playwright/test": "Playwright",
    "playwright": "Playwright",
    "jasmine": "Jasmine",
    "ava": "AVA",
    "tape": "Tape",
}

_EXCLUDE_DIRS = {
    "node_modules", ".git", ".next", ".nuxt", "dist", "build", "coverage",
    ".turbo", ".cache", ".output", "__pycache__", ".svelte-kit",
    "out", ".vercel", ".netlify", "storybook-static",
}


class JavaScriptScanner(LanguageScanner):
    name = "javascript"
    display_name = "JavaScript/TypeScript"
    file_extensions = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")

    def detect(self, repo_path: str) -> bool:
        """Return True if repo contains JS/TS project indicators."""
        for marker in _PROJECT_MARKERS:
            if os.path.isfile(os.path.join(repo_path, marker)):
                return True
        # Fallback: check for source files at top level or in src/
        for entry in os.listdir(repo_path):
            if any(entry.endswith(ext) for ext in self.file_extensions):
                return True
        src_dir = os.path.join(repo_path, "src")
        if os.path.isdir(src_dir):
            src_files = self._walk_files(src_dir, self.file_extensions, max_depth=2)
            if src_files:
                return True
        return False

    def scan(self, repo_path: str, repo_name: str) -> dict:
        """Scan a repo and return JS/TS project data."""
        projects: list[dict] = []
        seen_roots: set[str] = set()

        # Find project roots via package.json
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in _EXCLUDE_DIRS]
            depth = root.replace(repo_path, "").count(os.sep)
            if depth > 10:
                dirs.clear()
                continue

            has_marker = "package.json" in files

            if has_marker:
                norm = os.path.normpath(root)
                # Skip if nested inside an already-found project
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

        # If nothing found, treat repo root as a project if it has source files
        if not projects:
            src_files = self._walk_files(repo_path, self.file_extensions, max_depth=3)
            if src_files:
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
        """Analyze a single JS/TS project directory."""
        rel_root = os.path.relpath(proj_root, repo_root)
        name = os.path.basename(proj_root) if proj_root != repo_root else repo_name

        # Count source files and lines
        src_files = self._walk_files(
            proj_root, self.file_extensions, max_depth=15, exclude_dirs=_EXCLUDE_DIRS
        )
        if not src_files:
            return None

        line_count = 0
        for fpath in src_files:
            content = self._safe_read(fpath)
            if content:
                line_count += content.count("\n") + 1

        # Parse package.json
        pkg = self._load_package_json(proj_root)
        if not pkg and not src_files:
            return None

        # Extract dependencies
        deps = self._parse_dependencies(pkg)

        # Detect frameworks
        dep_names = set(deps)
        detected_fw = ""
        for key, fw_name in _FRAMEWORKS.items():
            if key in dep_names:
                detected_fw = fw_name
                break

        # Detect test framework
        has_tests = False
        test_fw = ""
        for key, tfw_name in _TEST_FRAMEWORKS.items():
            if key in dep_names:
                has_tests = True
                test_fw = tfw_name
                break
        # Also check for test directories
        if not has_tests:
            for d in ("__tests__", "test", "tests", "spec", "e2e"):
                test_dir = os.path.join(proj_root, d)
                if os.path.isdir(test_dir):
                    test_files = self._walk_files(
                        test_dir, self.file_extensions, max_depth=5, exclude_dirs=_EXCLUDE_DIRS
                    )
                    if test_files:
                        has_tests = True
                        test_fw = "Jest"  # assume Jest by default
                        break

        # Detect build tool
        build_tool = self._detect_build_tool(proj_root)

        # Detect Node.js version
        node_version = self._detect_node_version(proj_root, pkg)

        # Use package.json name if available
        pkg_name = pkg.get("name", "") if pkg else ""
        if pkg_name and pkg_name != name:
            name = pkg_name

        # Categorize
        category = self._categorize(proj_root, name, deps, detected_fw, pkg)

        return {
            "name": name,
            "repo": repo_name,
            "root": rel_root if rel_root != "." else "",
            "category": category,
            "framework": detected_fw,
            "buildTool": build_tool,
            "nodeVersion": node_version,
            "dependencies": sorted(deps)[:50],
            "fileCount": len(src_files),
            "lineCount": line_count,
            "hasTests": has_tests,
            "testFramework": test_fw,
        }

    def _load_package_json(self, proj_root: str) -> dict | None:
        """Load and parse package.json."""
        pkg_path = os.path.join(proj_root, "package.json")
        if not os.path.isfile(pkg_path):
            return None
        content = self._safe_read(pkg_path)
        if not content:
            return None
        try:
            return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            return None

    def _parse_dependencies(self, pkg: dict | None) -> list[str]:
        """Extract dependency names from package.json."""
        if not pkg:
            return []
        deps: list[str] = []
        for key in ("dependencies", "devDependencies", "peerDependencies"):
            section = pkg.get(key, {})
            if isinstance(section, dict):
                deps.extend(section.keys())
        # Deduplicate preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for d in deps:
            if d not in seen:
                seen.add(d)
                unique.append(d)
        return unique

    def _detect_build_tool(self, proj_root: str) -> str:
        """Detect the package manager used."""
        if os.path.isfile(os.path.join(proj_root, "pnpm-lock.yaml")):
            return "pnpm"
        if os.path.isfile(os.path.join(proj_root, "yarn.lock")):
            return "Yarn"
        if os.path.isfile(os.path.join(proj_root, "bun.lockb")) or \
           os.path.isfile(os.path.join(proj_root, "bun.lock")):
            return "Bun"
        if os.path.isfile(os.path.join(proj_root, "package-lock.json")):
            return "npm"
        return ""

    def _detect_node_version(self, proj_root: str, pkg: dict | None) -> str:
        """Detect Node.js version from project config."""
        # .nvmrc
        nvmrc = os.path.join(proj_root, ".nvmrc")
        if os.path.isfile(nvmrc):
            content = self._safe_read(nvmrc)
            if content:
                return content.strip().splitlines()[0].strip()

        # .node-version
        nv_file = os.path.join(proj_root, ".node-version")
        if os.path.isfile(nv_file):
            content = self._safe_read(nv_file)
            if content:
                return content.strip().splitlines()[0].strip()

        # package.json engines.node
        if pkg:
            engines = pkg.get("engines", {})
            if isinstance(engines, dict) and "node" in engines:
                return str(engines["node"])

        return ""

    def _categorize(self, proj_root: str, name: str, deps: list[str],
                    framework: str, pkg: dict | None) -> str:
        """Categorize the JS/TS project."""
        name_lower = name.lower()
        dep_set = set(deps)

        # Web app frameworks
        if framework in ("React", "Angular", "Vue", "Svelte", "SvelteKit",
                         "Next.js", "Nuxt", "Gatsby", "Astro", "Remix",
                         "Ember", "Preact", "Solid", "Qwik", "Ionic"):
            return "WebApp"

        # Server frameworks
        if framework in ("Express", "NestJS", "Fastify", "Koa", "Hapi"):
            return "WebApp"

        # Desktop
        if framework == "Electron":
            return "Application"

        # Mobile
        if framework == "React Native":
            return "Application"

        # CLI tool — has bin field
        if pkg and pkg.get("bin"):
            return "Tool"

        # Test project
        if name_lower.startswith("test") or name_lower.endswith("tests") or \
           "test" in name_lower.split("-"):
            return "Test"

        # Library — has main or exports field
        if pkg and (pkg.get("main") or pkg.get("exports") or pkg.get("module")):
            return "Library"

        # Worker
        worker_deps = {"bull", "bullmq", "bee-queue", "agenda", "node-cron"}
        if dep_set & worker_deps:
            return "Worker"

        return "Application"
