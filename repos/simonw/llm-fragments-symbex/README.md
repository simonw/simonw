# llm-fragments-symbex

[![PyPI](https://img.shields.io/pypi/v/llm-fragments-symbex.svg)](https://pypi.org/project/llm-fragments-symbex/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-fragments-symbex?include_prereleases&label=changelog)](https://github.com/simonw/llm-fragments-symbex/releases)
[![Tests](https://github.com/simonw/llm-fragments-symbex/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-fragments-symbex/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-fragments-symbex/blob/main/LICENSE)

LLM fragment loader for Python symbols

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-fragments-symbex
```
## Usage

Use the fragment loader like this:

```bash
llm -f symbex:path/to/directory
```
This will load the function, class and method signatures of every Python file in that directory (and its subdirectories) along with their docstrings and concatenate them into a single fragment.

It uses the same AST parsing logic as [Symbex](https://github.com/simonw/symbex).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-fragments-symbex
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
