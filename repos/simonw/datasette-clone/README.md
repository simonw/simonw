# datasette-clone

[![PyPI](https://img.shields.io/pypi/v/datasette-clone.svg)](https://pypi.org/project/datasette-clone/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-clone?include_prereleases&label=changelog)](https://github.com/simonw/datasette-clone/releases)
[![Tests](https://github.com/simonw/datasette-clone/workflows/Test/badge.svg)](https://github.com/simonw/datasette-clone/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-clone/blob/main/LICENSE)

Create a local copy of database files from a Datasette instance.

See [datasette-clone](https://simonwillison.net/2020/Apr/14/datasette-clone/) on my blog for background on this project.

## How to install

    $ pip install datasette-clone

## Usage

This only works against Datasette instances running immutable databases (with the `-i` option). Databases published using the `datasette publish` command should be compatible with this tool.

To download copies of all `.db` files from an instance, run:

    datasette-clone https://latest.datasette.io

You can provide an optional second argument to specify a directory:

    datasette-clone https://latest.datasette.io /tmp/here-please

The command stores its own copy of a `databases.json` manifest and uses it to only download databases that have changed the next time you run the command.

It also stores a copy of the instance's `metadata.json` to ensure you have a copy of any source and licensing information for the downloaded databases.

If your instance is protected by an API token, you can use `--token` to provide it:

    datasette-clone https://latest.datasette.io --token=xyz

For verbose output showing what the tool is doing, use `-v`.
