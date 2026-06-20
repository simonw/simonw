# dogsheep-beta

[![PyPI](https://img.shields.io/pypi/v/dogsheep-beta.svg)](https://pypi.org/project/dogsheep-beta/)
[![Changelog](https://img.shields.io/github/v/release/dogsheep/beta?include_prereleases&label=changelog)](https://github.com/dogsheep/beta/releases)
[![Tests](https://github.com/dogsheep/beta/workflows/Test/badge.svg)](https://github.com/dogsheep/beta/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dogsheep/beta/blob/main/LICENSE)

Build a search index across content from multiple SQLite database tables and run faceted searches against it using Datasette

## Example

A live example of this plugin is running at https://datasette.io/-/beta - configured using [this YAML file](https://github.com/simonw/datasette.io/blob/main/templates/dogsheep-beta.yml).

Read more about how this example works in [Building a search engine for datasette.io](https://simonwillison.net/2020/Dec/19/dogsheep-beta/).

## Installation

Install this tool like so:

    $ pip install dogsheep-beta

## Usage

Run the indexer using the `dogsheep-beta` command-line tool:

    $ dogsheep-beta index dogsheep.db config.yml

The `config.yml` file contains details of the databases and document types that should be indexed:

```yaml
twitter.db:
    tweets:
        sql: |-
            select
                tweets.id as key,
                'Tweet by @' || users.screen_name as title,
                tweets.created_at as timestamp,
                tweets.full_text as search_1
            from tweets join users on tweets.user = users.id
    users:
        sql: |-
            select
                id as key,
                name || ' @' || screen_name as title,
                created_at as timestamp,
                description as search_1
            from users
```

This will create a `search_index` table in the `dogsheep.db` database populated by data from those SQL queries.

By default the search index that this tool creates will be configured for Porter stemming. This means that searches for words like `run` will match documents containing `runs` or `running`.

If you don't want to use Porter stemming, use the `--tokenize none` option:

    $ dogsheep-beta index dogsheep.db config.yml --tokenize none

You can pass other SQLite tokenize argumenst here, see [the SQLite FTS tokenizers documentation](https://www.sqlite.org/fts5.html#tokenizers).

## Columns

The columns that can be returned by our query are:

- `key` - a unique (within that type) primary key
- `title` - the title for the item
- `timestamp` - an ISO8601 timestamp, e.g. `2020-09-02T21:00:21`
- `search_1` - a larger chunk of text to be included in the search index
- `category` - an integer category ID, see below
- `is_public` - an integer (0 or 1, defaults to 0 if not set) specifying if this is public or not

Public records are things like your public tweets, blog posts and GitHub commits.

## Categories

Indexed items can be assigned a category. Categories are integers that correspond to records in the `categories` table, which defaults to containing the following:

|   id | name       |
|------|------------|
|    1 | created    |
|    2 | saved      |
|    3 | received   |

`created` is for items that have been created by the Dogsheep instance owner.

`saved` is for items that they have saved, liked or favourited.

`received` is for items that have been specifically sent to them by other people - incoming emails or direct messages for example.

## Datasette plugin

Run `datasette install dogsheep-beta` (or use `pip install dogsheep-beta` in the same environment as Datasette) to install the Dogsheep Beta Datasette plugin.

Once installed, a custom search interface will be made available at `/-/beta`. You can use this interface to execute searches.

The Datasette plugin has some configuration options. You can set these by adding the following to your `metadata.json` configuration file:

```json
{
    "plugins": {
        "dogsheep-beta": {
            "database": "beta",
            "config_file": "dogsheep-beta.yml",
            "template_debug": true
        }
    }
}
```
The configuration settings for the plugin are:
- `database` - the database file that contains your search index. If the file is `beta.db` you should set `database` to `beta`.
- `config_file` - the YAML file containing your Dogsheep Beta configuration.
- `template_debug` - set this to `true` to enable debugging output if errors occur in your custom templates, see below.

## Custom results display

Each indexed item type can define custom display HTML as part of the `config.yml` file. It can do this using a `display` key containing a fragment of Jinja template, and optionally a `display_sql` key with extra SQL to execute to fetch the data to display.

Here's how to define a custom display template for a tweet:

```yaml
twitter.db:
    tweets:
        sql: |-
            select
                tweets.id as key,
                'Tweet by @' || users.screen_name as title,
                tweets.created_at as timestamp,
                tweets.full_text as search_1
            from tweets join users on tweets.user = users.id
        display: |-
            <p>{{ title }} - tweeted at {{ timestamp }}</p>
            <blockquote>{{ search_1 }}</blockquote>
```
This example reuses the value that were stored in the `search_index` table when the indexing query was run.

To load in extra values to display in the template, use a `display_sql` query like this:

```yaml
twitter.db:
    tweets:
        sql: |-
            select
                tweets.id as key,
                'Tweet by @' || users.screen_name as title,
                tweets.created_at as timestamp,
                tweets.full_text as search_1
            from tweets join users on tweets.user = users.id
        display_sql: |-
            select
                users.screen_name,
                tweets.full_text,
                tweets.created_at
            from
                tweets join users on tweets.user = users.id
            where
                tweets.id = :key
        display: |-
            <p>{{ display.screen_name }} - tweeted at {{ display.created_at }}</p>
            <blockquote>{{ display.full_text }}</blockquote>
```
The `display_sql` query will be executed for every search result, passing the key value from the `search_index` table as the `:key` parameter and the user's search term as the `:q` parameter.

This performs well because [many small queries are efficient in SQLite](https://www.sqlite.org/np1queryprob.html).

If an error occurs while rendering one of your templates the search results page will return a 500 error. You can use the `template_debug` configuration setting described above to instead output debugging information for the search results item that experienced the error.

## Displaying maps

This plugin will eventually include a number of useful shortcuts for rendering interesting content.

The first available shortcut is for displaying maps. Make your custom content output something like this:

```html
<div
    data-map-latitude="{{ display.latitude }}"
    data-map-longitude="{{ display.longitude }}"
    style="display: none; float: right; width: 250px; height: 200px; background-color: #ccc;"
></div>
```
JavaScript on the page will look for any elements with `data-map-latitude` and `data-map-longitude` and, if it finds any, will load Leaflet and convert those elements into maps centered on that location. The default zoom level will be 12, or you can set a `data-map-zoom` attribute to customize this.

## Development

To run the tests:

    uv run pytest

To run tests against Datasette pre-1.0:

    uv run --with 'datasette<1.0' pytest

To run tests against Datasette 1.0 and higher:

    uv run --with 'datasette>=1.0a26' pytest
