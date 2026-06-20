# datasette-column-sum

[![PyPI](https://img.shields.io/pypi/v/datasette-column-sum.svg)](https://pypi.org/project/datasette-column-sum/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-column-sum?include_prereleases&label=changelog)](https://github.com/datasette/datasette-column-sum/releases)
[![Tests](https://github.com/datasette/datasette-column-sum/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-column-sum/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-column-sum/blob/main/LICENSE)

Sum the values in numeric Datasette columns

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-column-sum
```
## Usage

Numeric columns (float and integer) will have a new "Sum this column" menu item in their column action menu (accessible via the cog icon).

Text columns get options to calculate sums for those numeric columns grouped by the text column.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-column-sum
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
