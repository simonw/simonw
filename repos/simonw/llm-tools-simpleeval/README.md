# llm-tools-simpleeval

[![PyPI](https://img.shields.io/pypi/v/llm-tools-simpleeval.svg)](https://pypi.org/project/llm-tools-simpleeval/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-tools-simpleeval?include_prereleases&label=changelog)](https://github.com/simonw/llm-tools-simpleeval/releases)
[![Tests](https://github.com/simonw/llm-tools-simpleeval/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-tools-simpleeval/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-simpleeval/blob/main/LICENSE)

Make simple_eval available as an LLM tool

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-simpleeval
```
## Usage

```bash
llm -T simple_eval "4444 * 233423" --td
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-simpleeval
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
