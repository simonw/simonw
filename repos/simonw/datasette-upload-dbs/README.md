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

This plugin requires you to configure a directory in which uploaded files will be stored.

On startup, Datasette will automatically load any SQLite files that it finds in that directory. This means it is safe to restart your server in between file uploads.

To configure the directory as `/home/datasette/uploads`, add this to a `metadata.yml` configuration file:

```yaml
plugins:
  datasette-upload-dbs:
    directory: /home/datasette/uploads
```

Or if you are using `metadata.json`:

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

    datasette -m metadata.yml

The plugin defaults to loading all databases in the configured directory.

You can disable this by adding the following setting:
```
"skip_startup_scan": true
```
## Usage

Only users with the `upload-dbs` permission will be able to upload files. The `root` user has this permission by default - other users can be granted access using permission plugins, see the [Permissions](https://docs.datasette.io/en/stable/authentication.html#permissions) documentation for details.

To start Datasette as the root user, run this:

    datasette -m metadata.yml --root

And follow the link that is displayed on the console.

If a user has that permission they will see an "Upload database" link in the navigation menu.

This will take them to `/-/upload-dbs` where they will be able to upload database files, by selecting them or by dragging them onto the drop area.

![Animated demo showing a file being dropped onto a box, then uploading and redirecting to the database page](https://github.com/simonw/datasette-upload-dbs/raw/main/upload-demo.gif)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-upload-dbs
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
