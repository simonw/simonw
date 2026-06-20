# yaml-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/yaml-to-sqlite.svg)](https://pypi.org/project/yaml-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/yaml-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/yaml-to-sqlite/releases)
[![Tests](https://github.com/simonw/yaml-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/yaml-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/yaml-to-sqlite/blob/main/LICENSE)

Load the contents of a YAML file into a SQLite database table.

```
$ yaml-to-sqlite --help
Usage: yaml-to-sqlite [OPTIONS] DB_PATH TABLE YAML_FILE

  Convert YAML files to SQLite

Options:
  --version             Show the version and exit.
  --pk TEXT             Column to use as a primary key
  --single-column TEXT  If YAML file is a list of values, populate this column
  --help                Show this message and exit.
```
## Usage

Given a `news.yml` file containing the following:
```yaml
- date: 2021-06-05
  body: |-
    [Datasette 0.57](https://docs.datasette.io/en/stable/changelog.html#v0-57) is out with an important security patch.
- date: 2021-05-10
  body: |-
    [Django SQL Dashboard](https://simonwillison.net/2021/May/10/django-sql-dashboard/) is a new tool that brings a useful authenticated subset of Datasette to Django projects that are built on top of PostgreSQL.
```
Running this command:
```bash
$ yaml-to-sqlite news.db stories news.yml
```
Will create a database file with this schema:
```bash
$ sqlite-utils schema news.db
CREATE TABLE [stories] (
   [date] TEXT,
   [body] TEXT
);
```
The `--pk` option can be used to set a column as the primary key for the table:

```bash
$ yaml-to-sqlite news.db stories news.yml --pk date
$ sqlite-utils schema news.db
CREATE TABLE [stories] (
   [date] TEXT PRIMARY KEY,
   [body] TEXT
);
```
## Single column YAML lists

The `--single-column` option can be used when the YAML file is a list of values, for example a file called `dogs.yml` containing the following:

```yaml
- Cleo
- Pancakes
- Nixie
```
Running this command:
```bash
$ yaml-to-sqlite dogs.db dogs.yaml --single-column=name
```
Will create a single `dogs` table with a single `name` column that is the primary key:

```bash
$ sqlite-utils schema dogs.db
CREATE TABLE [dogs] (
   [name] TEXT PRIMARY KEY
);
$ sqlite-utils dogs.db 'select * from dogs' -t
name
--------
Cleo
Pancakes
Nixie
```
