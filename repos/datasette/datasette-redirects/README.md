# datasette-redirects

[![PyPI](https://img.shields.io/pypi/v/datasette-redirects.svg)](https://pypi.org/project/datasette-redirects/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-redirects?include_prereleases&label=changelog)](https://github.com/datasette/datasette-redirects/releases)
[![Tests](https://github.com/datasette/datasette-redirects/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-redirects/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-redirects/blob/main/LICENSE)

Configure redirects for a Datasette instance

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-redirects
```
## Usage

Configure redirects in your `datasette.yaml` configuration file. Redirects are organized by HTTP status code:

```yaml
plugins:
  datasette-redirects:
    301:
      old-page: https://example.com/new-page
      another-old-page: /new-location
    302:
      temporary-page: /temporary-location
```

This configuration will:

- Redirect `/old-page` to `https://example.com/new-page` with a 301 (permanent) status
- Redirect `/another-old-page` to `/new-location` with a 301 status
- Redirect `/temporary-page` to `/temporary-location` with a 302 (temporary) status

Both `/path` and `/path/` variants are matched automatically - you don't need to configure both.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-redirects
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
