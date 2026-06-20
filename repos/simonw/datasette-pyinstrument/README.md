# datasette-pyinstrument

[![PyPI](https://img.shields.io/pypi/v/datasette-pyinstrument.svg)](https://pypi.org/project/datasette-pyinstrument/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-pyinstrument?include_prereleases&label=changelog)](https://github.com/simonw/datasette-pyinstrument/releases)
[![Tests](https://github.com/simonw/datasette-pyinstrument/workflows/Test/badge.svg)](https://github.com/simonw/datasette-pyinstrument/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-pyinstrument/blob/main/LICENSE)

Use pyinstrument to analyze Datasette page performance

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-pyinstrument

## Usage

Once installed, adding `?_pyinstrument=1` to any URL within Datasette will replace the output of that page with the pyinstrument profiler results for it.

## Demo

You can see the output of this plugin at https://latest-with-plugins.datasette.io/fixtures/sortable?_pyinstrument=1

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-pyinstrument
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
