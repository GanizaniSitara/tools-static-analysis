#!/usr/bin/env python3
"""Master runner: scans, diagrams, docs, web server."""

import html as html_mod
import http.server
import json
import os
import subprocess
import sys
import threading
from urllib.parse import urlparse, parse_qs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure scanner package is importable
sys.path.insert(0, SCRIPT_DIR)


class ViewerHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that adds a /_view endpoint for source file viewing."""

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/_view":
            params = parse_qs(parsed.query)
            file_path = params.get("path", [""])[0]
            line = int(params.get("line", ["0"])[0])
            self._serve_file_view(file_path, line)
            return
        super().do_GET()

    def _serve_file_view(self, file_path: str, highlight_line: int):
        """Render a source file as HTML with line numbers and highlighting."""
        if not file_path:
            self.send_error(400, "Missing path parameter")
            return
        real_path = os.path.realpath(file_path)
        if not os.path.isfile(real_path):
            self.send_error(404, f"File not found: {file_path}")
            return
        try:
            with open(real_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except OSError as exc:
            self.send_error(500, str(exc))
            return

        lines = content.split("\n")
        html_lines = []
        for i, line_text in enumerate(lines, 1):
            esc = html_mod.escape(line_text).replace("\t", "    ")
            cls = ' class="hl"' if i == highlight_line else ""
            html_lines.append(
                f'<tr{cls} id="L{i}"><td class="ln">{i}</td>'
                f'<td class="code"><pre>{esc}</pre></td></tr>'
            )

        fname = html_mod.escape(os.path.basename(real_path))
        fpath = html_mod.escape(real_path)
        line_note = f" &mdash; line {highlight_line}" if highlight_line else ""
        scroll = (
            f'<script>document.getElementById("L{highlight_line}")'
            f'.scrollIntoView({{block:"center"}});</script>'
            if highlight_line
            else ""
        )

        page = (
            "<!DOCTYPE html>\n"
            f"<html><head><meta charset='utf-8'><title>{fname}</title><style>\n"
            "body{margin:0;font-family:Consolas,'Courier New',monospace;"
            "background:#1e1e1e;color:#d4d4d4;font-size:13px;}\n"
            ".hdr{background:#252526;padding:0.5rem 1rem;border-bottom:1px solid #3c3c3c;"
            "font-size:0.85rem;position:sticky;top:0;z-index:1;}\n"
            ".hdr .p{color:#569cd6;}\n"
            "table{border-collapse:collapse;width:100%;}\n"
            ".ln{padding:0 0.8rem;text-align:right;color:#858585;user-select:none;"
            "border-right:1px solid #3c3c3c;vertical-align:top;min-width:3rem;}\n"
            ".code{padding:0 0 0 0.8rem;white-space:pre;}\n"
            ".code pre{margin:0;}\n"
            "tr.hl{background:rgba(255,255,0,0.15);}\n"
            "tr.hl .ln{color:#fff;font-weight:bold;}\n"
            "</style></head><body>\n"
            f'<div class="hdr"><span class="p">{fpath}</span>{line_note}</div>\n'
            f"<table>{''.join(html_lines)}</table>\n"
            f"{scroll}\n"
            "</body></html>"
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def log_message(self, fmt, *args):
        # Suppress noisy per-request logs except errors
        if args and str(args[0]).startswith("2"):
            return
        super().log_message(fmt, *args)


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
    server = http.server.HTTPServer(("", port), ViewerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
