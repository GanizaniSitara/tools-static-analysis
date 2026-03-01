"""SonarQube integration adapter.

SonarQube is an open-source platform for continuous code quality and
security analysis. This adapter supports:

- Importing findings from a SonarQube server via its Web API
- Exporting our scan results for correlation
- Demo mode with realistic mock data when no server is available

The Community Edition is free and can be run locally via Docker:
    docker run -d --name sonarqube -p 9000:9000 sonarqube:community

API reference: https://next.sonarqube.com/sonarqube/web_api
Authentication: Bearer token or basic auth (token as username, empty password).
"""

from __future__ import annotations

import base64
import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from .base import SecurityIntegration

# Demo findings simulating a SonarQube analysis of a .NET codebase
_DEMO_FINDINGS = [
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S3649",
        "severity": "critical",
        "category": "security",
        "message": "SQL injection: sanitize this input before using it in a SQL query",
        "file": "src/DataAccess/QueryBuilder.cs",
        "line": 142,
        "context": "string.Format(\"SELECT * FROM {0} WHERE id = {1}\", table, userId)",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S5131",
        "severity": "high",
        "category": "security",
        "message": "XSS: user-controlled data is used in HTML output without sanitization",
        "file": "src/Web/Controllers/SearchController.cs",
        "line": 87,
        "context": "ViewBag.Query = Request.QueryString[\"q\"]",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S2068",
        "severity": "critical",
        "category": "security",
        "message": "Hard-coded credentials are security-sensitive",
        "file": "src/Infrastructure/ConfigLoader.cs",
        "line": 34,
        "context": "var password = \"admin123\";",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S4423",
        "severity": "high",
        "category": "security",
        "message": "Weak SSL/TLS protocols should not be used",
        "file": "src/Infrastructure/HttpClientFactory.cs",
        "line": 22,
        "context": "ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls;",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S1871",
        "severity": "medium",
        "category": "quality",
        "message": "Duplicated code block — two branches have identical implementations",
        "file": "src/Services/OrderService.cs",
        "line": 95,
        "context": "if/else branches at lines 95-110 and 112-127 are identical",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S3776",
        "severity": "high",
        "category": "quality",
        "message": "Cognitive complexity of method is 42 (max allowed: 15)",
        "file": "src/Core/PaymentProcessor.cs",
        "line": 56,
        "context": "public decimal CalculateTotal(Order order) — deeply nested conditionals",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S1144",
        "severity": "medium",
        "category": "quality",
        "message": "Dead code: remove this unused private method",
        "file": "src/Common/LegacyHelpers.cs",
        "line": 203,
        "context": "private void ObsoleteValidation() — no callers found",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S108",
        "severity": "high",
        "category": "quality",
        "message": "Empty catch block — either handle the exception or add a comment explaining why it is ignored",
        "file": "src/Services/NotificationService.cs",
        "line": 67,
        "context": "catch (Exception) { }",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S4457",
        "severity": "medium",
        "category": "quality",
        "message": "Split this method into two: one handling parameters check and the other async",
        "file": "src/Services/UserService.cs",
        "line": 112,
        "context": "public async Task<User> GetUserAsync(string id) — validation before await",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S2583",
        "severity": "medium",
        "category": "quality",
        "message": "Condition is always true — change this condition so that it does not always evaluate to true",
        "file": "src/Core/ApplicationManager.cs",
        "line": 289,
        "context": "if (result != null) — result is never null at this point",
    },
    {
        "tool": "sonarqube",
        "ruleId": "roslyn:CA1822",
        "severity": "low",
        "category": "quality",
        "message": "Member does not access instance data and can be marked as static",
        "file": "src/Common/StringUtils.cs",
        "line": 45,
        "context": "public string Sanitize(string input) — no instance fields used",
    },
    {
        "tool": "sonarqube",
        "ruleId": "csharpsquid:S927",
        "severity": "low",
        "category": "quality",
        "message": "Parameter name differs from the base class declaration",
        "file": "src/Services/AccountService.cs",
        "line": 78,
        "context": "override void Save(Account acct) — base uses 'entity'",
    },
]

