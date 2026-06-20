# datasette-packages

[![PyPI](https://img.shields.io/pypi/v/datasette-packages.svg)](https://pypi.org/project/datasette-packages/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-packages?include_prereleases&label=changelog)](https://github.com/simonw/datasette-packages/releases)
[![Tests](https://github.com/simonw/datasette-packages/workflows/Test/badge.svg)](https://github.com/simonw/datasette-packages/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-packages/blob/main/LICENSE)

Show a list of currently installed Python packages

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-packages
```
## Usage

Visit `/-/packages` to see a list of installed Python packages. Each package links to a detail page at `/-/packages/package-name` showing the full metadata and README for that package.

Visit `/-/packages.json` to get the list back as JSON.

## Demo

The output of this plugin can be seen here:

- https://latest-with-plugins.datasette.io/-/packages
- https://latest-with-plugins.datasette.io/-/packages.json

## With datasette-graphql

if you have version 2.1 or higher of the [datasette-graphql](https://datasette.io/plugins/datasette-graphql) plugin installed you can also query the list of packages using this GraphQL query:

```graphql
{
  packages {
    name
    version
  }
}
```
[Demo of this query](https://latest-with-plugins.datasette.io/graphql?query=%7B%0A%20%20packages%20%7B%0A%20%20%20%20name%0A%20%20%20%20version%0A%20%20%7D%0A%7D).

## Development

Run the tests using `uv run pytest`:
```bash
cd datasette-packages
uv run pytest
```
To try the plugin locally, use:
```bash
uv run datasette
```
Then visit `http://localhost:8001/-/packages`
