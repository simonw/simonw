# datasette-unsafe-expose-env

[![PyPI](https://img.shields.io/pypi/v/datasette-unsafe-expose-env.svg)](https://pypi.org/project/datasette-unsafe-expose-env/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-unsafe-expose-env?include_prereleases&label=changelog)](https://github.com/simonw/datasette-unsafe-expose-env/releases)
[![Tests](https://github.com/simonw/datasette-unsafe-expose-env/workflows/Test/badge.svg)](https://github.com/simonw/datasette-unsafe-expose-env/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-unsafe-expose-env/blob/main/LICENSE)

Datasette plugin to expose some environment variables at `/-/env` - for debugging

> :warning: **This plugin is no longer maintained**. [datasette-expose-env](https://datasette.io/plugins/datasette-expose-env) is recommended as a safe replacement that only exposes environment variables that you have explicitly configured.

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-unsafe-expose-env

## Usage

Once installed, the plugin will show a list of environment variables at `/-/env`

It will redact the following variables by default:

- `DATABASE_URL`
- `GPG_KEY`
- `DATASETTE_SECRET`

You can configure an alternative set of redacted secrets in your `metadata.yml` configuration:

```yaml
plugins:
  datasette-unsafe-expose-env:
    redact:
    - DATASETTE_SECRET
    - GPG_KEY
    - MY_OTHER_SECRET
```

Once again though: only use this plugin if you need it for debugging purposes and are absolutely certain it won't expose any valuable information. If in doubt, do not use this at all.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-unsafe-expose-env
    python3 -mvenv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
