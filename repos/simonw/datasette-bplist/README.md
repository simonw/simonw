# datasette-bplist

[![PyPI](https://img.shields.io/pypi/v/datasette-bplist.svg)](https://pypi.org/project/datasette-bplist/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-bplist.svg?style=svg)](https://circleci.com/gh/simonw/datasette-bplist)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-bplist/blob/master/LICENSE)

Datasette plugin for working with Apple's [binary plist](https://en.wikipedia.org/wiki/Property_list) format.

This plugin adds two features: a display hook and a SQL function.

The display hook will detect any database values that are encoded using the binary plist format. It will decode them, convert them into JSON and display them pretty-printed in the Datasette UI.

The SQL function `bplist_to_json(value)` can be used inside a SQL query to convert a binary plist value into a JSON string. This can then be used with SQLite's `json_extract()` function or with the [datasette-jq](https://github.com/simonw/datasette-jq) plugin to further analyze that data as part of a SQL query.

Install this plugin in the same environment as Datasette to enable this new functionality:

    pip install datasette-bplist

## Trying it out

If you use a Mac you already have plenty of SQLite databases that contain binary plist data.

One example is the database that powers the Apple Photos app.

This database tends to be locked, so you will need to create a copy of the database in order to run queries against it:

    cp ~/Pictures/Photos\ Library.photoslibrary/database/photos.db /tmp/photos.db

The database also makes use of custom SQLite extensions which prevent it from opening in Datasette.

You can work around this by exporting the data that you want to experiment with into a new SQLite file.

I recommend trying this plugin against the `RKMaster_dataNote` table, which contains plist-encoded EXIF metadata about the photos you have taken.

You can export that table into a fresh database like so:

    sqlite3 /tmp/photos.db ".dump RKMaster_dataNote" | sqlite3 /tmp/exif.db

Now run `datasette /tmp/exif.db` and you can start trying out the plugin.

## Using the bplist_to_json() SQL function

Once you have the `exif.db` demo working, you can try the `bplist_to_json()` SQL function.

Here's a query that shows the camera lenses you have used the most often to take photos:

    select
        json_extract(
            bplist_to_json(value),
            "$.{Exif}.LensModel"
        ) as lens,
        count(*) as n
    from RKMaster_dataNote
    group by lens
    order by n desc;

If you have a large number of photos this query can take a long time to execute, so you may need to increase the SQL time limit enforced by Datasette like so:

    $ datasette /tmp/exif.db \
        --config sql_time_limit_ms:10000

Here's another query, showing the time at which you took every photo in your library which is classified as as screenshot:

    select
        attachedToId,
        json_extract(
            bplist_to_json(value),
            "$.{Exif}.DateTimeOriginal"
        )
    from RKMaster_dataNote
    where
        json_extract(
            bplist_to_json(value),
            "$.{Exif}.UserComment"
        ) = "Screenshot"

And if you install the [datasette-cluster-map](https://github.com/simonw/datasette-cluster-map) plugin, this query will show you a map of your most recent 1000 photos:

    select
        *, 
        json_extract(
            bplist_to_json(value),
            "$.{GPS}.Latitude"
        ) as latitude,
        -json_extract(
            bplist_to_json(value),
            "$.{GPS}.Longitude"
        ) as longitude,
        json_extract(
            bplist_to_json(value),
            "$.{Exif}.DateTimeOriginal"
        ) as datetime
    from
        RKMaster_dataNote
    where
        latitude is not null
    order by
        attachedToId desc
