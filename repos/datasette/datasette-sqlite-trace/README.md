# datasette-sqlite-trace

[![PyPI](https://img.shields.io/pypi/v/datasette-sqlite-trace.svg)](https://pypi.org/project/datasette-sqlite-trace/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-sqlite-trace?include_prereleases&label=changelog)](https://github.com/datasette/datasette-sqlite-trace/releases)
[![Tests](https://github.com/datasette/datasette-sqlite-trace/workflows/Test/badge.svg)](https://github.com/datasette/datasette-sqlite-trace/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-sqlite-trace/blob/main/LICENSE)

Datasette plugin that prints all executed SQL to stderr

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-sqlite-trace
```

## Usage

Once installed, this plugin will log every SQL query executed by Datasette to standard error.
