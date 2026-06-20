# datasette-agent-openai-imagegen

[![PyPI](https://img.shields.io/pypi/v/datasette-agent-openai-imagegen.svg)](https://pypi.org/project/datasette-agent-openai-imagegen/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-agent-openai-imagegen?include_prereleases&label=changelog)](https://github.com/datasette/datasette-agent-openai-imagegen/releases)
[![Tests](https://github.com/datasette/datasette-agent-openai-imagegen/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-agent-openai-imagegen/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-agent-openai-imagegen/blob/main/LICENSE)

Generate images in [Datasette agent](https://github.com/datasette/datasette-agent).

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-agent-openai-imagegen
```
## Usage

Once installed Datasette Agent will have a new tool for generating images, provided an OpenAI API key has been configured for `datasette-llm`.

The tool will default to using the faster, cheaper [gpt-image-1-mini](https://developers.openai.com/api/docs/models/gpt-image-1-mini) but can be told to use the higher quality and more expensive [gpt-image-2](https://developers.openai.com/api/docs/models/gpt-image-2) instead.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-agent-openai-imagegen
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
