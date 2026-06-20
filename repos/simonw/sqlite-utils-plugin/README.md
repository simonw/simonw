# sqlite-utils-plugin cookiecutter template

A cookiecutter template for creating new [sqlite-utils plugins](https://sqlite-utils.datasette.io/en/stable/plugins.html).
`
## Installation

You'll need to have [cookiecutter](https://cookiecutter.readthedocs.io/) installed. I recommend pipx for this:

    pipx install cookiecutter

Regular `pip` will work OK too.

## Usage

Run `cookiecutter gh:simonw/sqlite-utils-plugin` and then answer the prompts. Here's an example run:

```bash
cookiecutter gh:simonw/sqlite-utils-plugin
```
```
plugin_name []: plugin template demo
description []: Demonstrating https://github.com/simonw/sqlite-utils-plugin
hyphenated [plugin-template-demo]: 
underscored [plugin_template_demo]: 
github_username []: simonw
author_name []: Simon Willison
```
I strongly recommend accepting the suggested value for "hyphenated" and "underscored" by hitting enter on those prompts.

This will create a directory called `sqlite-utils-plugin-template-demo` - the plugin name you enter is converted to lowercase and uses hyphens instead of spaces.

## Developing your plugin

Having created the new plugin structure from the template, here's how to start working on the plugin.

You can install the plugin in "editable" mode like so:

```bash
sqlite-utils install -e .
```
Run this in the `sqlite-utils-plugin-template-demo` directory.

You can also pass the path to that directory like this:

```bash
sqlite-utils install -e path/to/sqlite-utils-plugin-template-demo
```

To confirm it is installed, run:

```bash
sqlite-utils plugins
```

You should see the following:
```json
[
  {
    "name": "sqlite-utils-plugin-template-demo",
    "hooks": [
      "prepare_connection",
      "register_commands"
    ],
    "version": "0.1"
  }
]
```
You can run the tests for your plugin with `python -m pytest` - follow the development environment instructions in the plugin's generated README for details.

## Publishing your plugin to GitHub

Use https://github.com/new to create a new GitHub repository sharing the same name as your plugin, which should be something like `sqlite-utils-my-new-plugin`.

Push your `main` branch to GitHub like this:
```bash
git remote add origin git@github.com:YOURNAME/sqlite-utils-my-new-plugin.git
git push -u origin main
```
The template will have created a GitHub Action which runs your plugin's test suite against every commit.

## Publishing your plugin as a package to PyPI

The template also includes an Action for publishing packages to [PyPI](https://pypi.org/).

For this to work, you need to create an environment in your GitHub repository called `release`. You then need to configure PyPI with a new "pending publisher" with the following settings:

- PyPI Project Name: `sqlite-utils-name-of-your-plugin`
- Owner: Your GitHub username or organization
- Repository name: The name of your repository
- Workflow name: `publish.yml`
- Environment name: `release`

See [Publish releases to PyPI from GitHub Actions without a password or token](https://til.simonwillison.net/pypi/pypi-releases-from-github) for details.

With that configured, create a GitHub release with a name that corresponds to the version number listed in your `pyproject.toml` file and the action will build and publish a PyPI package for you.
