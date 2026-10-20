# llm-public-ai

[![PyPI](https://img.shields.io/pypi/v/llm-public-ai.svg)](https://pypi.org/project/llm-public-ai/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-public-ai?include_prereleases&label=changelog)](https://github.com/simonw/llm-public-ai/releases)
[![Tests](https://github.com/simonw/llm-public-ai/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-public-ai/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-public-ai/blob/main/LICENSE)

Access models hosted by the [Public AI Inference Utility](https://publicai.co/) from [LLM](https://llm.datasette.io/), including the Swiss AI [Apertus](https://www.swiss-ai.org/apertus) models, AI Singapore's SEA-LION models, Bielik and ALIA.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-public-ai
```
## Configuration

You will need an API key from the [Public AI developer portal](https://platform.publicai.co/). Configure it like this:
```bash
llm keys set publicai
# Paste key here
```
Or set the `PUBLICAI_API_KEY` environment variable.

## Usage

Models are listed by the Public AI API and registered with a `publicai/` prefix. Run `llm models -q publicai` to see them:

```bash
llm -m publicai/swiss-ai/apertus-70b-instruct "Three fun facts about Switzerland"
```
The list of models is cached in `publicai_models.json` in the LLM user directory and refreshed once an hour. To refresh it immediately run:
```bash
llm publicai refresh
```
To see the models along with their pricing and the features this plugin supports for each one:
```bash
llm publicai models
```
Add `--json` for the raw JSON returned by the API.

The `/v1/models` endpoint does not report model capabilities, so the plugin records which models support tools, schemas, images and thinking based on testing each one. Models not in that list are assumed to support tools and schemas.

### Thinking

`swiss-ai/apertus-v1.5-70b`, `aisingapore/Qwen-SEA-LION-v4.5-27B-IT` and `aisingapore/Nemotron-SEA-LION-v4.8-120B-A12B` can turn their thinking mode on or off using the `thinking` option. Apertus v1.5 does not think by default; the two SEA-LION models do:
```bash
llm -m publicai/swiss-ai/apertus-v1.5-70b -o thinking 1 "What is 47 * 86?"
llm -m publicai/aisingapore/Qwen-SEA-LION-v4.5-27B-IT -o thinking 0 "Hello"
```
None of these models support thinking levels: `reasoning_effort` and similar parameters are ignored by the API.

Reasoning is displayed separately from the response, and can be hidden using `llm -R/--hide-reasoning`. Apertus v1.5 returns its thinking inline wrapped in `<|inner_prefix|>` and `<|inner_suffix|>` tokens; the plugin separates that out into reasoning.

The Public AI gateway caches responses, and its cache ignores the thinking setting. The plugin bypasses that cache for models that support `thinking`, so a cached response generated with the other setting is never returned.

### Tools, schemas and images

Most models support [tools](https://llm.datasette.io/en/stable/tools.html) and [schemas](https://llm.datasette.io/en/stable/schemas.html):
```bash
llm -m publicai/aisingapore/Qwen-SEA-LION-v4-32B-IT -T llm_version "What version of LLM is this?" --td
llm -m publicai/speakleash/Bielik-11B-v3.0-Instruct --schema 'name, age int, bio' "Invent a dog"
```
`swiss-ai/apertus-v1.5-70b`, `aisingapore/Gemma-SEA-LION-v4-27B-IT` and `aisingapore/Qwen-SEA-LION-v4.5-27B-IT` accept image attachments:
```bash
llm -m publicai/swiss-ai/apertus-v1.5-70b -a photo.jpg "Describe this image"
```
### Options

All models support the `temperature`, `max_tokens`, `top_p`, `frequency_penalty`, `presence_penalty`, `stop` and `seed` options. Run `llm models --options -q publicai` for details.

## Development

To set up this plugin locally, first checkout the code. Then run the tests with `uv`:
```bash
cd llm-public-ai
uv run pytest
```
The tests replay recorded API responses from `tests/cassettes`. To record new ones, set `PUBLICAI_API_KEY` and run:
```bash
uv run pytest --record-mode once
```
To run LLM with your in-development plugin:
```bash
uv run llm --help
```
