# llm-jina-api

[![PyPI](https://img.shields.io/pypi/v/llm-jina-api.svg)](https://pypi.org/project/llm-jina-api/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-jina-api?include_prereleases&label=changelog)](https://github.com/simonw/llm-jina-api/releases)
[![Tests](https://github.com/simonw/llm-jina-api/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-jina-api/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-jina-api/blob/main/LICENSE)

Access Jina AI embeddings via their API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-jina-api
```
## Usage

The plugin adds an embedding model called `jina-clip-v1-api`. You'll need to set [an API key](https://jina.ai/embeddings/) first:

```bash
llm keys set jina
# paste API key here
```

Follow the [LLM documentation](https://llm.datasette.io/en/stable/embeddings/cli.html) using `jina-clip-v1-api` as the model name. For example:

```bash
llm embed -m jina-clip-v1-api -c 'pelican'

# To embed an image file:
llm embed --binary -m jina-clip-v1-api -i pelican.jpg
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-jina-api
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
