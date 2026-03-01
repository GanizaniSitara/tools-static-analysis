"""ArmorCode ASPM integration adapter.

ArmorCode is an Application Security Posture Management platform that
aggregates findings from multiple security tools. This adapter supports:

- Exporting local scan findings to ArmorCode via its REST API
- Importing aggregated findings from ArmorCode
- Demo mode with realistic mock data when no API credentials are available

API reference: ArmorCode uses a REST API with Bearer token authentication.
Base URL pattern: https://<tenant>.armorcode.ai/api/v1/
"""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen

from .base import SecurityIntegration

# Demo findings simulating what ArmorCode would aggregate from multiple tools
_DEMO_FINDINGS = [
    {
        "tool": "armorcode",
        "ruleId": "AC-SAST-001",
        "severity": "critical",
        "category": "security",
        "message": "SQL Injection vulnerability in data access layer — parameterize queries",
        "file": "src/DataAccess/QueryBuilder.cs",
        "line": 142,
        "context": "string.Format(\"SELECT * FROM {0} WHERE id = {1}\", table, userId)",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-SAST-002",
        "severity": "high",
        "category": "security",
        "message": "Cross-site scripting (XSS) — user input rendered without encoding",
        "file": "src/Web/Controllers/SearchController.cs",
        "line": 87,
        "context": "ViewBag.Query = Request.QueryString[\"q\"]",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-SCA-001",
        "severity": "critical",
        "category": "security",
        "message": "Known vulnerable dependency: Newtonsoft.Json < 13.0.1 (CVE-2024-21907)",
        "file": "src/Core/Core.csproj",
        "line": 18,
        "context": "PackageReference Include=\"Newtonsoft.Json\" Version=\"12.0.3\"",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-SCA-002",
        "severity": "high",
        "category": "security",
        "message": "Outdated dependency with known vulnerabilities: System.Text.Json < 8.0.5",
        "file": "src/Api/Api.csproj",
        "line": 22,
        "context": "PackageReference Include=\"System.Text.Json\" Version=\"7.0.0\"",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-SECRET-001",
        "severity": "critical",
        "category": "security",
        "message": "Hardcoded connection string with embedded credentials",
        "file": "src/Infrastructure/appsettings.json",
        "line": 5,
        "context": "\"ConnectionString\": \"Server=prod;User Id=sa;Password=...\"",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-DAST-001",
        "severity": "high",
        "category": "security",
        "message": "Missing Content-Security-Policy header on API responses",
        "file": "src/Web/Startup.cs",
        "line": 0,
        "context": "Response headers missing CSP directive",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-DAST-002",
        "severity": "medium",
        "category": "security",
        "message": "Server version disclosed in HTTP headers (X-Powered-By)",
        "file": "src/Web/Startup.cs",
        "line": 0,
        "context": "X-Powered-By: ASP.NET header present",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-IAC-001",
        "severity": "high",
        "category": "security",
        "message": "Container running as root — specify non-root USER in Dockerfile",
        "file": "Dockerfile",
        "line": 1,
        "context": "FROM mcr.microsoft.com/dotnet/aspnet:8.0 (no USER directive)",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-RISK-001",
        "severity": "medium",
        "category": "security",
        "message": "Component risk score elevated — 3 critical findings in authentication module",
        "file": "src/Auth/AuthService.cs",
        "line": 0,
        "context": "ArmorCode risk aggregation: auth module flagged",
    },
    {
        "tool": "armorcode",
        "ruleId": "AC-COMPLIANCE-001",
        "severity": "medium",
        "category": "security",
        "message": "Logging sensitive data — PII fields written to application logs",
        "file": "src/Services/UserService.cs",
        "line": 203,
        "context": "logger.LogInformation($\"User login: {user.Email}, {user.SSN}\")",
    },
]


