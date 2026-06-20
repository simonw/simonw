# datasette-insert-unsafe

[![PyPI](https://img.shields.io/pypi/v/datasette-insert-unsafe.svg)](https://pypi.org/project/datasette-insert-unsafe/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-insert-unsafe?include_prereleases&label=changelog)](https://github.com/simonw/datasette-insert-unsafe/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-insert-unsafe/blob/master/LICENSE)

Unsafe permissions for datasette-insert - allows all actions without authentication

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-insert-unsafe

## Usage

Once installed, all actions performed using [datasette-insert](https://github.com/simonw/datasette-insert) will be allowed without authentication.

This is **not safe** if you are running Datasette with `datasette-insert` on the public internet. You should only use this plugin if you are running Datasette on your own local machine, or on a private network.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-insert-unsafe
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
