#!/usr/bin/env python3
"""Read-only local dependency and MCP checks; no third-party Python modules."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.error
import urllib.request


class MCPClient:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        self.request_id = 0
        # A local MCP endpoint must not go through a configured web proxy.
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def send(self, method, params=None, notification=False):
        message = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        if not notification:
            self.request_id += 1
            message["id"] = self.request_id
        request = urllib.request.Request(
            self.url, json.dumps(message).encode("utf-8"), self.headers
        )
        with self.opener.open(request, timeout=10) as response:
            session = response.headers.get("Mcp-Session-Id")
            if session:
                self.headers["Mcp-Session-Id"] = session
            raw = response.read().decode("utf-8")
            content_type = response.headers.get("Content-Type", "")
        if notification:
            return None
        if "text/event-stream" in content_type:
            response_data = None
            for event in raw.replace("\r\n", "\n").split("\n\n"):
                data = "\n".join(
                    line[5:].lstrip() for line in event.splitlines()
                    if line.startswith("data:")
                )
                if data:
                    candidate = json.loads(data)
                    if candidate.get("id") == message["id"]:
                        response_data = candidate
                        break
            if response_data is None:
                raise ValueError("MCP response did not include the requested result")
        else:
            response_data = json.loads(raw)
        if "error" in response_data:
            raise ValueError("MCP returned an error for " + method)
        return response_data["result"]

    def initialize(self):
        result = self.send("initialize", {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "diffusion-studio-doctor", "version": "0.1.2"},
        })
        self.headers["Mcp-Protocol-Version"] = result["protocolVersion"]
        self.send("notifications/initialized", notification=True)
        return result


def diagnose():
    executable = shutil.which("dapi") or shutil.which("diffusion")
    report = {"cli": {"available": executable is not None}}
    if executable:
        version = subprocess.run(
            [executable, "--version"], capture_output=True, text=True, timeout=10
        )
        report["cli"]["version"] = version.stdout.strip()
        report["cli"]["healthy"] = version.returncode == 0
    plugin_root = Path(__file__).resolve().parents[1]
    config = json.loads((plugin_root / ".mcp.json").read_text())
    url = config["mcpServers"]["diffusion-studio"]["url"]
    client = MCPClient(url)
    init = client.initialize()
    tools = client.send("tools/list")["tools"]
    names = {tool["name"] for tool in tools}
    missing = sorted({"open", "context", "capture", "check", "export"} - names)
    context = client.send("tools/call", {"name": "context", "arguments": {}})
    report["server"] = {
        "name": init["serverInfo"]["name"],
        "version": init["serverInfo"].get("version"),
        "toolCount": len(tools),
        "missingRequiredTools": missing,
        "contextReadable": not context.get("isError", False),
    }
    report["mcpReady"] = not missing and report["server"]["contextReadable"]
    if not report["cli"]["available"]:
        report["nextStep"] = "Install dapi in Diffusion Studio Settings → MCP & CLI for shell workflows."
    return report


def main():
    try:
        report = diagnose()
        status = 0 if report["mcpReady"] else 1
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        report = {
            "mcpReady": False,
            "errorType": type(error).__name__,
            "nextStep": "Launch Diffusion Studio, then retry. If it is running, check Settings → MCP & CLI.",
        }
        status = 1
    print(json.dumps(report, indent=2))
    return status


if __name__ == "__main__":
    sys.exit(main())
