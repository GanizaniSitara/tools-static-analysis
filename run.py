#!/usr/bin/env python3
"""Master runner: scans, diagrams, docs, web server."""

import http.server
import json
import os
import subprocess
import sys
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure scanner package is importable
sys.path.insert(0, SCRIPT_DIR)


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py /path/to/repos [output-name] [port]")
        print()
        print("  /path/to/repos   Directory containing repos to scan")
        print("  output-name      Output directory name (default: output)")
        print("  port             Web server port (default: 8000)")
        sys.exit(1)

    repos = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "output"
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000

    os.makedirs(out, exist_ok=True)

    print(f"=== Pipeline: {repos} → {out} ===\n")

    def run(script, *args):
        path = os.path.join(SCRIPT_DIR, script)
        result = subprocess.run([sys.executable, path, *args])
        if result.returncode != 0:
            print(f"ERROR: {script} failed (exit {result.returncode})")
            sys.exit(1)

    # Step 1: Scan projects (must complete first — produces project-meta.json, test-projects.json)
    print("--- Step 1: Scanning projects ---")
    run("1_scan_projects.py", repos, out)

    # Step 2: Scan smells (needs project-meta.json and test-projects.json from step 1)
    print("\n--- Step 2: Scanning smells ---")
    run("2_scan_smells.py", repos, out)

    # Run language scanners (auto-discovered plugins)
    print("\n--- Language scanners ---")
    try:
        from scanners import discover_scanners
        scanners = discover_scanners()
        if scanners:
            print(f"  Discovered {len(scanners)} scanner(s): {', '.join(s.display_name for s in scanners)}")

            # Discover repo directories (same logic as 1_scan_projects.py)
            repos_abs = os.path.abspath(repos)
            repo_dirs: list[tuple[str, str]] = []  # (name, path)
            # Check if root is a single repo
            has_subdirs = False
            for entry in sorted(os.listdir(repos_abs)):
                sub = os.path.join(repos_abs, entry)
                if os.path.isdir(sub) and not entry.startswith("."):
                    has_subdirs = True
                    repo_dirs.append((entry, sub))
            if not repo_dirs:
                repo_dirs = [(os.path.basename(repos_abs), repos_abs)]

            for scanner in scanners:
                detected_repos = []
                for repo_name, repo_path in repo_dirs:
                    try:
                        if scanner.detect(repo_path):
                            detected_repos.append((repo_name, repo_path))
                    except Exception as exc:
                        print(f"  Warning: {scanner.display_name} detect failed for {repo_name}: {exc}")

                if not detected_repos:
                    print(f"  {scanner.display_name}: no repos detected, skipping")
                    continue

                print(f"  {scanner.display_name}: scanning {len(detected_repos)} repo(s)...")
                all_projects: list[dict] = []
                combined_summary: dict = {}

                for repo_name, repo_path in detected_repos:
                    try:
                        result = scanner.scan(repo_path, repo_name)
                        all_projects.extend(result.get("projects", []))
                        # Merge summaries
                        if not combined_summary:
                            combined_summary = result.get("summary", {})
                        else:
                            s = result.get("summary", {})
                            combined_summary["totalProjects"] = combined_summary.get("totalProjects", 0) + s.get("totalProjects", 0)
                            combined_summary["totalFiles"] = combined_summary.get("totalFiles", 0) + s.get("totalFiles", 0)
                            combined_summary["totalLines"] = combined_summary.get("totalLines", 0) + s.get("totalLines", 0)
                            for fw, cnt in s.get("frameworks", {}).items():
                                combined_summary.setdefault("frameworks", {})[fw] = combined_summary.get("frameworks", {}).get(fw, 0) + cnt
                            for cat, cnt in s.get("categories", {}).items():
                                combined_summary.setdefault("categories", {})[cat] = combined_summary.get("categories", {}).get(cat, 0) + cnt
                    except Exception as exc:
                        print(f"  Warning: {scanner.display_name} scan failed for {repo_name}: {exc}")

                if all_projects:
                    output_data = {
                        "displayName": scanner.display_name,
                        "projects": all_projects,
                        "summary": combined_summary,
                    }
                    out_path = os.path.join(out, scanner.output_filename())
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(output_data, f, indent=2)
                    print(f"  {scanner.display_name}: {len(all_projects)} projects, wrote {scanner.output_filename()}")
                else:
                    print(f"  {scanner.display_name}: no projects found")
        else:
            print("  No language scanners found")
    except ImportError:
        print("  Language scanner module not available, skipping")

    # Step 3 needs graph.json from step 1
    print("\n--- Step 3: Generating diagrams ---")
    run("3_gen_diagrams.py", out)

    # Step 4 needs all outputs
    print("\n--- Step 4: Generating docs + viewer ---")
    run("4_gen_docs.py", out)

    print(f"\n=== Done. Opening viewer at http://localhost:{port}/viewer.html ===\n")

    os.chdir(out)
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(("", port), handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
