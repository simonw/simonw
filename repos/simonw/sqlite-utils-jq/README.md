# sqlite-utils-jq

[![PyPI](https://img.shields.io/pypi/v/sqlite-utils-jq.svg)](https://pypi.org/project/sqlite-utils-jq/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-utils-jq?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-utils-jq/releases)
[![Tests](https://github.com/simonw/sqlite-utils-jq/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-utils-jq/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-utils-jq/blob/main/LICENSE)

Plugin adding a `jq()` SQL function to [sqlite-utils](https://sqlite-utils.datasette.io/).

## Installation

Install this plugin in the same environment as `sqlite-utils`:
```bash
sqlite-utils install sqlite-utils-jq
```

## Usage

This plugin adds a `jq()` function for executing [jq](https://jqlang.github.io/jq/) programs against JSON values.

```bash
sqlite-utils memory "select jq(:doc, :expr) as result" \
  -p doc '{"foo": "bar"}' \
  -p expr '.foo' \
  --table
```
Output:
```
result
--------
"bar"
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd sqlite-utils-jq
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
