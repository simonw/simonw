# scrape-open-data

[![Scrape latest data](https://github.com/simonw/scrape-open-data/actions/workflows/scrape.yml/badge.svg)](https://github.com/simonw/scrape-open-data/actions/workflows/scrape.yml)

Scrapes every available dataset from Socrata and stores them as newline-delimited JSON in this repository, to track changes over time through [Git scraping](https://simonwillison.net/2020/Oct/9/git-scraping/).

- `socrata/data.delaware.gov.jsonl` contains the latest datasets for a specific domain. This is updated twice a day.
- `socrata/data.delaware.gov.stats.jsonl` contains information on page views and download numbers. This is updated once a week to avoid every single fetch including updated counts for many different datasets.

The resulting database is deployed to https://open-data.datasette.io/

## scrape_socrata.py

Run `python scrape_socrata.py socrata/` to scrape the data from Socrata and save it in the `socrata/` directory.

Add `--stats` to include page view and download statistics in separate files.

Add `--verbose` for verbose output.

## build_socrata_db.py`

Run this command to build a SQLite database from the `.jsonl` files in `socrata/`:

    python build_socrata_db.py socrata.db socrata
