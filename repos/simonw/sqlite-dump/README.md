# sqlite-dump

[![PyPI](https://img.shields.io/pypi/v/sqlite-dump.svg)](https://pypi.org/project/sqlite-dump/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-dump?label=changelog)](https://github.com/simonw/sqlite-dump/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-dump/blob/master/LICENSE)

An improved version of `.iterdump()` for Python's `sqlite3`

## Background

Python's `sqlite3` standard library module provides a method for dumping the contents of a database out as lines of SQL that can be used to recreate the database:

```python
import sqlite3

conn = sqlite3.connect("mydb.db")
for line in conn.iterdump():
    print(line)
```

This mechanism is convenient but unfortunately does not support every SQLite feature. In particular it doesn't correctly dump databases that use SQLite's full-text search functionality from the [FTS module](https://www.sqlite.org/fts5.html). This library offers an improved alternative to the `.iterdump()` method.

## Installation

Install this plugin using `pip`:

    $ pip install sqlite-dump

## Usage

To loop through lines of SQL that can recreate a SQLite database file:

```python
import sqlite3
from sqlite_dump import iterdump

conn = sqlite3.connect(db_path)
for line in iterdump(conn):
    print(line)
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd sqlite-dump
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
