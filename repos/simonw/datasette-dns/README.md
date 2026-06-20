# datasette-dns

[![PyPI](https://img.shields.io/pypi/v/datasette-dns.svg)](https://pypi.org/project/datasette-dns/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-dns?include_prereleases&label=changelog)](https://github.com/simonw/datasette-dns/releases)
[![Tests](https://github.com/simonw/datasette-dns/workflows/Test/badge.svg)](https://github.com/simonw/datasette-dns/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-dns/blob/main/LICENSE)

Custom SQL function for making DNS lookups

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-dns

## Usage

So far the only supported SQL function is:

    select dns_txt("oreilly.com");

Try this out in [the live demo](https://datasette-dns-demo.vercel.app/empty?sql=select+dns_txt%28%22oreilly.com%22%29%3B).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-dns
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
