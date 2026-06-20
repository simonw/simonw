# datasette-public

[![PyPI](https://img.shields.io/pypi/v/datasette-public.svg)](https://pypi.org/project/datasette-public/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-public?include_prereleases&label=changelog)](https://github.com/datasette/datasette-public/releases)
[![Tests](https://github.com/datasette/datasette-public/workflows/Test/badge.svg)](https://github.com/datasette/datasette-public/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-public/blob/main/LICENSE)

Make selected Datasette databases, tables and queries visible to the public

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-public
```
## Usage

This plugin can only be used with Datasette 1.0a22+ and requires Datasette to be run with both `--default-deny` and a persistent internal database:

```bash
datasette --internal internal.db --default-deny data.db
```

The `--default-deny` flag is required because `datasette-public` is designed to work in an environment where everything is private by default, and specific databases, tables and queries are then made public by users with the `datasette-public` permission.

Users with the `datasette-public` permission will see action menu items on database, table and query pages that allow them to toggle visibility between public and private.

## How visibility works

**Databases**: When a database is made public, all tables and views within it are automatically public. Users can also choose whether to allow public execution of arbitrary SQL queries against the database. Note that canned queries are NOT automatically public when a database is made public - they must be made public individually.

**Tables**: Individual tables can be made public while keeping the rest of their database private. In this case, users will not be able to use the `?_where=` parameter on those tables (to prevent data exfiltration via crafted queries).

**Queries**: Named canned queries must always be made public individually, even if their parent database is public. This allows fine-grained control over which queries are exposed.

The action menu items only appear when they would be useful:
- Database visibility toggle appears when the database is private (can be made public) or was made public via this plugin (can be made private)
- Table visibility toggle only appears when the parent database is private
- Query visibility toggle appears when the parent database is private OR was made public via this plugin (since queries require explicit public status)

The interfaces for managing visibility include an audit log showing the history of changes.

## Internals

This plugin uses four tables in the internal database:

- `public_databases` - stores the public status of databases and if execute SQL is enabled
- `public_tables` - stores the public status of tables
- `public_queries` - stores the public status of queries
- `public_audit_log` - stores the history of changes to the public status of databases, tables and queries

## Development

To set up this plugin locally, first checkout the code. Then run the tests using `uv`:
```bash
cd datasette-public
uv run pytest
```
In local development it's useful to run Datasette like this:
```bash
uv run datasette data.db \
  --internal internal.db \
  --default-deny \
  --root \
  --secret fixed \
  --reload
```
