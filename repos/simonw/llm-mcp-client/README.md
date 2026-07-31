# llm-mcp-client

[![PyPI](https://img.shields.io/pypi/v/llm-mcp-client.svg)](https://pypi.org/project/llm-mcp-client/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-mcp-client?include_prereleases&label=changelog)](https://github.com/simonw/llm-mcp-client/releases)
[![Tests](https://github.com/simonw/llm-mcp-client/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-mcp-client/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-mcp-client/blob/main/LICENSE)

Access tools from MCP servers as LLM tools

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-mcp-client
```
## Usage

This plugin registers a toolbox called `MCP` which connects to an [MCP](https://modelcontextprotocol.io/) server, discovers the tools it exposes and makes them available as LLM tools.

Pass the URL of an MCP server to the toolbox:

```bash
llm -T 'MCP("https://example.com/mcp")' 'Ask something that needs a tool' --td
```

The `--td` option shows details of the tool calls as they execute.

It works in `llm chat` too:

```bash
llm chat -T 'MCP("https://example.com/mcp")'
```

## Templates

You can save an MCP to a named [LLM template](https://llm.datasette.io/en/latest/templates.html) like this:
```bash
llm -T 'MCP("https://datasette.simonwillison.net/-/mcp")' --save blog
```
Now you can query it without specifying the full tool definition like this:
```bash
llm -t blog 'count entries and notes'
```

### Protocol modes

By default the client negotiates the protocol automatically. You can force a specific mode with the `mode=` argument:

```bash
# Force modern stateless MCP:
llm -T 'MCP("https://example.com/mcp", mode="stateless")' '...'
# Force the legacy initialize handshake:
llm -T 'MCP("https://example.com/mcp", mode="legacy")' '...'
```

### Tool name prefixes

If you are using tools from more than one server and their names might clash, give each server a prefix:

```bash
llm -T 'MCP("https://one.example.com/mcp", prefix="one_")' \
    -T 'MCP("https://two.example.com/mcp", prefix="two_")' '...'
```

### Python API

```python
import llm
from llm_mcp_client import MCP

model = llm.get_model("gpt-4.1-mini")
result = model.chain(
    "Ask something that needs a tool",
    tools=[MCP("https://example.com/mcp")],
).text()
```

Tool results containing MCP image or audio content are returned to the model as LLM attachments. An MCP error result raises `llm_mcp_client.MCPToolError`, which LLM passes back to the model as an error message.

## Development

To set up this plugin locally, first checkout the code. Then run the tests with `uv`:
```bash
cd llm-mcp-client
uv run pytest
```
To run LLM with your in-development plugin:
```bash
uv run llm --help
```
