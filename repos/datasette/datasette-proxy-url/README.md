# datasette-proxy-url

[![PyPI](https://img.shields.io/pypi/v/datasette-proxy-url.svg)](https://pypi.org/project/datasette-proxy-url/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-proxy-url?include_prereleases&label=changelog)](https://github.com/datasette/datasette-proxy-url/releases)
[![Tests](https://github.com/datasette/datasette-proxy-url/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-proxy-url/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-proxy-url/blob/main/LICENSE)

Proxy a URL through a Datasette instance

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-proxy-url
```
## Usage

This plugin can be configured to set specific paths within Datasette to proxy content from another URL.

Configure the plugin like this:
```json
{
    "plugins": {
        "datasette-proxy-url": {
            "paths": [
                {"path": "/proxy", "backend": "http://example.com/"},
            ]
        }
    }
}
```
Now any request to `/proxy` will serve the HTML content from `http://example.com/`.

The `content-type` response header and the content body will be passed through. All other headers are currently ignored.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-proxy-url
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
