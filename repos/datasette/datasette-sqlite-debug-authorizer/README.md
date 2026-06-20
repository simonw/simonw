# datasette-sqlite-debug-authorizer

[![PyPI](https://img.shields.io/pypi/v/datasette-sqlite-debug-authorizer.svg)](https://pypi.org/project/datasette-sqlite-debug-authorizer/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-sqlite-debug-authorizer?include_prereleases&label=changelog)](https://github.com/datasette/datasette-sqlite-debug-authorizer/releases)
[![Tests](https://github.com/datasette/datasette-sqlite-debug-authorizer/workflows/Test/badge.svg)](https://github.com/datasette/datasette-sqlite-debug-authorizer/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-sqlite-debug-authorizer/blob/main/LICENSE)

Debug SQLite authorizer calls

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-sqlite-debug-authorizer

## Usage

Once installed, every SQLite permission check using the `conn.set_authorizer()` API will be logged to standard error.

This is useful for if you want to use that authorizer API to implement your own custom permissions, and need to see what calls are being made to the authorizer.

Example output (it's generally a lot noisier than this) for `select * from sqlite_master`:

```
SQLITE_SELECT: 
SQLITE_READ:  table="sqlite_master" column="type" db_name=main
SQLITE_READ:  table="sqlite_master" column="name" db_name=main
SQLITE_READ:  table="sqlite_master" column="tbl_name" db_name=main
SQLITE_READ:  table="sqlite_master" column="rootpage" db_name=main
SQLITE_READ:  table="sqlite_master" column="sql" db_name=main
```
See [sqlite-authorizer-examples](https://github.com/simonw/sqlite-authorizer-examples) for more detailed documentation on what to expect from these calls.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-sqlite-debug-authorizer
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
