# image-diff

[![PyPI](https://img.shields.io/pypi/v/image-diff.svg)](https://pypi.org/project/image-diff/)
[![Changelog](https://img.shields.io/github/v/release/simonw/image-diff?include_prereleases&label=changelog)](https://github.com/simonw/image-diff/releases)
[![Tests](https://github.com/simonw/image-diff/workflows/Test/badge.svg)](https://github.com/simonw/image-diff/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/image-diff/blob/master/LICENSE)

CLI tool for comparing images

## Installation

Install this tool using `pip`:

    $ pip install image-diff

## Image diff

To generate an image showing the difference between two images:

    image-diff first.jpg second.jpg -o diff.png

## Count differing pixels

To count the number of pixels that have changed, use `image-diff count`:

    image-diff first.jpg second.jpg

This will output a number followed by a newline.

## Compile an image

The `image-diff compile` command exists mainly to make this tool easier to test.

It can be used to compile an image from a JSON definition - for example:

    echo '[
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [255, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ]' | image-diff compile - -o one-pixel.png

## Similar projects

- [pixelmatch](https://github.com/mapbox/pixelmatch) by Mapbox is a JavaScript library with an accompanying CLI tool.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd image-diff
    python -m venv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
