# django-plugin-database-url

[![PyPI](https://img.shields.io/pypi/v/django-plugin-database-url.svg)](https://pypi.org/project/django-plugin-database-url/)
[![Changelog](https://img.shields.io/github/v/release/simonw/django-plugin-database-url?include_prereleases&label=changelog)](https://github.com/simonw/django-plugin-database-url/releases)
[![Tests](https://github.com/simonw/django-plugin-database-url/workflows/Test/badge.svg)](https://github.com/simonw/django-plugin-database-url/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/django-plugin-database-url/blob/main/LICENSE)

Django plugin that reads the `DATABASE_URL` environment variable

## Installation

First configure your Django project [to use DJP](https://djp.readthedocs.io/en/latest/installing_plugins.html).

Then install this plugin in the same environment as your Django application.
```bash
pip install django-plugin-database-url
```
## Usage

Once installed, any `DATABASE_URL` environment variable will be automatically used to configure your Django database setting, using [dj-database-url](https://github.com/jazzband/dj-database-url).

This plugin mainly exists to demonstrate the [settings() plugin hook](https://djp.readthedocs.io/en/latest/plugin_hooks.html#settings-current-settings) in [DJP](https://djp.readthedocs.io/).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd django-plugin-database-url
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
