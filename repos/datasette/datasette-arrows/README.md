# datasette-arrows

[![PyPI](https://img.shields.io/pypi/v/datasette-arrows.svg)](https://pypi.org/project/datasette-arrows/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-arrows?include_prereleases&label=changelog)](https://github.com/datasette/datasette-arrows/releases)
[![Tests](https://github.com/datasette/datasette-arrows/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-arrows/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-arrows/blob/main/LICENSE)

Streaming exports for Datasette using Arrow IPC.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-arrows
```
## Usage

This plugin adds a `.arrows` export format to every table, view, row and SQL query page. It returns the rows as an [Arrow IPC stream](https://arrow.apache.org/docs/format/Columnar.html#ipc-streaming-format), served as `application/vnd.apache.arrow.stream`. The format is also listed in Datasette's "Export data" dialog.

    /database/table.arrows
    /database/-/query.arrows?sql=select+*+from+table

Like Datasette's CSV export, a table or view URL returns a single page of rows unless you add `?_stream=1`, which streams every row:

    /database/table.arrows?_stream=1

Rows are fetched and sent one page at a time, as one Arrow record batch per page, so a table of any size can be exported without loading it into memory. Filters, sort order and `?_col=` options all apply to the export.

In the "Export data" dialog the Arrow format is listed with TSV and CSV. Check "Include all rows" there to download every row.

Datasette's [allow_stream](https://docs.datasette.io/en/latest/settings.html#allow-stream) and [max_stream_mb](https://docs.datasette.io/en/latest/settings.html#max-stream-mb) settings apply to these exports. Add `?_dl=1` to download the response as a file.

Reading an export in Python:

```python
import urllib.request
import pyarrow as pa

with urllib.request.urlopen(
    "http://localhost:8001/data/dogs.arrows?_stream=1"
) as response:
    table = pa.ipc.open_stream(response).read_all()
```

### Column types

SQLite columns can hold values of any type, but each column in an Arrow stream has a single type which is sent before the first row. The plugin picks that type using the type the column was declared with in its table, if it has one, together with the values in the first page of rows:

| SQLite values | Arrow type |
| --- | --- |
| Integers | `int64` |
| Floating point, or a mix of floating point and integers | `float64` |
| Text, or a mix of text and numbers | `string` |
| Blobs, or a mix of blobs and anything else | `binary` |
| Nothing but `null`, in a column with no declared type | `string` |

A value on a later page is converted if the column's type can represent it: an integer in a `float64` column, or a number in a `string` column. If it cannot - text in a column declared as `INTEGER`, for example - the export fails by dropping the connection, so that an incomplete file is not mistaken for a complete one. Export a column like that using a SQL query that casts it, such as `select cast(value as text) as value from ...`.

With `?_labels=on` each foreign key column is followed by a `column_label` column containing the label of the row it refers to.

This plugin requires streaming output renderers, which are in Datasette's `main` branch but have not yet been included in a release.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-arrows
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
