# sqlite-utils-fast-fks

[![PyPI](https://img.shields.io/pypi/v/sqlite-utils-fast-fks.svg)](https://pypi.org/project/sqlite-utils-fast-fks/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-utils-fast-fks?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-utils-fast-fks/releases)
[![Tests](https://github.com/simonw/sqlite-utils-fast-fks/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-utils-fast-fks/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-utils-fast-fks/blob/main/LICENSE)

Fast foreign key addition for [sqlite-utils](https://sqlite-utils.datasette.io/).

## Background

SQLite does not yet have a built-in method for adding foreign key constraints to an existing table.

There are two workarounds for this limitation:

1. You can create brand new table with the new foreign keys, copy the data across, then drop the old table and rename the new one. This method is implemented by the [sqlite-utils table.transform() method](https://sqlite-utils.datasette.io/en/stable/python-api.html#transforming-a-table).
2. You can set `PRAGMA writable_schema = 1`, then directly modify the schema stored in the `sqlite_master` table for that table. Then increment the `schema_version`, set `writable_schema = 0` again and run a vacuum against the database.

For tables with large numbers of rows that second option is a lot faster, as you don't need to create an entirely new copy of all of the data.

Prior to version 3.35 [sqlite-utils](https://sqlite-utils.datasette.io/) implemented the latter pattern as part of its `table.add_foreign_key()` and `db.add_foreign_keys()` methods. 

It turned out these caused `table sqlite_master may not be modified` errors on some Python installations, primarily on macOS where the ability to modify the `sqlite_master` table is sometimes disabled by default.

This plugin brings the same functionality back again. You can use this if you want fast foreign key addition and you know that your platform does not suffer from the `table sqlite_master may not be modified` error.

## Installation

Install this plugin in the same environment as sqlite-utils.
```bash
sqlite-utils install sqlite-utils-fast-fks
```
Or install using `pip`:
```bash
pip install sqlite-utils-fast-fks
```

## Python library

To add foreign keys in Python code, use the `add_foreign_keys(db, foreign_keys)` function. Here's an example:
```python
from sqlite_utils_fast_fks import add_foreign_keys
from sqlite_utils import Database

db = Database("my_database.db")
db["country"].insert_all([{"id": 1, "name": "United Kingdom"}])
db["continent"].insert_all([{"id": 1, "name": "Europe"}])
db["places"].insert(
    {
        "id": 1,
        "name": "London",
        "country_id": 1,
        "continent_id": 1,
    }
)

# Now modify that places table to have two foreign keys:
add_foreign_keys(
    db,
    [
        ("places", "country_id", "country", "id"),
        ("places", "continent_id", "continent", "id"),
    ],
)
```
The `foreign_keys` argument is a list of tuples, each containing four values:

- The table to add the foreign key to
- The column in that table that will be a foreign key
- The other table that the column should reference
- The column in that other table that should be referenced

## Command-line tool

When installed as a [sqlite-utils plugin](https://sqlite-utils.datasette.io/en/stable/plugins.html), this library adds a new `sqlite-utils fast-fks` command. It can be used like this:

```bash
sqlite-utils fast-fks my_database.db places country_id country id
```
The command takes a path to a database, then the table name, the column name, the other table name and the other column name.

You can specify multiple foreign keys to add at once by repeating the last four arguments:

```bash
sqlite-utils fast-fks my_database.db \
    places country_id country id \
    places continent_id continent id
```
## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd sqlite-utils-fast-fks
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
