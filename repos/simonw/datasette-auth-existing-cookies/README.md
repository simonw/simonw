# datasette-auth-existing-cookies

[![PyPI](https://img.shields.io/pypi/v/datasette-auth-existing-cookies.svg)](https://pypi.org/project/datasette-auth-existing-cookies/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-auth-existing-cookies?include_prereleases&label=changelog)](https://github.com/simonw/datasette-auth-existing-cookies/releases)
[![Tests](https://github.com/simonw/datasette-auth-existing-cookies/workflows/Test/badge.svg)](https://github.com/simonw/datasette-auth-existing-cookies/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-auth-existing-cookies/blob/master/LICENSE)

Datasette plugin that authenticates users based on existing domain cookies.

## When to use this

This plugin allows you to build custom authentication for Datasette when you are hosting a Datasette instance on the same domain as another, authenticated website.

Consider a website on `www.example.com` which supports user authentication.

You could run Datasette on `data.example.com` in a way that lets it see cookies that were set for the `.example.com` domain.

Using this plugin, you could build an API endpoint at `www.example.com/user-for-cookies` which returns a JSON object representing the currently signed-in user, based on their cookies.

The plugin running on `data.example.com` will then make the `actor` available to the rest of Datasette based on the response from that API.

Read about [Datasette's authentication and permissions system](https://docs.datasette.io/en/stable/authentication.html) for more on how actors and permissions work.

## Configuration

This plugin requires some configuration in the Datasette [metadata.json file](https://datasette.readthedocs.io/en/stable/plugins.html#plugin-configuration).

The following configuration options are supported:

- `api_url`: this is the API endpoint that Datasette should call with the user's cookies in order to identify the logged in user.
- `cookies`: optional. A list of cookie names that should be passed through to the API endpoint - if left blank, the default is to send all cookies.
- `ttl`: optional. By default Datasette will make a request to the API endpoint for every HTTP request recieved by Datasette itself. A `ttl` value of 5 will cause Datasette to cache the actor associated with the user's cookies for 5 seconds, reducing that API traffic.
- `headers`: an optional list of other headers to forward to the API endpoint as query string parameters.

Here is an example that uses all four of these settings:

```json
{
    "plugins": {
        "datasette-auth-existing-cookies": {
            "api_url": "http://www.example.com/user-from-cookies",
            "cookies": ["sessionid"],
            "headers": ["host"],
            "ttl": 10
        }
    }
}
```
With this configuration any hit to a Datasette hosted at `data.example.com` will result in the following request being made to the `http://www.example.com/user-from-cookies` API endpoint:
```
GET http://www.example.com/user-from-cookies?host=data.example.com
Cookie: sessionid=abc123
```
That API is expected to return a JSON object representing the current user:

```json
{
    "id": 1,
    "name": "Barry"
}
```
Since `ttl` is set to 10 that actor will be cached for ten seconds against that exact combination of cookies and headers. When that cache expires another hit will be made to the API.

When deciding on a TTL value, take into account that users who lose access to the core site - maybe because their session expires, or their account is disabled - will still be able to access the Datasette instance until that cache expires.
