# datasette-events-db

[![PyPI](https://img.shields.io/pypi/v/datasette-events-db.svg)](https://pypi.org/project/datasette-events-db/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-events-db?include_prereleases&label=changelog)](https://github.com/datasette/datasette-events-db/releases)
[![Tests](https://github.com/datasette/datasette-events-db/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-events-db/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-events-db/blob/main/LICENSE)

Log Datasette events to a database table

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-events-db
```
This plugin depends on [Datasette 1.0a8](https://docs.datasette.io/en/latest/changelog.html#a8-2024-02-07) or higher.
## Usage

Once installed, all [Datasette events](https://docs.datasette.io/en/latest/events.html) will be logged to a table called `datasette_events`. This table will be created in the private internal database, but can be moved to another database using the following plugin configuration option:

```yaml
plugins:
  datasette-events-db:
    database: my_database
```

The table will be created when Datasette starts up, if it does not already exist.

## Table schema

```sql
create table if not exists datasette_events (
    id integer primary key,
    event text,
    created text,
    actor_id text,
    database_name text,
    table_name text,
    properties text -- JSON other properties
)
```
- `event` is the text name of the event, for example `create-table`
- `created` is an ISO formatted UTC timestamp
- `actor_id` will be populated with the ID of the responsible actor, or `null` if not available
- `database_name` will be the `database` property recorded by the event, if present
- `table_name` will be the `table` property recorded by the event, if present
- `properties` will be a JSON object containing any other properties recorded by the event

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-events-db
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
