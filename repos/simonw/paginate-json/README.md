# paginate-json

[![PyPI](https://img.shields.io/pypi/v/paginate-json.svg)](https://pypi.python.org/pypi/paginate-json)
[![Changelog](https://img.shields.io/github/v/release/simonw/paginate-json?include_prereleases&label=changelog)](https://github.com/simonw/paginate-json/releases)
[![Tests](https://github.com/simonw/paginate-json/workflows/Test/badge.svg)](https://github.com/simonw/paginate-json/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/paginate-json/blob/main/LICENSE)

CLI tool for retrieving JSON from paginated APIs.

This tool works against APIs that use the HTTP Link header for pagination. The GitHub API is [one example of this](https://developer.github.com/v3/guides/traversing-with-pagination/).

Recipes using this tool:

- [Combined release notes from GitHub with jq and paginate-json](https://til.simonwillison.net/jq/combined-github-release-notes)
- [Export a Mastodon timeline to SQLite](https://til.simonwillison.net/mastodon/export-timeline-to-sqlite)

## Installation

```bash
pip install paginate-json
```
Or use [pipx](https://pypa.github.io/pipx/):
```bash
pipx install paginate-json
```

## Usage

Run this tool against a URL that returns a JSON list of items and uses the `link:` HTTP header to indicate the URL of the next page of results.

It will output a single JSON list containing all of the records, across multiple pages.
```bash
paginate-json \
  https://api.github.com/users/simonw/events
```
You can use the `--header` option to send additional request headers. For example, if you have a GitHub OAuth token you can pass it like this:
```bash
paginate-json \
  https://api.github.com/users/simonw/events \
  --header Authorization "bearer e94d9e404d86..."
```
Some APIs may return a root level object where the items you wish to gather are stored in a key, like this example from the [Datasette JSON API](https://docs.datasette.io/en/latest/json_api.html):
```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "name": "San Francisco"
    },
    {
      "id": 2,
      "name": "Los Angeles"
    },
    {
      "id": 3,
      "name": "Detroit"
    },
    {
      "id": 4,
      "name": "Memnonia"
    }
  ]
}
```
In this case, use `--key rows` to specify which key to extract the items from:
```bash
paginate-json \
  https://latest.datasette.io/fixtures/facet_cities.json \
  --key rows
```
The output JSON will be streamed as a pretty-printed JSON array by default.

To switch to newline-delimited JSON, with a separate object on each line, add `--nl`:
```bash
paginate-json \
  https://latest.datasette.io/fixtures/facet_cities.json \
  --key rows \
  --nl
```
The output from that command looks like this:
```
{"id": 1, "name": "San Francisco"}
{"id": 2, "name": "Los Angeles"}
{"id": 3, "name": "Detroit"}
{"id": 4, "name": "Memnonia"}
```



## Using this with sqlite-utils

This tool works well in conjunction with [sqlite-utils](https://github.com/simonw/sqlite-utils). For example, here's how to load all of the GitHub issues for a project into a local SQLite database.
```bash
paginate-json \
  "https://api.github.com/repos/simonw/datasette/issues?state=all&filter=all" \
  --nl | \
  sqlite-utils upsert /tmp/issues.db issues - --nl --pk=id
```
You can then use [other features of sqlite-utils](https://sqlite-utils.readthedocs.io/en/latest/cli.html) to enhance the resulting database. For example, to enable full-text search on the issue title and body columns:
```bash
sqlite-utils enable-fts /tmp/issues.db issues title body
```
## Using jq to transform each page

If you install the optional [jq](https://pypi.org/project/jq/) or [pyjq](https://pypi.org/project/pyjq/) dependency you can also pass `--jq PROGRAM` to transform the results of each page using a [jq program](https://stedolan.github.io/jq/). The `jq` option you supply should transform each page of fetched results into an array of objects.

For example, to extract the `id` and `title` from each issue:
```bash
paginate-json \
  "https://api.github.com/repos/simonw/datasette/issues" \
  --nl \
  --jq 'map({id, title})'
```
If you installed `paginate-json` using `pipx` you can inject the extra dependency into the correct virtual environment like this:
```bash
pipx inject paginate-json jq
```

## paginate-json --help

<!-- [[[cog
import cog
from paginate_json import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: paginate-json")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: paginate-json [OPTIONS] URL

  Fetch paginated JSON from a URL

  Example usage:

      paginate-json https://api.github.com/repos/simonw/datasette/issues

Options:
  --version                Show the version and exit.
  --nl                     Output newline-delimited JSON
  --key TEXT               Top-level key to extract from each page
  --jq TEXT                jq transformation to run on each page
  --accept TEXT            Accept header to send
  --sleep INTEGER          Seconds to delay between requests
  --silent                 Don't show progress on stderr - default
  -v, --verbose            Show progress on stderr
  --show-headers           Dump response headers out to stderr
  --ignore-http-errors     Keep going on non-200 HTTP status codes
  --header <TEXT TEXT>...  Send custom request headers
  --help                   Show this message and exit.

```
<!-- [[[end]]] -->

