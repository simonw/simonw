# datasette-import-table

[![PyPI](https://img.shields.io/pypi/v/datasette-import-table.svg)](https://pypi.org/project/datasette-import-table/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-import-table?include_prereleases&label=changelog)](https://github.com/datasette/datasette-import-table/releases)
[![Tests](https://github.com/datasette/datasette-import-table/workflows/Test/badge.svg)](https://github.com/datasette/datasette-import-table/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-import-table/blob/main/LICENSE)

Datasette plugin for importing tables from other Datasette instances

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-import-table

## Usage

Visit `/-/import-table` for the interface. Paste in the URL to a table page on another Datasette instance and click the button to import that table.

By default only [the root actor](https://datasette.readthedocs.io/en/stable/authentication.html#using-the-root-actor) can access the page - so you'll need to run Datasette with the `--root` option and click on the link shown in the terminal to sign in and access the page.

The `import-table` permission governs access. You can use permission plugins such as [datasette-permissions-sql](https://github.com/simonw/datasette-permissions-sql) to grant additional access to the write interface.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-import-table
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
