# datasette-low-disk-space-hook

[![PyPI](https://img.shields.io/pypi/v/datasette-low-disk-space-hook.svg)](https://pypi.org/project/datasette-low-disk-space-hook/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-low-disk-space-hook?include_prereleases&label=changelog)](https://github.com/simonw/datasette-low-disk-space-hook/releases)
[![Tests](https://github.com/simonw/datasette-low-disk-space-hook/workflows/Test/badge.svg)](https://github.com/simonw/datasette-low-disk-space-hook/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-low-disk-space-hook/blob/main/LICENSE)

Datasette plugin providing the low_disk_space hook for other plugins to check for low disk space

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-low-disk-space-hook

You are unlikely to need to install this plugin directly though: it will usually be automatically be installed as a dependency of another plugin.

## Usage

This plugin adds a new plugin hook to Datasette called `low_disk_space(datasette=datasette)`.

It also adds a new `space_is_running_low(datasette)` utility function which can be called to check if the Datasette instance is running out of space:

```python
from datasette_low_disk_space_hook import space_is_running_low

if await space_is_running_low(datasette):
    print("Disk space is running low")
```
The idea is for plugins such as `datasette-upload-csvs` and `datasette-socrata` to call this hook before writing any new data into Datasette, to check if they should continue.

Other plugins can then implement the hook to warn when Datasette is running out of space.

Working together, this will help plugins avoid filling the disk entirely with data which could cause Datasette instances to crash.

## Implementing the hook

An implementation of this hook (in yet another plugin) looks like this:

```python
from datasette import hookimpl
import shutil

@hookimpl
def low_disk_space(self, datasette):
    usage = shutil.disk_usage("/mnt")
    # Fail at 95% or more used
    if (usage.used / usage.total) > 0.95:
        return True
```
The plugin can also return an `async` function if it needs to use `await` as part of its execution:
```python
from datasette import hookimpl
from somewhere import check_disk_usage_percentage_async

@hookimpl
def low_disk_space(self, datasette):
    async def inner():
        usage = await check_disk_usage_percentage_async("/mnt")
        if usage > 0.95:
            return True
    return inner
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-low-disk-space-hook
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
