# datasette-ip-rate-limit

[![PyPI](https://img.shields.io/pypi/v/datasette-ip-rate-limit.svg)](https://pypi.org/project/datasette-ip-rate-limit/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-ip-rate-limit?include_prereleases&label=changelog)](https://github.com/datasette/datasette-ip-rate-limit/releases)
[![Tests](https://github.com/datasette/datasette-ip-rate-limit/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-ip-rate-limit/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-ip-rate-limit/blob/main/LICENSE)

Rate limit Datasette requests by client IP address.

This plugin is designed for Datasette instances that need a lightweight in-process guard against one client sending too many expensive requests.

## Installation

Install this plugin in the same environment as Datasette.

```bash
datasette install datasette-ip-rate-limit
```

## Configuration

Configure the plugin in `datasette.yaml`:

```yaml
plugins:
  datasette-ip-rate-limit:
    debug: true
    rules:
    - paths:
      - "/*"
      block_seconds: 20
```

This applies rate limiting to every non-debug path and enables
`/-/ip-rate-limit-debug` so you can inspect the current in-memory state.

For a more targeted configuration:

```yaml
plugins:
  datasette-ip-rate-limit:
    max_keys: 10000
    exempt_paths:
    - "/static/*"
    - "/-/turnstile*"
    rules:
    - name: expensive-table-pages
      paths:
      - "/global-power-plants/*"
      - "/legislators/*"
      query_params_min: 2
      window_seconds: 60
      max_requests: 120
      block_seconds: 600
```

This allows each IP address to make 120 matching requests per 60 seconds. If
an IP exceeds that rate, it receives `429 Too Many Requests` responses for 600
seconds with a `Retry-After` header.

The example only applies to matching table pages with at least two query string parameters, so ordinary page views are left alone.

By default, the client IP address is read from the ASGI connection. If
Datasette is running behind a trusted proxy, set `header` to the request header
that proxy uses for the client IP address.

## Options

- `header`: Optional request header used for the client IP instead of the ASGI
  connection address.
- `max_keys`: Maximum number of `(rule, IP)` entries kept in memory. Defaults to `10000`.
- `exempt_paths`: Path patterns that should never be rate limited.
- `rules`: List of rate limit rules. The first matching rule is used.
- `debug`: Set to `true` to enable `/-/ip-rate-limit-debug`, a debug page
  showing the current in-memory rate limit state as pretty-printed JSON. This
  includes client IP addresses, so it should only be enabled while debugging.

Each rule supports:

- `name`: Stable rule name used as part of the in-memory key. Defaults to the rule index.
- `paths`: Path patterns to match. `*` matches any characters.
- `methods`: Optional list of HTTP methods to match.
- `query_params_min`: Optional minimum number of query string parameters required before the rule applies.
- `window_seconds`: Token refill window. Defaults to `60`.
- `max_requests`: Number of requests allowed per window. Defaults to `60`.
- `block_seconds`: How long to block an IP after it exceeds the rate. Defaults to `300`.

## Memory Behavior

The limiter uses a token bucket, not a sliding request log. It stores one small record for each tracked `(rule, IP)` pair: token count, last update time, and optional blocked-until time.

The `max_keys` setting caps the number of tracked records. If more keys are seen, the least recently used keys are evicted. That bounds RAM usage even if a crawler rotates through many IP addresses.

This is intentionally fail-open for evicted keys: if a key is evicted and later appears again, it starts with a fresh bucket.

## Development

To run the tests:

```bash
uv run pytest
```
