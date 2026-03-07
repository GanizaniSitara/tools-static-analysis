"""Java language scanner — discovers Java projects and collects metadata."""

from __future__ import annotations

import os
import re

from .base import LanguageScanner

# Marker files that indicate a Java project root
_PROJECT_MARKERS = ("pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle")

# Framework detection patterns (applied to dependency names)
_FRAMEWORKS: dict[str, str] = {
    "spring-boot": "Spring Boot",
    "spring-webmvc": "Spring MVC",
    "spring-webflux": "Spring WebFlux",
    "jakarta.ee": "Jakarta EE",
    "jakarta.servlet-api": "Jakarta Servlet",
    "javax.servlet-api": "Java EE",
    "micronaut-core": "Micronaut",
    "micronaut-http": "Micronaut",
    "quarkus-core": "Quarkus",
    "quarkus-resteasy": "Quarkus",
    "play_": "Play Framework",
    "vert.x": "Vert.x",
    "dropwizard": "Dropwizard",
    "spark-core": "Spark Java",
}

_TEST_FRAMEWORKS: dict[str, str] = {
    "junit": "JUnit",
    "junit-jupiter": "JUnit 5",
    "testng": "TestNG",
    "spock": "Spock",
    "mockito": "Mockito",
    "assertj": "AssertJ",
}


