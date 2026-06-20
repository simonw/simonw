# llm-reka

[![PyPI](https://img.shields.io/pypi/v/llm-reka.svg)](https://pypi.org/project/llm-reka/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-reka?include_prereleases&label=changelog)](https://github.com/simonw/llm-reka/releases)
[![Tests](https://github.com/simonw/llm-reka/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-reka/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-reka/blob/main/LICENSE)

Access [Reka](https://www.reka.ai/) models via the Reka API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-reka
```
## Usage

Get [a Reka API key](https://platform.reka.ai/apikeys) and configure it like this:
```bash
llm keys set reka
# Paste in the API key
```

Use `llm -m reka-flash "prompt"` to run prompts against `reka-flash`.

The other models supported are `reka-core` and `reka-edge`.

Core is the most expensive, then Flash, then Edge is cheapest. [Pricing here](https://www.reka.ai/reka-api).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-reka
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest
```
