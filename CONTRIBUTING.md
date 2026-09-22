# Contributing to h4kfi

Thanks for your interest in improving h4kfi. This guide covers how to set up, make changes, and propose them. If you're an AI agent working on the project, read [AGENTS.md](AGENTS.md) first — it has the operating and safety rules; the behavior contracts live in [specs/](specs/).

## Ground rules

- **Authorized use only.** h4kfi is for authorized security testing and education. Don't contribute features whose only purpose is to make unauthorized attacks easier or harder to trace.
- **English-only repository.** Code, comments, docs, commit messages, and specs are all in English.
- **Keep the CLI usable without the `mcp` extra.** Only `mcp_server.py` imports `mcp`, and only the `h4kfi-mcp` entry point loads it. Never import it from `cli.py`.
- **Spec-first for behavior changes.** If you change how a subsystem behaves on purpose, update the matching file in `specs/` in the same change.

## Development setup

```bash
git clone https://github.com/digenaldo/h4kfi.git
cd h4kfi
python -m venv .venv && . .venv/bin/activate
pip install -e ".[mcp]"
```

Run the CLI locally with `sudo h4kfi` (wireless operations need root). For MCP work, see [specs/installation.md](specs/installation.md).

## Making changes

1. Branch from `main`: `git checkout -b feat/short-description`.
2. Keep changes focused. Match the surrounding style; standard library plus `rich` and `click`, no new runtime dependencies without discussion.
3. Verify a clean build and that the CLI still runs:
   ```bash
   python -m build --wheel
   python -m venv /tmp/h4kfi-check && /tmp/h4kfi-check/bin/pip install dist/h4kfi-*.whl
   /tmp/h4kfi-check/bin/h4kfi --version
   ```
4. Don't commit build artifacts (`dist/`, `build/`, `*.egg-info/`) — they're gitignored.

## Commit messages

- Imperative mood, concise subject: `Fix PMKID capture on hcxdumptool v6.x`.
- Explain the *why* in the body when it isn't obvious. One logical change per commit.

## Pull requests

- Describe what changed and why, and how you verified it.
- Reference any spec you updated.
- Small, reviewable PRs are preferred over large ones.

## Versioning

Versions come from git tags via `setuptools-scm` — never hardcode a version. Releases are cut by maintainers (see [specs/versioning-release.md](specs/versioning-release.md)); you don't need to bump anything in your PR.

## Reporting issues

Open a GitHub issue with your OS/distro, adapter and chipset, the exact command or MCP tool call, and the full output. For anything that looks security-sensitive, describe the class of problem rather than a working exploit.

## License

By contributing, you agree that your contributions are licensed under the project's [GPL-3.0](LICENSE).
