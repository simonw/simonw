# datasette-sql-comments-metadata

[![PyPI](https://img.shields.io/pypi/v/datasette-sql-comments-metadata.svg)](https://pypi.org/project/datasette-sql-comments-metadata/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-sql-comments-metadata?include_prereleases&label=changelog)](https://github.com/datasette/datasette-sql-comments-metadata/releases)
[![Tests](https://github.com/datasette/datasette-sql-comments-metadata/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-sql-comments-metadata/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-sql-comments-metadata/blob/main/LICENSE)

Adopt table metadata from SQL comments in CREATE statements

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-sql-comments-metadata
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-sql-comments-metadata
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
