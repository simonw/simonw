# sqlite-utils-litecli

[![PyPI](https://img.shields.io/pypi/v/sqlite-utils-litecli.svg)](https://pypi.org/project/sqlite-utils-litecli/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-utils-litecli?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-utils-litecli/releases)
[![Tests](https://github.com/simonw/sqlite-utils-litecli/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-utils-litecli/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-utils-litecli/blob/main/LICENSE)

Interactive shell for [sqlite-utils](https://sqlite-utils.datasette.io/) using [litecli](https://github.com/dbcli/litecli).

## Installation

Install this plugin in the same environment as `sqlite-utils`.
```bash
sqlite-utils install sqlite-utils-litecli
```

## Usage

Start running the shell like this:
```bash
sqlite-utils litecli data.db
```
This will start a `litecli` interactive shell session.

Custom SQL functions provided by other plugins will be available in the shell.

<img src="https://raw.githubusercontent.com/simonw/sqlite-utils-litecli/main/screenshot.jpg" width="483" alt="Screenshot showing the plugin in action - it includes autocomplete of SQLite table names">

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd sqlite-utils-litecli
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
