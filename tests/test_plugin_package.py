"""Distribution contracts shared by the Codex and Claude Code packages."""

import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "diffusion-studio"


def read_json(path):
    return json.loads(path.read_text())


def load_doctor(plugin):
    spec = importlib.util.spec_from_file_location(
        "diffusion_doctor", plugin / "scripts" / "doctor.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackageTests(unittest.TestCase):
    def test_both_marketplaces_resolve_the_same_contained_package(self):
        claude = read_json(ROOT / ".claude-plugin" / "marketplace.json")
        codex = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        self.assertEqual(claude["name"], codex["name"])
        for catalog, source in [
            (claude, claude["plugins"][0]["source"]),
            (codex, codex["plugins"][0]["source"]["path"]),
        ]:
            self.assertEqual(catalog["plugins"][0]["name"], "diffusion-studio")
            self.assertTrue(source.startswith("./"))
            resolved = (ROOT / source).resolve()
            self.assertTrue(resolved.is_relative_to(ROOT))
            self.assertEqual(resolved, PLUGIN)

    def test_client_manifests_have_one_release_identity(self):
        manifests = [
            read_json(PLUGIN / "plugin.json"),
            read_json(PLUGIN / ".codex-plugin" / "plugin.json"),
            read_json(PLUGIN / ".claude-plugin" / "plugin.json"),
        ]
        self.assertEqual({item["name"] for item in manifests}, {"diffusion-studio"})
        versions = {item["version"] for item in manifests}
        self.assertEqual(len(versions), 1)
        version = versions.pop()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertIn("## " + version + " ", (ROOT / "CHANGELOG.md").read_text())

    def test_portable_and_client_mcp_endpoints_match(self):
        portable = read_json(PLUGIN / "mcp.json")["mcpServers"]["diffusion-studio"]
        client = read_json(PLUGIN / ".mcp.json")["mcpServers"]["diffusion-studio"]
        self.assertEqual(portable["type"], "streamable-http")
        self.assertEqual(client["type"], "http")
        self.assertEqual(portable["url"], client["url"])
        self.assertEqual(client["url"], "http://127.0.0.1:3274/mcp")

    def test_copied_package_diagnostic_resolves_its_own_config(self):
        # Marketplace installers copy only this directory, not the repository.
        with tempfile.TemporaryDirectory(prefix="diffusion package ") as temp:
            copied = Path(temp) / "plugin"
            shutil.copytree(PLUGIN, copied)
            doctor = load_doctor(copied)
            with mock.patch.object(doctor.shutil, "which", return_value=None), \
                    mock.patch.object(doctor, "MCPClient") as factory:
                client = factory.return_value
                client.initialize.return_value = {
                    "serverInfo": {"name": "diffusion", "version": "test"}
                }
                client.send.side_effect = [
                    {"tools": [{"name": name} for name in
                               ("open", "context", "capture", "check", "export")]},
                    {"content": [{"type": "text", "text": "{}"}]},
                ]
                report = doctor.diagnose()
                self.assertTrue(report["mcpReady"])
                factory.assert_called_once_with("http://127.0.0.1:3274/mcp")
                client.send.assert_any_call(
                    "tools/call", {"name": "context", "arguments": {}}
                )
                self.assertTrue((copied / "skills/diffusion-edit/SKILL.md").is_file())
                self.assertFalse(report["cli"]["available"])


class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.doctor = load_doctor(PLUGIN)

    def test_failed_context_is_not_reported_ready(self):
        with mock.patch.object(self.doctor.shutil, "which", return_value=None), \
                mock.patch.object(self.doctor, "MCPClient") as factory:
            client = factory.return_value
            client.initialize.return_value = {"serverInfo": {"name": "diffusion"}}
            client.send.side_effect = [
                {"tools": [{"name": name} for name in
                           ("open", "context", "capture", "check", "export")]},
                {"isError": True},
            ]
            self.assertFalse(self.doctor.diagnose()["mcpReady"])

    def test_missing_editing_tools_are_reported(self):
        with mock.patch.object(self.doctor.shutil, "which", return_value=None), \
                mock.patch.object(self.doctor, "MCPClient") as factory:
            client = factory.return_value
            client.initialize.return_value = {"serverInfo": {"name": "diffusion"}}
            client.send.side_effect = [
                {"tools": [{"name": "context"}]}, {"content": []},
            ]
            report = self.doctor.diagnose()
            self.assertFalse(report["mcpReady"])
            self.assertEqual(
                report["server"]["missingRequiredTools"],
                ["capture", "check", "export", "open"],
            )

    def test_connection_error_does_not_disclose_private_paths(self):
        output = io.StringIO()
        with mock.patch.object(
            self.doctor, "diagnose",
            side_effect=OSError("private-project-path must not be printed"),
        ), mock.patch("sys.stdout", output):
            self.assertEqual(self.doctor.main(), 1)
        report = json.loads(output.getvalue())
        self.assertFalse(report["mcpReady"])
        self.assertEqual(report["errorType"], "OSError")
        self.assertNotIn("private-project-path", output.getvalue())

    def test_sse_matches_response_id_and_keeps_session(self):
        client = self.doctor.MCPClient("http://127.0.0.1:3274/mcp")
        response = mock.MagicMock()
        response.headers = {
            "Content-Type": "text/event-stream",
            "Mcp-Session-Id": "test-session",
        }
        response.read.return_value = (
            b'data: {"jsonrpc":"2.0","method":"notifications/progress"}\r\n\r\n'
            b'data: {"jsonrpc":"2.0","id":99,"result":{"wrong":true}}\r\n\r\n'
            b'data: {"jsonrpc":"2.0","id":1,"result":{"tools":[]}}\r\n\r\n'
        )
        response.__enter__.return_value = response
        client.opener = mock.Mock()
        client.opener.open.return_value = response
        self.assertEqual(client.send("tools/list"), {"tools": []})
        self.assertEqual(client.headers["Mcp-Session-Id"], "test-session")
        request = client.opener.open.call_args.args[0]
        self.assertEqual(json.loads(request.data)["method"], "tools/list")


if __name__ == "__main__":
    unittest.main()
