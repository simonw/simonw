# datasette-sitemap

[![PyPI](https://img.shields.io/pypi/v/datasette-sitemap.svg)](https://pypi.org/project/datasette-sitemap/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-sitemap?include_prereleases&label=changelog)](https://github.com/simonw/datasette-sitemap/releases)
[![Tests](https://github.com/simonw/datasette-sitemap/workflows/Test/badge.svg)](https://github.com/simonw/datasette-sitemap/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-sitemap/blob/main/LICENSE)

Generate sitemap.xml for Datasette sites

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-sitemap

## Demo

This plugin is used for the sitemap on [til.simonwillison.net](https://til.simonwillison.net/):

- https://til.simonwillison.net/sitemap.xml

Here's [the configuration](https://github.com/simonw/til/blob/d4f67743a90a67100b46145986b2dec6f8d96583/metadata.yaml#L14-L16) used for that sitemap.

## Usage

Once configured, this plugin adds a sitemap at `/sitemap.xml` with a list of URLs.

This list is defined using a SQL query in `metadata.json` (or `.yml`) that looks like this:

```json
{
  "plugins": {
    "datasette-sitemap": {
      "query": "select '/' || id as path from my_table"
    }
  }
}
```

Using `metadata.yml` allows for multi-line SQL queries which can be easier to maintain:

```yaml
plugins:
  datasette-sitemap:
    query: |
      select
        '/' || id as path
      from
        my_table
```
The SQL query must return a column called `path`. The values in this column must begin with a `/`. They will be used to generate a sitemap that looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/1</loc></url>
  <url><loc>https://example.com/2</loc></url>
</urlset>
```
You can use ``UNION`` in your SQL query to combine results from multiple tables, or include literal paths that you want to include in the index:

```sql
select
  '/data/table1/' || id as path
  from table1
union
select
  '/data/table2/' || id as path
  from table2
union
select
  '/about' as path
```
If your Datasette instance has multiple databases you can configure the database to query using the `database` configuration property.

By default the domain name for the genearted URLs in the sitemap will be detected from the incoming request.

You can set `base_url` instead to override this. This should not include a trailing slash.

This example shows both of those settings, running the query against the `content` database and setting a custom base URL:

```yaml
plugins:
  datasette-sitemap:
    query: |
      select '/plugins/' || name as path from plugins
      union
      select '/tools/' || name as path from tools
      union
      select '/news' as path
    database: content
    base_url: https://datasette.io
```
[Try that query](https://datasette.io/content?sql=select+%27%2Fplugins%2F%27+||+name+as+path+from+plugins%0D%0Aunion%0D%0Aselect+%27%2Ftools%2F%27+||+name+as+path+from+tools%0D%0Aunion%0D%0Aselect+%27%2Fnews%27+as+path%0D%0A).

## robots.txt

This plugin adds a `robots.txt` file pointing to the sitemap:

```
Sitemap: http://example.com/sitemap.xml
```

You can take full control of the sitemap by installing and configuring the [datasette-block-robots](https://datasette.io/plugins/datasette-block-robots) plugin.

This plugin will add the `Sitemap:` line even if you are using `datasette-block-robots` for the rest of your `robots.txt` file.

## Adding paths to the sitemap from other plugins

This plugin adds a new [plugin hook](https://docs.datasette.io/en/stable/plugin_hooks.html) to Datasete called `sitemap_extra_paths()` which can be used by other plugins to add their own additional lines to the `sitemap.xml` file.

The hook accepts these optional parameters:

- `datasette`: The current [Datasette instance](https://docs.datasette.io/en/stable/internals.html#datasette-class). You can use this to execute SQL queries or read plugin configuration settings.
- `request`: The [Request object](https://docs.datasette.io/en/stable/internals.html#request-object) representing the incoming request to `/sitemap.xml`.

The hook should return a list of strings, each representing a path to be added to the sitemap. Each path must begin with a `/`.

It can also return an `async def` function, which will be awaited and used to generate a list of lines. Use this option if you need to make `await` calls inside you hook implementation.

This example uses the hook to add two extra paths, one of which came from a SQL query:

```python
from datasette import hookimpl

@hookimpl
def sitemap_extra_paths(datasette):
    async def inner():
        db = datasette.get_database()
        path_from_db = (await db.execute("select '/example'")).single_value()
        return ["/about", path_from_db]
    return inner
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-sitemap
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
