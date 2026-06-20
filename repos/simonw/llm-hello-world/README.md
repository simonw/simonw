# llm-hello-world

[![PyPI](https://img.shields.io/pypi/v/llm-hello-world.svg)](https://pypi.org/project/llm-hello-world/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-hello-world?include_prereleases&label=changelog)](https://github.com/simonw/llm-hello-world/releases)
[![Tests](https://github.com/simonw/llm-hello-world/workflows/Test/badge.svg)](https://github.com/simonw/llm-hello-world/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-hello-world/blob/main/LICENSE)

Hello world plugin for LLM

## Installation

Install this plugin in the same environment as LLM.

    llm install llm-hello-world

## Usage

This plugin adds a hello-world command:

    llm hello-world

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd llm-hello-world
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
