# llm-mlx-llama

[![PyPI](https://img.shields.io/pypi/v/llm-mlx-llama.svg)](https://pypi.org/project/llm-mlx-llama/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-mlx-llama?include_prereleases&label=changelog)](https://github.com/simonw/llm-mlx-llama/releases)
[![Tests](https://github.com/simonw/llm-mlx-llama/workflows/Test/badge.svg)](https://github.com/simonw/llm-mlx-llama/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-mlx-llama/blob/main/LICENSE)

Using MLX on macOS to run Llama 2. **Highly experimental**.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install https://github.com/simonw/llm-mlx-llama/archive/refs/heads/main.zip
```
## Usage

Download `Llama-2-7b-chat.npz` and `tokenizer.model` from [mlx-llama/Llama-2-7b-chat-mlx](https://huggingface.co/mlx-llama/Llama-2-7b-chat-mlx/tree/main).

Pass paths to those files as options when you run a prompt:

```bash
llm -m mlx-llama \
  'five great reasons to get a pet pelican:' \
  -o model Llama-2-7b-chat.npz \
  -o tokenizer tokenizer.model
```
Chat mode and continuing a conversation are not yet supported.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-mlx-llama
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
