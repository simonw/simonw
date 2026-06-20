# datasette-llm-limits

[![PyPI](https://img.shields.io/pypi/v/datasette-llm-limits.svg)](https://pypi.org/project/datasette-llm-limits/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-llm-limits?include_prereleases&label=changelog)](https://github.com/datasette/datasette-llm-limits/releases)
[![Tests](https://github.com/datasette/datasette-llm-limits/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-llm-limits/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-llm-limits/blob/main/LICENSE)

A Datasette plugin for enforcing **windowed spending caps** on LLM usage.

`datasette-llm-limits` plugs into [`datasette-llm-accountant`](https://github.com/datasette/datasette-llm-accountant)
as an `Accountant` implementation, so every prompt issued through `datasette-llm`
is checked against your configured caps before it is allowed to run.

It is designed for the case of **time-windowed caps that reset automatically** —
"no single user may spend more than $1.00 per day", or "the whole instance is
capped at $50 per calendar month".

For a top-up-style refillable balance, see the sibling project
`datasette-llm-allowance`.

## Installation

Install this plugin in the same environment as Datasette:

```bash
datasette install datasette-llm-limits
```

This will also install `datasette-llm-accountant`, which is required.

## Configuration

All configuration lives in `datasette.yaml` under
`plugins.datasette-llm-limits.limits`. Each entry is a named limit; on every
reservation the plugin checks **every matching limit** and rejects the call if
any one would be exceeded.

```yaml
plugins:
  datasette-llm-limits:
    limits:
      # Per-user, rolling 24 hours
      per-user-daily:
        scope: actor
        window: rolling-24h
        amount_usd: 1.00

      # Per-user, calendar month (resets at UTC midnight on day 1)
      per-user-monthly:
        scope: actor
        window: calendar-month
        amount_usd: 20.00

      # Per-actor cap that only applies to one purpose
      enrichments-per-user-daily:
        scope: actor
        window: rolling-24h
        amount_usd: 5.00
        purpose: enrichments

      # Instance-wide cap, any actor, any purpose
      instance-monthly:
        scope: instance
        window: calendar-month
        amount_usd: 250.00

      # Per-model cap (e.g. limit expensive models per actor)
      gpt5-pro-per-user-weekly:
        scope: actor
        window: rolling-7d
        amount_usd: 10.00
        model_id: gpt-5-pro
```

### Field reference

| Field        | Type     | Required | Description |
|--------------|----------|----------|-------------|
| `scope`      | string   | yes      | One of `actor` or `instance`. `actor` partitions usage by `actor_id`; `instance` aggregates across every caller. |
| `window`     | string   | yes      | One of `rolling-24h`, `rolling-7d`, `rolling-30d`, `calendar-day`, `calendar-week`, `calendar-month`. Rolling windows look back N seconds from now. Calendar windows reset at UTC midnight on the appropriate boundary. |
| `amount_usd` | number   | yes      | Cap in US dollars. Stored internally in nanocents. |
| `purpose`    | string   | no       | If set, the limit only applies when the prompt's `purpose` matches. Omit to apply regardless of purpose. |
| `model_id`   | string   | no       | If set, the limit only applies when the prompt's `model_id` matches. Omit to apply regardless of model. |

A limit "matches" a reservation when:

- `purpose` is unset OR equals the prompt's purpose, AND
- `model_id` is unset OR equals the prompt's model id, AND
- `scope` is `instance`, OR (`scope` is `actor` AND the reservation has a
  non-empty `actor_id`).

Reservations made by unauthenticated callers (no `actor_id`) skip any
`scope: actor` limits but still count toward `scope: instance` limits.

### Validation

Configuration is validated at startup. Unknown fields, unknown `scope` or
`window` values, missing required fields, or non-positive `amount_usd` raise
`ValueError` before Datasette starts.

## How rejections look

When a reservation would exceed any matching limit, the call is rejected with an
`InsufficientBalanceError` whose message follows this format:

```
Limit "per-user-daily" exceeded: $0.95 used of $1.00 in rolling-24h.
```

For calendar windows the message also tells the caller when the window resets:

```
Limit "per-user-monthly" exceeded: $19.80 used of $20.00 in calendar-month.
Try again after 2026-04-01T00:00:00Z.
```

`datasette-llm` will surface this message to the end user.

## The `/-/llm-limits` inspection view

The plugin registers a read-only view at `/-/llm-limits` that lists every
configured limit. Instance-scoped limits include their current usage, remaining
headroom, and the time of the next reset (for calendar windows). Actor-scoped
limits show their cap as a per-actor cap, with usage broken out in a separate
actor usage table. The view also shows the 50 most recent transactions.

The view supports both HTML (default) and JSON:

```bash
curl -H "Accept: application/json" http://localhost:8001/-/llm-limits
# or:
curl http://localhost:8001/-/llm-limits?_format=json
```

### Permissions

The view is gated by a plugin-defined permission, `datasette-llm-limits-view`,
which defaults to **deny**. Grant it in `datasette.yaml`:

```yaml
permissions:
  datasette-llm-limits-view:
    id: "*"          # any signed-in actor
    # or: id: ["github:9599"] for specific actor ids
```

Anyone without this permission gets a 403.

## Storage

The plugin keeps its state in Datasette's internal database (the path passed
via `--internal`). On startup it creates an `llm_limits_tx` table that records
every reservation and settlement. Rows for rolled-back transactions remain in
the audit trail with `settled_nanocents = 0`.

```sql
CREATE TABLE llm_limits_tx (
    id TEXT PRIMARY KEY,                -- ULID for monotonic ordering
    created_at TEXT NOT NULL,           -- ISO-8601 UTC
    settled_at TEXT,                    -- ISO-8601 UTC; NULL while reserved
    actor_id TEXT,                      -- NULL for unauthenticated
    purpose TEXT,                       -- NULL when not provided
    model_id TEXT,                      -- NULL when not provided
    reserved_nanocents INTEGER NOT NULL,
    settled_nanocents INTEGER,          -- NULL while reserved
    matched_limits TEXT NOT NULL        -- JSON array of limit names
);
```

If you have `view-database` on `_internal`, you can query `llm_limits_tx`
directly to build your own reports.

## How it fits with `datasette-llm-accountant`

`datasette-llm-limits` does not perform pricing or wrap LLM calls itself — that
is the job of `datasette-llm-accountant`. The accountant calls into this
plugin's `reserve` / `settle` / `rollback` methods, and this plugin enforces
the configured caps.

You may stack multiple accountants: for example, `datasette-llm-allowance` for
a refillable balance plus `datasette-llm-limits` for a daily cap. A prompt only
goes through if **every** registered accountant approves it.

## Development

To set up this plugin locally, check out the code, then:

```bash
cd datasette-llm-limits
# Confirm the plugin is visible
uv run datasette plugins
```

To run the tests:

```bash
uv run pytest
```

To format and lint:

```bash
uv run --with black black --target-version py311 .
uv run --with ruff ruff check .
```
