# Diffusion Studio

An independent Codex plugin for the Diffusion Studio desktop app. Version 0.1.2 is a GitHub distribution candidate. It includes the app's MCP connection, an editing skill, an original independent icon, and a read-only connection diagnostic. It does not bundle or modify Diffusion Studio.

## Requirements

- Codex with plugin support and local terminal/file access.
- Diffusion Studio installed and running on the same computer as Codex.
- The app's `dapi` CLI, installed in Settings → MCP & CLI, for launching and shell workflows.
- Python 3 only if you use the bundled diagnostic.

The connection uses the app's Streamable HTTP server at `http://127.0.0.1:3274/mcp`. It needs no additional authentication for this local connection. Generative and analysis features can use the services and account configured in Diffusion Studio; basic composition and local previews do not require this plugin to obtain an OpenAI API key.

## Install from this marketplace

From the repository root:

```sh
codex plugin marketplace add .
codex plugin add diffusion-studio@diffusion-studio-community
```

Start a new Codex chat after installation so it can load the plugin's tools and skill. Keep Diffusion Studio running. Invoke Diffusion Studio and ask it to check the connection or create a short title card in a new project.

Run the diagnostic from the plugin folder:

```sh
python3 scripts/doctor.py
```

It checks CLI availability, the MCP handshake, tool discovery, and a read-only `context` request. It does not open a project, generate media, export, or publish anything. A successful result has `mcpReady: true`. Missing `dapi` does not prevent an already-running MCP server from working.

## Package layout

The root `plugin.json` and `mcp.json` follow the portable Agent Plugins schemas. `.codex-plugin/plugin.json` supplies OpenAI presentation and the compatibility MCP/skill declarations; `.mcp.json` is the Codex HTTP configuration. Keep both MCP files in sync. Skills read the documentation shipped with the installed Diffusion Studio version rather than bundling a potentially outdated copy.

## Limits and publication

This version works with local Codex execution on the computer running the editor. A remote ChatGPT or cloud Codex environment cannot reach your computer's loopback address. The local HTTP server is not a public submission endpoint.

For architecture and known limitations, see the repository-root README. This distribution includes no official Diffusion Studio brand assets. This package has not been submitted to or approved by OpenAI and is not affiliated with Diffusion Studio.

References: [Diffusion Studio](https://github.com/diffusionstudio/editor), [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins), [public submission](https://developers.openai.com/plugins/deploy/submission).
