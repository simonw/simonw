# datasette-render-timestamps

[![PyPI](https://img.shields.io/pypi/v/datasette-render-timestamps.svg)](https://pypi.org/project/datasette-render-timestamps/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-render-timestamps.svg?style=svg)](https://circleci.com/gh/simonw/datasette-render-timestamps)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-render-timestamps/blob/master/LICENSE)

Datasette plugin for rendering timestamps.

## Installation

Install this plugin in the same environment as Datasette to enable this new functionality:

    pip install datasette-render-timestamps

The plugin will then look out for integer numbers that are likely to be timestamps - anything that would be a number of seconds from 5 years ago to 5 years in the future.

These will then be rendered in a more readable format.

## Configuration

You can disable automatic column detection in favour of explicitly listing the columns that you would like to render using [plugin configuration](https://datasette.readthedocs.io/en/stable/plugins.html#plugin-configuration) in a `metadata.json` file.

Add a `"datasette-render-timestamps"` configuration block and use a `"columns"` key to list the columns you would like to treat as timestamp values:

```json
{
    "plugins": {
        "datasette-render-timestamps": {
            "columns": ["created", "updated"]
        }
    }
}
```
This will cause any `created` or `updated` columns in any table to be treated as timestamps and rendered.

Save this to `metadata.json` and run datasette with the `--metadata` flag to load this configuration:

    datasette serve mydata.db --metadata metadata.json

To disable automatic timestamp detection entirely, you can use `"columnns": []`.

This configuration block can be used at the top level, or it can be applied just to specific databases or tables. Here's how to apply it to just the `entries` table in the `news.db` database:

```json
{
    "databases": {
        "news": {
            "tables": {
                "entries": {
                    "plugins": {
                        "datasette-render-timestamps": {
                            "columns": ["created", "updated"]
                        }
                    }
                }
            }
        }
    }
}
```

And here's how to apply it to every `created` column in every table in the `news.db` database:

```json
{
    "databases": {
        "news": {
            "plugins": {
                "datasette-render-timestamps": {
                    "columns": ["created", "updated"]
                }
            }
        }
    }
}
```

### Customizing the date format

The default format is `%B %d, %Y - %H:%M:%S UTC` which renders for example: `October 10, 2019 - 07:18:29 UTC`. If you want another format, the date format can be customized using plugin configuration. Any format string supported by [strftime](http://strftime.org/) may be used. For example:

```json
{
    "plugins": {
        "datasette-render-timestamps": {
            "format": "%Y-%m-%d-%H:%M:%S"
        }
    }
}
```
