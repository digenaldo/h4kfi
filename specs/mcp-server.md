# Spec: MCP server

## Purpose

Expose h4kfi's wireless-testing capabilities to an AI agent over MCP stdio transport, so an agent can run a full engagement from a plain-language brief. Primary client: OpenCode.

## Requirements

1. **Transport.** The server (`h4kfi-mcp`) speaks MCP over stdio. It requires the `mcp` extra (`mcp>=1.0,<2.0`; the low-level `Server` API it uses was removed in 2.x). The server name it registers is `h4kfi`, so tools appear to clients as `h4kfi_<tool>` / `mcp__h4kfi__<tool>`.
2. **Privilege.** Every tool that touches a wireless interface requires root (see [installation.md](installation.md)). Tools that only read local state may run unprivileged but are expected to run under the same root process in practice.
3. **Shared session state.** The server keeps state across calls within a session (selected monitor interface, last scan results, current target, captured handshake path) so the agent doesn't re-pass everything each call.
4. **Safety posture.** Tool descriptions and behavior must not encourage use outside an authorized scope. Active tools (`deauth`, capture, WPS, crack) assume the operator has authorized the target; the agent is responsible for confirming scope per `AGENTS.md`.

## Tool surface

Read-only / safe-first (no air impact, no connectivity loss):

| Tool | Purpose |
|------|---------|
| `list_interfaces` | List wireless interfaces with mode/driver/chipset |
| `check_dependencies` | Report which external tools are installed |
| `find_wordlists` | Discover installed wordlists (rockyou, seclists, …) |
| `get_recommended_attacks` | Suggest attack vectors for a target from its encryption |
| `verify_handshake` | Validate a capture file offline |

State-changing / air-affecting (root; may drop connectivity or touch other devices):

| Tool | Purpose | Notes |
|------|---------|-------|
| `enable_monitor` | Put an interface into monitor mode | Drops connectivity on that adapter |
| `disable_monitor` | Restore managed mode | Run at end of engagement |
| `scan_networks` | Discover networks + per-client MAC/signal/packets | Passive but requires monitor mode |
| `capture_handshake` | Capture a WPA/WPA2 4-way handshake | Often paired with `deauth` |
| `capture_pmkid` | Capture a PMKID hash (clientless) | Uses hcxdumptool (v6.x CLI) |
| `wps_pixie_dust` | Offline WPS PIN recovery | WPS-enabled targets only |
| `deauth` | Send deauthentication frames | Affects the targeted client(s) — scope only |
| `crack_handshake` | Crack handshake/PMKID | Backends: aircrack / hashcat / john |

## Verification

- A client can list all tools above under the `h4kfi` server.
- `check_dependencies` and `list_interfaces` succeed without touching the air.
- A full path (enable_monitor → scan_networks → capture_handshake + deauth → verify_handshake → crack_handshake → disable_monitor) completes against an authorized test AP.

## Non-goals

- Remote/HTTP MCP transport. stdio only for now.
- Exposing raw shell access as a tool. Each capability is a specific, named tool.
