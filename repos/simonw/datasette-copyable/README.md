# datasette-copyable

[![PyPI](https://img.shields.io/pypi/v/datasette-copyable.svg)](https://pypi.org/project/datasette-copyable/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-copyable?include_prereleases&label=changelog)](https://github.com/simonw/datasette-copyable/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-copyable/blob/master/LICENSE)

Datasette plugin for outputting tables in formats suitable for copy and paste

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-copyable

## Demo

You can try this plugin in [Datasette Lite](https://lite.datasette.io/?install=datasette-copyable#/content/stats.copyable) - that link installs the plugin and shows the copyable interface for an example table. Browse for other tables or queries there and look for the "copyable" link.

## Usage

This plugin adds a `.copyable` output extension to every table, view and query.

Navigating to this page will show an interface allowing you to select a format for copying and pasting the demo. The default is TSV, which is suitable for copying into Google Sheets or Excel.

You can add `?_raw=1` to get back just the raw data.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-copyable
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
