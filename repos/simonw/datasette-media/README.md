# datasette-media

[![PyPI](https://img.shields.io/pypi/v/datasette-media.svg)](https://pypi.org/project/datasette-media/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-media?include_prereleases&label=changelog)](https://github.com/simonw/datasette-media/releases)
[![Tests](https://github.com/simonw/datasette-media/workflows/Test/badge.svg)](https://github.com/simonw/datasette-media/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-media/blob/main/LICENSE)

Datasette plugin for serving media based on a SQL query.

Use this when you have a database table containing references to files on disk - or binary content stored in BLOB columns - that you would like to be able to serve to your users.

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-media

### HEIC image support

Modern iPhones save their photos using the [HEIC image format](https://en.wikipedia.org/wiki/High_Efficiency_Image_File_Format). Processing these images requires an additional dependency, [pyheif](https://pypi.org/project/pyheif/). You can include this dependency by running:

    $ pip install datasette-media[heif]

## Usage

You can use this plugin to configure Datasette to serve static media based on SQL queries to an underlying database table.

Media will be served from URLs that start with `/-/media/`. The full URL to each media asset will look like this:

    /-/media/type-of-media/media-key

`type-of-media` will correspond to a configured SQL query, and might be something like `photo`. `media-key` will be an identifier that is used as part of the underlying SQL query to find which file should be served.

### Serving static files from disk

The following ``metadata.json`` configuration will cause this plugin to serve files from disk, based on queries to a database table called `apple_photos`.

```json
{
    "plugins": {
        "datasette-media": {
            "photo": {
                "sql": "select filepath from apple_photos where uuid=:key"
            }
        }
    }
}
```

A request to `/-/media/photo/CF972D33-5324-44F2-8DAE-22CB3182CD31` will execute the following SQL query:

```sql
select filepath from apple_photos where uuid=:key
```

The value from the URL -  in this case `CF972D33-5324-44F2-8DAE-22CB3182CD31` - will be passed as the `:key` parameter to the query.

The query returns a `filepath` value that has been read from the table. The plugin will then read that file from disk and serve it in response to the request.

SQL queries default to running against the first connected database. You can specify a different database to execute the query against using `"database": "name_of_db"`. To execute against `photos.db`, use this:

```json
{
    "plugins": {
        "datasette-media": {
            "photo": {
                "sql": "select filepath from apple_photos where uuid=:key",
                "database": "photos"
            }
        }
    }
}
```

See [dogsheep-photos](https://github.com/dogsheep/dogsheep-photos) for an example of an application that can benefit from this plugin.

### Serving binary content from BLOB columns

If your SQL query returns a `content` column, this will be served directly to the user:

```json
{
    "plugins": {
        "datasette-media": {
            "photo": {
                "sql": "select thumbnail as content from photos where uuid=:key",
                "database": "thumbs"
            }
        }
    }
}
```

You can also return a `content_type` column which will be used as the `Content-Type` header served to the user:

```json
{
    "plugins": {
        "datasette-media": {
            "photo": {
                "sql": "select body as content, 'text/html;charset=utf-8' as content_type from documents where id=:key",
                "database": "documents"
            }
        }
    }
}
```

If you do not specify a `content_type` the default of `application/octet-stream` will be used.

### Serving content proxied from a URL

To serve content that is itself fetched from elsewhere, return a `content_url` column. This can be particularly useful when combined with the ability to resize images (described in the next section).

```json
{
    "plugins": {
        "datasette-media": {
            "photos": {
                "sql": "select photo_url as content_url from photos where id=:key",
                "database": "photos",
                "enable_transform": true
            }
        }
    }
}
```

Now you can access resized versions of images from that URL like so:

    /-/media/photos/13?w=200

### Setting a download file name

The `content_filename` column can be returned to force browsers to download the content using a specific file name.

```json
{
    "plugins": {
        "datasette-media": {
            "hello": {
                "sql": "select 'Hello ' || :key as content, 'hello.txt' as content_filename"
            }
        }
    }
}
```

Visiting `/-/media/hello/Groot` will cause your browser to download a file called `hello.txt` containing the text `Hello Groot`.

### Resizing or transforming images

Your SQL query can specify that an image should be resized and/or converted to another format by returning additional columns. All three are optional.

* `resize_width` - the width to resize the image to
* `resize_width` - the height to resize the image to
* `output_format` - the output format to use (e.g. `jpeg` or `png`) - any output format [supported by Pillow](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) is allowed here.

If you specify one but not the other of `resize_width` or `resize_height` the unspecified one will be calculated automatically to maintain the aspect ratio of the image.

Here's an example configuration that will resize all images to be JPEGs that are 200 pixels in height:

```json
{
    "plugins": {
        "datasette-media": {
            "photo": {
                "sql": "select filepath, 200 as resize_height, 'jpeg' as output_format from apple_photos where uuid=:key",
                "database": "photos"
            }
        }
    }
}
```

If you enable the `enable_transform` configuration option you can instead specify transform parameters at runtime using querystring parameters. For example:

- `/-/media/photo/CF972D33?w=200` to resize to a fixed width
- `/-/media/photo/CF972D33?h=200` to resize to a fixed height
- `/-/media/photo/CF972D33?format=jpeg` to convert to JPEG

That option is added like so:

```json
{
    "plugins": {
        "datasette-media": {
            "photo": {
                "sql": "select filepath from apple_photos where uuid=:key",
                "database": "photos",
                "enable_transform": true
            }
        }
    }
}
```

The maximum allowed height or width is 4000 pixels. You can change this limit using the `"max_width_height"` option:

```json
{
    "plugins": {
        "datasette-media": {
            "photo": {
                "sql": "select filepath from apple_photos where uuid=:key",
                "database": "photos",
                "enable_transform": true,
                "max_width_height": 1000
            }
        }
    }
}
```

## Configuration

In addition to the different named content types, the following special plugin configuration setting is available:

- `transform_threads` - number of threads to use for running transformations (e.g. resizing). Defaults to 4.

This can be used like this:

```json
{
    "plugins": {
        "datasette-media": {
            "photo": {
                "sql": "select filepath from apple_photos where uuid=:key",
                "database": "photos"
            },
            "transform_threads": 8
        }
    }
}
```
