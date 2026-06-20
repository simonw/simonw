# sqlite-utils-ask

[![PyPI](https://img.shields.io/pypi/v/sqlite-utils-ask.svg)](https://pypi.org/project/sqlite-utils-ask/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-utils-ask?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-utils-ask/releases)
[![Tests](https://github.com/simonw/sqlite-utils-ask/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-utils-ask/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-utils-ask/blob/main/LICENSE)

Ask questions of your data with LLM assistance

See [Ask questions of SQLite databases and CSV/JSON files in your terminal](https://simonwillison.net/2024/Nov/25/ask-questions-of-sqlite/) for background on this project.

## Installation

Install this plugin in the same environment as sqlite-utils.
```bash
sqlite-utils install sqlite-utils-ask
```
## sqlite-utils ask

Ask questions of a SQLite database file like this:

```bash
sqlite-utils ask content.db 'How many repos?'
```
The tool will use an LLM (`gpt-4o-mini` by default) to generate the appropriate SQL query by passing through your question and the database schema, and will then execute the query and return the result.

## sqlite-utils ask-files

You can also ask questions directly of CSV, TSV or JSON files. These will be imported into an in-memory SQLite database prior to running the query.

```bash
sqlite-utils ask-files data.csv 'How many repos?'
```
You can pass multiple files and run queries across multiple resulting tables.

```bash
sqlite-utils ask-files legislators.csv votes.csv 'How many votes did each legislator cast?'
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd sqlite-utils-ask
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
To capture new HTTP interactions, run:
```bash
PYTEST_OPENAI_API_KEY=your-key python -m pytest --record-mode once
```
Or use `--record-mode all` to re-record all interactions.
