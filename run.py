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
        "enableWslTools": False,
        "wslDistro": "Ubuntu",
        "wslPathPrefix": "\\\\wsl$\\Ubuntu",
        "claudeCodeUseWsl": False,
        "claudeCodePath": "claude",
        "micromambaEnv": "",
        "openCodePath": "/usr/local/bin/opencode",
        "githubCopilotEnabled": False
    }
    if not config_path.exists():
        return default
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return {**default, **yaml.safe_load(f)}
    except Exception:
        return default


CONFIG = _load_config()


def _is_wsl() -> bool:
    """Detect if running under Windows Subsystem for Linux."""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except OSError:
        return False


def _windows_to_wsl_path(win_path: str) -> str:
    """Convert C:\\foo\\bar -> /mnt/c/foo/bar using wslpath."""
    try:
        result = subprocess.run(
            ["wsl", "-d", CONFIG["wslDistro"], "wslpath", "-u", win_path],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    # Fallback: manual conversion
    if len(win_path) > 1 and win_path[1] == ':':
        drive = win_path[0].lower()
        rest = win_path[2:].replace('\\', '/')
        return f"/mnt/{drive}{rest}"
    return win_path.replace('\\', '/')


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
        elif editor == "opencode":
            self._open_opencode(file_path, line, project_name, smell_description)
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
        """Open file in VS Code with solution directory as workspace."""
        code_cmd = shutil.which("code")
        if not code_cmd:
            self._json_response({"error": "VS Code (code) not found in PATH"}, 500)
            return

        # Find solution file using existing helper
        sln_path = _find_solution(file_path, self.repo_roots, self.solutions_map)

        cmd = [code_cmd]
        if sln_path:
            # Open solution directory as workspace
            cmd.append(str(Path(sln_path).parent))

        # Navigate to specific file and line
        cmd.extend(["--goto", f"{file_path}:{line or 1}"])

        try:
            subprocess.Popen(cmd, start_new_session=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._json_response({"status": "ok", "editor": "code",
                               "solution": sln_path if sln_path else None})
        except OSError as exc:
            self._json_response({"error": f"Failed to launch VS Code: {exc}"}, 500)

    def _open_claude(self, file_path: str, line: int = None, project_name: str = None,
                     smell_description: str = None):
        """Open Claude Code with context: workspace dir, file:line, and custom prompt.

        Uses claudeCodeUseWsl toggle:
        - false: Run Claude Code natively on Windows (opens new terminal window)
        - true: Run Claude Code via WSL with optional micromamba activation
        """
        # Find solution file using existing helper (handles relative paths correctly)
        sln_path = _find_solution(file_path, self.repo_roots, self.solutions_map)

        # Get solution directory - require valid solution to avoid opening in wrong directory
        if not sln_path:
            self._json_response({"error": "No .sln solution file found for this file"}, 404)
            return

        sln_dir = str(Path(sln_path).parent)

        # Build prompt from config + project + smell
        prompt_parts = [CONFIG["claudePrompt"]]
        if project_name:
            prompt_parts.append(f"\n\nProject: {project_name}")
        if smell_description:
            prompt_parts.append(f"\n\nArchitectural Smell:\n{smell_description}")
        prompt = "".join(prompt_parts)

        # Choose between Windows native or WSL execution
        if CONFIG.get("claudeCodeUseWsl", False):
            # WSL mode with optional micromamba activation
            wsl_file = _windows_to_wsl_path(file_path)
            workspace_dir = _windows_to_wsl_path(sln_dir)

            # Build Claude Code command
            claude_cmd = CONFIG.get("claudeCodePath", "claude")
            claude_args = f"{claude_cmd} --add-dir {shlex.quote(workspace_dir)} @{wsl_file}"
            if line:
                claude_args += f":{line}"
            claude_args += f" --append-system-prompt {shlex.quote(prompt)}"

            # Build WSL command with optional micromamba activation
            micromamba_env = CONFIG.get("micromambaEnv", "")
            if micromamba_env:
                # Activate micromamba environment before running claude
                wsl_cmd = [
                    "wsl", "-d", CONFIG["wslDistro"], "--", "bash", "-c",
                    f'eval "$(micromamba shell hook --shell bash)" && micromamba activate {micromamba_env} && {claude_args}'
                ]
            else:
                # Run without environment activation
                wsl_cmd = [
                    "wsl", "-d", CONFIG["wslDistro"], "--", "bash", "-c",
                    claude_args
                ]

            try:
                subprocess.Popen(wsl_cmd, start_new_session=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                env_info = f" (micromamba: {micromamba_env})" if micromamba_env else " (WSL)"
                self._json_response({"status": "ok", "editor": "claude", "workspace": workspace_dir, "mode": "wsl" + env_info})
            except OSError as exc:
                self._json_response({"error": f"Failed to launch Claude Code via WSL: {exc}"}, 500)
        else:
            # Windows native mode - launch in new terminal window
            workspace_dir = sln_dir

            # Make file path relative to solution directory for Claude
            try:
                rel_file_path = os.path.relpath(file_path, workspace_dir)
            except ValueError:
                # Different drives - use absolute path
                rel_file_path = file_path

            # Build Claude Code command - use relative path from workspace
            claude_args = f'@{rel_file_path}' + (f':{line}' if line else '')
            claude_args += f' --append-system-prompt "{prompt}"'

            # Launch claude in a new command window on Windows
            # This allows the TUI to run in its own terminal
            if sys.platform == "win32":
                # Windows: Use start /d to set working directory
                # This is simpler than cd /d && since start supports /d flag
                cmd_str = f'start "" /d "{workspace_dir}" claude {claude_args}'
                try:
                    subprocess.Popen(cmd_str, shell=True)
                    self._json_response({"status": "ok", "editor": "claude", "workspace": workspace_dir, "mode": "windows"})
                except OSError as exc:
                    self._json_response({"error": f"Failed to launch Claude Code: {exc}"}, 500)
            elif _is_wsl():
                # WSL: Launch Windows claude.exe via cmd.exe
                try:
                    cmd_str = f'cmd.exe /c start "" cmd /k {full_cmd}'
                    subprocess.Popen(cmd_str, shell=True)
                    self._json_response({"status": "ok", "editor": "claude", "workspace": workspace_dir, "mode": "windows-from-wsl"})
                except OSError as exc:
                    self._json_response({"error": f"Failed to launch Claude Code from WSL: {exc}"}, 500)
            else:
                # Native Linux: Claude Code not typically used here, suggest WSL mode
                self._json_response(
                    {"error": "Claude Code Windows mode requires Windows or WSL. Set claudeCodeUseWsl: true in config.yaml to use WSL mode."},
                    501
                )

    def _open_opencode(self, file_path: str, line: int = None, project_name: str = None,
                       smell_description: str = None):
        """Open OpenCode via WSL with context: workspace dir, file:line, and custom prompt."""
        if not CONFIG["enableWslTools"]:
            self._json_response({"error": "WSL tools are disabled in config.json"}, 400)
            return

        # Find solution file using existing helper
        sln_path = _find_solution(file_path, self.repo_roots, self.solutions_map)
        if not sln_path:
            self._json_response({"error": "No .sln solution file found for this file"}, 404)
            return

        sln_dir = str(Path(sln_path).parent)

        # Convert paths to WSL
        wsl_file = _windows_to_wsl_path(file_path)
        workspace_dir = _windows_to_wsl_path(sln_dir)

        # Build prompt
        prompt_parts = [CONFIG["claudePrompt"]]
        if project_name:
            prompt_parts.append(f"\n\nProject: {project_name}")
        if smell_description:
            prompt_parts.append(f"\n\nArchitectural Smell:\n{smell_description}")

        # Execute via WSL
        wsl_cmd = [
            "wsl", "-d", CONFIG["wslDistro"], "--",
            CONFIG["openCodePath"],
            "--add-dir", workspace_dir,
            f"@{wsl_file}" + (f":{line}" if line else ""),
            "--append-system-prompt", "".join(prompt_parts)
        ]

        try:
            subprocess.Popen(wsl_cmd, start_new_session=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._json_response({"status": "ok", "editor": "opencode", "workspace": workspace_dir})
        except OSError as exc:
            self._json_response({"error": f"Failed to launch OpenCode: {exc}"}, 500)

    def _open_github_copilot(self, file_path: str, line: int = None, project_name: str = None,
                             smell_description: str = None):
        """Ask GitHub Copilot for refactoring suggestions via WSL."""
        if not CONFIG["enableWslTools"] or not CONFIG["githubCopilotEnabled"]:
            self._json_response({"error": "GitHub Copilot is disabled in config.json"}, 400)
            return

        wsl_file = _windows_to_wsl_path(file_path)

        # Build context message
        context_parts = [f"I'm looking at file: {wsl_file}"]
        if line:
            context_parts.append(f" (line {line})")
        if project_name:
            context_parts.append(f"\n\nProject: {project_name}")
        if smell_description:
            context_parts.append(f"\n\nArchitectural Smell:\n{smell_description}")
        context_parts.append("\n\nPlease suggest a refactoring to address this issue.")

        wsl_cmd = [
            "wsl", "-d", CONFIG["wslDistro"], "--",
            "gh", "copilot", "suggest",
            "-t", "shell",
            "".join(context_parts)
        ]

        try:
            subprocess.Popen(wsl_cmd, start_new_session=True)
            self._json_response({"status": "ok", "editor": "copilot"})
        except OSError as exc:
            self._json_response({"error": f"Failed to launch GitHub Copilot: {exc}"}, 500)

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
    parser.add_argument("repos", nargs="?", help="Directory containing repos to scan")
    parser.add_argument("out", nargs="?", default="output", help="Output directory name (default: output)")
    parser.add_argument("port", nargs="?", type=int, default=8020, help="Web server port (default: 8020)")
    parser.add_argument("--level", choices=["critical", "high", "medium", "low"], default="high",
                        help="Minimum severity level for smell scanner (default: high)")
    parser.add_argument("--serve-only", action="store_true",
                        help="Skip pipeline, just start the web server on existing output")
    parser.add_argument("--tools", default="none",
                        help="External tools: semgrep,bandit,detect-secrets,radon,all,none (default: none)")
    args = parser.parse_args()

    if not args.serve_only and not args.repos:
        parser.error("repos is required unless --serve-only is used")

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

        # Step 5: External tools (optional, off by default)
        if args.tools and args.tools.lower() != "none":
            print("\n--- External tools ---")
            run("5_external_tools.py", repos, out, "--tools", args.tools)

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
