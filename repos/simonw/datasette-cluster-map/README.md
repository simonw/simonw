# datasette-cluster-map

[![PyPI](https://img.shields.io/pypi/v/datasette-cluster-map.svg)](https://pypi.org/project/datasette-cluster-map/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-cluster-map?include_prereleases&label=changelog)](https://github.com/simonw/datasette-cluster-map/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-cluster-map/blob/main/LICENSE)

A [Datasette plugin](https://docs.datasette.io/en/stable/plugins.html) that detects tables with `latitude` and `longitude` columns and then plots them on a map using [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster).

More about this project: [Datasette plugins, and building a clustered map visualization](https://simonwillison.net/2018/Apr/20/datasette-plugins/).

## Demo

[global-power-plants.datasettes.com](https://global-power-plants.datasettes.com/global-power-plants/global-power-plants) hosts a demo of this plugin running against a database of 33,000 power plants around the world.

![Cluster map demo](https://static.simonwillison.net/static/2020/global-power-plants.png)

## Installation

Run `datasette install datasette-cluster-map` to add this plugin to your Datasette virtual environment. Datasette will automatically load the plugin if it is installed in this way.

If you are deploying using the `datasette publish` command you can use the `--install` option:

    datasette publish cloudrun mydb.db --install=datasette-cluster-map

If any of your tables have one of the following pairs of columns a map will be automatically displayed:

- `latitude` and `longitude`
- `lat` and `lng`
- `lat` and `lon`
- `lat` and `long`
- `*_latitude` and `*_longitude`
- `*_lat` and `*_lng` for any of the three variants of `lng`

## Configuration

If your columns are called something else you can configure the column names using [plugin configuration](https://docs.datasette.io/en/stable/plugins.html#plugin-configuration) in a `metadata.json` file. For example, if all of your columns are called `xlat` and `xlng` you can create a `metadata.json` file like this:

```json
{
    "title": "Regular metadata keys can go here too",
    "plugins": {
        "datasette-cluster-map": {
            "latitude_column": "xlat",
            "longitude_column": "xlng"
        }
    }
}
```

Then run Datasette like this:

    datasette mydata.db -m metadata.json

This will configure the required column names for every database loaded by that Datasette instance.

If you want to customize the column names for just one table in one database, you can do something like this:

```json
{
    "databases": {
        "polar-bears": {
            "tables": {
                "USGS_WC_eartag_deployments_2009-2011": {
                    "plugins": {
                        "datasette-cluster-map": {
                            "latitude_column": "Capture Latitude",
                            "longitude_column": "Capture Longitude"
                        }
                    }
                }
            }
        }
    }
}
```

You can also use a custom SQL query to rename those columns to `latitude` and `longitude`, [for example](https://polar-bears.now.sh/polar-bears?sql=select+*%2C%0D%0A++++%22Capture+Latitude%22+as+latitude%2C%0D%0A++++%22Capture+Longitude%22+as+longitude%0D%0Afrom+%5BUSGS_WC_eartag_deployments_2009-2011%5D):

```sql
select *,
    "Capture Latitude" as latitude,
    "Capture Longitude" as longitude
from [USGS_WC_eartag_deployments_2009-2011]
```

The map defaults to being displayed above the main results table on the page. You can use the `"container"` plugin setting to provide a CSS selector indicating an element that the map should be appended to instead.

## Custom tile layers

You can customize the tile layer used  by the maps using the `tile_layer` and `tile_layer_options` configuration settings. For example, to use the [OpenTopoMap](https://opentopomap.org/) you can use these settings:

```json
{
    "plugins": {
        "datasette-cluster-map": {
            "tile_layer": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            "tile_layer_options": {
                "attribution": "Map data: &copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors, <a href='http://viewfinderpanoramas.org'>SRTM</a> | Map style: &copy; <a href='https://opentopomap.org'>OpenTopoMap</a> (<a href='https://creativecommons.org/licenses/by-sa/3.0/'>CC-BY-SA</a>)",
                "maxZoom": 17
            }
        }
    }
}
```
If your tile server provides retina tiles, add `"detectRetina": true` to `tile_layer_options` to enable them.

The [Leaflet Providers preview list](https://leaflet-extras.github.io/leaflet-providers/preview/index.html) has details of many other tile layers you can use.

## Custom marker popups

The marker popup defaults to displaying the data for the underlying database row.

You can customize this by including a `popup` column in your results containing JSON that defines a more useful popup.

The JSON in the popup column should look something like this:

```json
{
    "image": "https://niche-museums.imgix.net/dodgems.heic?w=800&h=400&fit=crop",
    "alt": "Dingles Fairground Heritage Centre",
    "title": "Dingles Fairground Heritage Centre",
    "description": "Home of the National Fairground Collection, Dingles has over 45,000 indoor square feet of vintage fairground rides... and you can go on them! Highlights include the last complete surviving and opera",
    "link": "/browse/museums/26"
}
```

Each of these columns is optional.

- `title` is the title to show at the top of the popup
- `image` is the URL to an image to display in the popup
- `alt` is the alt attribute to use for that image
- `description` is a longer string of text to use as a description
- `link` is a URL that the marker content should link to

You can use the SQLite `json_object()` function to construct this data dynamically as part of your SQL query. Here's an example:

```sql
select json_object(
  'image', photo_url || '?w=800&h=400&fit=crop',
  'title', name,
  'description', substr(description, 0, 200),
  'link', '/browse/museums/' || id
  ) as popup,
  latitude, longitude from museums
where id in (26, 27) order by id
```

[Try that example here](https://www.niche-museums.com/browse?sql=select+json_object%28%0D%0A++%27image%27%2C+photo_url+%7C%7C+%27%3Fw%3D800%26h%3D400%26fit%3Dcrop%27%2C%0D%0A++%27title%27%2C+name%2C%0D%0A++%27description%27%2C+substr%28description%2C+0%2C+200%29%2C%0D%0A++%27link%27%2C+%27%2Fbrowse%2Fmuseums%2F%27+%7C%7C+id%0D%0A++%29+as+popup%2C%0D%0A++latitude%2C+longitude+from+museums) or take a look at [this demo built using a SQL view](https://dogsheep-photos.dogsheep.net/public/photos_on_a_map).

## How I deployed the demo

    datasette publish cloudrun global-power-plants.db \
        --service global-power-plants \
        --metadata metadata.json \
        --install=datasette-cluster-map \
        --extra-options="--config facet_time_limit_ms:1000"

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-cluster-map
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
