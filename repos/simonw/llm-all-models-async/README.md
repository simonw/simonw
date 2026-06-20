# llm-all-models-async

[![PyPI](https://img.shields.io/pypi/v/llm-all-models-async.svg)](https://pypi.org/project/llm-all-models-async/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-all-models-async?include_prereleases&label=changelog)](https://github.com/simonw/llm-all-models-async/releases)
[![Tests](https://github.com/simonw/llm-all-models-async/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-all-models-async/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-all-models-async/blob/main/LICENSE)

Make all LLM sync models available as async

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-all-models-async
```
## Usage

Once installed, any other model plugins that do not define both sync and async models (for example [llm-mrchatterbox](https://github.com/simonw/llm-mrchatterbox)) will gain an async version. Under the hood this uses a thread pool.

## Development

To set up this plugin locally, first checkout the code. Then run the tests:
```bash
cd llm-all-models-async
uv run pytest
```
