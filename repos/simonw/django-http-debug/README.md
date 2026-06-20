# django-http-debug

[![PyPI](https://img.shields.io/pypi/v/django-http-debug.svg)](https://pypi.org/project/django-http-debug/)
[![Tests](https://github.com/simonw/django-http-debug/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/django-http-debug/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/django-http-debug?include_prereleases&label=changelog)](https://github.com/simonw/django-http-debug/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/django-http-debug/blob/main/LICENSE)

Django app for creating database-backed HTTP debug endpoints

Background on this project: [django-http-debug, a new Django app mostly written by Claude](https://simonwillison.net/2024/Aug/8/django-http-debug/)

## Installation

Install this library using `pip`:
```bash
pip install django-http-debug
```
## Configuration

Once installed in the same environment as your Django application, add the following to `INSTALLED_APPS` in your Django settings:
```python
INSTALLED_APPS = [
    # ...
    'django_http_debug',
    # ...
]
```
And add this to `MIDDLEWARE`:
```python
MIDDLEWARE = [
    # ...
    "django_http_debug.middleware.DebugMiddleware",
    # ...
]
```
Then run `./manage.py migrate` to create the necessary database tables.

## Usage

You can configure new endpoints in the Django admin. These will only work if they are for URLs that are not yet being served by the rest of your application.

Give an endpoint a path (starting without a `/`) such as:

    webhooks/debug/

You can optionally configure the returned body or HTTP headers here too.

If you want to return a binary body - a GIF for example - you can set that endpoint to use Base64 encoding and then paste a base64-encoded string into the body field.

On macOS you can create base64 strings like this:
```bash
base64 -i pixel.gif -o -
```
Any HTTP requests made to `/webhooks/debug/` will be logged in the database. You can view these requests in the Django admin.

You can turn off the "Logging enabled" option on an endpoint to stop logging requests to it to the database.

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd django-http-debug
python -m venv venv
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
