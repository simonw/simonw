# datasette-insecure-auth-as-root

[![PyPI](https://img.shields.io/pypi/v/datasette-insecure-auth-as-root.svg)](https://pypi.org/project/datasette-insecure-auth-as-root/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-insecure-auth-as-root?include_prereleases&label=changelog)](https://github.com/simonw/datasette-insecure-auth-as-root/releases)
[![Tests](https://github.com/simonw/datasette-insecure-auth-as-root/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/datasette-insecure-auth-as-root/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-insecure-auth-as-root/blob/main/LICENSE)

Extremely unsafe plugin: every Datasette visitor is treated as the root user

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-insecure-auth-as-root
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-insecure-auth-as-root
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
