# geojson-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/geojson-to-sqlite.svg)](https://pypi.org/project/geojson-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/geojson-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/geojson-to-sqlite/releases)
[![Tests](https://github.com/simonw/geojson-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/geojson-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/geojson-to-sqlite/blob/main/LICENSE)

CLI tool for converting GeoJSON to SQLite (optionally with SpatiaLite)

[RFC 7946: The GeoJSON Format](https://tools.ietf.org/html/rfc7946)

## How to install

    $ pip install geojson-to-sqlite

## How to use

You can run this tool against a GeoJSON file like so:

    $ geojson-to-sqlite my.db features features.geojson

This will load all of the features from the `features.geojson` file into a table called `features`.

Each row will have a `geometry` column containing the feature geometry, and columns for each of the keys found in any `properties` attached to those features. (To bundle all properties into a single JSON object, use the `--properties` flag.)

The table will be created the first time you run the command.

On subsequent runs you can use the `--alter` option to add any new columns that are missing from the table.

You can pass more than one GeoJSON file, in which case the contents of all of the files will be inserted into the same table.

If your features have an `"id"` property it will be used as the primary key for the table. You can also use `--pk=PROPERTY` with the name of a different property to use that as the primary key instead. If you don't want to use the `"id"` as the primary key (maybe it contains duplicate values) you can use `--pk ''` to specify no primary key.

Specifying a primary key also will allow you to upsert data into the rows instead of insert data into new rows.

If no primary key is specified, a SQLite `rowid` column will be used.

You can use `-` as the filename to import from standard input. For example:

    $ curl https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_20m.json \
        | geojson-to-sqlite my.db states - --pk GEO_ID

## Using with SpatiaLite

By default, the `geometry` column will contain JSON.

If you have installed the [SpatiaLite](https://www.gaia-gis.it/fossil/libspatialite/index) module for SQLite you can instead import the geometry into a geospatially indexed column.

You can do this using the `--spatialite` option, like so:

    $ geojson-to-sqlite my.db features features.geojson --spatialite

The tool will search for the SpatiaLite module in the following locations:

- `/usr/lib/x86_64-linux-gnu/mod_spatialite.so`
- `/usr/local/lib/mod_spatialite.dylib`

If you have installed the module in another location, you can use the `--spatialite_mod=xxx` option to specify where:

    $ geojson-to-sqlite my.db features features.geojson \
        --spatialite_mod=/usr/lib/mod_spatialite.dylib

You can create a SpatiaLite spatial index on the `geometry` column using the `--spatial-index` option:

    $ geojson-to-sqlite my.db features features.geojson --spatial-index

Using this option implies `--spatialite` so you do not need to add that.

## Streaming large datasets

For large datasets, consider using newline-delimited JSON to stream features into the database without loading the entire feature collection into memory.

For example, to load a day of earthquake reports from USGS:

    $ geojson-to-sqlite quakes.db quakes tests/quakes.ndjson \
      --nl --pk=id --spatialite

When using newline-delimited JSON, tables will also be created from the first feature, instead of guessing types based on the first 100 features.

If you want to use a larger subset of your data to guess column types (for example, if some fields are inconsistent) you can use [fiona](https://fiona.readthedocs.io/en/latest/cli.html) to collect features into a single collection.

    $ head tests/quakes.ndjson | fio collect | \
      geojson-to-sqlite quakes.db quakes - --spatialite

This will take the first 10 lines from `tests/quakes.ndjson`, pass them to `fio collect`, which turns them into a single feature collection, and pass that, in turn, to `geojson-to-sqlite`.

## Using this with Datasette

Databases created using this tool can be explored and published using [Datasette](https://datasette.readthedocs.io/).

The Datasette documentation includes a section on [how to use it to browse SpatiaLite databases](https://datasette.readthedocs.io/en/stable/spatialite.html).

The [datasette-leaflet-geojson](https://datasette.io/plugins/datasette-leaflet-geojson) plugin can be used to visualize columns containing GeoJSON geometries on a [Leaflet](https://leafletjs.com/) map.

If you are using SpatiaLite you will need to output the geometry as GeoJSON in order for that plugin to work. You can do that using the SpaitaLite `AsGeoJSON()` function - something like this:

```sql
select rowid, AsGeoJSON(geometry) from mytable limit 10
```

The [datasette-geojson-map](https://datasette.io/plugins/datasette-geojson-map) is an alternative plugin which will automatically render SpatiaLite geometries as a Leaflet map on the corresponding table page, without needing you to call `AsGeoJSON(geometry)`.
