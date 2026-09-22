# AGENTS.md

Guidance for AI agents (OpenCode first, Claude Code and others second) that install, operate, or develop h4kfi. Read this before running any tool or changing any code. Detailed contracts live in [`specs/`](specs/).

## What h4kfi is

A wireless penetration-testing framework meant to be driven by an AI agent over MCP. It wraps the aircrack-ng suite, hashcat, reaver/bully, and hcxdumptool, and exposes the whole chain — monitor mode, scanning, handshake/PMKID capture, WPS attacks, deauth, cracking — as MCP tools plus a CLI/TUI. OpenCode is the primary MCP client; Claude Code works but its auto-mode classifier blocks some tools (see the README's "Claude Code limitations").

## Safety rules — non-negotiable

1. **Authorized targets only.** Never run capture, deauth, WPS, or crack tools against a network the operator has not confirmed in writing they own or are authorized to test. If scope is unstated, ask before acting.
2. **Pick the right interface.** Enabling monitor mode on the adapter that carries the machine's internet **drops that connection**. Before `enable_monitor`, `scan_networks`, or any capture, confirm which interface to use and prefer a dedicated secondary (e.g. USB) adapter — never the primary uplink unless the operator explicitly accepts losing connectivity.
3. **Start read-only.** When exploring, prefer non-invasive tools first: `list_interfaces`, `check_dependencies`, `find_wordlists`. These don't touch the air or drop connectivity.
4. **`deauth` and active attacks affect other devices.** They are only ever run inside the authorized scope, against the authorized target.
5. **Restore state.** After an engagement, return interfaces to managed mode (`disable_monitor`).

## Repository layout

```
h4kfi/            Python package
  cli.py          Entry point, interactive TUI, CLI subcommands
  ui.py           Rich-based terminal UI (banner, menus, tables)
  scanner.py      Network discovery + client tracking
  attacks.py      WEP / WPA / WPS / PMKID attack implementations
  handshake.py    Handshake capture + verification
  cracker.py      aircrack-ng / hashcat / john backends
  interface.py    Wireless interface management
  session.py      Session persistence (~/.h4kfi/)
  report.py       HTML / JSON / text reports
  config.py       Config at ~/.h4kfi/config.json
  deps.py         Dependency checks
  mcp_server.py   MCP server (stdio) exposing the tools above
specs/            Behavior/contract specs (source of truth for intent)
docs/             README images (banner, screenshot)
pyproject.toml    Packaging; version comes from git tags (setuptools-scm)
```

## Installing h4kfi (AI-driven)

Full contract: [`specs/installation.md`](specs/installation.md). Summary:

1. **System deps** (per distro; only aircrack-ng is strictly required):
   `sudo apt install -y aircrack-ng reaver bully hcxdumptool hcxtools hashcat macchanger mdk4 tshark`
2. **Install the package globally** so it's on root's `secure_path` and survives across shells. Prefer installing a **built wheel**, not the source dir, so no build runs as root inside the working tree:
   ```bash
   python -m build --wheel                 # produces dist/h4kfi-<ver>-py3-none-any.whl
   sudo pipx install --global --force "dist/h4kfi-<ver>-py3-none-any.whl[mcp]"
   ```
   This puts `h4kfi` and `h4kfi-mcp` in `/usr/local/bin`.
3. **Grant the MCP server passwordless root**, scoped to the exact binary (it runs as a TTY-less subprocess, so plain sudo can't prompt):
   ```bash
   echo "$USER ALL=(root) NOPASSWD: /usr/local/bin/h4kfi-mcp" > /tmp/h4kfi-mcp-sudoers
   sudo visudo -c -f /tmp/h4kfi-mcp-sudoers
   sudo install -m 0440 -o root -g root /tmp/h4kfi-mcp-sudoers /etc/sudoers.d/h4kfi-mcp
   rm -f /tmp/h4kfi-mcp-sudoers
   ```
4. **Register the MCP server** with the client. OpenCode (`~/.config/opencode/opencode.json`):
   ```json
   { "mcp": { "h4kfi": { "type": "local", "command": ["sudo", "-n", "/usr/local/bin/h4kfi-mcp"], "enabled": true } } }
   ```

**Note for agents:** steps 1–3 need root. An agent without a TTY cannot enter a sudo password — surface the exact commands to the operator to run, rather than trying to work around it.

## Operating h4kfi over MCP

Tool contracts: [`specs/mcp-server.md`](specs/mcp-server.md). The agent drives an engagement from a plain-language brief: pick interface → scan → choose target from encryption → capture → crack, reacting to each tool's output. Keep the operator at the level of intent and authorization; make the tactical calls yourself, but honor the safety rules above.

## Development

### Versioning & releases — driven by git tags

The version is **not** hardcoded. `pyproject.toml` uses `setuptools-scm`, and `h4kfi/__init__.py` reads it from installed metadata. Everything that shows the version (CLI banner, `h4kfi --version`) follows the latest git tag automatically.

- To cut a release: `git tag -a vX.Y.Z -m "h4kfi vX.Y.Z" && git push origin vX.Y.Z`, then rebuild the wheel and reinstall.
- Between tags, builds report a dev version like `X.Y.(Z+1).devN+g<hash>` — expected, not a bug.
- Never reintroduce a hardcoded `version = "..."` in `pyproject.toml` or `__version__` in `__init__.py`.

Details: [`specs/versioning-release.md`](specs/versioning-release.md).

### Build & verify

```bash
python -m build --wheel
python -m venv /tmp/h4kfi-check && /tmp/h4kfi-check/bin/pip install "dist/h4kfi-<ver>-py3-none-any.whl"
/tmp/h4kfi-check/bin/h4kfi --version    # should print the tag version
```

Avoid `sudo pip`/`sudo pipx install --global <source-dir>`: building as root inside the repo leaves root-owned `build/` and `*.egg-info/` behind that then break non-root builds. Install a wheel instead.

### Conventions

- Python ≥ 3.9, standard library + `rich` + `click`; MCP is an optional extra.
- The CLI/TUI must work without the `mcp` extra installed. `mcp_server.py` is the only module that imports `mcp`, and it's loaded solely by the `h4kfi-mcp` entry point — never import it from `cli.py`.
- Terminal branding is red/black/white to match the README banner. The CLI ASCII banner lives in `h4kfi/ui.py` (`BANNER_ART`).
- The repository is English-only, including code comments, docs, and specs.
- Don't commit build artifacts (`dist/`, `build/`, `*.egg-info/`) — they're gitignored.

## Client-specific notes

- **OpenCode (primary):** no extra classifier layer; once the MCP server is registered and the sudoers rule is in place, all `h4kfi_*` tools are available.
- **Claude Code (secondary):** its auto-mode classifier blocks `scan_networks` (as a "Third-Party Attack") and won't let the model grant itself the exemption (blocked as "Self-Modification"). The operator must add an allowlist to `~/.claude/settings.json` by hand — see the README.
