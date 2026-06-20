# sqlite-chronicle

[![PyPI](https://img.shields.io/pypi/v/sqlite-chronicle.svg)](https://pypi.org/project/sqlite-chronicle/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-chronicle?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-chronicle/releases)
[![Tests](https://github.com/simonw/sqlite-chronicle/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-chronicle/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-chronicle/blob/main/LICENSE)

Use triggers to track when rows in a SQLite table were inserted, updated, or deleted

## Core idea

Create a `_chronicle_{table_name}` table to accompany a regular table. Each row in the regular table has a corresponding row in the chronicle table that records timestamps for when it was added or last updated plus an incrementing version number, all maintained using SQLite triggers. This lets you efficiently identify which rows have been added, updated or deleted since a previous timestamp or version.

## Installation

```bash
pip install sqlite-chronicle
```

## Command-line interface

You can enable chronicle for specific tables in a SQLite database using the command-line interface, passing in one or more table names:

```bash
sqlite-chronicle database.db table_1 table_2
```

To disable chronicle tracking, use the `--disable` flag:

```bash
sqlite-chronicle database.db table_1 --disable
```

You can also run this tool without installing it first using [uvx](https://docs.astral.sh/uv/concepts/tools/):

```bash
uvx sqlite-chronicle --help
```

## Python API

This package exposes several Python functions for configuring and using chronicle tables:

### enable_chronicle(conn, table_name)

This module provides a function: `sqlite_chronicle.enable_chronicle(conn, table_name)`, which does the following:

1. Checks if a `_chronicle_{table_name}` table exists already. If so, it does nothing. Otherwise...
2. Creates that table, with the same primary key columns as the original table plus integer columns `__added_ms`, `__updated_ms`, `__version` and `__deleted`
3. Creates a new row in the chronicle table corresponding to every row in the original table, setting `__added_ms` and `__updated_ms` to the current timestamp in milliseconds, and `__version` column that starts at 1 and increments for each subsequent row
4. Sets up four triggers on the table:

  - A BEFORE INSERT trigger, which snapshots existing row data into a helper table to support `INSERT OR REPLACE` change detection
  - An AFTER INSERT trigger, which creates a new row in the chronicle table, sets `__added_ms` and `__updated_ms` to the current time and sets the `__version` to one higher than the current maximum version for that table. For `INSERT OR REPLACE`, it compares against the snapshot to detect whether the data actually changed
  - An AFTER UPDATE trigger, which updates the `__updated_ms` timestamp and increments the `__version` - but only if at least one column in the row has changed
  - An AFTER DELETE trigger, which updates the `__updated_ms`, increments the `__version` and places a `1` in the `deleted` column - but only for real deletes, not the implicit delete inside `INSERT OR REPLACE`

The function will raise a `sqlite_chronicle.ChronicleError` exception if the table does not exist or if it does not have a single or compound primary key, 

Note that the `__version` for a table is a globally incrementing number, so every time it is set it will be set to the current `max(__version)` + 1 for that entire table.

The end result is a chronicle table that looks something like this:

|  id |    __added_ms  | __updated_ms | __version | __deleted |
|-----|---------------|---------|--------|---------|
|  47 | 1694408890954 | 1694408890954 | 2 |      0 |
|  48 | 1694408874863 | 1694408874863 | 3 |      1 |
|   1 | 1694408825192 | 1694408825192 | 4 |      0 |
|   2 | 1694408825192 | 1694408825192 | 5 |      0 |
|   3 | 1694408825192 | 1694408825192 | 6 |      0 |

### disable_chronicle(conn, table_name)

Use `sqlite_chronicle.disable_chronicle(conn, table_name)` to remove chronicle tracking from a table. This will:

1. Drop the `_chronicle_{table_name}` table
2. Remove all associated triggers
3. Remove the version index

Returns `True` if chronicle was disabled, `False` if no chronicle table existed for that table.

```python
import sqlite_chronicle

# Disable chronicle on the dogs table
result = sqlite_chronicle.disable_chronicle(conn, "dogs")
if result:
    print("Chronicle disabled")
else:
    print("No chronicle found")
```

### is_chronicle_enabled(conn, table_name)

Use `sqlite_chronicle.is_chronicle_enabled(conn, table_name)` to check if chronicle tracking is enabled for a table.

Returns `True` if a chronicle table exists for the given table, `False` otherwise.

```python
import sqlite_chronicle

if sqlite_chronicle.is_chronicle_enabled(conn, "dogs"):
    print("Chronicle is enabled for dogs")
else:
    print("Chronicle is not enabled for dogs")
```

### list_chronicled_tables(conn)

Use `sqlite_chronicle.list_chronicled_tables(conn)` to get a list of all tables that have chronicle tracking enabled.

```python
import sqlite_chronicle

tables = sqlite_chronicle.list_chronicled_tables(conn)
print(f"Chronicle is enabled for: {tables}")
# Output: Chronicle is enabled for: ['dogs', 'cats']
```

### upgrade_chronicle(conn, table_name)

This function detects if the specified table has previously had an older version of the chronicle table and triggers created for it, and if so it will upgrade that table to the latest implementation, preserving existing timestamp and version data.

### updates_since(conn, table_name, since=None, batch_size=1000)

The `sqlite_chronicle.updates_since()` function returns a generator over a list of `Change` objects.

These objects represent changes that have occurred to rows in the table since the `since` version number, or since the beginning of time if `since` is not provided.

- `conn` is a SQLite connection object
- `table_name` is a string containing the name of the table to get changes for
- `since` is an optional integer version number - if not provided, all changes will be returned
- `batch_size` is an internal detail, controlling the number of rows that are returned from the database at a time. You should not need to change this as the function implements its own internal pagination.

Each `Change` returned from the generator looks something like this:

```python
Change(
    pks=(5,),
    added_ms=1701836971223,
    updated_ms=1701836971223,
    version=5,
    row={'id': 5, 'name': 'Simon'},
    deleted=False
)
```
A `Change` is a dataclass with the following properties:

- `pks` is a tuple of the primary key values for the row - this will be a tuple with a single item for normal primary keys, or multiple items for compound primary keys
- `added_ms` is the timestamp in milliseconds when the row was added
- `updated_ms` is the timestamp in milliseconds when the row was last updated
- `version` is the version number for the row - you can use this as a `since` value to get changes since that point
- `row` is a dictionary containing the current values for the row - these will be `None` if the row has been deleted (except for the primary keys)
- `deleted` is `0` if the row has not been deleted, or `1` if it has been deleted

Any time you call this you should track the last `version` number that you see, so you can pass it as the `since` value in future calls to get changes that occurred since that point.

Note that if a row had multiple updates in between calls to this function you will still only see one `Change` object for that row - the `updated_ms` and `version` will reflect the most recent update.

## Implementation notes

- Both `INSERT OR REPLACE` and `INSERT ... ON CONFLICT DO UPDATE` (UPSERT) are fully supported. If an `INSERT OR REPLACE` writes identical data to an existing row, no version bump occurs.
- If a row is deleted and then re-inserted with the same primary key, `__added_ms` is reset to the time of re-insertion (and `__deleted` flips back to `0`). This treats an "undelete" as a fresh addition rather than a continuation of the original row's history.
- Updates to columns that are part of a primary key for the record is not currently supported.

## Potential applications

Chronicle tables can be used to efficiently answer the question "what rows have been inserted, updated or deleted since I last checked" - by looking at the `version` column which has an index to make it fast to answer that question.

This has numerous potential applications, including:

- Synchronization and replication: other databases can "subscribe" to tables, keeping track of when they last refreshed their copy and requesting just rows that changed since the last time - and deleting rows that have been marked as deleted.
- Indexing: if you need to update an Elasticsearch index or a vector database embeddings index or similar you can run against just the records that changed since your last run - see also [The denormalized query engine design pattern](https://2017.djangocon.us/talks/the-denormalized-query-engine-design-pattern/)
- Enrichments: [datasette-enrichments](https://github.com/datasette/datasette-enrichments) needs to to persist something that says "every address column should be geocoded" - then have an enrichment that runs every X seconds and looks for newly inserted or updated rows and enriches just those.
- Showing people what has changed since their last visit - "52 rows have been updated and 16 deleted since yesterday" kind of thing.

## Example SQL schema

Here's an example SQL schema showing the `_chronicle_dogs` table that would be created for a `dogs` table, along with its triggers:


<!-- [[[cog
import cog
import sqlite3
import sqlite_chronicle
db = sqlite3.connect(":memory:")
db.execute('create table dogs (id integer primary key, name text, age integer)')
sqlite_chronicle.enable_chronicle(db, 'dogs')
cog.out('```sql\n')
cog.outl(';\n\n'.join(r[0] for r in db.execute('select sql from sqlite_master').fetchall() if r[0]))
cog.out('\n```')
]]] -->
```sql
CREATE TABLE dogs (id integer primary key, name text, age integer);

CREATE TABLE "_chronicle_dogs" (
  "id" INTEGER,
  __added_ms INTEGER,
  __updated_ms INTEGER,
  __version INTEGER,
  __deleted INTEGER DEFAULT 0,
  PRIMARY KEY("id")
);

CREATE INDEX "_chronicle_dogs__version_idx"
  ON "_chronicle_dogs"(__version);

CREATE TABLE "_chroniclesnapshots" (table_name TEXT, key TEXT, value TEXT, PRIMARY KEY(table_name, key));

CREATE TRIGGER "chronicle_dogs_bi"
BEFORE INSERT ON "dogs"
FOR EACH ROW
WHEN EXISTS(SELECT 1 FROM "dogs" WHERE "id"=NEW."id")
BEGIN
  INSERT OR REPLACE INTO "_chroniclesnapshots"(table_name, key, value)
  VALUES('dogs', CAST(NEW."id" AS TEXT), (SELECT json_array(quote("name"), quote("age")) FROM "dogs" WHERE "id"=NEW."id"));
END;

CREATE TRIGGER "chronicle_dogs_ai"
AFTER INSERT ON "dogs"
FOR EACH ROW
BEGIN
  -- Un-delete if re-inserting a previously deleted row
  UPDATE "_chronicle_dogs"
  SET __added_ms = CAST((julianday('now') - 2440587.5)*86400*1000 AS INTEGER), __updated_ms = CAST((julianday('now') - 2440587.5)*86400*1000 AS INTEGER), __version = COALESCE((SELECT MAX(__version) FROM "_chronicle_dogs"),0) + 1, __deleted = 0
  WHERE "id"=NEW."id" AND __deleted = 1;

  -- Replace with actual change: bump version
  UPDATE "_chronicle_dogs"
  SET __updated_ms = CAST((julianday('now') - 2440587.5)*86400*1000 AS INTEGER), __version = COALESCE((SELECT MAX(__version) FROM "_chronicle_dogs"),0) + 1
  WHERE "id"=NEW."id" AND __deleted = 0
    AND EXISTS(SELECT 1 FROM "_chroniclesnapshots" WHERE table_name = 'dogs' AND key = CAST(NEW."id" AS TEXT))
    AND json_array(quote(NEW."name"), quote(NEW."age")) IS NOT (SELECT value FROM "_chroniclesnapshots" WHERE table_name = 'dogs' AND key = CAST(NEW."id" AS TEXT));

  -- Clean up snapshot
  DELETE FROM "_chroniclesnapshots" WHERE table_name = 'dogs' AND key = CAST(NEW."id" AS TEXT);

  -- Fresh insert: create chronicle entry (NO INSERT OR IGNORE!)
  INSERT INTO "_chronicle_dogs"("id", __added_ms, __updated_ms, __version, __deleted)
  SELECT NEW."id", CAST((julianday('now') - 2440587.5)*86400*1000 AS INTEGER), CAST((julianday('now') - 2440587.5)*86400*1000 AS INTEGER), COALESCE((SELECT MAX(__version) FROM "_chronicle_dogs"),0) + 1, 0
  WHERE NOT EXISTS(SELECT 1 FROM "_chronicle_dogs" WHERE "id"=NEW."id");
END;

CREATE TRIGGER "chronicle_dogs_au"
AFTER UPDATE ON "dogs"
FOR EACH ROW
WHEN OLD."name" IS NOT NEW."name" OR OLD."age" IS NOT NEW."age"
BEGIN
  UPDATE "_chronicle_dogs"
  SET __updated_ms = CAST((julianday('now') - 2440587.5)*86400*1000 AS INTEGER),
    __version = COALESCE((SELECT MAX(__version) FROM "_chronicle_dogs"),0) + 1
  WHERE "id"=NEW."id";
END;

CREATE TRIGGER "chronicle_dogs_ad"
AFTER DELETE ON "dogs"
FOR EACH ROW
WHEN NOT EXISTS(SELECT 1 FROM "_chroniclesnapshots" WHERE table_name = 'dogs' AND key = CAST(OLD."id" AS TEXT))
BEGIN
  UPDATE "_chronicle_dogs"
    SET __updated_ms = CAST((julianday('now') - 2440587.5)*86400*1000 AS INTEGER),
      __version = COALESCE((SELECT MAX(__version) FROM "_chronicle_dogs"),0) + 1,
      __deleted = 1
  WHERE "id"=OLD."id";
END

```
<!-- [[[end]]] -->
