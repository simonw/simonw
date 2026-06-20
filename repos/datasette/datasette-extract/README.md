# datasette-extract

[![PyPI](https://img.shields.io/pypi/v/datasette-extract.svg)](https://pypi.org/project/datasette-extract/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-extract?include_prereleases&label=changelog)](https://github.com/datasette/datasette-extract/releases)
[![Tests](https://github.com/datasette/datasette-extract/workflows/Test/badge.svg)](https://github.com/datasette/datasette-extract/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-extract/blob/main/LICENSE)

Import unstructured data (text and images) into structured tables

## Installation

Install this plugin in the same environment as [Datasette](https://datasette.io/).
```bash
datasette install datasette-extract
```

This plugin depends on [datasette-llm](https://github.com/datasette/datasette-llm) for LLM model management, API key handling, and model provider integration. See the [datasette-llm README](https://github.com/datasette/datasette-llm/blob/main/README.md) for instructions on installing model providers and configuring API keys.

## Configuration

datasette-extract registers an `extract` purpose with datasette-llm. You can optionally configure which models are available and set a default model for extraction using datasette-llm's purpose-specific configuration:

```yaml
plugins:
  datasette-llm:
    purposes:
      extract:
        model: gpt-5.4-mini
        models:
        - gpt-5.4-nano
        - gpt-5.4
        - claude-opus-4.6
```

The model selector in the UI is only shown if more than one model is available.

## Usage

This plugin provides the following features:

- In the database action cog menu for a database select "Create table with extracted data" to create a new table with data extracted from text or an image
- In the table action cog menu select "Extract data into this table" to extract data into an existing table

When creating a table you can specify the column names, types and provide an optional hint (like "YYYY-MM-DD" for dates) to influence how the data should be extracted.

When populating an existing table you can provide hints and select which columns should be populated.

Text input can be pasted directly into the textarea.

Drag and drop a PDF or text file onto the textarea to populate it with the contents of that file. PDF files will have their text extracted, but only if the file contains text as opposed to scanned images.

Drag and drop a single image onto the textarea - or select it with the image file input box - to process an image.

## Permissions

Users must have the `datasette-extract` permission to use this tool.

In order to create tables they also need the `create-table` permission.

To insert rows into an existing table they need `insert-row`.

## Development

The recommended way to develop this plugin uses [uv](https://github.com/astral-sh/uv). To run the tests:
```bash
cd datasette-extract
uv run pytest
```
To run a development server with an OpenAI API key:
```bash
DATASETTE_SECRETS_OPENAI_API_KEY="sk-..." \
  uv run datasette data.db --create --root --secret 1 \
  -s plugins.datasette-llm.purposes.extract.models '["gpt-5.4-mini"]' \
  --internal internal.db --reload
```
