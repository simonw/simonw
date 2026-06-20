# datasette-verify

[![PyPI](https://img.shields.io/pypi/v/datasette-verify.svg)](https://pypi.org/project/datasette-verify/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-verify?include_prereleases&label=changelog)](https://github.com/simonw/datasette-verify/releases)
[![Tests](https://github.com/simonw/datasette-verify/workflows/Test/badge.svg)](https://github.com/simonw/datasette-verify/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-verify/blob/main/LICENSE)

Verify that SQLite files can be opened using Datasette

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-verify

This plugin depends on [Datasette 0.59a2](https://github.com/simonw/datasette/releases/tag/0.59a2) or higher, as it uses the [register_commands()](https://docs.datasette.io/en/latest/plugin_hooks.html#plugin-hook-register-commands) plugin hook.

## Usage

To confirm that files can be opened by Datasette, run the following:

    datasette verify file1.db file2.db

You can pass one or more file paths.

The command will exit silently with a 0 exit code if the files are all valid SQLite databases that Datasette can open.

It will exit with a 1 exit code and display an error for the first file it finds that is not valid.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-verify
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
