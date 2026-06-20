# asgi-debug

[![PyPI](https://img.shields.io/pypi/v/asgi-debug.svg)](https://pypi.org/project/asgi-debug/)
[![CircleCI](https://circleci.com/gh/simonw/asgi-debug.svg?style=svg)](https://circleci.com/gh/simonw/asgi-debug)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/asgi-debug/blob/master/LICENSE)

ASGI middleware for debugging ASGI applications

## Installation

    pip install asgi-debug

## Usage

Wrap your application in the middleware like this:

```python
from asgi_debug import asgi_debug_decorator


@asgi_debug_decorator()
async def hello_world_app(scope, receive, send):
    assert scope["type"] == "http"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"application/json"]],
        }
    )
    await send({"type": "http.response.body", "body": b'{"hello": "world"}'})
```

When you run the app, debugging information will print to your terminal.

If you save the above in `demo.py` you can `pip install uvicorn` and run it like this:

```
uvicorn demo:hello_world_app
```