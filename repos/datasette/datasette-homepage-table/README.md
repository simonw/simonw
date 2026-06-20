# datasette-homepage-table

[![PyPI](https://img.shields.io/pypi/v/datasette-homepage-table.svg)](https://pypi.org/project/datasette-homepage-table/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-homepage-table?include_prereleases&label=changelog)](https://github.com/datasette/datasette-homepage-table/releases)
[![Tests](https://github.com/datasette/datasette-homepage-table/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-homepage-table/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-homepage-table/blob/main/LICENSE)

Show a specific Datasette table on the homepage

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-homepage-table
```
## Usage

This plugin changes the Datasette homepage to display a table instead of the default list of databases.

Without configuration, it will take the first table in the first attached database.

Alternatively you can configure it like this:

```json
{
    "plugins": {
        "datasette-homepage-table": {
            "database": "mydatabase",
            "table": "mytable"
        }
    }
}
```
Both keys are optional: if you omit `database` it will use the first attached database, and if you omit `table` it will use the first table in the database.

You can customize the `table.html` template to [change the appearance of the table](https://docs.datasette.io/en/stable/custom_templates.html#custom-templates).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-homepage-table
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
