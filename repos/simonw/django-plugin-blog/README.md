# django-plugin-blog

[![PyPI](https://img.shields.io/pypi/v/django-plugin-blog.svg)](https://pypi.org/project/django-plugin-blog/)
[![Changelog](https://img.shields.io/github/v/release/simonw/django-plugin-blog?include_prereleases&label=changelog)](https://github.com/simonw/django-plugin-blog/releases)
[![Tests](https://github.com/simonw/django-plugin-blog/workflows/Test/badge.svg)](https://github.com/simonw/django-plugin-blog/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/django-plugin-blog/blob/main/LICENSE)

A simple blog implemented as a [DJP plugin](https://djp.readthedocs.io/).

## Installation

Install this plugin in the same environment as your Django application.
```bash
pip install django-plugin-blog
```
## Usage

This adds a blog at `/blog/`, configured to be edited using the Django admin.

## Custom templates

The default templates expect a base template with `{% block title %}` and `{% block content %}` and `{% block extra_head %}` blocks.

You can use the `DJANGO_PLUGIN_BLOG_BASE_TEMPLATE` setting to point to an existing base template.

You can also provide your own versions of the following template files in your own templates directory:

- `django_plugin_blog/base.html` - the base template for the blog
- `django_plugin_blog/index.html` - the index page, at `/blog/`
- `django_plugin_blog/archive.html` - the archive page, at `/blog/archive/`
- `django_plugin_blog/year.html` - the archive for a year, at `/blog/YYYY/`
- `django_plugin_blog/tag.html` - the archive for a tag, at `/blog/tag/TAG/`
- `django_plugin_blog/entry.html` - the detail page for an entry, at `/blog/YYYY/slug/`

## Atom feed

A feed is provided at `/blog/feed/`. You can customize the title of this feed using the `DJANGO_PLUGIN_BLOG_FEED_TITLE` setting.

## Custom URL

The plugin adds URLs under `/blog/` by default. You can change this using the `DJANGO_PLUGIN_BLOG_URL_PREFIX` setting.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd django-plugin-blog
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
