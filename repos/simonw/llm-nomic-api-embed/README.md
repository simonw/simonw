# llm-nomic-api-embed

[![PyPI](https://img.shields.io/pypi/v/llm-nomic-api-embed.svg)](https://pypi.org/project/llm-nomic-api-embed/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-nomic-api-embed?include_prereleases&label=changelog)](https://github.com/simonw/llm-nomic-api-embed/releases)
[![Tests](https://github.com/simonw/llm-nomic-api-embed/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-nomic-api-embed/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-nomic-api-embed/blob/main/LICENSE)

Create embeddings using the Nomic API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-nomic-api-embed
```
## Usage

This plugin requires [a Nomic API key](https://atlas.nomic.ai/). These include a generous free allowance for their embedding API.

Configure the key like this:
```bash
llm keys set nomic
# Paste key here
```
You can then use the Nomic embedding models like this:
```bash
llm embed -m nomic-1.5 -c 'hello world'
```
This will return a 768 item floating point array as JSON.

See [the LLM embeddings documentation](https://llm.datasette.io/en/stable/embeddings/index.html) for more you can do with the tool.

## Models

Run `llm embed-models` for a full list. The Nomic models are:

```
nomic-embed-text-v1 (aliases: nomic-1)
nomic-embed-text-v1.5 (aliases: nomic-1.5)
nomic-embed-text-v1.5-512 (aliases: nomic-1.5-512)
nomic-embed-text-v1.5-256 (aliases: nomic-1.5-256)
nomic-embed-text-v1.5-128 (aliases: nomic-1.5-128)
nomic-embed-text-v1.5-64 (aliases: nomic-1.5-64)
nomic-embed-vision-v1
nomic-embed-vision-v1.5
nomic-embed-combined-v1
nomic-embed-combined-v1.5
```
Vision models can be used with image files using the `--binary` option, for example:

```bash
llm embed-multi images --files . '*.png' \
  --binary --model nomic-embed-vision-v1.5
```

### Combined vision and text models

The `nomic-embed-combined-v1` and `nomic-embed-combined-v1.5` models are special - they will automatically use their respective text models for text inputs and their respective vision models for images.

This means you can use them to create a collection that mixes images and text, or you can create an image collection with them and then use text to find similar images.

Here's how do do that for a `photos/` directory full of JPEGs:

```bash
llm embed-multi --binary -m nomic-embed-combined-v1.5 \
  -d photos.db photos --files photos/ '*.jpeg'
```
Then run similarity searches like this:
```bash
llm similar photos -d photos.db -c pelican
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-nomic-api-embed
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
