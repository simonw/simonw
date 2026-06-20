# sqlite-utils-shell

[![PyPI](https://img.shields.io/pypi/v/sqlite-utils-shell.svg)](https://pypi.org/project/sqlite-utils-shell/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-utils-shell?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-utils-shell/releases)
[![Tests](https://github.com/simonw/sqlite-utils-shell/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-utils-shell/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-utils-shell/blob/main/LICENSE)

An interactive shell for [sqlite-utils](https://sqlite-utils.datasette.io/)

**Alternative**: [sqlite-utils-litecli](https://github.com/simonw/sqlite-utils-litecli) is similar to this but better, because it includes full autocompletion against table and column names.

## Installation

Install this plugin in the same environment as sqlite-utils.
```bash
sqlite-utils install sqlite-utils-shell
```

## Usage

To start a new interactive shell session against a database:
```bash
sqlite-utils shell data.db
```
Type `quit` or `exit` to end the session.

Omit the filename to run against an in-memory database.

To load additional SQLite extensions pass their paths as one or more `--load-extension` arguments:
```bash
sqlite-utils shell data.db \
  --load-extension /path/to/extension.so
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd sqlite-utils-shell
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
