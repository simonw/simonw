# datasette-auth-tailscale

[![PyPI](https://img.shields.io/pypi/v/datasette-auth-tailscale.svg)](https://pypi.org/project/datasette-auth-tailscale/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-auth-tailscale?include_prereleases&label=changelog)](https://github.com/datasette/datasette-auth-tailscale/releases)
[![Tests](https://github.com/datasette/datasette-auth-tailscale/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-auth-tailscale/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-auth-tailscale/blob/main/LICENSE)

Configure access to a Datasette instance with Tailscale

> [!WARNING]
> This is pre-alpha software that has not been thoroughly tested or reviewed yet!

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-auth-tailscale
```
## Usage

This plugin authenticates Datasette users from the identity headers that
[Tailscale Serve](https://tailscale.com/kb/1242/tailscale-serve) injects when
proxying tailnet traffic to a backend.

Run Datasette behind `tailscale serve`, listening only on localhost:

```bash
datasette mydata.db --host 127.0.0.1 --port 8001
tailscale serve --https=443 http://127.0.0.1:8001
```

> [!WARNING]
> **Bind Datasette to localhost.** These headers are trusted unconditionally —
> Tailscale strips them from incoming requests before adding its own, but only
> for requests that actually arrive via Serve. If Datasette is reachable from
> your LAN or tailnet directly, anyone can spoof the headers and impersonate
> any user. Always bind to `127.0.0.1` (or the loopback interface) so the only
> path to Datasette is through Serve.
>
> Tailscale Funnel does **not** include identity headers. Funnel users will be
> rejected by default (see `require_tailscale` below).

### Actor shape

A request from `alice@example.com` produces an actor like:

```json
{
  "id": "alice@example.com",
  "display": "Alice Architect",
  "picture": "https://example.com/alice.jpg",
}
```

- `id` — `Tailscale-User-Login`
- `display` — `Tailscale-User-Name` (omitted if not present)
- `picture` — `Tailscale-User-Profile-Pic` (omitted if not present)

### Configuration

Configure under `plugins.datasette-auth-tailscale` in `datasette.yaml`:

```yaml
plugins:
  datasette-auth-tailscale:
    require_tailscale: true
```
