# datasette-permissions-sql

[![PyPI](https://img.shields.io/pypi/v/datasette-permissions-sql.svg)](https://pypi.org/project/datasette-permissions-sql/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-permissions-sql.svg?style=svg)](https://circleci.com/gh/simonw/datasette-permissions-sql)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-permissions-sql/blob/master/LICENSE)

Datasette plugin for configuring permission checks using SQL queries

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-permissions-sql

## Usage

First, read up on how Datasette's [authentication and permissions system](https://datasette.readthedocs.io/en/latest/authentication.html) works.

This plugin lets you define rules containing SQL queries that are executed to see if the currently authenticated actor has permission to perform certain actions.

Consider a canned query which authenticated users should only be able to execute if a row in the `users` table says that they are a member of staff.

That `users` table in the `mydatabase.db` database could look like this:

| id | username | is_staff |
|--|--------|--------|
| 1 | cleopaws | 0 |
| 2 | simon | 1 |

Authenticated users have an `actor` that looks like this:

```json
{
    "id": 2,
    "username": "simon"
}
```

To configure the canned query to only be executable by staff users, add the following to your `metadata.json`:

```json
{
    "plugins": {
        "datasette-permissions-sql": [
            {
                "action": "view-query",
                "resource": ["mydatabase", "promote_to_staff"],
                "sql": "SELECT * FROM users WHERE is_staff = 1 AND id = :actor_id"
            }
        ]
    },
    "databases": {
        "mydatabase": {
            "queries": {
                "promote_to_staff": {
                    "sql": "UPDATE users SET is is_staff=1 WHERE id=:id",
                    "write": true
                }
            }
        }
    }
}
```

The `"datasette-permissions-sql"` key is a list of rules. Each of those rules has the following shape:

```json
{
    "action": "name-of-action",
    "resource": ["resource identifier to run this on"],
    "sql": "SQL query to execute",
    "database": "mydatabase"
}
```

Both `"action"` and `"resource"` are optional. If present, the SQL query will only be executed on permission checks that match the action and, if present, the resource indicators.

`"database"` is also optional: it specifies the named database that the query should be executed against. If it is not present the first connected database will be used.

The Datasette documentation includes a [list of built-in permissions](https://datasette.readthedocs.io/en/stable/authentication.html#built-in-permissions) that you might want to use here.

### The SQL query

If the SQL query returns any rows the action will be allowed. If it returns no rows, the plugin hook will return `False` and deny access to that action.

The SQL query is called with a number of named parameters. You can use any of these as part of the query.

The list of parameters is as follows:

* `action` - the action, e.g. `"view-database"`
* `resource_1` - the first component of the resource, if one was passed
* `resource_2` - the second component of the resource, if available
* `actor_*` - a parameter for every key on the actor. Usually `actor_id` is present.

If any rows are returned, the permission check passes. If no rows are returned the check fails.

Another example table, this time granting explicit access to individual tables. Consider a table called `table_access` that looks like this:

| user_id | database | table |
| - | - | - |
| 1 | mydb | dogs |
| 2 | mydb | dogs |
| 1 | mydb | cats |

The following SQL query would grant access to the `dogs` ttable in the `mydb.db` database to users 1 and 2 - but would forbid access for user 2 to the `cats` table:

```sql
SELECT
    *
FROM
    table_access
WHERE
    user_id = :actor_id
    AND "database" = :resource_1
    AND "table" = :resource_2
```
In a `metadata.yaml` configuration file that would look like this:

```yaml
databases:
  mydb:
    allow_sql: {}
plugins:
  datasette-permissions-sql:
  - action: view-table
    sql: |-
      SELECT
        *
      FROM
        table_access
      WHERE
        user_id = :actor_id
        AND "database" = :resource_1
        AND "table" = :resource_2
```
We're using `allow_sql: {}` here to disable arbitrary SQL queries. This prevents users from running `select * from cats` directly to work around the permissions limits.

### Fallback mode

The default behaviour of this plugin is to take full control of specified permissions. The SQL query will directly control if the user is allowed or denied access to the permission.

This means that the default policy for each permission (which in Datasette core is "allow" for `view-database` and friends) will be ignored. It also means that any other `permission_allowed` plugins will not get their turn once this plugin has executed.

You can change this on a per-rule basis using ``"fallback": true``:

```json
{
    "action": "view-table",
    "resource": ["mydatabase", "mytable"],
    "sql": "select * from admins where user_id = :actor_id",
    "fallback": true
}
```

When running in fallback mode, a query result returning no rows will cause the plugin hook to return ``None`` - which means "I have no opinion on this permission, fall back to other plugins or the default".

In this mode you can still return `False` (for "deny access") by returning a single row with a single value of `-1`. For example:

```json
{
    "action": "view-table",
    "resource": ["mydatabase", "mytable"],
    "sql": "select -1 from banned where user_id = :actor_id",
    "fallback": true
}
```
