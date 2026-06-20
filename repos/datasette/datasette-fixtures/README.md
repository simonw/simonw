# datasette-fixtures

[![PyPI](https://img.shields.io/pypi/v/datasette-fixtures.svg)](https://pypi.org/project/datasette-fixtures/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-fixtures?include_prereleases&label=changelog)](https://github.com/datasette/datasette-fixtures/releases)
[![Tests](https://github.com/datasette/datasette-fixtures/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-fixtures/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-fixtures/blob/main/LICENSE)

Make the Datasette fixtures database available

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-fixtures
```

## Usage

Install the plugin in the same environment as Datasette and it will create a
named in-memory database called `fixtures` on startup.

```bash
datasette
```
Or to try it with `uvx` without first installing Datasette:

```bash
uvx --with datasette-fixtures datasette
```

The Datasette fixtures database will then be available at `/fixtures`.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-fixtures
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
