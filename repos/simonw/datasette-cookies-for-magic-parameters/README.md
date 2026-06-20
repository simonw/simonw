# datasette-cookies-for-magic-parameters

[![PyPI](https://img.shields.io/pypi/v/datasette-cookies-for-magic-parameters.svg)](https://pypi.org/project/datasette-cookies-for-magic-parameters/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-cookies-for-magic-parameters?include_prereleases&label=changelog)](https://github.com/simonw/datasette-cookies-for-magic-parameters/releases)
[![Tests](https://github.com/simonw/datasette-cookies-for-magic-parameters/workflows/Test/badge.svg)](https://github.com/simonw/datasette-cookies-for-magic-parameters/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-cookies-for-magic-parameters/blob/main/LICENSE)

UI for setting cookies to populate magic parameters

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-cookies-for-magic-parameters

## Usage

This plugin only affects canned queries. If you have a canned query configured like this:

```yaml
databases:
  mydatabase:
    queries:
      api_query:
        sql: select 'Your API key is' || :_cookie_openai_api_token;
```
Then the `/mydatabase/api_query` page will include a new interface for setting the `openapi_api_token` cookie, or unsetting it if it has already been set.

## Why use this?

This plugin was initially developed to use with [datasette-openai](https://github.com/simonw/datasette-openai) - a plugin that provides custom SQL functions that take an API token as one of their parameters.

Passing these API tokens in a GET query string is unsafe, as they may leak through referrers or other log files.

Instead, this plugin enables them to be set and passed using a cookie, which is much less likely to be logged.

This pattern takes advantage of the `:_cookie_x` feature of Datasette's [magic parameters](https://docs.datasette.io/en/stable/sql_queries.html#magic-parameters) mechanism.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-cookies-for-magic-parameters
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
