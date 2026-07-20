# ready-for-datasette

[![PyPI](https://img.shields.io/pypi/v/ready-for-datasette.svg)](https://pypi.org/project/ready-for-datasette/)
[![Changelog](https://img.shields.io/github/v/release/datasette/ready-for-datasette?include_prereleases&label=changelog)](https://github.com/datasette/ready-for-datasette/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/ready-for-datasette/blob/main/LICENSE)

Check whether a Datasette plugin is ready to publish and works with Datasette
1.0.

## Installation

Install this tool using `uv`:

```bash
uv tool install ready-for-datasette
```

You can also run it without installing it first using `uvx`.

## Usage

Run this from inside a Datasette plugin repository:

```bash
ready-for-datasette
```

Or pass the path to a plugin repository:

```bash
ready-for-datasette path/to/plugin
```

The command checks the plugin's packaging metadata, GitHub Actions test matrix,
action versions and trusted publishing configuration. It performs a clean
build, inspects the wheel and source distribution, and runs the tests included
in the source distribution against Datasette 1.0 alpha and the latest stable
Datasette release.

Use `--verbose` to show output from successful build and test commands.

To run a plugin's working-tree tests with Datasette 1.0a37 and the dependencies
from its `dependency-groups.dev`, use:

```bash
ready-for-datasette test path/to/plugin
```

The equivalent one-off commands, without installing the tool first, are:

```bash
uvx ready-for-datasette path/to/plugin
uvx ready-for-datasette test path/to/plugin
```

## Datasette 1.0 plugin tracker

Tracking which Datasette plugins are ready for Datasette 1.0 stable.

https://lite.datasette.io/?json=https%3A%2F%2Fdatasette.github.io%2Fready-for-datasette%2Fplugins.json#/data/plugins

## Updating the plugin list

`update_plugins.py` scans the public repositories owned by `simonw`, `dogsheep`,
`datasette`, and `asg017`, identifies Datasette plugins from their packaging
entry points, and writes `plugins.json`.

```bash
uv run --no-project python update_plugins.py
```

Each record includes the ETag and SHA-256 of the repository's `pyproject.toml`
or `setup.py`. The ETag enables conditional raw GitHub requests, and an
unchanged SHA-256 reuses the PyPI version already in `plugins.json`, avoiding an
unnecessary API request. Use `--refresh-pypi` to bypass the PyPI cache:

```bash
uv run --no-project python update_plugins.py --refresh-pypi
```

The `Update plugins` GitHub Actions workflow performs a full refresh every day
at 01:30 UTC and can also be run manually using `workflow_dispatch`. It commits
and pushes `plugins.json` when the output changes.

## Testing a released plugin

`run_plugin_tests.py` resolves the latest Datasette 1.0 alpha and the plugin's
latest PyPI release, then writes its test result under `results/`:

```bash
uv run --no-project python run_plugin_tests.py datasette-cluster-map
```

Only released code is tested. The runner downloads and verifies the SHA-256 of
the non-yanked PyPI source distribution. If the repository has a Git tag that
exactly matches that PyPI version, it uses the test suite from that tag;
otherwise it uses only tests included in the source distribution. It never
tests the repository's unreleased default branch. The package installed in the
test environment is always the verified PyPI source distribution; a Git tag
supplies tests only. If that tag contains tests but the source distribution
does not, the runner records a `tests_missing_from_sdist` warning.

The runner only requests a package test extra when that exact PyPI release
advertises one. It also reads standard PEP 735 `test`, `tests`, `testing`, or
`dev` dependency groups (plus compatible optional and legacy uv dependency
declarations) from the exact release source and installs those dependencies
explicitly. The selected extra, dependency source, and dependency list are
recorded in each result. Runner-version changes cause older results to be
scheduled for a fresh run while preserving their immutable history.

Additional pytest arguments follow `--`:

```bash
uv run --no-project python run_plugin_tests.py datasette-cluster-map -- -x
```

Each immutable run contains `pytest.txt` and `result.json`. The newest result
for a package/Datasette pair is copied to `latest.json`, and `results/index.json`
contains all latest results. A failed test suite is successfully recorded and
does not make the runner command itself fail; infrastructure or metadata errors
do.

## Working through the test backlog

The `Test plugins` workflow runs on a schedule and can also
be started manually with `workflow_dispatch`, and runs on pushes to `main`. It
selects five released package/version and Datasette-alpha combinations by
default, with a configurable maximum of ten, that have not reached a terminal
result. New plugin releases take priority, followed by plugins that have never
been tested and plugins that need testing against a new Datasette alpha.
Infrastructure failures are retried after a six-hour cooldown.

Manual runs also accept up to ten comma-separated plugin names. When provided,
that list replaces backlog selection and reruns those exact plugins using their
current PyPI releases, even if they already have results. Named runs refresh
those packages from PyPI first and commit the exact refreshed `plugins.json`
records alongside the results. A newly released plugin can be added without a
full owner scan when its PyPI metadata links to its GitHub repository.

Each selected combination runs independently. A final serialized job downloads
their artifacts, merges each immutable run into `results/`, rebuilds the latest
files and index, and commits and pushes the changes. The nightly plugin refresh
uses the same repository-write concurrency group so the two workflows cannot
push at the same time.

## Publishing the progress report

`generate_report.py` builds a static, searchable scoreboard plus a flat JSON
dataset containing one object for every plugin:

```bash
uv run --no-project python generate_report.py --output site
```

The output is `site/index.html`, `site/plugins.json`, and `site/.nojekyll`.
Every value in each JSON plugin object is a scalar—there are no nested objects
or arrays. The final job in the `Test plugins` workflow always regenerates and
deploys this report to GitHub Pages, even when planning, testing, or merging
results fails.
