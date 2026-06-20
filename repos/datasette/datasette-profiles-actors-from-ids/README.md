# datasette-profiles-actors-from-ids

[![PyPI](https://img.shields.io/pypi/v/datasette-profiles-actors-from-ids.svg)](https://pypi.org/project/datasette-profiles-actors-from-ids/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-profiles-actors-from-ids?include_prereleases&label=changelog)](https://github.com/datasette/datasette-profiles-actors-from-ids/releases)
[![Tests](https://github.com/datasette/datasette-profiles-actors-from-ids/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-profiles-actors-from-ids/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-profiles-actors-from-ids/blob/main/LICENSE)

Use [datasette-profiles](https://github.com/datasette/datasette-profiles) to handle [actors_from_ids](https://docs.datasette.io/en/latest/plugin_hooks.html#actors-from-ids-datasette-actor-ids)

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-profiles-actors-from-ids
```
## Usage

Once installed, calls to the [datasette.actors_from_ids()](https://docs.datasette.io/en/latest/internals.html#datasette-actors-from-ids) method will incorporate details from user profiles stored by the [datasette-profiles](https://github.com/datasette/datasette-profiles) plugin.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-profiles-actors-from-ids
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
