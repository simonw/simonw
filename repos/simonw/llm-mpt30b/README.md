# llm-mpt30b

[![PyPI](https://img.shields.io/pypi/v/llm-mpt30b.svg)](https://pypi.org/project/llm-mpt30b/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-mpt30b?include_prereleases&label=changelog)](https://github.com/simonw/llm-mpt30b/releases)
[![Tests](https://github.com/simonw/llm-mpt30b/workflows/Test/badge.svg)](https://github.com/simonw/llm-mpt30b/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-mpt30b/blob/main/LICENSE)

Plugin for [LLM](https://llm.datasette.io/) adding support for the [MPT-30B language model](https://huggingface.co/mosaicml/mpt-30b).

This plugin uses [TheBloke/mpt-30B-GGML](https://huggingface.co/TheBloke/mpt-30B-GGML). The code was inspired by [abacaj/mpt-30B-inference](https://github.com/abacaj/mpt-30B-inference).

## Installation

Install this plugin in the same environment as LLM.
```bash
llm install llm-mpt30b
```
After installing the plugin you will need to download the ~19GB model file. You can do this by running:

```bash
llm mpt30b download
```

## Usage

This plugin adds a model called `mpt30b`. You can execute it like this:

```bash
llm -m mpt30b "Three great names for a pet goat"
```
The alias `-m mpt` works as well.

You can pass the option `-o verbose 1` to see more verbose output - currently a progress bar showing any additional downloads that are made during execution.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd llm-mpt30b
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
