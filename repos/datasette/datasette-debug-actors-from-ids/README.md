# datasette-debug-actors-from-ids

[![PyPI](https://img.shields.io/pypi/v/datasette-debug-actors-from-ids.svg)](https://pypi.org/project/datasette-debug-actors-from-ids/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-debug-actors-from-ids?include_prereleases&label=changelog)](https://github.com/datasette/datasette-debug-actors-from-ids/releases)
[![Tests](https://github.com/datasette/datasette-debug-actors-from-ids/workflows/Test/badge.svg)](https://github.com/datasette/datasette-debug-actors-from-ids/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-debug-actors-from-ids/blob/main/LICENSE)

A Datasette plugin for debugging the [new actors_from_ids plugin hook](https://github.com/simonw/datasette/issues/2180).

## Installation

```bash
datasette install datasette-debug-actors-from-ids
```

## Usage

Adds a URL at `/-/debug-actors-from-ids`. Call it with `?ids=1,3,4` to exercise the plugin hook.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-debug-actors-from-ids
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```
pip install -e '.[test]'
```
```
To run the tests:
```bash
pytest
```
