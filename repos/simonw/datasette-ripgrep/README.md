# datasette-ripgrep

[![PyPI](https://img.shields.io/pypi/v/datasette-ripgrep.svg)](https://pypi.org/project/datasette-ripgrep/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-ripgrep?include_prereleases&label=changelog)](https://github.com/simonw/datasette-ripgrep/releases)
[![Tests](https://github.com/simonw/datasette-ripgrep/workflows/Test/badge.svg)](https://github.com/simonw/datasette-ripgrep/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-ripgrep/blob/main/LICENSE)

Web interface for searching your code using [ripgrep](https://github.com/BurntSushi/ripgrep), built as a [Datasette](https://datasette.io/) plugin

For background on this project see [datasette-ripgrep: deploy a regular expression search engine for your source code](https://simonwillison.net/2020/Nov/28/datasette-ripgrep/).

## Demo

Try this plugin out at https://ripgrep.datasette.io/-/ripgrep - where you can run regular expression searches across the source code of Datasette and all of the `datasette-*` plugins belonging to the [simonw GitHub user](https://github.com/simonw).

Some example searches:

- [with.\*AsyncClient](https://ripgrep.datasette.io/-/ripgrep?pattern=with.*AsyncClient) - regular expression search for `with.*AsyncClient`
- [.plugin_config, literal=on](https://ripgrep.datasette.io/-/ripgrep?pattern=.plugin_config\(&literal=on) - a non-regular expression search for `.plugin_config(`
- [with.\*AsyncClient glob=datasette/\*\*](https://ripgrep.datasette.io/-/ripgrep?pattern=with.*AsyncClient&glob=datasette%2F%2A%2A) - search for that pattern only within the `datasette/` top folder
- ["sqlite-utils\[">\] glob=setup.py](https://ripgrep.datasette.io/-/ripgrep?pattern=%22sqlite-utils%5B%22%3E%5D&glob=setup.py) - a regular expression search for packages that depend on either `sqlite-utils` or `sqlite-utils>=some-version`
- [test glob=!\*.html](https://ripgrep.datasette.io/-/ripgrep?pattern=test&glob=%21*.html) - search for the string `test` but exclude results in HTML files

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-ripgrep

The `rg` executable needs to be [installed](https://github.com/BurntSushi/ripgrep/blob/master/README.md#installation) such that it can be run by this tool.

## Usage

This plugin requires configuration: it needs to a `path` setting so that it knows where to run searches.

Create a `datasette.yaml` file that looks like this:

```yaml
plugins:
  datasette-ripgrep:
    path: /path/to/your/files
```

Now run Datasette using `datasette --config datasette.yaml`. The plugin will add an interface at `/-/ripgrep` for running searches.

## Plugin configuration

The `"path"` configuration is required. Optional extra configuration options are:

- `time_limit` - floating point number. The `rg` process will be terminated if it takes longer than this limit. The default is one second, `1.0`.
- `max_lines` - integer. The `rg` process will be terminated if it returns more than this number of lines. The default is `2000`.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-ripgrep
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
