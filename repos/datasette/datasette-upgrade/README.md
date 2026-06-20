# datasette-upgrade

[![PyPI](https://img.shields.io/pypi/v/datasette-upgrade.svg)](https://pypi.org/project/datasette-upgrade/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-upgrade?include_prereleases&label=changelog)](https://github.com/datasette/datasette-upgrade/releases)
[![Tests](https://github.com/datasette/datasette-upgrade/workflows/Test/badge.svg)](https://github.com/datasette/datasette-upgrade/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-upgrade/blob/main/LICENSE)

Upgrade Datasette instance configuration to handle new features

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-upgrade
```
## Usage

The plugin currently provides one command, which will split an old style `metadata.json` or `metadata.yml` file - which contains both metadata and plugin configuration and permissions, into a Datasette 1.0+ `metadata.yml` file and a `datasette.yml` file.

```bash
datasette upgrade metadata-to-config metadata.json -m metadata.yml -c datasette.yml
```
This will leave `metadata.json` in place, but will write out `metadata.yml` and `datasette.yml` as two new files.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-upgrade
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