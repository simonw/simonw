# sitemap-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/sitemap-to-sqlite.svg)](https://pypi.org/project/sitemap-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sitemap-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/sitemap-to-sqlite/releases)
[![Tests](https://github.com/simonw/sitemap-to-sqlite/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/sitemap-to-sqlite/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sitemap-to-sqlite/blob/master/LICENSE)

Fetch data from a site's sitemap.xml into a SQLite table

## Installation

Install this tool using `pip`:
```bash
pip install sitemap-to-sqlite
```
## Usage

For help, run:
```bash
sitemap-to-sqlite --help
```
You can also use:
```bash
python -m sitemap_to_sqlite --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd sitemap-to-sqlite
python -m venv venv
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
