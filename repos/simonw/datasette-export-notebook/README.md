# datasette-export-notebook

[![PyPI](https://img.shields.io/pypi/v/datasette-export-notebook.svg)](https://pypi.org/project/datasette-export-notebook/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-export-notebook?include_prereleases&label=changelog)](https://github.com/simonw/datasette-export-notebook/releases)
[![Tests](https://github.com/simonw/datasette-export-notebook/workflows/Test/badge.svg)](https://github.com/simonw/datasette-export-notebook/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-export-notebook/blob/main/LICENSE)

Datasette plugin providing instructions for exporting data to a [Jupyter](https://jupyter.org/) or [Observable](https://observablehq.com/) notebook.

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-export-notebook

## Usage

Once installed, the plugin will add a `.Notebook` export option to every table and query. Clicking on this link will show instructions for exporting the data to Jupyter or Observable.

## Demo

You can see this plugin in action on the [latest-with-plugins.datasette.io](https://latest-with-plugins.datasette.io/) Datasette instance - for example on [/github/commits.Notebook](https://latest-with-plugins.datasette.io/github/commits.Notebook).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-export-notebook
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
