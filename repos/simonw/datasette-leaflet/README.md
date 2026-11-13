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

The JavaScript is packaged as a [JavaScript module](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules). You can dynamically import the JavaScript from a custom template like this:

```html+jinja
<script type="module">
import('{{ datasette_leaflet_url }}')
  .then((leaflet) => {
    /* Use leaflet here */
  });
</script>
```

Importing the module also sets a global `window.L` object with the same contents. Leaflet plugins that expect that global, such as [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster), can be loaded once the import has completed. Anything a plugin adds to `L` is available on that global, not on the imported `leaflet` module.

The bundled copy of Leaflet differs from the official release in one other way: tile layers send a `Referer` header by default. See [Tile layers and the Referer header](#tile-layers-and-the-referer-header).

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

## Tile layers and the Referer header

Datasette serves many of its pages, including table pages, with a `Referrer-Policy: no-referrer` header, so by default a browser will not send a `Referer` header when it loads map tiles for those pages. Some tile servers block requests like that. The OpenStreetMap tile server at `tile.openstreetmap.org` is one of them: its [usage policy](https://operations.osmfoundation.org/policies/tiles/) requires a valid `Referer`, and it returns "Access blocked" tiles without one.

To avoid this, the copy of Leaflet bundled with this plugin changes the default for the [referrerPolicy](https://leafletjs.com/reference.html#tilelayer-referrerpolicy) tile layer option from `false` to `"strict-origin-when-cross-origin"`. Tile requests then include a `Referer` header containing just the origin of your Datasette instance, such as `https://example.com/`. The path and query string of the page showing the map are never sent.

This applies to every `L.tileLayer()` and `L.tileLayer.wms()` created using the bundled Leaflet, including those created by other plugins.

### Changing the policy for a Datasette instance

Use the `tile_referrer_policy` plugin setting. Set it to `false` to go back to sending no `Referer` header for tiles:

```yaml
plugins:
  datasette-leaflet:
    tile_referrer_policy: false
```

Or set it to any other [referrer policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy#directives), such as `origin`:

```yaml
plugins:
  datasette-leaflet:
    tile_referrer_policy: origin
```

This goes in `datasette.yaml` for Datasette 1.0, or in `metadata.yaml` for earlier versions.

The value in use is available to JavaScript as `datasette.leaflet.TILE_REFERRER_POLICY`. Leaflet reads it once, when the JavaScript is first loaded.

### Changing the policy for a single tile layer

Pass the `referrerPolicy` option when you create the layer. This takes precedence over the plugin setting:

```javascript
let tiles = leaflet.tileLayer("https://tiles.example.com/{z}/{x}/{y}.png", {
    referrerPolicy: false
});
```

To change the default for every layer created after that point, use `leaflet.TileLayer.mergeOptions({referrerPolicy: false})`.
