# datasette-auth-tokens

[![PyPI](https://img.shields.io/pypi/v/datasette-auth-tokens.svg)](https://pypi.org/project/datasette-auth-tokens/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-auth-tokens?include_prereleases&label=changelog)](https://github.com/simonw/datasette-auth-tokens/releases)
[![Tests](https://github.com/simonw/datasette-auth-tokens/workflows/Test/badge.svg)](https://github.com/simonw/datasette-auth-tokens/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-auth-tokens/blob/main/LICENSE)

Datasette plugin for authenticating access using API tokens

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-auth-tokens
```
## Managed tokens mode

`datasette-auth-tokens` provides a managed tokens mode, where tokens are stored in a SQLite database table and the plugin provides an interface for creating and revoking tokens.

To turn this mode on, add `"manage_tokens": true` to your plugin configuration:

```json
{
    "plugins": {
        "datasette-auth-tokens": {
            "manage_tokens": true
        }
    }
}
```
This will add a "Create API token" option to the Datasette menu.

Tokens that are created will be kept in a new `_datasette_auth_tokens` table.

Users need the `auth-tokens-create` permission to create tokens. One way to grant that is to add this `"permissions"` block to your configuration:

```json
{
    "permissions": {
        "auth-tokens-create": {
            "id": "*"
        }
    }
}
```

Use the "Create API token" option in the Datasette menu or navigate to `/-/api/tokens` to create tokens and manage tokens.

When you create a new token a signed token string will be presented to you. You need to store this, as it is not stored directly in the database table and can only be retrieved once.

If you have multiple databases attached to Datasette you will need to specify which database should be used for the `_datasette_auth_tokens` table. You can do this with the `manage_tokens_database` setting:

```json
{
    "plugins": {
        "datasette-auth-tokens": {
            "manage_tokens": true,
            "manage_tokens_database": "tokens"
        }
    }
}
```
Now start Datasette like this:
```bash
datasette -c config.json mydb.db tokens.db --create
```
The `--create` option can be used to tell Datasette to create the `tokens.db` database file if it does not already exist.

In Datasette 1.0 you can instead use the `-s` option like this:
```bash
datasette \
  -s plugins.datasette-auth-tokens.manage_tokens true \
  -s plugins.datasette-auth-tokens.manage_tokens_database tokens \
  -s permissions.auth-tokens-create.id '*' # to enable token creation
```

### Viewing tokens

By default, users can only view tokens that they themselves have created on the `/-/api/tokens` page.

Grant the `auth-tokens-view-all` permission to allow a user to view all tokens, even those created by other users.

### Revoking tokens

A token can be revoked by the user that created it by clicking the "Revoke this token" button at the bottom of the token page that is linked to from `/-/api/tokens`.

A user with the `auth-tokens-revoke-all` permission can revoke any token.

## Hard-coded tokens

Read about Datasette's [authentication and permissions system](https://datasette.readthedocs.io/en/latest/authentication.html).

This plugin lets you configure secret API tokens which can be used to make authenticated requests to Datasette.

First, create a random API token. A useful recipe for doing that is the following:
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```
```
5f9a486dd807de632200b17508c75002bb66ca6fde1993db1de6cbd446362589
```
Decide on the actor that this token should represent, for example:

```json
{
    "bot_id": "my-bot"
}
```

You can then use `"allow"` blocks to provide that token with permission to access specific actions. To enable access to a configured writable SQL query you could use this in your `config.json` (for Datasette 1.0) or `metadata.json`: 

```json
{
    "plugins": {
        "datasette-auth-tokens": {
            "tokens": [
                {
                    "token": {
                        "$env": "BOT_TOKEN"
                    },
                    "actor": {
                        "bot_id": "my-bot"
                    }
                }
            ]
        }
    },
    "databases": {
        ":memory:": {
            "queries": {
                "show_version": {
                    "sql": "select sqlite_version()",
                    "allow": {
                        "bot_id": "my-bot"
                    }
                }
            }
        }
    }
}
```
This uses Datasette's [secret configuration values mechanism](https://datasette.readthedocs.io/en/stable/plugins.html#secret-configuration-values) to allow the secret token to be passed as an environment variable.

Run Datasette like this:
```bash
BOT_TOKEN="this-is-the-secret-token" \
    datasette -c config.json
```
You can now run authenticated API queries like this:
```bash
curl -H 'Authorization: Bearer this-is-the-secret-token' \
  'http://127.0.0.1:8001/:memory:/show_version.json?_shape=array'
```
```json
[{"sqlite_version()": "3.31.1"}]
```

## API tokens as a query string parameter

You can allow passing the API token as a query string parameter. This is disabled by default, since URLs with secret tokens need to be handled with care in case they accidentally end up in log files.

Enable this feature using the `param` config value:

```json
{
    "plugins": {
        "datasette-auth-tokens": {
            "tokens": [
                {
                    "token": {
                        "$env": "BOT_TOKEN"
                    },
                    "actor": {
                        "bot_id": "my-bot"
                    },
                }
            ],
            "param": "_auth_token"
        }
    }
}
```

You can now run authenticated API queries like this:
```bash
curl http://127.0.0.1:8001/:memory:/show_version.json?_shape=array&_auth_token=this-is-the-secret-token
```
```json
[{"sqlite_version()": "3.31.1"}]
```

## Custom tokens from your database

If you decide not to use managed tokens mode, you can instead configure `datasette-auth-tokens` to use tokens that are stored in your own custom database tables.

You can do this by configuring a custom SQL query that will execute to test if an incoming token is valid.

Your query needs to take a `:token_id` parameter and return at least two columns: one called `token_secret` and one called `actor_*` - usually `actor_id`. Further `actor_` prefixed columns can be returned to provide more details for the authenticated actor.

Here's a simple example of a configuration query:

```sql
select actor_id, actor_name, token_secret from tokens where token_id = :token_id
```

This can run against a table like this one:

| token_id | token_secret | actor_id | actor_name |
| -------- | ------------ | -------- | ---------- |
| 1        | bd3c94f51fcd | 78       | Cleopaws   |
| 2        | 86681b4d6f66 | 32       | Pancakes   |

The tokens are formed as the token ID, then a hyphen, then the token secret. For example:

- `1-bd3c94f51fcd`
- `2-86681b4d6f66`

The SQL query will be executed with the portion before the hyphen as the `:token_id` parameter.

The `token_secret` value returned by the query will be compared to the portion of the token after the hyphen to check if the token is valid.

Columns with a prefix of `actor_` will be used to populate the actor dictionary. In the above example, a token of `2-86681b4d6f66` will become an actor dictionary of `{"id": 32, "name": "Pancakes"}`.

To configure this, use a `"query"` block in your plugin configuration like this:

```json
{
    "plugins": {
        "datasette-auth-tokens": {
            "query": {
                "sql": "select actor_id, actor_name, token_secret from tokens where token_id = :token_id",
                "database": "tokens"
            }
        }
    },
    "databases": {
        "tokens": {
            "allow": false
        }
    }
}
```
The `"sql"` key here contains the SQL query. The `"database"` key has the name of the attached database file that the query should be executed against - in this case it would execute against `tokens.db`.

### Securing your custom tokens

If you implement the custom pattern above which reads `token_secret` from your own `tokens` table, you need to be aware that anyone with read access to your Datasette instance could read those tokens from your table. This probably isn't what you want!

To avoid this, you should lock down access to that table. The configuration example above shows how to do this using an `"allow": false` block to deny all access to that `tokens` database.

Consult Datasette's [Permissions documentation](https://datasette.readthedocs.io/en/stable/authentication.html#permissions) for more information about how to lock down this kind of access.

## Development

The recommended way to develop this plugin uses [uv](https://github.com/astral-sh/uv). To run the tests:
```bash
cd datasette-auth-tokens
uv run pytest
```
To run a development server with managed tokens mode enabled:
```bash
uv run datasette data.db --create --root \
  -s plugins.datasette-auth-tokens.manage_tokens true \
  -s permissions.auth-tokens-create.id '*' \
  --internal internal.db --reload
```
Click the link to sign in as root and then visit http://127.0.0.1:8001/-/api/tokens/create
