# datasette-paper

[![PyPI](https://img.shields.io/pypi/v/datasette-paper.svg)](https://pypi.org/project/datasette-paper/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-paper?include_prereleases&label=changelog)](https://github.com/datasette/datasette-paper/releases)
[![Tests](https://github.com/datasette/datasette-paper/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-paper/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-paper/blob/main/LICENSE)

Collaborative document editor for Datasette. ProseMirror frontend, SQLite-backed
storage in Datasette's internal database, real-time collaboration over SSE.

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
```

Run the test layers:

```bash
just test              # backend pytest
just test-frontend     # vitest
just test-e2e          # playwright (requires built bundle)
```

Always invoke Python with `uv run --prerelease=allow …` — `datasette` is on
a `>=1a23` pre-release pin.
