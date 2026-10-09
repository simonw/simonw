# ttok

[![PyPI](https://img.shields.io/pypi/v/ttok.svg)](https://pypi.org/project/ttok/)
[![Changelog](https://img.shields.io/github/v/release/simonw/ttok?include_prereleases&label=changelog)](https://github.com/simonw/ttok/releases)
[![Tests](https://github.com/simonw/ttok/workflows/Test/badge.svg)](https://github.com/simonw/ttok/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/ttok/blob/master/LICENSE)

Count and truncate text based on tokens

## Background

Large language models such as GPT-5 work in terms of tokens.

This tool can count tokens, using OpenAI's [tiktoken](https://github.com/openai/tiktoken) library.

It can also truncate text to a specified number of tokens.

See [llm, ttok and strip-tags—CLI tools for working with ChatGPT and other LLMs](https://simonwillison.net/2023/May/18/cli-tools-for-llms/) for more on this project.

## Installation

Install this tool using `pip`:
```bash
pip install ttok
```
Or `uv`:
```bash
uv tool install ttok
```
Or using Homebrew:
```bash
brew install simonw/llm/ttok
```
You can also run the tool without first installing it using `uvx`:
```bash
uvx ttok --help
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

To read text directly from a file, use `-i` or `--input`:

```bash
ttok -i input.txt
```

To pipe in text and then append extra tokens from arguments, use the `-i -` option:

```bash
echo -n "Hello world" | ttok more text -i -
```
```
4
```
## Different models

By default, the tokenizer model for GPT-5 (`o200k_base`) is used.

This default changed in ttok 1.0. To use the previous GPT-3.5 and GPT-4 tokenizer (`cl100k_base`), add `--model gpt-3.5-turbo`. Token counts, truncation results and token IDs can differ between tokenizers, so use the same model when encoding and decoding tokens.

To use the model for GPT-2 and GPT-3, add `--model gpt2`:

```bash
ttok boo Hello there this is -m gpt2
```
```
6
```
Compared to the default GPT-5 tokenizer:
```bash
ttok boo Hello there this is
```
```
5
```
Further model options are [documented here](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb).

## Truncating text

Use the `-t 3` or `--truncate 3` option to truncate text to three tokens:

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
13225 2375
```
The `--decode` method reverses this process:

```bash
ttok 13225 2375 --decode
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

## Special tokens

By default, special token strings such as `<|endoftext|>` cause an error. Use `--allow-special` to recognize them as special tokens when counting, truncating or encoding text:

```bash
ttok '<|endoftext|>' --allow-special
```
```
1
```

## Available models

These are the exact model names and their corresponding encodings recognized by `tiktoken`. Model names are valid for the `-m/--model` option.

Run `ttok --list-models` to see the model names and prefixes supported by your installed version of `tiktoken`.

<!-- [[[cog
import cog
import tiktoken
output = []
for key, value in tiktoken.model.MODEL_TO_ENCODING.items():
    output.append("- `{}` (`{}`)".format(key, value))
cog.out("\n".join(output))
]]] -->
- `o1` (`o200k_base`)
- `o3` (`o200k_base`)
- `o4-mini` (`o200k_base`)
- `gpt-5` (`o200k_base`)
- `gpt-4.1` (`o200k_base`)
- `gpt-4o` (`o200k_base`)
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

### Model name prefixes

The following prefixes are also recognized. The `*` stands for any suffix: for example, `gpt-5-mini` matches the GPT-5 prefix. Use the complete model name with `-m`. Exact names are checked first, then prefixes in the order listed. Prefix matching selects a tokenizer but does not verify that a model exists.

<!-- [[[cog
output = []
for key, value in tiktoken.model.MODEL_PREFIX_TO_ENCODING.items():
    output.append("- `{}*` (`{}`)".format(key, value))
cog.out("\n".join(output))
]]] -->
- `o1-*` (`o200k_base`)
- `o3-*` (`o200k_base`)
- `o4-mini-*` (`o200k_base`)
- `gpt-5*` (`o200k_base`)
- `gpt-4.5-*` (`o200k_base`)
- `gpt-4.1-*` (`o200k_base`)
- `chatgpt-4o-*` (`o200k_base`)
- `gpt-4o-*` (`o200k_base`)
- `gpt-4-*` (`cl100k_base`)
- `gpt-3.5-turbo-*` (`cl100k_base`)
- `gpt-35-turbo-*` (`cl100k_base`)
- `gpt-oss-*` (`o200k_harmony`)
- `ft:gpt-4o*` (`o200k_base`)
- `ft:gpt-4*` (`cl100k_base`)
- `ft:gpt-3.5-turbo*` (`cl100k_base`)
- `ft:davinci-002*` (`cl100k_base`)
- `ft:babbage-002*` (`cl100k_base`)
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

      ttok 13225 2375 --decode

  To see the details of the tokens:

      ttok "hello world" --tokens

  Outputs:

      [b'hello', b' world']

  To list model names and prefixes:

      ttok --list-models

Options:
  --version               Show the version and exit.
  -i, --input FILENAME
  -t, --truncate INTEGER  Truncate to this many tokens
  -m, --model TEXT        Which model to use  [default: gpt-5]
  --encode                Output token integers
  --decode                Convert token integers to text
  --tokens                Output full tokens
  --allow-special         Do not error on special tokens
  --list-models           List model names and prefixes and exit
  --help                  Show this message and exit.

```
<!-- [[[end]]] -->

You can also run this command using:

```bash
python -m ttok --help
```

## Development

To contribute to this tool, first checkout the code. Run the tests with `uv run pytest`:

```bash
cd ttok
uv run pytest
```
To run your development copy of the tool:
```bash
uv run ttok --help
```

The model names, prefixes and `--help` output in this README are generated using Cog. To regenerate them after making changes:

```bash
uv run cog -r README.md
```

To check that the generated sections are up to date, as CI does:

```bash
uv run cog --check README.md
```
