# llm-whisper-api

[![PyPI](https://img.shields.io/pypi/v/llm-whisper-api.svg)](https://pypi.org/project/llm-whisper-api/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-whisper-api?include_prereleases&label=changelog)](https://github.com/simonw/llm-whisper-api/releases)
[![Tests](https://github.com/simonw/llm-whisper-api/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-whisper-api/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-whisper-api/blob/main/LICENSE)

Run transcriptions using the OpenAI Whisper API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-whisper-api
```
## Usage

The plugin adds a new command, `llm whisper-api`. Use it like this:

```bash
llm whisper-api audio.mp3
```
The transcribed audio will be output directly to standard output as plain text.

The plugin will use the OpenAI API key you have already configured using:
```bash
llm keys set openai
# Paste key here
```
You can also pass an explicit API key using `--key` like this:

```bash
llm whisper-api audio.mp3 --key $OPENAI_API_KEY
```

You can pipe data to the tool if you specify `-` as a filename:

```bash
curl -s 'https://static.simonwillison.net/static/2024/russian-pelican-in-spanish.mp3' \
  | llm whisper-api -
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-whisper-api
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
