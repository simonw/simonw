# datasette-chatgpt-plugin

[![PyPI](https://img.shields.io/pypi/v/datasette-chatgpt-plugin.svg)](https://pypi.org/project/datasette-chatgpt-plugin/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-chatgpt-plugin?include_prereleases&label=changelog)](https://github.com/simonw/datasette-chatgpt-plugin/releases)
[![Tests](https://github.com/simonw/datasette-chatgpt-plugin/workflows/Test/badge.svg)](https://github.com/simonw/datasette-chatgpt-plugin/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-chatgpt-plugin/blob/main/LICENSE)

A Datasette plugin that turns a Datasette instance into a ChatGPT plugin - so you can use ChatGPT to ask questions of your data.

For more on this project, see [Building a ChatGPT plugin to ask questions of data hosted in Datasette](https://simonwillison.net/2023/Mar/24/datasette-chatgpt-plugin/).

⚠️ **Warning**: ChatGPT can still hallucinate results using this plugin! See [this issue](https://github.com/simonw/datasette-chatgpt-plugin/issues/2) for more details of this problem.

## Installation

Install this plugin in the same environment as Datasette, on a deployed instance.

    datasette install datasette-chatgpt-plugin

Or if you are using `datasette publish` to deploy Datasette:

    datasette publish cloudrun/vercel/fly/heroku data.db \
      --install datasette-chatgpt-plugin

## Usage

Once installed, your Datasette instance will work with the new [ChatGPT plugins](https://openai.com/blog/chatgpt-plugins) system - provided you have access to that preview.

Click `Plugins -> Plugin store -> Install an unverified plugin` and enter the URL of your Datasette instance.

If this doesn't work, try `Develop my own plugin -> My manifest is ready` instead and then paste in your URL.

ChatGPT will discover the plugin by hitting the `/.well-known/ai-plugin.json` endpoint.

You can then ask it questions! Some starting examples:

- Show a list of tables (this is always good to start with as it ensures ChatGPT knows which tables are available)
- Show the first 10 rows of the `mytable` table

This plugin currently exposes a single database - the first database attached to your instance.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-chatgpt-plugin
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
