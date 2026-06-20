# datasette-table-diagram

[![PyPI](https://img.shields.io/pypi/v/datasette-table-diagram.svg)](https://pypi.org/project/datasette-table-diagram/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-table-diagram?include_prereleases&label=changelog)](https://github.com/datasette/datasette-table-diagram/releases)
[![Tests](https://github.com/datasette/datasette-table-diagram/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-table-diagram/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-table-diagram/blob/main/LICENSE)

Show Entity Relationship diagrams of tables in Datasette

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-table-diagram
```
## Usage

Databases gain a new database action menu item called "Table diagram", which links to a page that displays Mermaid Entity Relationship diagrams of the tables in that database.

These diagrams can be panned and zoomed, or users can click a table name to zoom to that table and its relationships.

Users will only see tables that they have permission to view.

![Screenshot of a diagram of the fixtures.db table - tables are joined by curved lines, there is a + / - / reset button and a list of tables.](https://raw.githubusercontent.com/datasette/datasette-table-diagram/refs/heads/main/screenshot.png)

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-table-diagram
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
