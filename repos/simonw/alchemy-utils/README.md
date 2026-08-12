# alchemy-utils

[![PyPI](https://img.shields.io/pypi/v/alchemy-utils.svg)](https://pypi.org/project/alchemy-utils/)
[![Tests](https://github.com/simonw/alchemy-utils/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/alchemy-utils/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/alchemy-utils?include_prereleases&label=changelog)](https://github.com/simonw/alchemy-utils/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/alchemy-utils/blob/main/LICENSE)

An executable research spike for a subset of the
[`sqlite-utils`](https://sqlite-utils.datasette.io/) Python API backed by
SQLAlchemy Core, built [using GPT-5.6 Sol Ultra and Codex](https://gist.github.com/simonw/bd10e4886688e0fd1b833e4afaabf19e).

It demonstrates the same style of table-first API across SQLite, PostgreSQL,
and DuckDB:

```python
from alchemy_utils import Database

db = Database("sqlite:///:memory:")

people = db["people"].insert(
    {"id": 1, "name": "Ada", "profile": {"language": "Python"}},
    pk="id",
)
people.upsert({"id": 1, "name": "Ada Lovelace"})
people.insert_all(
    [
        {"id": 2, "name": "Grace"},
        {"id": 3, "name": "Katherine"},
    ]
)
people.update(2, {"name": "Grace Hopper"})

assert people.pks == ["id"]
assert people.columns_dict["profile"] is dict
assert people.get(1)["name"] == "Ada Lovelace"
```

Swap only the URL to use another engine:

```python
postgres = Database("postgresql+psycopg://user:password@localhost/app")
duckdb = Database("duckdb:///analytics.duckdb")
```

This is a spike, not a published compatibility promise. See
[RESEARCH.md](RESEARCH.md) for the conclusion, design trade-offs, and a rough
production estimate.

## Implemented API

`Database` supports:

- construction from a SQLAlchemy `Engine`, `URL`, URL string, or SQLite path;
- `db[name]`, `db.table()`, and `db.create_table()`;
- `table_names()`, `view_names()`, `tables`, and normalized `schema`;
- context-manager cleanup and `close()`.

`Table` supports:

- `create()` with Python or SQLAlchemy types, single/compound primary keys,
  partial column ordering, `NOT NULL`, server defaults, single/compound foreign
  keys, and existing-table options;
- `insert()`, `insert_all()`, `upsert()`, `upsert_all()`, and `update()`;
- generated integer primary keys on all three engines;
- `alter=True` for new nullable columns, plus insert `ignore=True` and
  `replace=True` conflict modes;
- `exists()`, `count`, `rows`, and `get()`;
- `columns`, `columns_dict`, `pks`, `foreign_keys`, `indexes`, `schema`,
  `default_values`, and `use_rowid`.

All mutation methods return the same `Table` object for chaining. A one-record
write sets `last_pk`; bulk writes leave it as `None`.

## Engine-specific architecture

Calling `Database(...)` selects an independent engine implementation:

```text
Database factory
├── SQLiteDatabase       SQLite ON CONFLICT and rowid capability
├── PostgreSQLDatabase   PostgreSQL ON CONFLICT
└── DuckDBDatabase       DuckDB ON CONFLICT, sequences, catalog fallbacks
         │
         └── PK / JSON / index / DDL reflection repairs

Table                     shared API and orchestration only
```

The shared `Table` class does not inspect dialect names or build dialect SQL.
It delegates conflict statements, generated-key DDL, table lifecycle, and
reflection to its `Database` instance.

## Install

The base package needs Click and SQLAlchemy and works with Python 3.10 or
later. Engine drivers are extras:

```bash
pip install alchemy-utils
pip install 'alchemy-utils[postgresql]'
pip install 'alchemy-utils[duckdb]'
```

For this checkout, `uv sync` installs the development group, including both
drivers and the test tools.

## Command-line interface

Installing the package adds a collision-safe `alchemy-utils` command.
It follows the relevant sqlite-utils command shapes, but its `DATABASE`
argument can be either a SQLite filename or any installed SQLAlchemy URL:

```bash
# SQLite: a bare path
alchemy-utils create-table data.db people \
  id integer name text profile json --pk id --not-null name

# PostgreSQL and DuckDB: SQLAlchemy URLs
alchemy-utils tables \
  postgresql+psycopg://user@localhost/app --json
alchemy-utils schema duckdb:///analytics.duckdb
```

For PostgreSQL credentials, prefer libpq environment variables or a password
file instead of putting a password in the command-line URL, where it could be
recorded in shell history.

`insert` and `upsert` each handle either one record or many records, mapping to
the corresponding single-record or `*_all()` API. The default input is a JSON
object or array. Use `--nl`, `--csv`, or `--tsv` for other formats; `-` reads
standard input, and those formats are also detected from file extensions.

```bash
echo '{"id": 1, "name": "Ada"}' \
  | alchemy-utils insert data.db people -

printf '%s\n' \
  '{"id": 1, "name": "Ada Lovelace"}' \
  '{"id": 2, "name": "Grace Hopper"}' \
  | alchemy-utils upsert data.db people - --nl

echo '{"name": "Amazing Grace", "active": true}' \
  | alchemy-utils update data.db people 2 - --alter
```

Repeat `--pk` for compound keys. `get` and `update` accept a JSON array for a
compound key, for example `'["acme", 7]'`. Binary JSON values use sqlite-utils'
portable shape, `{"$base64": true, "encoded": "AP8="}`.

Available inspection and read commands are `tables`, `views`, `schema`,
`columns`, `indexes`, `foreign-keys`, `rows`, `get`, and `count`. Metadata and
rows use normalized JSON (or JSON lines with `--nl` where offered); schema is
engine-shaped reflected DDL. `tables` and `views` use JSON by default, with
`--plain` for one name per line. Mutations are silent on success, as in
sqlite-utils. Run any command with `--help` for its options. The same interface
is also available as `python -m alchemy_utils`.

## Test

```bash
uv sync
uv run ruff check src tests
uv run pytest
```

PostgreSQL tests use `testing.postgresql` to start one disposable server and a
unique database per test. They never use an existing application database. The
fixture finds `postgres` and `initdb` from environment variables, `PATH`, or
`pg_config`; if it cannot find them, PostgreSQL cases are skipped.

Homebrew example:

```bash
PG_BIN="$(brew --prefix postgresql@18)/bin"
POSTGRESQL_PATH="$PG_BIN/postgres" \
INITDB_PATH="$PG_BIN/initdb" \
uv run pytest
```

The library and CLI suites run on all three engines and have been exercised on
both Python 3.10 and 3.14.3, with SQLAlchemy 2.0.52, SQLite 3.50.4, PostgreSQL
18.3, DuckDB 1.5.5, duckdb-engine 0.17.0, and psycopg 3.3.4.

## Deliberate spike limitations

- Bulk inputs are materialized in memory; `batch_size` is accepted but not yet
  used for streaming chunks.
- Bulk input supports mappings, not sqlite-utils' header-plus-sequence mode.
- `alter=True` only adds nullable columns. Full transforms are out of scope.
- Exact SQLite DDL text, implicit indexes, triggers, checks, FTS, and STRICT
  metadata are not portable and are not emulated.
- `hash_id`, extracts, conversions, `analyze`, and schema transforms are not
  implemented.
- Reflected type names and raw server-default SQL vary by engine. The stable
  portable fields are names, Python types, nullability, key ordering, foreign
  key shape, and explicit indexes.
- A hidden `rowid` is never synthesized as a primary key. `use_rowid` reports
  the SQLite capability, while `pks` returns only declared keys on every engine.
- Mixing explicit integer primary keys with later generated keys may require
  synchronizing the PostgreSQL or DuckDB sequence; this spike does not do that.
- DuckDB expression-index parsing is intentionally best-effort; ordinary
  column indexes are covered.
