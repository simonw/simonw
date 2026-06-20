# llm-smolvlm

<!-- [![PyPI](https://img.shields.io/pypi/v/llm-smolvlm.svg)](https://pypi.org/project/llm-smolvlm/) -->
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-smolvlm?include_prereleases&label=changelog)](https://github.com/simonw/llm-smolvlm/releases)
[![Tests](https://github.com/simonw/llm-smolvlm/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-smolvlm/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-smolvlm/blob/main/LICENSE)

SmolVLM for LLM

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install https://github.com/simonw/llm-smolvlm/archive/refs/heads/main.zip
```
## Usage

> [!WARNING]  
> This model does not yet support conversations - you can use it to send single prompts but the `llm -c` and `llm chat` modes will not take previous messages into account.

Run prompts against images like this - only URLs to images are supported at the moment.

```bash
llm -m smolvlm 'describe this image' -a https://static.simonwillison.net/static/2024/pelicans.jpg
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-smolvlm
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
