# datasette-secret-santa

[![PyPI](https://img.shields.io/pypi/v/datasette-secret-santa.svg)](https://pypi.org/project/datasette-secret-santa/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-secret-santa?include_prereleases&label=changelog)](https://github.com/simonw/datasette-secret-santa/releases)
[![Tests](https://github.com/simonw/datasette-secret-santa/workflows/Test/badge.svg)](https://github.com/simonw/datasette-secret-santa/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-secret-santa/blob/main/LICENSE)

Run a secret santa using Datasette

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-secret-santa

## Running this on Glitch

https://glitch.com/ is a great way to host this application.

You can [remix this project on Glitch](https://glitch.com/~datasette-secret-santa) to get your own copy.

Or you can create a new application and paste the following into your `glitch.json` file:

```json
{
  "install": "pip3 install --user datasette datasette-secret-santa -U",
  "start": "datasette --create .data/santa.db -p 3000"
}
```
Then visit your new app's homepage and click the link to create a new secret santa group.

## Usage

![Animated GIF showing the plugin in action - the user adds three names, then gets the password for their account - then hits the assign button and uses their password to find out who they have been assigned.](https://raw.githubusercontent.com/simonw/datasette-secret-santa/main/secret-santa.gif)

This plugin requires a database called `santa.db`. You can run it and create such a database like this:

    datasette santa.db --create

It expects to be the only plugin installed, and will take over the `/` homepage.

To create a new Secret Santa, visit `/santa/create_secret_santa` (linked from the homepage).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-secret-santa
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
