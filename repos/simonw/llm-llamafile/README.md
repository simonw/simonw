# llm-llamafile

[![PyPI](https://img.shields.io/pypi/v/llm-llamafile.svg)](https://pypi.org/project/llm-llamafile/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-llamafile?include_prereleases&label=changelog)](https://github.com/simonw/llm-llamafile/releases)
[![Tests](https://github.com/simonw/llm-llamafile/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-llamafile/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-llamafile/blob/main/LICENSE)

Access llamafile localhost models via LLM

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-llamafile
```
## Usage

Make sure you have a `llamafile` running on `localhost`, serving an OpenAI compatible API endpoint on port 8080.

You can then use `llm` to interact with that model like so:

```bash
llm -m llamafile "3 neat characteristics of a pelican"
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-llamafile
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
