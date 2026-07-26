# llm-apple-foundation

[![PyPI](https://img.shields.io/pypi/v/llm-apple-foundation.svg)](https://pypi.org/project/llm-apple-foundation/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-apple-foundation?include_prereleases&label=changelog)](https://github.com/simonw/llm-apple-foundation/releases)
[![Tests](https://github.com/simonw/llm-apple-foundation/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-apple-foundation/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-apple-foundation/blob/main/LICENSE)

Run prompts through the Apple Foundation model on macOS using Apple's official
[Foundation Models SDK for Python](https://github.com/apple/python-apple-fm-sdk).

Prompts and responses stay on your Mac. No API key is required.

## Requirements

- macOS 26 or later
- A Mac that supports Apple Intelligence
- Apple Intelligence turned on, with its model downloaded
- Xcode 26 or later, with the Xcode and Apple SDKs agreement accepted
- Python 3.10 or later

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-apple-foundation
```

## Usage

Run a prompt using the `apple-foundation` model:

```bash
llm -m apple-foundation "What is the capital of France?"
```

The shorter `afm` alias is also available:

```bash
llm -m afm "Suggest three names for a pelican"
```

LLM streams responses by default. Use `--no-stream` to wait for the complete
response:

```bash
llm -m apple-foundation --no-stream "Explain what a mutex is"
```

System prompts are passed to Apple as session instructions:

```bash
llm -m apple-foundation \
  --system "You explain technical topics using short sentences." \
  "Explain virtual memory"
```

### Conversations

Apple's native session transcript is stored in LLM's response metadata. This
allows conversations to continue even when separate CLI invocations are used.

Start an interactive chat:

```bash
llm chat -m apple-foundation
```

Or continue the most recent logged conversation:

```bash
llm -m apple-foundation "Remember that my favorite bird is the puffin"
llm -c "What is my favorite bird?"
```

### Options

Show the available options:

```bash
llm models --options -q apple-foundation
```

The plugin supports:

- `temperature`: Sampling temperature
- `max_tokens`: Maximum number of response tokens
- `sampling`: `greedy` or `random`
- `top`: Top-k constraint for random sampling
- `probability_threshold`: Cumulative probability constraint for random sampling
- `seed`: Seed for random sampling
- `use_case`: `general` or `content_tagging`
- `guardrails`: `default` or `permissive_content_transformations`

Use deterministic greedy sampling:

```bash
llm -m apple-foundation \
  -o sampling greedy \
  -o max_tokens 100 \
  "Summarize the purpose of DNS"
```

Use seeded random sampling over the top 40 tokens:

```bash
llm -m apple-foundation \
  -o sampling random \
  -o top 40 \
  -o seed 42 \
  "Write a tiny story about a cormorant"
```

Use Apple's content-tagging model configuration:

```bash
llm -m apple-foundation \
  -o use_case content_tagging \
  "Tag this note: Fixed a subtle race condition in the upload worker"
```

### Structured output

LLM JSON Schemas are translated to the schema format required by Apple:

```bash
llm -m apple-foundation \
  --schema 'bird, legs int' \
  "Describe a pelican"
```

Apple's SDK does not stream guided generation, so schema responses are returned
as one complete JSON value.

### Tools

Pass tools registered with LLM using `-T`:

```bash
llm -m afm -T llm_time "what time is it?"
```

Python functions can also be supplied as tools:

```python
import llm


def multiply(a: int, b: int) -> int:
    "Multiply two integers."
    return a * b


response = llm.get_model("afm").prompt(
    "What is 17 times 24?",
    tools=[multiply],
)
print(response.text())
```

### Async Python API

An async model is registered alongside the synchronous CLI model:

```python
import llm


async def generate():
    model = llm.get_async_model("apple-foundation")
    response = model.prompt("Suggest a birdwatching tip")
    return await response.text()
```

## Current scope

This initial version supports text generation, streaming, system instructions,
generation options, structured output, tools, persistent conversations, and
both the synchronous and asynchronous LLM APIs.

Image attachments are not yet supported by this plugin.

## Development

The tests use the actual on-device Apple Foundation model. They are skipped if
the SDK or model is unavailable.

```bash
cd llm-apple-foundation
uv run pytest
```

To run LLM with the development version:

```bash
uv run llm -m apple-foundation "Hello"
```

Build the distribution packages:

```bash
uv build
```
