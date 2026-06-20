# datasette-saved-queries

[![PyPI](https://img.shields.io/pypi/v/datasette-saved-queries.svg)](https://pypi.org/project/datasette-saved-queries/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-saved-queries?label=changelog)](https://github.com/simonw/datasette-saved-queries/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-saved-queries/blob/master/LICENSE)

Datasette plugin that lets users save and execute queries

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-saved-queries

## Usage

When the plugin is installed Datasette will automatically create a `saved_queries` table in the first connected database when it starts up.

It also creates a `save_query` writable canned query which you can use to save new queries.

Queries that you save will be added to the query list on the database page.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-saved-queries
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
