# datasette-preact

[![PyPI](https://img.shields.io/pypi/v/datasette-preact.svg)](https://pypi.org/project/datasette-preact/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-preact?include_prereleases&label=changelog)](https://github.com/datasette/datasette-preact/releases)
[![Tests](https://github.com/datasette/datasette-preact/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-preact/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-preact/blob/main/LICENSE)

A Datasette plugin that pre-bundles [Preact](https://github.com/preactjs/preact), for other frontend-heavy Datasette plugins

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-preact
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-preact
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
