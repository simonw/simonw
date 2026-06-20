# datasette-tail

[![PyPI](https://img.shields.io/pypi/v/datasette-tail.svg)](https://pypi.org/project/datasette-tail/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-tail?include_prereleases&label=changelog)](https://github.com/datasette/datasette-tail/releases)
[![Tests](https://github.com/datasette/datasette-tail/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-tail/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-tail/blob/main/LICENSE)

Tools for tailing your database

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-tail
```
## Usage

This plugin provides a simple debugging tool. Visit `/dbname/-/tail` to see a JSON representation of changes to your database. The first time you visit that page it will represent everything in the specified database. Refreshing the page will show any changes since the last time you loaded that page.

Use `/dbname/-/tail.json` to get the raw JSON.

The plugin obeys the `view-database` permission.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-tail
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
