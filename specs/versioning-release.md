# Spec: Versioning & release

## Purpose

Have a single source of truth for the version — the git tag — so releasing is just tagging, and the CLI always reports what was actually built.

## Requirements

1. **Git tags are authoritative.** The package version is derived from the latest `vX.Y.Z` tag by `setuptools-scm` at build time. There is no hardcoded version string in `pyproject.toml` (`dynamic = ["version"]`) or in `h4kfi/__init__.py`.
2. **Runtime reads metadata.** `h4kfi/__init__.py` sets `__version__` from `importlib.metadata.version("h4kfi")`, with a `0.0.0+unknown` fallback when the package isn't installed (e.g. run straight from a source checkout). The CLI banner and `h4kfi --version` both use `__version__`.
3. **Tag format.** Release tags are annotated and named `vX.Y.Z` (semantic versioning). The build strips the leading `v`, so tag `v1.0.0` → version `1.0.0`.
4. **Choosing the bump — strict semver.** Pick the version from the nature of the changes since the last tag, never by default:
   - **major** (`X`) — any backward-incompatible change (removed/renamed CLI flags or MCP tools, changed tool contracts, config format breaks).
   - **minor** (`Y`) — any new backward-compatible feature (`feat:` commits: a new tool, a new flag, a new capability).
   - **patch** (`Z`) — bug fixes, docs, chores only; no new features.

   If a release mixes fixes and features, the highest-ranked change wins (a feature makes it a minor, not a patch).
5. **Dev builds are expected.** A build from a commit after the last tag reports `X.Y.(Z+1).devN+g<hash>`. This is normal and must not be "fixed" by pinning a version.
6. **Clean release builds.** A release wheel is built from a checkout whose `HEAD` is the tag with a clean tree, so the version is exactly `X.Y.Z` with no `.devN`/`+dirty` suffix.

## Release procedure

```bash
# 1. Ensure the working tree is clean and on the release commit
git status

# 2. Tag and push
git tag -a vX.Y.Z -m "h4kfi vX.Y.Z"
git push origin main
git push origin vX.Y.Z

# 3. Build a clean wheel (version comes from the tag)
python -m build --wheel

# 4. Verify
python -m venv /tmp/h4kfi-check
/tmp/h4kfi-check/bin/pip install "dist/h4kfi-X.Y.Z-py3-none-any.whl"
/tmp/h4kfi-check/bin/h4kfi --version      # -> h4kfi vX.Y.Z

# 5. Reinstall globally from the wheel (see installation.md)
sudo pipx install --global --force "dist/h4kfi-X.Y.Z-py3-none-any.whl[mcp]"
```

## Verification

- `git describe --tags` on the release commit prints exactly `vX.Y.Z`.
- The built wheel filename and `h4kfi --version` both show `X.Y.Z` with no suffix.

## Non-goals

- Automated changelog generation or CI release pipelines (may be added later).
