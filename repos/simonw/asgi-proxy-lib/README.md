# asgi-proxy-lib

[![PyPI](https://img.shields.io/pypi/v/asgi-proxy-lib.svg)](https://pypi.org/project/asgi-proxy-lib/)
[![Changelog](https://img.shields.io/github/v/release/simonw/asgi-proxy-lib?include_prereleases&label=changelog)](https://github.com/simonw/asgi-proxy-lib/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/asgi-proxy-lib/blob/main/LICENSE)

An ASGI function for proxying to a backend over HTTP

**⚠️ Warning: this is an early alpha.**

## Installation

Install this library using `pip`:

    pip install asgi-proxy-lib

## Usage

This library provides a single ASGI function called `asgi_proxy`. You can use it like this:

```python
from asgi_proxy import asgi_proxy

app = asgi_proxy("https://datasette.io")
```
Now `app` is an ASGI application that will proxy all incoming HTTP requests to the equivalent URL on `https://datasette.io`.

The function takes an optional second argument, `log=` - set this to a Python logger, or any object that has `.info(msg)` and `.error(msg)` methods, and the proxy will log information about each request it proxies.

It also takes a `timeout=` option, which defaults to `None` for no timeout. This can be set to a floating point value in seconds to enforce a timeout on requests that are being proxied.

## CLI tool

You can try this module out like so:

```bash
python -m asgi_proxy https://datasette.io
```
You may need to `pip install uvicorn` first for this to work.

Alternatively, use [uv](https://github.com/astral-sh/uv) like this:
```bash
uv run --with uvicorn --with asgi-proxy-lib python -m asgi_proxy https://datasette.io
```

This will start a server on port 8000 that proxies to `https://datasette.io`.

Add `-p PORT` to specify a different port, `--timeout 3` to set a timeout, `--verbose` to see debug logging, and `--host 127.0.0.1` to listen on a different host (the default is `0.0.0.0`).

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd asgi-proxy-lib
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
