# datasette-template-request

[![PyPI](https://img.shields.io/pypi/v/datasette-template-request.svg)](https://pypi.org/project/datasette-template-request/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-template-request?include_prereleases&label=changelog)](https://github.com/simonw/datasette-template-request/releases)
[![Tests](https://github.com/simonw/datasette-template-request/workflows/Test/badge.svg)](https://github.com/simonw/datasette-template-request/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-template-request/blob/main/LICENSE)

Expose the Datasette request object to custom templates

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-template-request

## Usage

Once this plugin is installed, Datasette [custom templates](https://docs.datasette.io/en/stable/custom_templates.html) can use `{{ request }}` to access the current [request object](https://docs.datasette.io/en/stable/internals.html#request-object). For example, to access `?name=Cleo` in the query string a template could use this:

    Name: {{ request.args.name }}

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-template-request
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