# Demo quality gate / metrics
_DEMO_METRICS = {
    "qualityGate": "ERROR",
    "conditions": [
        {"metric": "new_reliability_rating", "status": "ERROR", "value": "4"},
        {"metric": "new_security_rating", "status": "ERROR", "value": "5"},
        {"metric": "new_maintainability_rating", "status": "OK", "value": "2"},
        {"metric": "new_coverage", "status": "WARN", "value": "42.3"},
        {"metric": "new_duplicated_lines_density", "status": "OK", "value": "3.2"},
    ],
    "measures": {
        "ncloc": 156000,
        "bugs": 23,
        "vulnerabilities": 15,
        "code_smells": 342,
        "coverage": 42.3,
        "duplicated_lines_density": 3.2,
        "reliability_rating": 4,
        "security_rating": 5,
        "sqale_rating": 2,
        "sqale_debt_ratio": 8.4,
    },
}


class SonarQubeIntegration(SecurityIntegration):
    """SonarQube adapter.

    Config keys:
        api_url:      SonarQube server URL (e.g. http://localhost:9000)
        api_token:    User token for authentication
        project_key:  SonarQube project key to query
    """

    name = "sonarqube"
    display_name = "SonarQube"

    def _has_credentials(self) -> bool:
        return bool(self.config.get("api_url") and self.config.get("api_token"))

    def _auth_header(self) -> str:
        """Build Basic auth header from token (token as user, empty password)."""
        token = self.config.get("api_token", "")
        encoded = base64.b64encode(f"{token}:".encode()).decode()
        return f"Basic {encoded}"

    def test_connection(self) -> dict:
        if self._demo_mode:
            return {
                "connected": False,
                "message": "Demo mode — no SonarQube credentials configured",
                "demo": True,
            }
        try:
            req = Request(
                f"{self.config['api_url']}/api/system/status",
                headers={"Authorization": self._auth_header()},
            )
            with urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                status = data.get("status", "unknown")
                version = data.get("version", "unknown")
                if status == "UP":
                    return {
                        "connected": True,
                        "message": f"Connected to SonarQube {version}",
                        "demo": False,
                    }
                return {
                    "connected": False,
                    "message": f"SonarQube status: {status}",
                    "demo": False,
                }
        except (URLError, OSError) as exc:
            return {"connected": False, "message": f"Connection failed: {exc}", "demo": False}

    def export_findings(self, findings: list[dict], metadata: dict | None = None) -> dict:
        """SonarQube doesn't have a direct findings import API.

        Instead, this prepares findings in SonarQube Generic Issue format
        (sonar.externalIssuesReportPaths) that can be passed to the scanner.
        """
        meta = metadata or {}
        generic_issues = []
        for f in findings:
            sev_map = {
                "critical": "CRITICAL", "high": "MAJOR",
                "medium": "MINOR", "low": "INFO",
            }
            type_map = {"security": "VULNERABILITY", "quality": "CODE_SMELL"}
            generic_issues.append({
                "engineId": f.get("tool", "tools-static-analysis"),
                "ruleId": f.get("ruleId", "unknown"),
                "severity": sev_map.get(f.get("severity", "medium"), "MINOR"),
                "type": type_map.get(f.get("category", "quality"), "CODE_SMELL"),
                "primaryLocation": {
                    "message": f.get("message", ""),
                    "filePath": f.get("file", ""),
                    "textRange": {"startLine": f.get("line", 1) or 1},
                },
            })

        report = {"issues": generic_issues}

        if self._demo_mode:
            return {
                "status": "demo",
                "platform": "sonarqube",
                "findingsExported": len(generic_issues),
                "message": (
                    "Demo mode — Generic Issue report prepared. "
                    "To use with SonarQube, save to a JSON file and set "
                    "sonar.externalIssuesReportPaths in your scanner config."
                ),
                "report": report,
            }

        # In live mode, write the report and return its path info
        return {
            "status": "success",
            "platform": "sonarqube",
            "findingsExported": len(generic_issues),
            "message": (
                "Generic Issue report ready. Pass to SonarQube scanner via "
                "sonar.externalIssuesReportPaths property."
            ),
            "report": report,
        }

    def import_findings(self, **kwargs) -> dict:
        """Pull findings from SonarQube via its Web API.

        In demo mode, returns realistic mock findings matching SonarQube
        rule IDs for C# projects.
        """
        project_key = kwargs.get("project_key", self.config.get("project_key", ""))

        if self._demo_mode:
            findings = list(_DEMO_FINDINGS)
            return {
                "tool": "sonarqube",
                "version": "demo",
                "status": "success",
                "demo": True,
                "findingCount": len(findings),
                "findings": findings,
                "truncated": False,
                "metrics": _DEMO_METRICS,
            }

        if not project_key:
            return {
                "tool": "sonarqube",
                "version": "api",
                "status": "error",
                "demo": False,
                "findingCount": 0,
                "findings": [],
                "truncated": False,
                "message": "No project_key configured — set sonarqube.project_key in config",
            }

        # Fetch issues via Web API
        findings = []
        page = 1
        while True:
            url = (
                f"{self.config['api_url']}/api/issues/search"
                f"?componentKeys={project_key}"
                f"&statuses=OPEN,CONFIRMED,REOPENED"
                f"&ps=100&p={page}"
            )
            req = Request(url, headers={"Authorization": self._auth_header()})
            try:
                with urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read())
            except (URLError, OSError, json.JSONDecodeError) as exc:
                return {
                    "tool": "sonarqube",
                    "version": "api",
                    "status": "error",
                    "demo": False,
                    "findingCount": len(findings),
                    "findings": findings[:500],
                    "truncated": False,
                    "message": f"API error on page {page}: {exc}",
                }

            for issue in data.get("issues", []):
                findings.append(self._transform_issue(issue))

            total = data.get("total", 0)
            if page * 100 >= total or page >= 5:
                break
            page += 1

        # Fetch quality gate status
        metrics = self._fetch_quality_gate(project_key)

        return {
            "tool": "sonarqube",
            "version": "api",
            "status": "success",
            "demo": False,
            "findingCount": len(findings),
            "findings": findings[:500],
            "truncated": len(findings) > 500,
            "metrics": metrics,
        }

    def get_quality_gate(self, project_key: str | None = None) -> dict:
        """Fetch the quality gate status for a project."""
        pk = project_key or self.config.get("project_key", "")
        if self._demo_mode:
            return {"status": "demo", "demo": True, "metrics": _DEMO_METRICS}
        return {"status": "success", "demo": False, "metrics": self._fetch_quality_gate(pk)}

    # -- internal helpers --

    def _fetch_quality_gate(self, project_key: str) -> dict:
        """Fetch quality gate + measures from the SonarQube API."""
        if not project_key:
            return {}
        try:
            # Quality gate status
            url = f"{self.config['api_url']}/api/qualitygates/project_status?projectKey={project_key}"
            req = Request(url, headers={"Authorization": self._auth_header()})
            with urlopen(req, timeout=15) as resp:
                qg_data = json.loads(resp.read())

            # Key measures
            metrics_list = "ncloc,bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density"
            url = (
                f"{self.config['api_url']}/api/measures/component"
                f"?component={project_key}&metricKeys={metrics_list}"
            )
            req = Request(url, headers={"Authorization": self._auth_header()})
            with urlopen(req, timeout=15) as resp:
                measures_data = json.loads(resp.read())

            measures = {}
            for m in measures_data.get("component", {}).get("measures", []):
                measures[m["metric"]] = m.get("value", "")

            return {
                "qualityGate": qg_data.get("projectStatus", {}).get("status", "UNKNOWN"),
                "conditions": qg_data.get("projectStatus", {}).get("conditions", []),
                "measures": measures,
            }
        except (URLError, OSError, json.JSONDecodeError):
            return {}

    def _transform_issue(self, issue: dict) -> dict:
        """Transform a SonarQube issue to our normalized format."""
        sev_map = {
            "BLOCKER": "critical", "CRITICAL": "critical",
            "MAJOR": "high", "MINOR": "medium", "INFO": "low",
        }
        type_map = {
            "VULNERABILITY": "security", "SECURITY_HOTSPOT": "security",
            "BUG": "quality", "CODE_SMELL": "quality",
        }
        component = issue.get("component", "")
        # Strip project prefix from component path
        file_path = component.split(":", 1)[-1] if ":" in component else component

        return {
            "tool": "sonarqube",
            "ruleId": issue.get("rule", ""),
            "severity": sev_map.get(issue.get("severity", "MINOR"), "medium"),
            "category": type_map.get(issue.get("type", "CODE_SMELL"), "quality"),
            "message": issue.get("message", ""),
            "file": file_path,
            "line": issue.get("line", 0),
            "context": issue.get("message", "")[:200],
        }
