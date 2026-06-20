# dogsheep-photos

[![PyPI](https://img.shields.io/pypi/v/dogsheep-photos.svg)](https://pypi.org/project/dogsheep-photos/)
[![Changelog](https://img.shields.io/github/v/release/dogsheep/dogsheep-photos?include_prereleases&label=changelog)](https://github.com/dogsheep/dogsheep-photos/releases)
[![CircleCI](https://circleci.com/gh/dogsheep/dogsheep-photos.svg?style=svg)](https://circleci.com/gh/dogsheep/dogsheep-photos)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dogsheep/dogsheep-photos/blob/master/LICENSE)

Save details of your photos to a SQLite database and upload them to S3.

See [Using SQL to find my best photo of a pelican according to Apple Photos](https://simonwillison.net/2020/May/21/apple-photos-sqlite/) for background information on this project.

## What these tools do

These tools are a work-in-progress mechanism for taking full ownership of your photos. The core idea is to help implement the following:

* Every photo you have taken lives in a single, private Amazon S3 bucket
* You have a single SQLite database file which stores metadata about those photos - potentially pulled from multiple different places. This may include EXIF data, Apple Photos, the results of running machine learning APIs against photos and much more besides.
* You can then use [Datasette](https://github.com/simonw/datasette) to explore your own photos.

I'm a heavy user of Apple Photos so the initial releases of this tool will have a bias towards that, but ideally I would like a subset of these tools to be useful to people no matter which core photo solution they are using.

## Installation

    $ pip install dogsheep-photos

## Authentication (if using S3)

If you want to use S3 to store your photos, you will need to first create S3 credentials for a new, dedicated bucket.

You may find the [s3-credentials tool](https://github.com/simonw/s3-credentials) useful for this.

Run this command and paste in your credentials. You will need three values: the name of your S3 bucket, your Access key ID and your Secret access key.

    $ dogsheep-photos s3-auth

This will create a file called `auth.json` in your current directory containing the required values. To save the file at a different path or filename, use the `--auth=myauth.json` option.

## Uploading photos

Run this command to upload every photo in a specific directory to your S3 bucket:

    $ dogsheep-photos upload photos.db \
        ~/Pictures/Photos\ Library.photoslibrary/original

The command will only upload photos that have not yet been uploaded, based on their sha256 hash.

`photos.db` will be created with an `uploads` table containing details of which files were uploaded.

To see what the command would do without uploading any files, use the `--dry-run` option.

The sha256 hash of the photo contents will be used as the name of the file in the bucket, with an extension matching the type of file. This is an implementation of the [Content addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage) pattern.

## Importing Apple Photos metadata

The `apple-photos` command imports metadata from your Apple Photos library.

    $ photo-to-sqlite apple-photos photos.db

Imported metadata includes places, people, albums, quality scores and machine learning labels for the photo contents.

## Creating a subset database

You can create a new, subset database of photos using the `create-subset` command.

This is useful for creating a shareable SQLite database that only contains metadata for a selected set of photos.

Since photo metadata contains latitude and longitude you may not want to share a database that includes photos taken at your home address.

`create-subset` takes three arguments: an existing database file created using the `apple-photos` command, the name of the new, shareable database file you would like to create and a SQL query that returns the `sha256` hash values of the photos you would like to include in that database.

For example, here's how to create a shareable database of just the photos that have been added to albums containing the word "Public":

    $ dogsheep-photos create-subset \
        photos.db \
        public.db \
        "select sha256 from apple_photos where albums like '%Public%'"

## Serving photos locally with datasette-media

If you don't want to upload your photos to S3 but you still want to browse them using Datasette you can do so using the [datasette-media](https://github.com/simonw/datasette-media) plugin. This plugin adds the ability to serve images and other static files directly from disk, configured using a SQL query.

To use it, first install Datasette and the plugin:

    $ pip install datasette datasette-media

If any of your photos are `.HEIC` images taken by an iPhone you should also install the optional `pyheif` dependency:

    $ pip install pyheif

Now create a `metadata.yaml` file configuring the plugin:

```yaml
plugins:
  datasette-media:
    thumbnail:
      sql: |-
        select path as filepath, 200 as resize_height from apple_photos where uuid = :key
    large:
      sql: |-
        select path as filepath, 1024 as resize_height from apple_photos where uuid = :key
```
This will configure two URL endpoints - one for 200 pixel high thumbnails and one for 1024 pixel high larger images.

Create your `photos.db` database using the `apple-photos` command, then run Datasette like this:

    $ datasette -m metadata.yaml

Your photos will be served on URLs that look like this:

    http://127.0.0.1:8001/-/media/thumbnail/F4469918-13F3-43D8-9EC1-734C0E6B60AD
    http://127.0.0.1:8001/-/media/large/F4469918-13F3-43D8-9EC1-734C0E6B60AD

You can find the UUIDs for use in these URLs by running `select uuid from photos_with_apple_metadata`.

### Displaying images using datasette-json-html

If you are using `datasette-media` to serve photos you can include images directly in Datasette query results using the [datasette-json-html](https://github.com/simonw/datasette-json-html) plugin.

Run `pip install datasette-json-html` to install the plugin, then use queries like this to view your images:

```sql
select
    json_object(
        'img_src',
        '/-/media/thumbnail/' || uuid
    ) as photo,
    uuid,
    date
from
    apple_photos
order by
    date desc
limit 10;
```
The `photo` column returned by this query should render as image tags that display the correct images.

### Displaying images using custom template pages

Datasette's [custom pages](https://datasette.readthedocs.io/en/stable/custom_templates.html#custom-pages) feature lets you create custom pages for a Datasette instance by dropping HTML templates into a `templates/pages` directory and then running Datasette using `datasette --template-dir=templates/`.

You can combine that ability with the [datasette-template-sql](https://github.com/simonw/datasette-template-sql) plugin to create custom template pages that directly display photos served by `datasette-media`.

Install the plugin using `pip install datasette-template-sql`.

Create a `templates/pages` folder and add the following files:

`recent-photos.html`
```html+jinja
<h1>Recent photos</h1>

<div>
{% for photo in sql("select * from apple_photos order by date desc limit 20") %}
    <img src="/-/media/photo/{{ photo['uuid'] }}">
{% endfor %}
</div>
```
`random-photos.html`
```html+jinja
<h1>Random photos</h1>

<div>
{% for photo in sql("with foo as (select * from apple_photos order by date desc limit 5000) select * from foo order by random() limit 20") %}
    <img src="/-/media/photo/{{ photo['uuid'] }}">
{% endfor %}
</div>
```
Now run Datasette like this:

    $ datasette photos.db -m metadata.yaml --template-dir=templates/

Visiting `http://localhost:8001/recent-photos` will display 20 recent photos. Visiting `http://localhost:8001/random-photos` will display 20 photos randomly selected from your 5,000 most recent.

