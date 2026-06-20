# Preview Server

[![PyPI](https://img.shields.io/pypi/v/preview-server.svg)](https://pypi.org/project/preview-server/)
[![Changelog](https://img.shields.io/github/v/release/simonw/preview-server?include_prereleases&label=changelog)](https://github.com/simonw/preview-server/releases)
[![Tests](https://github.com/simonw/preview-server/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/preview-server/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/preview-server/blob/main/LICENSE)

A Python ASGI web application that proxies incoming requests to ephemeral, per-ref sub-servers from a git repository. The system manages the lifecycle of sub-servers, automatically scaling down idle instances while maintaining request history and detailed status information.

## Unmaintained prototype

This project is an **unmaintained prototype**. Use at your own risk!

## Security Warning

**If you use this server with a GitHub repository that accepts Pull Requests, be aware of the security implications:**

An attacker could submit a PR containing malicious code. Even if the PR is never merged, the commit exists in your repository. If an attacker can craft a URL with that commit hash, they could execute arbitrary code on your server.

**To mitigate this risk, enable hostname signing:**

```bash
# Generate a secret and use it for signing
preview-server ~/my-repo --secret "your-secret-here"

# Generate signed URLs for specific refs
preview-server --sign main --secret "your-secret-here"
# Outputs: main--a1b2c3d4e5f6a7b8c9d0

# Only signed hostnames will be accepted
# http://main--a1b2c3d4e5f6a7b8c9d0.localhost:8000/ - works
# http://main.localhost:8000/ - rejected with 403
```

With signing enabled, only pre-authorized hostnames can access the server, preventing attackers from triggering arbitrary commits.

## Features

- **Per-ref Preview Servers**: Automatic sub-server creation for git branches, tags, and commits
- **Scale-to-Zero**: Idle servers are automatically terminated after a configurable TTL
- **Auto-Pull**: Automatically pull latest branch changes when not accessed recently
- **Signed Hostnames**: Cryptographic signing to restrict access to pre-authorized refs only
- **Request Streaming**: Proxies streaming responses and WebSocket connections without buffering
- **Status Monitoring**: Comprehensive `/-/preview-server` endpoint with server and request metrics
- **Basic Auth**: Optional HTTP Basic authentication protecting all endpoints
- **Graceful Startup**: Requests are queued during sub-server initialization
- **Resilient**: Auto-restart sub-servers on crash (up to 3 attempts)

## Installation

```bash
uv tool install preview-server
```
Or run it directly using `uvx`:

```bash
uvx preview-server --help
```

## Usage

```bash
# Using the CLI command (recommended)
preview-server /path/to/repo [OPTIONS]

# Or with uvx
uvx preview-server /path/to/repo [OPTIONS]

# Or as a module
python -m preview_server.cli /path/to/repo [OPTIONS]
```

### Options

- `-p, --port PORT`: Server port (default: 8000)
- `-h, --host HOST`: Host to bind to (default: 127.0.0.1). Use `0.0.0.0` to listen on all interfaces.
- `--idle-ttl DURATION`: Idle timeout before terminating sub-server (default: 5m)
  - Format: `5m`, `10s`, `2h`, etc.
- `--auto-pull DURATION`: Auto-pull branches if not requested within this duration (disabled by default)
  - Only affects branches (tags and commits are considered immutable)
  - Format: `5m`, `10s`, `2h`, etc.
- `--basic-auth USER:PASS`: Basic auth credentials (optional)
- `--secret SECRET`: Signing secret for hostname verification (optional)
  - When set, only signed hostnames are accepted
  - See [Hostname Signing](#hostname-signing) for details
- `--sign HOSTNAME`: Sign a hostname and print the result (requires --secret)
- `--log-file PATH`: JSON logs output file (default: stderr)
- `-c, --config PATH`: Path to TOML configuration file (optional)
- `--cleanup`: Remove all cached worktrees and repos, then exit
- `--cleanup-yes`: Same as `--cleanup` but skip the confirmation prompt
- `--admin-secret SECRET`: Secret for admin API access (optional)
  - Enables the management API at `/-/preview-server/repos/*`
  - Allows starting the server with no repos configured
  - Forces multi-repo mode even with a single repo
- `--persist-repos PATH`: JSON file path for persisting repo configuration (optional)
  - When set, repo changes made via the admin API are saved to this file
  - On startup, repos are loaded from this file if it exists
- `--base-domain DOMAIN`: Base domain for hostname parsing (default: localhost)
  - Use for custom wildcard domains like `example.com` or `preview.example.com`
  - Enables deployment behind production wildcard DNS records

### Examples

```bash
# Start server on port 8000, default 5-minute idle timeout
preview-server ~/my-repo

# Listen on all interfaces (for Docker, remote access, etc.)
preview-server ~/my-repo -h 0.0.0.0

# Use different port and idle timeout
preview-server ~/my-repo -p 3000 --idle-ttl 10m

# Enable basic auth
preview-server ~/my-repo --basic-auth admin:secret

# Enable auto-pull (pull latest if branch not accessed in 5 minutes)
preview-server ~/my-repo --auto-pull 5m

# Clone from GitHub
preview-server https://github.com/user/repo

# Use a configuration file
preview-server -c config.toml

# Clean up all cached worktrees and repos
preview-server --cleanup
```

## Cleanup

The preview server caches cloned repositories and worktrees in `~/.cache/preview-server/`. Over time, this can accumulate significant disk space.

Use the `--cleanup` flag to remove all cached data:

```bash
preview-server --cleanup
```

This will:
1. Show a summary of what will be deleted (dry run)
2. Display the total disk space to be freed
3. Ask for confirmation before proceeding
4. Remove all worktrees and cached repos

Use `--cleanup-yes` to skip the confirmation prompt (useful for scripts):

```bash
preview-server --cleanup-yes
```

Example output:
```
Cleaning up preview-server cache at /home/user/.cache/preview-server

Worktrees (3):
  - /home/user/.cache/preview-server/worktrees/main (1.0 KB)
  - /home/user/.cache/preview-server/worktrees/develop (1.4 KB)
  - /home/user/.cache/preview-server/worktrees/feature (1.6 KB)
Cached repos (1):
  - /home/user/.cache/preview-server/repos/my-project (33.4 KB)

Total: 37.4 KB

Continue? [y/N] y
Cleanup complete.
```

## Auto-Pull

The auto-pull feature keeps branch previews up-to-date by automatically pulling latest changes when a branch hasn't been accessed recently. This is useful for long-running preview servers where branches may receive updates.

### How It Works

1. When a request comes in for a branch that's already running
2. If the branch hasn't been requested within the `--auto-pull` duration
3. The server fetches and resets the worktree to `origin/<branch>`
4. The request waits for the pull to complete before being proxied

### Key Details

- **Only affects branches**: Tags and commits are considered immutable and are never auto-pulled
- **Disabled by default**: You must explicitly enable with `--auto-pull DURATION`
- **Request waits**: The pull happens synchronously before the request is proxied
- **30-second timeout**: Pull operations timeout after 30 seconds to prevent blocking
- **Handles force pushes**: Uses `git fetch` + `git reset --hard` to handle all updates

### Example

```bash
# Pull latest if branch not accessed in 5 minutes
preview-server ~/my-repo --auto-pull 5m

# Combined with idle timeout (common pattern)
# - Auto-pull after 5 minutes of inactivity
# - Terminate server after 30 minutes of inactivity
preview-server ~/my-repo --auto-pull 5m --idle-ttl 30m
```

## Hostname Signing

Hostname signing restricts which git refs can be previewed by requiring a cryptographic signature in the hostname. This is essential when running against repositories that accept untrusted contributions (like GitHub repos with PRs).

### How It Works

1. Generate a secret and start the server with `--secret`
2. Use `--sign` to generate signed hostnames for authorized refs
3. Only requests with valid signatures are accepted

### Generating Signed Hostnames

```bash
# Generate a signed hostname
preview-server --sign main --secret "your-secret-here"
# Output: main--a1b2c3d4e5f6a7b8c9d0

# For a specific commit
preview-server --sign "backend--a56fd34" --secret "your-secret-here"
# Output: backend--a56fd34--1234abcd5678ef90abcd

# For multi-repo projects
preview-server --sign "frontend--develop" --secret "your-secret-here"
```

### Running with Signing Enabled

```bash
# Start server with signing secret
preview-server ~/my-repo --secret "your-secret-here"

# Valid requests (with signature)
curl http://main--a1b2c3d4e5f6a7b8c9d0.localhost:8000/

# Invalid requests (rejected with 403)
curl http://main.localhost:8000/
curl http://main--wrongsig.localhost:8000/
```

### Signature Format

- Signatures are 20-character lowercase hex strings appended after `--`
- Example: `main--a1b2c3d4e5f6a7b8c9d0`
- Uses only subdomain-safe characters: `0-9` and `a-f`
- The signature is an HMAC-SHA256 truncated to 80 bits

### Config File

```toml
# Enable signing via config file
secret = "your-secret-here"
```

## Configuration File

You can use a TOML configuration file instead of (or in addition to) command-line arguments.

### CLI and Config File Merging

When using both a config file and CLI arguments, they are merged together:

- **CLI arguments override config file values** - If both specify the same option, CLI wins
- **CLI arguments add to config file** - Options only in CLI are added to config settings
- **Config values are preserved** - Options only in config file are kept

This allows you to keep common settings in a config file and override specific options via CLI:

```bash
# Config file has repo, port, idle-ttl
# CLI adds --secret (not in config) and overrides port
preview-server -c config.toml --port 9000 --secret mysecret
```

### Config File Format

Create a file named `config.toml` (or any name you prefer):

```toml
# Server port (default: 8000)
port = 8000

# Host to bind to (default: 127.0.0.1)
# Use "0.0.0.0" to listen on all interfaces
host = "0.0.0.0"

# Idle timeout before terminating sub-server (default: 5m)
# Format: "5m", "10s", "2h", etc.
idle-ttl = "10m"

# Auto-pull branches if not requested within this duration (disabled by default)
# Only affects branches; tags and commits are considered immutable
# Format: "5m", "10s", "2h", etc.
auto-pull = "5m"

# Basic auth credentials (optional)
# Format: "username:password"
basic-auth = "admin:secret"

# Signing secret for hostname verification (optional)
# When set, only signed hostnames are accepted
secret = "your-secret-here"

# JSON logs output file (default: stderr)
log-file = "/var/log/preview-server.log"

# Admin API secret (optional)
# Enables the management API at /-/preview-server/repos/*
admin-secret = "your-admin-secret"

# Persistence file for repo configuration (optional)
# When set, repo changes are saved to this file
persist-repos = "/var/lib/preview-server/repos.json"

# Base domain for hostname parsing (default: localhost)
# Use for custom wildcard domains like example.com
base-domain = "preview.example.com"

# Single repo mode (backwards compatible)
repo = "/path/to/repo"
```

All fields are optional. Missing values use defaults or CLI arguments.

**Note:** This feature requires Python 3.11+ (for the `tomllib` standard library module).

## Multi-Repo Mode

You can serve multiple repositories from a single preview server instance. There are two ways to configure multi-repo mode:

### Via Command Line

Use `label:path` syntax for each repository:

```bash
# Multiple local repos
preview-server frontend:/path/to/frontend backend:/path/to/backend

# Multiple GitHub repos
preview-server api:https://github.com/org/api web:https://github.com/org/web

# Mix of local and remote
preview-server frontend:~/dev/frontend backend:https://github.com/org/backend
```

### Via Config File

Use the `[repos]` section in your config file:

```toml
port = 8000
idle-ttl = "10m"

[repos]
frontend = "/path/to/frontend"
backend = "https://github.com/org/backend"
api = "git@github.com:org/api.git"
```

### Hostname Format

In multi-repo mode, the hostname format changes to include the project name:

- `project.localhost:8000` - Uses the default branch (main)
- `project--branch.localhost:8000` - Uses a specific branch

### Custom Domains

The server supports custom wildcard domains in addition to `*.localhost`. Use the `--base-domain` option:

```bash
# Use a custom domain
preview-server ~/my-repo --base-domain example.com

# Access via custom domain (requires wildcard DNS)
curl http://main.example.com:8000/
curl http://feature-branch.example.com:8000/

# Multi-repo with custom domain
preview-server frontend:/path/a backend:/path/b --base-domain preview.example.com
curl http://frontend--main.preview.example.com:8000/
```

This allows deployment behind a wildcard DNS record (e.g., `*.preview.example.com`) for production use cases where `.localhost` isn't suitable.

### Examples

```bash
# Start with multi-repo config file
preview-server -c config.toml

# Or via command line
preview-server frontend:/path/to/frontend backend:/path/to/backend -p 8000

# Access different projects and branches:
curl http://frontend.localhost:8000/           # frontend, main branch
curl http://frontend--develop.localhost:8000/  # frontend, develop branch
curl http://backend--feature.localhost:8000/   # backend, feature branch
curl http://api.localhost:8000/                # api, main branch
```

The `--` separator allows branch names to contain dots and other characters that would otherwise conflict with the hostname pattern.

## Status Endpoints

### HTML Dashboard: `GET /-/preview-server`

Access `http://localhost:8000/-/preview-server` (or your configured port) for an interactive dashboard that shows:
- Server status with color-coded indicators
- Running sub-servers in card layout
- Server details: port, PID, uptime, restart count, idle countdown
- Expandable details with command and recent logs (up to 100 lines)
- **Stream logs toggle**: Enable 1-second polling for live log updates (newest first)
- Responsive design with modern styling

### JSON API: `GET /-/preview-server.json`

For programmatic access, use `http://localhost:8000/-/preview-server.json` to get:
```json
{
  "status": "ok",
  "running_servers": 1,
  "idle_ttl_seconds": 300.0,
  "sub_servers": [
    {
      "ref": "main",
      "port": 53153,
      "pid": 24586,
      "uptime_seconds": 120,
      "restart_attempts": 0,
      "command": "./server.sh",
      "last_request_seconds_ago": 10.5,
      "idle_ttl_seconds": 300.0,
      "seconds_until_idle": 289.5,
      "recent_logs": [
        "[2024-12-20 10:30:45] [STARTUP] Started on port 53153",
        "[2024-12-20 10:30:46] Server listening..."
      ]
    }
  ]
}
```

## Repository Configuration

Each repository must contain a `server.sh` script in its root directory. This script is executed with the `PORT` environment variable set to the allocated port.

```bash
#!/bin/bash
# server.sh - starts your web server on $PORT
npm run dev -- --port $PORT
```

The `server.sh` approach is technology-agnostic - it works with any language or framework that can start an HTTP server on a specified port.

### Examples

**Node.js (Vite/React/Next.js):**
```bash
#!/bin/bash
npm install
npm run dev -- --port $PORT
```

**Python (Flask):**
```bash
#!/bin/bash
pip install -r requirements.txt
python app.py
```

```python
# app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Flask!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

**Python (FastAPI with uv):**
```bash
#!/bin/bash
uv run fastapi run app.py --port $PORT
```

**Go:**
```bash
#!/bin/bash
go run main.go
```

**Ruby (Rails):**
```bash
#!/bin/bash
bundle install
bin/rails server -p $PORT
```

## Admin API

The admin API enables runtime management of repositories without restarting the server. This is useful for adding new repos, removing existing ones, or temporarily pausing traffic to specific repos.

### Enabling the Admin API

Start the server with the `--admin-secret` option:

```bash
# Enable admin API
preview-server --admin-secret "your-secret-here"

# Start with no repos (configure at runtime)
preview-server --admin-secret "your-secret-here"

# Persist changes to a JSON file
preview-server --admin-secret "your-secret-here" --persist-repos /var/lib/preview-server/repos.json
```

### API Endpoints

All endpoints require the `x-api-secret` header with the admin secret.

| Endpoint | Method | Body | Description |
|----------|--------|------|-------------|
| `/-/preview-server/auth-check` | POST | - | Verify the admin secret is valid |
| `/-/preview-server/repos/add` | POST | `{"label": "...", "path": "..."}` | Add a new repo |
| `/-/preview-server/repos/remove` | POST | `{"label": "..."}` | Remove a repo |
| `/-/preview-server/repos/pause` | POST | `{"label": "..."}` | Pause traffic to a repo (returns 503) |
| `/-/preview-server/repos/resume` | POST | `{"label": "..."}` | Resume traffic to a paused repo |

### Examples

```bash
# Check authentication
curl -X POST http://localhost:8000/-/preview-server/auth-check \
  -H "x-api-secret: your-secret-here"
# Returns: {"ok": true}

# Add a new repository
curl -X POST http://localhost:8000/-/preview-server/repos/add \
  -H "x-api-secret: your-secret-here" \
  -H "Content-Type: application/json" \
  -d '{"label": "frontend", "path": "/path/to/frontend"}'
# Returns: {"ok": true, "label": "frontend"}

# Pause a repository (traffic returns 503)
curl -X POST http://localhost:8000/-/preview-server/repos/pause \
  -H "x-api-secret: your-secret-here" \
  -H "Content-Type: application/json" \
  -d '{"label": "frontend"}'
# Returns: {"ok": true}

# Resume a paused repository
curl -X POST http://localhost:8000/-/preview-server/repos/resume \
  -H "x-api-secret: your-secret-here" \
  -H "Content-Type: application/json" \
  -d '{"label": "frontend"}'
# Returns: {"ok": true}

# Remove a repository
curl -X POST http://localhost:8000/-/preview-server/repos/remove \
  -H "x-api-secret: your-secret-here" \
  -H "Content-Type: application/json" \
  -d '{"label": "frontend"}'
# Returns: {"ok": true}
```

### Web UI

When the admin API is enabled, the status dashboard at `/-/preview-server` includes a "Configuration" section where you can:

- Authenticate with the admin secret
- View all configured repositories with their pause status
- Pause/resume individual repositories
- Add new repositories
- Remove repositories

The UI stores the admin secret in `localStorage` (persists across browser sessions) and remembers the configuration section's open/closed state in `localStorage`.

### Persistence

By default, repository changes are stored in memory and lost when the server restarts. Use `--persist-repos` to save changes to a JSON file:

```bash
preview-server --admin-secret "secret" --persist-repos /var/lib/preview-server/repos.json
```

The persistence file format:
```json
{
  "repos": [
    {"label": "frontend", "path": "/path/to/frontend", "paused": false},
    {"label": "backend", "path": "https://github.com/org/backend", "paused": true}
  ]
}
```

On startup, if the persistence file exists, repos are loaded from it (ignoring any repos specified on the command line). Changes made via the API are automatically saved.

## Development

Run tests:

```bash
uv run pytest -v
```

## Architecture

The server consists of several key components:

- **Main ASGI Server**: Routes requests based on hostname subdomain
- **Sub-Server Manager**: Manages process lifecycle and resource cleanup
- **Git Manager**: Handles repository cloning, pulling, and ref resolution
- **Status Tracker**: Tracks request metrics and server health

## Testing

Tests use pytest with async support. Each feature implements Test-Driven Development:

1. Write test case (red)
2. Implement feature (green)
3. Commit with passing tests and README update

## Quick Start

```bash
# Start the preview server
preview-server ~/path/to/your/repo -p 3000

# In another terminal, test it
curl http://localhost:3000/-/preview-server

# Access a preview deployment for a specific branch
# (requires setting up .localhost DNS resolution on your system)
curl http://main.localhost:3000/
```

<details>
<summary>Implementation Status</summary>


- [x] Phase 1: CLI argument parsing and git setup (COMPLETE)
  - [x] CLI argument parsing
  - [x] Duration parsing
  - [x] Port selection
  - [x] Git repository initialization and cloning
- [x] Phase 2: ASGI app and request routing (COMPLETE)
  - [x] ASGI application with Starlette
  - [x] Request routing by hostname subdomain
  - [x] HTTP request proxying to sub-servers
  - [x] CLI entry point with uvicorn
  - [x] Sub-server manager with process lifecycle
  - [x] Remote git branch handling
  - [x] Fallback process startup methods
- [x] Phase 3: Status Endpoints (COMPLETE)
  - [x] JSON API at /-/preview-server.json
  - [x] HTML dashboard at /-/preview-server
  - [x] Auto-refreshing status display
  - [x] Comprehensive test coverage
- [x] Phase 4: Dynamic git pulls on unknown refs (COMPLETE)
- [x] Phase 5: Idle timeout and scale-to-zero (COMPLETE)
- [x] Phase 6: Basic authentication (COMPLETE)
  - [x] HTTP Basic auth protecting all endpoints
  - [x] Constant-time credential comparison (timing attack protection)
  - [x] Proper 401 responses with WWW-Authenticate header
  - [x] Comprehensive test coverage (30 tests)
- [x] Phase 7: Proxy headers (COMPLETE)
  - [x] X-Forwarded-For header chain
  - [x] X-Forwarded-Host header
  - [x] X-Forwarded-Proto header
  - [x] X-Real-IP header
- [x] Phase 8: Streaming and WebSocket support (COMPLETE)
  - [x] Stream request body (no buffering for large uploads)
  - [x] Stream response body (already implemented)
  - [x] WebSocket proxy with bidirectional message relay
  - [x] WebSocket authentication via query token parameter
  - [x] Comprehensive test coverage (22 tests)
- [x] Phase 9: Auto-pull for branches (COMPLETE)
  - [x] CLI --auto-pull argument with duration format
  - [x] TOML config file support for auto-pull
  - [x] Branch detection (distinguishes branches from tags/commits)
  - [x] Automatic git fetch + reset on stale branches
  - [x] 30-second timeout for pull operations
  - [x] Multi-repo mode support
- [x] Phase 10: Hostname Signing (COMPLETE)
  - [x] CLI --secret and --sign arguments
  - [x] TOML config file support for secret
  - [x] HMAC-SHA256 signature generation with lowercase hex encoding (subdomain-safe)
  - [x] Constant-time signature verification (timing attack protection)
  - [x] 403 rejection for invalid/missing signatures
  - [x] Comprehensive test coverage
- [x] Phase 11: Admin API (COMPLETE)
  - [x] CLI --admin-secret and --persist-repos arguments
  - [x] TOML config file support for admin-secret and persist-repos
  - [x] Runtime repo add/remove/pause/resume via REST API
  - [x] JSON file persistence for repo configuration
  - [x] Web UI for repo management in status dashboard
  - [x] Constant-time admin secret verification (timing attack protection)
  - [x] Comprehensive test coverage (34 tests)

</details>
