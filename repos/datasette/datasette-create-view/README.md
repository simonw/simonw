# datasette-create-view

[![PyPI](https://img.shields.io/pypi/v/datasette-create-view.svg)](https://pypi.org/project/datasette-create-view/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-create-view?include_prereleases&label=changelog)](https://github.com/datasette/datasette-create-view/releases)
[![Tests](https://github.com/datasette/datasette-create-view/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-create-view/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-create-view/blob/main/LICENSE)

Create a SQL view from a query

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-create-view
```
This plugin requires [Datasette 1.0a12](https://docs.datasette.io/en/latest/changelog.html#a12-2024-02-29) or later.

## Usage

Users with the `create-table` permission will get a new menu item on the query results page offering to save the query as a view.

This option will only show for SQL queries that do not use `:named` parameters.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-create-view
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
