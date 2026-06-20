# llm-fireworks

[![PyPI](https://img.shields.io/pypi/v/llm-fireworks.svg)](https://pypi.org/project/llm-fireworks/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-fireworks?include_prereleases&label=changelog)](https://github.com/simonw/llm-fireworks/releases)
[![Tests](https://github.com/simonw/llm-fireworks/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-fireworks/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-fireworks/blob/main/LICENSE)

Access [fireworks.ai](https://fireworks.ai/) models via API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-fireworks
```
## Usage

Obtain a [Fireworks API key](https://fireworks.ai/api-keys) and save it like this:

```bash
llm keys set fireworks
# <Paste key here>
```
Run `llm models` to get a list of models.

Run prompts like this:
```bash
llm -m fireworks/models/llama-v3-70b-instruct 'five great names for a pet ocelot'
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-fireworks
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
