---
name: diffusion-edit
description: Create, edit, inspect, preview, or export video projects in Diffusion Studio, or diagnose its local connection to Codex or Claude Code. Use when the user chooses or invokes Diffusion Studio.
---

Use Diffusion Studio's local MCP tools and composition source files to complete the user's editing request. The app is a local dependency; this plugin does not contain the editor or its runtime.

## Connect and find the current reference

Call the plugin's `context` tool to check the connection and identify the open project. Discover tools by their names and descriptions; clients add different prefixes to the app's tool names. In Claude Code the server appears in `/mcp` as `plugin:diffusion-studio:diffusion-studio`, and the editing skill can be invoked as `/diffusion-studio:diffusion-edit`.

If tools are unavailable, run the package's diagnostic. In Claude Code use `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/doctor.py"` when that plugin-root variable is available; otherwise resolve `../../scripts/doctor.py` relative to this skill's directory, not the shell's working directory. Its JSON output reports the installed CLI, MCP handshake, tool discovery, and app-context status without printing private project paths.

If the app is stopped, launch Diffusion Studio. With `dapi` installed, `dapi open --background` starts it without creating a project. Missing dependencies can be installed through the official app download and Settings → MCP & CLI; explain what is missing instead of claiming the connection worked. After installing or updating, start a new Codex chat or Claude Code session so it loads the plugin's tools. In Claude Code, check `/plugin` and `/mcp` if the plugin or server is disabled, and respect the user's normal tool permissions.

The server's initialization instructions give the installed documentation directory. Read its `skills/editor.md` for editing or `skills/watch.md` for footage questions, then only the relevant tool and JSX references. These app-version references are authoritative for syntax and tool fields. Read app documentation in place; never modify it. On macOS the usual location is `/Applications/Diffusion Studio.app/Contents/Resources/docs`; use the actual path reported by the app on other systems. If the instructions are unavailable, consult CLI help and the official repository's `docs/` directory, clearly noting any version difference.

## Edit the intended project

Use the project requested by the user. When creating something new, choose a new folder in the user's workspace and call `open` with its absolute path. For an existing project, inspect its entry file and preserve the user's changes. `open` may scaffold `index.tsx` and project metadata, so do not point it at unrelated folders.

The source is the document: a default-exported Solid component renders a `<stage>` with scenes. Saving recompiles and updates the editor. Use stable element IDs and mark one scene `active`. Read the installed JSX reference before choosing layout, timing, animations, captions, or generation declarations. The app provides `solid-js` and `@diffusionstudio/jsx` at runtime; other packages must resolve from the project.

For footage, probe the file first, then inspect the modalities needed to make editing decisions. Use filmstrips or waveform previews for an overview, timed transcripts for speech cuts, and grabbed frames for exact visual checks. Keep reusable footage in the project's asset library using the app's documented library paths. For a complex edit, save a short brief alongside the project and verify the result against it.

For generated assets, inspect available models, voices, constraints, and the user's existing settings. Add generation only when it serves the requested task; do not trigger paid generation merely to test the connection. Poll `context` for generation progress. Add automatic captions after the final audio placement is established.

## Verify and deliver

Run `check` on the changed scene to catch structural errors. Use `capture` at representative times to inspect actual rendered frames for substantial composition changes. Saving successfully or seeing the editor window is not visual verification. Report unresolved load, compile, or generation errors accurately.

Export only when the user requests a video file; use `capture` for previews. Read the export reference, use the scene's configured settings, and confirm the returned file exists before linking it. Include the project or source path and the preview or export in the response when useful.

The `report` tool publishes a GitHub issue immediately, including diagnostics. Use it only when the user explicitly asks to file a public issue and after inspecting the diagnostics. A connection test or bug investigation does not authorize that publication.
