# datasette-edit-templates

[![PyPI](https://img.shields.io/pypi/v/datasette-edit-templates.svg)](https://pypi.org/project/datasette-edit-templates/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-edit-templates?include_prereleases&label=changelog)](https://github.com/simonw/datasette-edit-templates/releases)
[![Tests](https://github.com/simonw/datasette-edit-templates/workflows/Test/badge.svg)](https://github.com/simonw/datasette-edit-templates/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-edit-templates/blob/main/LICENSE)

Plugin allowing Datasette templates to be edited within Datasette.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-edit-templates
```
## Usage

On startup. a `_templates_` table will be created in the database you are running Datasette against.

Use the app menu to navigate to the `/-/edit-templates` page, and edit templates there.

Changes should become visible instantly, and will be persisted to your database.

The interface is only available to users with the `edit-templates` permission.

The `root` user is granted this permission by default. You can sign in as the root user using `datasette mydb.db --root`.

## Configuration

To put the `_templates_` table in a specific database, set the `datasette-edit-templates: database` plugin configuration option:

```json
{
    "plugins": {
        "datasette-edit-templates": {
            "database": "some_database"
        }
    }
}
```
On Datasette [1.0a5](https://docs.datasette.io/en/latest/changelog.html#a5-2023-08-29) or higher you can use the [internal database](https://docs.datasette.io/en/latest/internals.html#internals-internal) with `"internal_db: true":`

```json
{
    "plugins": {
        "datasette-edit-templates": {
            "internal_db": true
        }
    }
}
```

By default the [prepare_jinja2_environment()](https://docs.datasette.io/en/stable/plugin_hooks.html#prepare-jinja2-environment-env-datasette) hook will be used to load the custom templates.

You can disable this behavior using the `skip_prepare_jinja2_environment` plugin configuration option:

```json
{
    "plugins": {
        "datasette-edit-templates": {
            "skip_prepare_jinja2_environment": true
        }
    }
}
```
Set this option if you want to further customize how the templates are loaded using another plugin.

The menu item used to access this plugin is labeled "Edit templates" by default. You can customize this using the `menu_label` plugin configuration option:

```json
{
    "plugins": {
        "datasette-edit-templates": {
            "menu_label": "Custom templates"
        }
    }
}
```
Set that to `null` to hide the menu option entirely.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-edit-templates
python3 -mvenv venv
source venv/bin/activate
```
Or if you are using `pipenv`:
```bash
pipenv shell
```
Now install the dependencies and tests:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
