# llm-embed-onnx

[![PyPI](https://img.shields.io/pypi/v/llm-embed-onnx.svg)](https://pypi.org/project/llm-embed-onnx/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-embed-onnx?include_prereleases&label=changelog)](https://github.com/simonw/llm-embed-onnx/releases)
[![Tests](https://github.com/simonw/llm-embed-onnx/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-embed-onnx/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-embed-onnx/blob/main/LICENSE)

Run embedding models using the [ONNX Runtime](https://onnxruntime.ai)

This LLM plugin is a wrapper around [onnx_embedding_models](https://github.com/taylorai/onnx_embedding_models) by Benjamin Anderson.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-embed-onnx
```
## Usage

This plugin adds the following embedding models, which can be listed using `llm embed-models`:

```
onnx-bge-micro
onnx-gte-tiny
onnx-minilm-l6
onnx-minilm-l12
onnx-bge-small
onnx-bge-base
onnx-bge-large
```

You can run any of these models using `llm embed` command:

```bash
llm embed -m onnx-bge-micro -c "Example content"
```
This will output a 384 length JSON array of floating point numbers, starting:
```
[-0.03910085942622519, -0.0030843335461659795, 0.032797761260860724,
```
The first time you use any of these models the model will be downloaded to the `llm_embed_onnx` directory in your [LLM data directory](https://llm.datasette.io/en/stable/setup.html#setting-a-custom-directory-location). On macOS this defaults to:

`~/Library/Application Support/io.datasette.llm/llm_embed_onnx`

For more on how to use these embedding models see [the LLM embeddings documentation](https://llm.datasette.io/en/stable/embeddings/index.html).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-embed-onnx
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
