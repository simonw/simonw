# llm-gpt4all

[![PyPI](https://img.shields.io/pypi/v/llm-gpt4all.svg)](https://pypi.org/project/llm-gpt4all/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-gpt4all?include_prereleases&label=changelog)](https://github.com/simonw/llm-gpt4all/releases)
[![Tests](https://github.com/simonw/llm-gpt4all/workflows/Test/badge.svg)](https://github.com/simonw/llm-gpt4all/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-gpt4all/blob/main/LICENSE)

Plugin for [LLM](https://llm.datasette.io/) adding support for the [GPT4All](https://gpt4all.io/) collection of models.

## Installation

Install this plugin in the same environment as LLM.
```bash
llm install llm-gpt4all
```
After installing the plugin you can see a new list of available models like this:

```bash
llm models list
```
The output will include something like this:
```
gpt4all: all-MiniLM-L6-v2-f16 - SBert, 43.76MB download, needs 1GB RAM (installed)
gpt4all: orca-mini-3b-gguf2-q4_0 - Mini Orca (Small), 1.84GB download, needs 4GB RAM (installed)
gpt4all: mistral-7b-instruct-v0 - Mistral Instruct, 3.83GB download, needs 8GB RAM (installed)
gpt4all: mistral-7b-openorca - Mistral OpenOrca, 3.83GB download, needs 8GB RAM (installed)
gpt4all: Meta-Llama-3-8B-Instruct - Llama 3 Instruct, 4.34GB download, needs 8GB RAM (installed) (aliases: l3)
gpt4all: all-MiniLM-L6-v2 - SBert, 43.82MB download, needs 1GB RAM
gpt4all: nomic-embed-text-v1 - Nomic Embed Text v1, 261.58MB download, needs 1GB RAM
gpt4all: nomic-embed-text-v1 - Nomic Embed Text v1.5, 261.58MB download, needs 1GB RAM
gpt4all: replit-code-v1_5-3b-newbpe-q4_0 - Replit, 1.82GB download, needs 4GB RAM
gpt4all: mpt-7b-chat - MPT Chat, 3.54GB download, needs 8GB RAM
gpt4all: orca-2-7b - Orca 2 (Medium), 3.56GB download, needs 8GB RAM
gpt4all: rift-coder-v0-7b-q4_0 - Rift coder, 3.56GB download, needs 8GB RAM
gpt4all: mpt-7b-chat-newbpe-q4_0 - MPT Chat, 3.64GB download, needs 8GB RAM
gpt4all: em_german_mistral_v01 - EM German Mistral, 3.83GB download, needs 8GB RAM
gpt4all: ghost-7b-v0 - Ghost 7B v0.9.1, 3.83GB download, needs 8GB RAM
gpt4all: Nous-Hermes-2-Mistral-7B-DPO - Nous Hermes 2 Mistral DPO, 3.83GB download, needs 8GB RAM
gpt4all: gpt4all-falcon-newbpe-q4_0 - GPT4All Falcon, 3.92GB download, needs 8GB RAM
gpt4all: gpt4all-13b-snoozy-q4_0 - Snoozy, 6.86GB download, needs 16GB RAM
gpt4all: wizardlm-13b-v1 - Wizard v1.2, 6.86GB download, needs 16GB RAM
gpt4all: orca-2-13b - Orca 2 (Full), 6.86GB download, needs 16GB RAM
gpt4all: nous-hermes-llama2-13b - Hermes, 6.86GB download, needs 16GB RAM
gpt4all: starcoder-newbpe-q4_0 - Starcoder, 8.37GB download, needs 4GB RAM
```
Further details on these models can be found [in this Observable notebook](https://observablehq.com/@simonw/gpt4all-models).

## Usage

### Model Installation and Prompting

You can execute a model using the name displayed in the `llm models list` output. The model file will be downloaded the first time you attempt to run it.

```bash
llm -m orca-mini-3b-gguf2-q4_0 '3 names for a pet cow'
```
The first time you run this you will see a progress bar for the model file download:
```
 31%|█████████▋                        | 1.16G/3.79G [00:26<01:02, 42.0MiB/s]
```
On subsequent uses the model output will be displayed immediately.

Note that the models will be downloaded to `~/.cache/gpt4all`.

### Model options

Run `llm models --options` for a list of available model options, which should include:

```
gpt4all: mistral-7b-instruct-v0 - Mistral Instruct, 3.83GB download, needs 8GB RAM (installed)
  max_tokens: int
    The maximum number of tokens to generate.
  temp: float
    The model temperature. Larger values increase creativity but decrease
    factuality.
  top_k: int
    Randomly sample from the top_k most likely tokens at each generation
    step. Set this to 1 for greedy decoding.
  top_p: float
    Randomly sample at each generation step from the top most likely
    tokens whose probabilities add up to top_p.
  repeat_penalty: float
    Penalize the model for repetition. Higher values result in less
    repetition.
  repeat_last_n: int
    How far in the models generation history to apply the repeat penalty.
  n_batch: int
    Number of prompt tokens processed in parallel. Larger values decrease
    latency but increase resource requirements.
```
Use them like this:

```bash
llm -m mistral-7b-instruct-v0 -o max_tokens 2 'hi'
```
```
Hello!
```

### Chatting

To chat with a model, avoiding the need to load it into memory for every message, use `llm chat`:

```bash
llm chat -m orca-mini-3b-gguf2-q4_0
```
```
Chatting with orca-mini-3b-gguf2-q4_0
Type 'exit' or 'quit' to exit
Type '!multi' to enter multiple lines, then '!end' to finish
> hi
 Hello! How can I assist you today?
> three jokes about a pelican and a chicken who are friends
 Sure, here are three jokes about a pelican and a chicken who are friends:

1. Why did the pelican cross the road? To get to the other side where the chicken was waiting for him!
2. What do you call a group of chickens playing basketball? A flock of feathers!
3. Why did the chicken invite the pelican over for dinner? Because it had nothing else to eat and needed some extra protein in its diet!
```

### Removing Models

To remove a downloaded model, delete the `.gguf` file from `~/.cache/gpt4all`.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-gpt4all
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
