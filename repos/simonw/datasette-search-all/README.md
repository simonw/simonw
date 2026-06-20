# datasette-search-all

[![PyPI](https://img.shields.io/pypi/v/datasette-search-all.svg)](https://pypi.org/project/datasette-search-all/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-search-all?include_prereleases&label=changelog)](https://github.com/simonw/datasette-search-all/releases)
[![Tests](https://github.com/simonw/datasette-search-all/workflows/Test/badge.svg)](https://github.com/simonw/datasette-search-all/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-search-all/blob/main/LICENSE)

Datasette plugin for searching all searchable tables at once.

## Installation

Install the plugin in the same Python environment as Datasette:

    pip install datasette-search-all

## Background

See [datasette-search-all: a new plugin for searching multiple Datasette tables at once](https://simonwillison.net/2020/Mar/9/datasette-search-all/) for background on this project. You can try the plugin out at https://fara.datasettes.com/

## Usage

This plugin only works if at least one of the tables connected to your Datasette instance has been configured for SQLite's full-text search.

The [Datasette search documentation](https://docs.datasette.io/en/stable/full_text_search.html) includes details on how to enable full-text search for a table.

You can also use the following tools:

* [sqlite-utils](https://sqlite-utils.datasette.io/en/stable/cli.html#configuring-full-text-search) includes a command-line tool for enabling full-text search.
* [datasette-enable-fts](https://github.com/simonw/datasette-enable-fts) is a Datasette plugin that adds a web interface for enabling search for specific columns.

If the plugin detects at least one searchable table it will add a search form to the homepage.

You can also navigate to `/-/search` on your Datasette instance to use the search interface directly.

## Screenshot

![Animated screenshot showing the plugin in action](https://raw.githubusercontent.com/simonw/datasette-search-all/main/animated-screenshot.gif)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-search-all
python -m venv venv
source venv/bin/activate
```
Or if you are using `pipenv`:
```bash
pipenv shell
```
Now install the dependencies and tests:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
To run the browser automation tests:
```bash
pip install -e '.[test,playwright]'
pytest
```
