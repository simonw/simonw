# cbsa-datasette

https://cbsa.datasettes.com/ - provides [an API](https://cbsa.datasettes.com/core/by_lat_lon) for looking up [core-based statistical areas](https://en.wikipedia.org/wiki/Core-based_statistical_area) based on a latitude/longitude point.

More details: [cbsa-datasette in my Weeknotes](https://simonwillison.net/2021/Jan/10/weeknotes/#cbsa-datasette)

## Running this locally

Download the shapefile from [Bureau of Transportation Stastics: Core Based Statistical Areas](https://geodata.bts.gov/datasets/usdot::core-based-statistical-areas/explore).

I have a copy of the file available here:

`wget https://static.simonwillison.net/static/2023/Core_Based_Statistical_Areas.zip`

Install [shapefile-to-sqlite](https://datasette.io/tools/shapefile-to-sqlite) and [SpatiaLite](https://docs.datasette.io/en/stable/spatialite.html#installation) and run this command:

    shapefile-to-sqlite core.db Core_Based_Statistical_Areas.zip \
        --table Core_Based_Statistical_Areas \
        --spatial-index

This will produce `core.db` containing a `Core_Based_Statistical_Areas` SpatiaLite table plus spatial indexes.

Run this command to browse it with Datasette:

    datasette -m metadata.yml core.db
