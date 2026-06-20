# datasette-endpoints

[![PyPI](https://img.shields.io/pypi/v/datasette-endpoints.svg)](https://pypi.org/project/datasette-endpoints/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-endpoints?include_prereleases&label=changelog)](https://github.com/datasette/datasette-endpoints/releases)
[![Tests](https://github.com/datasette/datasette-endpoints/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-endpoints/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-endpoints/blob/main/LICENSE)

Plugin to add a /-/endpoints debug page listing all configured endpoints

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-endpoints
```
## Usage

Once installed, this plugin adds two endpoints to your Datasette instance:

- `/-/endpoints.json` - JSON list of all registered endpoints
- `/-/endpoints` - HTML page showing all registered endpoints in a table

### JSON API

Visit `/-/endpoints.json` to get a JSON array of all registered routes:

```json
[
    {
        "path": "/-/plugins",
        "view": "JsonDataView",
        "pattern": "/-/plugins(\\.(?P<format>json))?$"
    },
    {
        "path": "/{database}/{table}",
        "view": "TableView",
        "pattern": "/(?P<database>[^\\/\\.]+)/(?P<table>[^\\/\\.]+)(\\.(?P<format>\\w+))?$"
    }
]
```

Each endpoint object includes:

- **path** - A simplified, human-readable URL path with `{name}` placeholders for URL parameters
- **view** - The name of the view class or function handling the route
- **pattern** - The raw regex pattern used for URL matching

### HTML page

Visit `/-/endpoints` to see a table of all registered endpoints with their paths, view names, and regex patterns. This includes both built-in Datasette routes and any routes added by plugins.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-endpoints
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
