# datasette-redirect-to-https

[![PyPI](https://img.shields.io/pypi/v/datasette-redirect-to-https.svg)](https://pypi.org/project/datasette-redirect-to-https/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-redirect-to-https?include_prereleases&label=changelog)](https://github.com/simonw/datasette-redirect-to-https/releases)
[![Tests](https://github.com/simonw/datasette-redirect-to-https/workflows/Test/badge.svg)](https://github.com/simonw/datasette-redirect-to-https/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-redirect-to-https/blob/main/LICENSE)

Datasette plugin that redirects all non-https requests to https

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-redirect-to-https

## Usage

Once installed, incoming GET requests to the `http://` protocol will be 301 redirected to the `https://` equivalent page.

HTTP verbs other than GET will get a 405 Method Not Allowed HTTP error.

## Configuration

Some hosting providers handle HTTPS for you, passing requests back to your application server over HTTP.

For this plugin to work correctly, it needs to detect that the original incoming request came in over HTTP.

Hosting providers like this often set an additional HTTP header such as `x-forwarded-proto: http` identifying the original protocol.

You can configure `datasette-redirect-to-https` to respect this header using the following plugin configuration in `metadata.json`:

```json
{
  "plugins": {
    "datasette-redirect-to-https": {
      "if_headers": {
        "x-forwarded-proto": "http"
      }
    }
  }
}
```
The above example will redirect to `https://` if the incoming request has a `x-forwarded-proto: http` request header.

If multiple `if_headers` are listed, the redirect will occur if any of them match.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-redirect-to-https
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
