# datasette-leaflet-geojson

[![PyPI](https://img.shields.io/pypi/v/datasette-leaflet-geojson.svg)](https://pypi.org/project/datasette-leaflet-geojson/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-leaflet-geojson?include_prereleases&label=changelog)](https://github.com/simonw/datasette-leaflet-geojson/releases)
[![Tests](https://github.com/simonw/datasette-leaflet-geojson/workflows/Test/badge.svg)](https://github.com/simonw/datasette-leaflet-geojson/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-leaflet-geojson/blob/main/LICENSE)

Datasette plugin that replaces any GeoJSON column values with a Leaflet map

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-leaflet-geojson

## Usage

Any columns containing valid GeoJSON strings will have their contents replaced with a Leaflet map when they are displayed in the Datasette interface.

## Demo

You can try this plugin out at https://calands.datasettes.com/calands/superunits_with_maps

![datasette-leaflet-geojson in action](https://raw.github.com/simonw/datasette-leaflet-geojson/main/datasette-leaflet-geojson.png)

## Configuration

By default this plugin displays maps for the first ten rows, and shows a "Click to load map" prompt for rows past the first ten.

You can change this limit using the `default_maps_to_load` plugin configuration setting. Add this to your `metadata.json`:

```json
{
    "plugins": {
        "datasette-leaflet-geojson": {
            "default_maps_to_load": 20
        }
    }
}
```
Then run Datasette with `datasette mydb.db -m metadata.json`.
