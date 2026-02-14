#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ $# -lt 1 ]; then
  echo "Usage: ./run.sh /path/to/repos [output-name] [port]"
  echo ""
  echo "  /path/to/repos   Directory containing .NET repos to scan"
  echo "  output-name      Output directory name (default: output)"
  echo "  port             Web server port (default: 8000)"
  exit 1
fi

REPOS="$1"
OUT="${2:-output}"
PORT="${3:-8000}"

echo "=== Pipeline: $REPOS → $OUT ==="
echo ""

# Steps 1 & 2 scan source — run in parallel
echo "--- Step 1+2: Scanning projects and smells (parallel) ---"
python3 "$SCRIPT_DIR/1_scan_projects.py" "$REPOS" "$OUT" &
PID1=$!
python3 "$SCRIPT_DIR/2_scan_smells.py" "$REPOS" "$OUT" &
PID2=$!
wait $PID1 || { echo "ERROR: 1_scan_projects.py failed"; exit 1; }
wait $PID2 || { echo "ERROR: 2_scan_smells.py failed"; exit 1; }

# Step 3 needs graph.json from step 1
echo ""
echo "--- Step 3: Generating diagrams ---"
python3 "$SCRIPT_DIR/3_gen_diagrams.py" "$OUT"

# Step 4 needs all outputs
echo ""
echo "--- Step 4: Generating docs + viewer ---"
python3 "$SCRIPT_DIR/4_gen_docs.py" "$OUT"

echo ""
echo "=== Done. Opening viewer at http://localhost:$PORT/viewer.html ==="
echo ""

cd "$OUT"
python3 -m http.server "$PORT"
