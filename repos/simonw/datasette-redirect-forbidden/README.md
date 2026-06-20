# datasette-redirect-forbidden

[![PyPI](https://img.shields.io/pypi/v/datasette-redirect-forbidden.svg)](https://pypi.org/project/datasette-redirect-forbidden/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-redirect-forbidden?include_prereleases&label=changelog)](https://github.com/simonw/datasette-redirect-forbidden/releases)
[![Tests](https://github.com/simonw/datasette-redirect-forbidden/workflows/Test/badge.svg)](https://github.com/simonw/datasette-redirect-forbidden/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-redirect-forbidden/blob/main/LICENSE)

Redirect forbidden requests to a login page

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-redirect-forbidden

## Usage

Add the following to your `metadata.yml` (or `metadata.json`) file to configure the plugin:

```yaml
plugins:
  datasette-redirect-forbidden:
    redirect_to: /-/login
```
Any 403 forbidden pages will redirect to the specified page.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-redirect-forbidden
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
