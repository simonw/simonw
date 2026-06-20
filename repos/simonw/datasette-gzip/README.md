# datasette-gzip

[![PyPI](https://img.shields.io/pypi/v/datasette-gzip.svg)](https://pypi.org/project/datasette-gzip/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-gzip?include_prereleases&label=changelog)](https://github.com/simonw/datasette-gzip/releases)
[![Tests](https://github.com/simonw/datasette-gzip/workflows/Test/badge.svg)](https://github.com/simonw/datasette-gzip/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-gzip/blob/main/LICENSE)

Add gzip compression to Datasette

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-gzip

## Usage

Once installed, Datasette will obey the `Accept-Encoding:` header sent by browsers or other user agents and return content compressed in the most appropriate way.

This plugin is a thin wrapper for the [asgi-gzip library](https://github.com/simonw/asgi-gzip), which extracts the [GzipMiddleware](https://www.starlette.io/middleware/#gzipmiddleware) from Starlette.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-gzip
    python3 -mvenv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
