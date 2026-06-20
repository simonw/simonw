# datasette-upload-csvs

[![PyPI](https://img.shields.io/pypi/v/datasette-upload-csvs.svg)](https://pypi.org/project/datasette-upload-csvs/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-upload-csvs?include_prereleases&label=changelog)](https://github.com/simonw/datasette-upload-csvs/releases)
[![Tests](https://github.com/simonw/datasette-upload-csvs/workflows/Test/badge.svg)](https://github.com/simonw/datasette-upload-csvs/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-upload-csvs/blob/main/LICENSE)

Datasette plugin for uploading CSV files and converting them to database tables

## Installation

    datasette install datasette-upload-csvs

## Usage

The plugin adds an interface at `/-/upload-csvs` for uploading a CSV file and using it to create a new database table.

By default only [the root actor](https://datasette.readthedocs.io/en/stable/authentication.html#using-the-root-actor) can access the page - so you'll need to run Datasette with the `--root` option and click on the link shown in the terminal to sign in and access the page.

The `upload-csvs` permission governs access. You can use permission plugins such as [datasette-permissions-sql](https://github.com/simonw/datasette-permissions-sql) to grant additional access to the write interface.
