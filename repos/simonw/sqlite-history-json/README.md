# sqlite-history-json

[![PyPI](https://img.shields.io/pypi/v/sqlite-history-json.svg)](https://pypi.org/project/sqlite-history-json/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-history-json?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-history-json/releases)
[![Tests](https://github.com/simonw/sqlite-history-json/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-history-json/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-history-json/blob/main/LICENSE)

A Python library for tracking SQLite table history using a JSON audit log.

Based on the pattern described in [Tracking SQLite table history using a JSON audit log](https://til.simonwillison.net/sqlite/json-audit-log).

## How it works

`sqlite-history-json` uses SQLite triggers to automatically record every INSERT, UPDATE, and DELETE operation on a tracked table into a companion audit log table. Changed values are stored as JSON, using SQLite's built-in `json_patch()` and `json_object()` functions.

This is the "updated values" approach: each audit entry records the **new** values of changed columns (not the old ones). This means:

- **INSERT** entries record all column values for the new row
- **UPDATE** entries record only the columns that changed, with their new values
- **DELETE** entries just record that the row was deleted (the PK identifies which row)

The audit log is self-contained: given only the audit table, you can fully reconstruct the tracked table's state at any point in history.

### JSON encoding conventions

| Value | JSON representation |
|-------|-------------------|
| Regular value | Stored directly: `"Widget"`, `42`, `3.14` |
| `NULL` | `{"null": 1}` (because `json_patch()` treats bare `null` as "remove key") |
| BLOB | `{"hex": "DEADBEEF"}` (hex-encoded binary) |

### Audit table schema

For a table called `items` with primary key `id`, the audit table `_history_json_items` looks like:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Auto-incrementing version number |
| `timestamp` | TEXT | ISO-8601 datetime with microsecond precision |
| `operation` | TEXT | `'insert'`, `'update'`, or `'delete'` |
| `pk_id` | (matches source PK type) | The primary key of the tracked row (prefixed with `pk_`) |
| `updated_values` | TEXT | JSON object of changed columns (NULL for deletes) |
| `group` | INTEGER | Foreign key to `_history_json.id` (NULL when no group is active) |

Primary key columns in the audit table are always prefixed with `pk_` to distinguish them from the audit table's own columns. For compound primary keys, each PK column gets its own `pk_`-prefixed column (e.g., `pk_user_id`, `pk_role_id`).

Indexes are automatically created on `timestamp` and the PK column(s) for efficient querying.

### Change groups table

A shared `_history_json` table (no suffix) is created when tracking is first enabled. It stores change-group metadata:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Auto-incrementing group identifier |
| `note` | TEXT | Optional description of the batch of changes |
| `current` | INTEGER | Set to `1` during an active `change_group()` block, otherwise NULL |

The `current` column is indexed. During a `change_group()` context, triggers use `(SELECT id FROM _history_json WHERE current = 1)` to look up the active group. When no group is active, this returns NULL and audit rows are written with `group = NULL`.

## Installation

```bash
pip install sqlite-history-json
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add sqlite-history-json
```

## Usage

### Enable tracking on a table

```python
import sqlite3
from sqlite_history_json import enable_tracking, disable_tracking, populate, restore, change_group

conn = sqlite3.connect("mydb.db")

# Create your table
conn.execute("""
    CREATE TABLE items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price FLOAT,
        quantity INTEGER
    )
""")

# Start tracking changes
enable_tracking(conn, "items")

# Now all INSERT, UPDATE, DELETE operations are automatically logged
conn.execute("INSERT INTO items VALUES (1, 'Widget', 9.99, 100)")
conn.execute("UPDATE items SET price = 12.99 WHERE id = 1")
conn.execute("DELETE FROM items WHERE id = 1")
```

### Snapshot existing data

By default, `enable_tracking()` automatically populates the audit log with a snapshot of all existing rows. This means the audit log is complete from the moment tracking starts:

```python
# Table already has rows in it...
enable_tracking(conn, "items")  # automatically snapshots existing rows

# From this point on, the audit log has a complete record
```

You can opt out of auto-population if you want to control when the snapshot happens:

```python
enable_tracking(conn, "items", populate_table=False)
# ... do something else ...
populate(conn, "items")  # manually snapshot when ready
```

### Transaction control during setup/teardown

By default, `enable_tracking()` and `disable_tracking()` wrap their work in a SQLite `SAVEPOINT` (`atomic=True`). This makes each operation atomic and safe whether or not you're already inside your own transaction.

```python
# Default: atomic via savepoint
enable_tracking(conn, "items")
disable_tracking(conn, "items")

# Opt out if you want to fully manage transaction boundaries yourself
enable_tracking(conn, "items", atomic=False)
disable_tracking(conn, "items", atomic=False)
```

### Restore to a point in time

```python
# Restore table state to a specific timestamp (creates a new table)
restored_name = restore(conn, "items", timestamp="2024-06-15 14:30:00.000000")

# Query the restored table
rows = conn.execute(f"SELECT * FROM [{restored_name}]").fetchall()
```

### Restore to a specific version (audit entry ID)

Since `datetime('now')` in SQLite has second-level precision in some contexts, you can use `up_to_id` to get exact version-level restore using the audit log's auto-incrementing primary key:

```python
# Restore to the state after audit entry #42
restored_name = restore(conn, "items", up_to_id=42)
```

### Restore with atomic swap

Replace the original table with the restored version:

```python
# Atomically replaces `items` with the restored state
restore(conn, "items", up_to_id=42, swap=True)

# `items` now contains the restored data
```

### Custom restored table name

```python
restored_name = restore(
    conn, "items", timestamp="2024-06-15 14:30:00",
    new_table_name="items_backup"
)
```

### Query the audit log

```python
from sqlite_history_json import get_history, get_row_history

# Get all history for a table, newest first
entries = get_history(conn, "items")

# Limit to most recent 10 entries
entries = get_history(conn, "items", limit=10)

# Get history for a specific row
entries = get_row_history(conn, "items", {"id": 1})

# Compound primary keys
entries = get_row_history(conn, "user_roles", {"user_id": 1, "role_id": 2})
```

Each entry is a dict:
```python
{
    "id": 1,
    "timestamp": "2024-06-15 14:30:00.123",
    "operation": "insert",
    "pk": {"id": 1},
    "updated_values": {"name": "Widget", "price": 9.99, "quantity": 100},
    "group": 1,           # integer group id, or None
    "group_note": "bulk import"  # note from the group, or None
}
```

- `pk` uses original column names (no `pk_` prefix)
- `updated_values` preserves the JSON conventions (`{"null": 1}` for NULL, `{"hex": "..."}` for BLOBs)
- For deletes, `updated_values` is `None`
- `group` and `group_note` are `None` when the change was made outside a `change_group()` block

### Disable tracking

```python
# Drops the triggers but keeps the audit table and its data
disable_tracking(conn, "items")
```

### Group changes with optional notes

Change groups work at the SQL level using the `_history_json` table. During a transaction, insert a row with `current = 1` and the triggers will automatically set the `group` column on any audit entries to that row's id:

```sql
BEGIN;
INSERT INTO _history_json (note, current) VALUES ('bulk import from CSV', 1);
INSERT INTO items VALUES (1, 'Widget', 9.99, 100);
INSERT INTO items VALUES (2, 'Gadget', 24.99, 50);
UPDATE items SET price = 12.99 WHERE id = 1;
-- Clear the current marker before committing
UPDATE _history_json SET current = NULL WHERE current = 1;
COMMIT;
```

The Python `change_group()` context manager is a convenient wrapper around this pattern that handles the setup and cleanup automatically:

```python
from sqlite_history_json import change_group

# All changes inside the block share the same group
with change_group(conn, note="bulk import from CSV") as group_id:
    conn.execute("INSERT INTO items VALUES (1, 'Widget', 9.99, 100)")
    conn.execute("INSERT INTO items VALUES (2, 'Gadget', 24.99, 50)")
    conn.execute("UPDATE items SET price = 12.99 WHERE id = 1")

# Changes outside the block have group = NULL
conn.execute("INSERT INTO items VALUES (3, 'Doohickey', 4.99, 200)")
```

The context manager yields the integer group id. You can also update the note during the block:

```python
with change_group(conn, note="migration step 1") as group_id:
    conn.execute("INSERT INTO items VALUES (1, 'Widget', 9.99, 100)")
    # Update the note mid-transaction
    conn.execute("UPDATE _history_json SET note = 'migration step 1 (3 rows)' WHERE id = ?", [group_id])
```

Groups work across multiple tracked tables — a single `change_group()` block groups changes to any table whose triggers are active:

```python
with change_group(conn, note="cross-table update"):
    conn.execute("INSERT INTO items VALUES (1, 'Widget', 9.99, 100)")
    conn.execute("INSERT INTO orders VALUES (1, 1)")  # both share the same group
```

### Compound primary keys

Tables with compound primary keys are fully supported:

```python
conn.execute("""
    CREATE TABLE user_roles (
        user_id INTEGER,
        role_id INTEGER,
        granted_by TEXT,
        active INTEGER,
        PRIMARY KEY (user_id, role_id)
    )
""")

enable_tracking(conn, "user_roles")

# The audit table `_history_json_user_roles` will have
# `pk_user_id` and `pk_role_id` columns
```

### Tables with special characters in names

Table names containing spaces, hyphens, dots, and other special characters are handled correctly:

```python
conn.execute('CREATE TABLE "order items" (id INTEGER PRIMARY KEY, product TEXT)')
enable_tracking(conn, "order items")
```

## API reference

### `enable_tracking(conn, table_name, *, populate_table=True, atomic=True)`

Creates the audit table `_history_json_{table_name}` and installs INSERT, UPDATE, and DELETE triggers on the source table. Also creates indexes on the audit table for timestamp and primary key columns.

By default, snapshots all existing rows into the audit log (equivalent to calling `populate()` automatically). Pass `populate_table=False` to skip this.

By default, runs inside a SQLite `SAVEPOINT` (`atomic=True`) so setup is atomic and safe to call both inside and outside an existing transaction. Pass `atomic=False` to skip this wrapper.

Idempotent: calling it twice has no additional effect (auto-populate only runs if the audit table is empty).

**Requirements:** The table must have an explicit `PRIMARY KEY` (not just `rowid`).

### `disable_tracking(conn, table_name, *, atomic=True)`

Drops the triggers. The audit table and its data are preserved.

By default, runs inside a SQLite `SAVEPOINT` (`atomic=True`) so trigger removal is atomic and safe inside or outside an existing transaction. Pass `atomic=False` to skip this wrapper.

Idempotent: calling it when no triggers exist is a no-op.

### `populate(conn, table_name)`

Inserts one `'insert'` audit entry per existing row, creating a baseline snapshot. Usually not needed directly since `enable_tracking()` calls this automatically, but useful if you passed `populate_table=False` and want to snapshot later.

### `restore(conn, table_name, *, timestamp=None, up_to_id=None, new_table_name=None, swap=False)`

Replays audit log entries to reconstruct the table state. All parameters after `table_name` are keyword-only.

- **`timestamp`**: Restore up to this ISO-8601 timestamp (inclusive)
- **`up_to_id`**: Restore up to this audit entry ID (inclusive). More precise than timestamp for operations within the same second.
- **`new_table_name`**: Name for the restored table (default: `{table_name}_restored`)
- **`swap`**: If `True`, atomically replaces the original table

Returns the name of the restored table.

### `get_history(conn, table_name, *, limit=None)`

Returns audit log entries for a table as a list of dicts, newest first. Each dict has keys: `id`, `timestamp`, `operation`, `pk`, `updated_values`, `group`, `group_note`.

- **`limit`**: Maximum number of entries to return

### `get_row_history(conn, table_name, pk_values, *, limit=None)`

Same as `get_history()` but filtered to a specific row. `pk_values` is a dict mapping primary key column names to values, e.g. `{"id": 1}` or `{"user_id": 1, "role_id": 2}`.

### `change_group(conn, note=None)`

Context manager that groups all audit entries created within its block. Every trigger-inserted audit row will share the same `group` id. An optional `note` string can describe the batch.

Yields the integer group id. The `current` marker is cleared automatically when the block exits (including on exceptions).

```python
with change_group(conn, note="migration") as group_id:
    conn.execute("INSERT INTO items VALUES (1, 'Widget', 9.99, 100)")
    # group_id is an integer you can reference later
```

### `row_state_sql(conn, table_name)`

Returns a SQL query string that reconstructs a single row's state at a given audit version using a recursive CTE and `json_patch()`. The query runs entirely inside SQLite with no Python-side replay.

The returned query takes named parameters:
- **`:pk`** for single-PK tables, or **`:pk_1`**, **`:pk_2`**, ... for compound PKs (numbered by PK column order)
- **`:target_id`** — the audit log entry ID to reconstruct up to

The query returns one row with a single `state` column containing the JSON object of non-PK column values at that version, or `NULL` if the row was deleted, or no rows if the PK has no history at that version.

Raises `ValueError` if tracking is not enabled for the table.

```python
from sqlite_history_json import row_state_sql

sql = row_state_sql(conn, "items")
# sql is a ready-to-execute query string

# Reconstruct row state at audit entry #3
result = conn.execute(sql, {"pk": 1, "target_id": 3}).fetchone()
if result is None:
    print("No history for this PK at this version")
elif result[0] is None:
    print("Row was deleted at this version")
else:
    state = json.loads(result[0])
    print(state)  # {"name": "Widget", "price": 9.99, "quantity": 100}

# Compound primary key
sql = row_state_sql(conn, "user_roles")
result = conn.execute(sql, {"pk_1": 1, "pk_2": 2, "target_id": 5}).fetchone()
```

For a table `items` with primary key `id`, the generated SQL looks like:

```sql
with entries as (
  select id, operation, updated_values,
         row_number() over (order by id) as rn
  from [_history_json_items]
  where [pk_id] = :pk
    and id <= :target_id
    and id >= (
      select max(id) from [_history_json_items]
      where [pk_id] = :pk
        and operation = 'insert' and id <= :target_id
    )
),
folded as (
  select rn, operation, updated_values as state
  from entries where rn = 1

  union all

  select e.rn, e.operation,
    case when e.operation = 'delete' then null
         else json_patch(f.state, e.updated_values)
    end
  from folded f
  join entries e on e.rn = f.rn + 1
)
select state from folded order by rn desc limit 1
```

The `entries` CTE finds the most recent `insert` for the row at or before the target version, then collects all entries from that insert through the target. The `folded` CTE recursively applies `json_patch()` to merge each entry's changed values into the accumulated state. Handles delete-and-reinsert cycles correctly by always starting from the latest insert.

## Command-line interface

All commands use the form:

```bash
python -m sqlite_history_json <command> <database> [options]
```

### `enable`

Enable tracking for a table:

```bash
python -m sqlite_history_json enable mydb.db items
```

Skip populating the audit log with existing rows:

```bash
python -m sqlite_history_json enable mydb.db items --no-populate
```

### `disable`

Disable tracking (drops triggers, keeps audit data):

```bash
python -m sqlite_history_json disable mydb.db items
```

### `history`

Show audit log entries for a table as JSON (newest first):

```bash
python -m sqlite_history_json history mydb.db items
python -m sqlite_history_json history mydb.db items -n 20
```

### `row-history`

Show audit log entries for a specific row. PK values are positional, matched to PK columns in their defined order:

```bash
python -m sqlite_history_json row-history mydb.db items 42
python -m sqlite_history_json row-history mydb.db user_roles 1 2
```

### `restore`

Restore a table from its audit log:

```bash
# Restore to a new table (default: items_restored)
python -m sqlite_history_json restore mydb.db items

# Restore up to a specific audit entry ID
python -m sqlite_history_json restore mydb.db items --id 3

# Restore up to a specific timestamp
python -m sqlite_history_json restore mydb.db items --timestamp "2024-06-15 14:30:00"

# Restore with a custom table name
python -m sqlite_history_json restore mydb.db items --id 3 --new-table items_v2

# Replace the original table with the restored version
python -m sqlite_history_json restore mydb.db items --id 3 --replace-table

# Restore to a different database file
python -m sqlite_history_json restore mydb.db items --id 3 --output-db backup.db
```

`--replace-table` and `--output-db` are mutually exclusive. Neither `--timestamp` nor `--id` is required (restores full history if neither given).

### `row-state-sql`

Output the SQL query that reconstructs a row's state at a given audit version:

```bash
python -m sqlite_history_json row-state-sql mydb.db items
```

The output is a ready-to-execute SQL query using a recursive CTE and `json_patch()`. You can pipe it to other tools or use it directly with named parameters (`:pk` and `:target_id` for single-PK tables, `:pk_1`, `:pk_2`, ... for compound PKs).

## Upgrading older databases

Databases created with version 0.3a0 or earlier do not have the `[group]` column or the `_history_json` groups table. A built-in upgrade script detects and applies the necessary schema changes.

Preview what would be changed:

```bash
python -m sqlite_history_json.upgrade mydb.db --dry-run
```

Apply the upgrade:

```bash
python -m sqlite_history_json.upgrade mydb.db
```

This will:

1. Create the `_history_json` groups table if it doesn't exist
2. Add the `[group]` column to any audit tables missing it
3. Drop and recreate triggers so they populate the new column

Existing audit data is preserved — pre-upgrade rows get `group = NULL`. The upgrade is idempotent: running it on an already-current database does nothing.

## Development

```bash
# Clone and set up
git clone https://github.com/simonw/sqlite-history-json
cd sqlite-history-json

# Run tests
uv run pytest tests/ -v

# Run CLI
uv run python -m sqlite_history_json --help
```

## How the triggers work

The UPDATE trigger uses nested `json_patch()` calls to build a JSON object containing only the columns that actually changed. The `[group]` column is populated by a subquery that looks up the active change group (or returns NULL if none is active):

```sql
INSERT INTO _history_json_items (timestamp, operation, pk_id, updated_values, [group])
VALUES (
    strftime('%Y-%m-%d %H:%M:%f', 'now'),
    'update',
    NEW.id,
    json_patch(
        json_patch(
            json_patch(
                '{}',
                CASE
                    WHEN OLD.name IS NOT NEW.name THEN
                        CASE
                            WHEN NEW.name IS NULL THEN json_object('name', json_object('null', 1))
                            ELSE json_object('name', NEW.name)
                        END
                    ELSE '{}'
                END
            ),
            CASE
                WHEN OLD.price IS NOT NEW.price THEN
                    CASE
                        WHEN NEW.price IS NULL THEN json_object('price', json_object('null', 1))
                        ELSE json_object('price', NEW.price)
                    END
                ELSE '{}'
            END
        ),
        CASE
            WHEN OLD.quantity IS NOT NEW.quantity THEN
                CASE
                    WHEN NEW.quantity IS NULL THEN json_object('quantity', json_object('null', 1))
                    ELSE json_object('quantity', NEW.quantity)
                END
            ELSE '{}'
        END
    ),
    (SELECT id FROM _history_json WHERE current = 1)
);
```

Each column gets a `CASE` expression that:
1. Checks if the old and new values differ (`IS NOT` handles NULL correctly)
2. If different, creates a JSON object with the column name and new value
3. If unchanged, returns `'{}'` (empty object)

These are combined with `json_patch()` which merges JSON objects together, building up the final diff.

The group subquery `(SELECT id FROM _history_json WHERE current = 1)` is the same in all three triggers (INSERT, UPDATE, DELETE). It returns the active group's id when called inside a `change_group()` context, or NULL otherwise.
