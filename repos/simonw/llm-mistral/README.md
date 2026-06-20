# llm-mistral

[![PyPI](https://img.shields.io/pypi/v/llm-mistral.svg)](https://pypi.org/project/llm-mistral/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-mistral?include_prereleases&label=changelog)](https://github.com/simonw/llm-mistral/releases)
[![Tests](https://github.com/simonw/llm-mistral/workflows/Test/badge.svg)](https://github.com/simonw/llm-mistral/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-mistral/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin providing access to [Mistral](https://mistral.ai) models using the Mistral API

## Installation

Install this plugin in the same environment as LLM:
```bash
llm install llm-mistral
```
## Usage

First, obtain an API key for [the Mistral API](https://console.mistral.ai/).

Configure the key using the `llm keys set mistral` command:
```bash
llm keys set mistral
```
```
<paste key here>
```
You can now access the Mistral hosted models. Run `llm models` for a list.

To run a prompt through `mistral-tiny`:

```bash
llm -m mistral-tiny 'A sassy name for a pet sasquatch'
```
To start an interactive chat session with `mistral-small`:
```bash
llm chat -m mistral-small
```
```
Chatting with mistral-small
Type 'exit' or 'quit' to exit
Type '!multi' to enter multiple lines, then '!end' to finish
> three proud names for a pet walrus
1. "Nanuq," the Inuit word for walrus, which symbolizes strength and resilience.
2. "Sir Tuskalot," a playful and regal name that highlights the walrus' distinctive tusks.
3. "Glacier," a name that reflects the walrus' icy Arctic habitat and majestic presence.
```
To use a system prompt with `mistral-medium` to explain some code:
```bash
cat example.py | llm -m mistral-medium -s 'explain this code'
```
## Vision

The Pixtral models are capable of interpreting images. You can use those like this:

```bash
llm -m pixtral-large 'describe this image' \
  -a https://static.simonwillison.net/static/2025/two-pelicans.jpg
```
Output:

> This image features two pelicans in flight against a clear blue sky. Pelicans are large water birds known for their long beaks and distinctive throat pouches, which they use for catching fish. In this photo, the birds are flying close to each other, showcasing their expansive wings and characteristic beaks. The clear sky provides a stark contrast, highlighting the details of their feathers and the graceful curves of their wings. The image captures a moment of synchronicity and elegance in nature.

You can pass filenames instead of URLs.

## Audio

The Voxtral models - `voxtral-small` and `voxtral-mini` - are capable of accepting audio input. This currently only works for URLs to MP3 files hosted online:

```bash
llm -m voxtral-small \
  -a https://static.simonwillison.net/static/2024/pelican-joke-request.mp3
```
Output:

> What do you call a pelican with no teeth? A gum-ican

## Tools

To see a list of Mistral models that support [tools](https://llm.datasette.io/en/stable/tools.html) (most of them) run:
```bash
llm models --tools -q mistral
```
Try one out like this:
```bash
llm -m mistral-medium -T llm_time 'What time is it?' --td
```
## Schemas

Mistral models (with the exception of `codestral-mamba`) also support [schemas](https://llm.datasette.io/en/stable/schemas.html):
```bash
llm -m mistral-small --schema 'name,bio:one sentence' 'invent a cool dog'
```
Output:
```json
{
  "name": "CyberHound",
  "bio": "A futuristic dog with glowing cybernetic enhancements and the ability to hack into any system."
}
```

## Model options

All three models accept the following options, using `-o name value` syntax:

- `-o temperature 0.7`: The sampling temperature, between 0 and 1. Higher increases randomness, lower values are more focused and deterministic.
- `-o top_p 0.1`: 0.1 means consider only tokens in the top 10% probability mass. Use this or temperature but not both.
- `-o max_tokens 20`: Maximum number of tokens to generate in the completion.
- `-o safe_mode 1`: Turns on [safe mode](https://docs.mistral.ai/platform/guardrailing/), which adds a system prompt to add guardrails to the model output.
- `-o random_seed 123`: Set an integer random seed to generate deterministic results.
- `-o prefix 'Prefix here`: Set a prefix that will be used for the start of the response. Try `{` to encourage JSON or `GlaDOS: ` to encourage a roleplay from a specific character.

## Available models

Run `llm models` for a full list of Mistral models. This plugin configures the following alias shortcuts:

<!-- [[[cog
import cog, json
from llm_mistral import DEFAULT_ALIASES
for model_id, alias in DEFAULT_ALIASES.items():
    cog.out(f"- `{alias}` for `{model_id}`\n")
]]] -->
- `mistral-tiny` for `mistral/mistral-tiny`
- `mistral-nemo` for `mistral/open-mistral-nemo`
- `mistral-small-2312` for `mistral/mistral-small-2312`
- `mistral-small-2402` for `mistral/mistral-small-2402`
- `mistral-small-2409` for `mistral/mistral-small-2409`
- `mistral-small-2501` for `mistral/mistral-small-2501`
- `magistral-small-2506` for `mistral/magistral-small-2506`
- `magistral-small` for `mistral/magistral-small-latest`
- `mistral-small` for `mistral/mistral-small-latest`
- `mistral-medium-2312` for `mistral/mistral-medium-2312`
- `mistral-medium-2505` for `mistral/mistral-medium-2505`
- `magistral-medium-2506` for `mistral/magistral-medium-2506`
- `magistral-medium` for `mistral/magistral-medium-latest`
- `mistral-medium` for `mistral/mistral-medium-latest`
- `mistral-large` for `mistral/mistral-large-latest`
- `codestral-mamba` for `mistral/codestral-mamba-latest`
- `codestral` for `mistral/codestral-latest`
- `ministral-3b` for `mistral/ministral-3b-latest`
- `ministral-8b` for `mistral/ministral-8b-latest`
- `pixtral-12b` for `mistral/pixtral-12b-latest`
- `pixtral-large` for `mistral/pixtral-large-latest`
- `devstral-small` for `mistral/devstral-small-latest`
- `voxtral-mini` for `mistral/voxtral-mini-2507`
- `voxtral-small` for `mistral/voxtral-small-2507`
<!-- [[[end]]] -->


## Refreshing the model list

Mistral sometimes release new models.

To make those models available to an existing installation of `llm-mistral` run this command:
```bash
llm mistral refresh
```
This will fetch and cache the latest list of available models. They should then become available in the output of the `llm models` command.

## Embeddings

The Mistral [Embeddings API](https://docs.mistral.ai/platform/client#embeddings) can be used to generate 1,024 dimensional embeddings for any text.

To embed a single string:

```bash
llm embed -m mistral-embed -c 'this is text'
```
This will return a JSON array of 1,024 floating point numbers.

Mistral's [Codestral Embed](https://mistral.ai/news/codestral-embed) is an embedding model that specializes in code. LLM supports that in four different sizes:

```bash
llm embed -m mistral/codestral-embed-256 -c 'code...'
llm embed -m mistral/codestral-embed-512 -c 'code...'
llm embed -m mistral/codestral-embed-1024 -c 'code...'
llm embed -m mistral/codestral-embed-1536 -c 'code...'
llm embed -m mistral/codestral-embed-3072 -c 'code...'
```
The number is the size of the vector that will be returned.

You can also use `codestral-embed` which is an alias for the default size, `codestral-embed-1536`.

```bash

The [LLM documentation](https://llm.datasette.io/en/stable/embeddings/index.html) has more, including how to embed in bulk and store the results in a SQLite database.

See [LLM now provides tools for working with embeddings](https://simonwillison.net/2023/Sep/4/llm-embeddings/) and [Embeddings: What they are and why they matter](https://simonwillison.net/2023/Oct/23/embeddings/) for more about embeddings.

## Development

To set up this plugin locally, first checkout the code and run the tests with `uv`:
```bash
cd llm-mistral
uv run pytest
```
To run `llm` against the development version of the plugin:
```bash
uv run llm -m mistral-small hi
```
