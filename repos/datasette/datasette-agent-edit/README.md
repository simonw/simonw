# datasette-agent-edit

Storage-agnostic file-editing tools (`view` / `str_replace` / `insert` / batch
`edit`) for Datasette Agent plugins. The same tool behaviour can sit on top of
any storage layer — SQLite, the local filesystem, S3, the GitHub contents API,
…

## The three layers

1. **`operations`** — pure, synchronous string surgery (`view_lines`,
   `str_replace`, `insert`, `apply_edits`). No I/O, no `await`, no Datasette.
2. **`EditStore`** — the storage seam. The defining method is
   `edit(ref, transform)`: the backend reads the current content, runs your
   *pure* transform inside whatever critical section it needs, and persists the
   result atomically. A failing transform persists nothing.
   - `SqliteVersionedStore` runs the transform inside Datasette's write thread
     (`execute_write_fn`) and keeps full version history.
   - `DiskStore` uses a lock + atomic `os.replace`.
   - S3 (`If-Match`) and GitHub (`sha`) backends fit the same shape with a
     compare-and-set retry loop.
3. **`EditToolset`** — turns any `EditStore` into Datasette Agent tools with one
   consistent JSON envelope. Two hooks absorb the plugin-specific parts:
   - `id_codec` maps internal refs to the ids the model sees (e.g. an
     `artifact-` prefix).
   - `render` optionally injects presentation (e.g. an `_html` iframe preview);
     omit it and no `*_render` tool is registered.

## What the tools do

With `name_prefix="file"` the toolset registers `file_view`, `file_str_replace`,
`file_insert` and `file_edit`, plus `file_render` if you pass a `render` hook.

Every tool returns a JSON object. Success includes the id (under `id_field`)
and the current `version`; any failure is `{"error": "..."}` and saves
nothing. Bad input from the model — a malformed range, an out-of-range line
number, an edit with missing keys, a ref the store rejects — comes back as an
error rather than raising.

- **view** returns the content with `N:<tab>` line-number prefixes, plus
  `metadata` and `version`. `view_range` is `"start,end"`, 1-indexed and
  inclusive, with `-1` meaning end-of-file. Trailing whitespace is shown as-is
  so the text can be pasted into `str_replace`.
- **str_replace** replaces `old_str`, which must appear exactly once.
- **insert** adds `insert_text` as whole lines after line `insert_line` (`0`
  for the start, the line count for the end). A line break is added if the
  text would otherwise run into a neighbouring line.
- **edit** applies an array of `str_replace` / `insert` operations in order as
  one atomic change. If any of them fails, none are saved and the error names
  the failing edit.

Only `\n` (and so `\r\n`) ends a line, so line numbers match what an editor
shows.

The `render` hook's result is merged into the output of `edit` and `render`.
It cannot override the id, `version` or `status` fields. Because the hook runs
after a batch edit has been saved, a hook that raises does not fail the edit:
the result reports the edits as saved and adds a `render_error` key.

## Backend notes

Both bundled backends raise `FileExistsError` from `create()` if the ref is
taken, and leave `version` untouched when an edit returns the content
unchanged.

`SqliteVersionedStore` appends a row to its versions table for every change.

`DiskStore` treats a ref as a path under its root directory:

- Symlinks are resolved first, so a ref cannot reach outside the root.
- Metadata lives in a `<path>.meta.json` sidecar, so refs ending in
  `.meta.json` are reserved and rejected.
- Files must be UTF-8 text. Line endings are preserved byte-for-byte and an
  edited file keeps its permission bits.
- Locking is per-process; see the module docstring for cross-process use.

## Why `transform` is synchronous

The transform sits *between* a backend's awaits, never inside them — the SQLite
backend literally cannot `await` on its write thread, and the S3/GitHub backends
must not re-run network calls on every compare-and-set retry. If an edit
decision needs async work, resolve it first and close over the result:

```python
resolved = await registry.lookup(name)
await store.edit(ref, lambda c: rewrite(c, resolved))
```

A rare backend that genuinely needs in-transaction async can implement the
optional `AsyncTransformStore.aedit` capability; the toolset never requires it.

## Example

```python
from datasette_agent_edit import EditToolset, SqliteVersionedStore, PrefixCodec

store = SqliteVersionedStore(datasette.get_internal_database())
toolset = EditToolset(
    store,
    name_prefix="artifact",
    id_field="artifact_id",
    id_codec=PrefixCodec("artifact-"),
    render=lambda editable: {"_html": build_iframe(editable.content, editable.metadata)},
)
agent_tools = toolset.tools()   # list of AgentTool, ready to register
```

## Development

```bash
uv run pytest
```

The tests need Python 3.11 or later. `datasette-agent` is a development
dependency, used to test `EditToolset.tools()` against the real `AgentTool`.
