# datasette-yaml

[![PyPI](https://img.shields.io/pypi/v/datasette-yaml.svg)](https://pypi.org/project/datasette-yaml/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-yaml?include_prereleases&label=changelog)](https://github.com/simonw/datasette-yaml/releases)
[![Tests](https://github.com/simonw/datasette-yaml/workflows/Test/badge.svg)](https://github.com/simonw/datasette-yaml/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-yaml/blob/main/LICENSE)

Export Datasette records as YAML

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-yaml

## Usage

Having installed this plugin, every table and query will gain a new `.yaml` export link.

You can also construct these URLs directly: `/dbname/tablename.yaml`

## Demo

The plugin is running on [covid-19.datasettes.com](https://covid-19.datasettes.co/) - for example [/covid/latest_ny_times_counties_with_populations.yaml](https://covid-19.datasettes.com/covid/latest_ny_times_counties_with_populations.yaml)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-yaml
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
