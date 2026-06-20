# datasette-secrets

[![PyPI](https://img.shields.io/pypi/v/datasette-secrets.svg)](https://pypi.org/project/datasette-secrets/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-secrets?include_prereleases&label=changelog)](https://github.com/datasette/datasette-secrets/releases)
[![Tests](https://github.com/datasette/datasette-secrets/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-secrets/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-secrets/blob/main/LICENSE)

Manage secrets such as API keys for use with other Datasette plugins

This plugin requires a **Datasette 1.0 alpha** release.

Datasette plugins sometimes need access to secrets, such as API keys used to integrate with tools hosted outside of Datasette - things like geocoders or hosted AI language models.

This plugin provides ways to configure those secrets:

- Secrets can be configured using environment variables, such as `DATASETTE_SECRETS_OPENAI_API_KEY`
- Secrets can be stored, encrypted, in a SQLite database table which administrator users can then update through the Datasette web interface

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-secrets
```
## Configuration

First you will need to generate an encryption key for this plugin to use. Run this command:

```bash
datasette secrets generate-encryption-key
```
Store this secret somewhere secure. It will be used to both encrypt and decrypt secrets stored by this plugin - if you lose it you will not be able to recover your secrets.

Configure the plugin with these these two plugin settings:

```yaml
plugins:
  datasette-secrets:
    encryption-key:
      $env: DATASETTE_SECRETS_ENCRYPTION_KEY
    database: name_of_database
```
The `encryption_key` setting should be set to the encryption key you generated earlier. You can store it in an environment variable if you prefer.

`database` is the name of the database that the encrypted keys should be stored in. Omit this setting to use the internal database.

### Using the internal database

While the secrets stored in the `datasette_secrets` table are encrypted, we still recommend hiding that table from view.

One way to do that is to keep the table in Datasette's internal database, which is invisible to all users, even users who are logged in.

By default, the internal database is an in-memory database that is reset when Datasette restarts. This is no good for persistent secret storage!

Instead, you should switch Datasette to using an on-disk internal database. You can do this by starting Datasette with the `--internal` option:
```bash
datasette data.db --internal internal.db
```
Your secrets will be stored in the `datasette_secrets` table in that database file.

### Permissions

Only users with the `manage-secrets` permission will have access to manage secrets through the Datasette web interface.

You can grant that permission to the `root` user (or the user with an ID of your choice) by including this in your `datasette.yml` file:

```yaml
permissions:
  manage-secrets:
    id: root
```
Then start Datasette like this (with `--root` to get a URL to login as the root user):
```bash
datasette data.db --internal internal.db -c datasette.yml --root
```
Alternatively, use the `-s` option to set that setting without creating a configuration file:
```bash
datasette data.db --internal internal.db \
  -s permissions.manage-secrets.id root \
  --root
```

## Usage

users with the `manage-secrets` permission will see a new "Manage secrets" link in the Datasette navigation menu. This interface can also be accessed at `/-/secrets`.

The page with the list of secrets will show the user who last updated each secret. This will use the [actors_from_ids()](https://docs.datasette.io/en/latest/plugin_hooks.html#actors-from-ids-datasette-actor-ids) mechanism, displaying the actor's `username` if available, otherwise the `name`, otherwise the `id`.

## For plugin authors

Plugins can depend on this plugin if they want to implement secrets.

`datasette-secrets` to the `dependencies` list in `pyproject.toml`.

Then declare the name and description of any secrets you need using the `register_secrets()` plugin hook:

```python
from datasette import hookimpl
from datasette_secrets import Secret

@hookimpl
def register_secrets():
    return [
        Secret(
            name="OPENAI_API_KEY",
            description="An OpenAI API key"
        ),
    ]
```
You can also provide optional `obtain_url` and `obtain_label` fields to link to a page where a user can obtain an API key:
```python
@hookimpl
def register_secrets():
    return [
        Secret(
            name="OPENAI_API_KEY",
            obtain_url="https://platform.openai.com/api-keys",
            obtain_label="Get an OpenAI API key"
        ),
    ]
```

The hook can take an optional `datasette` argument. It can return a list or an `async def` function that, when awaited, returns a list.

The list should consist of `Secret()` instances, each with a name and an optional description. The description can contain HTML.

To obtain the current value of the secret, use the `await get_secret()` method:

```python
from datasette_secrets import get_secret

# Third argument is the actor_id, optional
secret = await get_secret(datasette, "OPENAI_API_KEY", "root")
```
If the Datasette administrator set a `DATASETTE_SECRETS_OPENAI_API_KEY` environment variable, that will be returned.

Otherwise the encrypted value in the database table will be decrypted and returned - or `None` if there is no configured secret.

The `last_used_at` column is updated every time a secret is accessed. The `last_used_by` column will be set to the actor ID passed to `get_secret()`, or `null` if no actor ID was passed.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-secrets
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
