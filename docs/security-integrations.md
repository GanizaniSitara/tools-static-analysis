# Security Platform Integrations -- Setup and Testing Guide

This document covers how to stand up, configure, and test the ArmorCode and
SonarQube integrations that ship with the static analysis pipeline.

Both integrations work in **demo mode** out of the box (no credentials needed).
Demo mode returns realistic mock findings so you can exercise the full pipeline
without any external services running. The sections below explain what is
needed to connect to a real instance of each platform.

---

## Table of Contents

1. [Quick Start (Demo Mode)](#1-quick-start-demo-mode)
2. [SonarQube Setup](#2-sonarqube-setup)
3. [ArmorCode Setup](#3-armorcode-setup)
4. [Configuration File](#4-configuration-file)
5. [Running the Integration](#5-running-the-integration)
6. [Testing](#6-testing)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Quick Start (Demo Mode)

No setup required. Run the integration script with no config and both
platforms produce demo findings:

```bash
python3 6_security_integrations.py output-myproject --platforms all
```

Output: `output-myproject/security-integrations.json` with 10 ArmorCode
findings and 12 SonarQube findings across SAST, SCA, DAST, secrets, IaC,
quality, and compliance categories.

To run demo mode for a single platform:

```bash
python3 6_security_integrations.py output-myproject --platforms sonarqube
python3 6_security_integrations.py output-myproject --platforms armorcode
```

---

## 2. SonarQube Setup

SonarQube Community Edition is free and open source. You can run it locally
in under 5 minutes.

### 2.1 Start SonarQube with Docker

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -v sonarqube_data:/opt/sonarqube/data \
  -v sonarqube_logs:/opt/sonarqube/logs \
  sonarqube:community
```

Wait about 60 seconds for startup, then open http://localhost:9000 in your
browser. Default credentials: `admin` / `admin` (you will be asked to change
the password on first login).

### 2.2 Generate an API Token

1. Log in to SonarQube at http://localhost:9000
2. Click your avatar (top right) > **My Account**
3. Go to the **Security** tab
4. Under **Generate Tokens**, enter a name (e.g. `static-analysis`) and
   select type **User Token**
5. Click **Generate** and copy the token (starts with `squ_`)

### 2.3 Create a Project and Run a Scan

SonarQube needs at least one scan before the import API returns findings.

**Option A -- SonarScanner CLI (recommended for .NET):**

```bash
# Install the .NET SonarScanner globally
dotnet tool install --global dotnet-sonarscanner

# Begin analysis
dotnet sonarscanner begin \
  /k:"my-project-key" \
  /d:sonar.host.url="http://localhost:9000" \
  /d:sonar.token="squ_YOUR_TOKEN_HERE"

# Build
dotnet build

# End analysis (uploads results)
dotnet sonarscanner end /d:sonar.token="squ_YOUR_TOKEN_HERE"
```

**Option B -- Manual project creation (for testing the import without a real scan):**

1. In the SonarQube UI, click **Projects > Create Project > Manually**
2. Enter a project key (e.g. `my-project`) and display name
3. The project will be empty until you run a scan, but the API endpoints
   will respond

### 2.4 Configure the Adapter

Edit `config.yaml` (copy from `config.example.yaml` if you have not already):

```yaml
integrations:
  sonarqube:
    api_url: "http://localhost:9000"
    api_token: "squ_YOUR_TOKEN_HERE"
    project_key: "my-project-key"
```

### 2.5 What the Adapter Does

| Operation         | API Endpoint                              | Description                            |
|-------------------|-------------------------------------------|----------------------------------------|
| test_connection   | `GET /api/system/status`                  | Checks server is UP                    |
| import_findings   | `GET /api/issues/search`                  | Pulls open issues (paginated, max 500) |
| quality gate      | `GET /api/qualitygates/project_status`    | Fetches pass/fail gate status          |
| measures          | `GET /api/measures/component`             | Fetches ncloc, bugs, coverage, etc.    |
| export_findings   | N/A (generates Generic Issue JSON file)   | For `sonar.externalIssuesReportPaths`  |

The **export** path does not call SonarQube directly. Instead, it produces a
JSON file in the SonarQube Generic Issue Import format. You feed this to the
scanner via `sonar.externalIssuesReportPaths=path/to/report.json`.

---

## 3. ArmorCode Setup

ArmorCode is a commercial ASPM (Application Security Posture Management)
platform. There is no free tier, no self-hosted option, and no public trial.
You need an active ArmorCode subscription to use live mode.

### 3.1 Prerequisites

- An active ArmorCode account at https://app.armorcode.com
- An API key generated from the ArmorCode platform

### 3.2 Generate an API Key

1. Log in to https://app.armorcode.com
2. Navigate to **Settings > API Keys** (or see ArmorCode support article:
   https://support.armorcode.com/hc/en-us/articles/19447589108499)
3. Click **Generate API Key**
4. Copy the key

### 3.3 Configure the Adapter

```yaml
integrations:
  armorcode:
    api_token: "YOUR_ARMORCODE_API_KEY"
    # api_url defaults to https://app.armorcode.com/api
    # Override only if you have an on-prem or custom deployment:
    # api_url: "https://custom.armorcode.com/api"
    # Optionally scope findings to a specific product:
    # product: "my-product-name"
```

Only `api_token` is required. The base URL defaults to
`https://app.armorcode.com/api`.

### 3.4 What the Adapter Does

| Operation           | API Endpoint              | Description                              |
|---------------------|---------------------------|------------------------------------------|
| test_connection     | `GET /products?size=1`    | Verifies API key works                   |
| import_findings     | `GET /user/findings/`     | Pulls findings (paginated, max 500)      |
| export_findings     | `POST /user/findings/`    | Pushes local findings to ArmorCode       |
| get_alerts          | `GET /alerts`             | Fetches aggregated alerts                |
| get_products        | `GET /products`           | Lists configured products                |
| get_security_tools  | `GET /securityTools`      | Lists connected security tools           |

Authentication uses the `Token` header scheme:
`Authorization: Token <api_key>`

The adapter follows the same API contract as the official ArmorCode Python SDK:
https://github.com/armor-code/acsdk

### 3.5 If You Do Not Have an ArmorCode Account

Use **demo mode**. The adapter returns 10 realistic findings across these
categories:

- SAST (2): SQL injection, XSS
- SCA (2): vulnerable NuGet dependencies
- Secrets (1): hardcoded connection string
- DAST (2): missing CSP header, server version disclosure
- IaC (1): container running as root
- Risk (1): elevated component risk score
- Compliance (1): PII in logs

This is enough to exercise the full pipeline, generate the viewer, and see
how ArmorCode findings would appear alongside local scan results.

---

## 4. Configuration File

Copy the example config and edit:

```bash
cp config.example.yaml config.yaml
```

The `integrations:` section is the only part relevant to this feature.
`config.yaml` is gitignored, so credentials stay local.

Full example with both platforms configured:

```yaml
integrations:
  armorcode:
    api_token: "ac_live_xxxxxxxxxxxx"
    product: "eShop"
  sonarqube:
    api_url: "http://localhost:9000"
    api_token: "squ_abcdef123456"
    project_key: "eShopOnWeb"
```

If a platform section is missing or has empty credentials, that platform
runs in demo mode automatically.

---

## 5. Running the Integration

### Standalone

```bash
# Both platforms, demo mode (no config needed)
python3 6_security_integrations.py output-myproject --platforms all

# Single platform
python3 6_security_integrations.py output-myproject --platforms sonarqube

# With export: push local findings to platforms
python3 6_security_integrations.py output-myproject --platforms all \
  --export external-tools.json

# Custom config file
python3 6_security_integrations.py output-myproject --platforms all \
  --config /path/to/config.yaml
```

### As Part of the Full Pipeline

If `run.py` supports the `--integrations` flag:

```bash
python3 run.py repos/ output-myproject --integrations all
python3 run.py repos/ output-myproject --integrations armorcode,sonarqube
```

### Output

The script writes `security-integrations.json` to the output directory:

```json
{
  "generated": "2026-03-01T10:00:00",
  "platformsRequested": ["armorcode", "sonarqube"],
  "platformsExecuted": ["armorcode", "sonarqube"],
  "summary": {
    "totalFindings": 22,
    "findingsBySeverity": {"critical": 3, "high": 8, "medium": 7, "low": 4},
    "findingsByTool": {"armorcode": 10, "sonarqube": 12},
    "findingsByCategory": {"security": 13, "quality": 9}
  },
  "platforms": {
    "armorcode": { "...": "per-platform result" },
    "sonarqube": { "...": "per-platform result" }
  }
}
```

---

## 6. Testing

### 6.1 Unit Tests (No External Services Needed)

The test suite covers both demo and live-mode behavior without requiring a
running SonarQube or ArmorCode instance:

```bash
# Run all integration tests
python -m unittest test_integrations -v

# Run a specific test class
python -m unittest test_integrations.TestSonarQubeDemo -v
python -m unittest test_integrations.TestArmorCodeDemo -v
python -m unittest test_integrations.TestCLIIntegration -v
```

What the tests verify:

| Test Class              | What It Checks                                         |
|-------------------------|--------------------------------------------------------|
| TestDiscovery           | All adapters discovered, correct types, config routing  |
| TestBaseNormalization   | Severity string mapping (CRITICAL -> critical, etc.)    |
| TestArmorCodeDemo       | Demo findings: count, fields, severities, categories    |
| TestArmorCodeLive       | Live mode activates, connection fails gracefully        |
| TestSonarQubeDemo       | Demo findings, metrics, quality gate, generic export    |
| TestSonarQubeLive       | Live mode activates, connection fails gracefully        |
| TestCLIIntegration      | End-to-end subprocess: demo, single-platform, export    |

### 6.2 Manual Testing Against a Live SonarQube

This is the most practical way to test real API connectivity since SonarQube
Community Edition is free.

**Step 1: Start SonarQube**

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:community
```

**Step 2: Create a token** (see section 2.2 above)

**Step 3: Run a scan** against one of the test repos (eShop, StockSharp,
or OrchardCore):

```bash
cd /path/to/eShopOnWeb
dotnet sonarscanner begin \
  /k:"eShopOnWeb" \
  /d:sonar.host.url="http://localhost:9000" \
  /d:sonar.token="squ_YOUR_TOKEN"
dotnet build
dotnet sonarscanner end /d:sonar.token="squ_YOUR_TOKEN"
```

**Step 4: Configure and run the integration**

```bash
# In config.yaml
# integrations:
#   sonarqube:
#     api_url: "http://localhost:9000"
#     api_token: "squ_YOUR_TOKEN"
#     project_key: "eShopOnWeb"

python3 6_security_integrations.py output-eshop --platforms sonarqube
```

**Step 5: Verify output**

```bash
python3 -c "
import json
with open('output-eshop/security-integrations.json') as f:
    d = json.load(f)
sq = d['platforms']['sonarqube']
print(f\"Status: {sq['status']}\")
print(f\"Demo: {sq['demo']}\")
print(f\"Findings: {sq['findingCount']}\")
if sq.get('metrics'):
    print(f\"Quality gate: {sq['metrics'].get('qualityGate')}\")
"
```

You should see `demo: false` and real findings from SonarQube.

### 6.3 Manual Testing Against ArmorCode

Without a paid account, you are limited to demo mode. If you do have an
account:

```bash
# config.yaml
# integrations:
#   armorcode:
#     api_token: "your-real-api-key"

python3 6_security_integrations.py output-test --platforms armorcode
```

Check the output:

```bash
python3 -c "
import json
with open('output-test/security-integrations.json') as f:
    d = json.load(f)
ac = d['platforms']['armorcode']
print(f\"Status: {ac['status']}\")
print(f\"Demo: {ac['demo']}\")
print(f\"Findings: {ac['findingCount']}\")
"
```

### 6.4 Testing the Export Path

Export pushes local scan results to platforms. Test it end-to-end:

```bash
# First, run the scan pipeline to produce local findings
python3 1_scan_projects.py repos/eShopOnWeb output-eshop
python3 2_scan_smells.py repos/eShopOnWeb output-eshop

# Then export to platforms (demo mode is fine)
python3 6_security_integrations.py output-eshop --platforms all \
  --export external-tools.json
```

Check that the export block appears in the output:

```bash
python3 -c "
import json
with open('output-eshop/security-integrations.json') as f:
    d = json.load(f)
for name, platform in d['platforms'].items():
    exp = platform.get('export', {})
    print(f\"{name}: exported={exp.get('findingsExported', 0)}, status={exp.get('status', 'n/a')}\")
"
```

### 6.5 Quick Smoke Test (Python REPL)

```python
from integrations import discover_integrations

# Demo mode -- no config
reg = discover_integrations()
for name, adapter in reg.items():
    print(f"{name}: demo={adapter.is_demo}")
    result = adapter.import_findings()
    print(f"  findings: {result['findingCount']}, status: {result['status']}")
```

---

## 7. Troubleshooting

### SonarQube container fails to start

SonarQube needs `vm.max_map_count >= 262144`. On Linux:

```bash
sudo sysctl -w vm.max_map_count=262144
```

### SonarQube returns 401 Unauthorized

- Token may have expired -- generate a new one
- Token type must be **User Token** (not Project Token for some endpoints)
- Check that `api_url` does not have a trailing slash

### ArmorCode connection times out

- Verify your network can reach `https://app.armorcode.com`
- Check that the API key has not been revoked
- The adapter uses a 30-second timeout; corporate proxies may need longer

### "No project_key configured" error from SonarQube import

Set `project_key` in your config:

```yaml
integrations:
  sonarqube:
    api_url: "http://localhost:9000"
    api_token: "squ_xxx"
    project_key: "my-project"    # <-- required for import
```

### Import returns 0 findings from a live SonarQube

- The project may not have been scanned yet -- run `dotnet sonarscanner` first
- Check the issue filter: the adapter only pulls `OPEN`, `CONFIRMED`, and
  `REOPENED` issues
- Verify the project key matches exactly (case-sensitive)

### PyYAML not installed

The config loader needs PyYAML to read `config.yaml`:

```bash
pip install pyyaml
```

Without it, the script falls back to empty config (demo mode for all
platforms).
