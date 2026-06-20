# datasette-graphql

[![PyPI](https://img.shields.io/pypi/v/datasette-graphql.svg)](https://pypi.org/project/datasette-graphql/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-graphql?include_prereleases&label=changelog)](https://github.com/simonw/datasette-graphql/releases)
[![Tests](https://github.com/simonw/datasette-graphql/workflows/Test/badge.svg)](https://github.com/simonw/datasette-graphql/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-graphql/blob/main/LICENSE)

**Datasette plugin providing an automatic GraphQL API for your SQLite databases**

Read more about this project: [GraphQL in Datasette with the new datasette-graphql plugin](https://simonwillison.net/2020/Aug/7/datasette-graphql/)

<!-- Try out a live demo at [datasette-graphql-demo.datasette.io/graphql](https://datasette-graphql-demo.datasette.io/graphql?query=%7B%0A%20%20repos(first%3A10%2C%20search%3A%20%22sql%22%2C%20sort_desc%3A%20created_at)%20%7B%0A%20%20%20%20totalCount%0A%20%20%20%20pageInfo%20%7B%0A%20%20%20%20%20%20endCursor%0A%20%20%20%20%20%20hasNextPage%0A%20%20%20%20%7D%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20description_%0A%20%20%20%20%09stargazers_count%0A%20%20%20%20%20%20created_at%0A%20%20%20%20%20%20owner%20%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20html_url%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

<!-- toc -->

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  * [Querying for tables and columns](#querying-for-tables-and-columns)
  * [Fetching a single record](#fetching-a-single-record)
  * [Accessing nested objects](#accessing-nested-objects)
  * [Accessing related objects](#accessing-related-objects)
  * [Filtering tables](#filtering-tables)
  * [Sorting](#sorting)
  * [Pagination](#pagination)
  * [Search](#search)
  * [Columns containing JSON strings](#columns-containing-json-strings)
  * [Auto camelCase](#auto-camelcase)
  * [CORS](#cors)
  * [Execution limits](#execution-limits)
- [The graphql() template function](#the-graphql-template-function)
- [Adding custom fields with plugins](#adding-custom-fields-with-plugins)
- [Development](#development)

<!-- tocstop -->

![Animated demo showing autocomplete while typing a GraphQL query into the GraphiQL interface](https://static.simonwillison.net/static/2020/graphiql.gif)

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-graphql

## Configuration

By default this plugin adds the GraphQL API at `/graphql`. You can configure a different path using the `path` plugin setting, for example by adding this to `metadata.json`:
```json
{
  "plugins": {
    "datasette-graphql": {
      "path": "/-/graphql"
    }
  }
}
```
This will set the GraphQL API to live at `/-/graphql` instead.

## Usage

This plugin sets up `/graphql` as a GraphQL endpoint for the first attached database.

If you have multiple attached databases each will get its own endpoint at `/graphql/name_of_database`.

The automatically generated GraphQL schema is available at `/graphql/name_of_database.graphql`<!-- - here's [an example](https://datasette-graphql-demo.datasette.io/graphql/github.graphql) -->.

### Querying for tables and columns

Individual tables (and SQL views) can be queried like this:

```graphql
{
  repos {
    nodes {
      id
      full_name
      description_
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos%20%7B%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20description_%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

In this example query the underlying database table is called `repos` and its columns include `id`, `full_name` and `description`. Since `description` is a reserved word the query needs to ask for `description_` instead.

### Fetching a single record

If you only want to fetch a single record - for example if you want to fetch a row by its primary key - you can use the `tablename_row` field:

```graphql
{
  repos_row(id: 107914493) {
    id
    full_name
    description_
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos_row%28id%3A%20107914493%29%20%7B%0A%20%20%20%20id%0A%20%20%20%20full_name%0A%20%20%20%20description_%0A%20%20%7D%0A%7D%0A) -->

The `tablename_row` field accepts the primary key column (or columns) as arguments. It also supports the same `filter:`, `search:`, `sort:` and `sort_desc:` arguments as the `tablename` field, described below.

### Accessing nested objects

If a column is a foreign key to another table, you can request columns from the table pointed to by that foreign key using a nested query like this:

```graphql
{
  repos {
    nodes {
      id
      full_name
      owner {
        id
        login
      }
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos%20%7B%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20owner%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20login%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

### Accessing related objects

If another table has a foreign key back to the table you are accessing, you can fetch rows from that related table.

Consider a `users` table which is related to `repos` - a repo has a foreign key back to the user that owns the repository. The `users` object type will have a `repos_by_owner_list` field which can be used to access those related repos:

```graphql
{
  users(first: 1, search: "simonw") {
    nodes {
      name
      repos_by_owner_list(first: 5) {
        totalCount
        nodes {
          full_name
        }
      }
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20users%28first%3A%201%2C%20search%3A%20%22simonw%22%29%20%7B%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20repos_by_owner_list%28first%3A%205%29%20%7B%0A%20%20%20%20%20%20%20%20totalCount%0A%20%20%20%20%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->


### Filtering tables

You can filter the rows returned for a specific table using the `filter:` argument. This accepts a filter object mapping columns to operations. For example, to return just repositories with the Apache 2 license and more than 10 stars:

```graphql
{
  repos(filter: {license: {eq: "apache-2.0"}, stargazers_count: {gt: 10}}) {
    nodes {
      full_name
      stargazers_count
      license {
        key
      }
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos%28filter%3A%20%7Blicense%3A%20%7Beq%3A%20%22apache-2.0%22%7D%2C%20stargazers_count%3A%20%7Bgt%3A%2010%7D%7D%29%20%7B%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20stargazers_count%0A%20%20%20%20%20%20license%20%7B%0A%20%20%20%20%20%20%20%20key%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

See [table filters examples](https://github.com/simonw/datasette-graphql/blob/main/examples/filters.md) for more operations, and [column filter arguments](https://docs.datasette.io/en/stable/json_api.html#column-filter-arguments) in the Datasette documentation for details of how those operations work.

These same filters can be used on nested relationships, like so:

```graphql
{
  users_row(id: 9599) {
    name
    repos_by_owner_list(filter: {name: {startswith: "datasette-"}}) {
      totalCount
      nodes {
        full_name
      }
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20users_row%28id%3A%209599%29%20%7B%0A%20%20%20%20name%0A%20%20%20%20repos_by_owner_list%28filter%3A%20%7Bname%3A%20%7Bstartswith%3A%20%22datasette-%22%7D%7D%29%20%7B%0A%20%20%20%20%20%20totalCount%0A%20%20%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->


The `where:` argument can be used as an alternative to `filter:` when the thing you are expressing is too complex to be modeled using a filter expression. It accepts a string fragment of SQL that will be included in the `WHERE` clause of the SQL query.

```graphql
{
  repos(where: "name='sqlite-utils' or name like 'datasette-%'") {
    totalCount
    nodes {
      full_name
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos%28where%3A%20%22name%3D%27sqlite-utils%27%20or%20name%20like%20%27datasette-%25%27%22%29%20%7B%0A%20%20%20%20totalCount%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

### Sorting

You can set a sort order for results from a table using the `sort:` or `sort_desc:` arguments. The value for this argument should be the name of the column you wish to sort (or sort-descending) by.

```graphql
{
  repos(sort_desc: stargazers_count) {
    nodes {
      full_name
      stargazers_count
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos%28sort_desc%3A%20stargazers_count%29%20%7B%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20stargazers_count%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

### Pagination

By default the first 10 rows will be returned. You can control this using the `first:` argument.

```graphql
{
  repos(first: 20) {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      full_name
      stargazers_count
      license {
        key
      }
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos%28first%3A%2020%29%20%7B%0A%20%20%20%20totalCount%0A%20%20%20%20pageInfo%20%7B%0A%20%20%20%20%20%20hasNextPage%0A%20%20%20%20%20%20endCursor%0A%20%20%20%20%7D%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20stargazers_count%0A%20%20%20%20%20%20license%20%7B%0A%20%20%20%20%20%20%20%20key%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

The `totalCount` field returns the total number of records that match the query.

Requesting the `pageInfo.endCursor` field provides you with the value you need to request the next page. You can pass this to the `after:` argument to request the next page.

```graphql
{
  repos(first: 20, after: "134874019") {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      full_name
      stargazers_count
      license {
        key
      }
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos%28first%3A%2020%2C%20after%3A%20%22134874019%22%29%20%7B%0A%20%20%20%20totalCount%0A%20%20%20%20pageInfo%20%7B%0A%20%20%20%20%20%20hasNextPage%0A%20%20%20%20%20%20endCursor%0A%20%20%20%20%7D%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20stargazers_count%0A%20%20%20%20%20%20license%20%7B%0A%20%20%20%20%20%20%20%20key%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

The `hasNextPage` field tells you if there are any more records.

### Search

If a table has been configured to use SQLite full-text search you can execute searches against it using the `search:` argument:

```graphql
{
  repos(search: "datasette") {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      full_name
      description_
    }
  }
}
```
<!-- [Try this query](https://datasette-graphql-demo.datasette.io/graphql?query=%0A%7B%0A%20%20repos%28search%3A%20%22datasette%22%29%20%7B%0A%20%20%20%20totalCount%0A%20%20%20%20pageInfo%20%7B%0A%20%20%20%20%20%20hasNextPage%0A%20%20%20%20%20%20endCursor%0A%20%20%20%20%7D%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20full_name%0A%20%20%20%20%20%20description_%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A) -->

The [sqlite-utils](https://sqlite-utils.datasette.io/) Python library and CLI tool can be used to add full-text search to an existing database table.

### Columns containing JSON strings

If your table has a column that contains data encoded as JSON, `datasette-graphql` will make that column available as an encoded JSON string. Clients calling your API will need to parse the string as JSON in order to access the data.

You can return the data as a nested structure by configuring that column to be treated as a JSON column. The [plugin configuration](https://docs.datasette.io/en/stable/plugins.html#plugin-configuration) for that in `metadata.json` looks like this:

```json
{
    "databases": {
        "test": {
            "tables": {
                "repos": {
                    "plugins": {
                        "datasette-graphql": {
                            "json_columns": [
                                "tags"
                            ]
                        }
                    }
                }
            }
        }
    }
}
```

### Auto camelCase

The names of your columns and tables default to being matched by their representations in GraphQL.

If you have tables with `names_like_this` you may want to work with them in GraphQL using `namesLikeThis`, for consistency with GraphQL and JavaScript conventions.

You can turn on automatic camelCase using the `"auto_camelcase"` plugin configuration setting in `metadata.json`, like this:

```json
{
    "plugins": {
        "datasette-graphql": {
            "auto_camelcase": true
        }
    }
}
```

### CORS

This plugin obeys the `--cors` option passed to the `datasette` command-line tool. If you pass `--cors` it adds the following CORS HTTP headers to allow JavaScript running on other domains to access the GraphQL API:

    access-control-allow-headers: content-type
    access-control-allow-method: POST
    access-control-allow-origin: *

### Execution limits

The plugin implements two limits by default:

- The total time spent executing all of the underlying SQL queries that make up the GraphQL execution must not exceed 1000ms (one second)
- The total number of SQL table queries executed as a result of nested GraphQL fields must not exceed 100

These limits can be customized using the `num_queries_limit` and `time_limit_ms` plugin configuration settings, for example in `metadata.json`:

```json
{
    "plugins": {
        "datasette-graphql": {
            "num_queries_limit": 200,
            "time_limit_ms": 5000
        }
    }
}
```
Setting these to `0` will disable the limit checks entirely.

## The graphql() template function

The plugin also makes a Jinja template function available called `graphql()`. You can use that function in your Datasette [custom templates](https://docs.datasette.io/en/stable/custom_templates.html#custom-templates) like so:

```html+jinja
{% set users = graphql("""
{
    users {
        nodes {
            name
            points
            score
        }
    }
}
""")["users"] %}
{% for user in users.nodes %}
    <p>{{ user.name }} - points: {{ user.points }}, score = {{ user.score }}</p>
{% endfor %}
```

The function executes a GraphQL query against the generated schema and returns the results. You can assign those results to a variable in your template and then loop through and display them.

By default the query will be run against the first attached database. You can use the optional second argument to the function to specify a different database - for example, to run against an attached `github.db` database you would do this:

```html+jinja
{% set user = graphql("""
{
    users_row(id:9599) {
        name
        login
        avatar_url
    }
}
""", "github")["users_row"] %}

<h1>Hello, {{ user.name }}</h1>
```

You can use [GraphQL variables](https://graphql.org/learn/queries/#variables) in these template calls by passing them to the `variables=` argument:

```html+jinja
{% set user = graphql("""
query ($id: Int) {
    users_row(id: $id) {
        name
        login
        avatar_url
    }
}
""", database="github", variables={"id": 9599})["users_row"] %}

<h1>Hello, {{ user.name }}</h1>
```
## Adding custom fields with plugins

`datasette-graphql` adds a new [plugin hook](https://docs.datasette.io/en/stable/writing_plugins.html) to Datasette which can be used to add custom fields to your GraphQL schema.

The plugin hook looks like this:

```python
@hookimpl
def graphql_extra_fields(datasette, database):
    "A list of (name, field_type) tuples to include in the GraphQL schema"
```

You can use this hook to return a list of tuples describing additional fields that should be exposed in your schema. Each tuple should consist of a string naming the new field, plus a [Graphene Field object](https://docs.graphene-python.org/en/latest/types/objecttypes/) that specifies the schema and provides a `resolver` function.

This example implementation uses `pkg_resources` to return a list of currently installed Python packages:

```python
import graphene
from datasette import hookimpl
import pkg_resources


@hookimpl
def graphql_extra_fields():
    class Package(graphene.ObjectType):
        "An installed package"
        name = graphene.String()
        version = graphene.String()

    def resolve_packages(root, info):
        return [
            {"name": d.project_name, "version": d.version}
            for d in pkg_resources.working_set
        ]

    return [
        (
            "packages",
            graphene.Field(
                graphene.List(Package),
                description="List of installed packages",
                resolver=resolve_packages,
            ),
        ),
    ]
```

With this plugin installed, the following GraphQL query can be used to retrieve a list of installed packages:

```graphql
{
  packages {
    name
    version
  }
}
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-graphql
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
