# datasette-backup

[![PyPI](https://img.shields.io/pypi/v/datasette-backup.svg)](https://pypi.org/project/datasette-backup/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-backup?include_prereleases&label=changelog)](https://github.com/simonw/datasette-backup/releases)
[![Tests](https://github.com/simonw/datasette-backup/workflows/Test/badge.svg)](https://github.com/simonw/datasette-backup/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-backup/blob/main/LICENSE)

Plugin adding backup options to Datasette

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-backup

## Usage

Once installed, you can download a SQL backup of any of your databases from:

    /-/backup/dbname.sql

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-backup
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
