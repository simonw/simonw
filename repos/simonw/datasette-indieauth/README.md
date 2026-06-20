# datasette-indieauth

[![PyPI](https://img.shields.io/pypi/v/datasette-indieauth.svg)](https://pypi.org/project/datasette-indieauth/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-indieauth?include_prereleases&label=changelog)](https://github.com/simonw/datasette-indieauth/releases)
[![codecov](https://codecov.io/gh/simonw/datasette-indieauth/branch/main/graph/badge.svg)](https://codecov.io/gh/simonw/datasette-indieauth)
[![Tests](https://github.com/simonw/datasette-indieauth/workflows/Test/badge.svg)](https://github.com/simonw/datasette-indieauth/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-indieauth/blob/main/LICENSE)

Datasette authentication using [IndieAuth](https://indieauth.net/).

## Demo

You can try out the latest version of this plugin at [datasette-indieauth-demo.datasette.io](https://datasette-indieauth-demo.datasette.io/-/indieauth)

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-indieauth

## Usage

Ensure you have a website with a domain that supports IndieAuth or RelMeAuth. The easiest way to do that is to add the following HTML to your homepage, linking to your personal GitHub profile:

```html
<link href="https://github.com/simonw" rel="me">
<link rel="authorization_endpoint" href="https://indieauth.com/auth">
```
Your GitHub profile needs to link back to your website, to prove that your GitHub account should be a valid identifier for that page.

Now visit `/-/indieauth` on your Datasette instance to begin the sign-in progress.

## Actor

When a user signs in using IndieAuth they will be recieve a signed `ds_actor` cookie identifying them as an [actor](https://docs.datasette.io/en/stable/authentication.html#actors) that looks like this:

```json
{
    "me": "https://simonwillison.net/",
    "display": "simonwillison.net"
}
```

If the IndieAuth server returned additional `"profile"` fields those will be merged into the actor. You can visit `/-/actor` on your Datasette instance to see the full actor you are currently signed in as.

## Restricting access with the restrict_access plugin configuration

You can use [Datasette's permissions system](https://docs.datasette.io/en/stable/authentication.html#permissions) to control permissions of authenticated users - by default, an authenticated user will be able to perform the same actions as an unauthenticated user.

As a shortcut if you want to lock down access to your instance entirely to just specific users, you can use the `restrict_access` plugin configuration option like this:

```json
{
    "plugins": {
        "datasette-indieauth": {
            "restrict_access": "https://simonwillison.net/"
        }
    }
}
```

This can be a string or a list of user identifiers. It can also be a space separated list, which means you can use it with the [datasette publish](https://docs.datasette.io/en/stable/publish.html#datasette-publish) `--plugin-secret` configuration option to set permissions as part of a deployment, like this:
```
datasette publish vercel mydb.db --project my-secret-db \
    --install datasette-indieauth \
    --plugin-secret datasette-indieauth restrict_access https://simonwillison.net/
```
## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-indieauth
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
