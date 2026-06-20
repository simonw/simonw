# datasette-scale-to-zero

[![PyPI](https://img.shields.io/pypi/v/datasette-scale-to-zero.svg)](https://pypi.org/project/datasette-scale-to-zero/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-scale-to-zero?include_prereleases&label=changelog)](https://github.com/simonw/datasette-scale-to-zero/releases)
[![Tests](https://github.com/simonw/datasette-scale-to-zero/workflows/Test/badge.svg)](https://github.com/simonw/datasette-scale-to-zero/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-scale-to-zero/blob/main/LICENSE)

Quit Datasette if it has not received traffic for a specified time period

Some hosting providers such as [Fly](https://fly.io/) offer a scale to zero mechanism, where servers can shut down and will be automatically started when new traffic arrives.

This plugin can be used to configure Datasette to quit X minutes (or seconds, or hours) after the last request it received. It can also cause the Datasette server to exit after a configured maximum time whether or not it is receiving traffic.

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-scale-to-zero

## Configuration

This plugin will only take effect if it has been configured with a `duration` or `max_age` value. Without at least one of these settings the plugin will do nothing.

Add the following to your ``metadata.json`` or ``metadata.yml`` configuration file:

```json
{
    "plugins": {
        "datasette-scale-to-zero": {
            "duration": "10m"
        }
    }
}
```
This will cause Datasette to quit if it has not received any HTTP traffic for 10 minutes.

You can set this value using a suffix of `m` for minutes, `h` for hours or `s` for seconds.

To cause Datasette to exit if the server has been running for longer than a specific time, use `"max_age"`:

```json
{
    "plugins": {
        "datasette-scale-to-zero": {
            "max_age": "10h"
        }
    }
}
```
This example will exit the Datasette server if it has been running for more than ten hours.

You can use `"duration"` and `"max_age"` together in the same configuration file:

```json
{
    "plugins": {
        "datasette-scale-to-zero": {
            "max_age": "10h",
            "duration": "5m"
        }
    }
}
```
This example will quit if no traffic has been received in five minutes, or if the server has been running for ten hours.

## Configuring a shutdown HTTP message

You can also configure the plugin to send an HTTP request somewhere right before it quits, using the `"shutdown_url"` option:

```json
{
    "plugins": {
        "datasette-scale-to-zero": {
            "duration": "10m",
            "shutdown_url": "https://example.com/shutdown"
        }
    }
}
```
You can add additional headers to the GET request - for example to send Authorization headers - using `"shutdown_headers"`:

```json
{
    "plugins": {
        "datasette-scale-to-zero": {
            "duration": "10m",
            "shutdown_url": "https://example.com/shutdown",
            "shutdown_headers": {
                "Authorization": "Bearer secret"
            }
        }
    }
}
```
Use `"shutdown_method"` to set a different HTTP method, e.g. for `POST`. You can also set `shutdown_body` to specify the body that should be sent with the request:

```json
{
    "plugins": {
        "datasette-scale-to-zero": {
            "duration": "10m",
            "shutdown_url": "https://example.com/shutdown",
            "shutdown_method": "POST",
            "shutdown_headers": {
                "Authorization": "Bearer secret",
                "Content-Type": "application/json"
            },
            "shutdown_body": "{\"message\": \"shutting down\"}"
        }
    }
}
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-scale-to-zero
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
