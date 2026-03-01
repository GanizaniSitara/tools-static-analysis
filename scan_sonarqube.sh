#!/usr/bin/env bash
# ============================================================================
# scan_sonarqube.sh - Run SonarQube analysis on a .NET solution
# ============================================================================
# Prerequisites:
#   1. SonarQube running:  docker run -d --name sonarqube -p 9000:9000 sonarqube:community
#   2. dotnet-sonarscanner: dotnet tool install --global dotnet-sonarscanner
#   3. Java 17+:           apt install openjdk-17-jre  (scanner needs it)
#
# Usage:
#   ./scan_sonarqube.sh <solution-path> <project-key> [output-dir]
#
# Examples:
#   ./scan_sonarqube.sh /repos/eShop eShop
#   ./scan_sonarqube.sh /repos/StockSharp StockSharp output-stocksharp
#   ./scan_sonarqube.sh /repos/OrchardCore OrchardCore output-orchard
# ============================================================================

set -euo pipefail

SONAR_URL="http://localhost:9000"
SONAR_TOKEN="sqa_bc81e73194e5b2e8c2fbd12a7639dc5941c21595"

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
if [ $# -lt 2 ]; then
    echo "Usage: $0 <solution-path> <project-key> [output-dir]"
    echo ""
    echo "  solution-path  Path to .NET solution directory (contains .sln)"
    echo "  project-key    SonarQube project key (e.g. eShop, StockSharp)"
    echo "  output-dir     Pipeline output directory (default: output-<project-key>)"
    exit 1
fi

SOLUTION_PATH="$(cd "$1" && pwd)"
PROJECT_KEY="$2"
OUTPUT_DIR="${3:-output-${PROJECT_KEY}}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---------------------------------------------------------------------------
# Validate environment
# ---------------------------------------------------------------------------
echo "=== SonarQube Scanner ==="
echo "  Solution:    $SOLUTION_PATH"
echo "  Project key: $PROJECT_KEY"
echo "  Server:      $SONAR_URL"
echo "  Output:      $OUTPUT_DIR"
echo ""

# Check SonarQube is reachable
if ! curl -sf "${SONAR_URL}/api/system/status" > /dev/null 2>&1; then
    echo "ERROR: SonarQube not reachable at ${SONAR_URL}"
    echo "Start it with: docker run -d --name sonarqube -p 9000:9000 sonarqube:community"
    exit 1
fi
echo "  SonarQube is running."

# Check dotnet-sonarscanner is installed
if ! command -v dotnet-sonarscanner &> /dev/null; then
    echo "ERROR: dotnet-sonarscanner not found."
    echo "Install: dotnet tool install --global dotnet-sonarscanner"
    exit 1
fi

# Find .sln file
SLN_FILE="$(find "$SOLUTION_PATH" -maxdepth 2 -name '*.sln' -print -quit)"
if [ -z "$SLN_FILE" ]; then
    echo "ERROR: No .sln file found in $SOLUTION_PATH"
    exit 1
fi
echo "  Solution:    $SLN_FILE"
echo ""

# ---------------------------------------------------------------------------
# Step 1: Begin SonarQube analysis
# ---------------------------------------------------------------------------
echo "--- Step 1/3: Begin SonarScanner ---"
dotnet-sonarscanner begin \
    /k:"${PROJECT_KEY}" \
    /d:sonar.host.url="${SONAR_URL}" \
    /d:sonar.token="${SONAR_TOKEN}" \
    /d:sonar.cs.opencover.reportsPaths="**/coverage.opencover.xml" \
    /d:sonar.exclusions="**/obj/**,**/bin/**,**/node_modules/**,**/wwwroot/lib/**"

# ---------------------------------------------------------------------------
# Step 2: Build the solution
# ---------------------------------------------------------------------------
echo ""
echo "--- Step 2/3: Build solution ---"
dotnet build "$SLN_FILE" --no-incremental

# ---------------------------------------------------------------------------
# Step 3: End analysis (uploads results to SonarQube)
# ---------------------------------------------------------------------------
echo ""
echo "--- Step 3/3: End SonarScanner (uploading results) ---"
dotnet-sonarscanner end /d:sonar.token="${SONAR_TOKEN}"

# ---------------------------------------------------------------------------
# Wait for SonarQube to process
# ---------------------------------------------------------------------------
echo ""
echo "--- Waiting for SonarQube to finish processing ---"
for i in $(seq 1 30); do
    STATUS=$(curl -sf -u "${SONAR_TOKEN}:" \
        "${SONAR_URL}/api/ce/activity?component=${PROJECT_KEY}&ps=1" \
        | python3 -c "import sys,json; tasks=json.load(sys.stdin).get('tasks',[]); print(tasks[0]['status'] if tasks else 'PENDING')" 2>/dev/null || echo "PENDING")

    if [ "$STATUS" = "SUCCESS" ]; then
        echo "  Analysis complete."
        break
    elif [ "$STATUS" = "FAILED" ]; then
        echo "  WARNING: SonarQube analysis task failed. Results may be incomplete."
        break
    else
        printf "  Waiting... (%s) [%d/30]\r" "$STATUS" "$i"
        sleep 2
    fi
done
echo ""

# ---------------------------------------------------------------------------
# Step 4: Pull results into the pipeline
# ---------------------------------------------------------------------------
echo "--- Pulling results into pipeline ---"

# Write a temporary config with the SonarQube credentials
TEMP_CONFIG=$(mktemp /tmp/sonar-config-XXXXXX.yaml)
cat > "$TEMP_CONFIG" <<YAML
integrations:
  sonarqube:
    api_url: "${SONAR_URL}"
    api_token: "${SONAR_TOKEN}"
    project_key: "${PROJECT_KEY}"
YAML

mkdir -p "$OUTPUT_DIR"

python3 "${SCRIPT_DIR}/6_security_integrations.py" "$OUTPUT_DIR" \
    --platforms sonarqube \
    --config "$TEMP_CONFIG"

rm -f "$TEMP_CONFIG"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "=== Done ==="
echo "  SonarQube dashboard: ${SONAR_URL}/dashboard?id=${PROJECT_KEY}"
echo "  Pipeline results:    ${OUTPUT_DIR}/security-integrations.json"

if [ -f "${OUTPUT_DIR}/security-integrations.json" ]; then
    TOTAL=$(python3 -c "
import json
with open('${OUTPUT_DIR}/security-integrations.json') as f:
    data = json.load(f)
print(data.get('summary', {}).get('totalFindings', 0))
" 2>/dev/null || echo "?")
    echo "  Total findings:      ${TOTAL}"
fi
