# llm-command-r

[![PyPI](https://img.shields.io/pypi/v/llm-command-r.svg)](https://pypi.org/project/llm-command-r/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-command-r?include_prereleases&label=changelog)](https://github.com/simonw/llm-command-r/releases)
[![Tests](https://github.com/simonw/llm-command-r/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-command-r/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-command-r/blob/main/LICENSE)

Access the [Cohere Command R](https://docs.cohere.com/docs/command-r) family of models via the Cohere API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-command-r
```

## Configuration

You will need a [Cohere API key](https://dashboard.cohere.com/api-keys). Configure it like this:

```bash
llm keys set cohere
# Paste key here
```
To use an alternative base URL for the Cohere API, set the `COHERE_BASE_URL` environment variable.

## Usage

This plugin adds two models.

```bash
llm -m command-r 'Say hello from Command R'
llm -m command-r-plus 'Say hello from Command R Plus'
```

The Command R models have the ability to search the web as part of answering a prompt.

You can enable this feature using the `-o websearch 1` option to the models:

```bash
llm -m command-r 'What is the LLM CLI tool?' -o websearch 1
```
Running a search costs more as it involves spending tokens including the search results in the prompt.

The full search results are stored as JSON [in the LLM logs](https://llm.datasette.io/en/stable/logging.html).

You can also use the `command-r-search` command provided by this plugin to see a list of documents that were used to answer your question as part of the output:

```bash
llm command-r-search 'What is the LLM CLI tool by simonw?'
```
Example output:

> The LLM CLI tool is a command-line utility that allows users to access large language models. It was created by Simon Willison and can be installed via pip, Homebrew or pipx. The tool supports interactions with remote APIs and models that can be locally installed and run. Users can run prompts from the command line and even build an image search engine using the CLI tool.
>
> Sources:
>
> - GitHub - simonw/llm: Access large language models from the command-line - https://github.com/simonw/llm
> - llm, ttok and strip-tags—CLI tools for working with ChatGPT and other LLMs - https://simonwillison.net/2023/May/18/cli-tools-for-llms/
> - Sherwood Callaway on LinkedIn: GitHub - simonw/llm: Access large language models from the command-line - https://www.linkedin.com/posts/sherwoodcallaway_github-simonwllm-access-large-language-activity-7104448041041960960-2WRG
> - LLM Python/CLI tool adds support for embeddings | Hacker News - https://news.ycombinator.com/item?id=37384797
> - CLI tools for working with ChatGPT and other LLMs | Hacker News - https://news.ycombinator.com/item?id=35994037
> - GitHub - simonw/homebrew-llm: Homebrew formulas for installing LLM and related tools - https://github.com/simonw/homebrew-llm
> - LLM: A CLI utility and Python library for interacting with Large Language Models - https://llm.datasette.io/en/stable/
> - GitHub - simonw/llm-prompts: A collection of prompts for use with the LLM CLI tool - https://github.com/simonw/llm-prompts
> - GitHub - simonw/llm-cmd: Use LLM to generate and execute commands in your shell - https://github.com/simonw/llm-cmd

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-command-r
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest
```
To generate new recorded VCR cassettes:
```bash
PYTEST_COHERE_API_KEY="$(llm keys get cohere)" pytest --record-mode once
```