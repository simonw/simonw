# pge-outages

This repository tracks outages reported on the [PG&E outages map](https://pgealerts.alerts.pge.com/outage-tools/outage-map/) over time, using [Git scraping](https://simonwillison.net/2020/Oct/9/git-scraping/).

This repository started tracking outages on 4th February 2024. The implementation of the scraper can be found in [.github/workflows/fetch.yml](https://github.com/simonw/pge-outages/blob/main/.github/workflows/fetch.yml) - it uses a combination of `curl` and `jq`.

The most recently tracked outages are in [outages.json](https://github.com/simonw/pge-outages/blob/main/outages.json). The [commit history](https://github.com/simonw/pge-outages/commits/main/outages.json) of that file shows outages recorded over time.

A previous version of this repository ran from from 2019 to 2022. That data can now be found in [simonw/pge-outages-pre-2024](https://github.com/simonw/pge-outages-pre-2024/)

## Incomplete data warning

This repository only archives outages that are reported for a single location.

The outage map also includes polygon data, which is much more interesting... but has not proven practical to archive here, for [reasons explained in this issue comment](https://github.com/simonw/pge-outages/issues/4#issuecomment-1928758853). Short version: I'd have to constantly archive 100MB of data per snapshot because the polygons are so large!

## Browsing the latest data in Datasette Lite

Use this URL to open the latest `outages.json` in [Datasette Lite](https://github.com/simonw/datasette-lite):

https://lite.datasette.io/?json=https://github.com/simonw/pge-outages/blob/main/outages.json#/data/outages?_facet=CITY&_facet=OUTAGE_CAUSE&_facet=CREW_CURRENT_STATUS&_facet=OUTAGE_EXTENT

It will look something like this:

![Screenshot of Datasette Lite, faceting 674 outages by city, cause, crew current status and outage extent](https://github.com/simonw/pge-outages/assets/9599/ac0999f2-349a-4db7-a005-2ba42133dde0)
