# datasette-sqlite-history-json

[![PyPI](https://img.shields.io/pypi/v/datasette-sqlite-history-json.svg)](https://pypi.org/project/datasette-sqlite-history-json/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-sqlite-history-json?include_prereleases&label=changelog)](https://github.com/datasette/datasette-sqlite-history-json/releases)
[![Tests](https://github.com/datasette/datasette-sqlite-history-json/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-sqlite-history-json/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-sqlite-history-json/blob/main/LICENSE)

Track changes to data using triggers and hidden JSON tables using [sqlite-history-json](https://github.com/simonw/sqlite-history-json).

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-sqlite-history-json
```
## Usage

Install tracking on a table from Datasette's table actions menu (`Enable tracking`) or access the route directly:

```bash
/-/history-json/<database>/<table>/-/enable
```

Once enabled, the table action menu also shows:

- `View history` → table history page at `/-/history-json/<database>/<table>`
- `Disable tracking` if tracking is already active

On each row in a tracked table, the row action menu now shows:

- `View row history` → `/-/history-json/<database>/<table>/<primary-key>`, with a subtitle showing the number of changes.
- If the table is not tracked, or the user lacks permission, that action does not appear.

## API

All endpoints return JSON for machine access and can be used in scripts:

- Table history: `/-/history-json/<database>/<table>.json`
- Row history: `/-/history-json/<database>/<table>/<primary-key>.json`
- Filter by operation: `?operation=insert|update|delete`

## Permissions

The plugin registers:

- `sqlite-history-json` for enabling/disabling tracking (database-level action)
- `sqlite-history-json-view` for viewing history (table-level action)

`sqlite-history-json-view` is automatically allowed in non-`--default-deny` mode when the actor can `view-table`.

Required permissions by feature:

- Enable tracking: `sqlite-history-json` on `DatabaseResource(database)`
- Disable tracking: `sqlite-history-json` on `DatabaseResource(database)`
- View table history page/action: `sqlite-history-json-view` on `TableResource(database, table)` (plus the implicit `view-table` check)
- View row history action/page: same as table history permission above

In `--default-deny` mode, `sqlite-history-json-view` is not auto-granted. In that case, provide explicit grants for that action in your permission policy (and keep `sqlite-history-json` grants as needed for managing tracking).

## Notes

`<primary-key>` is URL-safe, tilde-encoded values in the same format Datasette uses internally (for example comma-joined values for composite keys).

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-sqlite-history-json
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
