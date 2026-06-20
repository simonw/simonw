<img src="https://datasette.io/static/datasette-logo.svg" alt="Datasette">

# datasette-hello-world

[![PyPI](https://img.shields.io/pypi/v/datasette-hello-world.svg)](https://pypi.org/project/datasette-hello-world/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-hello-world?include_prereleases&label=changelog)](https://github.com/simonw/datasette-hello-world/releases)
[![Tests](https://github.com/simonw/datasette-hello-world/workflows/Test/badge.svg)](https://github.com/simonw/datasette-hello-world/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-hello-world/blob/main/LICENSE)

The hello world of Datasette plugins

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-hello-world

## Usage

Run this to see "Hello world":

    datasette hello-world

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-hello-world
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
