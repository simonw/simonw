# datasette-paper

[![PyPI](https://img.shields.io/pypi/v/datasette-paper.svg)](https://pypi.org/project/datasette-paper/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-paper?include_prereleases&label=changelog)](https://github.com/datasette/datasette-paper/releases)
[![Tests](https://github.com/datasette/datasette-paper/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-paper/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-paper/blob/main/LICENSE)

Collaborative document editor for Datasette. ProseMirror frontend, SQLite-backed
storage in Datasette's internal database, real-time collaboration over SSE.

<p align="center"><img src="docs/screenshots/editor.png" alt="The paper editor: a rich-text document with headings, a table and a task list, a formatting toolbar, and a header showing the author, edit time and number of users online." width="800"></p>

Rich text with **tables** and **task lists**, **wiki-style links** between papers,
**images** (paste, drag-and-drop, or insert from the toolbar), and **per-paper
sharing**:

<table>
<tr>
<td><img src="docs/screenshots/tables.png" alt="A table in the editor with the floating action bar for adding/removing rows and columns and naming the table for the API."></td>
<td><img src="docs/screenshots/tasks.png" alt="A task list with checkboxes; completed items are struck through."></td>
</tr>
<tr>
<td><img src="docs/screenshots/wiki-links.png" alt="Typing [[ opens an autocomplete popup listing other papers to link to."></td>
<td><img src="docs/screenshots/share.png" alt="The share dialog showing people with access and their roles, plus general link access."></td>
</tr>
<tr>
<td><img src="docs/screenshots/link-edit.png" alt="Hovering a link while editing reveals a tooltip with Edit, Open and Copy; Edit opens a small dialog with Text and URL fields to rewrite the link."></td>
<td></td>
</tr>
</table>

Insert an image by pasting, dropping a file, or using the toolbar's image
button — which offers a paste area or a file upload with a live preview:

<p align="center"><img src="docs/screenshots/image-dialog-chosen.png" alt="The insert-image dialog with the Upload tab active, showing a preview of the chosen image, an alt-text field, and an enabled Insert button." width="440"></p>

And a paper index listing everyone's papers with author and last-edited time:

<p align="center"><img src="docs/screenshots/index.png" alt="The paper index: a table of papers with name, creator and updated time, plus tabs for Active / Archive / Trash / Templates." width="800"></p>

Drop inline **`#tags`** anywhere in a paper's body — type `#` for an
autocomplete of existing tags. Clicking a tag opens a results page listing
every paper whose body mentions it:

<table>
<tr>
<td><img src="docs/screenshots/inline-tags.png" alt="Inline #tag pills in a paper's body, distinct from the document-level metadata tags."></td>
<td><img src="docs/screenshots/tag-page.png" alt="The tag results page: every paper whose body contains #roadmap, each with a mention count."></td>
</tr>
</table>

## Installation

Install in the same environment as Datasette:

```bash
datasette install datasette-paper
```

## Quickstart

```bash
datasette --internal papers.db \
  -s permissions.datasette-paper-list true \
  -s permissions.datasette-paper-create true \
  -s permissions.datasette-paper-view true \
  -s permissions.datasette-paper-edit true
```

No user database is required — papers live in Datasette's internal database.

**Pass `--internal <path>` to persist papers across restarts.** Without it,
Datasette uses an ephemeral tempfile for the internal DB that is deleted
when the process exits. The plugin emits a startup warning when it detects
this, so you don't lose your papers to a forgotten flag.

## Permissions

Four actions gate access. The view/edit actions are per-paper; list/create
are global.

| Action | Scope | Gates |
|---|---|---|
| `datasette-paper-list` | global | The paper index page and the list endpoint. |
| `datasette-paper-create` | global (also-requires `list`) | Creating new papers. |
| `datasette-paper-view` | per-paper (`PaperResource`) | Reading a specific paper (bootstrap, SSE, document, tasks). |
| `datasette-paper-edit` | per-paper (`PaperResource`, also-requires `view`) | Modifying a specific paper (events, presence, rename, snapshot, share). |

The plugin registers a `permission_resources_sql` hook that resolves
per-paper view/edit grants from the `_datasette_paper_doc.created_by`
column (owners) and the `_datasette_paper_share` table (explicit grants
+ link-visibility levels).

## Sharing

Each paper has one of three visibility levels:

- `private` — only the owner and explicitly-shared actors can access.
- `link-view` — any authenticated actor with the link can view.
- `link-edit` — any authenticated actor with the link can view and edit.

Plus per-actor share rows that grant a specific actor a `viewer` or
`editor` role on a single paper.

The owner is whoever created the paper (`created_by`, captured from the
actor cookie at create time). Only the owner can change visibility or
mutate shares.

## Papers as data

Paper data lives in Datasette's internal database under tables prefixed
with `_datasette_paper_`:

- `_datasette_paper_doc` — one row per paper (id, name, visibility, created_by).
- `_datasette_paper_step` — append-only log of ProseMirror steps.
- `_datasette_paper_snapshot` — periodic full-document snapshots.
- `_datasette_paper_share` — per-actor view/edit grants.

## Wire protocol

JSON API rooted at `/-/paper/api/...` — no per-database segment. List/create
docs, bootstrap a paper, post step batches, stream updates over SSE, manage
shares, render markdown / extract tasks. See `CLAUDE.md` for the full
endpoint table.

## Frontend stack

Vite + Svelte 5 + ProseMirror. Bundle outputs to `datasette_paper/static/`.

## Development

```bash
npm install --prefix frontend
just frontend          # build the bundle
just dev               # run datasette with the plugin + permissions granted
just dev-with-hmr      # vite dev server + watchexec restart
just shots             # regenerate docs/screenshots/*.png (used in this README)
```

`just shots` is self-contained: it builds the bundle, boots a throwaway
Datasette with seeded papers, drives Playwright to capture each surface, and
tears the server down. The PNGs are committed, so re-run and commit when the UI
changes (the diff shows what changed). Pass shot names to regenerate a subset,
e.g. `just shots editor tables`.

Run the test layers:

```bash
just test              # backend pytest
just test-frontend     # vitest
just test-e2e          # playwright (requires built bundle)
```

Always invoke Python with `uv run --prerelease=allow …` — `datasette` is on
a `>=1a23` pre-release pin.
