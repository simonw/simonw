# llm-markov

[![PyPI](https://img.shields.io/pypi/v/llm-markov.svg)](https://pypi.org/project/llm-markov/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-markov?include_prereleases&label=changelog)](https://github.com/simonw/llm-markov/releases)
[![Tests](https://github.com/simonw/llm-markov/workflows/Test/badge.svg)](https://github.com/simonw/llm-markov/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-markov/blob/main/LICENSE)

Plugin for [LLM](https://llm.datasette.io/) adding a [Markov chain](https://en.wikipedia.org/wiki/Markov_chain) generating model

## Installation

Install this plugin in the same environment as LLM.
```bash
llm install llm-markov
```
## Usage

This plugin adds a model called `markov`. You can execute it like this:

```bash
llm -m markov "The quick brown fox jumps over the lazy dog"
```

My default it will produce 100 words. You can control the number of words with the `-o number` option:

```bash
llm -m markov -o 20 "The quick brown fox jumps over the lazy dog"
```
A delay of 0.02s is simulated between each token. You can modify this using the `-o delay` option - to `0` to disable it, or some other floating point number of seconds to customize it:

```bash
llm -m markov "The quick brown fox jumps over the lazy dog" -o delay 0
llm -m markov "The quick brown fox jumps over the lazy dog" -o delay 0.1 -o length 20
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd llm-markov
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
