# datasette-auth0

[![PyPI](https://img.shields.io/pypi/v/datasette-auth0.svg)](https://pypi.org/project/datasette-auth0/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-auth0?include_prereleases&label=changelog)](https://github.com/simonw/datasette-auth0/releases)
[![Tests](https://github.com/simonw/datasette-auth0/workflows/Test/badge.svg)](https://github.com/simonw/datasette-auth0/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-auth0/blob/main/LICENSE)

Datasette plugin that authenticates users using [Auth0](https://auth0.com/)

See [Simplest possible OAuth authentication with Auth0](https://til.simonwillison.net/auth0/oauth-with-auth0) for more about how this plugin works.

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-auth0

## Demo

You can try this out at [datasette-auth0-demo.datasette.io](https://datasette-auth0-demo.datasette.io/) - click on the top right menu icon and select "Sign in with Auth0".

## Initial configuration

First, create a new application in Auth0. You will need the domain, client ID and client secret for that application.

The domain should be something like `mysite.us.auth0.com`.

Add `http://127.0.0.1:8001/-/auth0-callback` to the list of Allowed Callback URLs.

Then configure these plugin secrets using `metadata.yml`:

```yaml
plugins:
  datasette-auth0:
    domain:
      "$env": AUTH0_DOMAIN
    client_id:
      "$env": AUTH0_CLIENT_ID
    client_secret:
      "$env": AUTH0_CLIENT_SECRET
```
Only the `client_secret` needs to be kept secret, but for consistency I recommend using the `$env` mechanism for all three.

In development, you can run Datasette and pass in environment variables like this:
```
AUTH0_DOMAIN="your-domain.us.auth0.com" \
AUTH0_CLIENT_ID="...client-id-goes-here..." \
AUTH0_CLIENT_SECRET="...secret-goes-here..." \
datasette -m metadata.yml
```

If you are deploying using `datasette publish` you can pass these using `--plugin-secret`. For example, to deploy using Cloud Run you might run the following:
```
datasette publish cloudrun mydatabase.db \
--install datasette-auth0 \
--plugin-secret datasette-auth0 domain "your-domain.us.auth0.com" \
--plugin-secret datasette-auth0 client_id "your-client-id" \
--plugin-secret datasette-auth0 client_secret "your-client-secret" \
--service datasette-auth0-demo
```
Once your Datasette instance is deployed, you will need to add its callback URL to the "Allowed Callback URLs" list in Auth0.

The callback URL should be something like:

    https://url-to-your-datasette/-/auth0-callback

## Usage

Once installed, a "Sign in with Auth0" menu item will appear in the Datasette main menu.

You can sign in and then visit the `/-/actor` page to see full details of the `auth0` profile that has been authenticated.

You can then use [Datasette permissions](https://docs.datasette.io/en/stable/authentication.html#configuring-permissions-in-metadata-json) to grant or deny access to different parts of Datasette based on the authenticated user.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-auth0
    python3 -mvenv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
