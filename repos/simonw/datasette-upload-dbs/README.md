# datasette-upload-dbs

[![PyPI](https://img.shields.io/pypi/v/datasette-upload-dbs.svg)](https://pypi.org/project/datasette-upload-dbs/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-upload-dbs?include_prereleases&label=changelog)](https://github.com/simonw/datasette-upload-dbs/releases)
[![Tests](https://github.com/simonw/datasette-upload-dbs/workflows/Test/badge.svg)](https://github.com/simonw/datasette-upload-dbs/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-upload-dbs/blob/main/LICENSE)

Upload SQLite database files to Datasette

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-upload-dbs

## Configuration

This plugin requires Datasette 1.0a38 or higher.

You will need to configure a directory in which uploaded files will be stored.

On startup, Datasette will automatically load any SQLite files that it finds in that directory. This means it is safe to restart your server in between file uploads.

To configure the directory as `/home/datasette/uploads`, add this to a `datasette.yml` configuration file:

```yaml
plugins:
  datasette-upload-dbs:
    directory: /home/datasette/uploads
```

Or if you are using `datasette.json`:

```json
{
  "plugins": {
    "datasette-upload-dbs": {
      "directory": "/home/datasette/uploads"
    }
  }
}
```
You can use `"."` for the current folder when the server starts, or `"uploads"` for a folder relative to that folder. The folder will be created on startup if it does not already exist.

Then start Datasette like this:

    datasette -c datasette.yml

The plugin defaults to loading all databases in the configured directory.

You can disable this by adding the following setting:
```
"skip_startup_scan": true
```

Uploads are unlimited in size by default. To enforce a maximum size, set the `max_file_size_mb` option - uploads larger than this will be rejected with an HTTP 413 error:

```yaml
plugins:
  datasette-upload-dbs:
    directory: /home/datasette/uploads
    max_file_size_mb: 100
```
## Usage

Only users with the `upload-dbs` permission will be able to upload files. The `root` user has this permission by default - other users can be granted access using permission plugins, see the [Permissions](https://docs.datasette.io/en/stable/authentication.html#permissions) documentation for details.

To start Datasette as the root user, run this:

    datasette -c datasette.yml --root

And follow the link that is displayed on the console.

If a user has that permission they will see an "Upload database" link in the navigation menu.

This will take them to `/-/upload-dbs` where they will be able to upload database files, by selecting them or by dragging them onto the drop area.

![Animated demo showing a file being dropped onto a box, then uploading and redirecting to the database page](https://github.com/simonw/datasette-upload-dbs/raw/main/upload-demo.gif)

## API

Databases can also be uploaded programmatically, for example at the end of a script or CI workflow that builds a SQLite file.

First create an API token that is allowed to perform the `upload-dbs` action. Signed-in users can create one using the form at `/-/create-token`, or you can use a plugin such as [datasette-auth-tokens](https://datasette.io/plugins/datasette-auth-tokens) to issue tokens.

Then send a `multipart/form-data` POST to `/-/upload-dbs` with these fields:

- `db` - the SQLite database file
- `db_name` - optional name for the database. If omitted, the name will be derived from the uploaded filename.

Include the token in an `Authorization: Bearer` header. Requests authenticated with a bearer token are exempt from Datasette's cross-origin (CSRF) protection.

Send an `Accept: application/json` header to receive JSON responses:

```bash
curl -X POST \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Accept: application/json" \
  -F "db=@fixtures.db" \
  -F "db_name=fixtures" \
  https://your-instance.example.com/-/upload-dbs
```

A successful upload returns a `200` status with the name Datasette assigned to the database - this may differ from the requested `db_name`, since invalid characters are replaced:

```json
{
  "ok": true,
  "database": "fixtures",
  "redirect": "/fixtures"
}
```

Uploading a file with the same name as an existing database will replace that database. Uploads are written to a temporary file and validated before being atomically moved into place, so a failed or invalid upload will never damage the existing database.

Errors return `{"ok": false, "error": "..."}` with an appropriate status code:

- `400` if the file is missing or not a valid SQLite database
- `403` if the request is not authorized to perform the `upload-dbs` action
- `413` if the file exceeds the configured `max_file_size_mb`

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-upload-dbs
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
