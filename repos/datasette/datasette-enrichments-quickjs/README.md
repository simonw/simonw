# datasette-enrichments-quickjs

[![PyPI](https://img.shields.io/pypi/v/datasette-enrichments-quickjs.svg)](https://pypi.org/project/datasette-enrichments-quickjs/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-enrichments-quickjs?include_prereleases&label=changelog)](https://github.com/datasette/datasette-enrichments-quickjs/releases)
[![Tests](https://github.com/datasette/datasette-enrichments-quickjs/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-enrichments-quickjs/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-enrichments-quickjs/blob/main/LICENSE)

[Datasette enrichment](https://github.com/simonw/datasette-enrichments) for enriching data with a custom JavaScript function

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-enrichments-quickjs
```
## Usage

This enrichment allows you to select rows from a table and specify a custom JavaScript function to use to generate a value for each of those rows, storing that value in a specified column and creating that column if it does not exist.

Code runs in a [QuickJS sandbox](https://github.com/PetterS/quickjs) with a 0.1s time limit for the execution of each function and a 4MB memory limit.

Enrichment JavaScript functions look like this:

```javascript
function enrich(row) {
    return row["title"] + "!";
}
```
The return value of your function will be stored in the output column of your choice.

Instead of picking an output column, you can have your function return an object with keys and values.

This example takes a `point` column with values like `37.7749,-122.4194 and splits it into `latitude` and `longitude` columns:

```javascript
function enrich(row) {
    const bits = row.point.split(",");
    return {
        "latitude": parseFloat(bits[0]),
        "longitude": parseFloat(bits[1])
    }
}
```
The enrichment will then create new columns in the table for each key in the object returned by that function.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-enrichments-quickjs
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
