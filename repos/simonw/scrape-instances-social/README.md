# scrape-instances-social

> **Repo archived** on 4th January 2025 - this project is no longer active.

For full details about how this works, see [Tracking Mastodon user numbers over time with a bucket of tricks](https://simonwillison.net/2022/Nov/20/tracking-mastodon/) on my blog.

https://instances.social/instances.json is a list of Mastodon instances, including their number of statuses and users.

This repo scrapes that and records the history of the file, a form of [Git scraping](https://simonwillison.net/2020/Oct/9/git-scraping/).

Visit this Observable notebook to see users-over-time figures plotted on charts:

https://observablehq.com/@simonw/mastodon-users-and-statuses-over-time

You can browse the most recent copy of the scraped data using Datasette Lite here: https://lite.datasette.io/?json=https%3A%2F%2Fraw.githubusercontent.com%2Fsimonw%2Fscrape-instances-social%2Fmain%2Finstances.json#/data/instances?_sort=users&_sort_by_desc=on

## Building a database

You can use the [git-history](https://datasette.io/tools/git-history) tool to build a SQLite database of the history of the instances:

    pip install -r requirements.txt
    # (or just pip install git-history)
    ./build-instance-history.sh

You can run that script multiple times and it will only update the database with new commits that have not been seen before.

You can also build a much smaller SQLite database of just the counts of users and statuses over time:

    ./build-count-history.sh

## Accessing the database

A script in this repository builds and publishes the `counts.db` database to S3. You can download the latest copy here - it's pretty small as it only records the total sum of users and statuses over time across all tracked instances.

https://scrape-instances-social.s3.amazonaws.com/counts.db

You can open this in [Datasette Lite](https://lite.datasette.io/) like so:

https://lite.datasette.io/?url=https://scrape-instances-social.s3.amazonaws.com/counts.db
