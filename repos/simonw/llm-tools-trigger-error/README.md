# llm-tools-trigger-error

[![PyPI](https://img.shields.io/pypi/v/llm-tools-trigger-error.svg)](https://pypi.org/project/llm-tools-trigger-error/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-tools-trigger-error?include_prereleases&label=changelog)](https://github.com/simonw/llm-tools-trigger-error/releases)
[![Tests](https://github.com/simonw/llm-tools-trigger-error/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-tools-trigger-error/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-trigger-error/blob/main/LICENSE)

Trigger an LLM tools error, useful for testing

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-trigger-error
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm -T trigger_error "Trigger an error about an escaped badger" --tools-debug
```

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_trigger_error import trigger_error

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "Trigger an error about an escaped badger",
    tools=[trigger_error]
).text()
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-trigger-error
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
