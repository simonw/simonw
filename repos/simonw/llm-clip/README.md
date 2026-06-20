# llm-clip

[![PyPI](https://img.shields.io/pypi/v/llm-clip.svg)](https://pypi.org/project/llm-clip/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-clip?include_prereleases&label=changelog)](https://github.com/simonw/llm-clip/releases)
[![Tests](https://github.com/simonw/llm-clip/workflows/Test/badge.svg)](https://github.com/simonw/llm-clip/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-clip/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for embedding images and text using [CLIP](https://openai.com/research/clip)

## Installation

Install this plugin in the same environment as LLM.
```bash
llm install llm-clip
```

## Usage

Once you have installed an embedding model you can use it to embed text like this:

```bash
llm embed -m clip -c 'Hello world'
```
Or an image like this:
```bash
llm embed -m clip --binary -i IMG_4801.jpeg
```

Embeddings are more useful if you store them in a database - see [the LLM documentation](https://llm.datasette.io/en/stable/embeddings/cli.html#storing-embeddings-in-sqlite) for details.

To embed every photograph in a folder and save them in a collection called "photos":

```bash
llm embed-multi photos -m clip --binary --files photos/ '*.jpg'
```
You can then search for photos of specific things like this:
```bash
llm similar photos -c 'bunny'
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-clip
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
