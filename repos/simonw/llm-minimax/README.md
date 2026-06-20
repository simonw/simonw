# llm-minimax

[![PyPI](https://img.shields.io/pypi/v/llm-minimax.svg)](https://pypi.org/project/llm-minimax/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-minimax?include_prereleases&label=changelog)](https://github.com/simonw/llm-minimax/releases)
[![Tests](https://github.com/simonw/llm-minimax/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-minimax/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-minimax/blob/main/LICENSE)

LLM plugin for accessing MiniMax models via their API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-minimax
```
## Usage

Obtain an API key for MiniMax from [their API platform site](https://platform.minimax.io/user-center/basic-information/interface-key).

Set the API key using:
```bash
llm keys set minimax
# Paste key here
```
Run MiniMax M2 like this:
```bash
llm -m m2 "Tell me about yourself"
```
## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-minimax
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
