# llm-mrchatterbox

[![PyPI](https://img.shields.io/pypi/v/llm-mrchatterbox.svg)](https://pypi.org/project/llm-mrchatterbox/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-mrchatterbox?include_prereleases&label=changelog)](https://github.com/simonw/llm-mrchatterbox/releases)
[![Tests](https://github.com/simonw/llm-mrchatterbox/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-mrchatterbox/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/simonw/llm-mrchatterbox/blob/main/LICENSE)

[Mr. Chatterbox](https://huggingface.co/tventurella/mr_chatterbox_model) is a language model trained from scratch by Trip Venturella using [nanochat](https://github.com/karpathy/nanochat) on a corpus of over 28,000 Victorian-era British texts published between 1837 and 1899, [made available](https://huggingface.co/datasets/TheBritishLibrary/blbooks) by the British Library.

This [LLM](https://llm.datasette.io/) plugin vendors enough of nanochat to get the model to work, also borrowing some details from Trip's [mr_chatterbox HuggingFace Space
](https://huggingface.co/spaces/tventurella/mr_chatterbox/tree/main). You can also [chat with the model](https://huggingface.co/spaces/tventurella/mr_chatterbox) using that Space in your browser.

See [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2026/Mar/30/mr-chatterbox/) for background on this project.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-mrchatterbox
```
## Usage

The first time you run a prompt the ~2GB model will be downloaded to your machine.

```bash
llm -m mrchatterbox 'hello good sir'
```
Chat with the model using the `chat` command:
```bash
llm chat -m mrchatterbox
```
The cached model is stored in the path revealed by this command:
```bash
llm mrchatterbox path
```
On a Mac that folder is:
```
~/Library/Application Support/io.datasette.llm/mrchatterbox
```
You can delete the model file using this command:
```bash
llm mrchatterbox delete-model
```

## Development

To set up this plugin locally, first checkout the code. Run the tests like this:
```bash
cd llm-mrchatterbox
uv run pytest
```
To run prompts through the model use:
```bash
uv run llm -m mrchatterbox 'hello good sir'
```
