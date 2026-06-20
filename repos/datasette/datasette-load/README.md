# datasette-load

[![PyPI](https://img.shields.io/pypi/v/datasette-load.svg)](https://pypi.org/project/datasette-load/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-load?include_prereleases&label=changelog)](https://github.com/datasette/datasette-load/releases)
[![Tests](https://github.com/datasette/datasette-load/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-load/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-load/blob/main/LICENSE)

API and UI for bulk loading data into Datasette from a URL

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-load
```

## Configuration

This plugin does not require configuration - by default it downloads files to the system temp directory and swaps them into the current working directory once they have been verified as valid SQLite.

The plugin provides two optional settings to control which directories are used here:

```yaml
plugins:
  datasette-load:
    staging_directory: /tmp
    database_directory: /home/location
```

`staging_directory` is used for the initial download. Files will be deleted from here if the download fails.

If the download succeeds (and the database integrity check passes) the file will be moved into the `database_directory` folder. This defaults to the directory in which the Datasette application was started if you do not otherwise configure it.

To enable WAL mode on the database once it has been saved to the `database_directory` include the `enable_wal: true` option:

```yaml
plugins:
  datasette-load:
    database_directory: /home/location
    enable_wal: true
```

## Usage

Users and API tokens with the `datasette-load` permission can visit `/-/load` where they can provide a URL to a SQLite database file and the name it should use within Datasette to trigger a download of that SQLite database.

You can assign that permission to the `root` user by starting Datasette like this:

```bash
datasette -s permissions.datasette-load.id root --root
```
Or with the following configuration in the `datasette -c datasette.yaml` file:
```yaml
permissions:
  datasette-load:
    id: root
```
API tokens with that permission can use this API:

```
POST /-/load
{"url": "https://s3.amazonaws.com/til.simonwillison.net/tils.db", "name": "tils"}
```
You can optionally include additional HTTP headers to be used when fetching the URL:
```
POST /-/load
{
  "url": "https://example.com/db.sqlite",
  "name": "db",
  "headers": {"Authorization": "Bearer XXX"}
}
```
This tells Datasette to download the SQLite database from the given URL and use it to create (or replace) the `/tils` database in the Datasette instance.

That API endpoint returns:
```json
{
  "id": "1D2A2328-199E-4D4D-AF3B-967131ADB795",
  "url": "https://s3.amazonaws.com/til.simonwillison.net/tils.db",
  "name": "tils",
  "done": false,
  "error": null,
  "todo_bytes": 20250624,
  "done_bytes": 0,
  "status_url": "https://blah.datasette/-/load/status/1D2A2328-199E-4D4D-AF3B-967131ADB795"
}
```
The `status_url` can be polled for completion. It will return the same JSON format.

When the download has finished the API will return `"done": true` and either `"error": null` if it worked or `"error": "error description"` if something went wrong.

## Zip support

The URL can point to either a SQLite database file or a zip file containing a SQLite database - if a zip file is provided, the largest file in the archive will be extracted and used (after verifying it is a valid SQLite database). For security, the plugin will reject zip files where the largest file would extract to more than 5x the size of the zip file itself.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-load
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
