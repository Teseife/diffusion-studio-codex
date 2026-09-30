# Validation and support

The integration was checked on macOS with Codex CLI 0.159.2 and Diffusion Studio/dapi 0.208.0.

- The original local plugin installed and was enabled in Codex.
- Real MCP initialization discovered 18 app tools and successfully read app context.
- A separate five-second composition passed the app's structural check and produced visually inspected captures at three timeline positions.
- Original plugin/MCP manifests passed Agent Plugins schemas, and the editing skill passed the Skill Creator validator.

Version 0.1.2 packages that integration for GitHub with an independent icon and a separate marketplace identity. Its package and archive checks are recorded during release preparation.

A full native-plugin chat workflow with real footage, captions, and video export remains to be acceptance-tested. Windows is unverified. Cloud clients cannot use the loopback endpoint. AI generation/analysis may require services configured in Diffusion Studio. This package has not been submitted to the OpenAI public directory.
