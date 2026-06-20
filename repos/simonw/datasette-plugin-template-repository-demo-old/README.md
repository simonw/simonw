# datasette-plugin-template-repository-demo

[![PyPI](https://img.shields.io/pypi/v/datasette-plugin-template-repository-demo.svg)](https://pypi.org/project/datasette-plugin-template-repository-demo/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-plugin-template-repository-demo?include_prereleases&label=changelog)](https://github.com/simonw/datasette-plugin-template-repository-demo/releases)
[![Tests](https://github.com/simonw/datasette-plugin-template-repository-demo/workflows/Test/badge.svg)](https://github.com/simonw/datasette-plugin-template-repository-demo/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-plugin-template-repository-demo/blob/main/LICENSE)

Demo of simonw/datasette-plugin-template-repository

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-plugin-template-repository-demo

## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-plugin-template-repository-demo
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
