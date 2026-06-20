# llm-anyscale-endpoints

[![PyPI](https://img.shields.io/pypi/v/llm-anyscale-endpoints.svg)](https://pypi.org/project/llm-anyscale-endpoints/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-anyscale-endpoints?include_prereleases&label=changelog)](https://github.com/simonw/llm-anyscale-endpoints/releases)
[![Tests](https://github.com/simonw/llm-anyscale-endpoints/workflows/Test/badge.svg)](https://github.com/simonw/llm-anyscale-endpoints/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-anyscale-endpoints/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for models hosted by [Anyscale Endpoints](https://app.endpoints.anyscale.com/)

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM.
```bash
llm install llm-anyscale-endpoints
```
## Configuration

You will need an API key from Anyscale Endpoints. You can [obtain one here](https://app.endpoints.anyscale.com/).

You can set that as an environment variable called `LLM_ANYSCALE_ENDPOINTS_KEY`, or add it to the `llm` set of saved keys using:

```bash
llm keys set anyscale-endpoints
```
```
Enter key: <paste key here>
```

## Usage

To list available models, run:
```bash
llm models list
```
You should see a list that looks something like this:
```
AnyscaleEndpoints: meta-llama/Llama-2-7b-chat-hf
AnyscaleEndpoints: meta-llama/Llama-2-13b-chat-hf
AnyscaleEndpoints: mistralai/Mixtral-8x7B-Instruct-v0.1
AnyscaleEndpoints: mistralai/Mistral-7B-Instruct-v0.1
AnyscaleEndpoints: meta-llama/Llama-2-70b-chat-hf
AnyscaleEndpoints: meta-llama/Llama-3-8b-chat-hf
AnyscaleEndpoints: meta-llama/Llama-3-70b-chat-hf
AnyscaleEndpoints: codellama/CodeLlama-70b-Instruct-hf
AnyscaleEndpoints: mistralai/Mixtral-8x22B-Instruct-v0.1
AnyscaleEndpoints: mlabonne/NeuralHermes-2.5-Mistral-7B
AnyscaleEndpoints: google/gemma-7b-it
```
To run a prompt against a model, pass its full model ID to the `-m` option, like this:
```bash
llm -m mistralai/Mixtral-8x22B-Instruct-v0.1 \
  'Five strident names for a pet walrus' \
  --system 'You love coming up with creative names for pets'
```
You can set a shorter alias for a model using the `llm aliases` command like so:
```bash
llm aliases set mix22b mistralai/Mixtral-8x22B-Instruct-v0.1
```
Now you can prompt Mixtral-8x22B-Instruct-v0.1 using the alias `mix22b`:
```bash
cat llm_anyscale_endpoints.py | \
  llm -m mix22b -s 'explain this code'
```

You can refresh the list of models by running:
```bash
llm anyscale-endpoints refresh
```
This will fetch the latest list of models from Anyscale Endpoints and story it in a local cache file.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-anyscale-endpoints
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
