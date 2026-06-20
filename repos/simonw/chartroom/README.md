# Chartroom

[![PyPI](https://img.shields.io/pypi/v/chartroom.svg)](https://pypi.org/project/chartroom/)
[![Changelog](https://img.shields.io/github/v/release/simonw/chartroom?include_prereleases&label=changelog)](https://github.com/simonw/chartroom/releases)
[![Tests](https://github.com/simonw/chartroom/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/chartroom/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/chartroom/blob/master/LICENSE)

CLI tool for creating charts from CSV, TSV, JSON, JSONL, or SQLite data using [matplotlib](https://matplotlib.org/). Designed to work well with [Showboat](https://github.com/simonw/showboat).

## Installation

```bash
pip install chartroom
```
Or:
```bash
uv tool install chartroom
```
Or run it directly with:
```bash
uvx chartroom
```

## Demo

See the [live demo document](https://github.com/simonw/chartroom/blob/main/demo/README.md) for examples of every chart type, input format, and style option with inline images. The demo was built using [Showboat](https://github.com/simonw/showboat).

## Usage

```bash
chartroom --help
```

### Chart types

- `chartroom bar` - Bar chart (vertical, supports grouped bars)
- `chartroom line` - Line chart (supports multiple series)
- `chartroom scatter` - Scatter plot
- `chartroom pie` - Pie chart
- `chartroom histogram` - Histogram

### Data input

Provide data as a file, via stdin, or from a SQLite query:

```bash
# From a CSV file (auto-detected)
chartroom bar data.csv

# Explicit format
chartroom bar --csv data.csv
chartroom bar --tsv data.tsv
chartroom bar --json data.json
chartroom bar --jsonl data.jsonl

# From stdin
cat data.csv | chartroom bar --csv

# From SQLite
chartroom bar --sql mydb.sqlite "SELECT name, count FROM items"
```

### Column selection

Columns are auto-detected from common names (`name`/`label`/`x` for x-axis, `value`/`count`/`y` for y-axis), or specify explicitly:

```bash
chartroom bar --csv -x region -y revenue data.csv
```

Multiple y columns create grouped/overlaid series:

```bash
chartroom bar --csv -x region -y q1 -y q2 -y q3 data.csv
```

### Output

By default, saves to `chart.png` (incrementing to `chart-2.png` etc. to avoid overwrites). Use `-o` to specify a path:

```bash
chartroom bar --csv data.csv -o sales.png
```

The full absolute path of the output file is printed to stdout.

### Output format

Use `-f` / `--output-format` to control what is printed to stdout:

```bash
# Default: just the file path
chartroom bar --csv data.csv
# /path/to/chart.png

# Markdown image syntax
chartroom bar --csv data.csv -f markdown --alt "Sales by region"
# ![Sales by region](/path/to/chart.png)

# HTML img tag
chartroom bar --csv data.csv -f html --alt "Sales by region"
# <img src="/path/to/chart.png" alt="Sales by region">

# JSON with path and alt text
chartroom bar --csv data.csv -f json
# {"path": "/path/to/chart.png", "alt": "Bar chart of value by name — ..."}

# Just the alt text
chartroom bar --csv data.csv -f alt
# Bar chart of value by name — alice: 10, bob: 20, charlie: 15
```

When `--alt` is omitted, alt text is auto-generated from the chart title (if set) or from the chart type and data. Small datasets get all values listed; larger datasets get a summary with range and extremes.

### Alt text generation

Chartroom automatically generates descriptive alt text for every chart, making output accessible to screen readers and useful in documentation. You can use `--alt` to provide your own alt text, or let chartroom generate it from the chart type and data.

The auto-generated alt text adapts to both chart type and dataset size:

- **Bar, line, and scatter charts** — Small datasets (6 rows or fewer) list every value (e.g. `Bar chart of value by name — alice: 10, bob: 20, charlie: 15`). Larger datasets summarize the count, range, and extremes (e.g. `Bar chart of population by city. 10 points, ranging from 17118 (Dhaka) to 37400 (Tokyo)`). Multiple y-columns are noted as additional series.
- **Pie charts** — Small datasets show each category with its percentage (e.g. `Pie chart showing Rent (57%), Food (19%), Transport (10%), Other (14%)`). Larger datasets list the top 3 categories by share.
- **Histograms** — Small datasets list all values. Larger datasets describe the distribution range (e.g. `Histogram of 10 score values ranging from 76 to 95`).

If a `--title` is set, it is prepended to the generated alt text (e.g. `Team Scores. Bar chart of value by name — alice: 10, bob: 20, charlie: 15`). The `--alt` option overrides this entirely with custom text. The alt text is embedded automatically when using `-f markdown`, `-f html`, or `-f json` output formats, or can be printed on its own with `-f alt`.

See the [alt text demo](https://github.com/simonw/chartroom/blob/main/demo/alt-text.md) for worked examples of every chart type and output format.

### Styling

```bash
chartroom bar --csv data.csv --title "Sales" --xlabel "Region" --ylabel "Revenue" \
  --width 12 --height 8 --dpi 150 --style ggplot
```

Available styles:

<!-- [[[cog
from click.testing import CliRunner
from chartroom.cli import cli
result = CliRunner().invoke(cli, ["styles"])
lines = [l for l in result.output.strip().split("\n") if l.strip()]
cog.out("\n".join(f"- `{l.strip()}`" for l in lines) + "\n")
]]] -->
- `Solarize_Light2`
- `bmh`
- `classic`
- `dark_background`
- `fast`
- `fivethirtyeight`
- `ggplot`
- `grayscale`
- `petroff10`
- `seaborn-v0_8`
- `seaborn-v0_8-bright`
- `seaborn-v0_8-colorblind`
- `seaborn-v0_8-dark`
- `seaborn-v0_8-dark-palette`
- `seaborn-v0_8-darkgrid`
- `seaborn-v0_8-deep`
- `seaborn-v0_8-muted`
- `seaborn-v0_8-notebook`
- `seaborn-v0_8-paper`
- `seaborn-v0_8-pastel`
- `seaborn-v0_8-poster`
- `seaborn-v0_8-talk`
- `seaborn-v0_8-ticks`
- `seaborn-v0_8-white`
- `seaborn-v0_8-whitegrid`
- `tableau-colorblind10`
<!-- [[[end]]] -->

See the [style gallery](https://github.com/simonw/chartroom/blob/main/demo/styles.md) for visual examples of every style.

## CLI reference

<!-- [[[cog
from click.testing import CliRunner
from chartroom.cli import cli
def all_help(cli):
    commands = []
    def find_commands(command, path=None):
        path = path or []
        commands.append(path + [command.name])
        if hasattr(command, 'commands'):
            for subcommand in command.commands.values():
                find_commands(subcommand, path + [command.name])
    find_commands(cli)
    commands = [command[1:] for command in commands]
    output = []
    for command in commands:
        heading_level = len(command) + 2
        result = CliRunner().invoke(cli, command + ["--help"])
        cmd_str = " ".join(["chartroom"] + command)
        output.append("#" * heading_level + " " + cmd_str + "\n")
        output.append("```")
        output.append(result.output.replace("Usage: cli", "Usage: chartroom").strip())
        output.append("```\n")
    return "\n".join(output)
cog.out(all_help(cli))
]]] -->
## chartroom

```
Usage: chartroom [OPTIONS] COMMAND [ARGS]...

  CLI tool for creating charts

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  bar        Create a bar chart from columnar data.
  histogram  Create a histogram showing the distribution of a numeric column.
  line       Create a line chart from columnar data.
  pie        Create a pie chart from columnar data.
  scatter    Create a scatter plot from columnar data.
  styles     List available matplotlib styles.
```

### chartroom bar

```
Usage: chartroom bar [OPTIONS] [FILE]

  Create a bar chart from columnar data.

  Examples:
    chartroom bar --csv data.csv
    chartroom bar --csv data.csv -x region -y revenue -o sales.png
    chartroom bar --csv -x name -y q1 -y q2 data.csv
    cat data.csv | chartroom bar --csv -f markdown
    chartroom bar --sql mydb.sqlite "SELECT name, count FROM items"

Options:
  -o, --output TEXT               Output file path (default: chart.png)
  -x TEXT                         Column for x-axis / categories
  -y TEXT                         Column(s) for y-axis / values (repeatable)
  --csv                           Parse input as CSV
  --tsv                           Parse input as TSV
  --json                          Parse input as JSON
  --jsonl                         Parse input as newline-delimited JSON
  --sql TEXT...                   Query a SQLite database. Takes two arguments:
                                  DATABASE QUERY. Example: --sql mydb.sqlite
                                  'SELECT name, count FROM items'
  --title TEXT                    Chart title, also prepended to generated alt
                                  text
  --xlabel TEXT                   X-axis label
  --ylabel TEXT                   Y-axis label
  --width FLOAT                   Figure width in inches
  --height FLOAT                  Figure height in inches
  --style TEXT                    Matplotlib style (e.g. ggplot,
                                  dark_background)
  --dpi INTEGER                   Output DPI
  -f, --output-format [path|markdown|html|json|alt]
                                  How to format stdout. path (default): absolute
                                  file path. markdown: ![alt](path). html: <img
                                  src=path alt=...>. json: {"path": ..., "alt":
                                  ...}. alt: just the alt text, no path. Alt
                                  text is auto-generated from chart type and
                                  data unless --alt is given.
  --alt TEXT                      Override the auto-generated alt text. Ignored
                                  when -f is path (the default). When omitted, a
                                  description is generated from the chart type
                                  and data.
  --help                          Show this message and exit.
```

### chartroom line

```
Usage: chartroom line [OPTIONS] [FILE]

  Create a line chart from columnar data.

  Examples:
    chartroom line --csv data.csv
    chartroom line --csv data.csv -x month -y revenue
    chartroom line --csv -x date -y temp -y humidity data.csv
    chartroom line --csv data.csv -f json

Options:
  -o, --output TEXT               Output file path (default: chart.png)
  -x TEXT                         Column for x-axis / categories
  -y TEXT                         Column(s) for y-axis / values (repeatable)
  --csv                           Parse input as CSV
  --tsv                           Parse input as TSV
  --json                          Parse input as JSON
  --jsonl                         Parse input as newline-delimited JSON
  --sql TEXT...                   Query a SQLite database. Takes two arguments:
                                  DATABASE QUERY. Example: --sql mydb.sqlite
                                  'SELECT name, count FROM items'
  --title TEXT                    Chart title, also prepended to generated alt
                                  text
  --xlabel TEXT                   X-axis label
  --ylabel TEXT                   Y-axis label
  --width FLOAT                   Figure width in inches
  --height FLOAT                  Figure height in inches
  --style TEXT                    Matplotlib style (e.g. ggplot,
                                  dark_background)
  --dpi INTEGER                   Output DPI
  -f, --output-format [path|markdown|html|json|alt]
                                  How to format stdout. path (default): absolute
                                  file path. markdown: ![alt](path). html: <img
                                  src=path alt=...>. json: {"path": ..., "alt":
                                  ...}. alt: just the alt text, no path. Alt
                                  text is auto-generated from chart type and
                                  data unless --alt is given.
  --alt TEXT                      Override the auto-generated alt text. Ignored
                                  when -f is path (the default). When omitted, a
                                  description is generated from the chart type
                                  and data.
  --help                          Show this message and exit.
```

### chartroom scatter

```
Usage: chartroom scatter [OPTIONS] [FILE]

  Create a scatter plot from columnar data.

  Examples:
    chartroom scatter --csv data.csv
    chartroom scatter --csv data.csv -x height -y weight
    chartroom scatter --csv data.csv -f html --alt "Height vs Weight"

Options:
  -o, --output TEXT               Output file path (default: chart.png)
  -x TEXT                         Column for x-axis / categories
  -y TEXT                         Column(s) for y-axis / values (repeatable)
  --csv                           Parse input as CSV
  --tsv                           Parse input as TSV
  --json                          Parse input as JSON
  --jsonl                         Parse input as newline-delimited JSON
  --sql TEXT...                   Query a SQLite database. Takes two arguments:
                                  DATABASE QUERY. Example: --sql mydb.sqlite
                                  'SELECT name, count FROM items'
  --title TEXT                    Chart title, also prepended to generated alt
                                  text
  --xlabel TEXT                   X-axis label
  --ylabel TEXT                   Y-axis label
  --width FLOAT                   Figure width in inches
  --height FLOAT                  Figure height in inches
  --style TEXT                    Matplotlib style (e.g. ggplot,
                                  dark_background)
  --dpi INTEGER                   Output DPI
  -f, --output-format [path|markdown|html|json|alt]
                                  How to format stdout. path (default): absolute
                                  file path. markdown: ![alt](path). html: <img
                                  src=path alt=...>. json: {"path": ..., "alt":
                                  ...}. alt: just the alt text, no path. Alt
                                  text is auto-generated from chart type and
                                  data unless --alt is given.
  --alt TEXT                      Override the auto-generated alt text. Ignored
                                  when -f is path (the default). When omitted, a
                                  description is generated from the chart type
                                  and data.
  --help                          Show this message and exit.
```

### chartroom pie

```
Usage: chartroom pie [OPTIONS] [FILE]

  Create a pie chart from columnar data.

  Uses the first -y column for slice sizes. Labels come from the -x column.

  Examples:
    chartroom pie --csv data.csv
    chartroom pie --csv data.csv -x category -y amount
    chartroom pie --csv data.csv -f markdown

Options:
  -o, --output TEXT               Output file path (default: chart.png)
  -x TEXT                         Column for x-axis / categories
  -y TEXT                         Column(s) for y-axis / values (repeatable)
  --csv                           Parse input as CSV
  --tsv                           Parse input as TSV
  --json                          Parse input as JSON
  --jsonl                         Parse input as newline-delimited JSON
  --sql TEXT...                   Query a SQLite database. Takes two arguments:
                                  DATABASE QUERY. Example: --sql mydb.sqlite
                                  'SELECT name, count FROM items'
  --title TEXT                    Chart title, also prepended to generated alt
                                  text
  --xlabel TEXT                   X-axis label
  --ylabel TEXT                   Y-axis label
  --width FLOAT                   Figure width in inches
  --height FLOAT                  Figure height in inches
  --style TEXT                    Matplotlib style (e.g. ggplot,
                                  dark_background)
  --dpi INTEGER                   Output DPI
  -f, --output-format [path|markdown|html|json|alt]
                                  How to format stdout. path (default): absolute
                                  file path. markdown: ![alt](path). html: <img
                                  src=path alt=...>. json: {"path": ..., "alt":
                                  ...}. alt: just the alt text, no path. Alt
                                  text is auto-generated from chart type and
                                  data unless --alt is given.
  --alt TEXT                      Override the auto-generated alt text. Ignored
                                  when -f is path (the default). When omitted, a
                                  description is generated from the chart type
                                  and data.
  --help                          Show this message and exit.
```

### chartroom histogram

```
Usage: chartroom histogram [OPTIONS] [FILE]

  Create a histogram showing the distribution of a numeric column.

  Requires -y to specify the column. Use --bins to control bucket count.

  Examples:
    chartroom histogram --csv -y score data.csv
    chartroom histogram --csv -y score data.csv --bins 20
    chartroom histogram --csv -y score data.csv -f alt

Options:
  -o, --output TEXT               Output file path (default: chart.png)
  -x TEXT                         Column for x-axis / categories
  -y TEXT                         Column(s) for y-axis / values (repeatable)
  --csv                           Parse input as CSV
  --tsv                           Parse input as TSV
  --json                          Parse input as JSON
  --jsonl                         Parse input as newline-delimited JSON
  --sql TEXT...                   Query a SQLite database. Takes two arguments:
                                  DATABASE QUERY. Example: --sql mydb.sqlite
                                  'SELECT name, count FROM items'
  --title TEXT                    Chart title, also prepended to generated alt
                                  text
  --xlabel TEXT                   X-axis label
  --ylabel TEXT                   Y-axis label
  --width FLOAT                   Figure width in inches
  --height FLOAT                  Figure height in inches
  --style TEXT                    Matplotlib style (e.g. ggplot,
                                  dark_background)
  --dpi INTEGER                   Output DPI
  -f, --output-format [path|markdown|html|json|alt]
                                  How to format stdout. path (default): absolute
                                  file path. markdown: ![alt](path). html: <img
                                  src=path alt=...>. json: {"path": ..., "alt":
                                  ...}. alt: just the alt text, no path. Alt
                                  text is auto-generated from chart type and
                                  data unless --alt is given.
  --alt TEXT                      Override the auto-generated alt text. Ignored
                                  when -f is path (the default). When omitted, a
                                  description is generated from the chart type
                                  and data.
  --bins INTEGER                  Number of histogram bins
  --help                          Show this message and exit.
```

### chartroom styles

```
Usage: chartroom styles [OPTIONS]

  List available matplotlib styles.

Options:
  --help  Show this message and exit.
```
<!-- [[[end]]] -->

## Development

```bash
git clone https://github.com/simonw/chartroom
cd chartroom
uv run pytest
```
