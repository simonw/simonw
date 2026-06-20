# sqlite-migrate

[![PyPI](https://img.shields.io/pypi/v/sqlite-migrate.svg)](https://pypi.org/project/sqlite-migrate/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-migrate?include_prereleases&label=changelog)](https://sqlite-migrate.datasette.io/en/stable/changelog.html)
[![Tests](https://github.com/simonw/sqlite-migrate/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-migrate/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-migrate/blob/main/LICENSE)

A simple database migration system for SQLite, based on [sqlite-utils](https://sqlite-utils.datasette.io/).

**This project is an early alpha. Expect breaking changes.**

## Installation

This tool works as a plugin for `sqlite-utils`. First [install that](https://sqlite-utils.datasette.io/en/stable/installation.html):

```bash
pip install sqlite-utils
```
Then install this plugin like so:
```bash
sqlite-utils install sqlite-migrate
```
## Migration files

This tool works against migration files. A migration file looks like this:

```python
from sqlite_migrate import Migrations

# Pick a unique name here - it must not clash with other migration sets that
# the user might run against the same database.

migration = Migrations("creatures")

# Use this decorator against functions that implement migrations
@migration()
def create_table(db):
    # db is a sqlite-utils Database instance
    db["creatures"].create(
        {"id": int, "name": str, "species": str},
        pk="id"
    )

@migration()
def add_weight(db):
    # db is a sqlite-utils Database instance
    db["creatures"].add_column("weight", float)
```
Here is [documentation on the Database instance](https://sqlite-utils.datasette.io/en/stable/python-api.html) passed to each migration function.

## Running migrations

Running this command will execute those migrations in sequence against the specified database file.

Call `migrate` with a path to your database and a path to the migrations file you want to apply:
```bash
sqlite-utils migrate creatures.db path/to/migrations.py
```
Running this multiple times will have no additional affect, unless you add more migration functions to the file.

If you call it without arguments it will search for and apply any `migrations.py` files in the current directory or any of its subdirectories.

You can also pass the path to a directory, in which case all `migrations.py` files in that directory and its subdirectories will be applied:

```bash
sqlite-utils migrate creatures.db path/to/parent/
```
When applying a single migrations file you can use the `--stop-before` option to apply all migrations up to but excluding the specified migration:

```bash
sqlite-utils migrate creatures.db path/to/migrations.py --stop-before add_weight
```

## Listing migrations

Add `--list` to list migrations without running them, for example:

```bash
sqlite-utils migrate creatures.db --list
```
The output will look something like this:
```
Migrations for: creatures

  Applied:
    create_table - 2023-07-23 04:09:40.324002
    add_weight - 2023-07-23 04:09:40.324649
    add_age - 2023-07-23 04:09:44.441616
    cleanup_columns - 2023-07-23 04:09:44.443394

  Pending:
    drop_table
```

## Verbose mode

Add `-v` or `--verbose` for verbose output, which will show the schema before and after the migrations were applied along with a diff:

```bash
sqlite-utils migrate creatures.db --verbose
```
Example output:

<!-- [[[cog
import cog
from sqlite_utils.cli import cli
import sqlite_utils
import textwrap
from click.testing import CliRunner
runner = CliRunner()
with runner.isolated_filesystem():
    # First migration creates the table
    open("migrations.py", "w").write(textwrap.dedent("""
    from sqlite_migrate import Migrations
    migration = Migrations("demo")
    @migration()
    def create_table(db):
        db["creatures"].create(
            {"id": int, "name": str, "species": str, "weight": float},
            pk="id",
        )
    """))
    runner.invoke(cli, ["migrate", "creatures.db"])
    # Second migration adds some columns
    open("migrations.py", "a").write("\n\n" + textwrap.dedent("""
    @migration()
    def add_columns(db):
        db["creatures"].add_column("age", int)
        db["creatures"].add_column("shoe_size", int)
        db["creatures"].transform()
    """))
    result = runner.invoke(cli, ["migrate", "creatures.db", "--verbose"])
cog.out(
    "```\n{}\n```".format(result.output.strip())
)
]]] -->
```
Migrating creatures.db

Schema before:

  CREATE TABLE [_sqlite_migrations] (
     [id] INTEGER PRIMARY KEY,
     [migration_set] TEXT,
     [name] TEXT,
     [applied_at] TEXT
  );
  CREATE UNIQUE INDEX [idx__sqlite_migrations_migration_set_name]
      ON [_sqlite_migrations] ([migration_set], [name]);
  CREATE TABLE [creatures] (
     [id] INTEGER PRIMARY KEY,
     [name] TEXT,
     [species] TEXT,
     [weight] FLOAT
  );

Schema after:

  CREATE TABLE [_sqlite_migrations] (
     [id] INTEGER PRIMARY KEY,
     [migration_set] TEXT,
     [name] TEXT,
     [applied_at] TEXT
  );
  CREATE UNIQUE INDEX [idx__sqlite_migrations_migration_set_name]
      ON [_sqlite_migrations] ([migration_set], [name]);
  CREATE TABLE "creatures" (
     [id] INTEGER PRIMARY KEY,
     [name] TEXT,
     [species] TEXT,
     [weight] FLOAT,
     [age] INTEGER,
     [shoe_size] INTEGER
  );

Schema diff:

 );
 CREATE UNIQUE INDEX [idx__sqlite_migrations_migration_set_name]
     ON [_sqlite_migrations] ([migration_set], [name]);
-CREATE TABLE [creatures] (
+CREATE TABLE "creatures" (
    [id] INTEGER PRIMARY KEY,
    [name] TEXT,
    [species] TEXT,
-   [weight] FLOAT
+   [weight] FLOAT,
+   [age] INTEGER,
+   [shoe_size] INTEGER
 );
```
<!-- [[[end]]] -->
