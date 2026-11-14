# datasette-vega

[![PyPI](https://img.shields.io/pypi/v/datasette-vega.svg)](https://pypi.org/project/datasette-vega/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-vega/blob/main/LICENSE)

A [Datasette](https://github.com/simonw/datasette) plugin that provides tools
for generating charts using [Vega](https://vega.github.io/).

![Datasette Vega interface](https://raw.githubusercontent.com/simonw/datasette-vega/main/datasette-vega.png)

Try it out in your browser using [Datasette Lite](https://lite.datasette.io/?install=datasette-vega&csv=https%3A%2F%2Fraw.githubusercontent.com%2Ffivethirtyeight%2Fdata%2Fmaster%2Fairline-safety%2Fairline-safety.csv#/data/airline-safety?_size=max#g.mark=bar&g.x_column=airline&g.x_type=ordinal&g.y_column=fatalities_00_14&g.y_type=quantitative), which installs the latest release of this plugin and charts fatalities per airline from 2000 to 2014, using [FiveThirtyEight's airline safety data](https://github.com/fivethirtyeight/data/tree/master/airline-safety).

To add this to your Datasette installation, install the plugin like so:

    pip install datasette-vega

The plugin will then add a "Show charting options" button to every Datasette table and SQL query page.

If you are publishing data using the `datasette publish` command, you can
include this plugin like so:

    datasette publish cloudrun mydatabase.db --service=my-service --install=datasette-vega

## Development

The JavaScript is bundled using [esbuild](https://esbuild.github.io/). Install the dependencies and build the plugin's static assets into `datasette_vega/static/` like this:

    npm install
    npm run build

This needs to run before building the Python package, since the bundled assets are not checked into the repository.

To work on the charting interface against the demo page in `public/index.html`, with automatic rebuilds:

    npm run dev

Then open `http://localhost:3000/`.

To run the Python tests (after `npm run build`):

    uv run pytest
