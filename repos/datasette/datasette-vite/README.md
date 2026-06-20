# datasette-vite

[![PyPI](https://img.shields.io/pypi/v/datasette-vite.svg)](https://pypi.org/project/datasette-vite/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-vite?include_prereleases&label=changelog)](https://github.com/datasette/datasette-vite/releases)
[![Tests](https://github.com/datasette/datasette-vite/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-vite/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-vite/blob/main/LICENSE)

Utility for writing frontend plugins for Datasette with Vite

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-vite
```
## Usage

This plugin provides a `vite_entry()` function that other Datasette plugins can use to include Vite-built JavaScript and CSS assets in their pages.

### Setting up your plugin

Your plugin needs a Vite project alongside its Python code. Configure `vite.config.ts` to output a manifest and place built files in a `static/` directory:

```ts
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    manifest: true,
    outDir: 'dist',
    rollupOptions: {
      input: 'src/main.ts',
      output: {
        assetFileNames: 'static/[name]-[hash][extname]',
        chunkFileNames: 'static/[name]-[hash].js',
        entryFileNames: 'static/[name]-[hash].js',
      }
    }
  }
})
```

After running `vite build`, copy `dist/.vite/manifest.json` and `dist/static/` into your plugin's Python package directory so they are included when your plugin is installed.

### Using `vite_entry()` in your plugin

```python
from datasette_vite import vite_entry

entry = vite_entry(
    datasette=datasette,
    plugin_package="my_datasette_plugin",
)
html = await entry("src/main.ts")
```

The returned `html` string contains `<script>` and `<link>` tags ready to include in your page:

```html
<link rel="stylesheet" href="/-/static-plugins/my_datasette_plugin/main-def456.css">
<script type="module" src="/-/static-plugins/my_datasette_plugin/main-abc123.js"></script>
```

### Development mode

During development, point your plugin at a running Vite dev server instead of reading from the manifest. This enables hot module replacement.

Configure a dev path via the `datasette-vite` plugin setting, keyed by your plugin's Python package name:

```bash
datasette \
    -s plugins.datasette-vite.dev_paths.my_datasette_plugin http://localhost:5173/
```

If your Vite config uses the default `base: '/'`, a port-only shorthand works too — datasette-vite expands it to `http://localhost:<port>/`:

```bash
datasette \
    -s plugins.datasette-vite.dev_ports.my_datasette_plugin 5173
```

Your plugin code is the same in dev and prod — datasette-vite reads the setting at request time:

```python
entry = vite_entry(
    datasette=datasette,
    plugin_package="my_datasette_plugin",
)
html = await entry("src/main.ts")
```

In dev mode this produces:

```html
<script type="module" src="http://localhost:5173/@vite/client"></script>
<script type="module" src="http://localhost:5173/src/main.ts"></script>
```

### Using `vite_js_urls()` and `vite_css_urls()` for content scripts

If your plugin needs to inject assets into *existing* Datasette pages (rather than owning the full template), use `vite_js_urls()` and `vite_css_urls()`. These return structured data suitable for Datasette's `extra_js_urls` and `extra_css_urls` hooks:

```python
from datasette import hookimpl
from datasette_vite import vite_js_urls, vite_css_urls

@hookimpl
def extra_js_urls(datasette):
    return vite_js_urls(
        datasette=datasette,
        entrypoint="src/main.ts",
        plugin_package="my_datasette_plugin",
    )

@hookimpl
def extra_css_urls(datasette):
    return vite_css_urls(
        datasette=datasette,
        entrypoint="src/main.ts",
        plugin_package="my_datasette_plugin",
    )
```

Dev-mode behavior is controlled by the same `plugins.datasette-vite.dev_paths` / `dev_ports` settings described above.

`vite_js_urls()` returns a list of `{"url": "...", "module": True}` dicts. In dev mode this includes the Vite client script; in prod mode it resolves the hashed filename from the manifest.

`vite_css_urls()` returns a list of CSS URL strings. In dev mode this returns `[]` (Vite injects CSS via JS). In prod mode it collects all CSS from the entrypoint and recursively from imported chunks.

### API reference

#### `vite_entry(datasette, plugin_package, manifest_dir=None)`

- **`datasette`**: The Datasette instance.
- **`plugin_package`**: The Python package name of your plugin (used to resolve the manifest location, generate static asset URLs, and look up dev-mode config).
- **`manifest_dir`**: Optional path to the directory containing `manifest.json`. Defaults to the directory of your plugin package's `__init__.py`.

Returns an async callable. Call it with an entrypoint path (matching a key in your Vite manifest) to get an HTML string of the corresponding `<script>` and `<link>` tags.

#### Dev-mode resolution order

For all three functions, the dev path is resolved from `datasette.plugin_config("datasette-vite")` in this order — first match wins:

1. `dev_paths.<plugin_package>` — full URL.
2. `dev_ports.<plugin_package>` — port number; expanded to `http://localhost:<port>/`.
3. None — production mode; assets are read from the manifest.

#### `vite_js_urls(datasette, entrypoint, plugin_package, manifest_dir=None)`

Returns a list of URL entries suitable for Datasette's `extra_js_urls` hook. Each entry is a `{"url": "...", "module": True}` dict.

#### `vite_css_urls(datasette, entrypoint, plugin_package, manifest_dir=None)`

Returns a list of CSS URL strings suitable for Datasette's `extra_css_urls` hook. Includes CSS from the entrypoint and recursively from imported chunks.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-vite
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
