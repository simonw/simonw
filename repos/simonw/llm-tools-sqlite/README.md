# llm-tools-sqlite

[![PyPI](https://img.shields.io/pypi/v/llm-tools-sqlite.svg)](https://pypi.org/project/llm-tools-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-tools-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/llm-tools-sqlite/releases)
[![Tests](https://github.com/simonw/llm-tools-sqlite/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-tools-sqlite/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-sqlite/blob/main/LICENSE)

LLM tools for running queries against SQLite

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-sqlite
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm -T 'SQLite("content.db")' \
  "Count rows in the most interesting looking table" --td
```
Or use `llm chat` to chat with your database over multiple rounds:
```bash
llm chat -T 'SQLite("content.db")' 
```
This tool currently only supports read-only queries. Attempts to write to the database will fail with an error.

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_sqlite import SQLite

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "Show me the three most interesting looking tables",
    tools=[SQLite("content.db")]
)
for s in result:
    print(s, end="", flush=True)
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-sqlite
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
