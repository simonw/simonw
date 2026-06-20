# dclient

[![PyPI](https://img.shields.io/pypi/v/dclient.svg)](https://pypi.org/project/dclient/)
[![Changelog](https://img.shields.io/github/v/release/simonw/dclient?include_prereleases&label=changelog)](https://github.com/simonw/dclient/releases)
[![Tests](https://github.com/simonw/dclient/workflows/Test/badge.svg)](https://github.com/simonw/dclient/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/dclient/blob/master/LICENSE)

A client CLI utility for [Datasette](https://datasette.io/) instances.

Much of the functionality requires Datasette 1.0a2 or higher.

## Things you can do with dclient

- Browse table data with filtering, sorting, and pagination — no SQL required
- Run SQL queries against Datasette and return the results as JSON, CSV, TSV, or an ASCII table
- Introspect databases, tables, plugins, and schema
- Run queries against authenticated Datasette instances
- Create aliases and set default instances/databases for convenient access
- Insert and upsert data using the [write API](https://docs.datasette.io/en/latest/json_api.html#the-json-write-api) (Datasette 1.0 alpha or higher)

## Installation

Install this tool using `pip`:
```bash
pip install dclient
```
If you want to install it in the same virtual environment as Datasette (to use it as a plugin) you can instead run:
```bash
datasette install dclient
```
## Quick start

Add an alias for a Datasette instance:
```bash
dclient alias add latest https://latest.datasette.io
dclient default instance latest
dclient default database latest fixtures
```
Now run queries directly:
```bash
dclient "select * from facetable limit 1"
```
Or be explicit:
```bash
dclient query fixtures "select * from facetable limit 1" -i latest
```
Output as a table with `-t`, or use `--csv`, `--tsv`, `--nl`:
```bash
dclient "select pk, state from facetable limit 3" -t
```
Browse table rows without SQL:
```bash
dclient rows facetable -f state eq CA --sort _city_id -t
```

## Introspection

```bash
dclient databases
dclient tables
dclient plugins
dclient schema facetable
```

## Documentation

Visit **[dclient.datasette.io](https://dclient.datasette.io)** for full documentation on using this tool.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd dclient
python -m venv venv
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
