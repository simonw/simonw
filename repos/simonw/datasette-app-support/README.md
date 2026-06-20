# datasette-app-support

[![PyPI](https://img.shields.io/pypi/v/datasette-app-support.svg)](https://pypi.org/project/datasette-app-support/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-app-support?include_prereleases&label=changelog)](https://github.com/simonw/datasette-app-support/releases)
[![Tests](https://github.com/simonw/datasette-app-support/workflows/Test/badge.svg)](https://github.com/simonw/datasette-app-support/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-app-support/blob/main/LICENSE)

Part of https://github.com/simonw/datasette-app

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-app-support

Using this outside of the context of `Datasette.app` probably won't work.

## API endpoints

This plugin exposes APIs that are called by the Electron wrapper.

All plugins are protected by authentication: they need to be called with a `Authorization: Bearer xxx` token here the `xxx` matches the value of the `DATASETTE_API_TOKEN` environment variable.

### /-/auth-app-user

```
POST /-/auth-app-user
{"redirect": "/-/metadata"}
```
If a valid `Authorization` header is passed, sets a signed cookie identifying the user as `{"id": "admin"}` and redirects them to the specified page.

### /-/open-database-file

```
POST /-/open-database-file
{"path": "/path/to/file.db"}
```
Attaches a new database file to the running Datasette instance - used by the "Open Database..." menu option.

Returns HTTP 200 status with `{"ok": True, "path": "/file"}` if it works, 400 with an `"error"` JSON string message if it fails.

### /-/new-empty-database-file

```
POST /-/new-empty-database-file
{"path": "/path/to/file.db"}
```
Creates a brand new empty SQLite database file at the specified path and attaches it to the Datasette instance. Used by the "Create Empty Database..." menu option.

Returns HTTP 200 status with `{"ok": True, "path": "/file"}` if it works, 400 with an `"error"` JSON string message if it fails.

### /-/open-csv-file

```
POST /-/open-csv-file
{"path": "/path/to/file.csv"}
```
Imports a CSV or TSV file into the default `/temporary` in-memory database. Used by the "Open CSV..." menu option.

Returns HTTP 200 status with `{"ok": True, "path": "/temporary/table"}` if it works, 400 or 500 with an `"error"` JSON string message if it fails.

### /-/import-csv-file

```
POST /-/import-csv-file
{"path": "/path/to/file.csv", "database": "database_name"}
```
Permanently imports a CSV or TSV file into the specified database. Used by the "Import CSV..." menu option.

Returns HTTP 200 status with `{"ok": True, "path": "/database_name/table"}` if it works, 400 or 500 with an `"error"` JSON string message if it fails.

### /-/open-csv-from-url

```
POST /-/open-csv-from-url
{"url": "https://example.com/file.csv", "table_name": "My_suggested_table_name"}
```
Imports a CSV file into the default `/temporary` in-memory database. Used by the "Open CSV from URL..." menu option. `table_name` is optional - if omitted the name to use will be derived from the URL.

Returns HTTP 200 status with `{"ok": True, "path": "/temporary/table"}` if it works, 400 or 500 with an `"error"` JSON string message if it fails.

### /-/dump-temporary-to-file

```
POST /-/dump-temporary-to-file
{"path": "/path/to/backup.db"}
```
Dumps the contents of the `temporary` in-memory database to the specified file. This is intended to be used to take a temporary backup when the Datasette server is restarted after a plugin has been installed, see [datasette-app/issues/42](https://github.com/simonw/datasette-app/issues/42).

Returns HTTP 200 status with `{"ok": True, "path": "/path/to/backup.db"}` if it works, 400 or 500 with an `"error"` JSON string message if it fails.

### /-/restore-temporary-to-file

```
POST /-/restore-temporary-from-file
{"path": "/path/to/backup.db"}
```
Restores the `temporary` in-memory database to the contents of the specified file.

Returns HTTP 200 status with `{"ok": True, "path": "/path/to/backup.db"}` if it works, 400 or 500 with an `"error"` JSON string message if it fails.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-app-support
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
