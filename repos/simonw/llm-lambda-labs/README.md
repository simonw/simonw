# llm-lambda-labs

[![PyPI](https://img.shields.io/pypi/v/llm-lambda-labs.svg)](https://pypi.org/project/llm-lambda-labs/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-lambda-labs?include_prereleases&label=changelog)](https://github.com/simonw/llm-lambda-labs/releases)
[![Tests](https://github.com/simonw/llm-lambda-labs/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-lambda-labs/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-lambda-labs/blob/main/LICENSE)

Run prompts against LLMs hosted by https://lambdalabs.com/

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-lambda-labs
```
## Usage

First, [obtain an API key](https://cloud.lambdalabs.com/api-keys) for Lambda Labs and set it like this:

```bash
llm keys set lambdalabs
# Paste key here
```

To see a list of available models, run this:

```bash
llm models
```
Run prompts like this:
```bash
llm -m lambdalabs/hermes3-405b 'short poem about a pelican with a twist'
```

The list of available models is fetched the first time the plugin is run. You can refresh that cached list by running:

```bash
llm lambdalabs refresh
```
To see a list of model information that has been stored in the cache, run this:

```bash
llm lambdalabs models
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-lambda-labs
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```

Run this to capture new recordings of HTTP interactions for the tests:
```bash
PYTEST_LAMBDALABS_KEY="$(llm keys get lambdalabs)" pytest --record-mode once
```