# datasette-referrer-policy

[![PyPI](https://img.shields.io/pypi/v/datasette-referrer-policy.svg)](https://pypi.org/project/datasette-referrer-policy/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-referrer-policy?include_prereleases&label=changelog)](https://github.com/datasette/datasette-referrer-policy/releases)
[![Tests](https://github.com/datasette/datasette-referrer-policy/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-referrer-policy/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-referrer-policy/blob/main/LICENSE)

Set the Referrer-Policy header for a Datasette site

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-referrer-policy
```
## Usage

Installing this plugin causes every page on your Datasette instance to return this header:

    Referrer-Policy: strict-origin-when-cross-origin

You can configure a different policy using this configuration:

```yaml
plugins:
  datasette-referrer-policy:
    policy: no-referrer
```
See [MDN: Referrer-Policy header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy) for other values.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-referrer-policy
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
