# llm-llama-server

[![PyPI](https://img.shields.io/pypi/v/llm-llama-server.svg)](https://pypi.org/project/llm-llama-server/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-llama-server?include_prereleases&label=changelog)](https://github.com/simonw/llm-llama-server/releases)
[![Tests](https://github.com/simonw/llm-llama-server/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-llama-server/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-llama-server/blob/main/LICENSE)

Interact with llama-server models

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-llama-server
```
## Usage

You'll need to be running a [llama-server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) on port 8080 to use this plugin.

You can `brew install llama.cpp` to obtain that binary. Then run it like this:
```bash
llama-server -hf unsloth/gemma-3-4b-it-GGUF:Q4_K_XL
```
This loads and serves the [unsloth/gemma-3-4b-it-GGUF](https://huggingface.co/unsloth/gemma-3-4b-it-GGUF) GGUF version of [Gemma 3 4B](https://ai.google.dev/gemma/docs/core) - a 3.2GB download.

To access regular models from LLM, use the `llama-server` model:
```bash
llm -m llama-server "say hi"
```
For vision models, use `llama-server-vision`:
```bash
llm -m llama-server-vision describe -a path/to/image.png
```
For models with [tools](https://llm.datasette.io/en/stable/tools.html) (which also support vision) use `llama-server-tools`:
```bash
llm -m llama-server-tools -T llm_time 'time?' --td
```
You'll need to run the `llama-server` with the `--jinja` flag in order for this to work:
```bash
llama-server --jinja -hf unsloth/gemma-3-4b-it-GGUF:Q4_K_XL
```
Or for a slightly stronger [7.3GB model](https://huggingface.co/unsloth/gemma-3-12b-it-qat-GGUF):
```bash
llama-server --jinja -hf unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M
```
## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-llama-server
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
