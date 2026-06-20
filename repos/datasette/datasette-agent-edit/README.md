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
