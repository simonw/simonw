# datasette-build

[![PyPI](https://img.shields.io/pypi/v/datasette-build.svg)](https://pypi.org/project/datasette-build/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-build?include_prereleases&label=changelog)](https://github.com/datasette/datasette-build/releases)
[![Tests](https://github.com/datasette/datasette-build/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-build/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-build/blob/main/LICENSE)

Build a directory full of files into a SQLite database

> ⚠️ **Early alpha preview**. Everything about this tool is likely to change.

## Installation

Install this tool using `pip` or `pipx`:
```bash
pipx install datasette-build
```
This will provide the `datasette-build` CLI application.

You can also install it as a Datasette plugin. First [install Datasette](https://docs.datasette.io/en/stable/installation.html), then run:
```bash
datasette install datasette-build
```
This will provide a `datasette build ...` command that works the same as the `datasette-build` CLI application.

Or you can install it as a plugin for [sqlite-utils](https://sqlite-utils.datasette.io/). With that installed, run this:
```bash
sqlite-utils install datasette-build
```
Now you can access the tool as `sqlite-utils build ...`

## Usage

The `datasette-build` (or `datasette build` or `sqlite-utils build`) command takes two arguments: a path to a SQLite database file and a path to a directory containing files to be loaded into that database:

```bash
datasette-build mydatabase.db myfiles/
```
The `myfiles/` folder can contain a mixture of CSV, TSV and JSON files. Each file will be loaded into a table in the `mydatabase.db` SQLite database.

The database file will be created if it does not already exist.

Consider a `myfiles/cities.csv` file like this:
```csv
id,name,latitude,longitude,country
nyc,New York City,40.7128,-74.006,US
lon,London,51.5074,-0.1278,GB
tok,Tokyo,35.6895,139.6917,JP
par,Paris,48.8566,2.3522,FR
ber,Berlin,52.52,13.405,DE
syd,Sydney,-33.8688,151.2093,AU
cai,Cairo,30.0444,31.2357,EG
rio,Rio de Janeiro,-22.9068,-43.1729,BR
mos,Moscow,55.7558,37.6173,RU
mum,Mumbai,19.076,72.8777,IN
```
Since this has a `id` column the primary key for the table will be set to `id`. Without an `id` column the primary key will not be defined.

A `myfiles/counties.tsv` file could look like this:
```tsv
id	name	population
US	United States	331002651
GB	United Kingdom	67886011
JP	Japan	126476461
FR	France	65273511
DE	Germany	83783942
AU	Australia	25499884
EG	Egypt	102334404
BR	Brazil	212559417
RU	Russia	145934462
IN	India	1380004385
```
And a `myfiles/museums.json` file like this:
```json
[
  {
    "id": 1,
    "name": "Metropolitan Museum of Art",
    "city_id": "nyc"
  },
  {
    "id": 2,
    "name": "British Museum",
    "city_id": "lon"
  }
]
```
Running `datasette-build mydatabase.db myfiles/` will create a SQLite database file containing three tables: `cities`, `counties` and `museums`. The schema will look like this:

```sql
CREATE TABLE [museums] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT,
   [city_id] TEXT
);
CREATE TABLE "cities" (
   [id] TEXT PRIMARY KEY,
   [name] TEXT,
   [latitude] FLOAT,
   [longitude] FLOAT,
   [country] TEXT
);
CREATE TABLE "countries" (
   [id] TEXT PRIMARY KEY,
   [name] TEXT,
   [population] INTEGER
);
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-build
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
