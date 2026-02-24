#!/usr/bin/env python3
"""Master runner: scans, diagrams, docs, web server."""

import html as html_mod
import http.server
import json
import os
import shlex
import shutil
import subprocess
import sys
import threading
import yaml
from pathlib import Path
from urllib.parse import urlparse, parse_qs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure scanner package is importable
sys.path.insert(0, SCRIPT_DIR)


def _load_config():
    """Load configuration from config.yaml with defaults."""
    config_path = Path(__file__).parent / "config.yaml"
    default = {
        "claudePrompt": "Please analyze this code and propose improvements.",
        "claudeCodePath": "claude",
        "githubCopilotEnabled": True,
        "copilotMode": "standalone",
        "copilotCliPath": "copilot",
        "copilotModel": "claude-opus-4.6",
    }
    if not config_path.exists():
        return default
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return {**default, **yaml.safe_load(f)}
    except Exception:
        return default


CONFIG = _load_config()


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


def _find_devenv() -> str:
    """Find Visual Studio 2022 devenv.exe in common installation paths."""
    # First try PATH
    devenv_cmd = shutil.which("devenv")
    if devenv_cmd:
        return devenv_cmd

    # Common VS 2022 installation paths
    common_paths = [
        r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\devenv.exe",
        r"C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\devenv.exe",
        r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\devenv.exe",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2022\Professional\Common7\IDE\devenv.exe",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe",
    ]

    for path in common_paths:
        if os.path.isfile(path):
            return path

    return ""


class ViewerHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with /_view and /_open endpoints for IDE integration."""

    # Set by main() before server starts
    repo_roots: dict = {}
    solutions_map: dict = {}

    # Set by main() so /_stop can shut down the server
    _server_ref = None

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
        if parsed.path == "/_stop":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Server stopping.\n")
            print("\nServer stopped via /_stop endpoint.")
            threading.Thread(target=self._server_ref.shutdown, daemon=True).start()
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
        line = int(params.get("line", ["0"])[0]) if params.get("line", ["0"])[0] else None
        project_name = params.get("project", [None])[0]
        smell_description = params.get("smell", [None])[0]

        if not file_path:
            self._json_error(400, "Missing path parameter")
            return

        if editor == "studio":
            self._open_visual_studio(file_path, line)
        elif editor == "code":
            self._open_vscode(file_path, line)
        elif editor == "claude":
            self._open_claude(file_path, line, project_name, smell_description)
        elif editor == "copilot":
            self._open_github_copilot(file_path, line, project_name, smell_description)
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
            # Windows native: find and launch devenv
            devenv_path = _find_devenv()
            if not devenv_path:
                self._json_response({"error": "devenv.exe not found — is Visual Studio 2022 installed?"}, 500)
                return

            cmd = [devenv_path, sln]
            if file_path:
                cmd.extend(["/edit", file_path])
            try:
                subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS)
                self._json_response({"status": "ok", "editor": "studio", "solution": sln})
            except FileNotFoundError:
                self._json_response({"error": "devenv.exe not found -- is Visual Studio 2022 installed?"}, 500)
        else:
            self._json_response(
                {"error": "Visual Studio 2022 is not available on Linux. Use Code (VS Code) instead."},
                501,
            )

    def _open_vscode(self, file_path: str, line: int):
        """Open file in VS Code with solution directory as workspace."""
        code_cmd = shutil.which("code")
        if not code_cmd:
            self._json_response({"error": "VS Code (code) not found in PATH"}, 500)
            return

        # Find solution file using existing helper
        sln_path = _find_solution(file_path, self.repo_roots, self.solutions_map)

        cmd = [code_cmd]
        workspace_dir = None

        if sln_path:
            # Open solution directory as workspace
            workspace_dir = str(Path(sln_path).parent)
            cmd.append(workspace_dir)

            # Make file path relative to workspace for proper association
            try:
                rel_path = os.path.relpath(file_path, workspace_dir)
                # Use relative path if file is within workspace, otherwise use absolute
                if not rel_path.startswith(".."):
                    file_path = rel_path
            except ValueError:
                # Different drives on Windows, keep absolute path
                pass

        # Navigate to specific file and line
        # Using --goto ensures the file opens at the specific line
        cmd.extend(["--goto", f"{file_path}:{line or 1}"])

        try:
            subprocess.Popen(cmd, start_new_session=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._json_response({"status": "ok", "editor": "code",
                               "workspace": workspace_dir,
                               "solution": sln_path if sln_path else None})
        except OSError as exc:
            self._json_response({"error": f"Failed to launch VS Code: {exc}"}, 500)

    def _open_claude(self, file_path: str, line: int = None, project_name: str = None,
                     smell_description: str = None):
        """Open Claude Code with context: workspace dir, file:line, and custom prompt."""
        sln_path = _find_solution(file_path, self.repo_roots, self.solutions_map)
        if not sln_path:
            self._json_response({"error": "No .sln solution file found for this file"}, 404)
            return

        workspace_dir = str(Path(sln_path).parent)

        # Build prompt: use focused smell prompt if provided, else generic config prompt
        if smell_description and '\n' in smell_description:
            prompt = smell_description
            if project_name:
                prompt += f"\n\nProject: {project_name}"
        else:
            prompt_parts = [CONFIG["claudePrompt"]]
            if project_name:
                prompt_parts.append(f"\n\nProject: {project_name}")
            if smell_description:
                prompt_parts.append(f"\n\nArchitectural Smell:\n{smell_description}")
            prompt = "".join(prompt_parts)

        # Make file path relative to solution directory for Claude
        try:
            rel_file_path = os.path.relpath(file_path, workspace_dir)
        except ValueError:
            rel_file_path = file_path

        claude_args = f'@{rel_file_path}' + (f':{line}' if line else '')
        claude_args += f' --append-system-prompt "{prompt}"'

        if sys.platform == "win32":
            cmd_str = f'start "" /d "{workspace_dir}" claude {claude_args}'
            try:
                subprocess.Popen(cmd_str, shell=True)
                self._json_response({"status": "ok", "editor": "claude", "workspace": workspace_dir, "mode": "windows"})
            except OSError as exc:
                self._json_response({"error": f"Failed to launch Claude Code: {exc}"}, 500)
        else:
            # Linux/macOS native
            claude_cmd = CONFIG.get("claudeCodePath", "claude")
            cmd = f'{claude_cmd} --add-dir {shlex.quote(workspace_dir)} @{file_path}'
            if line:
                cmd += f':{line}'
            cmd += f' --append-system-prompt {shlex.quote(prompt)}'
            try:
                subprocess.Popen(["bash", "-c", cmd], start_new_session=True,
                               cwd=workspace_dir)
                self._json_response({"status": "ok", "editor": "claude", "workspace": workspace_dir, "mode": "native"})
            except OSError as exc:
                self._json_response({"error": f"Failed to launch Claude Code: {exc}"}, 500)

    def _open_github_copilot(self, file_path: str, line: int = None, project_name: str = None,
                             smell_description: str = None):
        """Launch GitHub Copilot CLI in interactive mode with context."""
        if not CONFIG.get("githubCopilotEnabled"):
            self._json_response({"error": "GitHub Copilot is disabled in config.yaml"}, 400)
            return

        copilot_path = CONFIG.get("copilotCliPath", "copilot")
        copilot_mode = CONFIG.get("copilotMode", "standalone")
        copilot_model = CONFIG.get("copilotModel", "claude-opus-4.6")

        sln_path = _find_solution(file_path, self.repo_roots, self.solutions_map)
        work_dir = str(Path(sln_path).parent) if sln_path else os.path.dirname(file_path)

        if copilot_mode == "gh-extension":
            # Legacy gh copilot extension -- limited flags
            context = f"Analyze file {file_path}"
            if line:
                context += f" at line {line}"
            if smell_description:
                context += f". Issue: {smell_description}"
            if project_name:
                context += f" (Project: {project_name})"

            if sys.platform == "win32":
                safe_context = context.replace('"', '\\"')
                cmd_str = f'start "" /d "{work_dir}" gh copilot suggest -t shell "{safe_context}"'
                try:
                    subprocess.Popen(cmd_str, shell=True)
                    self._json_response({"status": "ok", "editor": "copilot", "mode": "windows",
                                         "copilotMode": copilot_mode})
                except OSError as exc:
                    self._json_response({"error": f"Failed to launch Copilot: {exc}"}, 500)
            else:
                try:
                    subprocess.Popen(
                        ["gh", "copilot", "suggest", "-t", "shell", context],
                        cwd=work_dir, start_new_session=True
                    )
                    self._json_response({"status": "ok", "editor": "copilot", "mode": "native",
                                         "copilotMode": copilot_mode})
                except OSError as exc:
                    self._json_response({"error": f"Failed to launch Copilot: {exc}"}, 500)
            return

        # Standalone mode: use -i (interactive + execute prompt) instead of -p (exits)
        # Build prompt using same claudePrompt config that Claude Code uses, since
        # Copilot CLI has no --system-prompt flag (instructions baked into the prompt).

        # Make path relative to workspace
        try:
            rel_file = os.path.relpath(file_path, work_dir)
        except ValueError:
            rel_file = file_path

        if smell_description and '\n' in smell_description:
            # Focused smell prompt (pre-built by the viewer) -- use as-is, same as Claude
            prompt = smell_description
            if project_name:
                prompt += f"\n\nProject: {project_name}"
        else:
            # Generic prompt from config -- same structure Claude receives
            prompt = CONFIG["claudePrompt"]
            if project_name:
                prompt += f"\n\nProject: {project_name}"
            if smell_description:
                prompt += f"\n\nArchitectural Smell:\n{smell_description}"

        prompt += f"\n\nFile: {rel_file}"
        if line:
            prompt += f" (line {line})"
        prompt += "\n\nPlease read the file above and propose concrete code changes to address the issue."

        # Use -i for interactive mode (stays open), --model for Opus, --add-dir for workspace
        copilot_args = [
            "--model", copilot_model,
            "--add-dir", work_dir,
            "-i", prompt,
        ]

        if sys.platform == "win32":
            safe_prompt = prompt.replace('"', '\\"')
            cmd_str = (f'start "" /d "{work_dir}" {copilot_path}'
                       f' --model {copilot_model}'
                       f' --add-dir "{work_dir}"'
                       f' -i "{safe_prompt}"')
            try:
                subprocess.Popen(cmd_str, shell=True)
                self._json_response({"status": "ok", "editor": "copilot", "mode": "windows",
                                     "copilotMode": copilot_mode, "model": copilot_model})
            except OSError as exc:
                self._json_response({"error": f"Failed to launch Copilot: {exc}"}, 500)
        else:
            try:
                subprocess.Popen(
                    [copilot_path] + copilot_args,
                    cwd=work_dir, start_new_session=True
                )
                self._json_response({"status": "ok", "editor": "copilot", "mode": "native",
                                     "copilotMode": copilot_mode, "model": copilot_model})
            except OSError as exc:
                self._json_response({"error": f"Failed to launch Copilot: {exc}"}, 500)

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
    parser.add_argument("--repos", help="Directory containing repos to scan")
    parser.add_argument("--out", default="output", help="Output directory name (default: output)")
    parser.add_argument("--port", type=int, default=8020, help="Web server port (default: 8020)")
    parser.add_argument("--level", choices=["critical", "high", "medium", "low"], default="high",
                        help="Minimum severity level for smell scanner (default: high)")
    parser.add_argument("--serve-only", action="store_true",
                        help="Skip pipeline, just start the web server on existing output")
    parser.add_argument("--tools", default="none",
                        help="External tools: semgrep,bandit,detect-secrets,radon,all,none (default: none)")
    parser.add_argument("--integrations", default="none",
                        help="Security platforms: armorcode,sonarqube,all,none (default: none)")
    args = parser.parse_args()

    if not args.serve_only and not args.repos:
        parser.error("--repos is required unless --serve-only is used")

    repos = args.repos or ""
    out = args.out
    port = args.port
    level = args.level

    os.makedirs(out, exist_ok=True)

    if args.serve_only:
        print(f"=== Serve-only: {out} on port {port} ===\n")
    else:
        print(f"=== Pipeline: {repos} → {out} ===\n")

    if not args.serve_only:
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

        # Resilience analysis (needs data-sources.json, dependencies.csv from step 1)
        print("\n--- Scanning resilience ---")
        run("6_scan_resilience.py", repos, out)

        # Step 5: External tools (optional, off by default)
        if args.tools and args.tools.lower() != "none":
            print("\n--- External tools ---")
            run("3_external_tools.py", repos, out, "--tools", args.tools)

        # Step 6: Security integrations (optional, off by default)
        if args.integrations and args.integrations.lower() != "none":
            print("\n--- Security integrations ---")
            integration_args = [out, "--platforms", args.integrations]
            # If external tools ran, also export those findings to platforms
            if args.tools and args.tools.lower() != "none":
                integration_args.extend(["--export", "external-tools.json"])
            run("6_security_integrations.py", *integration_args)

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
        run("4_gen_diagrams.py", out)

        # Step 4 needs all outputs
        print("\n--- Step 4: Generating docs + viewer ---")
        run("5_gen_docs.py", out)

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
    print(f"    Stop server: visit http://localhost:{port}/_stop")
    print(f"    Or press Ctrl+C\n")

    os.chdir(out)
    server = http.server.HTTPServer(("", port), ViewerHandler)
    ViewerHandler._server_ref = server

    import signal
    def _shutdown_handler(sig, frame):
        print("\nServer stopped.")
        threading.Thread(target=server.shutdown, daemon=True).start()
    signal.signal(signal.SIGINT, _shutdown_handler)
    if hasattr(signal, "SIGBREAK"):          # Windows Ctrl+Break
        signal.signal(signal.SIGBREAK, _shutdown_handler)

    server.serve_forever()


if __name__ == "__main__":
    main()
