# datasette-export

[![PyPI](https://img.shields.io/pypi/v/datasette-export.svg)](https://pypi.org/project/datasette-export/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-export?include_prereleases&label=changelog)](https://github.com/simonw/datasette-export/releases)
[![Tests](https://github.com/simonw/datasette-export/workflows/Test/badge.svg)](https://github.com/simonw/datasette-export/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-export/blob/main/LICENSE)

Export pages from Datasette to files on disk

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-export

## Usage

This plugin adds a new `export` command. You can use this to export one or more pages from Datasette to files on disk.

Pass the `--path` option one or more times to specify pages:

    datasette export mydata.db --path / --path /mydata.json --path /mydata/table1.csv

This will create an `export/` directory and save the following files to it:

- `index.html`
- `mydata.json`
- `mydata/table1.csv`

Use `--output` to specify an alternative directory for the export:

    datasette export mydata.db --path / --output mywebsite/

In addition to specifying paths, you can pass one or more SQL queries that can return lists of pages to be exported:

    datasette export mydata.db --sql "select path from pages"

For example, to export JSON for every row in the `fixtures/facetable` table:

    datasette export fixtures.db \
      --sql "select '/fixtures/facetable/' || pk || '.json' from facetable"

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-export
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
