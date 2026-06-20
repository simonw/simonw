# datasette-pretty-traces

[![PyPI](https://img.shields.io/pypi/v/datasette-pretty-traces.svg)](https://pypi.org/project/datasette-pretty-traces/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-pretty-traces?include_prereleases&label=changelog)](https://github.com/simonw/datasette-pretty-traces/releases)
[![Tests](https://github.com/simonw/datasette-pretty-traces/workflows/Test/badge.svg)](https://github.com/simonw/datasette-pretty-traces/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-pretty-traces/blob/main/LICENSE)

Prettier formatting for `?_trace=1` traces

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-pretty-traces
```
## Usage

Once installed, run Datasette using `--setting trace_debug 1`:
```bash
datasette fixtures.db --setting trace_debug 1
```
Then navigate to any page and add `?_trace=` to the URL:

    http://localhost:8001/?_trace=1

The plugin will scroll you down the page to the visualized trace information.

You can also visit the dedicated demo page to see the `fetch()` interception feature in action:

    http://localhost:8001/-/pretty-traces?_trace=1

## Demo

You can try out the demo here:

- [/?_trace=1](https://latest-with-plugins.datasette.io/?_trace=1) tracing the homepage
- [/github/commits?_trace=1](https://latest-with-plugins.datasette.io/github/commits?_trace=1) tracing a table page

## Screenshot

![Screenshot showing the visualization produced by the plugin](https://user-images.githubusercontent.com/9599/145883732-a53accdd-5feb-4629-94cd-f73407c7943d.png)

## Development

To set up this plugin locally, checkout the code and run the tests with `uv run pytest`:
```bash
cd datasette-pretty-traces
uv run pytest
```
To try your development version of plugin run it like this:
```bash
uv run datasette fixtures.db --setting trace_debug 1
```
