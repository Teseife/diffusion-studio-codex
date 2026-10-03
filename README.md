# Diffusion Studio for Codex and Claude Code

Create and edit video projects from Codex or Claude Code, preview your work, and continue editing in Diffusion Studio.

## Demo

https://github.com/user-attachments/assets/bfd0a3f8-aef8-49a7-bf9a-553e3071cd2b

**1:12 · 1080p · music and sound effects** — installation, a prompt in Codex, preview playback, and the editable Diffusion Studio timeline.

[Download the MP4](https://github.com/Teseife/diffusion-studio-codex/raw/refs/heads/main/docs/videos/Diffusion-Studio-Plugin-Launch-v2.mp4) · [Demo guide](./docs/demo.md)

## What you can do

- Create title cards, motion graphics, and short videos from a prompt.
- Edit footage and arrange scenes in a local project.
- Add readable captions.
- Check a composition and capture previews.
- Export a finished video when you're ready.

## Before you start

- Install a local [Codex client](https://developers.openai.com/codex/cli) or [Claude Code](https://code.claude.com/docs/en/overview) with plugin support and terminal/file access. Sign in to your chosen client for chat.
- Install and open [Diffusion Studio](https://www.diffusion.studio/download) on the same computer.
- In Diffusion Studio, go to **Settings → MCP & CLI** and install `dapi` for terminal workflows.

The repository is public. The editor and your chosen client run on the same computer.

## Install in Codex

1. Keep Diffusion Studio open and make sure `codex` is available in your terminal.
2. Clone the repository, register its marketplace, and install the plugin:

```sh
git clone https://github.com/Teseife/diffusion-studio-codex.git
cd diffusion-studio-codex
codex plugin marketplace add .
codex plugin add diffusion-studio@diffusion-studio-community
```

3. Start a new Codex chat. In **Plugins**, search for `diff`, open **Diffusion Studio**, and choose **Try now** or select the plugin in your chat.

Keep the cloned folder in place: Codex uses it as the local marketplace source. If the plugin doesn't appear, reopen the Plugins view or restart Codex after saving your work.

<details>
<summary>Alternative: install directly from GitHub</summary>

You can register the public GitHub marketplace without a manual clone:

```sh
codex plugin marketplace add Teseife/diffusion-studio-codex --ref main
codex plugin add diffusion-studio@diffusion-studio-community
```

</details>

<details>
<summary>Ask Codex to help install the plugin</summary>

Use a local Codex chat on the computer running Diffusion Studio:

```text
Help me install the Diffusion Studio plugin from
Teseife/diffusion-studio-codex on this computer.

Check existing installations first and use my existing Git authentication.
Register the diffusion-studio-community marketplace and install
diffusion-studio@diffusion-studio-community. Check that the plugin is
enabled and run its bundled connection diagnostic. Explain any missing
dependencies or repository-access problems. Preserve my existing projects.
```

Start a new chat after installation to load the plugin's tools.

</details>

## Install in Claude Code

Keep Diffusion Studio open, then run:

```sh
claude plugin marketplace add Teseife/diffusion-studio-codex
claude plugin install diffusion-studio@diffusion-studio-community
claude
```

In the new session, check `/plugin` for the enabled plugin and `/mcp` for `plugin:diffusion-studio:diffusion-studio`. Ask Claude to check your connection, then try:

```text
/diffusion-studio:diffusion-edit Create a five-second title card in a new project that says "Made with Diffusion Studio." Show me a preview.
```

The same skill also works with ordinary-language requests. See the [Claude Code guide](./docs/claude-code.md) for local-clone and agent-assisted installation, updates, and troubleshooting.

## Make your first video

First, ask your chosen client:

> Check my Diffusion Studio connection and explain what I can do with it.

Then try the prompt from the demo:

> Create a short animated video showcasing this plugin's capabilities: create and edit video, add captions, preview, and export. Use kinetic typography and show me a preview.

Review the preview, ask for changes, and open the project in Diffusion Studio to work with its canvas and timeline. When you're happy with the result, ask your client to export the video.

## More example prompts

> Create a five-second title card in a new project that says "Made with Diffusion Studio." Show me a preview.

> Edit this footage into a short video and add readable captions.

> Make the title orange, tighten the pacing, and show me the updated preview.

> Export the current composition as a 1080p MP4.

## Update

For Claude Code, run:

```sh
claude plugin marketplace update diffusion-studio-community
claude plugin update diffusion-studio@diffusion-studio-community
```

If you installed from a local clone, first pull the latest changes. Start a new Claude Code session after updating.

For Codex:

For the local clone installation, run these commands inside the cloned repository:

```sh
git pull --ff-only
codex plugin add diffusion-studio@diffusion-studio-community
```

For the direct GitHub marketplace installation:

```sh
codex plugin marketplace upgrade diffusion-studio-community
codex plugin add diffusion-studio@diffusion-studio-community
```

Start a new Codex chat after updating.

## Troubleshooting

For Claude Code plugin/session issues, see the [Claude Code troubleshooting guide](./docs/claude-code.md#troubleshooting). The diagnostic below works for either client.

**Plugin missing?** Check the installation:

```sh
codex plugin list --marketplace diffusion-studio-community --json
```

Look for `diffusion-studio@diffusion-studio-community` with `enabled: true`, then open a new chat.

**Editor connection unavailable?** Open Diffusion Studio and check **Settings → MCP & CLI**. From the cloned repository, run the optional diagnostic with Python 3:

```sh
python3 plugins/diffusion-studio/scripts/doctor.py
```

A ready connection reports `mcpReady: true`.

**Clone or download fails?** Check the repository URL and Git/network access. The repository is public. You can also download and extract its ZIP, then register that folder as the marketplace in your chosen client. Keep the extracted folder in place; download a fresh copy when updating a ZIP installation.

**Duplicate Diffusion Studio entries?** If you also have the personal `diffusion-studio-local` version installed, enable one copy at a time.

## Details and clarifications

- This is an independent community plugin, unaffiliated with Diffusion Studio, OpenAI, or Anthropic. It is distributed through this GitHub marketplace, not an official vendor directory.
- Codex and Claude Code connect to Diffusion Studio's local MCP server at `http://127.0.0.1:3274/mcp`. Run your client locally on the computer running the editor; cloud execution cannot reach that local address.
- macOS has been tested. Windows support has not been verified. Optional generation and analysis features use the services configured in Diffusion Studio.
- The demo combines recreated GitHub, terminal, and Codex interactions with real Diffusion Studio project output and an editor capture.
- Plugin code and the independent plugin icon are [MIT licensed](./LICENSE). Diffusion Studio is a separate dependency with its own terms; third-party branding in the demo and screenshots is not covered by this project's MIT license.

See [validation and limitations](./VALIDATION.md), [release notes](./CHANGELOG.md), and the [plugin package guide](./plugins/diffusion-studio/README.md).
