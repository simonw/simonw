# llm-glm

[![PyPI](https://img.shields.io/pypi/v/llm-glm.svg)](https://pypi.org/project/llm-glm/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-glm?include_prereleases&label=changelog)](https://github.com/simonw/llm-glm/releases)
[![Tests](https://github.com/simonw/llm-glm/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-glm/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-glm/blob/main/LICENSE)

Access models via the Z.ai API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-glm
```
## Usage

First, obtain an API key from [the Z.ai API keys page](https://z.ai/manage-apikey/apikey-list). Set it as the `zai` key:
```bash
llm keys set zai
# Paste key here
```
You can also set it using the `ZAI_API_KEY` environment variable.

Run `llm models -q glm` to see the available models, then run a prompt against one of them:
```bash
llm -m zai-glm/glm-5.3 'Five great names for a pet pelican'
```
Start a chat session with `llm chat`:
```bash
llm chat -m zai-glm/glm-5.3
```
This plugin uses the Z.ai [OpenAI Responses compatible API](https://docs.z.ai/devpack/quick-start) at `https://api.z.ai/api/v1`.

### Standard keys and GLM Coding Plan keys

Z.ai issues separate keys for pay-as-you-go API usage and for the [GLM Coding Plan](https://docs.z.ai/devpack/overview). Either kind of key can be set using `llm keys set zai`. Z.ai bill each request according to the type of key that was used to make it.

To use both, save the second key under a name of your choosing:
```bash
llm keys set zai-api
```
Then pass that name to `--key` to use it for a prompt:
```bash
llm -m zai-glm/glm-5.4 --key zai-api 'Five great names for a pet pelican'
```
The list of models is fetched using the `zai` key or `ZAI_API_KEY`. If you have not set either of those, fetch the list once using a key of your choice:
```bash
llm glm refresh --key zai-api
```

### Models

The list of models is fetched from Z.ai and cached for an hour. To fetch the latest list straight away:
```bash
llm glm refresh
```
The list can include models that your key does not have permission to use.

To see that list of models:
```bash
llm glm models
```
The Z.ai API includes details for some models about whether they accept images and which reasoning efforts they support. Models without this information are treated as supporting every feature, but will return errors if you attempt to use a feature that is not supported.

Add `--json` for the full details as JSON:
```bash
llm glm models --json
```

Both commands accept an optional `--key`.

### Reasoning

Most of these models reason before they answer. That reasoning is displayed as it streams in. Use `-R/--hide-reasoning` to hide it.

Use the `reasoning_effort` option to control how much reasoning a model does:
```bash
llm -m zai-glm/glm-5.3 'Why is the sky blue?' -o reasoning_effort low
```
Different models accept different values. `glm-5.3` and `glm-5.3-flash` accept `low`, `high` and `max`. Older models such as `glm-5.2` also accept `none` or `minimal`, which turn reasoning off. `llm glm models` shows the supported values for the models that Z.ai describe.

### Options

- `-o reasoning_effort low` - see above
- `-o temperature 0.5` - sampling temperature, from 0.0 to 1.0
- `-o top_p 0.9` - nucleus sampling, from 0.01 to 1.0
- `-o max_tokens 1000` - maximum number of tokens to generate, which includes reasoning tokens
- `-o json_object 1` - output a JSON object. The prompt must mention JSON

### Images

Some models, such as `glm-5.3-flash`, accept images as attachments:
```bash
llm -m zai-glm/glm-5.3-flash 'Describe this image' -a image.jpg
llm -m zai-glm/glm-5.3-flash 'Describe this image' \
  -a https://static.simonwillison.net/static/2024/pelicans.jpg
```

### Tools and schemas

These models support [tools](https://llm.datasette.io/en/stable/tools.html):
```bash
llm -m zai-glm/glm-5.3 'What time is it?' -T llm_time --td
```
And [schemas](https://llm.datasette.io/en/stable/schemas.html):
```bash
llm -m zai-glm/glm-5.3 'Invent a dog' --schema 'name, age int'
```
Schemas are only available for models that support them: currently `glm-5.3`, `glm-5.3-flash` and `glm-5.4`.

## Development

To set up this plugin locally, first checkout the code. Then run the tests with `uv`:
```bash
cd llm-glm
uv run pytest
```
To run LLM with your in-development plugin:
```bash
uv run llm --help
```
To record new cassettes for the tests that talk to the Z.ai API:
```bash
PYTEST_ZAI_API_KEY="$(llm keys get zai)" uv run pytest --record-mode once
```
