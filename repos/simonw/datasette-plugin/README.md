# datasette-plugin cookiecutter template

A cookiecutter template for creating new Datasette plugins. See [Writing Plugins](https://docs.datasette.io/en/stable/writing_plugins.html) in the Datasette documentation for more details.

Use this template on your own machine with cookiecutter, or create a brand new repository based on this template entirely through the GitHub web interface using [datasette-plugin-template-repository](https://github.com/simonw/datasette-plugin-template-repository).

## Installation

You'll need to have [cookiecutter](https://cookiecutter.readthedocs.io/) installed. I recommend pipx for this:
```bash
pipx install cookiecutter
```
Regular `pip` will work OK too.

## Usage

Run `cookiecutter gh:simonw/datasette-plugin` and then answer the prompts. Here's an example run:
```
$ cookiecutter gh:simonw/datasette-plugin
plugin_name []: plugin template demo
description []: Demonstrating https://github.com/simonw/datasette-plugin
hyphenated [plugin-template-demo]:
underscored [plugin_template_demo]:
github_username []: simonw
author_name []: Simon Willison
include_static_directory []: y
include_templates_directory []: y
```
I strongly recommend accepting the suggested value for "hyphenated" and "underscored" by hitting enter on those prompts.

The `include_static_directory` and `include_templates_directory` prompts will cause `../static` and `../templates` folders to be created and added to `setup.py` as `package_data`. Use these if your plugin needs to include templates or static assets (CSS and JavaScript). Leave these prompts blank if you do not want these directories to be created.

This will create a directory called `datasette-plugin-template-demo` - the plugin name you enter is converted to lowercase and uses hyphens instead of spaces.

See https://github.com/simonw/datasette-plugin-template-demo for the output of this example.

## Developing your plugin

Having created the new plugin structure from the template, here's how to start working on the plugin.

If your plugin is called `datasette-my-new-plugin`, you can start working on it like so:
```bash
cd datasette-my-new-plugin
# Run datasette and confirm the plugin is there
uv run datasette plugins
```
You should see the following:
```json
[
    {
        "name": "datasette-my-new-plugin",
        "static": false,
        "templates": false,
        "version": "0.1",
        "hooks": []
    }
]
```
You can run the default test for your plugin like so:
```bash
uv run pytest
```
This will execute the test in `tests/test_my_new_plugin.py`, which confirms that the plugin has been installed.

Now you can open the `datasette_my_new_plugin/__init__.py` file and start adding your [plugin hooks](https://docs.datasette.io/en/stable/plugin_hooks.html).

## Creating a Git repository for your plugin

You can initialize a Git repository for your plugin like this:
```bash
cd datasette-my-new-plugin
git init
git add .
git commit -m "Initial structure from template"
# Rename the 'master' branch to 'main':
git branch -m master main
```
## Publishing your plugin to GitHub

Use https://github.com/new to create a new GitHub repository sharing the same name as your plugin, which should be something like `datasette-my-new-plugin`.

Push your `main` branch to GitHub like this:
```bash
git remote add origin git@github.com:YOURNAME/datasette-my-new-plugin.git
git push -u origin main
```
The template will have created a GitHub Action which runs your plugin's test suite against every commit.

## Publishing your plugin as a package to PyPI

The template also includes an Action for publishing packages to [PyPI](https://pypi.org/).

For this to work, you need to create an environment in your GitHub repository called `release`. You then need to configure PyPI with a new "pending publisher" with the following settings:

- PyPI Project Name: `datasette-name-of-your-plugin`
- Owner: Your GitHub username or organization
- Repository name: The name of your repository
- Workflow name: `publish.yml`
- Environment name: `release`

See [Publish releases to PyPI from GitHub Actions without a password or token](https://til.simonwillison.net/pypi/pypi-releases-from-github) for details.

With that configured, create a GitHub release with a name that corresponds to the version number listed in your `pyproject.toml` file and the action will build and publish a PyPI package for you.
