# datasette-configure-fts

[![PyPI](https://img.shields.io/pypi/v/datasette-configure-fts.svg)](https://pypi.org/project/datasette-configure-fts/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-configure-fts?include_prereleases&label=changelog)](https://github.com/simonw/datasette-configure-fts/releases)
[![Tests](https://github.com/simonw/datasette-configure-fts/workflows/Test/badge.svg)](https://github.com/simonw/datasette-configure-fts/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-configure-fts/blob/main/LICENSE)

Datasette plugin for enabling full-text search against selected table columns

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-configure-fts

## Usage

Having installed the plugin, visit `/-/configure-fts` on your Datasette instance to configure FTS for tables on attached writable databases.

Any time you have permission to configure FTS for a table a menu item will appear in the table actions menu on the table page.

By default only [the root actor](https://datasette.readthedocs.io/en/stable/authentication.html#using-the-root-actor) can access the page - so you'll need to run Datasette with the `--root` option and click on the link shown in the terminal to sign in and access the page.

The `configure-fts` permission governs access. You can use permission plugins such as [datasette-permissions-sql](https://github.com/simonw/datasette-permissions-sql) to grant additional access to the write interface.
