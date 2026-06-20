# asgi-replay

[![PyPI](https://img.shields.io/pypi/v/asgi-replay.svg)](https://pypi.org/project/asgi-replay/)
[![Changelog](https://img.shields.io/github/v/release/simonw/asgi-replay?include_prereleases&label=changelog)](https://github.com/simonw/asgi-replay/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/asgi-replay/blob/main/LICENSE)

A tool for recording and replaying requests using ASGI.

## Very early prototype

This is an early prototype. I have used this tool exactly once.

## Installation

```bash
pip install asgi-replay
```

## Usage

The tool provides two commands - one for recording logs of ASGI requests and one for running a server to replay them.

### Recording

```bash
asgi-replay record https://www.example.com log.json --port 8000
```
This runs a local server on port `8000` that proxies content through to `www.example.com` - and logs each request to `log.json`.

The `log.json` file will be over-written for each request. This tool is mainly designed for capturing a single HTTP interaction.

If you add `--increment` a new file will be written for each request, starting with `log-0.json` and then `log-1.json` and so on.

### Replaying

To replay a single log - such that any HTTP request to the local server will replay that exact response - run this:
```bash
asgi-replay replay log.json --port 8000
```
(8000 is the default port for both commands.)

## What I built this for

I wanted to build a tiny application that could simulate the streaming response from an OpenAI completion endpoint.

The app I built is here: https://github.com/simonw/openai-canned-completion

You can hit it using [LLM](https://llm.datasette.io/) like this:
```bash
OPENAI_API_KEY='x' \
OPENAI_API_BASE='https://openai-canned-completion.vercel.app/v1' \
llm 'hello'
```

I first ran the following on my own machine:
```bash
asgi-replay record https://api.openai.com log.json --port 8000
```
Then:
```bash
OPENAI_API_BASE='http://localhost:8000/v1' \
llm 'hello'
```
This ran a real request against OpenAI and saved the response in `log.json`.

Then I ran the replay like this:
```bash
asgi-replay record https://api.openai.com log.json --port 8000
```
And when I ran the `llm` command again I got the same response, without hitting the OpenAI API:
```bash
OPENAI_API_BASE='http://localhost:8000/v1' \
llm 'hello'
```
```
Hello! How can I assist you today?
```
I copied the saved ASGI logs into this ASGI app: https://github.com/simonw/openai-canned-completion/blob/main/canned.py
