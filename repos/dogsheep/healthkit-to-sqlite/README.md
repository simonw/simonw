# healthkit-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/healthkit-to-sqlite.svg)](https://pypi.org/project/healthkit-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/dogsheep/healthkit-to-sqlite?include_prereleases&label=changelog)](https://github.com/dogsheep/healthkit-to-sqlite/releases)
[![Tests](https://github.com/dogsheep/healthkit-to-sqlite/workflows/Test/badge.svg)](https://github.com/dogsheep/healthkit-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dogsheep/healthkit-to-sqlite/blob/main/LICENSE)

Convert an Apple Healthkit export zip to a SQLite database

## How to install

    $ pip install healthkit-to-sqlite

## How to use

First you need to export your Apple HealthKit data.

1. On your iPhone, open the "Health" app
2. Click the profile icon in the top right
3. Click "Export Health Data" at the bottom of that page
4. Save the resulting file somewhere you can access it, or AirDrop it directly to your laptop.

Now you can convert the resulting `export.zip` file to SQLite like so:

    $ healthkit-to-sqlite export.zip healthkit.db

A progress bar will be displayed. You can disable this using `--silent`.

```
Importing from HealthKit  [#-------------]    5%  00:01:33
```

You can explore the resulting data using [Datasette](https://datasette.readthedocs.io/) like this:

    $ datasette healthkit.db
