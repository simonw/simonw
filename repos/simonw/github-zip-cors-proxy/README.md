# github-zip-cors-proxy

A Cloudflare Worker that serves GitHub source zips with CORS headers, so a
Pyodide page such as Datasette Lite can load the exact code from a commit or
pull request.

<details><summary>README by Claude Fable 5.2</summary>

GitHub's own zip downloads (`github.com/.../archive/...zip` and
`codeload.github.com`) send no `Access-Control-Allow-Origin` header, so
browsers refuse to let page JavaScript read them. This Worker fetches the zip
from GitHub and passes it through with that header added.

## URL format

```
GET https://<your-worker>/{owner}/{repo}/{ref}
```

`{ref}` is a branch, a tag or a commit SHA. For example:

```
https://<your-worker>/simonw/datasette/main
https://<your-worker>/simonw/datasette/1.0a19
https://<your-worker>/simonw/datasette/be0ce3e85f3b7d8e811ab01db4f0dc304f09b025
```

The response is the same zip GitHub serves, containing a single top-level
directory named `{repo}-{ref}` (with any `/` in the ref replaced by `-`).

## What it allows

| Rule | Value | Where to change it |
|---|---|---|
| Browser origins | `https://lite.datasette.io`, plus `http://localhost` and `http://127.0.0.1` on any port | `PRODUCTION_ORIGINS` and `LOCALHOST` in `src/index.js` |
| Repository owner | `simonw` | `ALLOWED_OWNER` in `wrangler.toml` |
| Refs | Branches, tags and commit SHAs, up to 200 characters of letters, digits, `.`, `_`, `-` and `/` | `PATH` and `isValidRef` in `src/index.js` |
| Methods | `GET`, `HEAD`, `OPTIONS` | `src/index.js` |

Everything else is refused before any request is made to GitHub:

| Status | Meaning |
|---|---|
| 403 | Missing or disallowed `Origin` header, or a repository owner other than `ALLOWED_OWNER` |
| 400 | Path is not `/{owner}/{repo}/{ref}`, or the ref has disallowed characters |
| 405 | Method other than `GET`, `HEAD` or `OPTIONS` |
| 404 | GitHub has no such repository, branch, tag or commit |
| 502 | GitHub returned some other error |

A full 40-character SHA always names the same content, so those responses are
sent with `Cache-Control: public, max-age=31536000, immutable`. Branches and
tags can move, so those are sent with `Cache-Control: public, max-age=60`.

## Deploy

You need Node.js 18 or later and a Cloudflare account.

```bash
./deploy.sh
```

This runs the tests, logs you in to Cloudflare if needed, and deploys with
`wrangler`. It prints the Worker's `workers.dev` URL. Pass that URL back in to
smoke-test the live Worker:

```bash
./deploy.sh https://github-zip-cors-proxy.YOUR-SUBDOMAIN.workers.dev
```

## Cost

Keep this Worker on an account that uses the **Workers Free** plan. That plan
has a hard limit of 100,000 requests a day; requests over the limit get an
error page until midnight UTC and are never billed. Workers Paid has no such
limit, so on a paid account abuse could cost money.

The origin check does not stop non-browser clients, which can send any
`Origin` header they like. It doesn't need to: all such a client can get is a
zip of a public `simonw` repository, which GitHub serves directly anyway.

## Use from Pyodide

```python
import sys, tomllib, micropip
from pyodide.http import pyfetch

sha = "be0ce3e85f3b7d8e811ab01db4f0dc304f09b025"
resp = await pyfetch(f"https://<your-worker>/simonw/datasette/{sha}")
await resp.unpack_archive(extract_dir="/src", format="zip")

root = f"/src/datasette-{sha}"
with open(f"{root}/pyproject.toml", "rb") as f:
    deps = tomllib.load(f)["project"]["dependencies"]
await micropip.install(deps)
sys.path.insert(0, root)

import datasette
```

Do not add custom request headers to the fetch. A plain `GET` is all the
Worker needs.

## Develop

```bash
npm test          # unit tests, no network or Cloudflare account needed
npx wrangler dev  # run locally on http://localhost:8787
```

To try it locally:

```bash
curl -i -H "Origin: http://localhost:8000" \
  http://localhost:8787/simonw/datasette/be0ce3e85f3b7d8e811ab01db4f0dc304f09b025
```

## Files

- `src/index.js`: the Worker
- `wrangler.toml`: Worker name and `ALLOWED_OWNER`
- `deploy.sh`: test, deploy and smoke-test
- `test/index.test.js`: unit tests

</details>
