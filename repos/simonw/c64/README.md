# c64

[![PyPI](https://img.shields.io/pypi/v/c64.svg)](https://pypi.org/project/c64/)
[![Changelog](https://img.shields.io/github/v/release/simonw/c64?include_prereleases&label=changelog)](https://github.com/simonw/c64/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/c64/blob/main/LICENSE)

Experimental package of ASGI utilities extracted from Datasette

This library is an **experimental alpha**. I have not yet committed to maintaining this in the long-term, so you should not use this for any projects.

## Installation

Install this library using `pip`:

    $ pip install c64

## Usage

The library provides `Request` and `Response` classes, which currently match the documented classes of the same name in Datasette, see [Datasette internals documentation](https://docs.datasette.io/en/stable/internals.html).

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd c64
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
