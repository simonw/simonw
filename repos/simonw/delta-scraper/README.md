# delta-scraper

IN EARLY DEVELOPMENT

[![PyPI](https://img.shields.io/pypi/v/delta-scraper.svg)](https://pypi.org/project/delta-scraper/)
[![CircleCI](https://circleci.com/gh/simonw/delta-scraper.svg?style=svg)](https://circleci.com/gh/simonw/delta-scraper)
[![Documentation Status](https://readthedocs.org/projects/delta-scraper/badge/?version=latest)](http://delta-scraper.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/delta-scraper/blob/master/LICENSE)

Python library for scraping data sources and creating readable deltas.

For background, see [Scraping hurricane Irma](https://simonwillison.net/2017/Sep/10/scraping-irma/).

## Concepts

This library allows you to define _scrapers_, which are objects that know how to retrieve information from a source (usually a web API, but scrapers can be written to operate against HTML or other formats) and persist that data somewhere as JSON.

When a scraper fetches fresh information it has the ability to compare that data to the old data and use the difference to create a human-readable message.

These capabilities can be combined with a git repository to create a commit log, with human-readable commit messages that accompany a machine-readable diff againts the generated JSON.

See [disaster-scrapers](https://github.com/simonw/disaster-scrapers) and [disaster-data](https://github.com/simonw/disaster-scrapers) for some examples of this pattern in action.

## Basic usage

You can define new scrapers by subclassing `DeltaScraper`. Here's an example which scrapes a list of FEMA shelters.

    class FemaShelters(DeltaScraper):
        url = "https://gis.fema.gov/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=FEMA:FEMANSSOpenShelters&maxFeatures=250&outputFormat=json"
        owner = "simonw"
        repo = "disaster-data"
        filepath = "fema/shelters.json"

        record_key = "SHELTER_ID"
        noun = "shelter"

        def fetch_data(self):
            data = requests.get(self.url, timeout=10).json()
            return [feature["properties"] for feature in data["features"]]

        def display_record(self, record):
            display = []
            display.append(
                "  {SHELTER_NAME} in {CITY}, {STATE} ({SHELTER_STATUS})".format(**record)
            )
            display.append(
                "    https://www.google.com/maps/search/{LATITUDE},{LONGITUDE}".format(
                    **record
                )
            )
            display.append("    population = {TOTAL_POPULATION}".format(**record))
            display.append("")
            return "\n".join(display)
