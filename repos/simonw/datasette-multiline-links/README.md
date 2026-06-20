# datasette-multiline-links

[![PyPI](https://img.shields.io/pypi/v/datasette-multiline-links.svg)](https://pypi.org/project/datasette-multiline-links/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-multiline-links?include_prereleases&label=changelog)](https://github.com/simonw/datasette-multiline-links/releases)
[![Tests](https://github.com/simonw/datasette-multiline-links/workflows/Test/badge.svg)](https://github.com/simonw/datasette-multiline-links/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-multiline-links/blob/main/LICENSE)

Make multiple newline separated URLs clickable in Datasette

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-multiline-links

## Demo

Try this plugin out against a [Google Sheets spreadsheet](https://docs.google.com/spreadsheets/d/1wZhPLMCHKJvwOkP4juclhjFgqIY8fQFMemwKL2c64vk) of previously featured datasets from [Data is Plural](https://www.data-is-plural.com/) using [Datasette Lite](https://lite.datasette.io/) here:

* <a href="https://lite.datasette.io/?install=datasette-multiline-links&csv=https://docs.google.com/spreadsheets/d/1wZhPLMCHKJvwOkP4juclhjFgqIY8fQFMemwKL2c64vk/export?format=csv#/data?sql=select+edition%2C+headline%2C+text%2C+links%2C+hattips+from+export+where%0Atext+like+'%25'+||+%3Aq+||+'%25'+or+headline+like+'%25'+||+%3Aq+||+'%25'+order+by+edition+desc&q=loans">Demo this plugin in Datasette Lite</a>

## Usage

Once installed, if a cell has contents like this:
```
https://example.com
Not a link
https://google.com
```
It will be rendered as:
```html
<a href="https://example.com">https://example.com</a>
Not a link
<a href="https://google.com">https://google.com</a>
```
## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-multiline-links
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
