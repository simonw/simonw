# datasette-plugin-template-repository-demo

[![PyPI](https://img.shields.io/pypi/v/datasette-plugin-template-repository-demo.svg)](https://pypi.org/project/datasette-plugin-template-repository-demo/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-plugin-template-repository-demo?include_prereleases&label=changelog)](https://github.com/simonw/datasette-plugin-template-repository-demo/releases)
[![Tests](https://github.com/simonw/datasette-plugin-template-repository-demo/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/datasette-plugin-template-repository-demo/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-plugin-template-repository-demo/blob/main/LICENSE)

Demo of datasette-plugin-template-repository

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-plugin-template-repository-demo
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-plugin-template-repository-demo
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
