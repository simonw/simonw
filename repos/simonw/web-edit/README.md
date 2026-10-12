# web-edit

[![PyPI](https://img.shields.io/pypi/v/web-edit.svg)](https://pypi.org/project/web-edit/)
[![Changelog](https://img.shields.io/github/v/release/simonw/web-edit?include_prereleases&label=changelog)](https://github.com/simonw/web-edit/releases)
[![Tests](https://github.com/simonw/web-edit/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/web-edit/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/web-edit/blob/main/LICENSE)

Web app for editing files in a folder.

## Installation

Install this tool using `pip`:

```bash
pip install web-edit
```

Or `uv`:

```bash
uv tool install web-edit
```

Or run directly with `uvx`:

```bash
uvx web-edit --help
```

## Usage

Run `web-edit` in a folder, or pass a path to target another folder:

```bash
uvx web-edit ~/sites/mysite
```

Defaults to `127.0.0.1:9000`. Use `-p/--port` for a different port and `-h/--host` for a different IP, including a Tailscale address. There is no authentication; use on a trusted local network or over Tailscale.

## Features

- Browse folders with inline previews of images smaller than 2 MB.
- Create and edit UTF-8 text files with bundled CodeMirror 6, including on mobile.
- Save explicitly, with unsaved-change warnings and checks for external edits.
- Upload multiple files with custom paths and names, individual progress bars, and retries.
- Download files, or delete files and folders with inline confirmation.

## Development

```bash
uv sync --extra test
uv run web-edit .
uv run pytest
```

After changing `frontend/app.js`, rebuild and commit the bundled JavaScript:

```bash
npm ci
npm run build
```
