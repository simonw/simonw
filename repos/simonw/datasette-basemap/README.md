# datasette-basemap

[![PyPI](https://img.shields.io/pypi/v/datasette-basemap.svg)](https://pypi.org/project/datasette-basemap/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-basemap?include_prereleases&label=changelog)](https://github.com/simonw/datasette-basemap/releases)
[![Test](https://github.com/simonw/datasette-basemap/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/datasette-basemap/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-basemap/blob/main/LICENSE)

A basemap for Datasette and datasette-leaflet

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-basemap

## Usage

This plugin will make a `basemap` database available containing OpenStreetMap tiles for zoom levels 0-6 in the [mbtiles](https://github.com/mapbox/mbtiles-spec) format. It is designed for use with the [datasette-tiles](https://datasette.io/plugins/datasette-tiles) tile server plugin.

## Demo

You can preview this map at https://datasette-tiles-demo.datasette.io/-/tiles/basemap and browse the database directly at https://datasette-tiles-demo.datasette.io/basemap

## License

The data bundled with this package is © OpenStreetMap contributors, licensed under the [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/). See [this page](https://www.openstreetmap.org/copyright) for more details.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-basemap
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
