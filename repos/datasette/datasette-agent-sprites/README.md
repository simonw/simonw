# datasette-agent-sprites

[![PyPI](https://img.shields.io/pypi/v/datasette-agent-sprites.svg)](https://pypi.org/project/datasette-agent-sprites/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-agent-sprites?include_prereleases&label=changelog)](https://github.com/datasette/datasette-agent-sprites/releases)
[![Tests](https://github.com/datasette/datasette-agent-sprites/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-agent-sprites/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-agent-sprites/blob/main/LICENSE)

Datasette Agent tools for working with [Fly Sprites](https://sprites.dev) - persistent, hardware-isolated Linux environments with a REST API.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-agent-sprites
```

## Configuration

This plugin uses [datasette-secrets](https://github.com/datasette/datasette-secrets) to manage the Sprites API key. You can get a token from <https://sprites.dev/account>.

There are two ways to configure it:

**Using an environment variable:**

```bash
export DATASETTE_SECRETS_SPRITES_API_KEY="your-token-here"
```
Or if you have `datasette-secrets` configured with an encrytion key:

**Using the datasette-secrets UI:** Navigate to `/-/secrets` in your Datasette instance and set the `SPRITES_API_KEY` secret.

## Tools

This plugin provides the following tools to the Datasette Agent:

| Tool | Description |
|------|-------------|
| **list_sprites** | List all available Sprites. Optionally filter by name prefix. |
| **create_sprite** | Create a new Sprite with a given name. It starts cold and warms on first use. |
| **get_sprite** | Get details and status of a specific Sprite. |
| **exec_on_sprite** | Execute a shell command on a Sprite via `bash -lc`. Returns stdout, stderr, and exit code. |
| **delete_sprite** | Permanently delete a Sprite and all its data. |
| **read_sprite_file** | Read a file from a Sprite's filesystem. Images are displayed inline; text files are returned directly. |
| **write_sprite_file** | Write text content to a file on a Sprite. Creates parent directories automatically. |

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-agent-sprites
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
