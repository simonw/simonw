# datasette-showboat

[![PyPI](https://img.shields.io/pypi/v/datasette-showboat.svg)](https://pypi.org/project/datasette-showboat/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-showboat?include_prereleases&label=changelog)](https://github.com/simonw/datasette-showboat/releases)
[![Tests](https://github.com/simonw/datasette-showboat/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/datasette-showboat/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-showboat/blob/main/LICENSE)

Datasette plugin that provides a remote viewer for [Showboat](https://github.com/simonw/showboat) documents. It receives streaming document chunks over HTTP and displays them in a live-updating web interface.

See [this blog post](https://simonwillison.net/2026/Feb/17/chartroom-and-datasette-showboat/#datasette-showboat) for background on this project.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-showboat
```

## Usage

Once installed, the plugin adds a `/-/showboat` page to your Datasette instance listing all received documents, and a `/-/showboat/receive` endpoint for ingesting chunks.

### Sending documents

Set the `SHOWBOAT_REMOTE_URL` environment variable to point at your Datasette instance:

```bash
export SHOWBOAT_REMOTE_URL="https://your-datasette-instance/-/showboat/receive"
```

The `/-/showboat` page will display the correct URL for your instance including the hostname.

### Permissions

Viewing showboat documents requires the `showboat` permission. By default this is **denied** to anonymous users — only the root user (when Datasette is started with `--root`) has access automatically.

To grant access to specific users, add to your `datasette.yaml`:

```yaml
permissions:
  showboat:
    id: your-username
```

Or to allow all authenticated users:

```yaml
permissions:
  showboat:
    id: "*"
```

The receive endpoint (`/-/showboat/receive`) does not require the `showboat` permission — it uses token authentication instead (see below).

### Token authentication

To protect the receive endpoint, configure a secret token in your `datasette.yaml` (or `metadata.yaml`):

```yaml
plugins:
  datasette-showboat:
    token: your-secret-token
```

When a token is configured, all requests to `/-/showboat/receive` must include it as a query parameter:

```bash
export SHOWBOAT_REMOTE_URL="https://your-datasette-instance/-/showboat/receive?token=your-secret-token"
```

Without a configured token, the receive endpoint accepts all POST requests.

### Custom database

By default chunks are stored in Datasette's internal database. To use a named database instead:

```yaml
plugins:
  datasette-showboat:
    database: my_database
```

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-showboat
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
