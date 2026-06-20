# datasette-tailscale

[![PyPI](https://img.shields.io/pypi/v/datasette-tailscale.svg)](https://pypi.org/project/datasette-tailscale/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-tailscale?include_prereleases&label=changelog)](https://github.com/datasette/datasette-tailscale/releases)
[![Tests](https://github.com/datasette/datasette-tailscale/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-tailscale/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-tailscale/blob/main/LICENSE)

Run a Datasette instance on a [Tailscale](https://tailscale.com/) network

> [!WARNING]
> This is an *experimental alpha* plugin. The underlying library it uses ([tailscale-rs](https://github.com/tailscale/tailscale-rs#tailscale-rs)) is also experimental and carries no security guarantees.

This plugin adds a `datasette tailscale` command that serves Datasette as its
own node on your [Tailscale](https://tailscale.com/) tailnet. Datasette itself
binds only to `127.0.0.1` — a userspace Tailscale node is the sole way in, so
the instance is reachable only by other devices on your tailnet and never from
the public internet or your local network.

It uses the [tailscale-py](https://pypi.org/project/tailscale-py/) package
(Python bindings for `tailscale-rs`), so there's no `tailscaled` daemon to run
and no root privileges required.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-tailscale
```
## Usage

Generate a [Tailscale auth key](https://login.tailscale.com/admin/settings/keys)
(an ephemeral, reusable key is a good choice). These settings for the key work well:

![Screenshot of a Tailscale "Generate auth key" modal dialog. Title: "Generate auth key" with a close (X) button. Description section: "Add an optional description for the key." with a text field containing "datasette-tailscale dev". Reusable: toggle on (blue), "Use this key to authenticate more than one device." Expiration: "Number of days until this auth key expires. This will not affect the node key expiry of any machine authenticated with this auth key." A number input set to "1" with minus and plus buttons and a "days" label. Below: "Must be between 1 and 90 days." DEVICE SETTINGS section: "These settings will apply to any devices authenticated using this key." Ephemeral: toggle on (blue), "Devices authenticated by this key will be automatically removed after going offline. Learn more" Tags: toggle off (gray), "Devices authenticated by this key will be automatically tagged. This will also disable node key expiry for the device. Learn more" Buttons at bottom: "Cancel" and "Generate key".](https://raw.githubusercontent.com/datasette/datasette-tailscale/refs/heads/main/tailscale-auth-key.png)

Serve a database like this:

```bash
datasette tailscale mydata.db --ts-authkey tskey-auth-xxxx
```

You can also supply the key via the `TS_AUTHKEY` environment variable:

```bash
export TS_AUTHKEY=tskey-auth-xxxx
datasette tailscale mydata.db
```

If you omit the auth key entirely, an interactive login URL is printed on first
run for you to click.

Once it connects you'll see:

```
Connected. Tailnet IPv4: 100.x.y.z
Serving Datasette at http://datasette (reachable only on your tailnet)
```

Any other device on your tailnet can now reach it at `http://datasette/` (via
MagicDNS) or by its tailnet IP.

### Options

The command accepts **all** the options that `datasette serve` accepts —
`-m/--metadata`, `--setting`, `--root`, `--immutable`, `--cors`, etc. — because
they are inherited dynamically from `datasette serve` at runtime. (The
`--host`, `--port`, `--reload`, `--uds`, `--get`, `--open` and `--ssl-*`
options are suppressed, since they don't apply when serving over a tailnet.)

In addition it adds these tailscale-specific options:

- `--ts-hostname` — the hostname this node registers as on your tailnet
  (default: `datasette`).
- `--ts-authkey` — your Tailscale auth key (or set `TS_AUTHKEY`). If omitted, an
  interactive login URL is printed on first run.
- `--ts-state-dir` — directory for persisting the tailnet node identity across
  restarts (default: `$XDG_STATE_HOME/datasette-tailscale`). A persistent state
  directory gives the node a stable identity; an ephemeral auth key lets the
  node disappear from your tailnet when the process exits.
- `--ts-port` — the port to listen on over the tailnet (default: `80`).

### HTTPS and security notes

Traffic between tailnet devices is end-to-end encrypted by WireGuard, so this
plugin serves plain **HTTP** over the tailnet rather than terminating TLS. The
URL is `http://`, but the wire is still encrypted.

`tailscale-rs` is early-stage, experimental software with unvalidated
cryptography. The plugin sets the `TS_RS_EXPERIMENT=this_is_unstable_software`
acknowledgement on your behalf and prints a warning. Use it only on a tailnet
you trust.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-tailscale
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
