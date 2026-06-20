# datasette-turnstile

[![PyPI](https://img.shields.io/pypi/v/datasette-turnstile.svg)](https://pypi.org/project/datasette-turnstile/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-turnstile?include_prereleases&label=changelog)](https://github.com/simonw/datasette-turnstile/releases)
[![Tests](https://github.com/simonw/datasette-turnstile/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/datasette-turnstile/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-turnstile/blob/main/LICENSE)

Protect Datasette paths with Cloudflare Turnstile challenges.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-turnstile
```

## Configuration

Configure the plugin in your `datasette.yaml`:

```yaml
plugins:
  datasette-turnstile:
    site_key: "0x4AAAAAAxxxxxxxxxxxxxxx"
    secret_key:
      $env: TURNSTILE_SECRET_KEY
    protected_paths:
      - "/admin/*"
      - "/-/import-*"
    exclude_patterns:
      - "*.json"
    cookie_max_age: 86400
```

### Configuration options

- **`site_key`** (required): Your Turnstile site key from the Cloudflare dashboard
- **`secret_key`** (required): Your Turnstile secret key (supports `$env` syntax)
- **`protected_paths`** (required): List of URL patterns to protect
- **`exclude_patterns`** (optional): Patterns to exclude from protection (e.g., `*.json`)
- **`cookie_max_age`** (optional): Cookie lifetime in seconds (default: 86400 = 24 hours)
- **`cookie_name`** (optional): Name of the verification cookie (default: `ds_turnstile`)

### URL Pattern Matching

Patterns use simple wildcard matching where `*` matches any characters:

- `/admin/*` - Protects all paths under `/admin/`
- `/-/import-*` - Protects `/-/import-csv`, `/-/import-json`, etc.

Use `?` in patterns to match against the full URL including query string. Without `?`, patterns only match the path.

#### Protecting URLs with query string parameters

The `?` and `&` characters in patterns match literal `?` and `&` in URLs. This lets you protect pages based on the shape of their query string — useful for blocking automated crawlers that probe expensive API endpoints while leaving simple page views unprotected.

- `/db/*?*&*` - Protects any table page with 2+ query string parameters (e.g. `/db/table?_sort=col&_size=100`)
- `/db?sql=*` - Protects the arbitrary SQL query interface (note: only matches when `sql=` is the first parameter)

A real-world example from [datasette.io](https://datasette.io/):

```yaml
protected_paths:
  # Arbitrary SQL execution
  - "/content?sql=*"
  - "/content.json?sql=*"

  # Multi-parameter table/API URLs (crawlers love these)
  - "/content/*?*&*"
  - "/content/*.json?*&*"
  - "/legislators/*?*&*"
  - "/legislators/*.json?*&*"
```

This protects expensive multi-facet queries like `/legislators/legislators?_facet=party&_facet=state` while leaving simple single-parameter pages like `/legislators/legislators?_sort=name` accessible without a challenge.

## How It Works

1. When a user visits a protected path, they're redirected to `/-/turnstile`
2. The challenge page displays a Cloudflare Turnstile widget
3. Upon completing the challenge, the token is verified server-side
4. On success, a signed cookie is set and the user is redirected to their original destination
5. The cookie remains valid for 24 hours (configurable)

### API Requests

For requests with `Accept: application/json` header, the plugin returns a 403 JSON response instead of redirecting:

```json
{"error": "turnstile_required"}
```

Use `exclude_patterns: ["*.json"]` to exclude JSON endpoints from protection entirely.

## Development

To set up this plugin locally, first checkout the code:
```bash
cd datasette-turnstile
```

To run the tests:
```bash
uv run pytest
```

Create a config file using [Turnstile test keys](https://developers.cloudflare.com/turnstile/troubleshooting/testing/):
```bash
cat > datasette.yaml << 'EOF'
plugins:
  datasette-turnstile:
    site_key: "1x00000000000000000000AA"
    secret_key:
      $env: TURNSTILE_SECRET_KEY
    protected_paths:
      - "/demo/example*
EOF
```
Create an example database:
```bash
sqlite3 demo.db "CREATE TABLE example (id INTEGER PRIMARY KEY, name TEXT);"
```

Put the secret in an environment variable and run Datasette with the plugin:
```bash
TURNSTILE_SECRET_KEY='1x0000000000000000000000000000000AA' uv run datasette -c datasette.yaml demo.db
```
