# llm-openrouter

[![PyPI](https://img.shields.io/pypi/v/llm-openrouter.svg)](https://pypi.org/project/llm-openrouter/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-openrouter?include_prereleases&label=changelog)](https://github.com/simonw/llm-openrouter/releases)
[![Tests](https://github.com/simonw/llm-openrouter/workflows/Test/badge.svg)](https://github.com/simonw/llm-openrouter/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-openrouter/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for models hosted by [OpenRouter](https://openrouter.ai/)

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM.
```bash
llm install llm-openrouter
```

## Configuration

You will need an API key from OpenRouter. You can [obtain one here](https://openrouter.ai/keys).

You can set that as an environment variable called `OPENROUTER_KEY`, or add it to the `llm` set of saved keys using:

```bash
llm keys set openrouter
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
OpenRouter: openrouter/openai/gpt-3.5-turbo
OpenRouter: openrouter/anthropic/claude-sonnet-4
OpenRouter: openrouter/meta-llama/llama-2-70b-chat
...
```
The list of models from OpenRouter is cached for an hour. You can force a refresh using this command:
```bash
llm openrouter refresh
```

To run a prompt against a model, pass its full model ID to the `-m` option, like this:
```bash
llm -m openrouter/anthropic/claude-sonnet-4 "Five spooky names for a pet tarantula"
```
You can set a shorter alias for a model using the `llm aliases` command like so:
```bash
llm aliases set claude openrouter/anthropic/claude-sonnet-4
```
Now you can prompt Claude using:
```bash
cat llm_openrouter.py | llm -m claude -s 'write some pytest tests for this'
```

Images are supported too, for some models:
```bash
llm -m openrouter/anthropic/claude-3.5-sonnet 'describe this image' -a https://static.simonwillison.net/static/2024/pelicans.jpg
llm -m openrouter/anthropic/claude-3-haiku 'extract text' -a page.png
```

### Vision models

Some OpenRouter models can accept image attachments. Run this command:

```bash
llm models --options -q openrouter
```
And look for models that list these attachment types:

```
  Attachment types:
    application/pdf, image/gif, image/jpeg, image/png, image/webp
```
You can feed these models images as URLs or file paths, for example:

```bash
llm -m openrouter/google/gemini-flash-1.5 'describe image' \
  -a https://static.simonwillison.net/static/2025/two-pelicans.jpg
```

### Schemas

LLM includes support for [schemas](https://llm.datasette.io/en/stable/schemas.html), allowing you to control the JSON structure of the output returned by the model.

Some of the models provided by OpenRouter are compatible with this feature, see [their full list of structured output models](https://openrouter.ai/models?order=newest&supported_parameters=structured_outputs) for details.

`llm-openrouter` currently enables schema support for the models in that list. Models have varying levels of quality in their schema support, so test carefully rather than assuming all models will correctly work the same.

```bash
llm -m openrouter/google/gemini-flash-1.5 'invent 3 cool capybaras' \
  --schema-multi 'name,bio'
```
Output:
```json
{
  "items": [
    {
      "bio": "Chill vibes only.  Spends most days floating on lily pads, occasionally accepting head scratches from passing frogs.",
      "name": "Professor Fluffernutter"
    },
    {
      "bio": "A thrill-seeker!  Capybara extraordinaire known for her daring escapes from the local zoo and impromptu skateboarding sessions.",
      "name": "Capybara-bara the Bold"
    },
    {
      "bio": "A renowned artist, creating masterpieces using mud, leaves, and her own surprisingly dexterous paws.",
      "name": "Michelangelo Capybara"
    }
  ]
}
```

### Tools

Most OpenRouter models support [tool calls](https://llm.datasette.io/en/stable/tools.html). You can try that out like so:

```bash
llm -m openrouter/openai/gpt-5 \
  -T llm_version -T llm_time \
  "What version of LLM and what time is it?" \
  --tools-debug
```
Example output:
```
Tool call: llm_version({})
  0.27.1


Tool call: llm_time({})
  {
    "utc_time": "2025-09-20 23:35:53 UTC",
    "utc_time_iso": "2025-09-20T23:35:53.205247+00:00",
    "local_timezone": "PDT",
    "local_time": "2025-09-20 16:35:53",
    "timezone_offset": "UTC-7:00",
    "is_dst": true
  }

LLM version: 0.27.1
Current time: 2025-09-20 16:35:53 PDT (2025-09-20 23:35:53 UTC)
```

### Reasoning

Some OpenRouter models such as [GPT-5](https://openrouter.ai/openai/gpt-5) support options for controlling reasoning:

- `-o reasoning_effort low|medium|high` - control reasoning effort
- `-o reasoning_max_tokens 2048` - an alternative way of specifying effort for some models
- `-o reasoning_enabled true` - use this to enable reasoning without setting an effort via one of the other two options

For example:

```bash
llm -m openrouter/openai/gpt-5 \
   'prove dogs exist' \
   -o reasoning_effort high
```

### Provider routing

OpenRouter offers [comprehensive options](https://openrouter.ai/docs/features/provider-routing) for controlling which underlying provider your request is routed to.

You can specify these using the OpenRouter JSON format, then pass that to LLM using the `-o provider '{JSON goes here}` option:

```bash
llm -m openrouter/meta-llama/llama-3.1-8b-instruct hi \
  -o provider '{"quantizations": ["fp8"]}'
```
This specifies that you would like only providers that [support fp8 quantization](https://openrouter.ai/docs/features/provider-routing#example-requesting-fp8-quantization) for that model.

### Incorporating search results from Exa

OpenRouter have [a partnership](https://openrouter.ai/docs/features/web-search) with [Exa](https://exa.ai/) where prompts through _any_ supported model can be augmented with relevant search results from the Exa index - a form of RAG.

Enable this feature using the `-o online 1` option:

```bash
llm -m openrouter/mistralai/mistral-small -o online 1 'key events on march 1st 2025'
```
Consult the OpenRouter documentation for [current pricing](https://openrouter.ai/docs/features/web-search#pricing).

### Listing models

The `llm models -q openrouter` command will display all available models, or you can use this command to see more detailed JSON:

```bash
llm openrouter models
```
Output starts like this:
```yaml
- id: latitudegames/wayfarer-large-70b-llama-3.3
  name: LatitueGames: Wayfarer Large 70B Llama 3.3
  context_length: 128,000
  architecture: text->text Llama3
  pricing: prompt $0.7/M, completion $0.7/M

- id: thedrummer/skyfall-36b-v2
  name: TheDrummer: Skyfall 36B V2
  context_length: 64,000
  architecture: text->text Other
  pricing: prompt $0.5/M, completion $0.5/M

- id: microsoft/phi-4-multimodal-instruct
  name: Microsoft: Phi 4 Multimodal Instruct
  context_length: 131,072
  architecture: text+image->text Other
  pricing: prompt $0.07/M, completion $0.14/M, image $0.2476/K
```
Add `--json` to get back JSON instead, which looks like this:
```json
[
  {
    "id": "microsoft/phi-4-multimodal-instruct",
    "name": "Microsoft: Phi 4 Multimodal Instruct",
    "created": 1741396284,
    "description": "Phi-4 Multimodal Instruct is a versatile...",
    "context_length": 131072,
    "architecture": {
      "modality": "text+image->text",
      "tokenizer": "Other",
      "instruct_type": null
    },
    "pricing": {
      "prompt": "0.00000007",
      "completion": "0.00000014",
      "image": "0.0002476",
      "request": "0",
      "input_cache_read": "0",
      "input_cache_write": "0",
      "web_search": "0",
      "internal_reasoning": "0"
    },
    "top_provider": {
      "context_length": 131072,
      "max_completion_tokens": null,
      "is_moderated": false
    },
    "per_request_limits": null
  }
```
Add `--free` for a list of just the models that are [available for free](https://openrouter.ai/models?max_price=0).
```bash
llm openrouter models --free
```

### Information about your API key

The `llm openrouter key` command shows you information about your current API key, including rate limits:

```bash
llm openrouter key
```
Example output:
```json
{
  "label": "sk-or-v1-0fa...240",
  "limit": null,
  "usage": 0.65017511,
  "limit_remaining": null,
  "is_free_tier": false,
  "rate_limit": {
    "requests": 40,
    "interval": "10s"
  }
}
```
This will default to inspecting the key you have set using `llm keys set openrouter` or using the `OPENROUTER_KEY` environment variable.

You can inspect a different key by passing the key itself - or the name of the key in the `llm keys` list - as the `--key` option:

```bash
llm openrouter key --key sk-xxx
```

## Development

To set up this plugin locally, first checkout the code. Then run the tests with `uv`:
```bash
cd llm-openrouter
uv run pytest
```
To run LLM with the plugin available:
```bash
uv run llm models
```
To update recordings and snapshots, run:
```bash
PYTEST_OPENROUTER_KEY="$(llm keys get openrouter)" \
  uv run pytest --record-mode=rewrite --inline-snapshot=fix
```

If tests against additional models are added, update `tests/models_persister.py` to preserve those model ids in the recordings.
