# datasette-agent-micropython

[![PyPI](https://img.shields.io/pypi/v/datasette-agent-micropython.svg)](https://pypi.org/project/datasette-agent-micropython/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-agent-micropython?include_prereleases&label=changelog)](https://github.com/datasette/datasette-agent-micropython/releases)
[![Tests](https://github.com/datasette/datasette-agent-micropython/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-agent-micropython/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-agent-micropython/blob/main/LICENSE)

Run Python code in a MicroPython/WASM sandbox

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-agent-micropython
```
## Usage

This plugin adds an `execute_micropython` tool to
[Datasette Agent](https://github.com/datasette/datasette-agent). The tool runs
Python code using a sandboxed MicroPython interpreter compiled to WASM.

Use it for pure computation, parsing, data transformation, math, and checking
algorithms. Output is captured from stdout and stderr, so code should use
`print()` to return values:

```python
print(sum(range(10)))
```

Each Datasette Agent conversation gets its own persistent MicroPython
interpreter. Variables, imports, and functions defined in one tool call can be
reused later in the same conversation:

```python
def fib(n):
    a, b = 0, 1
    out = []
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out

print(fib(10))
```

That state is not shared with other conversations. Use `reset_context=true` to
clear the current conversation's interpreter before running code. If execution
times out, exhausts fuel, or traps the WASM runtime, that conversation's
interpreter is discarded and the next call starts fresh.

No network APIs are available, and no host filesystem is exposed by default.

The MicroPython environment includes a `read_only_sql_query()` helper for
querying Datasette databases:

```python
result = read_only_sql_query(
    "data",
    "select name, qty from items where qty > :min_qty",
    {"min_qty": 2},
)
print(result["columns"])
print(result["rows"])
```

It accepts `name_of_database`, `sql`, and an optional params dict. It uses the
current actor's `execute-sql` permission and returns a dict containing
`columns`, `rows`, and `truncated`, or an `error` key.

The tool accepts:

- `python` - MicroPython code to execute
- `reset_context` - clear this conversation's interpreter before running
- `show_result` - render the code and captured output inline for the user

Use `show_result=true` when the user asked to see the code or output, or when
showing both would help with explanation, debugging, teaching, or
reproducibility. The rendered HTML shows the executed code, then the captured
stdout. When this is set, the tool result tells the agent that the output has
already been shown to the user and does not need to be repeated. Leave it unset
for scratch calculations.

## Configuration

Configure the plugin using Datasette plugin settings:

```yaml
plugins:
  datasette-agent-micropython:
    max_sessions: 16
    wall_clock_timeout_seconds: 5.0
    memory_bytes: 16777216
    fuel: 10000000
    max_output_chars: 10000
```

Settings:

- `max_sessions` - maximum live conversation interpreters to keep; defaults to
  `16`. The least recently used interpreter is closed when the limit is
  exceeded.
- `wall_clock_timeout_seconds` - timeout for each code execution; defaults to
  `5.0`.
- `memory_bytes` - maximum WebAssembly linear memory for each interpreter;
  defaults to `16777216` (16MB).
- `fuel` - Wasmtime fuel budget refreshed for each execution; defaults to
  `10000000`.
- `max_output_chars` - maximum captured output/error characters returned to the
  model; defaults to `10000`.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-agent-micropython
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
