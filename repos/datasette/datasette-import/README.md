# datasette-import

[![PyPI](https://img.shields.io/pypi/v/datasette-import.svg)](https://pypi.org/project/datasette-import/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-import?include_prereleases&label=changelog)](https://github.com/datasette/datasette-import/releases)
[![Tests](https://github.com/datasette/datasette-import/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-import/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-import/blob/main/LICENSE)

Tools for importing data into Datasette

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-import
```
## Usage

This plugin adds a database action item called "Create table with imported data".

This action is available to users with the `create-table` permission.

It links to a page that allows users to upload files or paste in CSV, TSV or JSON data, and then use that to create and populate a new table in Datasette.

CSV and TSV data must have headers on the first row.

JSON data must be an array of objects with the same keys, or a container object object where one of the keys is an array of objects.

## Credits

The CSV and TSV parsing is performed using [Papa Parse](https://www.papaparse.com/), an MIT licensed JavaScript library that is bundled with this plugin.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-import
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
