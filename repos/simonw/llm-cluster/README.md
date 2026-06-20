# llm-cluster

[![PyPI](https://img.shields.io/pypi/v/llm-cluster.svg)](https://pypi.org/project/llm-cluster/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-cluster?include_prereleases&label=changelog)](https://github.com/simonw/llm-cluster/releases)
[![Tests](https://github.com/simonw/llm-cluster/workflows/Test/badge.svg)](https://github.com/simonw/llm-cluster/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-cluster/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for clustering embeddings

Background on this project: [Clustering with llm-cluster](https://simonwillison.net/2023/Sep/4/llm-embeddings/#llm-cluster).

## Installation

Install this plugin in the same environment as LLM.
```bash
llm install llm-cluster
```

## Usage

The plugin adds a new command, `llm cluster`. This command takes the name of an [embedding collection](https://llm.datasette.io/en/stable/embeddings/cli.html#storing-embeddings-in-sqlite) and the number of clusters to return.

First, use [paginate-json](https://github.com/simonw/paginate-json) and [jq](https://stedolan.github.io/jq/) to populate a collection. I this case we are embedding the title and body of every issue in the [llm repository](https://github.com/simonw/llm), and storing the result in a `issues.db` database:
```bash
paginate-json 'https://api.github.com/repos/simonw/llm/issues?state=all&filter=all' \
  | jq '[.[] | {id: .id, title: .title}]' \
  | llm embed-multi llm-issues - \
    --database issues.db --store
```
The `--store` flag causes the content to be stored in the database along with the embedding vectors.

Now we can cluster those embeddings into 10 groups:
```bash
llm cluster llm-issues 10 \
  -d issues.db
```
If you omit the `-d` option the default embeddings database will be used.

The output should look something like this (truncated):
```json
[
  {
    "id": "2",
    "items": [
      {
        "id": "1650662628",
        "content": "Initial design"
      },
      {
        "id": "1650682379",
        "content": "Log prompts and responses to SQLite"
      }
    ]
  },
  {
    "id": "4",
    "items": [
      {
        "id": "1650760699",
        "content": "llm web command - launches a web server"
      },
      {
        "id": "1759659476",
        "content": "`llm models` command"
      },
      {
        "id": "1784156919",
        "content": "`llm.get_model(alias)` helper"
      }
    ]
  },
  {
    "id": "7",
    "items": [
      {
        "id": "1650765575",
        "content": "--code mode for outputting code"
      },
      {
        "id": "1659086298",
        "content": "Accept PROMPT from --stdin"
      },
      {
        "id": "1714651657",
        "content": "Accept input from standard in"
      }
    ]
  }
]
```
The content displayed is truncated to 100 characters. Pass `--truncate 0` to disable truncation, or `--truncate X` to truncate to X characters.

## Generating summaries for each cluster

The `--summary` flag will cause the plugin to generate a summary for each cluster, by passing the content of the items (truncated according to the `--truncate` option) through a prompt to a Large Language Model.

This feature is still experimental. You should experiment with custom prompts to improve the quality of your summaries.

Since this can run a large amount of text through a LLM this can be expensive, depending on which model you are using.

This feature only works for embeddings that have had their associated content stored in the database using the `--store` flag.

You can use it like this:

```bash
llm cluster llm-issues 10 \
  -d issues.db \
  --summary
```
This uses the default prompt and the default model.

Partial example output:
```json
[
  {
    "id": "5",
    "items": [
      {
        "id": "1650682379",
        "content": "Log prompts and responses to SQLite"
      },
      {
        "id": "1650757081",
        "content": "Command for browsing captured logs"
      }
    ],
    "summary": "Log Management and Interactive Prompt Tracking"
  },
  {
    "id": "6",
    "items": [
      {
        "id": "1650771320",
        "content": "Mechanism for continuing an existing conversation"
      },
      {
        "id": "1740090291",
        "content": "-c option for continuing a chat (using new chat_id column)"
      },
      {
        "id": "1784122278",
        "content": "Figure out truncation strategy for continue conversation mode"
      }
    ],
    "summary": "Continuing Conversation Mechanism and Management"
  }
]
```

To use a different model, e.g. GPT-4, pass the `--model` option:
```bash
llm cluster llm-issues 10 \
  -d issues.db \
  --summary \
  --model gpt-4
```
The default prompt used is:

> Short, concise title for this cluster of related documents.

To use a custom prompt, pass `--prompt`:

```bash
llm cluster llm-issues 10 \
  -d issues.db \
  --summary \
  --model gpt-4 \
  --prompt 'Summarize this in a short line in the style of a bored, angry panda'
```
A `"summary"` key will be added to each cluster, containing the generated summary.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-cluster
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
