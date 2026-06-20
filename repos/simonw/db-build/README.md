# db-build

[![PyPI](https://img.shields.io/pypi/v/db-build.svg)](https://pypi.org/project/db-build/)
[![Changelog](https://img.shields.io/github/v/release/simonw/db-build?include_prereleases&label=changelog)](https://github.com/simonw/db-build/releases)
[![Tests](https://github.com/simonw/db-build/workflows/Test/badge.svg)](https://github.com/simonw/db-build/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/db-build/blob/main/LICENSE)

Tools for building SQLite databases from files and directories

## Installation

Install using `pip` or `pipx`:
```bash
pip install db-build
```
If you have `sqlite-utils` installed as well, this will act as a plugin and add a `sqlite-utils build` command.

## Usage

`db-build` can build databases from a number of different flat file formats.

It is always called with a SQLite database as the first argument, which can be a file that does not exist yet.

Any subsequent arguments will be treated as files or directories that should be loaded into that database.

A simple initial example, adding all CSV files in the current directory:

```bash
db-build data.db *.csv
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd db-build
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
