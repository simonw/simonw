# json-post

[![PyPI](https://img.shields.io/pypi/v/json-post.svg)](https://pypi.org/project/json-post/)
[![Changelog](https://img.shields.io/github/v/release/simonw/json-post?include_prereleases&label=changelog)](https://github.com/simonw/json-post/releases)
[![Tests](https://github.com/simonw/json-post/workflows/Test/badge.svg)](https://github.com/simonw/json-post/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/json-post/blob/master/LICENSE)

Tool for posting JSON to an API, broken into pages

## Why would you need this?

This tool is for a very specific use-case. Let's say you have 80MB of data that you want to send to an API. The data is a big JSON file with thousands of items in it - but the API you are using can only accept 50 items at a time.

`json-post` can take that big JSON file and break it up into batches, then send each batch to the API in turn.

    json-post my-big-json-file.json https://example.com/my-api --batch-size 50

## Installation

Install this tool using `pip`:

    $ pip install json-post

## Options

`-h` or `--header KEY VALUE`

Takes two arguments to specify an HTTP header, for example to send an authorization token you might use:

    json-post d.json https://example.com/api --header Authorization "Bearer x...."

`--log FILENAME`

A filename to log the JSON responses from the API to, as newline-delimited JSON.

`--batch-size N`

The batch size to use. Omit this and the data will be sent in a single request.

`--stop-after N`

Send this many items and then stop. Useful for debugging.

`--reverse`

Send the items from the file in reverse order.

`--shuffle`

Send the items from the file in random order.

`--http-read-timeout N`

Timeout (in seconds) for network read operations.

`--filter 'item.get("field")'`

Filter the items in the array using this Python expression before sending them. The variable `item` will refer to each item in the list.

`--count`

Output the number of items that would be sent and then exit. Useful for testing that your `--filter` operation works as expected.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd json-post
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
