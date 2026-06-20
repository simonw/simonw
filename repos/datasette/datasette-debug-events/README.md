# datasette-debug-events

[![PyPI](https://img.shields.io/pypi/v/datasette-debug-events.svg)](https://pypi.org/project/datasette-debug-events/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-debug-events?include_prereleases&label=changelog)](https://github.com/datasette/datasette-debug-events/releases)
[![Tests](https://github.com/datasette/datasette-debug-events/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-debug-events/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-debug-events/blob/main/LICENSE)

Print Datasette events to standard error

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-debug-events
```
## Usage

Once installed, any events fired by the [Datasette events mechanism](https://docs.datasette.io/en/latest/events.html) (introduced [in Datasette 1.0a8](https://simonwillison.net/2024/Feb/7/datasette-1a8/#datasette-events)) will be sent to standard error and should display in your terminal.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-debug-events
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
