# datasette-render-html

[![PyPI](https://img.shields.io/pypi/v/datasette-render-html.svg)](https://pypi.org/project/datasette-render-html/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-render-html?include_prereleases&label=changelog)](https://github.com/simonw/datasette-render-html/releases)
[![Tests](https://github.com/simonw/datasette-render-html/workflows/Test/badge.svg)](https://github.com/simonw/datasette-render-html/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-render-html/blob/main/LICENSE)

This Datasette plugin lets you configure Datasette to render specific columns as HTML in the table and row interfaces.

This means you can store HTML in those columns and have it rendered as such on those pages.

If you have a database called `docs.db` containing a `glossary` table and you want the `definition` column in that table to be rendered as HTML, you would use a `metadata.json` file that looks like this:

    {
        "databases": {
            "docs": {
                "tables": {
                    "glossary": {
                        "plugins": {
                            "datasette-render-html": {
                                "columns": ["definition"]
                            }
                        }
                    }
                }
            }
        }
    }

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-render-html

## Usage

With the plugin installed, launch Datasette with the above `metadata.json` configuration:

    $ datasette -m metadata.json docs.db

## Security

This plugin allows HTML to be rendered exactly as it is stored in the database. As such, you should be sure only to use this against columns with content that you trust - otherwise you could open yourself up to an [XSS attack](https://owasp.org/www-community/attacks/xss/).

It's possible to configure this plugin to apply to columns with specific names across whole databases or the full Datasette instance, but doing so is not safe. It could open you up to XSS vulnerabilities where an attacker composes a SQL query that results in a column containing unsafe HTML.

As such, you should only use this plugin against specific columns in specific tables, as shown in the example above.
