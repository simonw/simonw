# datasette-placekey

[![PyPI](https://img.shields.io/pypi/v/datasette-placekey.svg)](https://pypi.org/project/datasette-placekey/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-placekey?include_prereleases&label=changelog)](https://github.com/simonw/datasette-placekey/releases)
[![Tests](https://github.com/simonw/datasette-placekey/workflows/Test/badge.svg)](https://github.com/simonw/datasette-placekey/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-placekey/blob/main/LICENSE)

SQL functions for working with [placekeys](https://www.placekey.io/).

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-placekey

## Usage

The following SQL functions are exposed - [documentation here](https://placekey.github.io/placekey-py/placekey.html#module-placekey.placekey).

```sql
select
  geo_to_placekey(33.0896104,129.7900839),
  placekey_to_geo('@6nh-nhh-kvf'),
  placekey_to_geo_latitude('@6nh-nhh-kvf'),
  placekey_to_geo_longitude('@6nh-nhh-kvf'),
  placekey_to_h3('@6nh-nhh-kvf'),
  h3_to_placekey('8a30d94e4c87fff'),
  placekey_to_geojson('@6nh-nhh-kvf'),
  placekey_to_wkt('@6nh-nhh-kvf'),
  placekey_format_is_valid('@6nh-nhh-kvf');
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-placekey
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
