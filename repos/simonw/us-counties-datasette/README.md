# us-counties-datasette

https://us-counties.datasette.io/

A Datasette instance exposing US counties, FIPS codes and polygons.

Source data: the `cb_2018_us_county_500k.zip` shapefile released by the US census.

Download that from https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

Run `./build.sh` to build the database.

To run locally:

    datasette counties.db -m metadata.yml --load-extension=spatialite

I run `./deploy.sh` to deploy it to Cloud Run.

## API

This query will return the county for a latitude and longitude:

https://us-counties.datasette.io/counties/county_for_latitude_longitude

Here's that as a JSON API:

https://us-counties.datasette.io/counties/county_for_latitude_longitude.json?longitude=-122.676968&latitude=45.266289&_shape=array
