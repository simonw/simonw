# genome-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/genome-to-sqlite.svg)](https://pypi.org/project/genome-to-sqlite/)
[![CircleCI](https://circleci.com/gh/dogsheep/genome-to-sqlite.svg?style=svg)](https://circleci.com/gh/dogsheep/genome-to-sqlite)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dogsheep/genome-to-sqlite/blob/master/LICENSE)

Import your genome into a SQLite database.

## How to install

    $ pip install genome-to-sqlite

## How to use

First, export your genome. This tool has only been tested against 23andMe so far. You can request an export of your genome from https://you.23andme.com/tools/data/download/

Now you can convert the resulting `export.zip` file to SQLite like so:

    $ genome-to-sqlite export.zip genome.db

A progress bar will be displayed. You can disable this using `--silent`.

```
Importing genome  [#----------------]    5%  00:01:33
```

You can explore the resulting data using [Datasette](https://datasette.readthedocs.io/) like this:

    $ datasette genome.db --config facet_time_limit_ms:1000

Bumping up the facet time limit is useful in order to enable faceting by chromosome:

http://127.0.0.1:8001/genome/genome?_facet=chromosome&_sort=position
