# datasette-plugin-demos

[![PyPI](https://img.shields.io/pypi/v/datasette-plugin-demos.svg)](https://pypi.org/project/datasette-plugin-demos/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-plugin-demos?label=changelog)](https://github.com/simonw/datasette-plugin-demos/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-plugin-demos/blob/master/LICENSE)

Examples of plugins for Datasette

This repository hosts an example showing how Datasette plugins can be structured and packaged.

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-plugin-demos

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-plugin-demos
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
