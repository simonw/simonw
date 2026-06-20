# iam-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/iam-to-sqlite.svg)](https://pypi.org/project/iam-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/iam-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/iam-to-sqlite/releases)
[![Tests](https://github.com/simonw/iam-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/iam-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/iam-to-sqlite/blob/master/LICENSE)

Load Amazon IAM data into a SQLite database

## Installation

Install this tool using `pip`:

    $ pip install iam-to-sqlite

You will also need the `aws` command-line tool. Here are [the installation instructions](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) for that.

## Usage

Run this tool like so:

    iam-to-sqlite iam.db

This will create a SQLite database called `iam.db` containing the following tables:

- `Groups`
- `Policies`
- `Users`
- `Roles`

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd iam-to-sqlite
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
