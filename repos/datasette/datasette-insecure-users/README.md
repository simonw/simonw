# datasette-insecure-users

[![PyPI](https://img.shields.io/pypi/v/datasette-insecure-users.svg)](https://pypi.org/project/datasette-insecure-users/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-insecure-users?include_prereleases&label=changelog)](https://github.com/datasette/datasette-insecure-users/releases)
[![Tests](https://github.com/datasette/datasette-insecure-users/workflows/Test/badge.svg)](https://github.com/datasette/datasette-insecure-users/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-insecure-users/blob/main/LICENSE)

A username/password Datasette authentication plugin, where passwords are optional. Meant for debugging and private trusted instances!

## Installation

This plugin requires an alpha version of Datasette 1.0.

    pip install datasette==1.0a6

Then you can nstall this plugin in the same environment as Datasette.

    datasette install datasette-insecure-users

## Usage

Once installed, there will be a new "Log in" option in the upper-right hand menu. Users can then either login with a username/password, or with just a username.

If a password is provided, then future logins will require that same password. If no password is provided when logging in for the first time, then no password is needed in future login attempts.

Passwords are salted + hashed and stored in the new [Datasette internal database](https://docs.datasette.io/en/latest/internals.html#datasette-s-internal-database). By default this is an in-memory database that will disappear when Datasette exists, so to persist login information for all users, pass in a SQLite database with `--internal` like so:

    datasette --internal internal.db my_data.db

In this case, usernames/hashed passwords will be stored in `internal.db`, and `my_data.db` will be left untouched.

## Internals

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-insecure-users
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
