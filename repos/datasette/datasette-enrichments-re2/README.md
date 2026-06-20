# datasette-enrichments-re2

[![PyPI](https://img.shields.io/pypi/v/datasette-enrichments-re2.svg)](https://pypi.org/project/datasette-enrichments-re2/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-enrichments-re2?include_prereleases&label=changelog)](https://github.com/datasette/datasette-enrichments-re2/releases)
[![Tests](https://github.com/datasette/datasette-enrichments-re2/workflows/Test/badge.svg)](https://github.com/datasette/datasette-enrichments-re2/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-enrichments-re2/blob/main/LICENSE)

Enrich data using regular expressions

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-enrichments-re2
```
## Usage

This enrichment allows you to run a regular expression against a column and perform one of the following:

- Execute a search and replace against that column
- Extract the first matching result and store that in the specified column (adding a column if necessary)
- Extract all matching results and store them as a JSON array in the specified column. If the regular expression uses named capture groups this will be an array of objects, otherwise it will be an array of strings.
- Execute a regular expression with named capture groups and store the results in multiple columns, one for each of those named groups

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-enrichments-re2
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
