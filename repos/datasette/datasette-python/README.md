# datasette-python

[![PyPI](https://img.shields.io/pypi/v/datasette-python.svg)](https://pypi.org/project/datasette-python/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-python?include_prereleases&label=changelog)](https://github.com/datasette/datasette-python/releases)
[![Tests](https://github.com/datasette/datasette-python/workflows/Test/badge.svg)](https://github.com/datasette/datasette-python/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-python/blob/main/LICENSE)

Run a Python interpreter in the Datasette virtual environment

## Installation

Install this plugin in the same environment as [Datasette](https://datasette.io/).
```bash
datasette install datasette-python
```
## Usage

This plugin adds a new `python` command to Datasette. This executes Python in the same virtual environment as Datasette itself.

You can use this to check the Python version

```bash
datasette python --version
# Should output 'Python 3.12.4' or similar
```
Or  to run commands like `pip`:
```bash
datasette python -m pip install httpx
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-python
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
