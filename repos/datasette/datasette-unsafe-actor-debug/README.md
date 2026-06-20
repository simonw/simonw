# datasette-unsafe-actor-debug

[![PyPI](https://img.shields.io/pypi/v/datasette-unsafe-actor-debug.svg)](https://pypi.org/project/datasette-unsafe-actor-debug/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-unsafe-actor-debug?include_prereleases&label=changelog)](https://github.com/datasette/datasette-unsafe-actor-debug/releases)
[![Tests](https://github.com/datasette/datasette-unsafe-actor-debug/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-unsafe-actor-debug/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-unsafe-actor-debug/blob/main/LICENSE)

Debug plugin that lets you imitate any actor. **Only use this for debugging purposes.**

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-unsafe-actor-debug
```
## Configuration

You need to set the following plugin configuration to enable this tool:

```yaml
plugins:
  datasette-unsafe-actor-debug:
    enabled: true
```

With Datasette 1.0 alpha you can enable it like this:
```bash
datasette -s plugins.datasette-unsafe-actor-debug.enabled 1
```

## Usage

This plugin adds a public page at `/-/unsafe-actor` that lets you sign into Datasette as _any_ actor.

This option will also be available through the Datasette global navigation menu.

**Do not enable this tool in production!**

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-unsafe-actor-debug
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
