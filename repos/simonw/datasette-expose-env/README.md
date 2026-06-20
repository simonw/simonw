# datasette-expose-env

[![PyPI](https://img.shields.io/pypi/v/datasette-expose-env.svg)](https://pypi.org/project/datasette-expose-env/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-expose-env?include_prereleases&label=changelog)](https://github.com/simonw/datasette-expose-env/releases)
[![Tests](https://github.com/simonw/datasette-expose-env/workflows/Test/badge.svg)](https://github.com/simonw/datasette-expose-env/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-expose-env/blob/main/LICENSE)

Datasette plugin to expose selected environment variables at `/-/env` for debugging

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-expose-env
```
## Configuration

Decide on a list of environment variables you would like to expose, then add the following to your `metadata.yml` configuration:

```yaml
plugins:
  datasette-expose-env:
    variables:
    - ENV_VAR_1
    - ENV_VAR_2
    - ENV_VAR_3
```

If you are using JSON in a `metadata.json` file use the following:

```json
{
  "plugins": {
    "datasette-expose-env": {
      "variables": [
        "ENV_VAR_1",
        "ENV_VAR_2",
        "ENV_VAR_3"
      ]
    }
  }
}
```
To show a full list of redacted environment variables use `"show_all_redacted": true`:

```yaml
plugins:
  datasette-expose-env:
    show_all_redacted: true
    variables:
    - ENV_VAR_1
    - ENV_VAR_2
```
This will show the values for `ENV_VAR_1` and `ENV_VAR_2` and then a full list of other variables with their value shown as `...`.


Visit `/-/env` on your Datasette instance to see the values of the environment variables.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-expose-env
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```