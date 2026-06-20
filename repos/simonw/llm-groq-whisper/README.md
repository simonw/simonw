# llm-groq-whisper

[![PyPI](https://img.shields.io/pypi/v/llm-groq-whisper.svg)](https://pypi.org/project/llm-groq-whisper/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-groq-whisper?include_prereleases&label=changelog)](https://github.com/simonw/llm-groq-whisper/releases)
[![Tests](https://github.com/simonw/llm-groq-whisper/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-groq-whisper/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-groq-whisper/blob/main/LICENSE)

Transcribe audio using the [Groq.com Whisper API](https://console.groq.com/docs/speech-text)

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-groq-whisper
```
You'll need a [Groq API key](https://console.groq.com/keys). Configure the API key like this:
```bash
llm keys set groq
# Paste key here
```
## Usage

Run transcripts using:
```bash
llm groq-whisper audio.mp3
```


## llm groq-whisper --help

<!-- [[[cog
import cog
from llm import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["groq-whisper", "--help"])
help = result.output.replace("Usage: cli", "Usage: llm")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: llm groq-whisper [OPTIONS] AUDIO_FILE

  Run transcriptions or translations using the Groq Whisper API

  Usage:

      llm groq-whisper audio.mp3 > output.txt
      cat audio.mp3 | llm groq-whisper - > output.txt

  Examples:

      # Basic transcription
      llm groq-whisper audio.mp3

      # Translation to English
      llm groq-whisper --translate audio.mp3

      # Transcription with specific model and language
      llm groq-whisper --model whisper-large-v3 --language fr audio.mp3

      # Detailed JSON output with timestamps
      llm groq-whisper --response-format verbose_json audio.mp3

Options:
  --key TEXT                      Groq API key to use
  --model [whisper-large-v3-turbo|distil-whisper-large-v3-en|whisper-large-v3]
                                  Whisper model to use
  --response-format [json|verbose_json|text]
                                  Response format
  --language TEXT                 Language code (e.g., 'en' for English). Only
                                  for whisper-large-v3-turbo and whisper-
                                  large-v3
  --temperature FLOAT             Temperature between 0 and 1
  --prompt TEXT                   Optional context or spelling guidance (max 224
                                  tokens)
  --translate                     Use translation endpoint instead of
                                  transcription
  --help                          Show this message and exit.

```
<!-- [[[end]]] -->

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-groq-whisper
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
