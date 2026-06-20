# flatten-single-item-arrays

[![PyPI](https://img.shields.io/pypi/v/flatten-single-item-arrays.svg)](https://pypi.org/project/flatten-single-item-arrays/)
[![Changelog](https://img.shields.io/github/v/release/simonw/flatten-single-item-arrays?include_prereleases&label=changelog)](https://github.com/simonw/flatten-single-item-arrays/releases)
[![Tests](https://github.com/simonw/flatten-single-item-arrays/workflows/Test/badge.svg)](https://github.com/simonw/flatten-single-item-arrays/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/flatten-single-item-arrays/blob/master/LICENSE)

Given a JSON list of objects, flatten any keys which always contain single item arrays to just a single value

## Installation

Install this tool using `pip`:

    $ pip install flatten-single-item-arrays

## Usage

This will output the rewritten JSON:

    $ flatten-single-item-arrays input.json

You can save it to a file like this:

    $ flatten-single-item-arrays input.json > output.json

Use `--debug` to see extra debugging information displayed on standard error:

    $ flatten-single-item-arrays input.json --debug > output.json
    Item count: 2
    count_of_single_item_lists
    {
        "foo": 2
    }
    count_of_present_keys
    {
        "foo": 2,
        "bar": 2
    }
    keys_to_reformat:
    - foo

## What this does

This tool accepts the path to a JSON file and outputs a modified version of that JSON file where any keys that are *always* single item lists are rewritten to a single value.

For example, the following input:

```json
[
    {
        "foo": [
            "bar"
        ],
        "bar": 5
    },
    {
        "foo": [
            "baz"
        ],
        "bar": 6
    }
]
```

Will be transformed to this:

```json
[
    {
        "foo": "bar",
        "bar": 5
    },
    {
        "foo": "baz",
        "bar": 6
    }
]
```

I built this to help work with data from the Airtable API, which often contains this single-item-list pattern.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd flatten-single-item-arrays
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
