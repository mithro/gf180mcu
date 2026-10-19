# gf180mcu 1.0.0

GlobalFoundries' 180nm MCU process, a fully open-source CMOS technology (built on Google's open PDK initiative) for mixed-signal and analog IC design.

<!-- BADGES:START -->
[![Docs](https://github.com/gdsfactory/gf180mcu/actions/workflows/pages.yml/badge.svg)](https://github.com/gdsfactory/gf180mcu/actions/workflows/pages.yml)
[![Tests](https://github.com/gdsfactory/gf180mcu/actions/workflows/test_code.yml/badge.svg)](https://github.com/gdsfactory/gf180mcu/actions/workflows/test_code.yml)
[![DRC](https://github.com/gdsfactory/gf180mcu/raw/badges/drc.svg)](https://github.com/gdsfactory/gf180mcu/actions/workflows/drc.yml)
[![Model Regression](https://github.com/gdsfactory/gf180mcu/actions/workflows/model_regression.yml/badge.svg)](https://github.com/gdsfactory/gf180mcu/actions/workflows/model_regression.yml)
[![Test Coverage](https://github.com/gdsfactory/gf180mcu/raw/badges/coverage.svg)](https://github.com/gdsfactory/gf180mcu/actions/workflows/test_coverage.yml)
[![Model Coverage](https://github.com/gdsfactory/gf180mcu/raw/badges/model_coverage.svg)](https://github.com/gdsfactory/gf180mcu/actions/workflows/model_coverage.yml)
[![Issues](https://github.com/gdsfactory/gf180mcu/raw/badges/issues.svg)](https://github.com/gdsfactory/gf180mcu/issues)
[![PRs](https://github.com/gdsfactory/gf180mcu/raw/badges/prs.svg)](https://github.com/gdsfactory/gf180mcu/pulls)
<!-- BADGES:END -->

## Fork for gf180-tcad

This is [mithro/gf180mcu](https://github.com/mithro/gf180mcu), a fork of
[gdsfactory/gf180mcu](https://github.com/gdsfactory/gf180mcu) (forked at upstream `main`
[96b7324](https://github.com/gdsfactory/gf180mcu/commit/96b7324d85df05704f68c1370c175627d0a88034))
maintained for [gf180-tcad](https://github.com/mithro/gf180-tcad), which compares TCAD against
the PDK SPICE models for GF180MCU 5V devices. gf180-tcad's dev-HEAD TCAD image installs this
PDK together with gdsfactory's development HEAD (10.x), which upstream's `main` does not yet
import under; the fork carries the fixes needed for that.

- All work happens on `gf180/<topic>` branches with pull requests inside this fork (base
  `mithro/gf180mcu:main`).
- Upstream (gdsfactory/gf180mcu) is **read-only** for this fork: no pushes, pull requests,
  issues or comments are made there.
- Fork CI runs only `.github/workflows/test.yml`, on GitHub-hosted runners with no secrets. The
  upstream workflows are deleted: they call reusable workflows that need upstream secrets
  (`GFP_API_KEY`, `ANTHROPIC_API_KEY`, AWS roles) or publish (PyPI release, pages, badges,
  dependabot auto-merge), and this fork never releases or publishes.
- The fork keeps the upstream Apache-2.0 licence.


GlobalFoundries 180nm MCU based on [Google open source PDK](https://github.com/google/globalfoundries-pdk-libs-gf180mcu_fd_pr)

This is a pure python implementation of the PDK.

> **NOTE**: If you were previously using the `gf180` package, it has been renamed to `gf180mcu` and the original package is now deprecated. See the [migration guide](https://gdsfactory.github.io/gf180mcu/migration.html) for more information.

## Installation

We recommend `uv`

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation for users

Use python 3.11, 3.12 or 3.13. We recommend [VSCode](https://code.visualstudio.com/) as an IDE.

```
uv pip install gf180mcu --upgrade
```

Then you need to restart Klayout to make sure the new technology installed appears.

### Installation for contributors

For developers you need to `git clone` the GitHub repository, fork it, git add, git commit, git push and merge request your changes.

```
git clone https://github.com/gdsfactory/gf180mcu.git
cd gf180
uv venv --python 3.12
uv sync --extra docs
```

## Documentation

- [gdsfactory docs](https://gdsfactory.github.io/gdsfactory/)

## Pre-commit

Pre-commit hooks are centrally maintained in [pdk-ci-workflow-public](https://github.com/doplaydo/pdk-ci-workflow-public). `make dev` fetches the canonical config and installs the git hook.

```bash
make dev
```

## Tests

Run the test suite:

```bash
make test
```

## Release

```bash
gh workflow run release.yml --repo gdsfactory/gf180mcu -f version=X.Y.Z
```

Or from inside the repo directory (no `--repo` needed):

```bash
gh workflow run release.yml -f version=X.Y.Z
```

where `+gfpN` suffix is optional (e.g. `3.11.0+gfp0`).
