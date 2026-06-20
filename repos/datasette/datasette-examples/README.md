# datasette-examples

[![PyPI](https://img.shields.io/pypi/v/datasette-examples.svg)](https://pypi.org/project/datasette-examples/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-examples?include_prereleases&label=changelog)](https://github.com/datasette/datasette-examples/releases)
[![Tests](https://github.com/datasette/datasette-examples/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-examples/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-examples/blob/main/LICENSE)

Load example SQL scripts into Datasette on startup

## Installation

Install this plugin in the same environment as Datasette.

```bash
pip install datasette-examples
```

## Usage

This plugin is configured using `metadata.yaml` (or `metadata.json` or `datasette.yml` in Datasette 1.0). 

### Loading example SQL

Add a block like this that specifies the example SQL scripts you would like to load:

```yaml
plugins:
  datasette-examples:
    startup:
      examples:
      - url: https://example.com/path/to/example1.sql
        if_not_table: table_name_1
      - url: https://example.com/path/to/example2.sql
        if_not_table: table_name_2
```

When Datasette starts running, it will:

1. Check if the specified table (`if_not_table`) exists in the `examples.db` database
2. If the table doesn't exist, it will download the SQL file from the provided URL
3. Execute the SQL against `examples.db`

The `if_not_table` should be set to a table that is created by the script, to prevent the script from executing more than once.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-examples
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
