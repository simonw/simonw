# dbf-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/dbf-to-sqlite.svg)](https://pypi.python.org/pypi/dbf-to-sqlite)
[![Travis CI](https://travis-ci.com/simonw/dbf-to-sqlite.svg?branch=master)](https://travis-ci.com/simonw/dbf-to-sqlite)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/dbf-to-sqlite/blob/master/LICENSE)

CLI tool for converting DBF files (dBase, FoxPro etc) to SQLite.

## Installation

    pip install dbf-to-sqlite

## Usage

    $ dbf-to-sqlite --help
    Usage: dbf-to-sqlite [OPTIONS] DBF_PATHS... SQLITE_DB

      Convert DBF files (dBase, FoxPro etc) to SQLite

      https://github.com/simonw/dbf-to-sqlite

    Options:
      --version      Show the version and exit.
      --table TEXT   Table name to use (only valid for single files)
      -v, --verbose  Show what's going on
      --help         Show this message and exit.

Example usage:

    $ dbf-to-sqlite *.DBF database.db

This will create a new SQLite database called `database.db` containing one table for each of the `DBF` files in the current directory.

Looking for DBF files to try this out on? Try downloading the [Himalayan Database](http://himalayandatabase.com/) of all expeditions that have climbed in the Nepal Himalaya.
