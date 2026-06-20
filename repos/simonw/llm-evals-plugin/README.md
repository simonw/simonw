# llm-evals-plugin

[![PyPI](https://img.shields.io/pypi/v/llm-evals-plugin.svg)](https://pypi.org/project/llm-evals-plugin/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-evals-plugin?include_prereleases&label=changelog)](https://github.com/simonw/llm-evals-plugin/releases)
[![Tests](https://github.com/simonw/llm-evals-plugin/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-evals-plugin/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-evals-plugin/blob/main/LICENSE)

Run evals against prompts using LLM

**Very early alpha**: everything is likely to change.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-evals-plugin
```
## Usage

See [this issue comment](https://github.com/simonw/llm-evals-plugin/issues/1#issuecomment-2067916371).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-evals-plugin
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
