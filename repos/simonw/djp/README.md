# DJP: Django Plugins

[![PyPI](https://img.shields.io/pypi/v/djp.svg)](https://pypi.org/project/djp/)
[![Tests](https://github.com/simonw/djp/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/djp/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/djp?include_prereleases&label=changelog)](https://github.com/simonw/djp/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/djp/blob/main/LICENSE)

A plugin system for Django

Visit **[djp.readthedocs.io](https://djp.readthedocs.io/)** for full documentation, including how to install plugins and how to write new plugins.

See [DJP: A plugin system for Django](https://simonwillison.net/2024/Sep/25/djp-a-plugin-system-for-django/) for an introduction to this project.

## Installation

Install this library using `pip`:
```bash
pip install djp
```

## Configuration

Add this to the **end** of your `settings.py` file:
```python
import djp

# ... existing settings.py contents

djp.settings(globals())
```
Then add this to your URL configuration in `urls.py`:
```python
urlpatterns = [
    # ...
] + djp.urlpatterns()
```

## Usage

Installing a plugin in the same environment as your Django application should cause that plugin to automatically add the necessary 

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd djp
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
