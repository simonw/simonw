# django-plugin-django-header

[![PyPI](https://img.shields.io/pypi/v/django-plugin-django-header.svg)](https://pypi.org/project/django-plugin-django-header/)
[![Changelog](https://img.shields.io/github/v/release/simonw/django-plugin-django-header?include_prereleases&label=changelog)](https://github.com/simonw/django-plugin-django-header/releases)
[![Tests](https://github.com/simonw/django-plugin-django-header/workflows/Test/badge.svg)](https://github.com/simonw/django-plugin-django-header/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/django-plugin-django-header/blob/main/LICENSE)

Add a Django-Compositions HTTP header to a Django app

## Installation

First [install and configure DJP](https://djp.readthedocs.io/en/latest/installing_plugins.html).

Then install this plugin in the same environment as your Django application.
```bash
pip install django-plugin-django-header
```
## Usage

Once installed, every response from the application will include a `Django-Composition` HTTP header listing [a composition by Django Reinhardt](https://en.wikipedia.org/wiki/List_of_compositions_by_Django_Reinhardt). For example:

```bash
curl -I http://localhost:8000/
```
```
HTTP/1.1 200 OK
Server: WSGIServer/0.2 CPython/3.12.0
Content-Type: text/html; charset=utf-8
Django-Composition: Castle of My Dreams
...
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd django-plugin-django-header
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
