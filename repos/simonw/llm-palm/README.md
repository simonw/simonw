# llm-palm

[![PyPI](https://img.shields.io/pypi/v/llm-palm.svg)](https://pypi.org/project/llm-palm/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-palm?include_prereleases&label=changelog)](https://github.com/simonw/llm-palm/releases)
[![Tests](https://github.com/simonw/llm-palm/workflows/Test/badge.svg)](https://github.com/simonw/llm-palm/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-palm/blob/main/LICENSE)

Plugin for [LLM](https://llm.datasette.io/) adding support for Google's PaLM 2 model.

## Installation

Install this plugin in the same environment as LLM.
```bash
llm install llm-palm
```
## Configuration

You will need an API key from Google. Instructions for obtaining one: https://developers.generativeai.google/tutorials/setup

You can set that as an environment variable called `PALM_API_KEY`, or add it to the `llm` set of saved keys using:

```bash
llm keys set palm
```
```
Enter key: <paste key here>
```

## Usage

This plugin adds a model called `palm`. You can execute it like this:

```bash
llm -m palm "Ten great names for a pet pelican"
```
PaLM also supports system prompts:
```bash
echo "I like pelicans a lot" | llm -m palm --system "Translate to french"
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd llm-palm
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
