# fec-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/fec-to-sqlite.svg)](https://pypi.org/project/fec-to-sqlite/)
[![CircleCI](https://circleci.com/gh/simonw/fec-to-sqlite.svg?style=svg)](https://circleci.com/gh/simonw/fec-to-sqlite)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/fec-to-sqlite/blob/master/LICENSE)

Create a SQLite database using FEC campaign contributions data.

This tool builds on [fecfile](https://github.com/esonderegger/fecfile) by Evan Sonderegger.

## How to install

    $ pip install fec-to-sqlite

## Usage

    $ fec-to-sqlite filings filings.db 1146148

This fetches the filing with ID `1146148` and stores it in tables in a SQLite database called `filings.db`. It will create any tables it needs.

You can pass more than one filing ID, separated by spaces.
