# tableau-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/tableau-to-sqlite.svg)](https://pypi.org/project/tableau-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/tableau-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/tableau-to-sqlite/releases)
[![Tests](https://github.com/simonw/tableau-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/tableau-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/tableau-to-sqlite/blob/master/LICENSE)

Fetch data from Tableau into a SQLite database. A wrapper around [TableauScraper](https://github.com/bertrandmartel/tableau-scraping/).

## Installation

Install this tool using `pip`:

    $ pip install tableau-to-sqlite

## Usage

If you have the URL to a Tableau dashboard like this:

https://results.mo.gov/t/COVID19/views/VaccinationsDashboard/Vaccinations

You can pass that directly to the tool:

    tableau-to-sqlite tableau.db \
      https://results.mo.gov/t/COVID19/views/VaccinationsDashboard/Vaccinations

This will create a SQLite database called `tableau.db` containing one table for each of the worksheets in that dashboard.

If the dashboard is hosted on https://public.tableau.com/ you can instead provide the view name. This will be two strings separated by a `/` symbol - something like this:

    OregonCOVID-19VaccineProviderEnrollment/COVID-19VaccineProviderEnrollment

Now run the tool like this:

    tableau-to-sqlite tableau.db \
        OregonCOVID-19VaccineProviderEnrollment/COVID-19VaccineProviderEnrollment

## Get the data as JSON or CSV

If you're building a [git scraper](https://simonwillison.net/2020/Oct/9/git-scraping/) you may want to convert the data gathered by this tool to CSV or JSON to check into your repository.

You can do that using [sqlite-utils](https://sqlite-utils.datasette.io/). Install it using `pip`:

    pip install sqlite-utils

You can dump out a table as JSON like so:

    sqlite-utils rows tableau.db \
       'Admin Site and County Map Site No Info' > tableau.json

Or as CSV like this:

    sqlite-utils rows tableau.db --csv \
       'Admin Site and County Map Site No Info' > tableau.csv

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd tableau-to-sqlite
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
