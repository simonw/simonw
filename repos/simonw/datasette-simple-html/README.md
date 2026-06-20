# datasette-simple-html

[![PyPI](https://img.shields.io/pypi/v/datasette-simple-html.svg)](https://pypi.org/project/datasette-simple-html/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-simple-html?include_prereleases&label=changelog)](https://github.com/simonw/datasette-simple-html/releases)
[![Tests](https://github.com/simonw/datasette-simple-html/workflows/Test/badge.svg)](https://github.com/simonw/datasette-simple-html/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-simple-html/blob/main/LICENSE)

Datasette SQL functions for very simple HTML operations

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-simple-html

## Usage

This plugin provides the following SQL functions:

### html_strip_tags(text)

Returns the text with any `<...>` tags removed.

### html_escape(text)

Escapes any HTML special characters in the text, e.g. `>` becomes `&gt;`. Uses [html.escape(text, quote=True)](https://docs.python.org/3/library/html.html#html.escape) from the Python standard library.

### html_unescape(text)

Unescapes any HTML special characters, so `&gt;` becomes `>`. Also handles numeric entities, so `&#x27;` becomes `'`. Uses [html.unescape(text)](https://docs.python.org/3/library/html.html#html.unescape) from the Python standard library.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-simple-html
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
