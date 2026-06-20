# llm-mlc

[![PyPI](https://img.shields.io/pypi/v/llm-mlc.svg)](https://pypi.org/project/llm-mlc/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-mlc?include_prereleases&label=changelog)](https://github.com/simonw/llm-mlc/releases)
[![Tests](https://github.com/simonw/llm-mlc/workflows/Test/badge.svg)](https://github.com/simonw/llm-mlc/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-mlc/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for running models using [MLC](https://mlc.ai/mlc-llm/docs/)

## Installation

Install this plugin in the same environment as `llm`.
```bash
llm install llm-mlc
```
You need to install two dependencies manually - `mlc-chat-nightly` and `mlc-ai-nightly` - because the installation process differs from one platform to another in a way that is not yet automated.

The steps for this are [described in detail on the mlc.ai/package](https://mlc.ai/package/) site.

If you are on an Apple Silicon M1/M2 Mac you can run this command:
```bash
llm mlc pip install --pre --force-reinstall \
  mlc-ai-nightly \
  mlc-chat-nightly \
  -f https://mlc.ai/wheels
```
The `llm mlc pip` command here ensures that `pip` will run in the same virtual environment as `llm` itself.

For other systems, [follow the instructions here](https://mlc.ai/package/).

Finally, run the `llm mlc setup` command to complete the installation:
```bash
llm mlc setup
```
This will setup `git lfs` and use it to download some extra dependencies:
```
Git LFS is not installed. Should I run 'git lfs install' for you?
Install Git LFS? [y/N]: y
Updated Git hooks.
Git LFS initialized.
Downloading prebuilt binaries...
Cloning into '/Users/simon/Library/Application Support/io.datasette.llm/mlc/dist/prebuilt/lib'...
remote: Enumerating objects: 221, done.
remote: Counting objects: 100% (86/86), done.
remote: Compressing objects: 100% (54/54), done.
remote: Total 221 (delta 59), reused 56 (delta 32), pack-reused 135
Receiving objects: 100% (221/221), 52.06 MiB | 9.13 MiB/s, done.
Resolving deltas: 100% (152/152), done.
Updating files: 100% (60/60), done.
Ready to install models in /Users/simon/Library/Application Support/io.datasette.llm/mlc
```

## Installing models

After installation you will need to download a model using the `llm mlc download-model` command.

Here's how to download and install Llama 2:

```bash
llm mlc download-model Llama-2-7b-chat --alias llama2
```
This will download around 8GB of content.

You can also use `Llama-2-13b-chat` (about 15.15GB) or `Llama-2-70b-chat` (extremely big), though these files are a lot larger.

The `-a/--alias` is optional, but can be used to set a shorter alias for the model. This can then be used with `llm -m <alias>` instead of the full name.

The `download-model` command also takes a URL to one of [the MLC repositories on Hugging Face](https://huggingface.co/mlc-ai).

For example, to install [mlc-chat-WizardLM-13B-V1](https://huggingface.co/mlc-ai/mlc-chat-WizardLM-13B-V1.2-q4f16_1):
```bash
llm mlc download-model https://huggingface.co/mlc-ai/mlc-chat-WizardLM-13B-V1.2-q4f16_1
```
You can see a full list of models you have installed this way using:
```bash
llm mlc models
```
This will also show the name of the model you should use to activate it, e.g.:
```
MlcModel: mlc-chat-Llama-2-7b-chat-hf-q4f16_1 (aliases: llama2, Llama-2-7b-chat)
```
## Running a prompt through a model

Once you have downloaded and added a model, you can run a prompt like this:
```bash
llm -m Llama-2-7b-chat 'five names for a cute pet ferret'
```

> Great! Here are five cute and creative name suggestions for a pet ferret:
>
> 1. Ferbie - a playful and affectionate name for a friendly and outgoing ferret.
> 2. Mr. Whiskers - a suave and sophisticated name for a well-groomed and dignified ferret.
> 3. Luna - a celestial and dreamy name for a curious and adventurous ferret.
> 4. Felix - a cheerful and energetic name for a lively and mischievous ferret.
> 5. Sprinkles - a fun and playful name for a happy and energetic ferret with a sprinkle of mischief.
>
> Remember, the most important thing is to choose a name that you and your ferret will love and enjoy!

And to send a follow-up prompt to continue the current conversation, use `-c`:

```bash
llm -c 'two more'
```

> Of course! Here are two more cute name ideas for a pet ferret:
>
> 1. Digger - a fun and playful name that suits a pet that loves to dig and burrow, and is also a nod to the ferret's natural instincts as a burrower.
> 2. Gizmo - a fun and quirky name that suits a pet with a curious and mischievous personality, and is also a nod to the ferret's playful and inventive nature.

## Model options

These options are available for all models. They mostly take a floating point value between 0.0 and 1.0.

- `-o temperature`: A higher temperature encourages more diverse outputs, while a lower temperature produces more deterministic outputs.
- `-o top_p`: At each step, we select tokens from the minimal set that has a cumulative probability exceeding this value.
- `-o repetition_penalty`: Controls the likelihood of the model generating repeated texts.
- `-o max_gen_len`: Takes an integer, which controls the maximum length of the generated text.

Use them like this:

```bash
llm -m Llama-2-7b-chat \
  -o temperature 0.5 \
  -o top_p 0.9 \
  -o repetition_penalty 0.9 \
  -o max_gen_len 100 \
  'five names for a cute pet ferret'
```
The [MLC documentation](https://mlc.ai/mlc-llm/docs/get_started/mlc_chat_config.html) has more details on these options.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-mlc
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
