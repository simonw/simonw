# datasette-jupyterlite

[![PyPI](https://img.shields.io/pypi/v/datasette-jupyterlite.svg)](https://pypi.org/project/datasette-jupyterlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-jupyterlite?include_prereleases&label=changelog)](https://github.com/simonw/datasette-jupyterlite/releases)
[![Tests](https://github.com/simonw/datasette-jupyterlite/workflows/Test/badge.svg)](https://github.com/simonw/datasette-jupyterlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-jupyterlite/blob/main/LICENSE)

[JupyterLite](https://jupyterlite.readthedocs.io/en/latest/) as a Datasette plugin

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-jupyterlite

## Demo

You can try out a demo of the plugin here: https://latest-with-plugins.datasette.io/jupyterlite/

Run this example code in a Pyolite notebook to pull all of the data from the [github/stars](https://latest-with-plugins.datasette.io/github/stars) table into a Pandas DataFrame:

```python
import pandas, pyodide

df = pandas.read_csv(pyodide.open_url(
  "https://latest-with-plugins.datasette.io/github/stars.csv?_labels=on&_stream=on&_size=max")
)
```

## Usage

Once installed, visit `/jupyterlite/` to access JupyterLite served from your Datasette instance.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-jupyterlite
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
