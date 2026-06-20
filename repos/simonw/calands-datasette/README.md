# calands-datasette

This repository publishes a Datasette at https://calands.datasettes.com/ using the [California Protected Areas Database (CPAD 2020a) data](https://www.calands.org/cpad/) maintained by [GreenInfo Network](https://www.greeninfo.org/).

The site is built and published by [this GitHub Actions workflow](https://github.com/simonw/calands-datasette/blob/main/.github/workflows/build-and-deploy.yml).

See also [Drawing shapes on a map to query a SpatiaLite database](https://simonwillison.net/2021/Jan/24/drawing-shapes-spatialite/).

## Technology used

- [Datasette](https://datasette.io/)
- [datasette-leaflet-geojson](https://github.com/simonw/datasette-leaflet-geojson)
- [SpatiaLite](https://www.gaia-gis.it/fossil/libspatialite/index)
- [sqlite-utils](https://github.com/simonw/sqlite-utils)
- [shapefile-to-sqlite](https://github.com/simonw/shapefile-to-sqlite)
- [Google Cloud Run](https://cloud.google.com/run)
