# datasette-no-truncate

[![PyPI](https://img.shields.io/pypi/v/datasette-no-truncate.svg)](https://pypi.org/project/datasette-no-truncate/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-no-truncate?include_prereleases&label=changelog)](https://github.com/simonw/datasette-no-truncate/releases)
[![Tests](https://github.com/simonw/datasette-no-truncate/workflows/Test/badge.svg)](https://github.com/simonw/datasette-no-truncate/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-no-truncate/blob/main/LICENSE)

Tiny Datasette plugin to disable text truncation in table displays

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-no-truncate

## Usage

Once installed, text values should no longer be truncated when a table is displayed.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-no-truncate
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
