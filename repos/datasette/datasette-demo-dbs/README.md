# datasette-demo-dbs

[![PyPI](https://img.shields.io/pypi/v/datasette-demo-dbs.svg)](https://pypi.org/project/datasette-demo-dbs/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-demo-dbs?include_prereleases&label=changelog)](https://github.com/datasette/datasette-demo-dbs/releases)
[![Tests](https://github.com/datasette/datasette-demo-dbs/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-demo-dbs/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-demo-dbs/blob/main/LICENSE)

Fetch missing demo DBs from URLs when Datasette first starts

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-demo-dbs
```
## Configuration

Configure the plugin in your Datasette metadata (YAML or JSON). You specify:

- `path`: directory on disk where downloaded .db files will be stored (defaults to current directory)
- `dbs`: a mapping of database name to the URL of the SQLite database file

Example metadata.yml:

```yaml
plugins:
  datasette-demo-dbs:
    path: ./demo-dbs
    dbs:
      demo: https://example.com/path/to/demo.db
      census: https://example.com/path/to/census.db
```

Equivalent metadata.json:

```json
{
  "plugins": {
    "datasette-demo-dbs": {
      "path": "./demo-dbs",
      "dbs": {
        "demo": "https://example.com/path/to/demo.db",
        "census": "https://example.com/path/to/census.db"
      }
    }
  }
}
```
## How it works

On Datasette startup, for each entry in `dbs`:

1. If `path/<name>.db` already exists, it is left as-is and loaded into Datasette.
2. If a marker file `path/<name>.deleted` exists, the download is skipped.
3. Otherwise, the plugin downloads the content from the URL (following redirects), streams it to `path/<name>.db`, and registers that database in Datasette under the given name.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-demo-dbs
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
