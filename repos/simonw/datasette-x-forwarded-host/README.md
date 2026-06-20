# datasette-x-forwarded-host

[![PyPI](https://img.shields.io/pypi/v/datasette-x-forwarded-host.svg)](https://pypi.org/project/datasette-x-forwarded-host/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-x-forwarded-host?include_prereleases&label=changelog)](https://github.com/simonw/datasette-x-forwarded-host/releases)
[![Tests](https://github.com/simonw/datasette-x-forwarded-host/workflows/Test/badge.svg)](https://github.com/simonw/datasette-x-forwarded-host/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-x-forwarded-host/blob/main/LICENSE)

Treat the X-Forwarded-Host header as the Host header

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-x-forwarded-host

## Usage

Once installed, Datasette will replace the `host` header with the content of the incoming `x-forwarded-host` header.

This helps Datasette generate links to new pages that work when hosted behind a proxy that rewrites the `host` header.

Only use this plugin in deployment environmens where you know the `x-forwarded-host` header can be trusted!

This has been tested on [GitHub Codespaces](https://github.com/features/codespaces) and [GitPod](https://gitpod.io/).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-x-forwarded-host
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
