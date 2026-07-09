# llm-meta-ai

[![PyPI](https://img.shields.io/pypi/v/llm-meta-ai.svg)](https://pypi.org/project/llm-meta-ai/)
[![Tests](https://github.com/simonw/llm-meta-ai/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-meta-ai/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-meta-ai?include_prereleases&label=changelog)](https://github.com/simonw/llm-meta-ai/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-meta-ai/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for models hosted by the [Meta AI API](https://developer.meta.com/ai/)

## Installation

Install this plugin in the same environment as LLM:
```bash
llm install llm-meta-ai
```

## Usage

First, obtain an API key for the Meta AI API and set it as a key called `meta-ai`:

```bash
llm keys set meta-ai
# Paste key here
```

You can also set the key using the `META_AI_TOKEN` environment variable.

Run `llm models` to get a full list of available models. Models are prefixed with `meta-ai/`, for example:

```bash
llm -m meta-ai/muse-spark-1.1 "What is the capital of France?"
```

You can also list just the Meta AI models like this:

```bash
llm meta-ai models
```
Add `--json` for the full JSON model definitions.

The list of models is fetched from the API and cached for an hour. Run this command to refresh it:

```bash
llm meta-ai refresh
```

### Reasoning

These are reasoning models: they think before they answer, and the reasoning tokens count towards your output token budget - they are reported in the `completion_tokens_details.reasoning_tokens` key in `llm logs --json`. Control how much the model reasons with the `reasoning_effort` option, one of `none`, `minimal`, `low`, `medium`, `high` or `xhigh` (not every model supports every value):

```bash
llm -m meta-ai/muse-spark-1.1 'What is the capital of France?' -o reasoning_effort low
```

### Rate limits and max_tokens

Requests count against an output token rate limit *before* they run. Setting a token limit on your prompts helps avoid exhausting your quota - leave generous room for reasoning tokens:

```bash
llm -m meta-ai/muse-spark-1.1 'A short poem about a pelican' -o max_tokens 2000
```

Rate limits are applied per model - a model that returns 429 errors even after a long wait may not be enabled for your team, even if it shows up in the models list.

### Attachments

Models accept images (PNG, JPEG, WebP, GIF, ICO) and PDFs:

```bash
llm -m meta-ai/muse-spark-1.1 'Describe this image' \
  -a https://static.simonwillison.net/static/2024/pelicans.jpg
```

The API also supports MP4 video via its Files API, which this plugin does not yet use.

### Tools

Meta AI models support [tools](https://llm.datasette.io/en/stable/tools.html):

```bash
llm -m meta-ai/muse-spark-1.1 -T llm_time 'What time is it?' --td
```

### Schemas

They support [schemas](https://llm.datasette.io/en/stable/schemas.html) as well:

```bash
llm -m meta-ai/muse-spark-1.1 'Invent a dog' --schema 'name, age int, breed'
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd llm-meta-ai
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e . --group dev
```
To run the tests:
```bash
python -m pytest
```
