# evernote-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/evernote-to-sqlite.svg)](https://pypi.org/project/evernote-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/dogsheep/evernote-to-sqlite?include_prereleases&label=changelog)](https://github.com/dogsheep/evernote-to-sqlite/releases)
[![Tests](https://github.com/dogsheep/evernote-to-sqlite/workflows/Test/badge.svg)](https://github.com/dogsheep/evernote-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dogsheep/evernote-to-sqlite/blob/master/LICENSE)

Tools for converting Evernote content to SQLite. See [Building an Evernote to SQLite exporter](https://simonwillison.net/2020/Oct/16/building-evernote-sqlite-exporter/) for background on this project.

## Installation

Install this tool using `pip`:

    $ pip install evernote-to-sqlite

## Usage

Currently the only available command is `evernote-to-sqlite enex`, which converts Evernote's ENEX export files into a SQLite database.

You can create [an ENEX export](https://help.evernote.com/hc/en-us/articles/209005557-Export-notes-and-notebooks-as-ENEX-or-HTML) in the Evernote desktop application by selecting some notes (or all of your notes) and using the `File -> Export Notes...` menu option.

This used to be able to export everything in one go, but it looks like more recent Evernote versions only allow exporting up to fifty notes at a time, or let you export an entire notebook by right-clicking on the notebook and selecting "Export notebook...".

You can convert that file to SQLite like so:

    $ evernote-to-sqlite enex evernote.db MyNotes.enex

This will display a progress bar and create a SQLite database file called `evernote.db`.

### Limitations

Unfortunately the ENEX export format does not include a unique identifier for each note. This means you cannot use this tool to re-import notes after they have been updated - you should consider this tool to be a one-time transformation of an ENEX file into an equivalent SQLite database.

ENEX exports also do not include details of which notebook a note belongs to.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd evernote-to-sqlite
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
