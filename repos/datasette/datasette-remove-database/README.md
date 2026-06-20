# datasette-remove-database

[![PyPI](https://img.shields.io/pypi/v/datasette-remove-database.svg)](https://pypi.org/project/datasette-remove-database/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-remove-database?include_prereleases&label=changelog)](https://github.com/datasette/datasette-remove-database/releases)
[![Tests](https://github.com/datasette/datasette-remove-database/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-remove-database/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-remove-database/blob/main/LICENSE)

Remove a database from Datasette

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-remove-database
```
## Usage

Users with the `remove-database` permission will see a new menu item on the database page that allows them to remove the database.

By default databases that are removed from Datasette will still be available on disk.

To also delete the file from disk, add this configuration:
```yaml
plugins:
  datasette-remove-database:
    delete: true
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-remove-database
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
