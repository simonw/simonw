# llm-coding-agent

[![PyPI](https://img.shields.io/pypi/v/llm-coding-agent.svg)](https://pypi.org/project/llm-coding-agent/)
[![Tests](https://github.com/simonw/llm-coding-agent/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-coding-agent/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-coding-agent?include_prereleases&label=changelog)](https://github.com/simonw/llm-coding-agent/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-coding-agent/blob/main/LICENSE)

A coding agent built on LLM

## Built by Fable 5

The first working alpha was built [using the following prompts](https://claude.ai/code/session_01TEUBvBbMipbFSoqjMiJ7ha):

> `Write a spec.md for this project - it will depend on the latest “llm” alpha from PyPI and implement a Claude code style coding agent complete with tools for reading and editing files and executing commands`

Then:

> `Commit the spec, then build it using red/green TDD in a series of sensible commits (each with passing tests and updated docs) - occasionally manually test it using the OpenAI API key in your environment`

## Installation

Install this library using `pip` (the `--pre` flag is needed while this depends on an LLM alpha release):
```bash
pip install --pre llm-coding-agent
```
## Usage

See [spec.md](spec.md) for the full design.

This package is an [LLM plugin](https://llm.datasette.io/en/latest/plugins/index.html): installing it adds an `llm code` command that starts an interactive coding agent session in the current directory, using any tool-capable model LLM knows about:

```bash
llm code                                   # interactive session, default model
llm code "add type hints to utils.py"      # start with an initial task
llm code -m gpt-4.1 -d ~/dev/myproject     # pick a model and directory
llm code --yolo                            # auto-approve every tool call
llm code --allow "pytest*" --allow "git diff*"   # pre-approve some commands
```

The model can read, search and edit files under the session directory and run shell commands there. Read-only tools run freely; file writes, edits and shell commands show you what the model wants to do and ask for approval - `y` approves once, `a` approves similar actions for the rest of the session, anything else declines (the model is told, and can try another approach). Inside a session `!quit` exits, `!yolo` toggles auto-approval, `!model MODEL` switches models mid-conversation and `!tokens` reports token usage.

Sessions are logged to LLM's SQLite database just like `llm chat`, so `llm logs` shows full transcripts including every tool call, and conversations can be resumed:

```bash
llm code -c                 # continue the most recent conversation
llm code --cid 01ab...      # continue a specific conversation ID
llm logs --short            # review what the agent did
```

The plugin also registers the toolbox with LLM itself, so the same tools work with [llm chat or llm prompt](https://llm.datasette.io/en/latest/usage.html):

```bash
llm chat --tool CodingTools --chain-limit 20
```

### CodingAgent

`CodingAgent` runs the full agent loop against any [LLM model](https://llm.datasette.io/en/latest/python-api.html) that supports tools:

```python
from llm_coding_agent import CodingAgent

agent = CodingAgent(
    model="gpt-4.1-mini",        # any llm model ID, or a model instance
    root="/path/to/project",
    approve=True,                # approve every tool call
)
result = agent.run("Fix the failing test in tests/test_parser.py")
print(result.text)               # the model's final answer
for tool_call, tool_result in result.tool_calls:
    print(tool_call.name, tool_call.arguments)

agent.run("Now add a changelog entry")   # the conversation continues
```

The `approve=` parameter controls what happens when the model wants to run a mutating tool (`write_file`, `edit_file`, `execute_command` - read-only tools never ask):

- `approve=True` approves everything
- `approve=callable` - a `(tool, tool_call) -> bool` function; returning `False` cancels that call and the model is told it was declined
- `approve=None` (the default) pauses the run: `result.paused` is true, `result.pending_tool_calls` lists what the model wants to do, and calling `agent.resume()` approves those calls and continues the loop - useful for approval flows in applications with no terminal attached

A `chain_limit=` (default 25) bounds how many tool-execution rounds a single `run()` can use; if it is hit, `result.hit_limit` is true.

### CodingTools

The tools themselves live on `CodingTools`, an [llm.Toolbox](https://llm.datasette.io/en/latest/python-api.html#python-api-toolbox) confined to a root directory, usable directly with `model.chain()`:

```python
from llm_coding_agent import CodingTools

tools = CodingTools("/path/to/project")
print(tools.read_file("README.md"))          # numbered lines, like cat -n
print(tools.read_file("big.log", offset=100, limit=50))
tools.write_file("notes/todo.md", "- ship it\n")   # creates parent dirs
print(tools.edit_file("app.py", "DEBUG = True", "DEBUG = False"))
```

`edit_file` performs exact string replacement: `old_string` must appear exactly once in the file (pass `replace_all=True` to replace every occurrence) and the tool returns a unified diff of the change so the model can verify what it did.

For exploring a project there are two search tools:

```python
print(tools.list_files("**/*.py"))            # newest first, respects .gitignore
print(tools.search_files("TODO", glob="*.py"))  # path:line:content matches
```

`search_files` uses [ripgrep](https://github.com/BurntSushi/ripgrep) when it is installed and falls back to a pure-Python scan (with identical output format) when it is not.

Shell commands run in the session root, with stdout and stderr interleaved and the exit code reported at the end:

```python
print(tools.execute_command("pytest -x", timeout=300))
```

On timeout (default 120s, capped at 600s) the entire process tree is killed and any partial output is returned.

All file access is confined to the root directory - relative paths resolve against it, and any path that escapes it (via `..`, absolute paths or symlinks) returns an `Error:` string instead of file content, so a model using these tools can see and correct its mistake.

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd llm-coding-agent
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
