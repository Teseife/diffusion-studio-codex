# Diffusion Studio for Claude Code

Use Claude Code to create, edit, inspect, preview, and export local video projects in the Diffusion Studio desktop app. This plugin shares its editing skill and app connection with the Codex plugin.

## Requirements

- A current local [Claude Code installation](https://code.claude.com/docs/en/overview), signed in for chat.
- [Diffusion Studio](https://www.diffusion.studio/download) installed and running on the same computer.
- The app's `dapi` CLI, installed in **Settings → MCP & CLI**, for launch and shell workflows.
- Python 3 only for the optional connection diagnostic.

The plugin connects to the app's existing HTTP MCP server at `http://127.0.0.1:3274/mcp`. It does not run a second editor server or require hosting. An already-running editor works without `dapi`. Claude Code authentication is separate from the app connection; optional AI generation and media analysis use services configured in Diffusion Studio.

## Install from GitHub

Keep Diffusion Studio open. Run these commands in a terminal:

```sh
claude plugin marketplace add Teseife/diffusion-studio-codex
claude plugin install diffusion-studio@diffusion-studio-community
claude
```

The repository is public; no repository invitation is required. These commands install at user scope, making the plugin available in your local Claude Code projects.

In the new Claude Code session:

1. Open `/plugin` and confirm Diffusion Studio is enabled.
2. Open `/mcp` and confirm `plugin:diffusion-studio:diffusion-studio` connects.
3. Ask: **“Check my Diffusion Studio connection and explain what I can do with it.”**

Then run the editing skill explicitly:

```text
/diffusion-studio:diffusion-edit Create a five-second title card in a new project that says "Made with Diffusion Studio." Show me a preview.
```

You can also ask Claude in ordinary language to edit footage, add captions, or change the title. Review a captured preview first; ask for an export when you want a video file. The plugin respects Claude Code's normal tool permissions.

## Install from a local clone

```sh
git clone https://github.com/Teseife/diffusion-studio-codex.git
cd diffusion-studio-codex
claude plugin marketplace add "$PWD"
claude plugin install diffusion-studio@diffusion-studio-community
claude
```

Keep the clone in place as the local marketplace source. When using a ZIP download, extract it and run the last three commands from its root.

For one development session without a marketplace installation, run from the repository root:

```sh
claude --plugin-dir ./plugins/diffusion-studio
```

## Install with an agent

Paste this into a local Claude Code session on the computer running the editor:

```text
Install the independent Diffusion Studio plugin from the public GitHub
repository Teseife/diffusion-studio-codex on this computer.

Check existing marketplaces and plugins first. Check whether Diffusion Studio
is running and whether dapi is available. If dapi is present, start the editor
with dapi open --background without creating a project.

Register the marketplace with:
claude plugin marketplace add Teseife/diffusion-studio-codex

Install:
claude plugin install diffusion-studio@diffusion-studio-community

If already installed, update the marketplace and plugin instead of adding
a duplicate. Confirm it is enabled. Run the bundled scripts/doctor.py from
the actual installed plugin folder using Python 3 and report the result.

Preserve my existing projects, plugin settings and other MCP servers.
Do not generate media, export a video, or publish an issue as an install check.
Tell me to start a new Claude Code session to load the new tools and skill.
```

## Update

For a GitHub marketplace installation:

```sh
claude plugin marketplace update diffusion-studio-community
claude plugin update diffusion-studio@diffusion-studio-community
```

For a local clone, first run `git pull --ff-only` from its root, then run the same two commands. Start a new Claude Code session afterward.

## Troubleshooting

**Plugin missing:** Run `claude plugin list --json`. Look for `diffusion-studio@diffusion-studio-community` with `enabled: true`. If disabled, run `claude plugin enable diffusion-studio@diffusion-studio-community`, then start a new session.

**Cannot connect:** Open the editor and check **Settings → MCP & CLI**. From the repository root, run:

```sh
python3 plugins/diffusion-studio/scripts/doctor.py
```

A working connection reports `mcpReady: true`. This checks the live handshake, tool discovery and read-only app context; it does not modify projects. The installed copy contains the same script under its `scripts/` directory. Missing `dapi` affects shell workflows, not an already-running MCP connection.

**Duplicate MCP connection:** The plugin supplies the server automatically. You do not need to add it separately with `claude mcp add`. If you already configured the same endpoint manually, check `/mcp` to identify which connection is active.

**Claude requires sign-in:** Run `claude` and complete its sign-in flow. Successful plugin installation and an MCP connection do not authenticate a Claude chat session.

**Remote/cloud session:** A remote Claude Code executor cannot reach the editor on your own computer through `127.0.0.1`. Run Claude Code locally with the editor.

## Package and support

The repository-root `.claude-plugin/marketplace.json` lists `./plugins/diffusion-studio`. That shared package contains Claude's `.claude-plugin/plugin.json`, Codex's `.codex-plugin/plugin.json`, the shared `.mcp.json`, the editing skill, and the diagnostic.

macOS installation and live connectivity are validated; Windows and a signed-in Claude model-driven editing session remain unverified. See [validation](../VALIDATION.md). This is an independent community plugin, not an Anthropic, OpenAI, or Diffusion Studio endorsement or official directory listing.

References: [Claude Code plugins](https://code.claude.com/docs/en/plugins/create), [marketplace format](https://code.claude.com/docs/en/plugins/marketplace-reference), [plugin MCP servers](https://code.claude.com/docs/en/mcp#plugin-provided-mcp-servers).
