# datasette-enrichments-gpt

[![PyPI](https://img.shields.io/pypi/v/datasette-enrichments-gpt.svg)](https://pypi.org/project/datasette-enrichments-gpt/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-enrichments-gpt?include_prereleases&label=changelog)](https://github.com/datasette/datasette-enrichments-gpt/releases)
[![Tests](https://github.com/datasette/datasette-enrichments-gpt/workflows/Test/badge.svg)](https://github.com/datasette/datasette-enrichments-gpt/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-enrichments-gpt/blob/main/LICENSE)

Datasette enrichment for analyzing row data using OpenAI's GPT models

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-enrichments-gpt
```
## Configuration

This plugin can optionally be configured with an [OpenAI API key](https://platform.openai.com/api-keys). You can set this as an environment variable:
```bash
export DATASETTE_SECRETS_OPENAPI_API_KEY=sk-..
```
Or you can configure it using the [datasette-secrets](https://datasette.io/plugins/datasette-secrets) plugin.

If you do not configure an OpenAI API key users will be asked to enter one any time they execute the enrichment. The key they provide will not be stored anywhere other than in-memory during the enrichment run.

## Usage

Once installed, this plugin will allow users to select rows to enrich and run them through prompts using `gpt-3.5-turbo` or `gpt-4o`, saving the result of the prompt in the specified column.

The plugin also provides `gpt-4o vision`, which can run prompts against an image identified by a URL.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-enrichments-gpt
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
