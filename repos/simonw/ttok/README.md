# ttok

[![PyPI](https://img.shields.io/pypi/v/ttok.svg)](https://pypi.org/project/ttok/)
[![Changelog](https://img.shields.io/github/v/release/simonw/ttok?include_prereleases&label=changelog)](https://github.com/simonw/ttok/releases)
[![Tests](https://github.com/simonw/ttok/workflows/Test/badge.svg)](https://github.com/simonw/ttok/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/ttok/blob/master/LICENSE)

Count and truncate text based on tokens

## Background

Large language models such as GPT-3.5 and GPT-4 work in terms of tokens.

This tool can count tokens, using OpenAI's [tiktoken](https://github.com/openai/tiktoken) library.

It can also truncate text to a specified number of tokens.

See [llm, ttok and strip-tags—CLI tools for working with ChatGPT and other LLMs](https://simonwillison.net/2023/May/18/cli-tools-for-llms/) for more on this project.

## Installation

Install this tool using `pip`:
```bash
pip install ttok
```
Or using Homebrew:
```bash
brew install simonw/llm/ttok
```

## Counting tokens

Provide text as arguments to this tool to count tokens:

```bash
ttok Hello world
```
```
2
```
You can also pipe text into the tool:
```bash
echo -n "Hello world" | ttok
```
```
2
```
Here the `echo -n` option prevents echo from adding a newline - without that you would get a token count of 3.

To pipe in text and then append extra tokens from arguments, use the `-i -` option:

```bash
echo -n "Hello world" | ttok more text -i -
```
```
6
```
## Different models

By default, the tokenizer model for GPT-3.5 and GPT-4 is used.

To use the model for GPT-2 and GPT-3, add `--model gpt2`:

```bash
ttok boo Hello there this is -m gpt2
```
```
6
```
Compared to GPT-3.5:
```bash
ttok boo Hello there this is
```
```
5
```
Further model options are [documented here](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb).

## Truncating text

Use the `-t 10` or `--truncate 10` option to truncate text to a specified number of tokens:

```bash
ttok This is too many tokens -t 3
```
```
This is too
```

## Viewing tokens

The `--encode` option can be used to view the integer token IDs for the incoming text:

```bash
ttok Hello world --encode
```
```
9906 1917
```
The `--decode` method reverses this process:

```bash
ttok 9906 1917 --decode
```
```
Hello world
```
Add `--tokens` to either of these options to see a detailed breakdown of the tokens:

```bash
ttok Hello world --encode --tokens
```
```
[b'Hello', b' world']
```

## Available models

This is the full list of available models and their corresponding encodings. Model names and encoding names are valid for the `-m/--model` option.

<!-- [[[cog
import cog
import tiktoken
output = []
for key, value in tiktoken.model.MODEL_TO_ENCODING.items():
    output.append("- `{}` (`{}`)".format(key, value))
cog.out("\n".join(output))
]]] -->
- `gpt-4` (`cl100k_base`)
- `gpt-3.5-turbo` (`cl100k_base`)
- `gpt-3.5` (`cl100k_base`)
- `gpt-35-turbo` (`cl100k_base`)
- `davinci-002` (`cl100k_base`)
- `babbage-002` (`cl100k_base`)
- `text-embedding-ada-002` (`cl100k_base`)
- `text-embedding-3-small` (`cl100k_base`)
- `text-embedding-3-large` (`cl100k_base`)
- `text-davinci-003` (`p50k_base`)
- `text-davinci-002` (`p50k_base`)
- `text-davinci-001` (`r50k_base`)
- `text-curie-001` (`r50k_base`)
- `text-babbage-001` (`r50k_base`)
- `text-ada-001` (`r50k_base`)
- `davinci` (`r50k_base`)
- `curie` (`r50k_base`)
- `babbage` (`r50k_base`)
- `ada` (`r50k_base`)
- `code-davinci-002` (`p50k_base`)
- `code-davinci-001` (`p50k_base`)
- `code-cushman-002` (`p50k_base`)
- `code-cushman-001` (`p50k_base`)
- `davinci-codex` (`p50k_base`)
- `cushman-codex` (`p50k_base`)
- `text-davinci-edit-001` (`p50k_edit`)
- `code-davinci-edit-001` (`p50k_edit`)
- `text-similarity-davinci-001` (`r50k_base`)
- `text-similarity-curie-001` (`r50k_base`)
- `text-similarity-babbage-001` (`r50k_base`)
- `text-similarity-ada-001` (`r50k_base`)
- `text-search-davinci-doc-001` (`r50k_base`)
- `text-search-curie-doc-001` (`r50k_base`)
- `text-search-babbage-doc-001` (`r50k_base`)
- `text-search-ada-doc-001` (`r50k_base`)
- `code-search-babbage-code-001` (`r50k_base`)
- `code-search-ada-code-001` (`r50k_base`)
- `gpt2` (`gpt2`)
- `gpt-2` (`gpt2`)
<!-- [[[end]]] -->

## ttok --help

<!-- [[[cog
from ttok import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: ttok")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: ttok [OPTIONS] [PROMPT]...

  Count and truncate text based on tokens

  To count tokens for text passed as arguments:

      ttok one two three

  To count tokens from stdin:

      cat input.txt | ttok

  To truncate to 100 tokens:

      cat input.txt | ttok -t 100

  To truncate to 100 tokens using the gpt2 model:

      cat input.txt | ttok -t 100 -m gpt2

  To view token integers:

      cat input.txt | ttok --encode

  To convert tokens back to text:

      ttok 9906 1917 --decode

  To see the details of the tokens:

      ttok "hello world" --tokens

  Outputs:

      [b'hello', b' world']

Options:
  --version               Show the version and exit.
  -i, --input FILENAME
  -t, --truncate INTEGER  Truncate to this many tokens
  -m, --model TEXT        Which model to use
  --encode, --tokens      Output token integers
  --decode                Convert token integers to text
  --tokens                Output full tokens
  --allow-special         Do not error on special tokens
  --help                  Show this message and exit.

```
<!-- [[[end]]] -->

You can also run this command using:

```bash
python -m ttok --help
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

```bash
cd ttok
python -m venv venv
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
