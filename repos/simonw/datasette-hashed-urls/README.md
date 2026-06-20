# datasette-hashed-urls

[![PyPI](https://img.shields.io/pypi/v/datasette-hashed-urls.svg)](https://pypi.org/project/datasette-hashed-urls/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-hashed-urls?include_prereleases&label=changelog)](https://github.com/simonw/datasette-hashed-urls/releases)
[![Tests](https://github.com/simonw/datasette-hashed-urls/workflows/Test/badge.svg)](https://github.com/simonw/datasette-hashed-urls/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-hashed-urls/blob/main/LICENSE)

Optimize Datasette performance behind a caching proxy

When you open a database file in immutable mode using the `-i` option, Datasette calculates a SHA-256 hash of the contents of that file on startup.

This content hash can then optionally be used to create URLs that are guaranteed to change if the contents of the file changes in the future.

The result is pages  that can be cached indefinitely by both browsers and caching proxies - providing a significant performance boost.

## Demo

A demo of this plugin is running at https://datasette-hashed-urls.vercel.app/

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-hashed-urls

## Usage

Once installed, this plugin will act on any immutable database files that are loaded into Datasette:

    datasette -i fixtures.db

The database will automatically be renamed to incorporate a hash of the contents of the SQLite file - so the above database would be served as:

    http://127.0.0.1:8001/fixtures-aa7318b

Every page that accesss that database, including JSON endpoints, will be served with the following far-future cache expiry header:

    cache-control: max-age=31536000, public

Here `max-age=31536000` is the number of seconds in a year.

A caching proxy such as Cloudflare can then be used to cache and accelerate content served by Datasette.

When the database file is updated and the server is restarted, the hash will change and content will be served from a new URL. Any hits to the previous hashed URLs will be automatically redirected.

If you run Datasette using the `--crossdb` option to enable [cross-database queries](https://docs.datasette.io/en/stable/sql_queries.html#cross-database-queries) the `_memory` database will also have a hash added to its URL - in this case, the hash will be a combination of the hashes of the other attached databases.

## Configuration

You can use the `max_age` plugin configuration setting to change the cache duration specified in the `cache-control` HTTP header.

To set the cache expiry time to one hour you would add this to your Datasette `metadata.json` configuration file:

```json
{
    "plugins": {
        "datasette-hashed-urls": {
            "max_age": 3600
        }
    }
}
```

## History

This functionality used to ship as part of Datasette itself, as a feature called [Hashed URL mode](https://docs.datasette.io/en/0.60.2/performance.html#hashed-url-mode).

That feature has been deprecated and will be removed in Datasette 1.0. This plugin should be used as an alternative.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-hashed-urls
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
