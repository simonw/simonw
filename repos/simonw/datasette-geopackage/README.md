# datasette-geopackage

[![PyPI](https://img.shields.io/pypi/v/datasette-geopackage.svg)](https://pypi.org/project/datasette-geopackage/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-geopackage?include_prereleases&label=changelog)](https://github.com/simonw/datasette-geopackage/releases)
[![Tests](https://github.com/simonw/datasette-geopackage/workflows/Test/badge.svg)](https://github.com/simonw/datasette-geopackage/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-geopackage/blob/main/LICENSE)

Datasette plugin for working with GeoPackage databases

## Status

This package does almost nothing useful yet. It has not been published to PyPI.

<!--

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-geopackage

-->

## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-geopackage
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
