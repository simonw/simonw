# datasette-mcp

[![PyPI](https://img.shields.io/pypi/v/datasette-mcp.svg)](https://pypi.org/project/datasette-mcp/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-mcp?include_prereleases&label=changelog)](https://github.com/datasette/datasette-mcp/releases)
[![Tests](https://github.com/datasette/datasette-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-mcp/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-mcp/blob/main/LICENSE)

Adds a /-/mcp MCP server to any Datasette instance

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-mcp
```
## Usage

Start Datasette as normal, then configure an MCP client to connect to:

```
http://localhost:8001/-/mcp
```

The endpoint uses MCP Streamable HTTP and exposes three read-only tools by
default:

- `list_databases` lists the databases available to the current Datasette
  actor.
- `get_database_schema` returns the complete SQL schema for a database,
  including tables, indexes, views, and triggers.
- `execute_sql` executes one read-only SQL statement and returns structured
  columns, rows, and a truncation indicator.

Datasette database visibility and `execute-sql` permissions are enforced for
every tool call. SQL uses the same `validate_sql_select()` and read-only
`Database.execute()` path as Datasette's custom SQL interface.

## Registering additional MCP tools

Other Datasette plugins can add tools to this MCP server by implementing the
`register_mcp_tools(datasette, mcp)` plugin hook. The `mcp` argument is the
`MCPServer` for that Datasette instance, so implementations use the MCP Python
SDK's normal `@mcp.tool()` decorator:

```python
from datasette import hookimpl


@hookimpl
def register_mcp_tools(datasette, mcp):
    @mcp.tool()
    async def database_count() -> int:
        """Return the number of user-facing databases."""
        return len(
            [name for name in datasette.databases if name != "_internal"]
        )
```

The hook itself is synchronous because tools are registered while the MCP
server is being constructed. Tool functions can be synchronous or asynchronous
and can use all of the input, output, context, and annotation features provided
by the MCP Python SDK.

Datasette-mcp registers `list_databases`, `get_database_schema`, and
`execute_sql` through this same hook.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-mcp
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
