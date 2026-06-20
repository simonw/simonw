# datasette-enrichments-opencage

[![PyPI](https://img.shields.io/pypi/v/datasette-enrichments-opencage.svg)](https://pypi.org/project/datasette-enrichments-opencage/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-enrichments-opencage?include_prereleases&label=changelog)](https://github.com/datasette/datasette-enrichments-opencage/releases)
[![Tests](https://github.com/datasette/datasette-enrichments-opencage/workflows/Test/badge.svg)](https://github.com/datasette/datasette-enrichments-opencage/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-enrichments-opencage/blob/main/LICENSE)

Geocoding enrichment using OpenCage

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-enrichments-opencage
```
## Usage

This plugin adds an enrichment for geocoding using the [OpenCage Geocoder](https://opencagedata.com/).

You will need an API key from OpenCage - you can sign up for a free trial at https://opencagedata.com/users/sign_up.

Filter for data that you wish to geocode, then apply the OpenCage geocoder enrichment.

You'll need to specify a template to be passed to the geocoder, specifying which templates should be used as the input.

If you have a single column containing the address, you can use this:

    {{ address }}

If you have separate columns for the street, city, state and country, you can use this:

    {{ street }}, {{ city }}, {{ state }}, {{ country }}

If your address column is missing the country, but all of the addresses are in the USA, you could use this:

    {{ address }}, USA

See the [OpenCage guide](https://opencagedata.com/guides/how-to-format-your-geocoding-query) for tips on how to get the best results.

By default only the latitude and longitude from the geocoder will be stored, in the `latitude` and `longitude` columns on your table. These columns will be created if they do not yet exist.

You can optionally specify a column to store the full JSON output of the geocoder. This column will also be created if it does not exist.

The full JSON format is [described here](https://opencagedata.com/api#response).

## Configuration

You can use this plugin without configuration, but you'll need to enter your API key every time you run an enrichment.

To avoid that, you can set your API key as plugin configuration like this:

```bash
export OPENCAGE_API_KEY="your-api-key"
```
Then in `metadata.yml`:
```yaml
plugins:
  datasette-enrichments-opencage:
    api_key:
      $env: OPENCAGE_API_KEY
```
Then run Datasette like this:
```bash
datasette mydatabase.db -m metadata.yml --root
```
This well give you a URL to sign in as the "root" user, which grants you access to the enrichment.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-enrichments-opencage
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
