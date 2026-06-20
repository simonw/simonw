# sqlite-history

[![PyPI](https://img.shields.io/pypi/v/sqlite-history.svg)](https://pypi.org/project/sqlite-history/)
[![Tests](https://github.com/simonw/sqlite-history/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-history/actions?query=workflow%3ATest)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-history?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-history/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-history/blob/main/LICENSE)

Track changes to SQLite tables using triggers

For more on this project: [sqlite-history: tracking changes to SQLite tables using triggers](https://simonwillison.net/2023/Apr/15/sqlite-history/)

## Installation

Install this library using `pip`:

    pip install sqlite-history

## Usage

This library can be used to configure triggers on a SQLite database such that any inserts, updates or deletes against a table will have their changes recorded in a separate table.

You can enable history tracking for a table using the `configure_history()` function:

    import sqlite_history
    import sqlite3

    conn = sqlite3.connect("data.db")
    conn.execute("CREATE TABLE table1 (id INTEGER PRIMARY KEY, name TEXT)")
    sqlite_history.configure_history(conn, "table1")

Or you can use the CLI interface, available via `python -m sqlite_history`:

    python -m sqlite_history data.db table1 [table2 table3 ...]

Use `--all` to configure it for all tables:

    python -m sqlite_history data.db --all

## How this works

Given a table with the following schema:

<!-- [[[cog
import cog
create_table_sql = """
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    weight REAL
);
""".strip()
cog.out(
    "```sql\n{}\n```".format(create_table_sql)
)
]]] -->
```sql
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    weight REAL
);
```
<!-- [[[end]]] -->

This library will create a new table called `_people_history` with the following schema:

<!-- [[[cog
from sqlite_history import sql
import sqlite3
db = sqlite3.connect(":memory:")
db.execute(create_table_sql)
columns_and_types = sql.table_columns_and_types(db, "people")
history_schema = sql.history_table_sql("people", columns_and_types)
cog.out(
    "```sql\n{}\n```".format(history_schema.strip())
)
]]] -->
```sql
CREATE TABLE _people_history (
    _rowid INTEGER,
    id INTEGER,
    name TEXT,
    age INTEGER,
    weight REAL,
    _version INTEGER,
    _updated INTEGER,
    _mask INTEGER
);
CREATE INDEX idx_people_history_rowid ON _people_history (_rowid);
```
<!-- [[[end]]] -->
The `_rowid` column references the `rowid` of the row in the original table that is being tracked. If a row has been updated multiple times there will be multiple rows with the same `_rowid` in this table.

The `id`, `name`, `age` and `weight` columns represent the new values assigned to the row when it was updated. These can also be `null`, which might represent no change or might represent the value being set to `null` (hence the `_mask` column).

The `_version` column is a monotonically increasing integer that is incremented each time a row is updated.

The `_updated` column is a timestamp showing when the change was recorded. This is stored in milliseconds since the Unix epoch - to convert that to a human-readable UTC date you can use `strftime('%Y-%m-%d %H:%M:%S', _updated / 1000, 'unixepoch')` in your SQL queries.

The `_mask` column is a bit mask that indicates which columns changed in an update. The bit mask is calculated by adding together the following values:

    1: id
    2: name
    4: age
    8: weight

Tables with different schemas will have different `_mask` values.

A `_mask` of `-1` indicates that the row was deleted.

The following triggers are created to populate the `_people_history` table:
<!-- [[[cog
triggers_sql = sql.triggers_sql("people", [c[0] for c in columns_and_types])
cog.out(
    "```sql\n{}\n```".format(triggers_sql.strip())
)
]]] -->
```sql
CREATE TRIGGER people_insert_history
AFTER INSERT ON people
BEGIN
    INSERT INTO _people_history (_rowid, id, name, age, weight, _version, _updated, _mask)
    VALUES (new.rowid, new.id, new.name, new.age, new.weight, 1, cast((julianday('now') - 2440587.5) * 86400 * 1000 as integer), 15);
END;

CREATE TRIGGER people_update_history
AFTER UPDATE ON people
FOR EACH ROW
BEGIN
    INSERT INTO _people_history (_rowid, id, name, age, weight, _version, _updated, _mask)
    SELECT old.rowid, 
        CASE WHEN old.id != new.id then new.id else null end, 
        CASE WHEN old.name != new.name then new.name else null end, 
        CASE WHEN old.age != new.age then new.age else null end, 
        CASE WHEN old.weight != new.weight then new.weight else null end,
        (SELECT MAX(_version) FROM _people_history WHERE _rowid = old.rowid) + 1,
        cast((julianday('now') - 2440587.5) * 86400 * 1000 as integer),
        (CASE WHEN old.id != new.id then 1 else 0 end) + (CASE WHEN old.name != new.name then 2 else 0 end) + (CASE WHEN old.age != new.age then 4 else 0 end) + (CASE WHEN old.weight != new.weight then 8 else 0 end)
    WHERE old.id != new.id or old.name != new.name or old.age != new.age or old.weight != new.weight;
END;

CREATE TRIGGER people_delete_history
AFTER DELETE ON people
BEGIN
    INSERT INTO _people_history (_rowid, id, name, age, weight, _version, _updated, _mask)
    VALUES (
        old.rowid,
        old.id, old.name, old.age, old.weight,
        (SELECT COALESCE(MAX(_version), 0) from _people_history WHERE _rowid = old.rowid) + 1,
        cast((julianday('now') - 2440587.5) * 86400 * 1000 as integer),
        -1
    );
END;
```
<!-- [[[end]]] -->

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd sqlite-history
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
