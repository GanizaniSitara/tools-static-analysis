"""Tests for security platform integrations (ArmorCode, SonarQube)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from integrations import discover_integrations, KNOWN_INTEGRATIONS
from integrations.base import SecurityIntegration
from integrations.armorcode import ArmorCodeIntegration
from integrations.sonarqube import SonarQubeIntegration


# ── Discovery tests ──────────────────────────────────────────────────


class TestDiscovery(unittest.TestCase):
    """Test that integration adapters are discovered and instantiated."""

    def test_discover_returns_all_known(self):
        registry = discover_integrations()
        for name in KNOWN_INTEGRATIONS:
            self.assertIn(name, registry, f"Missing integration: {name}")

    def test_discover_returns_correct_types(self):
        registry = discover_integrations()
        for name, adapter in registry.items():
            self.assertIsInstance(adapter, SecurityIntegration)
            self.assertEqual(adapter.name, name)
            self.assertTrue(adapter.display_name)

    def test_discover_with_config(self):
        config = {
            "armorcode": {"api_url": "https://test.armorcode.ai/api/v1", "api_token": "tok"},
            "sonarqube": {"api_url": "http://localhost:9000", "api_token": "squ_test"},
        }
        registry = discover_integrations(config)
        self.assertFalse(registry["armorcode"].is_demo)
        self.assertFalse(registry["sonarqube"].is_demo)

    def test_discover_without_config_is_demo(self):
        registry = discover_integrations()
        for adapter in registry.values():
            self.assertTrue(adapter.is_demo)


# ── Base class tests ─────────────────────────────────────────────────


class TestBaseNormalization(unittest.TestCase):
    """Test the severity normalization in the base class."""

    def test_severity_mapping(self):
        cases = {
            "CRITICAL": "critical", "crit": "critical", "very-high": "critical",
            "HIGH": "high", "major": "high",
            "MEDIUM": "medium", "moderate": "medium",
            "LOW": "low", "minor": "low", "info": "low",
            "unknown-value": "medium",
        }
        for raw, expected in cases.items():
            self.assertEqual(SecurityIntegration._normalize_severity(raw), expected)


# ── ArmorCode tests ──────────────────────────────────────────────────


class TestArmorCodeDemo(unittest.TestCase):
    """Test ArmorCode adapter in demo mode (no credentials)."""

    def setUp(self):
        self.adapter = ArmorCodeIntegration({})

    def test_is_demo(self):
        self.assertTrue(self.adapter.is_demo)

    def test_connection_reports_demo(self):
        result = self.adapter.test_connection()
        self.assertTrue(result["demo"])
        self.assertFalse(result["connected"])

    def test_import_returns_findings(self):
        result = self.adapter.import_findings()
        self.assertEqual(result["tool"], "armorcode")
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["demo"])
        self.assertGreater(result["findingCount"], 0)
        self.assertEqual(len(result["findings"]), result["findingCount"])

    def test_import_findings_have_required_fields(self):
        result = self.adapter.import_findings()
        required = {"tool", "ruleId", "severity", "category", "message", "file", "line", "context"}
        for finding in result["findings"]:
            for field in required:
                self.assertIn(field, finding, f"Missing field: {field}")

    def test_import_findings_severities_valid(self):
        result = self.adapter.import_findings()
        valid = {"critical", "high", "medium", "low"}
        for finding in result["findings"]:
            self.assertIn(finding["severity"], valid)

    def test_import_has_categories(self):
        result = self.adapter.import_findings()
        self.assertIn("categories", result)
        self.assertGreater(len(result["categories"]), 0)

    def test_export_demo_mode(self):
        findings = [
            {"tool": "test", "ruleId": "T1", "severity": "high",
             "category": "security", "message": "Test", "file": "a.cs", "line": 1, "context": ""},
        ]
        result = self.adapter.export_findings(findings)
        self.assertEqual(result["status"], "demo")
        self.assertEqual(result["platform"], "armorcode")
        self.assertEqual(result["findingsExported"], 1)


class TestArmorCodeLive(unittest.TestCase):
    """Test ArmorCode adapter with credentials (but no real server)."""

    def setUp(self):
        self.adapter = ArmorCodeIntegration({
            "api_url": "https://test.armorcode.ai/api/v1",
            "api_token": "test-token",
        })

    def test_not_demo(self):
        self.assertFalse(self.adapter.is_demo)

    def test_connection_fails_gracefully(self):
        result = self.adapter.test_connection()
        self.assertFalse(result["connected"])
        self.assertFalse(result["demo"])
        self.assertIn("failed", result["message"].lower())


# ── SonarQube tests ──────────────────────────────────────────────────


class TestSonarQubeDemo(unittest.TestCase):
    """Test SonarQube adapter in demo mode (no credentials)."""

    def setUp(self):
        self.adapter = SonarQubeIntegration({})

    def test_is_demo(self):
        self.assertTrue(self.adapter.is_demo)

    def test_connection_reports_demo(self):
        result = self.adapter.test_connection()
        self.assertTrue(result["demo"])
        self.assertFalse(result["connected"])

    def test_import_returns_findings(self):
        result = self.adapter.import_findings()
        self.assertEqual(result["tool"], "sonarqube")
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["demo"])
        self.assertGreater(result["findingCount"], 0)
        self.assertEqual(len(result["findings"]), result["findingCount"])

    def test_import_findings_have_required_fields(self):
        result = self.adapter.import_findings()
        required = {"tool", "ruleId", "severity", "category", "message", "file", "line", "context"}
        for finding in result["findings"]:
            for field in required:
                self.assertIn(field, finding, f"Missing field: {field}")

    def test_import_findings_severities_valid(self):
        result = self.adapter.import_findings()
        valid = {"critical", "high", "medium", "low"}
        for finding in result["findings"]:
            self.assertIn(finding["severity"], valid)

    def test_import_has_metrics(self):
        result = self.adapter.import_findings()
        self.assertIn("metrics", result)
        metrics = result["metrics"]
        self.assertIn("qualityGate", metrics)
        self.assertIn("measures", metrics)

    def test_export_produces_generic_issues(self):
        findings = [
            {"tool": "test", "ruleId": "T1", "severity": "high",
             "category": "security", "message": "Test vuln", "file": "a.cs", "line": 10, "context": ""},
            {"tool": "test", "ruleId": "T2", "severity": "medium",
             "category": "quality", "message": "Test smell", "file": "b.cs", "line": 20, "context": ""},
        ]
        result = self.adapter.export_findings(findings)
        self.assertEqual(result["status"], "demo")
        self.assertEqual(result["findingsExported"], 2)
        # Verify SonarQube generic issue format
        report = result["report"]
        self.assertIn("issues", report)
        self.assertEqual(len(report["issues"]), 2)
        issue = report["issues"][0]
        self.assertIn("engineId", issue)
        self.assertIn("ruleId", issue)
        self.assertIn("severity", issue)
        self.assertIn("type", issue)
        self.assertIn("primaryLocation", issue)
        # Severity mapping
        self.assertEqual(issue["severity"], "MAJOR")  # high -> MAJOR
        self.assertEqual(issue["type"], "VULNERABILITY")  # security -> VULNERABILITY

    def test_quality_gate_demo(self):
        result = self.adapter.get_quality_gate()
        self.assertTrue(result["demo"])
        self.assertIn("metrics", result)


class TestSonarQubeLive(unittest.TestCase):
    """Test SonarQube adapter with credentials (but no real server)."""

    def setUp(self):
        self.adapter = SonarQubeIntegration({
            "api_url": "http://localhost:9999",
            "api_token": "squ_test",
            "project_key": "test-project",
        })

    def test_not_demo(self):
        self.assertFalse(self.adapter.is_demo)

    def test_connection_fails_gracefully(self):
        result = self.adapter.test_connection()
        self.assertFalse(result["connected"])
        self.assertFalse(result["demo"])


# ── CLI integration test ─────────────────────────────────────────────


class TestCLIIntegration(unittest.TestCase):
    """Test 6_security_integrations.py as a subprocess."""

    def test_cli_runs_demo_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPT_DIR, "6_security_integrations.py"),
                 tmpdir, "--platforms", "all"],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

            # Verify output file
            out_file = os.path.join(tmpdir, "security-integrations.json")
            self.assertTrue(os.path.isfile(out_file))

            with open(out_file, "r") as f:
                data = json.load(f)

            self.assertIn("generated", data)
            self.assertIn("platforms", data)
            self.assertIn("summary", data)
            self.assertGreater(data["summary"]["totalFindings"], 0)

            # Both platforms should have run
            for name in KNOWN_INTEGRATIONS:
                self.assertIn(name, data["platforms"])

    def test_cli_no_platforms(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPT_DIR, "6_security_integrations.py"),
                 tmpdir, "--platforms", "none"],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0)

    def test_cli_single_platform(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPT_DIR, "6_security_integrations.py"),
                 tmpdir, "--platforms", "sonarqube"],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0)
            out_file = os.path.join(tmpdir, "security-integrations.json")
            with open(out_file, "r") as f:
                data = json.load(f)
            self.assertIn("sonarqube", data["platforms"])
            self.assertNotIn("armorcode", data["platforms"])

    def test_cli_with_export_no_source(self):
        """Export flag with no source file should not crash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPT_DIR, "6_security_integrations.py"),
                 tmpdir, "--platforms", "all", "--export", "external-tools.json"],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0)

    def test_cli_with_export_source(self):
        """Export local findings to platforms."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock external-tools.json
            mock_data = {
                "generated": "2024-01-01T00:00:00",
                "scanRoot": "/test",
                "tools": {
                    "test-tool": {
                        "findings": [
                            {"tool": "test-tool", "ruleId": "T1", "severity": "high",
                             "category": "security", "message": "Test", "file": "a.cs",
                             "line": 1, "context": "test context"},
                        ]
                    }
                },
            }
            with open(os.path.join(tmpdir, "external-tools.json"), "w") as f:
                json.dump(mock_data, f)

            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPT_DIR, "6_security_integrations.py"),
                 tmpdir, "--platforms", "all", "--export", "external-tools.json"],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

            out_file = os.path.join(tmpdir, "security-integrations.json")
            with open(out_file, "r") as f:
                data = json.load(f)

            # Both platforms should have export results
            for name in KNOWN_INTEGRATIONS:
                self.assertIn("export", data["platforms"][name])
                self.assertGreater(data["platforms"][name]["export"]["findingsExported"], 0)


if __name__ == "__main__":
    unittest.main()
