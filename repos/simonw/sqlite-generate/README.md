# sqlite-generate

[![PyPI](https://img.shields.io/pypi/v/sqlite-generate.svg)](https://pypi.org/project/sqlite-generate/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-generate?label=changelog)](https://github.com/simonw/sqlite-generate/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-generate/blob/master/LICENSE)

Tool for generating demo SQLite databases

## Installation

Install this plugin using `pip`:

    $ pip install sqlite-generate

## Demo

You can see a demo of the database generated using this command running in [Datasette](https://github.com/simonw/datasette) at https://sqlite-generate-demo.datasette.io/

The demo is generated using the following command:

    sqlite-generate demo.db --seed seed --fts --columns=10 --fks=0,3 --pks=0,2

## Usage

To generate a SQLite database file called `data.db` with 10 randomly named tables in it, run the following:

    sqlite-generate data.db

You can use the `--tables` option to generate a different number of tables:

    sqlite-generate data.db --tables 20

You can run the command against the same database file multiple times to keep adding new tables, using different settings for each batch of generated tables.

By default each table will contain a random number of rows between 0 and 200. You can customize this with the `--rows` option:

    sqlite-generate data.db --rows 20

This will insert 20 rows into each table.

    sqlite-generate data.db --rows 500,2000

This inserts a random number of rows between 500 and 2000 into each table.

Each table will have 5 columns. You can change this using `--columns`:

    sqlite-generate data.db --columns 10

`--columns` can also accept a range:

    sqlite-generate data.db --columns 5,15

You can control the random number seed used with the `--seed` option. This will result in the exact same database file being created by multiple runs of the tool:

    sqlite-generate data.db --seed=myseed

By default each table will contain between 0 and 2 foreign key columns to other tables. You can control this using the `--fks` option, with either a single number or a range:

    sqlite-generate data.db --columns=20 --fks=5,15

Each table will have a single primary key column called `id`. You can use the `--pks=` option to change the number of primary key columns on each table. Drop it to 0 to generate [rowid tables](https://www.sqlite.org/rowidtable.html). Increase it above 1 to generate tables with compound primary keys. Or use a range to get a random selection of different primary key layouts:

    sqlite-generate data.db --pks=0,2

To configure [SQLite full-text search](https://www.sqlite.org/fts5.html) for all columns of type text, use `--fts`:

    sqlite-generate data.db --fts

This will use FTS5 by default. To use [FTS4](https://www.sqlite.org/fts3.html) instead, use `--fts4`.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd sqlite-generate
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
