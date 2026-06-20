# datasette-sandstorm-support

[![PyPI](https://img.shields.io/pypi/v/datasette-sandstorm-support.svg)](https://pypi.org/project/datasette-sandstorm-support/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-sandstorm-support?include_prereleases&label=changelog)](https://github.com/simonw/datasette-sandstorm-support/releases)
[![Tests](https://github.com/simonw/datasette-sandstorm-support/workflows/Test/badge.svg)](https://github.com/simonw/datasette-sandstorm-support/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-sandstorm-support/blob/main/LICENSE)

Authentication and permissions for Datasette on Sandstorm

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-sandstorm-support

## Usage

This plugin is part of [datasette-sandstorm](https://github.com/ocdtrekkie/datasette-sandstorm).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-sandstorm-support
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
