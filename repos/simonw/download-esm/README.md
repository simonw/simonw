# download-esm

[![PyPI](https://img.shields.io/pypi/v/download-esm.svg)](https://pypi.org/project/download-esm/)
[![Changelog](https://img.shields.io/github/v/release/simonw/download-esm?include_prereleases&label=changelog)](https://github.com/simonw/download-esm/releases)
[![Tests](https://github.com/simonw/download-esm/workflows/Test/badge.svg)](https://github.com/simonw/download-esm/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/download-esm/blob/master/LICENSE)

Download ESM modules from npm and jsdelivr

See [download-esm: a tool for downloading ECMAScript modules](https://simonwillison.net/2023/May/2/download-esm/) for background on this project.

## Installation

Install this tool using `pip`:

    pip install download-esm

## Warning

This is **alpha software**. It works for downloading Observable Plot, but has not been tested against many other packages yet.

[Your help welcome](https://github.com/simonw/download-esm/issues/2) in testing this further!

## Usage

To download Observable Plot and all of its dependencies as ECMAScript modules:

    download-esm @observablehq/plot

This will download around 40 `.js` files to the current directory.

To put them in another directory, add that as an argument:

    download-esm @observablehq/plot ./js

Each file will have any `import` and `export` statements rewritten as relative paths.

You can then use the library in your own HTML and JavaScript something like this:

```html
<div id="myplot"></div>
<script type="module">
import * as Plot from "./js/observablehq-plot-0-6-6.js";
const plot = Plot.rectY(
    {length: 10000}, Plot.binX({y: "count"}, {x: Math.random})
).plot();
const div = document.querySelector("#myplot");
div.append(plot);
</script>
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd download-esm
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
