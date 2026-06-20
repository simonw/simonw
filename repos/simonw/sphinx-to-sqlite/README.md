# sphinx-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/sphinx-to-sqlite.svg)](https://pypi.org/project/sphinx-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sphinx-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/sphinx-to-sqlite/releases)
[![Tests](https://github.com/simonw/sphinx-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/sphinx-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sphinx-to-sqlite/blob/master/LICENSE)

Create a SQLite database from Sphinx documentation.

## Demo

You can see the results of running this tool against the [Datasette documentation](https://docs.datasette.io/) at https://latest-docs.datasette.io/docs/sections

## Installation

Install this tool using `pip`:

    $ pip install sphinx-to-sqlite

## Usage

First run `sphinx-build` with the `-b xml` option to create XML files in your `_build/` directory.

Then run:

    $ sphinx-to-sqlite docs.db path/to/_build

To build the SQLite database.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd sphinx-to-sqlite
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
