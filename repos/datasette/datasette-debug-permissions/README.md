# datasette-debug-permissions

[![PyPI](https://img.shields.io/pypi/v/datasette-debug-permissions.svg)](https://pypi.org/project/datasette-debug-permissions/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-debug-permissions?include_prereleases&label=changelog)](https://github.com/datasette/datasette-debug-permissions/releases)
[![Tests](https://github.com/datasette/datasette-debug-permissions/workflows/Test/badge.svg)](https://github.com/datasette/datasette-debug-permissions/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-debug-permissions/blob/main/LICENSE)

A Datasette plugin that outputs debug information about permission checks.

## Installation

```bash
datasette install datasette-debug-permissions
```

## Usage

This plugin adds debugging output to standard error as Datasette is running showing any times the `permission_allowed()` plugin hook is called.

See [Authentication and permissions](https://docs.datasette.io/en/stable/authentication.html) in the Datasette documentation for more on why this is useful.

## Example output

```
INFO:     Uvicorn running on http://127.0.0.1:8434 (Press CTRL+C to quit)
permission_allowed: action=view-instance, resource=<None>, actor=<None>

  File "/datasette/views/base.py", line 134, in view
    return await self.dispatch_request(request)

  File "/datasette/views/base.py", line 91, in dispatch_request
    return await handler(request)

  File "/datasette/views/index.py", line 23, in get
    await self.ds.ensure_permissions(request.actor, ["view-instance"])

permission_allowed: action=view-database, resource=_memory, actor=<None>

  File "/datasette/views/base.py", line 91, in dispatch_request
    return await handler(request)

  File "/datasette/views/index.py", line 26, in get
    database_visible, database_private = await self.ds.check_visibility(

  File "/datasette/app.py", line 760, in check_visibility
    await self.ensure_permissions(actor, permissions)
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-debug-permissions
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
