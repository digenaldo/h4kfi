# Notice

h4kfi is a derivative work based on [AutoWIFI](https://github.com/momenbasel/AutoWIFI)
by momenbasel, licensed under GPL-3.0-only. This project keeps the wireless
attack engine largely as-is and rebuilds the project around MCP integration:
OpenCode as the primary client, with Claude Code kept as a secondary,
more restricted option (see the README for why).

Changes made on top of the original codebase include, among others:
- A fix for the MCP server, which didn't run on `mcp>=2.0`.
- A fix for PMKID capture, whose `hcxdumptool` CLI flags were removed in v6.x.
- Per-client details (MAC, signal, packet count) added to the `scan_networks`
  MCP tool output.
- Documentation of the sudo/NOPASSWD setup required for the MCP server to
  touch the wireless interface without a TTY.
- Documentation of Claude Code's auto mode classifier, which blocks these
  tool calls by default and can't be worked around by the model itself.

In keeping with GPL-3.0-only, this project remains under the same license.
