# sqlite-utils-tui

[![PyPI](https://img.shields.io/pypi/v/sqlite-utils-tui.svg)](https://pypi.org/project/sqlite-utils-tui/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-utils-tui?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-utils-tui/releases)
[![Tests](https://github.com/simonw/sqlite-utils-tui/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-utils-tui/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-utils-tui/blob/main/LICENSE)

Terminal UI for [sqlite-utils](https://sqlite-utils.datasette.io/), built on top of [Trogon](https://github.com/Textualize/trogon).

## Installation

Install this plugin in the same environment as sqlite-utils.
```bash
sqlite-utils install sqlite-utils-tui
```
## Usage

Once installed, run the following command to open a terminal UI for exploring the options made available by `sqlite-utils`:

```bash
sqlite-utils tui
```

![Screenshot of the TUI showing sqlite-utils options in an interactive terminal interface](https://raw.githubusercontent.com/simonw/sqlite-utils-tui/refs/heads/main/tui.png)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd sqlite-utils-tui
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
