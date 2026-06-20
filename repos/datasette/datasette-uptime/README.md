# datasette-uptime

[![PyPI](https://img.shields.io/pypi/v/datasette-uptime.svg)](https://pypi.org/project/datasette-uptime/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-uptime?include_prereleases&label=changelog)](https://github.com/datasette/datasette-uptime/releases)
[![Tests](https://github.com/datasette/datasette-uptime/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-uptime/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-uptime/blob/main/LICENSE)

Datasette plugin showing uptime at /-/uptime

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-uptime
```
## Usage

Adds an endpint at `/-/uptime` returning JSON that looks like this:
```json
{
    "started": 355764.709263208,
    "now": 355824.192608208,
    "uptime_seconds": 59.483345208049286,
    "uptime_hours": 0.0165231515625136
}
```
This shows how long the server has been running.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-uptime
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
