# commit-rewriter

A local Starlette app for editing the latest 100 commit messages reachable from local `main`, including merged commits. The UI is inline HTML, CSS, and dependency-free vanilla JavaScript.

## Run

Requires Git, Python 3.11+, and [uv](https://docs.astral.sh/uv/). From this project's folder:

```sh
uv run commit-rewriter /path/to/repository
```

The optional positional folder defaults to `.`:

```sh
uv run commit-rewriter
```

To run from another directory while using this project's dependencies:

```sh
uv run --project /path/to/commit-rewriter commit-rewriter /path/to/repository
```

Or install the CLI as a uv tool and use it from any repository:

```sh
uv tool install /path/to/commit-rewriter
commit-rewriter
```

Open http://127.0.0.1:8000. Use `--port 8001` to choose another port. Dependencies and the `commit-rewriter` CLI entry point are declared in `pyproject.toml`.

Use a complete, non-bare repository with a local `main` branch and a clean working tree (including untracked files). Keep the script outside the target repository, track it, or ignore it. If `main` is checked out in another worktree, run the app against that worktree.

## Editing

- Jump between commits using the side navigation, with subject previews and edit markers. On narrow screens it becomes a collapsible navigation panel.
- Edit subject and body, search by message/author/hash, or show only edited commits.
- Drafts persist in localStorage, keyed by repository identity and original main tip. Use the same browser, hostname, and port to recover them. Stale drafts remain available to copy, but must be discarded before editing the changed history.
- Empty or whitespace-only messages and NUL characters are blocked in both browser and server. Subjects over 72 characters show a nonblocking warning.
- Review the original/proposed messages, then choose **Back up & rewrite**.
- A progress bar counts affected commits (including descendants), followed by the backup branch and old-to-new hash mapping.

## Preservation and backup

Before writing replacement commits, the app creates `commit-message-backup/<UTC timestamp>-<random suffix>` at the original main tip. It rebuilds affected commits in topological order using raw Git objects, preserving tree hashes, merge parent order, author and committer identities, and both timestamps including timezone offsets **byte for byte**. Unedited messages retain their original bytes. Edited messages use the commit's declared encoding (UTF-8 by default); unsupported or unrepresentable encodings produce an error.

Only `main` moves. Other branches, tags, the index, and working-tree files are not rewritten. Descendant hashes change even when their messages do not. Invalidated `gpgsig`, `gpgsig-sha256`, and merge-tag signature headers are removed. A final compare-and-swap update refuses to overwrite a concurrently changed main. Preparation failures leave main unchanged and any already-created backup available. Nothing is pushed.

The server binds to `127.0.0.1`, checks hostnames, and requires a per-server request token for rewrites. Use one server per repository and avoid other Git operations while applying edits. Progress is kept in server memory; if the process stops, inspect main and the backup branches before retrying. Drafts remain in the browser.

To inspect an old state, use `git show <backup-branch>` or `git switch <backup-branch>`. Restoring main is a separate manual Git operation; the app does not automatically discard later work.

## Tests

The project was started with `uv init --app`.

```sh
uv sync
uv run pytest -q
```

The tests create temporary repositories and cover exact metadata/tree preservation, root and merge rewrites, backup creation, message validation, dirty and stale repositories, failure recovery, concurrent branch changes, the 100-commit limit, and the HTTP workflow and request token.

## Continuous integration

`.github/workflows/tests.yml` runs pytest on pushes, pull requests, and manual dispatches using Ubuntu and Python 3.11, 3.12, 3.13, and 3.14. It resolves and installs the project and test dependencies with `uv sync --dev`, then runs `uv run --no-sync pytest -q`. The workflow follows the [official uv GitHub Actions integration](https://docs.astral.sh/uv/guides/integration/github/) and pins its actions to commit SHAs.

`uv.lock` and `.python-version` are local files excluded from Git. CI selects Python explicitly for each matrix job and resolves dependencies from `pyproject.toml`.
