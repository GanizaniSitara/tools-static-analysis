#!/usr/bin/env python3
"""Master runner: scans, diagrams, docs, web server."""

import html as html_mod
import http.server
import json
import os
import shutil
import subprocess
import sys
import threading
from urllib.parse import urlparse, parse_qs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure scanner package is importable
sys.path.insert(0, SCRIPT_DIR)


def _is_wsl() -> bool:
    """Detect if running under Windows Subsystem for Linux."""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except OSError:
        return False


def _find_solution(file_path: str, repo_roots: dict, solutions_map: dict) -> str:
    """Find the .sln file that likely contains the given source file."""
    fp = file_path.replace("\\", "/")
    # Match file to a repo root
    best_repo = ""
    best_root = ""
    for repo_name, root in repo_roots.items():
        r = root.replace("\\", "/")
        if fp.startswith(r + "/") or fp.startswith(r + "\\"):
            if len(r) > len(best_root):
                best_root = r
                best_repo = repo_name
    if best_repo and best_repo in solutions_map:
        solutions = solutions_map[best_repo]
        if len(solutions) == 1:
            return os.path.join(best_root, solutions[0])
        # Multiple solutions: pick the one whose directory is closest to the file
        rel = fp[len(best_root) + 1:]
        best_sln = solutions[0]
        best_depth = 0
        for sln in solutions:
            sln_dir = os.path.dirname(sln).replace("\\", "/")
            if rel.startswith(sln_dir + "/") and len(sln_dir) > best_depth:
                best_sln = sln
                best_depth = len(sln_dir)
        return os.path.join(best_root, best_sln)
    # Fallback: search upward from the file for a .sln
    dir_path = os.path.dirname(file_path)
    for _ in range(20):  # max depth
        if not dir_path or dir_path == os.path.dirname(dir_path):
            break
        try:
            for entry in os.listdir(dir_path):
                if entry.endswith(".sln"):
                    return os.path.join(dir_path, entry)
        except OSError:
            break
        dir_path = os.path.dirname(dir_path)
    return ""


class ViewerHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with /_view and /_open endpoints for IDE integration."""

    # Set by main() before server starts
    repo_roots: dict = {}
    solutions_map: dict = {}

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/_view":
            params = parse_qs(parsed.query)
            file_path = params.get("path", [""])[0]
            line = int(params.get("line", ["0"])[0])
            self._serve_file_view(file_path, line)
            return
        if parsed.path == "/_open":
            params = parse_qs(parsed.query)
            self._handle_open(params)
            return
        super().do_GET()

    # ── /_view: render source file in browser ──

    def _serve_file_view(self, file_path: str, highlight_line: int):
        """Render a source file as HTML with line numbers and highlighting."""
        if not file_path:
            self._json_error(400, "Missing path parameter")
            return
        real_path = os.path.realpath(file_path)
        if not os.path.isfile(real_path):
            self._json_error(404, f"File not found: {file_path}")
            return
        try:
            with open(real_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except OSError as exc:
            self._json_error(500, str(exc))
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

    # ── /_open: launch editors ──

    def _handle_open(self, params: dict):
        editor = params.get("editor", [""])[0]
        file_path = params.get("path", [""])[0]
        line = int(params.get("line", ["0"])[0])

        if not file_path:
            self._json_error(400, "Missing path parameter")
            return

        if editor == "studio":
            self._open_visual_studio(file_path, line)
        elif editor == "code":
            self._open_vscode(file_path, line)
        elif editor == "claude":
            self._open_claude(file_path)
        else:
            self._json_error(400, f"Unknown editor: {editor}")

    def _open_visual_studio(self, file_path: str, line: int):
        """Open file in Visual Studio 2022 with the nearest solution."""
        sln = _find_solution(file_path, self.repo_roots, self.solutions_map)
        if not sln:
            self._json_response({"error": "No .sln solution file found for this file"}, 404)
            return

        is_win = sys.platform == "win32"
        is_wsl = _is_wsl()

        if is_win:
            # Windows native: launch devenv directly
            cmd = ["devenv", sln]
            if file_path:
                cmd.extend(["/edit", file_path])
            try:
                subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS)
                self._json_response({"status": "ok", "editor": "studio", "solution": sln})
            except FileNotFoundError:
                self._json_response({"error": "devenv.exe not found — is Visual Studio 2022 installed?"}, 500)
        elif is_wsl:
            # WSL: convert paths to Windows and call devenv.exe
            try:
                win_sln = subprocess.check_output(
                    ["wslpath", "-w", sln], text=True
                ).strip()
                win_file = subprocess.check_output(
                    ["wslpath", "-w", file_path], text=True
                ).strip()
                cmd = ["cmd.exe", "/c", "start", "", "devenv.exe", win_sln, "/edit", win_file]
                subprocess.Popen(cmd)
                self._json_response({"status": "ok", "editor": "studio", "solution": win_sln})
            except FileNotFoundError:
                self._json_response({"error": "WSL path conversion failed — is wslpath available?"}, 500)
            except subprocess.CalledProcessError as exc:
                self._json_response({"error": f"Failed to convert path: {exc}"}, 500)
        else:
            # Native Linux: Visual Studio not available, suggest VS Code
            self._json_response(
                {"error": "Visual Studio 2022 is not available on Linux. Use Code (VS Code) instead."},
                501,
            )

    def _open_vscode(self, file_path: str, line: int):
        """Open file in VS Code via CLI."""
        code_cmd = shutil.which("code")
        if not code_cmd:
            self._json_response({"error": "VS Code (code) not found in PATH"}, 500)
            return
        goto = f"{file_path}:{line}" if line else file_path
        try:
            subprocess.Popen([code_cmd, "--goto", goto])
            self._json_response({"status": "ok", "editor": "code"})
        except OSError as exc:
            self._json_response({"error": f"Failed to launch VS Code: {exc}"}, 500)

    def _open_claude(self, file_path: str):
        """Open Claude Code in a terminal at the file's directory."""
        dir_path = os.path.dirname(file_path) if os.path.isfile(file_path) else file_path
        if not os.path.isdir(dir_path):
            self._json_response({"error": f"Directory not found: {dir_path}"}, 404)
            return

        claude_cmd = shutil.which("claude")
        if not claude_cmd:
            self._json_response({"error": "Claude Code CLI (claude) not found in PATH"}, 500)
            return

        # Try terminal emulators in order of preference
        launched = False
        shell_cmd = f'cd "{dir_path}" && claude'
        terminals = [
            (["gnome-terminal", "--", "bash", "-c", shell_cmd], "gnome-terminal"),
            (["x-terminal-emulator", "-e", f"bash -c '{shell_cmd}'"], "x-terminal-emulator"),
            (["xterm", "-e", f"bash -c '{shell_cmd}'"], "xterm"),
            (["konsole", "-e", f"bash -c '{shell_cmd}'"], "konsole"),
        ]

        if sys.platform == "win32":
            # Windows: use cmd.exe start
            try:
                subprocess.Popen(["cmd.exe", "/c", "start", "claude"], cwd=dir_path)
                launched = True
            except OSError:
                pass
        elif _is_wsl():
            # WSL: use Windows Terminal or cmd.exe
            try:
                win_dir = subprocess.check_output(
                    ["wslpath", "-w", dir_path], text=True
                ).strip()
                subprocess.Popen(
                    ["cmd.exe", "/c", "start", "wsl.exe", "--cd", dir_path, "claude"]
                )
                launched = True
            except (OSError, subprocess.CalledProcessError):
                pass

        if not launched:
            for cmd, name in terminals:
                if shutil.which(cmd[0]):
                    try:
                        subprocess.Popen(cmd)
                        launched = True
                        break
                    except OSError:
                        continue

        if launched:
            self._json_response({"status": "ok", "editor": "claude", "directory": dir_path})
        else:
            self._json_response(
                {"error": "No terminal emulator found. Install gnome-terminal, xterm, or konsole."},
                500,
            )

    # ── Response helpers ──

    def _json_response(self, data: dict, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json_error(self, status: int, message: str):
        self._json_response({"error": message}, status)

    def log_message(self, fmt, *args):
        # Suppress noisy per-request logs except errors
        if args and str(args[0]).startswith("2"):
            return
        super().log_message(fmt, *args)


def main():
    import argparse as _ap
    parser = _ap.ArgumentParser(description="Pipeline: scans, diagrams, docs, web server.")
    parser.add_argument("repos", help="Directory containing repos to scan")
    parser.add_argument("out", nargs="?", default="output", help="Output directory name (default: output)")
    parser.add_argument("port", nargs="?", type=int, default=8000, help="Web server port (default: 8000)")
    parser.add_argument("--level", choices=["critical", "high", "medium", "low"], default="high",
                        help="Minimum severity level for smell scanner (default: high)")
    args = parser.parse_args()

    repos = args.repos
    out = args.out
    port = args.port
    level = args.level

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
    run("2_scan_smells.py", repos, out, "--level", level)

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

    # Load repos.json for solution discovery
    repos_json_path = os.path.join(out, "repos.json")
    if os.path.isfile(repos_json_path):
        try:
            with open(repos_json_path, "r", encoding="utf-8") as f:
                repos_data = json.load(f)
            ViewerHandler.repo_roots = {r["name"]: r.get("root", "") for r in repos_data}
            ViewerHandler.solutions_map = {r["name"]: r.get("solutions", []) for r in repos_data}
            print(f"  Loaded {len(repos_data)} repo(s) from repos.json for IDE integration")
        except (json.JSONDecodeError, KeyError) as exc:
            print(f"  Warning: could not parse repos.json: {exc}")

    print(f"\n=== Done. Opening viewer at http://localhost:{port}/viewer.html ===\n")

    os.chdir(out)
    server = http.server.HTTPServer(("", port), ViewerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
