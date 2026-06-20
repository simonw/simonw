# llm-gguf

[![PyPI](https://img.shields.io/pypi/v/llm-gguf.svg)](https://pypi.org/project/llm-gguf/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-gguf?include_prereleases&label=changelog)](https://github.com/simonw/llm-gguf/releases)
[![Tests](https://github.com/simonw/llm-gguf/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-gguf/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-gguf/blob/main/LICENSE)

Run models distributed as GGUF files using [LLM](https://llm.datasette.io/)

## Installation

Install this plugin in the same environment as LLM:
```bash
llm install llm-gguf
```
## Usage

This plugin runs models that have been distributed as GGUF files.

You can either ask the plugin to download these directly, or you can register models you have already downloaded.

To download the LM Studio GGUF of Llama 3.1 8B Instruct, run the following command:

```bash
llm gguf download-model \
  https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  --alias llama-3.1-8b-instruct --alias l31i
```
The `--alias` options set aliases for that model, you can omit them if you don't want to set any.

This command will download the 4.92GB file and store it in the directory revealed by running `llm gguf models-dir` - on macOS this will be `~/Library/Application Support/io.datasette.llm/gguf/models`.

Run `llm models` to confirm that the model has been installed.

You can then run prompts through that model like this:
```bash
llm -m gguf/Meta-Llama-3.1-8B-Instruct-Q4_K_M 'Five great names for a pet lemur'
```
Or using one of the aliases that you set like this:
```bash
llm -m l31i 'Five great names for a pet lemur'
```
You can start a persistent chat session with the model using `llm chat` - this will avoid having to load the model into memory for each prompt:
```bash
llm chat -m l31i
```
```
Chatting with gguf/Meta-Llama-3.1-8B-Instruct-Q4_K_M
Type 'exit' or 'quit' to exit
Type '!multi' to enter multiple lines, then '!end' to finish
> tell me a joke about a walrus, a pelican and a lemur getting lunch
Here's one: Why did the walrus, the pelican, and the lemur go to the cafeteria for lunch? ...
```

If you have downloaded the model already you can register it with the plugin while keeping the file in its current location like this:
```bash
llm gguf register-model \
  ~/Downloads/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  --alias llama-3.1-8b-instruct --alias l31i
```

This plugin **currently only works with chat models** - these are usually distributed in files with the prefix `-Instruct` or `-Chat` or similar.

For non-chat models you may have better luck with the older [llm-llama-cpp plugin](https://github.com/simonw/llm-llama-cpp).

## Embedding models

This plugin also supports [embedding models](https://llm.datasette.io/en/stable/embeddings/index.html) that are distributed as GGUFs.

These are managed using the `llm gguf embed-models`, `llm gguf download-embed-model` and `llm gguf register-embed-model` commands.

For example, to start using the excellent and tiny [mxbai-embed-xsmall-v1](https://huggingface.co/mixedbread-ai/mxbai-embed-xsmall-v1) model you can download the 30.8MB GGUF version like this:

```bash
llm gguf download-embed-model \
  https://huggingface.co/mixedbread-ai/mxbai-embed-xsmall-v1/resolve/main/gguf/mxbai-embed-xsmall-v1-q8_0.gguf
```
This will store the model in the directory shown if you run `llm gguf models-dir`.

Confirm that the new model is available by running this:

```bash
llm embed-models
```
You should see `gguf/mxbai-embed-xsmall-v1-q8_0` in the list.

Then try that model out like this:

```bash
llm embed -m gguf/mxbai-embed-xsmall-v1-q8_0 -c 'hello'
```
This will output a 384 element floating point JSON array.

Consult the [LLM documentation](https://llm.datasette.io/en/stable/embeddings/index.html) for more information on how to use these embeddings.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-gguf
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
