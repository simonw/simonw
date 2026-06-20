# datasette-configure-asgi

[![PyPI](https://img.shields.io/pypi/v/datasette-configure-asgi.svg)](https://pypi.org/project/datasette-configure-asgi/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-configure-asgi.svg?style=svg)](https://circleci.com/gh/simonw/datasette-configure-asgi)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-configure-asgi/blob/master/LICENSE)

Datasette plugin for configuring arbitrary ASGI middleware

## Installation

    pip install datasette-configure-asgi

## Usage

This plugin only takes effect if your `metadata.json` file contains relevant top-level plugin configuration in a `"datasette-configure-asgi"` configuration key.

For example, to wrap your Datasette instance in the `asgi-log-to-sqlite` middleware configured to write logs to `/tmp/log.db` you would use the following:

```json
{
    "plugins": {
        "datasette-configure-asgi": [
            {
                "class": "asgi_log_to_sqlite.AsgiLogToSqlite",
                "args": {
                    "file": "/tmp/log.db"
                }
            }
        ]
    }
}
```

The `"datasette-configure-asgi"` key should be a list of JSON objects. Each object should have a `"class"` key indicating the class to be used, and an optional `"args"` key providing any necessary arguments to be passed to that class constructor.

## Plugin structure

This plugin can be used to wrap your Datasette instance in any ASGI middleware that conforms to the following structure:

```python
class SomeAsgiMiddleware:
    def __init__(self, app, arg1, arg2):
        self.app = app
        self.arg1 = arg1
        self.arg2 = arg2

    async def __call__(self, scope, receive, send):
        start = time.time()
        await self.app(scope, receive, send)
        end = time.time()
        print("Time taken: {}".format(end - start))
```

So the middleware is a class with a constructor which takes the wrapped application as a first argument, `app`, followed by further named arguments to configure the middleware. It provides an `async def __call__(self, scope, receive, send)` method to implement the middleware's behavior.

