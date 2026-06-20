# google-takeout-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/google-takeout-to-sqlite.svg)](https://pypi.org/project/google-takeout-to-sqlite/)
[![CircleCI](https://circleci.com/gh/dogsheep/google-takeout-to-sqlite.svg?style=svg)](https://circleci.com/gh/dogsheep/google-takeout-to-sqlite)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dogsheep/google-takeout-to-sqlite/blob/master/LICENSE)

Save data from google-takeout to a SQLite database.

## How to install

    $ pip install google-takeout-to-sqlite

Request your Google data from https://takeout.google.com/ - wait for the email and download the zip file.

This tool only supports a subset of the available options. More will be added over time.

## My Activity

You can request the "My Activity" export and then import it with the following command:

    $ google-takeout-to-sqlite my-activity takeout.db ~/Downloads/takeout-20190530.zip

This will create a database file called `takeout.db` if one does not already exist.

## Location History

Your location history records latitude, longitude and timestame for where Google has tracked your location. You can import it using this command:

    $ google-takeout-to-sqlite location-history takeout.db ~/Downloads/takeout-20190530.zip

## Browsing your data with Datasette

Once you have imported Google data into a SQLite database file you can browse your data using [Datasette](https://github.com/simonw/datasette). Install Datasette like so:

    $ pip install datasette

Now browse your data by running this and then visiting `http://localhost:8001/`

    $ datasette takeout.db

Install the [datasette-cluster-map](https://github.com/simonw/datasette-cluster-map) plugin to see your location history on a map:

    $ pip install datasette-cluster-map
