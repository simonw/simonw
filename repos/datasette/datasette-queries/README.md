# datasette-queries

[![PyPI](https://img.shields.io/pypi/v/datasette-queries.svg)](https://pypi.org/project/datasette-queries/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-queries?include_prereleases&label=changelog)](https://github.com/datasette/datasette-queries/releases)
[![Tests](https://github.com/datasette/datasette-queries/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-queries/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-queries/blob/main/LICENSE)

Save SQL queries in Datasette

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-queries
```
## Usage

Users with the `datasette-queries` permission will see a new UI element on the results of a SQL query inviting them to save that query.

Saved queries (treated as [canned queries](https://docs.datasette.io/en/stable/sql_queries.html#canned-queries)) are then shown as a list on the database page.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-queries
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
