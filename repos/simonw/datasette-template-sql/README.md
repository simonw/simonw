# datasette-template-sql

[![PyPI](https://img.shields.io/pypi/v/datasette-template-sql.svg)](https://pypi.org/project/datasette-template-sql/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-template-sql?include_prereleases&label=changelog)](https://github.com/simonw/datasette-template-sql/releases)
[![Tests](https://github.com/simonw/datasette-template-sql/workflows/Test/badge.svg)](https://github.com/simonw/datasette-template-sql/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-template-sql/blob/main/LICENSE)

Datasette plugin for executing SQL queries from templates.

## Examples

[datasette.io](https://datasette.io/) uses this plugin extensively with [custom page templates](https://docs.datasette.io/en/stable/custom_templates.html#custom-pages), check out [simonw/datasette.io](https://github.com/simonw/datasette.io) to see how it works.

[www.niche-museums.com](https://www.niche-museums.com/) uses this plugin to run a custom themed website on top of Datasette. The full source code for the site [is here](https://github.com/simonw/museums) - see also [niche-museums.com, powered by Datasette](https://simonwillison.net/2019/Nov/25/niche-museums/).

[simonw/til](https://github.com/simonw/til) is another simple example, described in [Using a self-rewriting README powered by GitHub Actions to track TILs](https://simonwillison.net/2020/Apr/20/self-rewriting-readme/).

## Installation

Run this command to install the plugin in the same environment as Datasette:

    $ pip install datasette-template-sql

## Usage

This plugin makes a new function, `sql(sql_query)`, available to your Datasette templates.

You can use it like this:

```html+jinja
{% for row in sql("select 1 + 1 as two, 2 * 4 as eight") %}
    {% for key in row.keys() %}
        {{ key }}: {{ row[key] }}<br>
    {% endfor %}
{% endfor %}
```

The plugin will execute SQL against the current database for the page in  `database.html`, `table.html` and `row.html` templates. If a template does not have a current database (`index.html` for example) the query will execute against the first attached database.

### Queries with arguments

You can construct a SQL query using `?` or `:name` parameter syntax by passing a list or dictionary as a second argument:

```html+jinja
{% for row in sql("select distinct topic from til order by topic") %}
    <h2>{{ row.topic }}</h2>
    <ul>
        {% for til in sql("select * from til where topic = ?", [row.topic]) %}
            <li><a href="{{ til.url }}">{{ til.title }}</a> - {{ til.created[:10] }}</li>
        {% endfor %}
    </ul>
{% endfor %}
```

Here's the same example using the `:topic` style of parameters:

```html+jinja
{% for row in sql("select distinct topic from til order by topic") %}
    <h2>{{ row.topic }}</h2>
    <ul>
        {% for til in sql("select * from til where topic = :topic", {"topic": row.topic}) %}
            <li><a href="{{ til.url }}">{{ til.title }}</a> - {{ til.created[:10] }}</li>
        {% endfor %}
    </ul>
{% endfor %}
```

### Querying a different database

You can pass an optional `database=` argument to specify a named database to use for the query. For example, if you have attached a `news.db` database you could use this:

```html+jinja
{% for article in sql(
    "select headline, date, summary from articles order by date desc limit 5",
    database="news"
) %}
    <h3>{{ article.headline }}</h2>
    <p class="date">{{ article.date }}</p>
    <p>{{ article.summary }}</p>
{% endfor %}
```
