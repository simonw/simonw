# datasette-llm-usage

[![PyPI](https://img.shields.io/pypi/v/datasette-llm-usage.svg)](https://pypi.org/project/datasette-llm-usage/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-llm-usage?include_prereleases&label=changelog)](https://github.com/datasette/datasette-llm-usage/releases)
[![Tests](https://github.com/datasette/datasette-llm-usage/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-llm-usage/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-llm-usage/blob/main/LICENSE)

Track usage of LLM tokens in a SQLite table

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-llm-usage
```
## Usage

This plugin tracks LLM token usage in Datasette via the [datasette-llm](https://github.com/datasette/datasette-llm) `llm_prompt_context` hook. It creates two tables:

- `llm_usage`: Tracks token usage per request (model, purpose, actor, input/output tokens)
- `llm_usage_prompt_log`: Optionally logs full prompts and responses

### Configuration

By default the tables are created in the internal database passed to Datasette using `--internal internal.db`. You can change that by setting the following in your Datasette plugin configuration:

```json
{
    "plugins": {
        "datasette-llm-usage": {
            "database": "your_database_name"
        }
    }
}
```

To enable full prompt and response logging, set `log_prompts` to `true`:

```json
{
    "plugins": {
        "datasette-llm-usage": {
            "log_prompts": true
        }
    }
}
```

### Prompt testing tool

The plugin also provides a simple demo page at `/-/llm-usage-simple-prompt` which can be used to execute prompts for testing.

That page requires the user to have the `llm-usage-simple-prompt` permission.

## Development

Clone this repo and run the tests:

```bash
cd datasette-llm-usage
uv run pytest
```
