# datasette-enrichments-slow

[![PyPI](https://img.shields.io/pypi/v/datasette-enrichments-slow.svg)](https://pypi.org/project/datasette-enrichments-slow/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-enrichments-slow?include_prereleases&label=changelog)](https://github.com/datasette/datasette-enrichments-slow/releases)
[![Tests](https://github.com/datasette/datasette-enrichments-slow/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-enrichments-slow/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-enrichments-slow/blob/main/LICENSE)

An enrichment on a slow loop to help debug progress bars

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-enrichments-slow
```
## Usage

Select a table (or rows from a table) and run the enrichment. You can specify how many seconds to sleep for each row.

No changes will be recorded to your table. This plugin is for debugging purposes only.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-enrichments-slow
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
