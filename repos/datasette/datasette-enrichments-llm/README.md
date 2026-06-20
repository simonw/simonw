# datasette-enrichments-llm

[![PyPI](https://img.shields.io/pypi/v/datasette-enrichments-llm.svg)](https://pypi.org/project/datasette-enrichments-llm/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-enrichments-llm?include_prereleases&label=changelog)](https://github.com/datasette/datasette-enrichments-llm/releases)
[![Tests](https://github.com/datasette/datasette-enrichments-llm/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-enrichments-llm/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-enrichments-llm/blob/main/LICENSE)

Enrich data by prompting LLMs

This is an **early alpha**.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-enrichments-llm
```
This plugin depends on [datasette-llm](https://github.com/datasette/datasette-llm) for LLM model management, API key handling, and model provider integration. See the [datasette-llm README](https://github.com/datasette/datasette-llm/blob/main/README.md) for instructions on installing model providers and configuring API keys.

## Configuration

datasette-enrichments-llm registers an `enrichments` purpose with datasette-llm. You can optionally configure which models are available and set a default model for enrichments using datasette-llm's purpose-specific configuration:

```yaml
plugins:
  datasette-llm:
    purposes:
      enrichments:
        model: gpt-5.4-mini
        models:
        - gpt-5.4-nano
        - claude-opus-4.6
```

## Usage

Enrichments can be run against any [LLM](https://llm.datasette.io/) model that has an LLM plugin providing [asynchronous support](https://llm.datasette.io/en/stable/plugins/advanced-model-plugins.html#async-models) for that model.

Multi-modal models are supported via the `media_url` parameter.

## Development

To set up this plugin locally, first checkout the code. Run the tests like this:
```bash
cd datasette-enrichments-llm
uv run pytest
```
To try the plugin:
```bash
echo 'id,name\n1,Bob\n2,Kate' | uvx sqlite-utils insert data.db people - --csv
```
Then:
```bash
uv run datasette --root --secret 1 data.db
```
