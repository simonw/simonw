# summarize-template

[![PyPI](https://img.shields.io/pypi/v/summarize-template.svg)](https://pypi.org/project/summarize-template/)
[![Changelog](https://img.shields.io/github/v/release/simonw/summarize-template?include_prereleases&label=changelog)](https://github.com/simonw/summarize-template/releases)
[![Tests](https://github.com/simonw/summarize-template/workflows/Test/badge.svg)](https://github.com/simonw/summarize-template/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/summarize-template/blob/master/LICENSE)

Show a summary of a Django or Jinja template

## Installation

Install this tool using `pip`:

    pip install summarize-template

## Usage

You can run the command against a template file like this:

    summarize-template path/to/template.html

The tool will output just the structural tags from the template.

## Example

Given a template that looks like this:

```html+jinja
{% extends "base.html" %}

{% block title %}This is the title{% endblock %}

{% block content %}
<h1>{{ title }}</h1>
{% if docs %}
    <ul>
        {% for doc in docs %}
            <li><a href="{{ doc.url }}">{{ doc.title }}</a></li>
        {% endfor %}
    </ul>
{% endif %}
{% endblock %}
```
Running `summarize-template` against it will produce the following:
```html+jinja
{% extends "base.html" %}
{% block title %}   {% endblock %}
{% block content %}
{{ title }}
{% if docs %}
        {% for doc in docs %}
             {{ doc.url }}{{ doc.title }}
        {% endfor %}
{% endif %}
{% endblock %}
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd summarize-template
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
