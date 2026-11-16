# datasette-maplibre

[![PyPI](https://img.shields.io/pypi/v/datasette-maplibre.svg)](https://pypi.org/project/datasette-maplibre/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-maplibre?include_prereleases&label=changelog)](https://github.com/datasette/datasette-maplibre/releases)
[![Tests](https://github.com/datasette/datasette-maplibre/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-maplibre/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-maplibre/blob/main/LICENSE)

Datasette plugin that maps latitude/longitude and GeoJSON data using [MapLibre GL](https://maplibre.org/) and [OpenFreeMap](https://openfreemap.org/).

It combines the features of [datasette-cluster-map](https://github.com/simonw/datasette-cluster-map) and [datasette-leaflet-geojson](https://github.com/simonw/datasette-leaflet-geojson) on a vector map, and adds some of its own.

## Demo

**[Try the demo instance](https://lite.datasette.io/?install=datasette-maplibre&url=https://gist.githubusercontent.com/simonw/39fa5d399465766039549912e2b3d291/raw/f6dfba99a75cbb8b5d9386223220eb52272767ee/demo.db&metadata=https://gist.githubusercontent.com/simonw/39fa5d399465766039549912e2b3d291/raw/f6dfba99a75cbb8b5d9386223220eb52272767ee/metadata.yml)**, which runs in your browser using [Datasette Lite](https://lite.datasette.io/).

Its home page is a guided tour of every feature: 19 links, each opening a map set up to show one thing. It uses 35,000 power plants, a month of earthquakes, country boundaries, rivers, capital cities and landmarks with photographs.

To run the same demo locally, use the `demo/` directory:

    uv run python demo/build.py
    uv run datasette demo/demo.db -m demo/metadata.yml -c demo/datasette.yml --setting max_returned_rows 5000

`build.py` downloads about 14MB of open data to `demo/cache/` the first time it runs, then builds `demo/demo.db`. Run it with `--refresh` to fetch the data again, for example for more recent earthquakes.

## Installation

Install this plugin in the same environment as Datasette. It requires Datasette 1.0a43 or later.

    datasette install datasette-maplibre

MapLibre GL JS 6.17.0 is bundled with the plugin. Map styles, tiles and fonts are loaded from `tiles.openfreemap.org` unless you configure a different style.

## Usage

### An overview map above the table

A map is shown above any table, SQL query or row that has one of these pairs of columns:

- `latitude` and `longitude`
- `lat` and `lng`, `lon` or `long`
- `*_latitude` and `*_longitude`
- `*_lat` and `*_lng`, `*_lon` or `*_long`

It is also shown for tables and queries with several rows of GeoJSON, in which case every shape is drawn on the one map. A table with both gets points and shapes together.

Rows are loaded from the Datasette JSON API. If there are more rows than fit in one page a "load all" button fetches the rest, with a "pause" button to stop. The map is added to the page once the first row with a location has loaded.

The toolbar above the map offers:

- **View** - clusters, individual points or a heatmap
- **Colour by** - colour the points and shapes by any column. Columns with up to ten distinct values get a legend with counts, numeric columns with more get a colour ramp.
- **Globe** - switch between a globe and a flat map
- **Filter to this area** - on table pages, reloads the table with filters such as `?latitude__gte=...` so that it only contains rows inside the area the map is showing. "Clear area filter" removes them.
- **Download GeoJSON** - everything loaded onto the map so far, as a GeoJSON file with the other columns as properties

The map also has zoom, compass and fullscreen controls. To tilt it into 3D, drag with the right mouse button or with ctrl held down: zoom in to a city to see the buildings.

Other things to know:

- Clicking a point or shape shows a popup with the row, and highlights that row in the table if it is on the current page.
- Rows that share exactly the same location are drawn as one numbered disc at every zoom level, in every view. Clicking it opens a popup with arrows for stepping through each of those rows.
- Hovering over a table row highlights its point or shape on the map.
- The map shows every row, where the table shows one page of them. When the map has more, the line under it says "All 171 rows are on the map".
- Shapes that are too small to see at the current zoom level are marked with a circle.
- The position of the map is kept in the URL, as `#map=zoom/latitude/longitude`, so a link to the page is a link to that view of the map. So are the view, colour and globe when they differ from the configured ones: `#view=heatmap&color=fuel&globe=1`. These can be used in links you write yourself.
- The map never zooms out so far that the world is repeated side by side.
- Scrolling the page does not zoom the map. Use ctrl + scroll (⌘ + scroll on macOS), or the zoom buttons.

### A map for every GeoJSON value

Any table cell containing GeoJSON - a geometry, a `Feature` or a `FeatureCollection` - is replaced by a map of it.

Each cell first gets an outline of its geometry drawn as SVG, which is instant. Cells then turn into interactive maps as they scroll into view. Browsers limit how many WebGL maps a page can have, so only eight cells are live maps at once: when a ninth is needed, the oldest one that is off screen goes back to being an outline. This means a page with hundreds of shapes works.

### Custom popups

The popup defaults to displaying the row. Include a `popup` column containing JSON to replace it:

```sql
select json_object(
  'image', photo_url,
  'alt', 'Photo of ' || name,
  'title', name,
  'description', substr(description, 0, 200),
  'link', '/browse/museums/' || id
) as popup, latitude, longitude from museums
```

Every key is optional. This is the same format that datasette-cluster-map uses. `link` and `image` must be `http://`, `https://` or relative URLs.

## Configuration

All of these are optional. They can be set for the whole instance, for a database or for a table, and more specific settings are merged over more general ones.

```json
{
    "plugins": {
        "datasette-maplibre": {
            "latitude_column": "xlat",
            "longitude_column": "xlng",
            "style": "https://example.com/style.json",
            "view": "points",
            "color_column": "category",
            "height": "70vh",
            "scroll_zoom": true,
            "max_cell_maps": 12,
            "cluster_radius": 50,
            "container": "#map-goes-here"
        }
    }
}
```

- `latitude_column` and `longitude_column` - the columns to use, if they do not match the patterns above
- `style` - the URL of a [MapLibre style](https://maplibre.org/maplibre-style-spec/), or a complete style as a JSON object. Defaults to the OpenFreeMap Liberty style, `https://tiles.openfreemap.org/styles/liberty`.
- `view` - `clusters` (the default), `points` or `heatmap`
- `color_column` - a column to colour by to begin with
- `height` - CSS height of the overview map, default `500px`
- `scroll_zoom` - set to `true` to zoom the overview map with the scroll wheel alone
- `max_cell_maps` - how many GeoJSON cells can be interactive maps at once, default 8
- `cluster_radius` - how close points have to be, in pixels, to be merged into one cluster. Default 25. Smaller values give more, smaller clusters.
- `container` - CSS selector of an element to add the overview map to, instead of above the table

The MapLibre map object for the overview map is available to other JavaScript as `datasette.maplibre.map`.

## Development

To set up this plugin locally, first checkout the code. Then run the tests using [uv](https://docs.astral.sh/uv/):

    cd datasette-maplibre
    uv run pytest

Some of the tests use [Playwright](https://playwright.dev/python/) to drive a real browser. They use an empty map style, so they do not need to fetch any tiles. If they fail because the browser is missing, install it like this:

    uv run playwright install chromium

To update MapLibre GL JS, replace `maplibre-gl.mjs`, `maplibre-gl-worker.mjs` and `maplibre-gl.css` in `datasette_maplibre/static/` with the files from the `dist/` directory of the [maplibre-gl npm package](https://www.npmjs.com/package/maplibre-gl). The two `.mjs` files must stay next to each other.
