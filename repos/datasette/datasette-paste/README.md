# datasette-paste

[![PyPI](https://img.shields.io/pypi/v/datasette-paste.svg)](https://pypi.org/project/datasette-paste/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-paste?include_prereleases&label=changelog)](https://github.com/datasette/datasette-paste/releases)
[![Tests](https://github.com/datasette/datasette-paste/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-paste/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-paste/blob/main/LICENSE)

Paste data to create tables in Datasette

**This plugin is no longer being developed.** It has been replaced by [datasette-import](https://github.com/datasette/datasette-import).

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-paste
```
## Usage

This plugin adds a database action item called "Create table with pasted data".

This action is available to users with the `create-table` permission.

It links to a page that allows users to paste in CSV, TSV or JSON data, and then use that to create and populate a new table in Datasette.

CSV and TSV data must have headers on the first row.

JSON data must be an array of objects with the same keys, or a container object object where one of the keys is an array of objects.

## Credits

The CSV and TSV parsing is performed using [Papa Parse](https://www.papaparse.com/), an MIT licensed JavaScript library that is bundled with this plugin.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-paste
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
