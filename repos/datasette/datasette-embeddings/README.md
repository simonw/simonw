# datasette-embeddings

[![PyPI](https://img.shields.io/pypi/v/datasette-embeddings.svg)](https://pypi.org/project/datasette-embeddings/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-embeddings?include_prereleases&label=changelog)](https://github.com/datasette/datasette-embeddings/releases)
[![Tests](https://github.com/datasette/datasette-embeddings/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-embeddings/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-embeddings/blob/main/LICENSE)

Store and query embedding vectors in Datasette tables

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-embeddings
```
## Usage

Adds an [enrichment](https://enrichments.datasette.io/) for calculating and storing OpenAI embedding vectors for content in a table.

Users get to select the embedding model and the template (e.g. `{{ title }} {{ body }}`) for the columns they would like to embed.

Embeddings are stored as binary values in columns in a new table called `_embeddings_NAME`, where `NAME` is the name of the original source table.

The vectors are stored in columns that match the name of the embedding model, for example `emb_text_embedding_3_large_256` for the `text-embedding-3-large-256` model.

If you do not configure an OpenAI API key users will be asked for one any time they run the enrichment.

You can set an API key with plugin configuration like this:

```yaml
plugins:
  datasette-embeddings:
    api_key:
      $env: OPENAI_API_KEY
```
Then set the `OPENAI_API_KEY` environment variable before you start Datasette.

This plugin adds a "Semantic search against this table" table action item for tables with embeddings, but only if the API key environment variable has been configured as the key is needed to calculate embeddings for the user's search query.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-embeddings
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
The tests use captured examples of embedding APIs. The easiest way to re-generate these is to do the following:

- `rm -rf tests/cassettes` to remove the previous recordings
- `export OPENAPI_API_KEY='...'` to set an OpenAI API key
- `pytest --record-mode once` to recreate the cassettes

