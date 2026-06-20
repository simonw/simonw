# llm-rag

[![PyPI](https://img.shields.io/pypi/v/llm-rag.svg)](https://pypi.org/project/llm-rag/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-rag?include_prereleases&label=changelog)](https://github.com/simonw/llm-rag/releases)
[![Tests](https://github.com/simonw/llm-rag/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-rag/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-rag/blob/main/LICENSE)

Run Retrieval Augmented Generation against collections stored by LLM

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-rag
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-rag
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
