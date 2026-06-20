# datasette-leaflet

[![PyPI](https://img.shields.io/pypi/v/datasette-leaflet.svg)](https://pypi.org/project/datasette-leaflet/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-leaflet?include_prereleases&label=changelog)](https://github.com/simonw/datasette-leaflet/releases)
[![Tests](https://github.com/simonw/datasette-leaflet/workflows/Test/badge.svg)](https://github.com/simonw/datasette-leaflet/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-leaflet/blob/main/LICENSE)

Datasette plugin adding the [Leaflet](https://leafletjs.com/) JavaScript library.

A growing number of Datasette plugins depend on the Leaflet JavaScript mapping library. They each have their own way of loading Leaflet, which could result in loading it multiple times (with multiple versions) if more than one plugin is installed.

This library is intended to solve this problem, by providing a single plugin they can all depend on that loads Leaflet in a reusable way.

Plugins that use this:

- [datasette-leaflet-freedraw](https://datasette.io/plugins/datasette-leaflet-freedraw)
- [datasette-leaflet-geojson](https://datasette.io/plugins/datasette-leaflet-geojson)
- [datasette-cluster-map](https://datasette.io/plugins/datasette-cluster-map)

## Installation

You can install this plugin like so:

    datasette install datasette-leaflet

Usually this plugin will be a dependency of other plugins, so it should be installed automatically when you install them.

## Usage

The plugin makes `leaflet.js` and `leaflet.css` available as static files. It provides two custom template variables with the URLs of those two files.

- `{{ datasette_leaflet_url }}` is the URL to the JavaScript
- `{{ datasette_leaflet_css_url }}` is the URL to the CSS

These URLs are also made available as global JavaScript constants:

- `datasette.leaflet.JAVASCRIPT_URL`
- `datasette.leaflet.CSS_URL`

The JavaScript is packaed as a [JavaScript module](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules). You can dynamically import the JavaScript from a custom template like this:

```html+jinja
<script type="module">
import('{{ datasette_leaflet_url }}')
  .then((leaflet) => {
    /* Use leaflet here */
  });
</script>
```

You can load the CSS like this:

```html+jinja
<link rel="stylesheet" href="{{ datasette_leaflet_css_url }}">
```

Or dynamically like this:

```html+jinja
<script>
let link = document.createElement('link');
link.rel = 'stylesheet';
link.href = '{{ datasette_leaflet_css_url }}';
document.head.appendChild(link);
</script>
```

Here's a full example that loads the JavaScript and CSS and renders a map:

```html+jinja
<script type="module">
window.DATASETTE_CLUSTER_MAP_TILE_LAYER = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
window.DATASETTE_CLUSTER_MAP_TILE_LAYER_OPTIONS = {"maxZoom": 19, "detectRetina": true, "attribution": "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors"};
let link = document.createElement('link');
link.rel = 'stylesheet';
link.href = '{{ datasette_leaflet_css_url }}';
document.head.appendChild(link);
import('{{ datasette_leaflet_url }}')
  .then((leaflet) => {
    let div = document.createElement('div');
    div.style.height = '400px';
    document.querySelector('.content').appendChild(div);
    let tiles = leaflet.tileLayer(
        window.DATASETTE_CLUSTER_MAP_TILE_LAYER,
        window.DATASETTE_CLUSTER_MAP_TILE_LAYER_OPTIONS
    );
    let map = leaflet.map(div, {
        center: leaflet.latLng(0, 0),
        zoom: 2,
        layers: [tiles]
    });
  });
</script>
```
