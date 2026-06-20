# datasette-gunicorn

[![PyPI](https://img.shields.io/pypi/v/datasette-gunicorn.svg)](https://pypi.org/project/datasette-gunicorn/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-gunicorn?include_prereleases&label=changelog)](https://github.com/simonw/datasette-gunicorn/releases)
[![Tests](https://github.com/simonw/datasette-gunicorn/workflows/Test/badge.svg)](https://github.com/simonw/datasette-gunicorn/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-gunicorn/blob/main/LICENSE)

Run a [Datasette](https://datasette.io/) server using [Gunicorn](https://gunicorn.org/)

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-gunicorn

## Usage

The plugin adds a new `datasette gunicorn` command. This takes most of the same options as `datasette serve`, plus one more option for setting the number of Gunicorn workers to start:

`-w/--workers X` - set the number of workers. Defaults to 1.

To start serving a database using 4 workers, run the following:

    datasette gunicorn fixtures.db -w 4

It is advisable to switch your datasette [into WAL mode](https://til.simonwillison.net/sqlite/enabling-wal-mode) to get the best performance out of this configuration:

    sqlite3 fixtures.db 'PRAGMA journal_mode=WAL;'

Run `datasette gunicorn --help` for a full list of options (which are the same as `datasette serve --help`, with the addition of the new `-w` option).

## datasette gunicorn --help

Not all of the options to `datasette serve` are supported. Here's the full list of available options:

<!-- [[[cog
import cog
from datasette import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["gunicorn", "--help"])
help = result.output.replace("Usage: cli", "Usage: datasette")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: datasette gunicorn [OPTIONS] [FILES]...

  Start a Gunicorn server running to serve Datasette

Options:
  -i, --immutable PATH            Database files to open in immutable mode
  -h, --host TEXT                 Host for server. Defaults to 127.0.0.1 which
                                  means only connections from the local machine
                                  will be allowed. Use 0.0.0.0 to listen to all
                                  IPs and allow access from other machines.
  -p, --port INTEGER RANGE        Port for server, defaults to 8001. Use -p 0 to
                                  automatically assign an available port.
                                  [0<=x<=65535]
  --cors                          Enable CORS by serving Access-Control-Allow-
                                  Origin: *
  --load-extension PATH:ENTRYPOINT?
                                  Path to a SQLite extension to load, and
                                  optional entrypoint
  --inspect-file TEXT             Path to JSON file created using "datasette
                                  inspect"
  -m, --metadata FILENAME         Path to JSON/YAML file containing
                                  license/source metadata
  --template-dir DIRECTORY        Path to directory containing custom templates
  --plugins-dir DIRECTORY         Path to directory containing custom plugins
  --static MOUNT:DIRECTORY        Serve static files from this directory at
                                  /MOUNT/...
  --memory                        Make /_memory database available
  --config CONFIG                 Deprecated: set config option using
                                  configname:value. Use --setting instead.
  --setting SETTING...            Setting, see
                                  docs.datasette.io/en/stable/settings.html
  --secret TEXT                   Secret used for signing secure values, such as
                                  signed cookies
  --version-note TEXT             Additional note to show on /-/versions
  --help-settings                 Show available settings
  --create                        Create database files if they do not exist
  --crossdb                       Enable cross-database joins using the /_memory
                                  database
  --nolock                        Ignore locking, open locked files in read-only
                                  mode
  -w, --workers INTEGER           Number of Gunicorn workers  [default: 1]
  --help                          Show this message and exit.

```
<!-- [[[end]]] -->

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-gunicorn
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
