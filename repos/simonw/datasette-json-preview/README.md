# datasette-json-preview

[![PyPI](https://img.shields.io/pypi/v/datasette-json-preview.svg)](https://pypi.org/project/datasette-json-preview/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-json-preview?include_prereleases&label=changelog)](https://github.com/simonw/datasette-json-preview/releases)
[![Tests](https://github.com/simonw/datasette-json-preview/workflows/Test/badge.svg)](https://github.com/simonw/datasette-json-preview/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-json-preview/blob/main/LICENSE)

Preview of new JSON default format for Datasette, see [issue #782](https://github.com/simonw/datasette/issues/782)

This plugin will continue to change while the new output format is explored.

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-json-preview

## Usage

Use the `.json-preview` extension to preview the new JSON API design.

## Demos

- https://latest-with-plugins.datasette.io/github/commits.json-preview
- https://latest-with-plugins.datasette.io/github/commits.json-preview?_extra=next_url
- https://latest-with-plugins.datasette.io/github/commits.json-preview?_extra=total
- https://latest-with-plugins.datasette.io/github/commits.json-preview?_extra=next_url&_extra=total
- https://latest-with-plugins.datasette.io/github/commits.json-preview?_extra=total&_size=0

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-json-preview
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
