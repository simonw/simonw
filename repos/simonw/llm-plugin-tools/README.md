# llm-plugin-tools cookiecutter template

A cookiecutter template for creating a new [LLM plugin](https://llm.datasette.io/en/stable/plugins/index.html) that adds [tools](https://llm.datasette.io/en/latest/tools.html) to LLM.

## Installation

You'll need to have [cookiecutter](https://cookiecutter.readthedocs.io/) installed. I recommend pipx for this:

    pipx install cookiecutter

Regular `pip` will work OK too. Or you can use `uv tool install cookiecutter` or even `uvx cookiecutter ...`.

## Usage

Run `cookiecutter gh:simonw/llm-plugin-tools` and then answer the prompts. Here's an example run:

```bash
cookiecutter gh:simonw/llm-plugin-tools
```
Provide some information about your plugin:
```
  [1/7] plugin_name (): multiply
  [2/7] description (): A tool that can multiply numbers
  [3/7] function_name (example_hello): multiply
  [4/7] hyphenated (llm-tools-multiply):
  [5/7] underscored (llm_tools_multiply):
  [6/7] github_username (): simonw
  [7/7] author_name (): Simon Willison
```
I strongly recommend accepting the suggested value for "hyphenated" and "underscored" by hitting enter on those prompts.

This will create a directory called `llm-tools-multiply` - the plugin name you enter is converted to lowercase and uses hyphens instead of spaces, and the standard prefix `llm-tools-` is added.

Modify the code in `llm_tools_multiply.py` to implement your plugin, then update the tests in `tests/test_llm_tools_multiply.py` to confirm that it works.

## Developing your plugin

Having created the new plugin structure from the template, here's how to start working on the plugin.

You can install the plugin in "editable" mode like so:

```bash
llm install -e .
```
Run this in the `llm-tools-multiply` directory.

You can also pass the path to that directory like this:

```bash
llm install -e path/to/llm-tools-multiply
```

To confirm it is installed, run:

```bash
llm plugins
```

You should see the following:
```json
[
  {
    "name": "llm-tools-multiply",
    "hooks": [
      "register_tools"
    ],
    "version": "0.1"
  }
]
```
You can run the tests for your plugin with `python -m pytest` - follow the development environment instructions in the plugin's generated README for details.
