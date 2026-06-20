# datasette-enrichments

[![PyPI](https://img.shields.io/pypi/v/datasette-enrichments.svg)](https://pypi.org/project/datasette-enrichments/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-enrichments?include_prereleases&label=changelog)](https://github.com/simonw/datasette-enrichments/releases)
[![Tests](https://github.com/simonw/datasette-enrichments/workflows/Test/badge.svg)](https://github.com/simonw/datasette-enrichments/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-enrichments/blob/main/LICENSE)

Tools for running enrichments against data stored in Datasette

Potential use-cases for enrichments include:

- Geocoding an address and populating a latitude and longitude column
- Executing a template to generate output based on the values in each row
- Fetching data from a URL and populating a column with the result
- Executing OCR against a linked image or PDF file

Documentation for this plugin lives at **[enrichments.datasette.io](https://enrichments.datasette.io/)**.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-enrichments
python3 -mvenv venv
source venv/bin/activate
```
Or if you are using `pipenv`:
```bash
pipenv shell
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```