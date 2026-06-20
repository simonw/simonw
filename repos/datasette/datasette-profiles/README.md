# datasette-profiles

[![PyPI](https://img.shields.io/pypi/v/datasette-profiles.svg)](https://pypi.org/project/datasette-profiles/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-profiles?include_prereleases&label=changelog)](https://github.com/datasette/datasette-profiles/releases)
[![Tests](https://github.com/datasette/datasette-profiles/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-profiles/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-profiles/blob/main/LICENSE)

Editable user profile pages for Datasette

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-profiles
```
## Usage

Adds the ability for users to view profiles and edit their profile, from options in the main application menu.

Stores data in the internal database, so Datasette needs to be run with the `--internal internal.db` option.

## Plugin hook

This plugin adds a plugin hook: `bottom_profile(datasette, request, profile_actor)`. Other plugins can use this to return HTML to be included at the bottom of the public user profile page - or return an `async def` function that returns that HTML.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-profiles
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
