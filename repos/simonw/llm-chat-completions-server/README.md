# llm-chat-completions-server

[![PyPI](https://img.shields.io/pypi/v/llm-chat-completions-server.svg)](https://pypi.org/project/llm-chat-completions-server/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-chat-completions-server?include_prereleases&label=changelog)](https://github.com/simonw/llm-chat-completions-server/releases)
[![Tests](https://github.com/simonw/llm-chat-completions-server/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-chat-completions-server/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-chat-completions-server/blob/main/LICENSE)

LLM plugin to serve an OpenAI Chat Completions API endpoint

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-chat-completions-server
```

## Usage

Start the server:

```bash
llm chat-completions-server
```

It listens on `http://127.0.0.1:8002` by default. Use `-p` or `--port` to
select a different port:

```bash
llm chat-completions-server --port 9000
```

For development, `--reload` restarts the server when Python files change:

```bash
llm chat-completions-server --reload
```

The server does not require an API token. Models may still need credentials
configured on the server using the usual `llm keys set` commands.

### List models

`GET /v1/models` lists the models registered with LLM that provide an async
implementation. Sync-only models are not served.

```bash
curl http://127.0.0.1:8002/v1/models
```

### Create a chat completion

`POST /v1/chat/completions` implements the classic OpenAI Chat Completions
request and response format using LLM's async model API.

```bash
curl -s http://127.0.0.1:8002/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gemini/gemini-2.5-flash",
    "messages": [
      {"role": "user", "content": "Tell me a short joke about pelicans"}
    ],
    "stream": false
  }'
```

Streaming responses use server-sent events and finish with `data: [DONE]`:

```bash
curl -N http://127.0.0.1:8002/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gemini/gemini-2.5-flash",
    "messages": [
      {"role": "user", "content": "Count to three"}
    ],
    "stream": true,
    "stream_options": {"include_usage": true}
  }'
```

The endpoint accepts system, developer, user, assistant and tool messages,
including image URL content and function tool calls. Sampling options are
passed through when they are supported by the selected LLM model. Only
`n=1` is currently supported.

Completed responses—including streamed responses—are written to LLM's normal
`logs.db`. This populates both the legacy response tables and the current
content-addressed message and turn tables. The global `llm logs off` setting
is respected.

## Development

This checkout is configured to use the editable in-development LLM checkout
at `~/dev/llm`. Run the tests with:

```bash
cd llm-chat-completions-server
uv run pytest
```

To run the server with additional model plugins under development:

```bash
uv run \
  --with-editable . \
  --with-editable ~/dev/llm \
  --with-editable ~/dev/ecosystem/llm-gemini \
  --with-editable ~/dev/ecosystem/llm-anthropic \
  --with-editable ~/dev/ecosystem/llm-apple-foundation \
  llm chat-completions-server --reload
```
