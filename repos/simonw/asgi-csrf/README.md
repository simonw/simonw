# asgi-csrf

[![PyPI](https://img.shields.io/pypi/v/asgi-csrf.svg)](https://pypi.org/project/asgi-csrf/)
[![Changelog](https://img.shields.io/github/v/release/simonw/asgi-csrf?include_prereleases&label=changelog)](https://github.com/simonw/asgi-csrf/releases)
[![codecov](https://codecov.io/gh/simonw/asgi-csrf/branch/main/graph/badge.svg)](https://codecov.io/gh/simonw/asgi-csrf)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/asgi-csrf/blob/main/LICENSE)

ASGI middleware for protecting against CSRF attacks

## Installation

    pip install asgi-csrf

## Background

See the [OWASP guide to Cross Site Request Forgery (CSRF)](https://owasp.org/www-community/attacks/csrf) and their [Cross-Site Request Forgery (CSRF) Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html).

This middleware implements the [Double Submit Cookie pattern](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie), where a cookie is set that is then compared to a `csrftoken` hidden form field or a `x-csrftoken` HTTP header.

## Usage

Decorate your ASGI application like this:

```python
from asgi_csrf import asgi_csrf
from .my_asgi_app import app


app = asgi_csrf(app, signing_secret="secret-goes-here")
```

The middleware will set a `csrftoken` cookie, if one is missing. The value of that token will be made available to your ASGI application through the `scope["csrftoken"]` function.

Your application code should include that value as a hidden form field in any POST forms:

```html
<form action="/login" method="POST">
    ...
    <input type="hidden" name="csrftoken" value="{{ request.scope.csrftoken() }}">
</form>
```

Note that `request.scope["csrftoken"]()` is a function that returns a string. Calling that function also lets the middleware know that the cookie should be set by that page, if the user does not already have that cookie.

If the cookie needs to be set, the middleware will add a `Vary: Cookie` header to the response to ensure it is not incorrectly cached by any CDNs or intermediary proxies.

The middleware will return a 403 forbidden error for any POST requests that do not include the matching `csrftoken` - either in the POST data or in a `x-csrftoken` HTTP header (useful for JavaScript `fetch()` calls).

The `signing_secret` is used to sign the tokens, to protect against subdomain vulnerabilities.

If you do not pass in an explicit `signing_secret` parameter, the middleware will look for a `ASGI_CSRF_SECRET` environment variable.

If it cannot find that environment variable, it will generate a random secret which will persist for the lifetime of the server.

This means that if you do not configure a specific secret your user's `csrftoken` cookies will become invalid every time the server restarts! You should configure a secret.

## Always setting the cookie if it is not already set

By default this middleware only sets the `csrftoken` cookie if the user encounters a page that needs it - due to that page calling the `request.scope["csrftoken"]()` function, for example to populate a hidden field in a form.

If you would like the middleware to set that cookie for any incoming request that does not already provide the cookie, you can use the `always_set_cookie=True` argument:

```python
app = asgi_csrf(app, signing_secret="secret-goes-here", always_set_cookie=True)
```

## Configuring the cookie

The middleware can be configured with several options to control how the CSRF cookie is set:

```python
app = asgi_csrf(
    app,
    signing_secret="secret-goes-here",
    cookie_name="csrftoken",
    cookie_path="/",
    cookie_domain=None,
    cookie_secure=False,
    cookie_samesite="Lax"
)
```

- `cookie_name`: The name of the cookie to set. Defaults to `"csrftoken"`.
- `cookie_path`: The path for which the cookie is valid. Defaults to `"/"`, meaning the cookie is valid for the entire domain.
- `cookie_domain`: The domain for which the cookie is valid. Defaults to `None`, which means the cookie will only be valid for the current domain.
- `cookie_secure`: If set to `True`, the cookie will only be sent over HTTPS connections. Defaults to `False`.
- `cookie_samesite`: Controls how the cookie is sent with cross-site requests. Can be set to `"Strict"`, `"Lax"`, or `"None"`. Defaults to `"Lax"`.

## Other cases that skip CSRF protection

If the request includes an `Authorization: Bearer ...` header, commonly used by OAuth and JWT authentication, the request will not be required to include a CSRF token. This is because browsers cannot send those headers in a context that can be abused.

If the request has no cookies at all it will be allowed through, since CSRF protection is only necessary for requests from authenticated users.

### always_protect

If you have paths that should always be protected even without cookies - your login form for example (to avoid [login CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#login-csrf) attacks) you can protect those paths by passing them as the ``always_protect`` parameter:

```python
app = asgi_csrf(
    app,
    signing_secret="secret-goes-here",
    always_protect={"/login"}
)
```

### skip_if_scope

There may be situations in which you want to opt-out of CSRF protection even for authenticated POST requests - this is often the case for web APIs for example.

The `skip_if_scope=` parameter can be used to provide a callback function which is passed an ASGI scope and returns `True` if CSRF protection should be skipped for that request.

This example skips CSRF protection for any incoming request where the request path starts with `/api/`:

```python
def skip_api_paths(scope)
    return scope["path"].startswith("/api/")

app = asgi_csrf(
    app,
    signing_secret="secret-goes-here",
    skip_if_scope=skip_api_paths
)
```

## Custom errors with send_csrf_failed

By default, when a CSRF token is missing or invalid, the middleware will return a 403 Forbidden response page with a short error message.

You can customize this behavior by passing a `send_csrf_failed` function to the middleware. This function should accept the ASGI `scope` and `send` functions, and the `message_id` of the error that occurred.

The `message_id` will be an integer representing an item from the `asgi_csrf.Errors` enum.

This example shows how you could customize the error message based on that `message_id`:

```python
async def custom_csrf_failed(scope, send, message_id):
    assert scope["type"] == "http"
    await send(
        {
            "type": "http.response.start",
            "status": 403,
            "headers": [[b"content-type", b"text/html; charset=utf-8"]],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": {
                Errors.FORM_URLENCODED_MISMATCH: "custom form-urlencoded error",
                Errors.MULTIPART_MISMATCH: "custom multipart error",
                Errors.FILE_BEFORE_TOKEN: "custom file before token error",
                Errors.UNKNOWN_CONTENT_TYPE: "custom unknown content type error",
            }
            .get(message_id, "")
            .encode("utf-8"),
        }
    )


app = asgi_csrf(
    app,
    signing_secret="secret-goes-here",
    send_csrf_failed=custom_csrf_failed
)
```