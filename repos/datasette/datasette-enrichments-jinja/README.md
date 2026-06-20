# datasette-enrichments-jinja

[![PyPI](https://img.shields.io/pypi/v/datasette-enrichments-jinja.svg)](https://pypi.org/project/datasette-enrichments-jinja/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-enrichments-jinja?include_prereleases&label=changelog)](https://github.com/datasette/datasette-enrichments-jinja/releases)
[![Tests](https://github.com/datasette/datasette-enrichments-jinja/workflows/Test/badge.svg)](https://github.com/datasette/datasette-enrichments-jinja/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-enrichments-jinja/blob/main/LICENSE)

[Datasette enrichment](https://github.com/simonw/datasette-enrichments) for evaluating templates in a Jinja sandbox

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-enrichments-jinja
```
## Usage

This enrichment allows you to select rows from a table and specify a Jinja template to use to generate new text for each of those rows.

The text can then be saved to a new or existing column on the table.

Code runs in a [Jinja sandbox](https://jinja.palletsprojects.com/en/3.1.x/sandbox/). This should protect against innocent mistakes, but may not be robust against malicious attackers - so only make this enrichment available to users who you trust not to abuse it.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-enrichments-jinja
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
