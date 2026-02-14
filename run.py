#!/usr/bin/env python3
"""Master runner: scans, diagrams, docs, web server."""

import http.server
import os
import subprocess
import sys
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py /path/to/repos [output-name] [port]")
        print()
        print("  /path/to/repos   Directory containing .NET repos to scan")
        print("  output-name      Output directory name (default: output)")
        print("  port             Web server port (default: 8000)")
        sys.exit(1)

    repos = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "output"
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000

    print(f"=== Pipeline: {repos} → {out} ===\n")

    def run(script, *args):
        path = os.path.join(SCRIPT_DIR, script)
        result = subprocess.run([sys.executable, path, *args])
        if result.returncode != 0:
            print(f"ERROR: {script} failed (exit {result.returncode})")
            sys.exit(1)

    # Steps 1 & 2 scan source — run in parallel
    print("--- Step 1+2: Scanning projects and smells (parallel) ---")
    p1 = subprocess.Popen([sys.executable, os.path.join(SCRIPT_DIR, "1_scan_projects.py"), repos, out])
    p2 = subprocess.Popen([sys.executable, os.path.join(SCRIPT_DIR, "2_scan_smells.py"), repos, out])
    rc1 = p1.wait()
    rc2 = p2.wait()
    if rc1 != 0:
        print("ERROR: 1_scan_projects.py failed"); sys.exit(1)
    if rc2 != 0:
        print("ERROR: 2_scan_smells.py failed"); sys.exit(1)

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
