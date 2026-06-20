# datasette-psutil

[![PyPI](https://img.shields.io/pypi/v/datasette-psutil.svg)](https://pypi.org/project/datasette-psutil/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-psutil?include_prereleases&label=changelog)](https://github.com/simonw/datasette-psutil/releases)
[![Tests](https://github.com/simonw/datasette-psutil/workflows/Test/badge.svg)](https://github.com/simonw/datasette-psutil/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-psutil/blob/main/LICENSE)

Datasette plugin adding a `/-/psutil` debugging endpoint

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-psutil

## Usage

Visit `/-/psutil` on your Datasette instance to see various information provided by [psutil](https://psutil.readthedocs.io/).

## Demo

https://latest-with-plugins.datasette.io/-/psutil is a live demo of this plugin, hosted on Google Cloud Run.
