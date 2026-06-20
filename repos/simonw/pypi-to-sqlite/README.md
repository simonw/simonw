# pypi-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/pypi-to-sqlite.svg)](https://pypi.org/project/pypi-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/pypi-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/pypi-to-sqlite/releases)
[![Tests](https://github.com/simonw/pypi-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/pypi-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/pypi-to-sqlite/blob/master/LICENSE)

Load data about Python packages from PyPI into SQLite

## Installation

Install this tool using `pip`:

    pip install pypi-to-sqlite

## Usage

To create a SQLite database with details of one or more packages, run:

    pypi-to-sqlite pypi.db datasette sqlite-utils

You can also process JSON that you have previously saved to disk like so:

    curl -o datasette.json https://pypi.org/pypi/datasette/json
    pypi-to-sqlite pypi.db -f datasette.json

The tool will create three tables: `packages`, `versions` and `releases`. The full table schema is shown below.

To create the tables with a prefix, use `--prefix prefix`. For example:

    pypi-to-sqlite pypi.db datasette --prefix pypi_

This will create tables called `pypi_packages`, `pypi_versions` and `pypi_releases`.

## Demo

You can see examples of tables created using this tool running in [Datasette](https://datasette.io/) here:

- [packages](https://datasette.io/content/pypi_packages)
- [versions](https://datasette.io/content/pypi_versions)
- [releases](https://datasette.io/content/pypi_releases)

## Database schema

<!-- [[[cog
import cog, json
from pypi_to_sqlite import cli
from click.testing import CliRunner
import sqlite_utils
import tempfile, pathlib
tmpdir = pathlib.Path(tempfile.mkdtemp())
db_path = str(tmpdir / "pypi.db")
runner = CliRunner()
result = runner.invoke(cli.cli, [db_path, "-f", "tests/datasette-block.json"])
cog.out("```sql\n")
cog.out(sqlite_utils.Database(db_path).schema)
cog.out("\n```")
]]] -->
```sql
CREATE TABLE [packages] (
   [name] TEXT PRIMARY KEY,
   [summary] TEXT,
   [classifiers] TEXT,
   [description] TEXT,
   [author] TEXT,
   [author_email] TEXT,
   [description_content_type] TEXT,
   [home_page] TEXT,
   [keywords] TEXT,
   [license] TEXT,
   [maintainer] TEXT,
   [maintainer_email] TEXT,
   [package_url] TEXT,
   [platform] TEXT,
   [project_url] TEXT,
   [project_urls] TEXT,
   [release_url] TEXT,
   [requires_dist] TEXT,
   [requires_python] TEXT,
   [version] TEXT,
   [yanked] INTEGER,
   [yanked_reason] TEXT
);
CREATE TABLE [versions] (
   [id] TEXT PRIMARY KEY,
   [package] TEXT REFERENCES [packages]([name]),
   [name] TEXT
);
CREATE TABLE [releases] (
   [md5_digest] TEXT PRIMARY KEY,
   [package] TEXT REFERENCES [packages]([name]),
   [version] TEXT REFERENCES [versions]([id]),
   [packagetype] TEXT,
   [filename] TEXT,
   [comment_text] TEXT,
   [digests] TEXT,
   [has_sig] INTEGER,
   [python_version] TEXT,
   [requires_python] TEXT,
   [size] INTEGER,
   [upload_time] TEXT,
   [upload_time_iso_8601] TEXT,
   [url] TEXT,
   [yanked] INTEGER,
   [yanked_reason] TEXT
);
```
<!-- [[[end]]] -->

## pypi-to-sqlite --help

<!-- [[[cog
result = runner.invoke(cli.cli, ["--help"])
cog.out("```\n")
cog.out(result.output.replace("Usage: cli", "Usage: pypi-to-sqlite"))
cog.out("\n```")
]]] -->
```
Usage: pypi-to-sqlite [OPTIONS] DB_PATH [PACKAGE]...

  Load data about Python packages from PyPI into SQLite

  Usage example:

      pypi-to-sqlite pypy.db datasette sqlite-utils

  Use -f to load data from a JSON file instead:

      pypi-to-sqlite pypy.db -f datasette.json

  Created tables will be packages, versions and releases

  To create tables called pypi_packages, pypi_versions, pypi_releases use
  --prefix pypi_:

      pypi-to-sqlite pypy.db datasette sqlite-utils --prefix pypi_

Options:
  --version            Show the version and exit.
  -f, --file FILENAME  Import JSON from this file
  -d, --delay FLOAT    Wait this many seconds between requests
  --prefix TEXT        Prefix to use for the created database tables
  --help               Show this message and exit.

```
<!-- [[[end]]] -->

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd pypi-to-sqlite
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
