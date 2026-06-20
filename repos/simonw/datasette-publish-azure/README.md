# datasette-publish-azure

[![PyPI](https://img.shields.io/pypi/v/datasette-publish-azure.svg)](https://pypi.org/project/datasette-publish-azure/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-publish-azure?include_prereleases&label=changelog)](https://github.com/simonw/datasette-publish-azure/releases)
[![Tests](https://github.com/simonw/datasette-publish-azure/workflows/Test/badge.svg)](https://github.com/simonw/datasette-publish-azure/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-publish-azure/blob/main/LICENSE)

Publish Datasette instances to Azure Functions

**UNDER CONSTRUCTION**: This plugin does not work yet!

See [simonw/azure-functions-datasette](https://github.com/simonw/azure-functions-datasette) for the prototype.

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-publish-azure

## Usage

Usage instructions will go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-publish-azure
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
