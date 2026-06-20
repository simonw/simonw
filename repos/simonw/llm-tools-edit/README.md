# llm-tools-edit

[![PyPI](https://img.shields.io/pypi/v/llm-tools-edit.svg)](https://pypi.org/project/llm-tools-edit/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-tools-edit?include_prereleases&label=changelog)](https://github.com/simonw/llm-tools-edit/releases)
[![Tests](https://github.com/simonw/llm-tools-edit/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-tools-edit/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-edit/blob/main/LICENSE)

LLM plugin providing tools for editing files. Gives LLMs the ability to create, view, and modify files using three interchangeable backends.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-edit
```

## Backends

This plugin provides three Toolbox backends. Each provides the same five tools:

| Tool | Description |
|------|-------------|
| `view` | View file contents with line numbers, or list a directory |
| `str_replace` | Replace an exact string in a file (must appear exactly once) |
| `create` | Create a new file (errors if it already exists) |
| `insert` | Insert text after a given line number |
| `list_files` | List all files |

### Filesystem

Edit real files on disk, scoped to a specific directory. All paths are relative to the root directory, and path traversal outside the root is blocked.

```bash
llm -T 'Filesystem("/tmp/myproject")' "Create a Python hello world app"
```

The `path` argument is the root directory. All file operations are restricted to this directory and its subdirectories.

### MemoryFS

An in-memory virtual filesystem. Files exist only in memory and are discarded when the process exits. State persists across tool calls within a single conversation, so an LLM agent can create files and iteratively edit them without touching disk.

```bash
llm -T MemoryFS "Create a Flask app with two routes"
```

No arguments required. Paths use absolute format (e.g. `/src/main.py`).

### SQLiteFS

Store files in a SQLite database table. The table is created automatically if it doesn't exist. State persists across sessions — you can come back later and continue editing.

```bash
llm -T 'SQLiteFS(db_path="demo.db", table_name="files")' "Create a hello world app"
```

Arguments:
- `db_path` — path to the SQLite database file
- `table_name` — name of the table to store files in (schema: `path TEXT PRIMARY KEY, content TEXT`)

## Output truncation

Large files and single-line blobs (e.g. minified JS) can overwhelm a model's context window. All three backends accept optional `max_lines` and `max_chars` keyword arguments that truncate `view` output and append a message telling the model how to see more:

```bash
llm -T 'Filesystem("/tmp/myproject", max_lines=200, max_chars=20000)' "Fix the bug in app.py"
```

```python
fs = MemoryFS(max_lines=200, max_chars=20000)
sqlfs = SQLiteFS("demo.db", "files", max_lines=200, max_chars=20000)
```

- **`max_lines`** — truncate after this many lines. A footer like `[Showing lines 1-200 of 5,432 total. Use view_range to see more.]` is appended.
- **`max_chars`** — truncate after this many characters of formatted output. Catches the degenerate case of a single 2 MB line with no newlines. A footer like `[Truncated: output exceeded 20,000 character limit. ...]` is appended.

Both limits are off (`None`) by default. When both are set, whichever triggers first takes effect — and both footers appear if both trigger. The model can always use `view_range` to read specific sections of a large file without hitting the limits.

## Tool details

### view

View a file's contents with line numbers, or list a directory's entries.

The optional `view_range` parameter accepts a comma-separated start and end line number (1-indexed). Use `-1` for end to mean end-of-file.

Examples: `view_range="1,10"` shows lines 1-10, `view_range="5,-1"` shows line 5 to end.

### str_replace

Find and replace an exact string in a file. The `old_str` must appear exactly once in the file — if it appears zero times or more than once, the tool raises an error. This ensures replacements are unambiguous.

### create

Create a new file with the given content. Raises an error if the file already exists (to prevent accidental overwrites). For `Filesystem`, parent directories are created automatically if needed.

### insert

Insert text after a given line number. Use `insert_line=0` to insert at the beginning of the file.

## Library functions

The text-editing primitives used internally by the Toolbox classes are also available as standalone functions. You can import and use these directly in your own code.

### `view_lines(content, view_range="", *, max_lines=None, max_chars=None)`

Format a string as numbered lines. Returns each line prefixed by its 1-indexed line number and a tab.

```python
from llm_tools_edit.lib import view_lines

view_lines("alpha\nbeta\ngamma\n")
# '1:\talpha\n2:\tbeta\n3:\tgamma'

view_lines("alpha\nbeta\ngamma\n", view_range="2,3")
# '2:\tbeta\n3:\tgamma'

view_lines("alpha\nbeta\ngamma\n", view_range="2,-1")
# '2:\tbeta\n3:\tgamma'
```

The `view_range` parameter accepts `"start,end"` (1-indexed). Use `-1` for end to mean end-of-file.

The optional `max_lines` and `max_chars` parameters truncate output and append a descriptive footer when limits are exceeded:

```python
content = "".join(f"line {i}\n" for i in range(10_000))

view_lines(content, max_lines=3)
# '1:\tline 0\n2:\tline 1\n3:\tline 2\n[Showing lines 1-3 of 10000 total. Use view_range to see more.]'

view_lines("x" * 1_000_000, max_chars=50)
# '1:\txxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n[Truncated: ...]'
```

### `str_replace_content(content, path, old_str, new_str)`

Replace exactly one occurrence of `old_str` in `content`. Raises `ValueError` if the string is not found or appears more than once, ensuring every replacement is unambiguous. The `path` argument is used only in error messages.

```python
from llm_tools_edit.lib import str_replace_content

str_replace_content("hello world", "f.py", "hello", "goodbye")
# 'goodbye world'

str_replace_content("aaa\naaa", "f.py", "aaa", "bbb")
# ValueError: old_str appears 2 times in f.py; must be unique
```

### `insert_content(content, insert_line, insert_text)`

Insert text after a given line number. Use `insert_line=0` to insert at the beginning.

```python
from llm_tools_edit.lib import insert_content

insert_content("line1\nline2\n", 1, "new\n")
# 'line1\nnew\nline2\n'

insert_content("line1\nline2\n", 0, "header\n")
# 'header\nline1\nline2\n'
```

### `list_dir_from_paths(paths, prefix)`

Given a flat list of absolute file paths and a directory prefix, return the set of immediate children — files as bare names, subdirectories with a trailing `/`. Returns `None` if nothing matches.

```python
from llm_tools_edit.lib import list_dir_from_paths

list_dir_from_paths(["/src/main.py", "/src/utils.py", "/README.md"], "/")
# {'README.md', 'src/'}

list_dir_from_paths(["/src/main.py", "/src/lib/helper.py"], "/src")
# {'main.py', 'lib/'}

list_dir_from_paths(["/src/main.py"], "/other")
# None
```

## Python API

```python
import llm
from llm_tools_edit import Filesystem, MemoryFS, SQLiteFS

model = llm.get_model("gpt-4.1-mini")

# Real filesystem — scoped to a directory
fs = Filesystem("/tmp/myproject")
result = model.chain(
    "Create a hello world Python app",
    tools=[fs],
).text()

# In-memory filesystem
memfs = MemoryFS()
result = model.chain(
    "Create a Flask app",
    tools=[memfs],
).text()

# SQLite-backed filesystem
sqlfs = SQLiteFS("demo.db", "files")
result = model.chain(
    "Create a hello world app",
    tools=[sqlfs],
).text()
```

For multi-turn conversations where state persists across prompts:

```python
memfs = MemoryFS()
conversation = model.conversation(tools=[memfs])
conversation.chain("Create /app.py with a Flask hello-world app")
conversation.chain("Add a /goodbye route to the app")
conversation.chain("View the final version of /app.py")
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-edit
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
