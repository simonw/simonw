# datasette-charts

[![PyPI](https://img.shields.io/pypi/v/datasette-charts.svg)](https://pypi.org/project/datasette-charts/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-charts?include_prereleases&label=changelog)](https://github.com/datasette/datasette-charts/releases)
[![Tests](https://github.com/datasette/datasette-charts/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-charts/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-charts/blob/main/LICENSE)

Suggests charts for any Datasette table, view or SQL query, and lets you build your own.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-charts
```
## Screenshot

![A vertical bar chart of total capacity_mw by decade from 1950 to 2010, with three annotations. A gray shaded range covers 1950 through 1990, labeled "Much smaller summed capacity in earlier decades": those bars run from 80.9K to 446.4K. A dashed horizontal line labeled "1,000,000 MW reference" crosses the chart, level with the top of the 2010 bar at 1M. A callout with a dot on the tallest bar, 2000 at 1.2M, reads "Largest decade total in these records: 1.157 million MW". A caption under the chart reads "Global plant records with commissioning years 1950–2019; coverage and missing years may affect comparisons."](https://raw.githubusercontent.com/datasette/datasette-charts/main/chart-with-annotations.webp)

## Usage

Every table, view and SQL query page gets a **Suggested charts** panel at the top. It shows a row of charts, best first, each with a thumbnail, a title and the reason it was suggested. Select one to see it at full size.

Beside the full-size chart is a builder for changing the chart type, columns, aggregates, time units and bins. "Build a chart" at the end of the row starts from scratch. Anything the plugin can suggest can be built by hand.

The chart you are looking at is kept in the page's URL fragment, so the address bar always holds a link to it.

Charts never fetch every row. Each one compiles to a SQL query that returns a small, aggregated result, available through the "This chart's SQL" link.

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

### Annotations

A chart can carry notes: a dashed line where a rule changed, a target line, a shaded range for a recession, a callout on one data point or a free-floating note. In the builder, **Annotations** lists them, with buttons to add, edit and remove them. Editing one opens a dialog with a live preview of the chart. The dialog is Datasette's own `<datasette-modal>`.

Annotations are part of the chart's spec, so they are kept in the `#chart=` link, drawn by `<datasette-chart>` embeds and written by Datasette Agent. They change nothing about the chart's SQL. They are listed under `annotations`:

```json
{
  "v": 1,
  "type": "bar",
  "encoding": {
    "x": {"column": "year", "sort": "key", "limit": 50, "other": false},
    "y": {"column": "delays", "aggregate": "sum"}
  },
  "options": {"orientation": "vertical"},
  "annotations": [
    {"type": "line", "x": 2009, "position": "after", "text": "Tarmac delay rule enacted"}
  ]
}
```

| Type | Example | Draws |
|------|---------|-------|
| `line` at x | `{"type": "line", "x": 2009, "position": "after", "text": "Rule enacted"}` | A line across the chart at an x value |
| `line` at y | `{"type": "line", "y": 100, "text": "Target", "stroke": "solid"}` | A line at a y value, such as a threshold |
| `range` | `{"type": "range", "x": "2007-12", "x2": "2009-06", "text": "Recession"}` | A shaded band between two x values, or `y` and `y2` |
| `point` | `{"type": "point", "x": "2020-04", "text": "Pandemic spike"}` | A callout on a data point, with a dot and a line to the text |
| `text` | `{"type": "text", "left": 0.02, "top": 0.05, "text": "Source: FAA"}` | A note placed by fractions of the plot area |

- `x` and `y` are the spec's own x and y channels. On a horizontal bar chart x is the category axis, down the side, so a line at an x value there is horizontal.
- x values are written the way the chart shows them: a category, a year (`2009`), a month (`"2009-06"`), a date or time (`"2009-06-15"`, `"2009-06-15T10:30"`), or a number.
- `position` places a line at an x category or time: `before`, `center` or `after`. Before or after a category puts the line between it and its neighbour. On a time axis a value names a period, and the line goes at its start (the default), middle or end: `"x": 2009, "position": "after"` is the end of 2009.
- A `range` over categories or periods covers both ends whole.
- A `point` with no `y` uses the chart's own value at x. `series` picks a series on a line or stacked bar chart. Scatter plots need `y`.
- Every annotation's label is laid out together with the others, in one of three ways picked each time the chart is drawn, including when it is resized. No label is ever drawn over the data or another label, and text is wrapped at word boundaries, never cut short.
  1. **Beside what it labels**, when every label fits there clear of the data, the other labels and the edges of the plot, and callouts read in the same order as their points.
  2. **In lanes**, when they do not. Labels for callouts, ranges and lines across the x axis move to a band above the plot, in order along the axis, each with a thin leader to what it labels; labels on lines and ranges across the y axis that still fit stay where they are, and the rest go in a column at the right (on a flat bar chart the two swap). The chart grows to make room rather than drawing over the data. At most 3 lanes above (2 at the side), and the band may add at most half the plot's height (or 40% of the chart's width, at the side). Text notes become captions under the chart.
  3. **As a numbered key**, when lanes would not fit either, as on a phone with several long labels: a small numbered badge on each point, line or range, numbered across the chart, and the texts listed under it, after any captions.

  A label with an `anchor` stays where its author put it, if it fits there clear of the data; otherwise it moves like the rest. Callout text wraps narrowly, to about 12 to 17 characters a line, and labels in lanes may take up to twice that width for longer text.
- Optional styling: `anchor` is where the text sits from what it labels (`top-left`, `top`, `top-right`, `left`, `center`, `right`, `bottom-left`, `bottom`, `bottom-right`); `color` is `blue`, `orange`, `green`, `yellow`, `pink`, `red`, `purple`, `gray` (all following the chart's light or dark palette) or a hex color; lines take `stroke`: `dashed` (the default), `solid` or `dotted`; points take `"marker": false` for text with no dot.
- Text is at most 200 characters. It wraps to stay inside the plot, and a line break in it starts a new line. A chart takes at most 20 annotations.

Bar, line, histogram, scatter and stacked bar charts take every type. Maps take `text` only, since they have no x or y axis. A chart type from another plugin takes none unless it says which it draws, with `annotation_types`.

Annotations are checked on the server like the rest of the spec, and a mistake comes back as an error naming the annotation, such as `annotations[0]: a line needs x (a vertical line on most charts) or y (a horizontal line), not both`. An annotation at a value the chart does not show, such as a year outside its range, is not drawn, and a note under the chart says so.

Bar charts take an `orientation` option, `horizontal` (the default) or `vertical`, for upright bars such as one per year. When upright bars are too narrow for their labels to sit level, the labels are turned, then made smaller (down to 9px), then turned further, up to upright. Only as a last resort, and only for ordered values such as years, every second (or Nth) label is left out. Named categories always keep every label.

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

When [datasette-agent](https://github.com/datasette/datasette-agent) is installed as well, the agent gets three tools:

- `suggest_charts` returns the role of each column and the ranked suggestions for a table, view, stored query or SQL query: the same ones the Suggested charts panel shows.
- `chart` draws a chart in the chat from a spec, and returns the rows it plots to the model so it can comment on them. A spec that does not fit the data comes back as a list of errors for the model to correct. Its description teaches the model the [annotation](#annotations) format, with an example.
- `annotate_chart` adds, changes or removes the annotations on a chart that has been drawn, and draws it again. It takes the `chart_path` from an earlier result, or the address of a chart page the user has open in the panel, with `add`, `update` (`[{"index": 0, "text": "..."}]`), `remove` (indexes) or `annotations` (a whole new list).

An annotation that names a category the chart does not show is valid, but is not drawn, so `chart` and `annotate_chart` return an `annotation_warnings` list for those, with the values that are there.

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

Other plugins can add chart types. A chart type is a Python class that proposes charts and compiles them to SQL, plus a JavaScript module that draws the result, registered with the `register_chart_types` hook. The built-in chart types are registered the same way.

[Writing chart type plugins](docs/plugins.md) has a tutorial that builds one from start to finish, and a reference for the Python classes, the profile that suggestions are worked out from, and the JavaScript helpers every renderer is handed. This interface is not stable yet.

## Potential future improvements

From the spec, in rough order of how much it matters:

- **The background full tier and stored profiles.** Nothing is written to the internal database and no background task runs. Profiles are kept in memory for a few minutes. A source too large to profile under the time limit gets suggestions from a sample, or none.
- **The verify stage.** Candidates go straight from propose to rank, so nothing checks whether a time series is flat or two measures are related.
- **Precomputed thumbnails.** Every thumbnail runs its query when it scrolls into view.
- **Magic parameters in stored queries**, such as `:_actor_id`.

The map draws points over a coarse world land outline, which needs no network access. The spec leaves the choice of basemap open.

Charts are drawn with [Observable Plot](https://observablehq.com/plot/), which is bundled along with D3. See `datasette_charts/static/vendor/README.md` for versions and licenses.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-charts
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
