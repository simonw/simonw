# datasette-charts-pie

[![PyPI](https://img.shields.io/pypi/v/datasette-charts-pie.svg)](https://pypi.org/project/datasette-charts-pie/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-charts-pie?include_prereleases&label=changelog)](https://github.com/datasette/datasette-charts-pie/releases)
[![Tests](https://github.com/datasette/datasette-charts-pie/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-charts-pie/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-charts-pie/blob/main/LICENSE)

Pie, donut, sunburst and rose charts for [datasette-charts](https://charts.datasette.io/).

## Installation

Install this plugin in the same environment as Datasette and datasette-charts.
```bash
datasette install datasette-charts-pie
```
## Chart types

| Type | Shows | Suggested when |
|------|-------|----------------|
| `pie` | Each value of a category as a share of the whole: the top slices plus "Other" | A category with 3 to 6 values, none of them too dominant or too rare. Always ranked below the bar chart of the same column |
| `donut` | The same, with the total in the hole | Not suggested |
| `sunburst` | Two categories as two rings: each inner slice broken down by a second column | Not suggested |
| `rose` | A count or an aggregate around a cycle: month of the year, day of the week or hour of the day | A date column that spans at least 2 years (months), 8 weeks (weekdays) or 7 days (hours, not for dates with no time of day) |

All of these chart types can be constructed by hand in the chart builder. Pie and Rose charts will be suggested if the data matches the above criteria.

### `pie` and `donut`

<img src="screenshots/pie.png" width="580" alt="A pie chart of orders by status. Delivered is the largest slice, at 69%, running clockwise from 12 o'clock, then Shipped at 17%, Cancelled at 9% and Returned at 5%, whose share is written outside its thin slice with a short leader line. A legend on the right lists each status with its count and share: Delivered 2,079, Shipped 505, Cancelled 265 and Returned 151.">

<img src="screenshots/donut.png" width="580" alt="A donut chart of the total amount of orders by sales channel, with 164.9K and Total amount written in the hole. Website is 45%, Mobile app 28%, Marketplace 15%, Phone 8% and In store 4%, which is too thin for a label. The legend on the right gives each channel's total, from 74,313.87 for Website down to 6,248.85 for In store, and its share.">

```json
{
  "v": 1,
  "type": "donut",
  "encoding": {
    "x": {"column": "primary_fuel", "limit": 6, "other": true},
    "y": {"column": "capacity_mw", "aggregate": "sum"}
  },
  "options": {"labels": "percent", "sweep": "full", "center": "total"}
}
```

- `x`: the slices, a category. `limit` defaults to 6. At most 8 slices are drawn, as core has eight series colors: a larger `limit` is treated as 8. The rest are always summed into an "Other" slice, and `other: false` is ignored, since leaving out the small slices would make the rest look like the whole.
- `sort`: slices run clockwise from 12 o'clock, largest first, with "Other" last. `key` or `-key` orders them by value instead, for categories with a natural order.
- `y`: optional, a count of rows (the default) or `sum` of a column. Averages and the other aggregates are not shares of anything, so they are not offered.
- `labels`: `percent` (the default), `value` or `none`. A label goes inside its slice when it fits, outside with a short leader when the slice is too thin but at least 4% of the whole, and nowhere below that. The legend always has every name, value and share.
- `sweep`: `full` (the default) or `half`, for a half circle from 9 o'clock to 3 o'clock.
- `center`, on a donut only: `total` (the default) writes the sum of the slices in the hole, and `none` leaves it empty.
- A slice whose value is zero or null is left out. If any group's sum is below zero there is no whole to take shares of, and the chart says so.

### `sunburst`

<img src="screenshots/sunburst.png" width="580" alt="A sunburst chart of customers by country, then city. The inner ring has a slice for each country, in the series colors: United Kingdom 33%, United States 24%, Germany 14%, France 9%, Japan 9%, Brazil 5% and a gray Other. The outer ring breaks each country down by city, in paler tints of the country's color, largest first, with the names written along the radius where they fit: London, Manchester shortened to Manc…, Leeds and Bristol for the United Kingdom, New York, Chicago, Austin and Seattle for the United States, and so on. The legend on the right lists the countries with their counts and shares.">

```json
{
  "v": 1,
  "type": "sunburst",
  "encoding": {
    "x": {"column": "country", "limit": 6},
    "series": {"column": "city", "limit": 5},
    "y": {"aggregate": "count"}
  }
}
```

- `x`: the inner ring, a category. `limit` defaults to 6, at most 8, with the rest in one "Other" slice that is not broken down.
- `series`: the outer ring, a different column. Its values are ranked within each inner slice, so each country gets its own largest cities. `limit` defaults to 5 for each inner slice, at most 8, with the rest of each in a pale "Other".
- `y`: optional, a count of rows (the default) or `sum` of a column. Cells whose sum is zero or below are left out, so a sum of a column with negative values is not supported.
- The legend lists the inner ring. The outer ring is named by labels where the arcs are long enough, and by tooltips.
- It is best for columns that really nest, such as city inside country. For two columns that cut across each other, a stacked bar chart is easier to read.

### `rose`

<img src="screenshots/rose.png" width="580" alt="A rose chart of orders by hour of the day. Twenty-four wedges run clockwise from midnight at the top, each reaching out as far as its number of orders, with hours labelled 00, 03, 06 and so on around the outside like a clock. The wedges are short overnight, from about 01:00 to 06:00, and longest around 12:00 and again from 19:00 to 21:00. Rings at 50, 100 and 150 orders are labelled up the 12 o'clock line, and Rows is written under the chart.">

```json
{
  "v": 1,
  "type": "rose",
  "encoding": {
    "x": {"column": "started_at"},
    "y": {"aggregate": "count"}
  },
  "options": {"cycle": "month"}
}
```

- `x`: a date or time column: ISO dates or datetimes, or Unix seconds or milliseconds, as the column's profile says. Times are read as UTC, as in core.
- `cycle`: `month` (the default), `weekday` (Monday first) or `hour`. A column of dates has no hours, and a column of years has none of these, so those are errors.
- `y`: optional, a count of rows (the default) or any aggregate of a column: `sum`, `avg`, `min`, `max` or `count_distinct`. A rose shows magnitude, not shares, so an average for each month is fine. A chart with any value below zero shows a message instead.
- Every step of the cycle gets a wedge of the same angle, so a month with no rows is an empty wedge. A wedge's radius grows with the square root of its value, so the area it fills is in proportion to it.

## Development

This plugin is developed against a checkout of datasette-charts next to it, set in `pyproject.toml`:

```toml
[tool.uv.sources]
datasette-charts = { path = "../datasette-charts", editable = true }
```

To run the tests:
```bash
cd datasette-charts-pie
uv run pytest
```
The tests of the drawing geometry in `static/arcs.js` run in node, and are skipped if node is not installed.

To try the charts on made-up data:
```bash
uv run python demo/build_demo.py
uv run datasette demo/demo.db
```
The `screenshots/` folder has the screenshots in this README, taken from the demo database.
