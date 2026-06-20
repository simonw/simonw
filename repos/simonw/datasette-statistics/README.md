# datasette-statistics

[![PyPI](https://img.shields.io/pypi/v/datasette-statistics.svg)](https://pypi.org/project/datasette-statistics/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-statistics?include_prereleases&label=changelog)](https://github.com/simonw/datasette-statistics/releases)
[![Tests](https://github.com/simonw/datasette-statistics/workflows/Test/badge.svg)](https://github.com/simonw/datasette-statistics/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-statistics/blob/main/LICENSE)

SQL statistics functions for Datasette

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-statistics
```
## Usage

This plugin adds new SQL aggregate functions for use within Datasette:

- `statistics_mean()` for calculating the [mean](https://docs.python.org/3/library/statistics.html#statistics.mean)
- `statistics_geometric_mean()` for calculating the [geometric mean](https://docs.python.org/3/library/statistics.html#statistics.geometric_mean) (requires Python 3.8+)
- `statistics_median()` for calculating the [median](https://docs.python.org/3/library/statistics.html#statistics.median)
- `statistics_median_low()` for calculating the [low median](https://docs.python.org/3/library/statistics.html#statistics.median_low)
- `statistics_median_high()` for calculating the [high median](https://docs.python.org/3/library/statistics.html#statistics.median_high)
- `statistics_mode()` for calculating the [mode](https://docs.python.org/3/library/statistics.html#statistics.mode)
- `statistics_stdev()` for calculating the [sample standard deviation](https://docs.python.org/3/library/statistics.html#statistics.stdev)
- `statistics_pstdev()` for calculating the [population standard deviation](https://docs.python.org/3/library/statistics.html#statistics.pstdev)
- `statistics_variance()` for calculating the [sample variance](https://docs.python.org/3/library/statistics.html#statistics.variance)
- `statistics_pvariance()` for calculating the [population variance](https://docs.python.org/3/library/statistics.html#statistics.pvariance)

These all use the implementations from the [Python statistics library](https://docs.python.org/3/library/statistics.html).

Use them like this:
```sql
select statistics_mean(numeric_column) from mytable
```
## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-statistics
python3 -mvenv venv
source venv/bin/activate
```
Or if you are using `pipenv`:
```bash
pipenv shell
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```