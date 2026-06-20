# llm-logging-debug

[![PyPI](https://img.shields.io/pypi/v/llm-logging-debug.svg)](https://pypi.org/project/llm-logging-debug/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-logging-debug?include_prereleases&label=changelog)](https://github.com/simonw/llm-logging-debug/releases)
[![Tests](https://github.com/simonw/llm-logging-debug/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-logging-debug/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-logging-debug/blob/main/LICENSE)

Set logging.DEBUG while running LLM

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-logging-debug
```
## Usage

Set the `LLM_LOGGING_DEBUG` environment variable to `1` before running LLM:
```bash
export LLM_LOGGING_DEBUG=1
llm "Say hello in five languages" -m gemma3:27b
```
Or just for one invocation like this:
```bash
LLM_LOGGING_DEBUG=1 llm "Say hello in five languages" -m gemma3:27b
```
This will set the Python logging level to `DEBUG` for the duration of the LLM command.

One consequence of this is that plugins that use `httpx` will show detailed debugging information about the requests they are making.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-logging-debug
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
