# datasette-explain

[![PyPI](https://img.shields.io/pypi/v/datasette-explain.svg)](https://pypi.org/project/datasette-explain/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-explain?include_prereleases&label=changelog)](https://github.com/simonw/datasette-explain/releases)
[![Tests](https://github.com/simonw/datasette-explain/workflows/Test/badge.svg)](https://github.com/simonw/datasette-explain/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-explain/blob/main/LICENSE)

Explain SQL queries executed using Datasette

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-explain
```
## Usage

The plugin adds JavaScript to the query editor page which will constantly update the page with information gained from running EXPLAIN QUERY PLAN queries against the entered SQL.

This may result in an error message, or it may show the query plan along with any tables used by the query.

## Demo

You can see this plugin in action on [datasette.simonwillison.net](https://datasette.simonwillison.net/simonwillisonblog?sql=select%0D%0A++blog_tag.tag%2C%0D%0A++blog_blogmark.link_title%2C%0D%0A++blog_blogmark.link_url%0D%0Afrom%0D%0A++blog_blogmark_tags%0D%0A++join+blog_tag+on+tag_id+%3D+blog_tag.id%0D%0A++join+blog_blogmark+on+blog_blogmark_tags.blogmark_id+%3D+blog_blogmark.id%0D%0Aorder+by+blog_blogmark.id+desc).

<img src="https://raw.githubusercontent.com/simonw/datasette-explain/main/datasette-explain-screenshot.jpg" alt="Demo of this plugin - a SQL query shows the explain plan as well as the three tables that were used in the query (their names and columns)" width="832">

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-explain
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
