# mcp-explorer

[![PyPI](https://img.shields.io/pypi/v/mcp-explorer.svg)](https://pypi.org/project/mcp-explorer/)
[![Changelog](https://img.shields.io/github/v/release/simonw/mcp-explorer?include_prereleases&label=changelog)](https://github.com/simonw/mcp-explorer/releases)
[![Tests](https://github.com/simonw/mcp-explorer/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/mcp-explorer/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/mcp-explorer/blob/master/LICENSE)

CLI tool for exploring MCP servers

## Installation

Install this tool using `pip`:
```bash
pip install mcp-explorer
```
## Usage

List the tools exposed by a streamable HTTP MCP server:

```bash
mcp-explorer list https://agentic-mermaid.dev/mcp
```

The default output is deliberately compact: each tool is shown as a signature
and a one-line description. Use `-N` or `--no-truncate` for full descriptions
and detailed parameter metadata:

```bash
mcp-explorer list -N https://agentic-mermaid.dev/mcp
```

This forces the current MCP 2 stateless protocol by default. Use `--legacy` to
force the older initialize-handshake protocol instead:

```bash
mcp-explorer list https://agentic-mermaid.dev/mcp --legacy
```

Use `--json` to output the complete tool definitions, including their input
schemas:

```bash
mcp-explorer list https://agentic-mermaid.dev/mcp --json
```

Inspect a single tool in detail:

```bash
mcp-explorer inspect https://agentic-mermaid.dev/mcp render_svg
```

This displays the tool's complete description, nested input and output schemas,
annotations, execution metadata, icons, and `_meta`. Use `--json` for the
complete tool definition as a single JSON object:

```bash
mcp-explorer inspect https://agentic-mermaid.dev/mcp render_svg --json
```

Call a tool by passing its arguments as a JSON object:

```bash
mcp-explorer call \
  https://agentic-mermaid.dev/mcp \
  verify \
  '{"source":"graph TD; A-->B"}'
```

Alternatively, use repeatable `-a/--argument NAME VALUE` options:

```bash
mcp-explorer call \
  https://agentic-mermaid.dev/mcp \
  render_svg \
  -a source 'graph TD; A-->B' \
  -a options '{"padding":24}'
```

Use `-` to read the raw JSON object from standard input:

```bash
mcp-explorer call URL TOOL - < arguments.json
```

When raw JSON and `-a` are combined, individual arguments override matching
top-level keys in the JSON object and later `-a` values win. Values are
interpreted using the tool's input schema: strings remain literal, while
numbers, booleans, arrays, objects, and null are parsed as JSON. The assembled
arguments are validated against the input schema before the tool is called.

Use `--json` for the complete MCP `CallToolResult`:

```bash
mcp-explorer call URL TOOL -a name value --json
```

List every prompt exposed by a server:

```bash
mcp-explorer prompts URL
mcp-explorer prompts URL --json
mcp-explorer prompts URL --legacy
```

The human-readable output includes prompt arguments and whether each is
required. JSON output contains the complete prompt definitions.

List every directly-addressable resource exposed by a server:

```bash
mcp-explorer resources URL
mcp-explorer resources URL --json
mcp-explorer resources URL --legacy
```

The human-readable output includes each resource URI, MIME type, size, and
description when available. Both commands follow pagination until all results
have been collected.

Use `info` to show the selected protocol, negotiation mechanism, supported
versions, server identity, capabilities, and instructions:

```bash
mcp-explorer info https://agentic-mermaid.dev/mcp
mcp-explorer info https://agentic-mermaid.dev/mcp --json
```

Use `doctor` to check both stateless and legacy compatibility. The selected
mode is checked first and determines the exit status:

```bash
mcp-explorer doctor https://agentic-mermaid.dev/mcp
mcp-explorer doctor https://agentic-mermaid.dev/mcp --legacy
```

Every command accepts `--json` and `--stateless/--legacy`. These options can
appear anywhere after the command name.

For help, run:

```bash
mcp-explorer --help
```

You can also use:

```bash
python -m mcp_explorer --help
```
## Development

To contribute to this tool, first checkout the code. Run the tests like this:
```bash
cd mcp-explorer
uv run pytest
```
And the development version of the tool like this:
```bash
uv run mcp-explorer --help
```
