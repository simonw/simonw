# llm-plugin cookiecutter template

A cookiecutter template for creating new [llm plugins](https://llm.datasette.io/en/stable/plugins/index.html).
`
## Installation

You'll need to have [cookiecutter](https://cookiecutter.readthedocs.io/) installed. I recommend pipx for this:
```bash
pipx install cookiecutter
```
Regular `pip` will work OK too, or `uv tool install`, or run `uvx cookiecutter ...` directly.

## Usage

Run `cookiecutter gh:simonw/llm-plugin` and then answer the prompts. Here's an example run:

```bash
cookiecutter gh:simonw/llm-plugin
```
```
plugin_name []: plugin template demo
description []: Demonstrating https://github.com/simonw/llm-plugin
hyphenated [plugin-template-demo]:
underscored [plugin_template_demo]:
github_username []: simonw
author_name []: Simon Willison
```
I strongly recommend accepting the suggested value for "hyphenated" and "underscored" by hitting enter on those prompts.

This will create a directory called `llm-plugin-template-demo` - the plugin name you enter is converted to lowercase and uses hyphens instead of spaces.

## Developing your plugin

Having created the new plugin structure from the template, here's how to start working on the plugin.

You can install the plugin in "editable" mode like so:

```bash
llm install -e .
```
Run this in the `llm-plugin-template-demo` directory.

You can also pass the path to that directory like this:

```bash
llm install -e path/to/llm-plugin-template-demo
```

To confirm it is installed, run:

```bash
llm plugins
```

You should see the following:
```json
[
  {
    "name": "llm-plugin-template-demo",
    "hooks": [
      "prepare_connection",
      "register_commands"
    ],
    "version": "0.1"
  }
]
```
You can run the tests for your plugin with `python -m pytest` - follow the development environment instructions in the plugin's generated README for details.
