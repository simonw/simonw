# llm-keys-ui

[![PyPI](https://img.shields.io/pypi/v/llm-keys-ui.svg)](https://pypi.org/project/llm-keys-ui/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-keys-ui?include_prereleases&label=changelog)](https://github.com/simonw/llm-keys-ui/releases)
[![Tests](https://github.com/simonw/llm-keys-ui/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-keys-ui/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-keys-ui/blob/main/LICENSE)

A local web UI for setting keys used by [LLM](https://llm.datasette.io/).

This plugin is particularly useful if you are running a coding agent on a remote machine and want to set some API keys without pasting them into the agent context.

See [this blog post](https://simonwillison.net/2026/Sep/20/llm-keys-ui/) for screenshots and details.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-keys-ui
```

## Usage

Start the server on `127.0.0.1:8010`:

```bash
llm keys-ui
```

The port can be changed with `-p` or `--port`:

```bash
llm keys-ui -p 8080
```

Use `-h` or `--host` to listen on a different interface:

```bash
llm keys-ui -h 0.0.0.0
```

The `--all` option also listens on `0.0.0.0` and prints an HTTP URL for every IPv4 address assigned to the computer:

```bash
llm keys-ui --all
```

Use this if you want to set keys for a machine accessible via your local network or over Tailscale.

The interface does not implement authentication. Stop the server once you have set your keys.

Existing key values cannot be read using this tool.

## Development

To set up this plugin locally, first checkout the code. Then run the tests with `uv`:

```bash
cd llm-keys-ui
uv run pytest
```

To run LLM with your in-development plugin:

```bash
uv run llm --help
```
