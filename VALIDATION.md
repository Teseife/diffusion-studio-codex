# Validation and support

## 0.1.3 — Claude Code support, October 3, 2026

Checked on macOS with Claude Code 2.1.284 and Diffusion Studio/dapi 0.209.0:

- Claude Code's native validator passed the new marketplace and plugin manifests with `--strict`, with no errors or warnings.
- An isolated Claude Code configuration registered the local marketplace and installed `diffusion-studio@diffusion-studio-community` version 0.1.3, enabled.
- Claude Code's component inventory discovered the `diffusion-edit` skill and one MCP server from the installed package.
- `claude mcp list` reported the plugin's HTTP server as connected.
- The read-only diagnostic completed MCP initialization, discovered 19 app tools, and read app context with `mcpReady: true`.
- Eight automated tests passed, covering marketplace source resolution, shared release/MCP consistency, the diagnostic in a copied package, missing tools, failed app context, private-path redaction and SSE response/session handling.

The GitHub workflow runs the automated tests, strict native Claude manifest validation, and a fresh-profile plugin install on Linux. Its installation check does not require Claude sign-in or a running editor.

The existing Codex marketplace, MCP endpoint and presentation configuration are retained. The Codex, Claude and portable manifests share version 0.1.3; the editing skill now addresses both clients.

Claude Code was not signed in on the test computer. A Claude model-driven editing conversation remains to be acceptance-tested; package installation and live MCP connectivity were verified independently. Windows and cloud execution remain outside the validated setup.

## Original Codex integration

The integration was checked on macOS with Codex CLI 0.159.2 and Diffusion Studio/dapi 0.208.0.

- The original local plugin installed and was enabled in Codex.
- Real MCP initialization discovered 18 app tools and successfully read app context.
- A separate five-second composition passed the app's structural check and produced visually inspected captures at three timeline positions.
- Original plugin/MCP manifests passed Agent Plugins schemas, and the editing skill passed the Skill Creator validator.

Version 0.1.2 packaged that integration for GitHub with an independent icon and a separate marketplace identity.

A full native-plugin chat workflow with real footage, captions, and video export remains to be acceptance-tested. Windows is unverified. Cloud clients cannot use the loopback endpoint. AI generation/analysis may require services configured in Diffusion Studio. This package has not been submitted to the OpenAI public directory.
