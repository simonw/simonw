# datasette-block-robots

[![PyPI](https://img.shields.io/pypi/v/datasette-block-robots.svg)](https://pypi.org/project/datasette-block-robots/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-block-robots?label=changelog)](https://github.com/simonw/datasette-block-robots/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-block-robots/blob/master/LICENSE)

Datasette plugin that blocks robots and crawlers using robots.txt

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-block-robots

## Usage

Having installed the plugin, `/robots.txt` on your Datasette instance will return the following:

    User-agent: *
    Disallow: /

This will request all robots and crawlers not to visit any of the pages on your site.

Here's a demo of the plugin in action: https://sqlite-generate-demo.datasette.io/robots.txt

## Configuration

By default the plugin will block all access to the site, using `Disallow: /`.

If you want the index page to be indexed by search engines without crawling the database, table or row pages themselves, you can use the following:

```json
{
    "plugins": {
        "datasette-block-robots": {
            "allow_only_index": true
        }
    }
}
```
This will return a `/robots.txt` like so:

    User-agent: *
    Disallow: /db1
    Disallow: /db2

With a `Disallow` line for every attached database.

To block access to specific areas of the site using custom paths, add this to your `metadata.json` configuration file:

```json
{
    "plugins": {
        "datasette-block-robots": {
            "disallow": ["/mydatabase/mytable"]
        }
    }
}
```
This will result in a `/robots.txt` that looks like this:

    User-agent: *
    Disallow: /mydatabase/mytable

Alternatively you can set the full contents of the `robots.txt` file using the `literal` configuration option. Here's how to do that if you are using YAML rather than JSON and have a `metadata.yml` file:

```yaml
plugins:
    datasette-block-robots:
        literal: |-
            User-agent: *
            Disallow: /
            User-agent: Bingbot
            User-agent: Googlebot
            Disallow:
```
This example would block all crawlers with the exception of Googlebot and Bingbot, which are allowed to crawl the entire site.

## Extending this with other plugins

This plugin adds a new [plugin hook](https://docs.datasette.io/en/stable/plugin_hooks.html) to Datasete called `block_robots_extra_lines()` which can be used by other plugins to add their own additional lines to the `robots.txt` file.

The hook can optionally accept these parameters:

- `datasette`: The current [Datasette instance](https://docs.datasette.io/en/stable/internals.html#datasette-class). You can use this to execute SQL queries or read plugin configuration settings.
- `request`: The [Request object](https://docs.datasette.io/en/stable/internals.html#request-object) representing the incoming request to `/robots.txt`.

The hook should return a list of strings, each representing a line to be added to the `robots.txt` file.

It can also return an `async def` function, which will be awaited and used to generate a list of lines. Use this option if you need to make `await` calls inside you hook implementation.

This example uses the hook to add a `Sitemap: http://example.com/sitemap.xml` line to the `robots.txt` file:

```python
from datasette import hookimpl

@hookimpl
def block_robots_extra_lines(datasette, request):
    return [
        "Sitemap: {}".format(datasette.absolute_url(request, "/sitemap.xml")),
    ]
```
This example blocks access to paths based on a database query:

```python
@hookimpl
def block_robots_extra_lines(datasette):
    async def inner():
        db = datasette.get_database()
        result = await db.execute("select path from mytable")
        return [
            "Disallow: /{}".format(row["path"]) for row in result
        ]
    return inner
```
[datasette-sitemap](https://datasette.io/plugins/datasette-sitemap) is an example of a plugin that uses this hook.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-block-robots
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
