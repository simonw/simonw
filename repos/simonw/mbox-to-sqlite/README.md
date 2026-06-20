# mbox-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/mbox-to-sqlite.svg)](https://pypi.org/project/mbox-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/mbox-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/mbox-to-sqlite/releases)
[![Tests](https://github.com/simonw/mbox-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/mbox-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/mbox-to-sqlite/blob/master/LICENSE)

Load email from .mbox files into SQLite

## Installation

Install this tool using `pip`:

    pip install mbox-to-sqlite

## Usage

Use the `mbox` command to import a `.mbox` file into a SQLite database:

    mbox-to-sqlite mbox emails.db path/to/messages.mbox

You can try this out against an example containing a sample of 3,266 emails from the [Enron corpus](https://en.wikipedia.org/wiki/Enron_Corpus) like this:

    curl -O https://raw.githubusercontent.com/ivanhb/EMA/master/server/data/mbox/enron/mbox-enron-white-s-all.mbox
    mbox-to-sqlite mbox enron.db mbox-enron-white-s-all.mbox

You can then explore the resulting database using [Datasette](https://datasette.io/):

    datasette enron.db

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd mbox-to-sqlite
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
