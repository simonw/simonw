# asgi-auth-github

[![PyPI](https://img.shields.io/pypi/v/asgi-auth-github.svg)](https://pypi.org/project/asgi-auth-github/)
[![CircleCI](https://circleci.com/gh/simonw/asgi-auth-github.svg?style=svg)](https://circleci.com/gh/simonw/asgi-auth-github)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/asgi-auth-github/blob/master/LICENSE)

ASGI middleware that authenticates users against GitHub.

(Originally part of [datasette-auth-github](https://github.com/simonw/datasette-auth-github), now split off as a separate project.)

## Setup instructions

* Install the package - `pip install asgi-auth-github`
* Create a GitHub OAuth app: https://github.com/settings/applications/new
* Set the Authorization callback URL to `http://127.0.0.1:8001/-/auth-callback`

## Adding this to your ASGI application

```python
from asgi_auth_github import GitHubAuth
from your_asgi_app import asgi_app


app = GitHubAuth(
    asgi_app,
    client_id="github_client_id",
    client_secret="github_client_secret",
    require_auth=True,
    # Other options:
    # cookie_ttl=24 * 60 * 60,
    # disable_auto_login=True,
    # allow_users=["simonw"],
    # allow_orgs=["my-org"],
    # allow_teams=["my-org/engineering"],
)
```

See the [datasette-auth-github 0.12 documentation](https://github.com/simonw/datasette-auth-github/blob/0.12/README.md) for documentation of the other parameters.

Once wrapped in this way, your application will redirect users to GitHub to authenticate if they are not yet signed in. Authentication is recorded using a signed cookie.

The middleware adds a new `"auth"` key to the scope containing details of the signed-in user, which is then passed to your application. The contents of the `scope["auth"]` key will look like this:

```json
{
    "id": "1234 (their GitHub user ID)",
    "name": "Their Display Name",
    "username": "their-github-username",
    "email": "their-github@email-address.com",
    "ts": 1562602415
}
```
The `"ts"` value is an integer `time.time()` timestamp representing when the user last signed in.

If the user is not signed in (and you are not using required authentication) the `"auth"` scope key will be set to `None`.

## Example using Starlette

Here's an example using the [Starlette](https://www.starlette.io/) ASGI framework. You'll need to add your `client_id` and `client_secret` to this code before running it.

Save the following as `starlette_demo.py`:

```python
from asgi_auth_github import GitHubAuth
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

app = Starlette(debug=True)


async def homepage(request):
    return JSONResponse({"auth": request.scope["auth"]})


app = Starlette(debug=True, routes=[Route("/", homepage),])


authenticated_app = GitHubAuth(
    app,
    client_id="...",
    client_secret="...",
    require_auth=True,
)

if __name__ == "__main__":
    uvicorn.run(authenticated_app, host="0.0.0.0", port=8001)
```

Install the dependencies like this:

    pip install uvicorn starlette asgi-auth-github

Then run it with:

    python starlette_demo.py
