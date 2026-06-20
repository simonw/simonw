# llm-llama-cpp

[![PyPI](https://img.shields.io/pypi/v/llm-llama-cpp.svg)](https://pypi.org/project/llm-llama-cpp/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-llama-cpp?include_prereleases&label=changelog)](https://github.com/simonw/llm-llama-cpp/releases)
[![Tests](https://github.com/simonw/llm-llama-cpp/workflows/Test/badge.svg)](https://github.com/simonw/llm-llama-cpp/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-llama-cpp/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for running models using [llama.cpp](https://github.com/ggerganov/llama.cpp)

## Installation

Install this plugin in the same environment as `llm`.
```bash
llm install llm-llama-cpp
```
The plugin has an additional dependency on [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) which needs to be installed separately.

If you have a C compiler available on your system you can install that like so:
```bash
llm install llama-cpp-python
```
You could also try installing one of the wheels made available in their [latest release](https://github.com/abetlen/llama-cpp-python/releases/latest) on GitHub. Find the URL to the wheel for your platform, if one exists, and run:
```bash
llm install https://...
```
If you are on an Apple Silicon Mac you can try this command, which should compile the package with METAL support for running on your GPU:

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 llm install llama-cpp-python
```
## Running a GGUF model directly

The quickest way to try this plugin out is to download a GGUF file and execute that using the `gguf` model with the `-o path PATH` option:

For example, download the `una-cybertron-7b-v2-bf16.Q8_0.gguf` file from [TheBloke/una-cybertron-7B-v2-GGUF](https://huggingface.co/TheBloke/una-cybertron-7B-v2-GGUF/tree/main) and execute it like this:

```bash
llm -m gguf \
  -o path una-cybertron-7b-v2-bf16.Q8_0.gguf \
  'Instruction: Five reasons to get a pet walrus
Response:'
```
The output starts like this:

>  1. Walruses are fascinating animals that possess unique qualities that can captivate and entertain you for hours on end. Getting the chance to be around one regularly would ensure that you'll never run out of interesting things to learn about them, whether from an educational or personal standpoint.
>
> 2. Pet walruses can help alleviate depression and anxiety, as they require constant care and attention. Nurturing a relationship with these intelligent creatures provides comfort and fulfillment, fostering a sense of purpose in your daily life. Moreover, their playful nature encourages laughter and joy, promoting overall happiness. [...]

## Adding models

You can also add or download models to execute them directly using the `-m` option.

This tool should work with any model that works with `llama.cpp`.

The plugin can download models for you. Try running this command:

```bash
llm llama-cpp download-model \
  https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q6_K.gguf \
  --alias llama2-chat --alias l2c --llama2-chat
```
This will download the Llama 2 7B Chat GGUF model file (this one is 5.53GB), save it and register it with the plugin - with two aliases, `llama2-chat` and `l2c`.

The `--llama2-chat` option configures it to run using a special Llama 2 Chat prompt format. You should omit this for models that are not Llama 2 Chat models.

If you have already downloaded a `llama.cpp` compatible model you can tell the plugin to read it from its current location like this:

```bash
llm llama-cpp add-model path/to/llama-2-7b-chat.Q6_K.gguf \
  --alias l27c --llama2-chat
```
The model filename (minus the `.gguf` extension) will be registered as its ID for executing the model.

You can also set one or more aliases using the `--alias` option.

You can see a list of models you have registered in this way like this:
```bash
llm llama-cpp models
```
Models are registered in a `models.json` file. You can find the path to that file in order to edit it directly like so:
```bash
llm llama-cpp models-file
```
For example, to edit that file in Vim:
```bash
vim "$(llm llama-cpp models-file)"
```
To find the directory with downloaded models, run:
```bash
llm llama-cpp models-dir
```
Here's how to change to that directory:
```bash
cd "$(llm llama-cpp models-dir)"
```

## Running a prompt through a model

Once you have downloaded and added a model, you can run a prompt like this:
```bash
llm -m llama-2-7b-chat.Q6_K 'five names for a cute pet skunk'
```
Or if you registered an alias you can use that instead:
```bash
llm -m llama2-chat 'five creative names for a pet hedgehog'
```

## More models to try

### Llama 2 7B

This model is Llama 2 7B GGML without the chat training. You'll need to prompt it slightly differently:
```bash
llm llama-cpp download-model \
  https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q6_K.gguf \
  --alias llama2
```
Try prompts that expect to be completed by the model, for example:
```bash
llm -m llama2 'Three fancy names for a posh albatross are:'
```
### Llama 2 Chat 13B

This model is the Llama 2 13B Chat GGML model - a 10.7GB download:
```bash
llm llama-cpp download-model \
  'https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q6_K.gguf'\
  -a llama2-chat-13b --llama2-chat
```

### Llama 2 Python 13B

This model is the Llama 2 13B Python GGML model - a 9.24GB download:
```bash
llm llama-cpp download-model \
  'https://huggingface.co/TheBloke/CodeLlama-13B-Python-GGUF/resolve/main/codellama-13b-python.Q5_K_M.gguf'\
  -a llama2-python-13b --llama2-chat
```

## Options

The following options are available:

- `-o verbose 1` - output more verbose logging
- `-o max_tokens 100` - max tokens to return. Defaults to 4000.
- `-o no_gpu 1` - remove the default `n_gpu_layers=1`` argument, which should disable GPU usage
- `-o n_gpu_layers 10` - increase the `n_gpu_layers` argument to a higher value (the default is `1`)
- `-o n_ctx 1024` - set the `n_ctx` argument to `1024` (the default is `4000`)

For example:

```bash
llm chat -m llama2-chat-13b -o n_ctx 1024
```

These are mainly provided to support experimenting with different ways of executing the underlying model.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-llama-cpp
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
