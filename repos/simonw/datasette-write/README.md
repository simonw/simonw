# datasette-write

[![PyPI](https://img.shields.io/pypi/v/datasette-write.svg)](https://pypi.org/project/datasette-write/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-write?label=changelog)](https://github.com/simonw/datasette-write/releases)
[![Tests](https://github.com/simonw/datasette-write/workflows/Test/badge.svg)](https://github.com/simonw/datasette-write/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-write/blob/master/LICENSE)

Datasette plugin providing a UI for writing to a database

## Installation

Install this plugin in the same environment as Datasette.
```bash
pip install datasette-write
```
## Usage

Having installed the plugin, visit `/db/-/write` on your Datasette instance to submit SQL queries that will be executed against a write connection to the specified database.

By default only the `root` user can access the page - so you'll need to run Datasette with the `--root` option and click on the link shown in the terminal to sign in and access the page.

The `datasette-write` permission governs access. You can use permission plugins such as [datasette-permissions-sql](https://github.com/simonw/datasette-permissions-sql) to grant additional access to the write interface.

Pass `?sql=...` in the query string to pre-populate the SQL editor with a query.

## Parameterized queries

SQL queries can include parameters like this:
```sql
insert into news (title, body)
    values (:title, :body_textarea)
```
These will be converted into form fields on the `/db/-/write` page.

If a parameter name ends with `_textarea` it will be rendered as a multi-line textarea instead of a text input.

If a parameter name ends with `_hidden` it will be rendered as a hidden input.

## Updating rows with SQL

On Datasette 1.0a13 and higher a row actions menu item will be added to the row page linking to a SQL query for updating that row, for users with the `datasette-write` permission.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-write
python3 -mvenv venv
source venv/bin/activate
```
Or if you are using `pipenv`:
```bash
pipenv shell
```
Now install the dependencies and tests:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
