# asgi-cors

[![PyPI](https://img.shields.io/pypi/v/asgi-cors.svg)](https://pypi.org/project/asgi-cors/)
[![Tests](https://github.com/simonw/asgi-cors/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/asgi-cors/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/asgi-cors?include_prereleases&label=changelog)](https://github.com/simonw/asgi-cors/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/asgi-cors/blob/main/LICENSE)

ASGI middleware for applying CORS headers to an ASGI application.

## Installation
```bash
pip install asgi-cors
```
## Some background on CORS

CORS stands for Cross-Origin Resource Sharing. It is a web standard that allows applications to opt-in to allowing JavaScript running on other domains to make `fetch()` calls that can retrieve data from the application.

See [MDN's CORS article](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) for more background.

The easiest way to allow scripts running on other domains to access data from an application is to add the following HTTP header:
```
Access-Control-Allow-Origin: *
```
This will allow scripts running on ANY domain to make `fetch()` calls against the application. For public data this is often fine, but there are situations where this may not be what you want to do: one example might be code that runs behind a VPN and needs to allow specific, trusted hosts to load data without opening itself up to every site on the internet.

For these cases, the server needs to inspect the Origin header from the client and return that Origin in the above header. For example, an incoming request from `http://localhost:8000` might be judged as trusted - in which case the application server needs to reply like so:
```
Access-Control-Allow-Origin: http://localhost:8000
```
Note that the `Access-Control-Allow-Origin` header can only return a single value. This means that if you want to allow requests from multiple origins you need to dynamically allowlist those origins and return a different header value depending on the incoming request.

Additionally if specific HTTP methods should be allowed an application should add:
```
Access-Control-Allow-Methods: GET, OPTIONS
```
Here `GET` and `OPTIONS` are allowed.

Similarly specific headers can be allowed:
```
Access-Control-Allow-Headers: content-type, Authorization
```
In this case `content-type` and `Authorization` headers are allowed to be sent to the server in a CORS request.

Verbs other than `GET` (such as `POST`) will trigger a preflight request. This is an `OPTIONS` request that the browser sends to the server to ask if the server will accept the request.

The `access-control-max-age` header can be used to specify how long the results of a preflight request can be cached. This can reduce the number of requests made to the server.

## How to use this middleware

We will assume you have an existing ASGI app, in a variable called `app`.

First, import the `asgi_cors` function:
```python
from asgi_cors import asgi_cors
```
To enable CORS headers for everywhere (by adding the `Access-Control-Allow-Origin: *` header to every request), do this:
```python
app = asgi_cors(app, allow_all=True)
```
If you wish to only allow it from a specific host, use the following:
```python
app = asgi_cors(app, hosts=[
    "https://www.example.com"
])
```
Now JavaScript executing on https://www.example.com will be able to call your API. You can test this out by opening up example.com in your browser, opening your browser's devtools console and pasting in the following JavaScript:
```javascript
fetch("https://your-api.com/").then(r => r.json()).then(d => console.log(d))
```
You can include multiple hosts in the list.

If you want to open your application up to requests from a wildcard-defined selection of hosts, use the following:
```python
app = asgi_cors(app, host_wildcards=[
    "http://localhost:800*",
    "http://*.example.com"
])
```
This will enable access from any JavaScript running on a local host server on ports 8000 through 8009 - or from any subdomain of example.com.

If you need to do something more complicated that cannot be expressed using the `hosts=` or `host_wildcards=` parameters, you can use `callback=` to specify a custom function. For example:
```python
def validate_origin(origin):
    return origin.startswith("https://")

app = asgi_cors(app, callback=validate_origin)
```
Your callback function will be passed the `Origin` header that was passed in by the browser. Both regular and async functions are supported.

To add specific allowed headers or methods you can specify them with the `headers=` and `methods=` parameters:
```python
app = asgi_cors(app, methods=[
    "GET", "OPTIONS"
], headers=[
    "Authorization","content-type"
])
```
To set a `access-control-max-age` header, use the `max_age=` parameter:

```python
app = asgi_cors(app, host_wildcards=["*"], max_age=3600)
```

## Using the middleware as a decorator

If you are defining your ASGI application directly as a function, you can use the `asgi_cors_decorator` function decorator like so:
```python
from asgi_cors import asgi_cors_decorator


@asgi_cors_decorator(allow_all=True)
async def my_asgi_app(scope, receive, send):
    # Your app goes here
```