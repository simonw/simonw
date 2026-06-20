# datasette-render-image-tags

[![PyPI](https://img.shields.io/pypi/v/datasette-render-image-tags.svg)](https://pypi.org/project/datasette-render-image-tags/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-render-image-tags?include_prereleases&label=changelog)](https://github.com/simonw/datasette-render-image-tags/releases)
[![Tests](https://github.com/simonw/datasette-render-image-tags/workflows/Test/badge.svg)](https://github.com/simonw/datasette-render-image-tags/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-render-image-tags/blob/main/LICENSE)

Turn any URLs ending in .jpg/.png/.gif into img tags with width 200

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-render-image-tags

## Usage

Once installed, any cells contaning a URL that ends with `.png` or `.jpg` or `.jpeg` or `.gif` will be rendered using an image tag, with a width of 200px.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-render-image-tags
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
