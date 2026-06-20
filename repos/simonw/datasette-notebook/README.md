# datasette-notebook

[![PyPI](https://img.shields.io/pypi/v/datasette-notebook.svg)](https://pypi.org/project/datasette-notebook/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-notebook?include_prereleases&label=changelog)](https://github.com/simonw/datasette-notebook/releases)
[![Tests](https://github.com/simonw/datasette-notebook/workflows/Test/badge.svg)](https://github.com/simonw/datasette-notebook/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-notebook/blob/main/LICENSE)

A markdown wiki and dashboarding system for Datasette

This is an **experimental alpha** and everything about it is likely to change.

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-notebook

## Usage

Start Datasette with a SQLite file called `notebook.db`:

    datasette notebook.db --create

Here the `--create` option will create that file if it does not yet exist.

Visit `/n` to create an index page. Visit `/n/name` to create a page with that name.

You can link to other pages using `[[WikiLink]]` syntax. This will create a link to `/n/WikiLink` - spaces will be converted to underscores, and you can link to nested pages such as `[[nested/page]]`.

## Configuration

You can use a file other than `notebook.db` by configuring it using `metadata.yml`. To use a database file called `otherfile.db` you would use this:

```yaml
plugins:
  datasette-notebook:
    database: otherfile
```
Then start Datasette like so:

    datasette otherfile.db


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-notebook
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
