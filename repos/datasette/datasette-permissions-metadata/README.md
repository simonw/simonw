# datasette-permissions-metadata

[![PyPI](https://img.shields.io/pypi/v/datasette-permissions-metadata.svg)](https://pypi.org/project/datasette-permissions-metadata/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-permissions-metadata?include_prereleases&label=changelog)](https://github.com/datasette/datasette-permissions-metadata/releases)
[![Tests](https://github.com/datasette/datasette-permissions-metadata/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-permissions-metadata/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-permissions-metadata/blob/main/LICENSE)

Configure permissions for Datasette 0.x in `metadata.json`

## Background

Datasette 1.0 will introduce [a new way of configuring permissions](https://docs.datasette.io/en/latest/authentication.html#other-permissions-in-datasette-yaml) using YAML or JSON directly in the Datasette `datasette.yml` configuration file.

This plugin makes a similar ability available to the Datasette 0.64+ series of releases, by allowing a `permissions` key to be added to the `metadata.json` or `metadata.yml` file used with that version of Datasette.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-permissions-metadata
```
## Configuration

To grant the `upload-csvs` permission (used by the [datasette-upload-csvs](https://datasette.io/plugins/datasette-upload-csvs) plugin) to an user with an `id` of `simon`, add the following to `metadata.json`:

```json
{
  "permissions": {
    "upload-csvs": {
      "id": "simon"
    }
  }
}
```
See [the documentation on allow blocks](https://docs.datasette.io/en/stable/authentication.html#defining-permissions-with-allow-blocks) for more details on this configuration format.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-permissions-metadata
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
