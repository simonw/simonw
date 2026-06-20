# webvtt-to-json

[![PyPI](https://img.shields.io/pypi/v/webvtt-to-json.svg)](https://pypi.org/project/webvtt-to-json/)
[![Changelog](https://img.shields.io/github/v/release/simonw/webvtt-to-json?include_prereleases&label=changelog)](https://github.com/simonw/webvtt-to-json/releases)
[![Tests](https://github.com/simonw/webvtt-to-json/workflows/Test/badge.svg)](https://github.com/simonw/webvtt-to-json/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/webvtt-to-json/blob/master/LICENSE)

Convert WebVTT to JSON, optionally removing duplicate lines

## Installation

Install this tool using `pip`:

    pip install webvtt-to-json

## Usage

To output JSON for a WebVTT file:

    webvtt-to-json subtitles.vtt

This will output to standard output. Use `-o filename` to send it to a specified file.

Subtitles can often include duplicate lines. Add `-d` or `--dedupe` to attempt to remove those duplicates from the output:

    webvtt-to-json --dedupe subtitles.vtt

Use `-s` or `--single` to output single `"line"` keys instead of a `"lines"` array.

You can also use:

    python -m webvtt_to_json ...

## Output

Standard output:
```json
[
    {
        "start": "00:00:00.000",
        "end": "00:00:01.829",
        "lines": [
            " ",
            "my<00:00:00.160><c> career</c><00:00:00.480><c> in</c><00:00:00.640><c> side</c><00:00:00.880><c> projects</c><00:00:01.280><c> and</c><00:00:01.520><c> open</c>"
        ]
    }
]
```
`--dedupe` output:
```json
[
    {
        "start": "00:00:01.829",
        "end": "00:00:01.839",
        "lines": ["my career in side projects and open"]
    }
]
```
`--dedupe --single` output:
```json
[
    {
        "start": "00:00:01.829",
        "end": "00:00:01.839",
        "line": "my career in side projects and open"
    }
]
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd webvtt-to-json
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
