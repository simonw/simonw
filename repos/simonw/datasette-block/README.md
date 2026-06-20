# datasette-block

[![PyPI](https://img.shields.io/pypi/v/datasette-block.svg)](https://pypi.org/project/datasette-block/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-block?include_prereleases&label=changelog)](https://github.com/simonw/datasette-block/releases)
[![Tests](https://github.com/simonw/datasette-block/workflows/Test/badge.svg)](https://github.com/simonw/datasette-block/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-block/blob/main/LICENSE)

Block all access to specific path prefixes

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-block

## Configuration

Add the following to `metadata.json` to block specific path prefixes:

```json
{
    "plugins": {
        "datasette-block": {
            "prefixes": ["/all/"]
        }
    }
}
```

This will cause a 403 error to be returned for any path beginning with `/all/`.

This blocking happens as an ASGI wrapper around Datasette.

## Why would you need this?

You almost always would not. I use it with `datasette-ripgrep` to block access to static assets for unauthenticated users.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-block
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
