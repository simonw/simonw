# datasette-charts

[![PyPI](https://img.shields.io/pypi/v/datasette-charts.svg)](https://pypi.org/project/datasette-charts/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-charts?include_prereleases&label=changelog)](https://github.com/datasette/datasette-charts/releases)
[![Tests](https://github.com/datasette/datasette-charts/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-charts/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-charts/blob/main/LICENSE)

Suggests charts for any Datasette table, view or SQL query, and lets you build your own.

This is an early version of the design in [spec.md](spec.md): enough to try the idea out against small tables and queries. See [What is not built yet](#what-is-not-built-yet).

## Requirements

This needs a Datasette newer than 1.0a43: commit `56e02c1` or later, which is not yet in a release. Until it is, run against a checkout of Datasette's `main` branch. From a checkout of this repository:

```bash
uv run --no-project --with-editable ~/dev/datasette --with-editable . datasette content.db
```

`--no-project` matters here. Without it, uv also installs the latest stable Datasette into this project's own environment, and that copy is the one that gets imported.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-charts
```
## Usage

Every table, view and SQL query page gets a **Charts** panel at the top. It shows a row of suggested charts, best first, each with a thumbnail, a title and the reason it was suggested. Select one to see it at full size.

Beside the full-size chart is a builder for changing the chart type, columns, aggregates, time units and bins. "Build a chart" at the end of the row starts from scratch. Anything the plugin can suggest can be built by hand.

The chart you are looking at is kept in the page's URL fragment, so the address bar always holds a link to it.

When nothing is suggested for a table, the panel starts collapsed. Opening it still offers "Build a chart".

Charts never fetch every row. Each one compiles to a SQL query that returns a small, aggregated result, and that query is what "View and edit this chart's SQL" links to.

### Filters and facets

On a filtered table page the charts cover the rows the page shows. Column filters such as `?state=CA` and `?price__gt=5`, `?_search=`, `?_where=` and `?_through=` all apply, and so does anything you click in a facet. The suggestions are worked out again for the filtered rows, so a column that the filter has narrowed to a single value is no longer suggested.

The chart you select stays selected as you filter, facet, sort and page through a table: each new page opens with the same chart, now drawn from that page's rows. Close the chart to stop it coming back. This is remembered per table, in the browser tab.

### Chart types

| Type | Shows | Suggested when |
|------|-------|----------------|
| `histogram` | The distribution of a numeric column, on a log scale when it has a long tail | A measure has spread |
| `bar` | A count or an aggregate for each value of a category: the top N plus "Other" | A category has a workable number of values |
| `line` | A count or an aggregate over time, optionally split into series | A date or timestamp column spans several buckets |
| `scatter` | Two numeric columns: points for small sources, a binned heatmap for large ones | There are two measures |
| `map` | Latitude and longitude: points for small sources, grid cells for large ones | A latitude/longitude pair exists |
| `stacked_bar` | Stacked or grouped bars for two categories, or a category over time | There are two categories |

### How large sources are handled

Suggestions come from a profile of the source: row count, types, distinct counts, top values, ranges and detected dates. Profiling runs inline, under Datasette's SQL time limit.

- A source of up to 50,000 rows (and 1,000,000 cells) is profiled in full.
- A larger one is profiled from a sample of up to 10,000 rows. The panel says so when this happens. Charts still query every row.
- For a table, the sample is spread evenly across its rows. For a view, a query or a filtered table it is the first rows the source returns, which can be less representative.

To let more work happen inline, raise Datasette's time limit and the plugin's limits together:

```bash
datasette data.db --setting sql_time_limit_ms 10000 -c datasette.yaml
```
```yaml
plugins:
  datasette-charts:
    inline_row_limit: 5000000
    inline_cell_limit: 100000000
```

## Configuration

All settings are optional. These are the defaults:

```yaml
plugins:
  datasette-charts:
    max_suggestions: 8
    inline_row_limit: 50000       # profile the whole source up to this many rows...
    inline_cell_limit: 1000000    # ...and this many rows x columns
    sample_rows: 10000            # sample size for larger sources
    temporal_min_match_rate: 0.95 # share of values that must look like dates
    thumbnail_row_limit: 100000   # above this, thumbnails load on hover
    thumbnail_concurrency: 2
    hard_max_rows: 5000           # cap on the rows any chart query returns
    distinct_cap: 1000
    top_values: 20
    profile_budget_ms: null       # default: twice sql_time_limit_ms, at least 5000
    chart_time_limit_ms: null     # default: sql_time_limit_ms
    profile_cache_seconds: 300    # profiles are kept in memory this long
    auto_suggest: true            # false: wait until the panel is opened
```

Dates are detected from values: ISO 8601 dates and datetimes always, and Unix timestamps and years when the column name or declared type also suggests a time. To correct a column, set its kind in table-level configuration, or `false` to say it is not a time:

```yaml
databases:
  shop:
    tables:
      orders:
        plugins:
          datasette-charts:
            temporal:
              shipped: unix_seconds
              build_number: false
```

The kinds are `iso_date`, `iso_datetime`, `unix_seconds`, `unix_ms` and `year`.

## Permissions

- Charts for a table or view need `view-table`. They do not need `execute-sql`.
- Charts for a SQL query need `execute-sql`.
- Charts for a stored query need `view-query`.
- The compiled SQL is only shown to actors with `execute-sql`.

## Command line

```bash
datasette charts suggest data.db orders
datasette charts suggest data.db --sql "select * from orders where state = :s" -p s CA
datasette charts profile data.db orders
```

`suggest` prints the ranked suggestions with the signals behind each score. `profile` prints the facts gathered about each column. Both take `--json`, and `--time-limit-ms 10000` to run with a longer SQL time limit.

## HTTP API

| Endpoint | Returns |
|----------|---------|
| `/-/charts/types.json` | The registered chart types |
| `/<db>/<table>/-/charts/suggest.json` | Suggestions for a table or view |
| `/<db>/-/charts/suggest.json?sql=...` | Suggestions for a SQL query |
| `/<db>/-/charts/data.json?source=...&spec=...` | The rows for one chart |
| `/<db>/-/charts/profile.json?source=...` | The profile of a source |

`source` is a JSON object such as `{"kind": "table", "table": "orders"}` or `{"kind": "query", "sql": "...", "params": {}}`.

A filtered table is a table source with the filters from the table page's query string as pairs: `{"kind": "table", "table": "orders", "filters": [["state", "CA"], ["price__gt", "5"]]}`. The table's own suggestions endpoint takes that query string directly, so `/<db>/<table>/-/charts/suggest.json?state=CA&price__gt=5` means the same rows as the table page with those parameters, and its response includes the `source` to pass to `data.json`.

`spec` is a chart in the JSON format the suggestions use:

```json
{
  "v": 1,
  "type": "line",
  "encoding": {
    "x": {"column": "created_at", "timeUnit": "month"},
    "y": {"aggregate": "count"},
    "series": {"column": "status", "limit": 5, "other": true}
  },
  "options": {}
}
```

## Using charts from Datasette Agent

When [datasette-agent](https://github.com/datasette/datasette-agent) is installed as well, the agent gets two tools:

- `suggest_charts` returns the role of each column and the ranked suggestions for a table, view, stored query or SQL query: the same ones the Charts panel shows.
- `chart` draws a chart in the chat from a spec, and returns the rows it plots to the model so it can comment on them. A spec that does not fit the data comes back as a list of errors for the model to correct.

Both take `database` and one of `table`, `sql` or `query_name`, with optional `filters` for a table (`{"state": "CA", "price__gt": "5"}`) and `params` for a query.

The model writes specs in the same JSON format as the rest of this plugin. It writes no JavaScript, and no SQL unless it charts a query. The description of the `chart` tool is built from the registered chart types, so a chart type added with `register_chart_types` is available to the agent too.

Each chart in the chat has an "Open in the chart builder" link. It opens the table or query page in the agent's panel with that chart selected, where it can be changed. When you change a chart there and then send a message, the agent is told the address of the page, which holds the chart you are looking at.

The tools apply the permissions of whoever is chatting, as listed under [Permissions](#permissions). Charting a table needs `view-table` and not `execute-sql`.

The chart in the chat is not a picture stored with the conversation. It is drawn again from current data each time the conversation is opened.

### Embedding a chart from another plugin

The agent tools are built on a small Python API, which other plugins can use to put a chart on their own pages:

```python
from datasette_charts import api

source = await api.resolve(
    datasette, actor, {"database": "shop", "kind": "table", "table": "orders"}
)
html = api.embed_html(datasette, source, spec)
```

`resolve()` checks the source against what the actor may see. `embed_html()` returns a `<datasette-chart>` element with the script and stylesheet it needs. `api.chart_data()`, `api.suggest()` and `api.chart_path()` return what the HTTP endpoints return, and a link to a chart. This interface is not stable yet.

## Adding chart types

A chart type is a Python class that proposes charts and compiles them to SQL, plus a JavaScript module that draws the result. Other plugins register theirs with the `register_chart_types` hook, which is how the built-in ones are registered too:

```python
from datasette import hookimpl
from datasette_charts import ChartType


class SankeyChart(ChartType):
    name = "sankey"
    ...


@hookimpl
def register_chart_types(datasette):
    return [SankeyChart]
```

The built-in chart types in `datasette_charts/chart_types/` are the reference for now. This interface is not stable yet.

## What is not built yet

From the spec, in rough order of how much it matters:

- **The background full tier and stored profiles.** Nothing is written to the internal database and no background task runs. Profiles are kept in memory for a few minutes. A source too large to profile under the time limit gets suggestions from a sample, or none.
- **The verify stage.** Candidates go straight from propose to rank, so nothing checks whether a time series is flat or two measures are related.
- **Precomputed thumbnails.** Every thumbnail runs its query when it scrolls into view.
- **The snapshot harness, contact sheet and benchmarks.**
- **Magic parameters in stored queries**, such as `:_actor_id`.

The map draws points over a coarse world land outline, which needs no network access. The spec leaves the choice of basemap open.

Charts are drawn with [Observable Plot](https://observablehq.com/plot/), which is bundled along with D3. See `datasette_charts/static/vendor/README.md` for versions and licenses.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-charts
# Confirm the plugin is visible
uv run --no-project --with-editable ~/dev/datasette --with-editable . datasette plugins
```
To run the tests, which also need Datasette's `main` branch for now:
```bash
uv run --no-project --with-editable ~/dev/datasette --with-editable . \
  --with pytest --with pytest-asyncio pytest
```
