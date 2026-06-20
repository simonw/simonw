# sqlite-utils-dateutil

[![PyPI](https://img.shields.io/pypi/v/sqlite-utils-dateutil.svg)](https://pypi.org/project/sqlite-utils-dateutil/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-utils-dateutil?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-utils-dateutil/releases)
[![Tests](https://github.com/simonw/sqlite-utils-dateutil/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-utils-dateutil/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-utils-dateutil/blob/main/LICENSE)

Date utility functions for [sqlite-utils](https://sqlite-utils.datasette.io/).

## Installation

Install this plugin in the same environment as sqlite-utils.
```bash
sqlite-utils install sqlite-utils-dateutil
```

## Usage

This plugin adds a variety of SQL functions for parsing dates. For example:

```bash
sqlite-utils memory "select dateutil_parse('10 october 2020 3pm')" --table
```
Output:
```
dateutil_parse('10 october 2020 3pm')
---------------------------------------
2020-10-10T15:00:00
```
Consult [the datasette-dateutil documentation](https://github.com/simonw/datasette-dateutil/blob/main/README.md#usage) for a full list of functions.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd sqlite-utils-dateutil
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
