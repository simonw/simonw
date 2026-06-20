# json-to-files

[![PyPI](https://img.shields.io/pypi/v/json-to-files.svg)](https://pypi.org/project/json-to-files/)
[![Changelog](https://img.shields.io/github/v/release/simonw/json-to-files?include_prereleases&label=changelog)](https://github.com/simonw/json-to-files/releases)
[![Tests](https://github.com/simonw/json-to-files/workflows/Test/badge.svg)](https://github.com/simonw/json-to-files/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/json-to-files/blob/master/LICENSE)

Create separate files on disk based on a JSON object

## Installation

Install this tool using `pip`:

    pip install json-to-files

## Usage

This tool takes a JSON file that looks like this:

```json
{
    "foo.txt": "The contents of foo.txt",
    "bar/baz.txt": "The contents of baz.txt"
}
```
And uses it to write out the following files on disk:

- `foo.txt` containing "The contents of foo.txt"
- `bar/baz.txt` containing "The contents of baz.txt"

You can run it like this:

    json-to-files bundle.json

Or you can specify a directory to write those files to:

    json-to-files bundle.json -d /tmp/other-directory

The `bundles.json` file name is optional - if omitted, this tool will read from standard input:

    cat bundle.json | json-to-files

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd json-to-files
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