class ArmorCodeIntegration(SecurityIntegration):
    """ArmorCode ASPM adapter.

    Config keys:
        api_url:   ArmorCode tenant API URL (e.g. https://acme.armorcode.ai/api/v1)
        api_token: Bearer token for authentication
        product:   ArmorCode product name to scope findings
    """

    name = "armorcode"
    display_name = "ArmorCode"

    def _has_credentials(self) -> bool:
        return bool(self.config.get("api_url") and self.config.get("api_token"))

    def test_connection(self) -> dict:
        if self._demo_mode:
            return {
                "connected": False,
                "message": "Demo mode — no ArmorCode API credentials configured",
                "demo": True,
            }
        try:
            req = Request(
                f"{self.config['api_url']}/health",
                headers={"Authorization": f"Bearer {self.config['api_token']}"},
            )
            with urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return {"connected": True, "message": "Connected to ArmorCode", "demo": False}
                return {
                    "connected": False,
                    "message": f"ArmorCode responded with status {resp.status}",
                    "demo": False,
                }
        except (URLError, OSError) as exc:
            return {"connected": False, "message": f"Connection failed: {exc}", "demo": False}

    def export_findings(self, findings: list[dict], metadata: dict | None = None) -> dict:
        """Push findings to ArmorCode.

        In demo mode, simulates a successful export and returns what
        the API response would look like.
        """
        meta = metadata or {}
        payload = {
            "source": "tools-static-analysis",
            "scanDate": meta.get("generated", self._timestamp()),
            "scanRoot": meta.get("scanRoot", ""),
            "findings": self._transform_for_export(findings),
        }

        if self._demo_mode:
            return {
                "status": "demo",
                "platform": "armorcode",
                "findingsExported": len(findings),
                "message": "Demo mode — findings prepared but not sent (no API credentials)",
                "payload_preview": {
                    "source": payload["source"],
                    "findingCount": len(payload["findings"]),
                    "severityBreakdown": self._severity_breakdown(findings),
                },
            }

        # Live API call
        req = Request(
            f"{self.config['api_url']}/findings/import",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config['api_token']}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read())
                return {
                    "status": "success",
                    "platform": "armorcode",
                    "findingsExported": len(findings),
                    "response": body,
                }
        except (URLError, OSError, json.JSONDecodeError) as exc:
            return {
                "status": "error",
                "platform": "armorcode",
                "findingsExported": 0,
                "message": f"Export failed: {exc}",
            }

    def import_findings(self, **kwargs) -> dict:
        """Pull findings from ArmorCode.

        In demo mode, returns realistic mock findings covering SAST, SCA,
        DAST, secrets, IaC, and risk aggregation categories.
        """
        product = kwargs.get("product", self.config.get("product", ""))

        if self._demo_mode:
            findings = list(_DEMO_FINDINGS)
            return {
                "tool": "armorcode",
                "version": "demo",
                "status": "success",
                "demo": True,
                "findingCount": len(findings),
                "findings": findings,
                "truncated": False,
                "categories": {
                    "SAST": 2, "SCA": 2, "DAST": 2,
                    "Secrets": 1, "IaC": 1, "Risk": 1, "Compliance": 1,
                },
            }

        # Live API call
        url = f"{self.config['api_url']}/findings"
        if product:
            url += f"?product={product}"
        req = Request(
            url,
            headers={"Authorization": f"Bearer {self.config['api_token']}"},
        )
        try:
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            findings = self._transform_from_import(data)
            return {
                "tool": "armorcode",
                "version": "api",
                "status": "success",
                "demo": False,
                "findingCount": len(findings),
                "findings": findings[:500],
                "truncated": len(findings) > 500,
            }
        except (URLError, OSError, json.JSONDecodeError) as exc:
            return {
                "tool": "armorcode",
                "version": "api",
                "status": "error",
                "demo": False,
                "findingCount": 0,
                "findings": [],
                "truncated": False,
                "message": f"Import failed: {exc}",
            }

    # -- internal helpers --

    def _transform_for_export(self, findings: list[dict]) -> list[dict]:
        """Transform our normalized findings to ArmorCode import format."""
        out = []
        for f in findings:
            out.append({
                "title": f.get("message", ""),
                "severity": f.get("severity", "medium").upper(),
                "category": f.get("category", "security"),
                "source_tool": f.get("tool", "unknown"),
                "rule_id": f.get("ruleId", ""),
                "file_path": f.get("file", ""),
                "line_number": f.get("line", 0),
                "code_snippet": f.get("context", ""),
            })
        return out

    def _transform_from_import(self, data: dict) -> list[dict]:
        """Transform ArmorCode API response to our normalized format."""
        findings = []
        for item in data.get("findings", data.get("results", [])):
            findings.append({
                "tool": "armorcode",
                "ruleId": item.get("rule_id", item.get("id", "")),
                "severity": self._normalize_severity(
                    item.get("severity", "medium")
                ),
                "category": item.get("category", "security"),
                "message": item.get("title", item.get("description", "")),
                "file": item.get("file_path", item.get("location", "")),
                "line": item.get("line_number", 0),
                "context": item.get("code_snippet", "")[:200],
            })
        return findings

    @staticmethod
    def _severity_breakdown(findings: list[dict]) -> dict:
        counts: dict[str, int] = {}
        for f in findings:
            sev = f.get("severity", "unknown")
            counts[sev] = counts.get(sev, 0) + 1
        return counts
