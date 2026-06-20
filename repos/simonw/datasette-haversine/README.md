# datasette-haversine

[![PyPI](https://img.shields.io/pypi/v/datasette-haversine.svg)](https://pypi.org/project/datasette-haversine/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-haversine?include_prereleases&label=changelog)](https://github.com/simonw/datasette-haversine/releases)
[![Tests](https://github.com/simonw/datasette-haversine/workflows/Test/badge.svg)](https://github.com/simonw/datasette-haversine/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-haversine/blob/main/LICENSE)

Datasette plugin that adds a custom SQL function for haversine distances

Install this plugin in the same environment as Datasette to enable the `haversine()` SQL function.
```bash
datasette install datasette-haversine
```
The plugin is built on top of the [haversine](https://github.com/mapado/haversine) library.

## haversine() to calculate distances

```sql
select haversine(lat1, lon1, lat2, lon2);
```

This will return the distance in kilometers between the point defined by `(lat1, lon1)` and the point defined by `(lat2, lon2)`.

## Demo

You can try this function [here using Datasette Lite](https://lite.datasette.io/?install=datasette-haversine#/content?sql=select+haversine%28%0A++40.7128%2C+-74.0060%2C+--+New+York%0A++37.7749%2C+-122.4194%2C+--+San+Francisco%0A++%27mi%27%0A%29+as+distance_in_miles%3B).

```sql
select haversine(
  40.7128, -74.0060, -- New York
  37.7749, -122.4194, -- San Francisco
  'mi'
) as distance_in_miles;
```

## Custom units

By default `haversine()` returns results in km. You can pass an optional third argument to get results in a different unit:

- `ft` for feet
- `m` for meters
- `in` for inches
- `mi` for miles
- `nmi` for nautical miles
- `km` for kilometers (the default)

```sql
select haversine(lat1, lon1, lat2, lon2, 'mi');
```
