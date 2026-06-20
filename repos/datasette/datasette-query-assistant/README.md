# datasette-query-assistant

[![PyPI](https://img.shields.io/pypi/v/datasette-query-assistant.svg)](https://pypi.org/project/datasette-query-assistant/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-query-assistant?include_prereleases&label=changelog)](https://github.com/datasette/datasette-query-assistant/releases)
[![Tests](https://github.com/datasette/datasette-query-assistant/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-query-assistant/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-query-assistant/blob/main/LICENSE)

Query databases and tables with AI assistance

**Early alpha**.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-query-assistant
```

## Configuration

Set the model ID to be used by this plugin by adding this to your Datasette configuration:

```yaml
plugins:
  datasette-query-assistant:
    model: openai/gpt-4.1-mini
    key_env_var: OPENAI_API_KEY
```
To use the `openai/gpt-4.1-mini` model you'll need to install `llm-openai-plugin` in addition to `datasette-query-assistant`.

If the model needs an API key, set the `key_env_var` to the name of an environment variable and ensure that environment variable is correctly set.

You can use any model that is available via an [LLM plugin](https://llm.datasette.io/en/stable/plugins/directory.html)

## Usage

Users with `execute-sql` permission will gain a database action menu item for "Query this database with AI assistance" which will let them ask a question and be redirected to a commented SQL query that will hopefully answer it.

## Development

To set up this plugin locally, checkout the code and run the tests with `uv` like this:
```bash
cd datasette-query-assistant
uv run pytest
```
To re-generate the tests with refreshed examples from the API:
```bash
uv run pytest -x --record-mode=rewrite --inline-snapshot=fix
```
