# datasette-total-page-time

[![PyPI](https://img.shields.io/pypi/v/datasette-total-page-time.svg)](https://pypi.org/project/datasette-total-page-time/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-total-page-time?include_prereleases&label=changelog)](https://github.com/simonw/datasette-total-page-time/releases)
[![Tests](https://github.com/simonw/datasette-total-page-time/workflows/Test/badge.svg)](https://github.com/simonw/datasette-total-page-time/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-total-page-time/blob/main/LICENSE)

Add a note to the Datasette footer measuring the total page load time

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-total-page-time

## Usage

Once this plugin is installed, a note will appear in the footer of every page showing how long the page took to generate.

> Queries took 326.74ms · Page took 386.310ms

## How it works

Measuring how long a page takes to load and then injecting that note into the page is tricky, because you need to finish generating the page before you know how long it took to load it!

This plugin uses the [asgi_wrapper](https://docs.datasette.io/en/stable/plugin_hooks.html#asgi-wrapper-datasette) plugin hook to measure the time taken by Datasette and then inject the following JavaScript at the bottom of the response, after the closing `</html>` tag but with the correct measured value:

```html
<script>
let footer = document.querySelector("footer");
if (footer) {
    let ms = 37.224;
    let s = ` &middot; Page took ${ms.toFixed(3)}ms`;
    footer.innerHTML += s;
}
</script>
```
This script is injected only on pages with the `text/html` content type - so it should not affect JSON or CSV returned by Datasette.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-total-page-time
    python3 -mvenv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