class JavaScanner(LanguageScanner):
    name = "java"
    display_name = "Java"
    file_extensions = (".java",)

    def detect(self, repo_path: str) -> bool:
        """Return True if repo contains Java project indicators."""
        for marker in _PROJECT_MARKERS:
            if os.path.isfile(os.path.join(repo_path, marker)):
                return True
        # Fallback: check for .java files in src/main/java or at top level
        src_java = os.path.join(repo_path, "src", "main", "java")
        if os.path.isdir(src_java):
            java_files = self._walk_files(src_java, (".java",), max_depth=3)
            if java_files:
                return True
        # Check top level
        for entry in os.listdir(repo_path):
            if entry.endswith(".java"):
                return True
        return False

    def scan(self, repo_path: str, repo_name: str) -> dict:
        """Scan a repo and return Java project data."""
        projects: list[dict] = []
        seen_roots: set[str] = set()

        # 1. Find project roots via marker files
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in {
                "node_modules", ".git", "target", "build", "out",
                ".gradle", ".idea", ".vscode", "bin", ".settings",
                ".classpath", ".project", "dist",
            }]
            depth = root.replace(repo_path, "").count(os.sep)
            if depth > 10:
                dirs.clear()
                continue

            has_marker = any(f in files for f in _PROJECT_MARKERS)

            if has_marker:
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

        # If nothing found at all, treat repo root as a project if it has .java files
        if not projects:
            java_files = self._walk_files(repo_path, (".java",), max_depth=3)
            if java_files:
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
        """Analyze a single Java project directory."""
        rel_root = os.path.relpath(proj_root, repo_root)
        name = os.path.basename(proj_root) if proj_root != repo_root else repo_name

        # Count .java files and lines
        java_files = self._walk_files(proj_root, (".java",), max_depth=15)
        if not java_files:
            return None

        line_count = 0
        for fpath in java_files:
            content = self._safe_read(fpath)
            if content:
                line_count += content.count("\n") + 1

        # Detect build tool
        build_tool = self._detect_build_tool(proj_root)

        # Parse dependencies
        deps = self._parse_dependencies(proj_root, build_tool)

        # Detect frameworks
        dep_names_lower = {d.lower() for d in deps}
        detected_fw = ""
        for key, fw_name in _FRAMEWORKS.items():
            if any(key.lower() in dep.lower() for dep in deps):
                detected_fw = fw_name
                break

        # Detect test framework
        has_tests = False
        test_fw = ""
        for key, tfw_name in _TEST_FRAMEWORKS.items():
            if any(key.lower() in dep.lower() for dep in deps):
                has_tests = True
                test_fw = tfw_name
                break
        # Also check for test directories
        if not has_tests:
            for d in ("src/test/java", "test", "tests"):
                test_dir = os.path.join(proj_root, d.replace("/", os.sep))
                if os.path.isdir(test_dir):
                    test_files = self._walk_files(test_dir, (".java",), max_depth=5)
                    if test_files:
                        has_tests = True
                        test_fw = "JUnit"  # assume JUnit by default
                        break

        # Detect Java version
        java_version = self._detect_java_version(proj_root, build_tool)

        # Categorize
        category = self._categorize(proj_root, name, deps, detected_fw)

        return {
            "name": name,
            "repo": repo_name,
            "root": rel_root if rel_root != "." else "",
            "category": category,
            "framework": detected_fw,
            "buildTool": build_tool,
            "javaVersion": java_version,
            "dependencies": sorted(deps)[:50],
            "fileCount": len(java_files),
            "lineCount": line_count,
            "hasTests": has_tests,
            "testFramework": test_fw,
        }

    def _detect_build_tool(self, proj_root: str) -> str:
        """Detect whether project uses Maven or Gradle."""
        if os.path.isfile(os.path.join(proj_root, "pom.xml")):
            return "Maven"
        if os.path.isfile(os.path.join(proj_root, "build.gradle")) or \
           os.path.isfile(os.path.join(proj_root, "build.gradle.kts")):
            return "Gradle"
        return ""

    def _parse_dependencies(self, proj_root: str, build_tool: str) -> list[str]:
        """Parse dependencies from pom.xml or build.gradle."""
        deps: list[str] = []

        if build_tool == "Maven":
            deps = self._parse_maven_dependencies(proj_root)
        elif build_tool == "Gradle":
            deps = self._parse_gradle_dependencies(proj_root)

        # Deduplicate preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for d in deps:
            dl = d.lower()
            if dl not in seen:
                seen.add(dl)
                unique.append(d)
        return unique

    def _parse_maven_dependencies(self, proj_root: str) -> list[str]:
        """Parse dependencies from pom.xml using basic regex."""
        pom_path = os.path.join(proj_root, "pom.xml")
        if not os.path.isfile(pom_path):
            return []

        content = self._safe_read(pom_path)
        if not content:
            return []

        deps: list[str] = []
        # Extract <dependency> blocks with <groupId> and <artifactId>
        # Pattern: <dependency>...<groupId>group</groupId>...<artifactId>artifact</artifactId>...</dependency>
        dep_blocks = re.findall(
            r'<dependency[^>]*>(.*?)</dependency>',
            content,
            re.DOTALL
        )

        for block in dep_blocks:
            group_match = re.search(r'<groupId>([^<]+)</groupId>', block)
            artifact_match = re.search(r'<artifactId>([^<]+)</artifactId>', block)

            if group_match and artifact_match:
                group = group_match.group(1).strip()
                artifact = artifact_match.group(1).strip()
                # Format: groupId:artifactId
                deps.append(f"{group}:{artifact}")

        return deps

    def _parse_gradle_dependencies(self, proj_root: str) -> list[str]:
        """Parse dependencies from build.gradle or build.gradle.kts using basic regex."""
        gradle_files = ["build.gradle", "build.gradle.kts"]
        content = ""

        for gradle_file in gradle_files:
            gradle_path = os.path.join(proj_root, gradle_file)
            if os.path.isfile(gradle_path):
                content = self._safe_read(gradle_path)
                if content:
                    break

        if not content:
            return []

        deps: list[str] = []

        # Pattern: implementation 'group:artifact:version' or implementation "group:artifact:version"
        # Also: implementation("group:artifact:version") for Kotlin DSL
        patterns = [
            r'(?:implementation|api|compile|testImplementation|testCompile)\s*[(\'"]\s*([^\s\'"()]+)',
            r'(?:implementation|api|compile|testImplementation|testCompile)\s*\(\s*["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Extract group:artifact from group:artifact:version
                parts = match.split(":")
                if len(parts) >= 2:
                    dep = f"{parts[0]}:{parts[1]}"
                    deps.append(dep)

        return deps

    def _detect_java_version(self, proj_root: str, build_tool: str) -> str:
        """Try to detect the Java version from project config."""
        if build_tool == "Maven":
            pom_path = os.path.join(proj_root, "pom.xml")
            if os.path.isfile(pom_path):
                content = self._safe_read(pom_path)
                if content:
                    # Check for maven.compiler.source or maven.compiler.target
                    match = re.search(r'<maven\.compiler\.(?:source|target)>([^<]+)</maven\.compiler\.(?:source|target)>', content)
                    if match:
                        return match.group(1).strip()
                    # Check for java.version property
                    match = re.search(r'<java\.version>([^<]+)</java\.version>', content)
                    if match:
                        return match.group(1).strip()

        elif build_tool == "Gradle":
            gradle_files = ["build.gradle", "build.gradle.kts"]
            for gradle_file in gradle_files:
                gradle_path = os.path.join(proj_root, gradle_file)
                if os.path.isfile(gradle_path):
                    content = self._safe_read(gradle_path)
                    if content:
                        # Check for sourceCompatibility or targetCompatibility
                        match = re.search(r'(?:source|target)Compatibility\s*=\s*["\']?([0-9.]+)', content)
                        if match:
                            return match.group(1).strip()
                        # Check for JavaLanguageVersion
                        match = re.search(r'JavaLanguageVersion\.of\((\d+)\)', content)
                        if match:
                            return match.group(1).strip()

        return ""

    def _categorize(self, proj_root: str, name: str, deps: list[str],
                    framework: str) -> str:
        """Categorize the Java project."""
        name_lower = name.lower()
        dep_lower = {d.lower() for d in deps}

        # Web frameworks
        if framework in ("Spring Boot", "Spring MVC", "Spring WebFlux",
                        "Jakarta EE", "Jakarta Servlet", "Java EE",
                        "Micronaut", "Quarkus", "Play Framework",
                        "Vert.x", "Dropwizard", "Spark Java"):
            return "WebApp"

        # Test projects
        if any("junit" in d or "testng" in d or "spock" in d for d in dep_lower):
            if name_lower.startswith("test") or name_lower.endswith("tests") or \
               "test" in name_lower:
                return "Test"

        # Check for main class or Spring Boot application
        src_main = os.path.join(proj_root, "src", "main", "java")
        if os.path.isdir(src_main):
            java_files = self._walk_files(src_main, (".java",), max_depth=10)
            has_main = False
            for fpath in java_files[:20]:  # Check first 20 files
                content = self._safe_read(fpath)
                if content:
                    if "public static void main" in content or \
                       "@SpringBootApplication" in content:
                        has_main = True
                        break
            if has_main:
                return "Application"

        # Library if it has pom.xml or build.gradle but no main class
        if os.path.isfile(os.path.join(proj_root, "pom.xml")) or \
           os.path.isfile(os.path.join(proj_root, "build.gradle")) or \
           os.path.isfile(os.path.join(proj_root, "build.gradle.kts")):
            return "Library"

        return "Application"
