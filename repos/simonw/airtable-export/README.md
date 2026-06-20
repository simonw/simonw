# airtable-export

[![PyPI](https://img.shields.io/pypi/v/airtable-export.svg)](https://pypi.org/project/airtable-export/)
[![Changelog](https://img.shields.io/github/v/release/simonw/airtable-export?include_prereleases&label=changelog)](https://github.com/simonw/airtable-export/releases)
[![Tests](https://github.com/simonw/airtable-export/workflows/Test/badge.svg)](https://github.com/simonw/airtable-export/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/airtable-export/blob/master/LICENSE)

Export Airtable data to files on disk

## Installation

Install this tool using `pip`:

    $ pip install airtable-export

## Usage

You will need to the following information:

- Your Airtable base ID - this is a string starting with `app...`
- Your Airtable personal access token - this is a string starting with `pat...`

If you just want to export a subset of your tables you also need to know the names of those tables.

You can export all of your data to a folder called `export/` by running the following:

    airtable-export export base_id --key=key

This example would files for each of your tables, for example: `export/table1.yml` and `export/table2.yml`.

Rather than passing the API key using the `--key` option you can set it as an environment variable called `AIRTABLE_KEY`.

To export only specified tables, pass their names as additional arguments:

    airtable-export export base_id table1 table2 --key=key

## Export options

By default the tool exports your data as YAML.

You can also export as JSON or as [newline delimited JSON](http://ndjson.org/) using the `--json` or `--ndjson` options:

    airtable-export export base_id --key=key --ndjson

You can pass multiple format options at once. This command will create a `.json`, `.yml` and `.ndjson` file for each exported table:

    airtable-export export base_id \
        --key=key --ndjson --yaml --json

If you import all tables, or if you add the `--schema` option, a JSON schema for the base will be written to `output-dir/_schema.json`.

### SQLite database export

You can export tables to a SQLite database file using the `--sqlite database.db` option:

    airtable-export export base_id \
        --key=key --sqlite database.db

This can be combined with other format options. If you only specify `--sqlite` the export directory argument will be ignored.

The SQLite database will have a table created for each table you export. Those tables will have a primary key column called `airtable_id`.

If you run this command against an existing SQLite database records with matching primary keys will be over-written by new records from the export.

## Request options

By default the tool uses [python-httpx](https://www.python-httpx.org)'s default configurations.

You can override the `user-agent` using the `--user-agent` option:

    airtable-export export base_id table1 table2 --key=key --user-agent "Airtable Export Robot"

You can override the [timeout during a network read operation](https://www.python-httpx.org/advanced/#fine-tuning-the-configuration) using the `--http-read-timeout` option. If not set, this defaults to 5s.

    airtable-export export base_id table1 table2 --key=key --http-read-timeout 60

## Running this using GitHub Actions

[GitHub Actions](https://github.com/features/actions) is GitHub's workflow automation product. You can use it to run `airtable-export` in order to back up your Airtable data to a GitHub repository. Doing this gives you a visible commit history of changes you make to your Airtable data - like [this one](https://github.com/natbat/rockybeaches/commits/main/airtable).

To run this for your own Airtable database you'll first need to add the following secrets to your GitHub repository:

<dl>
  <dt>AIRTABLE_BASE_ID</dt>
  <dd>The base ID, a string beginning `app...`</dd>
  <dt>AIRTABLE_KEY</dt>
  <dd>Your Airtable API key</dd>
  <dt>AIRTABLE_TABLES</dt>
  <dd>A space separated list of the Airtable tables that you want to backup. If any of these contain spaces you will need to enclose them in single quotes, e.g. <samp>'My table with spaces in the name' OtherTableWithNoSpaces</samp></dd>
</dl>

Once you have set those secrets, add the following as a file called `.github/workflows/backup-airtable.yml`:
```yaml
name: Backup Airtable

on:
  workflow_dispatch:
  schedule:
  - cron: '32 0 * * *'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Check out repo
      uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - uses: actions/cache@v2
      name: Configure pip caching
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-
        restore-keys: |
          ${{ runner.os }}-pip-
    - name: Install airtable-export
      run: |
        pip install airtable-export
    - name: Backup Airtable to backups/
      env:
        AIRTABLE_BASE_ID: ${{ secrets.AIRTABLE_BASE_ID }}
        AIRTABLE_KEY: ${{ secrets.AIRTABLE_KEY }}
        AIRTABLE_TABLES: ${{ secrets.AIRTABLE_TABLES }}
      run: |-
        airtable-export backups $AIRTABLE_BASE_ID $AIRTABLE_TABLES -v
    - name: Commit and push if it changed
      run: |-
        git config user.name "Automated"
        git config user.email "actions@users.noreply.github.com"
        git add -A
        timestamp=$(date -u)
        git commit -m "Latest data: ${timestamp}" || exit 0
        git push
```
This will run once a day (at 32 minutes past midnight UTC) and will also run if you manually click the "Run workflow" button, see [GitHub Actions: Manual triggers with workflow_dispatch](https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/).

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd airtable-export
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
