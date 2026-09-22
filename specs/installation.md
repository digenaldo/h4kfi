# Spec: Installation & MCP registration

## Purpose

Define a repeatable install that leaves h4kfi available to the operator's shell, to `sudo`, and to an MCP client — persistently, without polluting the system Python or the working tree.

## Requirements

1. **Persistent, isolated install.** h4kfi is installed with `pipx` into an isolated venv, not into system site-packages. `pip install` into the system interpreter is disallowed (the host is externally-managed).
2. **Visible to root.** The `h4kfi` and `h4kfi-mcp` entry points must resolve on root's `secure_path`. This is satisfied by a global pipx install, which links them into `/usr/local/bin`. A user-only install in `~/.local/bin` is **not** sufficient, because `sudo`'s `secure_path` excludes it — this is the failure where `sudo h4kfi` reports "command not found" while `h4kfi` works.
3. **Install from a built wheel.** The global install uses a wheel (`dist/h4kfi-<ver>-py3-none-any.whl`), not the source directory. Building as root inside the repo leaves root-owned `build/` and `*.egg-info/` artifacts that break later non-root builds; a wheel install avoids running the build in the tree at all.
4. **MCP privileges are scoped.** The MCP server needs root for every wireless operation but runs as a TTY-less subprocess. Passwordless sudo is granted via a single `/etc/sudoers.d/h4kfi-mcp` rule scoped to the exact absolute path `/usr/local/bin/h4kfi-mcp` — never a blanket `NOPASSWD: ALL`. The rule is validated with `visudo -c` before being installed at mode `0440`, owner `root:root`.
5. **Client points at `sudo -n`.** MCP clients invoke `sudo -n /usr/local/bin/h4kfi-mcp`. The `-n` fails fast instead of hanging if the sudoers rule is ever missing.
6. **No orphan rules.** Installing over a previous name/path (e.g. the old `autowifi-mcp`) removes the stale sudoers rule.
7. **Clean uninstall.** Removing h4kfi means `sudo pipx uninstall --global h4kfi` plus deleting `/etc/sudoers.d/h4kfi-mcp` and the client MCP entry.

## Verification

- `sudo h4kfi --version` prints the current tag version.
- `sudo -n /usr/local/bin/h4kfi-mcp </dev/null` starts without a password prompt and exits cleanly on stdin EOF.
- The MCP client lists the `h4kfi_*` tools.

## Non-goals

- Publishing to PyPI (the project may add this later; installation here is from source/wheel or a git URL).
- Windows/macOS support. h4kfi targets Linux with a monitor-mode-capable adapter.
