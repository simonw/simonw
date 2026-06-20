# datasette-sqlite-authorizer

[![PyPI](https://img.shields.io/pypi/v/datasette-sqlite-authorizer.svg)](https://pypi.org/project/datasette-sqlite-authorizer/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-sqlite-authorizer?include_prereleases&label=changelog)](https://github.com/datasette/datasette-sqlite-authorizer/releases)
[![Tests](https://github.com/datasette/datasette-sqlite-authorizer/workflows/Test/badge.svg)](https://github.com/datasette/datasette-sqlite-authorizer/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-sqlite-authorizer/blob/main/LICENSE)

Configure Datasette to block operations using the SQLite set_authorizer mechanism

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-sqlite-authorizer
```
## Usage

This plugin currently offers a single configuration option: `read_only_tables`. You can use this to specify a list of tables that should be read-only.

If a table is read-only, any attempt to write to it - `insert`, `update`, `delete`, `drop table`, `alter table` - will be denied with an error message.

To configure read-only tables, add the following to your `metadata.yaml` file:

```yaml
plugins:
  datasette-sqlite-authorizer:
    read_only_tables:
    - table: my_table
      database: my_database
```
You can omit the `database` key if you want to apply the same rule to all databases.

Here's how to use this plugin to make all tables relating to [Litestream](https://litestream.io/) synchronization read-only, across all attached databases:

```yaml
plugins:
  datasette-sqlite-authorizer:
    read_only_tables:
    - table: _litestream_lock
    - table: _litestream_seq
```

## Logging actions

To enable debug output (to standard error) for specific action checks, add them to a `debug_actions` list. For example, to log all `SQLITE_INSERT` actions:

```yaml
plugins:
  datasette-sqlite-authorizer:
    debug_actions:
    - SQLITE_INSERT
    - SQLITE_DELETE
```
Logged output will look something like this:
```
authorizer: {"action": "SQLITE_INSERT", "arg1": "foo", "arg2": null, "db_name": "main", "trigger_name": null, "result": "OK"}
authorizer: {"action": "SQLITE_DELETE", "arg1": "foo", "arg2": null, "db_name": "main", "trigger_name": null, "result": "OK"}
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-sqlite-authorizer
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
