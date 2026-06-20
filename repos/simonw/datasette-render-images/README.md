# datasette-render-images

[![PyPI](https://img.shields.io/pypi/v/datasette-render-images.svg)](https://pypi.org/project/datasette-render-images/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-render-images?include_prereleases&label=changelog)](https://github.com/simonw/datasette-render-images/releases)
[![Tests](https://github.com/simonw/datasette-render-images/workflows/Test/badge.svg)](https://github.com/simonw/datasette-render-images/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-render-images/blob/main/LICENSE)

A Datasette plugin that renders binary blob images with data-uris, using the [render_cell() plugin hook](https://docs.datasette.io/en/stable/plugins.html#render-cell-value-column-table-database-datasette).

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-render-images

## Usage

If a database row contains binary image data (PNG, GIF or JPEG), this plugin will detect that it is an image (using the [imghdr module](https://docs.python.org/3/library/imghdr.html) and render that cell using an `<img src="data:image/png;base64,...">` element.

Here's a [demo of the plugin in action](https://datasette-render-images-demo.datasette.io/favicons/favicons).

## Creating a compatible database table

You can use the [sqlite-utils insert-files](https://sqlite-utils.datasette.io/en/stable/cli.html#inserting-data-from-files) command to insert image files into a database table:

    $ pip install sqlite-utils
    $ sqlite-utils insert-files gifs.db images *.gif

See [Fun with binary data and SQLite](https://simonwillison.net/2020/Jul/30/fun-binary-data-and-sqlite/) for more on this tool.

## Configuration

By default the plugin will only render images that are smaller than 100KB. You can adjust this limit using the `size_limit` plugin configuration option - for example, to increase the limit to 1MB (1000000 bytes) use the following in `metadata.json`:

```json
{
    "plugins": {
        "datasette-render-images": {
            "size_limit": 1000000
        }
    }
}
```
