# llm-mlx

[![PyPI](https://img.shields.io/pypi/v/llm-mlx.svg)](https://pypi.org/project/llm-mlx/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-mlx?include_prereleases&label=changelog)](https://github.com/simonw/llm-mlx/releases)
[![Tests](https://github.com/simonw/llm-mlx/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-mlx/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-mlx/blob/main/LICENSE)

Support for [MLX](https://github.com/ml-explore/mlx) models in [LLM](https://llm.datasette.io/).

Read my blog for [background on this project](https://simonwillison.net/2025/Feb/15/llm-mlx/).

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/). This plugin likely only works on macOS.
```bash
llm install llm-mlx
```
This plugin depends on [sentencepiece](https://pypi.org/project/sentencepiece/) which does not yet publish a binary wheel for Python 3.13. You will find this plugin easier to run on Python 3.12 or lower. One way to install a version of LLM that uses Python 3.12 is like this, using [uv](https://github.com/astral-sh/uv):

```bash
uv tool install llm --python 3.12
```
See [issue #7](https://github.com/simonw/llm-mlx/issues/7) for more on this.

## Usage

To install an MLX model from Hugging Face, use the `llm mlx download-model` command. This example downloads 1.8GB of model weights from [mlx-community/Llama-3.2-3B-Instruct-4bit](https://huggingface.co/mlx-community/Llama-3.2-3B-Instruct-4bit):

```bash
llm mlx download-model mlx-community/Llama-3.2-3B-Instruct-4bit
```
Then run prompts like this:
```bash
llm -m mlx-community/Llama-3.2-3B-Instruct-4bit 'Capital of France?' -s 'you are a pelican'
```
The [mlx-community](https://huggingface.co/mlx-community) organization is a useful source for compatible models.

### Models to try

The following models all work well with this plugin:

- `mlx-community/gemma-3-27b-it-qat-4bit` - [16GB](https://huggingface.co/mlx-community/gemma-3-27b-it-qat-4bit)
- `mlx-community/Qwen2.5-0.5B-Instruct-4bit` - [278MB](https://huggingface.co/mlx-community/Qwen2.5-0.5B-Instruct-4bit)
- `mlx-community/Mistral-7B-Instruct-v0.3-4bit` - [4.08GB](https://huggingface.co/mlx-community/Mistral-7B-Instruct-v0.3-4bit)
-  `mlx-community/Mistral-Small-24B-Instruct-2501-4bit` — [13.26 GB](https://huggingface.co/mlx-community/Mistral-Small-24B-Instruct-2501-4bit)
- `mlx-community/DeepSeek-R1-Distill-Qwen-32B-4bit` - [18.5GB](https://huggingface.co/mlx-community/DeepSeek-R1-Distill-Qwen-32B-4bit)
- `mlx-community/Llama-3.3-70B-Instruct-4bit` - [40GB](https://huggingface.co/mlx-community/Llama-3.3-70B-Instruct-4bit)

### Model options

MLX models can use the following model options:

- `-o max_tokens INTEGER`: Maximum number of tokens to generate in the completion (defaults to 1024)
- `-o unlimited 1`: Generate an unlimited number of tokens in the completion
- `-o temperature FLOAT`: Sampling temperature (defaults to 0.8)
- `-o top_p FLOAT`: Sampling top-p (defaults to 0.9)
- `-o min_p FLOAT`: Sampling min-p (defaults to 0.1)
- `-o min_tokens_to_keep INT`: Minimum tokens to keep for min-p sampling (defaults to 1)
- `-o seed INT`: Random number seed to use

For example:
```bash
llm -m mlx-community/Llama-3.2-3B-Instruct-4bit 'Joke about pelicans' -o max_tokens 60 -o temperature 1.0
```

## Managing existing models from your Hugging Face cache

If you have used MLX models in the past you may already have some installed in your `~/.cache/huggingface/hub` directory.

The `llm mlx manage-models` command can detect these and provide you with the option to add them to the list of models registered with LLM.

```bash
llm mlx manage-models
```
This will open an interface like this one:
```
Available model files (↑/↓ to navigate, SPACE to select, ENTER to confirm, Ctrl+C to quit):
  ○ Unregister mlx-community/gemma-3-27b-it-qat-4bit (gemma3)
  ○ Register mlx-community/DeepSeek-R1-Distill-Llama-8B (llama)
> ○ Register mlx-community/Llama-3.2-3B-Instruct-4bit (llama)
  ○ Unregister mlx-community/SmolLM-135M-Instruct-4bit (llama)
  ○ Register mlx-community/nanoLLaVA-1.5-8bit (llava-qwen2)
  ○ Register mlx-community/Mistral-Small-3.1-Text-24B-Instruct-2503-8bit (mistral)
  ○ Unregister mlx-community/OLMo-2-0325-32B-Instruct-4bit (olmo2)
  ○ Unregister mlx-community/OpenELM-270M-Instruct (openelm)
  ○ Unregister mlx-community/DeepCoder-14B-Preview-4bit (qwen2)
  ○ Unregister mlx-community/Qwen2.5-0.5B-Instruct-4bit (qwen2)
```
Navigate <up> and <down>, hit `<space>` to select actions you want to take and then hit `<enter>` to confirm. You can use this interface to both register new models and unregister existing models.

This tool only changes the list of available models recorded in your `~/Library/Application Support/io.datasette.llm/llm-mlx.json` file. It does not delete any model files from your Hugging Face cache.

## Using models from Python

If you have registered models with the `llm download-model` command you can use in Python like this:
```python
import llm
model = llm.get_model("mlx-community/Llama-3.2-3B-Instruct-4bit")
print(model.prompt("hi").text())
```
You can avoid that registration step entirely by accessing the models like this instead:
```python
from llm_mlx import MlxModel
model = MlxModel("mlx-community/Llama-3.2-3B-Instruct-4bit")
print(model.prompt("hi").text())
# Outputs: How can I assist you today?
```

The [LLM Python API documentation](https://llm.datasette.io/en/stable/python-api.html) has more details on how to use LLM models.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-mlx
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
