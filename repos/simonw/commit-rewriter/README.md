# commit-rewriter

[![PyPI](https://img.shields.io/pypi/v/commit-rewriter.svg)](https://pypi.org/project/commit-rewriter/)
[![Changelog](https://img.shields.io/github/v/release/simonw/commit-rewriter?include_prereleases&label=changelog)](https://github.com/simonw/commit-rewriter/releases)
[![Tests](https://github.com/simonw/commit-rewriter/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/commit-rewriter/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/commit-rewriter/blob/master/LICENSE)

Local web app for editing local commit messages to a Git repository.

## Usage

```bash
uvx commit-rewriter /path/to/repository
```
Or omit the path if the repository is your current working directory.

Defaults to running on `http://127.0.0.1:8000` - use `-p/--port 8002` to run on a different port.

Edit multiple commit messages using the web UI. When you apply them the tool will first create a branch to back up the repository prior to making the changes.

## Installation

```bash
pip install commit-rewriter
# or
uv tool install commit-rewriter
```

## Screenshot

![Screenshot of the commit-rewriter web interface. A heading reads commit-rewriter above the repository path and current branch and commit hash, with a short description of the tool. A toolbar shows a pending edits count with Discard drafts and Rewrite commit messages buttons, followed by a search box for message, author, or hash and an Edited only checkbox. A left sidebar titled Navigate commits lists recent commit messages with their short hashes. The main panel shows a card for each commit with its hash, author and timestamp, an editable text area containing the commit message, and a View full formatted diff toggle.](https://raw.githubusercontent.com/simonw/commit-rewriter/refs/heads/main/screenshot.webp)

## Contributing

To run the tests:
```bash
uv run pytest
```
To re-take the screenshot using [shot-scraper](https://shot-scraper.datasette.io/):
```bash
shot-scraper multi shots.yml
```
