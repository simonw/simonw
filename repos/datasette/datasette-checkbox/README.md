# datasette-checkbox

[![PyPI](https://img.shields.io/pypi/v/datasette-checkbox.svg)](https://pypi.org/project/datasette-checkbox/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-checkbox?include_prereleases&label=changelog)](https://github.com/datasette/datasette-checkbox/releases)
[![Tests](https://github.com/datasette/datasette-checkbox/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-checkbox/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-checkbox/blob/main/LICENSE)

Add interactive checkboxes to columns in Datasette. Requires Datasette 1.0 alpha or higher.

![Animated demo showing checkboxes in columns for is_done, should_be_deleted and is_happy - checking the checkboxes shows an updated message next to each one which then fades away.](https://raw.githubusercontent.com/datasette/datasette-checkbox/main/datasette-checkbox.gif)

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-checkbox
```
## Usage

This plugin adds checkboxes to the table and row pages in Datasette for any column with a name that starts `is_*` or `should_*` or `has_*` and that is of type `integer`.

Toggling those checkboxes updates the underlying column to a `1` or a `0`.

The checkbox interface will only be shown for users who have `update-row` permission for the table.

The easiest way to try this plugin is using the `--root` Datasette option:

```bash
datasette data.db --root
```
Or use the [Datasette permission system](https://docs.datasette.io/en/latest/authentication.html#permissions) to grant `update-row` to specific users.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-checkbox
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
