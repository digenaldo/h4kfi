# specs

Specifications describing how h4kfi is meant to behave. They are the source of truth for *intent* — when code and spec disagree, one of them is a bug. Agents and contributors should read the relevant spec before changing a subsystem, and update the spec in the same change when behavior changes on purpose.

Each spec follows a light shape: **Purpose**, **Requirements** (numbered, testable), and **Non-goals**. Keep them short and concrete.

## Index

- [installation.md](installation.md) — how h4kfi is installed and registered as an MCP server, and the invariants that keeps.
- [mcp-server.md](mcp-server.md) — the MCP tool surface: each tool's purpose, inputs, effects, and privilege/safety requirements.
- [versioning-release.md](versioning-release.md) — git-tag-driven versioning and the release procedure.

See [`../AGENTS.md`](../AGENTS.md) for the operating and development guidance that ties these together.
