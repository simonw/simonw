# datasette-query-links

[![PyPI](https://img.shields.io/pypi/v/datasette-query-links.svg)](https://pypi.org/project/datasette-query-links/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-query-links?include_prereleases&label=changelog)](https://github.com/simonw/datasette-query-links/releases)
[![Tests](https://github.com/simonw/datasette-query-links/workflows/Test/badge.svg)](https://github.com/simonw/datasette-query-links/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-query-links/blob/main/LICENSE)

Turn SELECT queries returned by a query into links to execute them

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-query-links

## Usage

This is an experimental plugin, requiring Datasette  0.59a1 or higher.

Any SQL query that returns a value that itself looks like a valid SQL query will be converted into a link to execute that SQL query when it is displayed in the Datasette interface.

These links will only show for valid SQL query - if a SQL query would return an error it will not be turned into a link.

## Demo

* [Here's an example query](https://latest-with-plugins.datasette.io/fixtures?sql=select%0D%0A++%27select+*+from+%5Bfacetable%5D%27+as+query%0D%0Aunion%0D%0Aselect%0D%0A++%27select+sqlite_version()%27%0D%0Aunion%0D%0Aselect%0D%0A++%27select+this+is+invalid+SQL+so+will+not+be+linked%27) showing the plugin in action.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-query-links
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
