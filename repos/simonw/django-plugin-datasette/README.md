# django-plugin-datasette

[![PyPI](https://img.shields.io/pypi/v/django-plugin-datasette.svg)](https://pypi.org/project/django-plugin-datasette/)
[![Changelog](https://img.shields.io/github/v/release/simonw/django-plugin-datasette?include_prereleases&label=changelog)](https://github.com/simonw/django-plugin-datasette/releases)
[![Tests](https://github.com/simonw/django-plugin-datasette/workflows/Test/badge.svg)](https://github.com/simonw/django-plugin-datasette/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/django-plugin-datasette/blob/main/LICENSE)

Run [Datasette](https://datasette.io/) inside Django as a [DJP](https://djp.readthedocs.io/) plugin

## Installation

First configure your Django project [to use DJP](https://djp.readthedocs.io/en/latest/installing_plugins.html). Be sure to configure your `asgi.py` file.

Then install this plugin in the same environment as your Django application.
```bash
pip install django-plugin-datasette
```
## Usage

Once installed, `/-/datasette/` will serve a Datasette instance that exposes the contents of any SQLite databases used by Django.

You will need to run Django using ASGI. One way to do that is with [Uvicorn](https://www.uvicorn.org/):

```bash
pip install uvicorn
uvicorn myproject.asgi:application
```

**Warning:** This will expose your entire Django database to anyone who visits `/-/datasette/`. The `auth_user.password` field is automatically redacted, but you should still take care that this does not expose any other sensitive information.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd django-plugin-datasette
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
