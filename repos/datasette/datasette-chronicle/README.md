# datasette-chronicle

[![PyPI](https://img.shields.io/pypi/v/datasette-chronicle.svg)](https://pypi.org/project/datasette-chronicle/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-chronicle?include_prereleases&label=changelog)](https://github.com/datasette/datasette-chronicle/releases)
[![Tests](https://github.com/datasette/datasette-chronicle/workflows/Test/badge.svg)](https://github.com/datasette/datasette-chronicle/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-chronicle/blob/main/LICENSE)

Use [sqlite-chronicle](https://github.com/simonw/sqlite-chronicle) with tables in Datasette

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-chronicle
```
## Usage

Once installed, users with the `enable-chronicle` and `disable-chronicle` permissions (granted to the `root` user by default) will have access to new table action menu options for enabling and disabling row version tracking for a table.

Tables that have had row version tracking enabled will now support a new `?_since=X` query string parameter on the table page, which will filter for just rows that have been inserted or updated since the specified chronicle version.

See the [sqlite-chronicle documentation](https://github.com/simonw/sqlite-chronicle/blob/main/README.md) for more details on what this is and how it works.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-chronicle
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
