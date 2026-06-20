# hacker-news-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/hacker-news-to-sqlite.svg)](https://pypi.org/project/hacker-news-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/dogsheep/hacker-news-to-sqlite?include_prereleases&label=changelog)](https://github.com/dogsheep/hacker-news-to-sqlite/releases)
[![Tests](https://github.com/dogsheep/hacker-news-to-sqlite/workflows/Test/badge.svg)](https://github.com/dogsheep/hacker-news-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/hacker-news-to-sqlite/blob/main/LICENSE)

Create a SQLite database containing data fetched from [Hacker News](https://news.ycombinator.com/).

## How to install

    $ pip install hacker-news-to-sqlite

## Usage

    $ hacker-news-to-sqlite user hacker-news.db your-username
    Importing items:  37%|███████████                        | 845/2297 [05:09<11:02,  2.19it/s]

Imports all of your Hacker News submissions and comments into a SQLite database called `hacker-news.db`.

    $ hacker-news-to-sqlite trees hacker-news.db 22640038 22643218

Fetches the entire comments tree in which any of those content IDs appears.

## Browsing your data with Datasette

You can use [Datasette](https://datasette.readthedocs.org/) to browse your data. Install Datasette like this:

    $ pip install datasette

Now run it against your `hacker-news.db` file like so:

    $ datasette hacker-news.db

Visit `https://localhost:8001/` to search and explore your data.

You can improve the display of your data usinng the [datasette-render-timestamps](https://github.com/simonw/datasette-render-timestamps) and [datasette-render-html](https://github.com/simonw/datasette-render-html) plugins. Install them like this:

    $ pip install datasette-render-timestamps datasette-render-html

Now save the following configuration in a file called `metadata.json`:

```json
{
    "databases": {
        "hacker-news": {
            "tables": {
                "items": {
                    "plugins": {
                        "datasette-render-html": {
                            "columns": [
                                "text"
                            ]
                        },
                        "datasette-render-timestamps": {
                            "columns": [
                                "time"
                            ]
                        }
                    }
                },
                "users": {
                    "plugins": {
                        "datasette-render-timestamps": {
                            "columns": [
                                "created"
                            ]
                        }
                    }
                }
            }
        }
    }
}
```
Run Datasette like this:

    $ datasette -m metadata.json hacker-news.db

The timestamp columns will now be rendered as human-readable dates, and any HTML in your posts will be displayed as rendered HTML.
