# datasette-auth-passwords

[![PyPI](https://img.shields.io/pypi/v/datasette-auth-passwords.svg)](https://pypi.org/project/datasette-auth-passwords/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-auth-passwords?label=changelog)](https://github.com/simonw/datasette-auth-passwords/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-auth-passwords/blob/master/LICENSE)

Datasette plugin for authenticating access using passwords

## Installation

Install this plugin in the same environment as Datasette.

```bash
datasette install datasette-auth-passwords
```

## Demo

A demo of this plugin is running at https://datasette-auth-passwords-demo.datasette.io/

The demo is configured to show the `public.db` database to everyone, but the `private.db` database only to logged in users.

You can log in at https://datasette-auth-passwords-demo.datasette.io/-/login with username `root` and password `password!`.

## Usage

This plugin works based on a list of username/password accounts that are hard-coded into the plugin configuration.

First, you'll need to create a password hash. There are three ways to do that:

- Install the plugin, then use the interactive tool located at `/-/password-tool`
- Use the hosted version of that tool at https://datasette-auth-passwords-demo.datasette.io/-/password-tool
- Use the `datasette hash-password` command, described below

Now add the following to your `metadata.json`:

```json
{
    "plugins": {
        "datasette-auth-passwords": {
            "someusername_password_hash": {
                "$env": "PASSWORD_HASH_1"
            }
        }
    }
}
```

The password hash can now be specified in an environment variable when you run Datasette. You can do that like so:

    PASSWORD_HASH_1='pbkdf2_sha256$...' \
        datasette -m metadata.json

Be sure to use single quotes here otherwise the `$` symbols in the password hash may be incorrectly interpreted by your shell.

You will now be able to log in to your instance using the form at `/-/login` with `someusername` as the username and the password that you used to create your hash as the password.

You can include as many accounts as you like in the configuration, each with different usernames.

### datasette hash-password

The plugin exposes a new CLI command, `datasette hash-password`. You can run this without arguments to interactively create a new password hash:
```bash
datasette hash-password
```
```
Password: 
Repeat for confirmation: 
pbkdf2_sha256$260000$1513...
```
Or if you want to use it as part of a script, you can add the `--no-confirm` option to generate a hash directly from a value passed to standard input:
```bash
echo 'my password' | datasette hash-password --no-confirm
```
```
pbkdf2_sha256$260000$daa...
```
### Specifying actors

By default, a logged in user will result in an [actor block](https://datasette.readthedocs.io/en/stable/authentication.html#actors) that just contains their username:

```json
{
    "id": "someusername"
}
```

You can customize the actor that will be used for a username by including an `"actors"` configuration block, like this:

```json
{
    "plugins": {
        "datasette-auth-passwords": {
            "someusername_password_hash": {
                "$env": "PASSWORD_HASH_1"
            },
            "actors": {
                "someusername": {
                    "id": "someusername",
                    "name": "Some user"
                }
            }
        }
    }
}
```
### HTTP Basic authentication option

This plugin defaults to implementing login using an HTML form that sets a signed authentication cookie.

You can alternatively configure it to use [HTTP Basic authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#basic_authentication_scheme) instead.

Do this by adding `"http_basic_auth": true` to the `datasette-auth-passwords` block in your plugin configuration.

This option introduces the following behaviour:

- Account usernames and passwords are configured in the same way as form-based authentication
- Every page within Datasette - even pages that normally do not use authentication, such as static assets - will display a browser login prompt
- Users will be unable to log out without closing their browser entirely

There is a demo of this mode at https://datasette-auth-passwords-http-basic-demo.datasette.io/ - sign in with username `root` and password `password!`

### Using with datasette publish

If you are publishing data using a [datasette publish](https://datasette.readthedocs.io/en/stable/publish.html#datasette-publish) command you can use the `--plugin-secret` option to securely configure your password hashes (see [secret configuration values](https://datasette.readthedocs.io/en/stable/plugins.html#secret-configuration-values)).

You would run the command something like this:

    datasette publish cloudrun mydatabase.db \
        --install datasette-auth-passwords \
        --plugin-secret datasette-auth-passwords root_password_hash 'pbkdf2_sha256$...' \
        --service datasette-auth-passwords-demo

This will allow you to log in as username `root` using the password that you used to create the hash.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-auth-passwords
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
