# llm-fragments-reader

[![PyPI](https://img.shields.io/pypi/v/llm-fragments-reader.svg)](https://pypi.org/project/llm-fragments-reader/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-fragments-reader?include_prereleases&label=changelog)](https://github.com/simonw/llm-fragments-reader/releases)
[![Tests](https://github.com/simonw/llm-fragments-reader/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-fragments-reader/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-fragments-reader/blob/main/LICENSE)

Run URLs through the Jina Reader API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-fragments-reader
```
## Usage

Use `-f 'reader:URL` to fetch a converted Markdown document for a URL.

```bash
llm -f 'reader:https://simonwillison.net/tags/jina/' summary
```

Uses [the Jina Reader API](https://jina.ai/reader/).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-fragments-reader
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
