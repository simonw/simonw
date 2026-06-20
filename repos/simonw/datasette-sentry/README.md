# datasette-sentry

[![PyPI](https://img.shields.io/pypi/v/datasette-sentry.svg)](https://pypi.org/project/datasette-sentry/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-sentry?include_prereleases&label=changelog)](https://github.com/simonw/datasette-sentry/releases)
[![Tests](https://github.com/simonw/datasette-sentry/workflows/Test/badge.svg)](https://github.com/simonw/datasette-sentry/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-sentry/blob/main/LICENSE)

Datasette plugin for configuring Sentry for error reporting
 
## Installation
```bash
pip install datasette-sentry
```
## Usage

This plugin only takes effect if your `metadata.json` file contains relevant top-level plugin configuration in a `"datasette-sentry"` configuration key.

You will need a Sentry DSN - see their [Getting Started instructions](https://docs.sentry.io/error-reporting/quickstart/?platform=python).

Add it to `metadata.json` like this:

```json
{
    "plugins": {
        "datasette-sentry": {
            "dsn": "https://KEY@sentry.io/PROJECTID"
        }
    }
}
```
Settings in `metadata.json` are visible to anyone who visits the `/-/metadata` URL so this is a good place to take advantage of Datasette's [secret configuration values](https://datasette.readthedocs.io/en/stable/plugins.html#secret-configuration-values), in which case your configuration will look more like this:
```json
{
    "plugins": {
        "datasette-sentry": {
            "dsn": {
                "$env": "SENTRY_DSN"
            }
        }
    }
}
```
Then make a `SENTRY_DSN` environment variable available to Datasette.

## Configuration

In addition to the `dsn` setting, you can also configure the Sentry [sample rate](https://docs.sentry.io/platforms/python/configuration/sampling/) by setting  `sample_rate` to a floating point number between 0 and 1.

For example, to capture 25% of errors you would do this:

```json
{
    "plugins": {
        "datasette-sentry": {
            "dsn": {
                "$env": "SENTRY_DSN"
            },
            "sample_rate": 0.25
        }
    }
}
```

### Performance monitoring

Sentry [Performance Monitoring](https://docs.sentry.io/product/performance/) records full traces of page for further analysis, in addition to tracking errors.

You can enable that by adding "enable_tracing" to your plugin configuration:

```json
{
    "plugins": {
        "datasette-sentry": {
            "dsn": {
                "$env": "SENTRY_DSN"
            },
            "enable_tracing": true
        }
    }
}
```
The default sample rate if you do this will be `1.0`, meaning every response will be traced. This can get expensive - you can adjust the tracing rate using `traces_sample_rate`. Set that to `0.1` to sample 10% of requests, for example:

```json
{
    "plugins": {
        "datasette-sentry": {
            "dsn": {
                "$env": "SENTRY_DSN"
            },
            "enable_tracing": true,
            "traces_sample_rate": 0.1
        }
    }
}
```