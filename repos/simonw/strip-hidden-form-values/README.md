# strip-hidden-form-values

[![PyPI](https://img.shields.io/pypi/v/strip-hidden-form-values.svg)](https://pypi.org/project/strip-hidden-form-values/)
[![Changelog](https://img.shields.io/github/v/release/simonw/strip-hidden-form-values?include_prereleases&label=changelog)](https://github.com/simonw/strip-hidden-form-values/releases)
[![Tests](https://github.com/simonw/strip-hidden-form-values/workflows/Test/badge.svg)](https://github.com/simonw/strip-hidden-form-values/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/strip-hidden-form-values/blob/master/LICENSE)

CLI tool for stripping hidden form values from an HTML document

Why would you need this? Imagine you're running a [Git scraper](https://simonwillison.net/2020/Oct/9/git-scraping/) against a website that includes hidden form fields (such as those produced by `__VIEWSTATE` fields) that change on every request. You can pipe the HTML through this tool to strip those hidden form values such that a change is only recorded if the rest of the page is modified in some way.

[scrape-ca-wildlife-rules](https://github.com/simonw/scrape-ca-wildlife-rules) is an example of a repository that uses this tool for that, see the [scrape.yml](https://github.com/simonw/scrape-ca-wildlife-rules/blob/main/.github/workflows/scrape.yml) workflow there for details.

## Installation

Install this tool using `pip`:

    $ pip install strip-hidden-form-values

## Usage

You can pipe HTML into this tool:

    curl http://... | strip-hidden-form-values > output.html

Or pass it a filename:

    strip-hidden-form-values input.html > output.html

The tool will replace the `value=` attribute of any hidden form fields with a blank string,
so the following:

    <input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="p8nVm4PgVPA" />

Will be replaced with:

    <input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="" />

All other HTML will remain unchanged.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd strip-hidden-form-values
    python -m venv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
