# datasette-tiddlywiki

[![PyPI](https://img.shields.io/pypi/v/datasette-tiddlywiki.svg)](https://pypi.org/project/datasette-tiddlywiki/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-tiddlywiki?include_prereleases&label=changelog)](https://github.com/simonw/datasette-tiddlywiki/releases)
[![Tests](https://github.com/simonw/datasette-tiddlywiki/workflows/Test/badge.svg)](https://github.com/simonw/datasette-tiddlywiki/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-tiddlywiki/blob/main/LICENSE)

Run [TiddlyWiki](https://tiddlywiki.com/) in Datasette and save Tiddlers to a SQLite database

Read more about this project [on my blog](https://simonwillison.net/2021/Dec/24/datasette-tiddlywiki/).

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-tiddlywiki

## Usage

Start Datasette with a `tiddlywiki.db` database. You can create it if it does not yet exist using `--create`.

You need to be signed in as the `root` user to write to the wiki, so use the `--root` option and click on the link it provides:

    % datasette tiddlywiki.db --create --root
    http://127.0.0.1:8001/-/auth-token?token=456670f1e8d01a8a33b71e17653130de17387336e29afcdfb4ab3d18261e6630
    # ...

Navigate to `/-/tiddlywiki` on your instance to interact with TiddlyWiki.

## Authentication and permissions

By default, the wiki can be read by anyone who has permission to read the `tiddlywiki.db` database. Only the signed in `root` user can write to it.

You can sign in using the `--root` option described above, or you can set a password for that user using the [datasette-auth-passwords](https://datasette.io/plugins/datasette-auth-passwords) plugin and sign in using the `/-/login` page.

You can use the `edit-tiddlywiki` permission to grant edit permisions to other users, using another plugin such as [datasette-permissions-sql](https://datasette.io/plugins/datasette-permissions-sql).

You can use the `view-database` permission against the `tiddlywiki` database to control who can view the wiki.

Datasette's permissions mechanism is described in full in [the Datasette documentation](https://docs.datasette.io/en/stable/authentication.html).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-tiddlywiki
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
