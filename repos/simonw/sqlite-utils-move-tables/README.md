# sqlite-utils-move-tables

[![PyPI](https://img.shields.io/pypi/v/sqlite-utils-move-tables.svg)](https://pypi.org/project/sqlite-utils-move-tables/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-utils-move-tables?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-utils-move-tables/releases)
[![Tests](https://github.com/simonw/sqlite-utils-move-tables/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-utils-move-tables/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-utils-move-tables/blob/main/LICENSE)

Command for sqlite-utils to move tables from one database to another

## Installation

Install this plugin in the same environment as `sqlite-utils`.
```bash
sqlite-utils install sqlite-utils-move-tables
```
## Usage

This plugin adds a single command, `sqlite-utils move-tables`. The command can be used to move one or more tables from one database file to another.
```bash
sqlite-utils move-tables origin.db destination.db tablename
```
You can pass multiple tables to the command to move multiple tables in one go:
```bash
sqlite-utils move-tables origin.db destination.db table1 table2
```
A moved table will have its columns and primary keys recreated and all data copied across to the new database. The original table will then be dropped.

Foreign key constraints, indexes and triggers will not be copied across.

To keep the original table, use `--keep`:

```bash
sqlite-utils move-tables origin.db destination.db tablename --keep
```
The command checks for the existence of all of the tables in the first database, and ensures they do not yet exist in the second database. It will show an error if either of these conditions are not meant.

To ignore that error and fail silently if a table is missing or already created, use `--ignore`.

To over-write and replace a table in the destination database with a name that matches one of the tables to be moved, use `--replace`.

**It is advisable to create a copy of your origin database before running this command!**

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd sqlite-utils-move-tables
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
