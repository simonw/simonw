# Datasette Lite

Datasette running in your browser using WebAssembly and [Pyodide](https://pyodide.org)

Live tool: https://lite.datasette.io/

More about this project:

- [Datasette Lite: a server-side Python web application running in a browser](https://simonwillison.net/2022/May/4/datasette-lite/)
- [Joining CSV files in your browser using Datasette Lite](https://simonwillison.net/2022/Jun/20/datasette-lite-csvs/)
- [Plugin support for Datasette Lite](https://simonwillison.net/2022/Aug/17/datasette-lite-plugins/)

## How this works

Datasette Lite runs the full server-side Datasette Python web application directly in your browser, using the [Pyodide](https://pyodide.org) build of Python compiled to WebAssembly.

When you launch the demo, your browser will download and start executing a full Python interpreter, install the [datasette](https://pypi.org/project/datasette/) package (and its dependencies), download one or more SQLite database files and start the application running in a browser window (actually a [Web Worker](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) attached to that window).

## Load a different Datasette version

Datasette Lite uses the most recent stable Datasette release [from PyPI](https://pypi.org/project/datasette/).

To use the most recent preview version (alpha or beta) add `?ref=pre`:

- https://lite.datasette.io/?ref=pre

Or for a specific release pass the version number as `?ref=`:

- https://lite.datasette.io/?ref=0.64.2
- https://lite.datasette.io/?ref=1.0a11

## Loading CSV data

You can load data from a CSV file hosted online (provided it allows `access-control-allow-origin: *`) by passing that URL as a `?csv=` parameter - or by clicking the "Load CSV by URL" button and pasting in a URL.

This example loads a CSV of college fight songs from the [fivethirtyeight/data](https://github.com/fivethirtyeight/data/blob/master/fight-songs/README.md) GitHub repository:

- https://lite.datasette.io/?csv=https%3A%2F%2Fraw.githubusercontent.com%2Ffivethirtyeight%2Fdata%2Fmaster%2Ffight-songs%2Ffight-songs.csv

You can pass `?csv=` multiple times to load more than one CSV file. You can then execute SQL joins to combine that data.

This example loads [the latest Covid-19 per-county data](https://github.com/nytimes/covid-19-data) from the NY Times, the 2019 county populations data from the US Census, joins them on FIPS code and runs a query that calculates cases per million across that data:

[https://lite.datasette.io/?csv=https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-recent.csv&csv=https://raw.githubusercontent.com/simonw/covid-19-datasette/main/us_census_county_populations_2019.csv#/data?sql=select%0A++%5Bus-counties-recent%5D.*%2C%0A++us_census_county_populations_2019.population%2C%0A++1.0+*+%5Bus-counties-recent%5D.cases+%2F+us_census_county_populations_2019.population+*+1000000+as+cases_per_million%0Afrom%0A++%5Bus-counties-recent%5D%0A++join+us_census_county_populations_2019+on+us_census_county_populations_2019.fips+%3D+%5Bus-counties-recent%5D.fips%0Awhere%0A++population+%3E+10000%0Aorder+by%0A++cases_per_million+desc
](https://lite.datasette.io/?csv=https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-recent.csv&csv=https://raw.githubusercontent.com/simonw/covid-19-datasette/main/us_census_county_populations_2019.csv#/data?sql=select%0A++%5Bus-counties-recent%5D.*%2C%0A++us_census_county_populations_2019.population%2C%0A++1.0+*+%5Bus-counties-recent%5D.cases+%2F+us_census_county_populations_2019.population+*+1000000+as+cases_per_million%0Afrom%0A++%5Bus-counties-recent%5D%0A++join+us_census_county_populations_2019+on+us_census_county_populations_2019.fips+%3D+%5Bus-counties-recent%5D.fips%0Awhere%0A++date+%3D+%28select+max%28date%29+from+%5Bus-counties-recent%5D%29%0Aorder+by%0A++cases_per_million+desc)

## Loading JSON data

If you have data in a JSON file that looks something like this you can load it directly into Datasette Lite using the `?json=URL` parameter:

```json
[
  {
    "id": 1,
    "name": "Item 1"
  },
  {
    "id": 2,
    "name": "Item 2"
  }
]
```
This also works with JSON documents where one of the keys is a list of objects, such as this one:
```json
{
  "rows": [
    {
      "id": 1,
      "name": "Item 1"
    },
    {
      "id": 2,
      "name": "Item 2"
    }
  ]
}
```
In this case it will search for the first key that contains a list of objects.

If a document is a JSON object where every value is a JSON object, like this:

```json
{
  "anchor-positioning": {
    "spec": "https://drafts.csswg.org/css-anchor-position-1/#anchoring"
  },
  "array-at": {
    "spec": "https://tc39.es/ecma262/multipage/indexed-collections.html#sec-array.prototype.at"
  },
  "array-flat": {
    "caniuse": "array-flat",
    "spec": "https://tc39.es/ecma262/multipage/indexed-collections.html#sec-array.prototype.flat"
  }
}
```
Each of those objects will be loaded as a separate row, with a `_key` primary key column containing the object key.

[This example loads scraped data](https://lite.datasette.io/?json=https://github.com/simonw/scrape-san-mateo-fire-dispatch/blob/main/incidents.json#/data/incidents) from [this repo](https://github.com/simonw/scrape-san-mateo-fire-dispatch).

Newline-delimited JSON works too - for example a file that looks like this:

```
{"id": 1, "name": "Item 1"}
{"id": 2, "name": "Item 2"}
```

## Loading SQLite databases

You can use this tool to open any SQLite database file that is hosted online and served with a `access-control-allow-origin: *` CORS header. Files served by GitHub Pages automatically include this header, as do database files that have been published online [using datasette publish](https://docs.datasette.io/en/stable/publish.html).

Copy the URL to the `.db` file and either paste it into the "Load SQLite DB by URL" prompt, or construct a URL like the following:

    https://lite.datasette.io/?url=https://latest.datasette.io/fixtures.db

Some examples to try out:

- [Global Power Plants](https://lite.datasette.io/?url=https://global-power-plants.datasettes.com/global-power-plants.db) - 33,000 power plants around the world
- [United States members of congress](https://lite.datasette.io/?url=https://congress-legislators.datasettes.com/legislators.db) - the example database from the [Learn SQL with Datasette](https://datasette.io/tutorials/learn-sql) tutorial

## Loading Parquet

To load a Parquet file, pass a URL to `?parquet=`.

For example this file:

https://github.com/Teradata/kylo/blob/master/samples/sample-data/parquet/userdata1.parquet

Can be loaded like this:

https://lite.datasette.io/?parquet=https://github.com/Teradata/kylo/blob/master/samples/sample-data/parquet/userdata1.parquet

## Initializing with SQL

You can also initialize the `data.db` database by passing the URL to a SQL file. The easiest way to do this is to create a [GitHub Gist](https://gist.github.com/).

This [example SQL file](https://gist.githubusercontent.com/simonw/ac4e19920b4b360752ac0f3ce85ba238/raw/90d31cf93bf1d97bb496de78559798f849b17e85/demo.sql) creates a table and populates it with three records. It's hosted in [this Gist](https://gist.github.com/simonw/ac4e19920b4b360752ac0f3ce85ba238).

    https://gist.githubusercontent.com/simonw/ac4e19920b4b360752ac0f3ce85ba238/raw/90d31cf93bf1d97bb496de78559798f849b17e85/demo.sql

You can paste this URL into the "Load SQL by URL" prompt, or you can pass it as the `?sql=` parameter [like this](https://lite.datasette.io/?sql=https%3A%2F%2Fgist.githubusercontent.com%2Fsimonw%2Fac4e19920b4b360752ac0f3ce85ba238%2Fraw%2F90d31cf93bf1d97bb496de78559798f849b17e85%2Fdemo.sql).

SQL will be executed before any CSV imports, so you can use initial SQL to create a table and then use `?csv=` to import data into it.

## Starting with just an in-memory database

To skip loading the default databases and just provide `/_memory` - useful for demonstrating plugins - pass `?memory=1`, for example:

https://lite.datasette.io/?memory=1

## Loading metadata

Datasette [supports metadata](https://docs.datasette.io/en/stable/metadata.html), as a `metadata.json` or `metadata.yml` file.

You can load a metadata file in either of these formats by passing a URL to the `?metadata=` query string option.

## Special handling of GitHub URLs

A tricky thing about using Datasette Lite is that the files you load via URL need to be hosted somewhere that serves open CORS headers.

Both regular GitHub and [GitHub Gists](https://gist.github.com/) do this by default. This makes them excellent options to host data files that you want to load into Datasette Lite.

You can paste in the "raw" URL to a file, but Datasette Lite also has a shortcut: if you paste in the URL to a page on GitHub or a Gist it will automatically convert it to the "raw" URL for you.

Try the following to see this in action:

- https://lite.datasette.io/?json=https://gist.github.com/simonw/7eacc70cd8b2868be0a18796cec078b9 ([this Gist](https://gist.github.com/simonw/7eacc70cd8b2868be0a18796cec078b9))
- https://lite.datasette.io/?csv=https://github.com/nytimes/covid-19-data/blob/master/us-counties-recent.csv ([this file](https://github.com/nytimes/covid-19-data/blob/master/us-counties-recent.csv))

## Installing plugins

Datasette has a number of [plugins](https://datasette.io/plugins) that enable new features.

You can install plugins into Datasette Lite by adding one or more `?install=name-of-plugin` parameters to the URL.

Not all plugins are compatible with Datasette Lite at the moment, for example plugins that load their own JavaScript and CSS do not currently work, see [issue #8](https://github.com/simonw/datasette-lite/issues/8).

Here's a list of plugins that have been tested with Datasette Lite, plus demo links to see them in action:

- [datasette-packages](https://datasette.io/plugins/datasette-packages) - Show a list of currently installed Python packages - [demo](https://lite.datasette.io/?install=datasette-packages#/-/packages)
- [datasette-dateutil](https://datasette.io/plugins/datasette-dateutil) - dateutil functions for Datasette - [demo](https://lite.datasette.io/?install=datasette-dateutil#/fixtures?sql=select%0A++dateutil_parse%28%2210+october+2020+3pm%22%29%2C%0A++dateutil_parse_fuzzy%28%22This+is+due+10+september%22%29%2C%0A++dateutil_parse%28%221%2F2%2F2020%22%29%2C%0A++dateutil_parse%28%222020-03-04%22%29%2C%0A++dateutil_parse_dayfirst%28%222020-03-04%22%29%3B)
- [datasette-schema-versions](https://datasette.io/plugins/datasette-schema-versions) - Datasette plugin that shows the schema version of every attached database - [demo](https://lite.datasette.io/?install=datasette-schema-versions#/-/schema-versions)
- [datasette-debug-asgi](https://datasette.io/plugins/datasette-debug-asgi) - Datasette plugin for dumping out the ASGI scope. - [demo](https://lite.datasette.io/?install=datasette-debug-asgi#/-/asgi-scope)
- [datasette-query-links](https://datasette.io/plugins/datasette-query-links) - Turn SELECT queries returned by a query into links to execute them - [demo](https://lite.datasette.io/?install=datasette-query-links#/fixtures?sql=select%0D%0A++'select+*+from+[facetable]'+as+query%0D%0Aunion%0D%0Aselect%0D%0A++'select+sqlite_version()'%0D%0Aunion%0D%0Aselect%0D%0A++'select+this+is+invalid+SQL+so+will+not+be+linked')
- [datasette-json-html](https://datasette.io/plugins/datasette-json-html) - Datasette plugin for rendering HTML based on JSON values - [demo](https://lite.datasette.io/?install=datasette-json-html#/fixtures?sql=select+%27%5B%0A++++%7B%0A++++++++%22href%22%3A+%22https%3A%2F%2Fsimonwillison.net%2F%22%2C%0A++++++++%22label%22%3A+%22Simon+Willison%22%0A++++%7D%2C%0A++++%7B%0A++++++++%22href%22%3A+%22https%3A%2F%2Fgithub.com%2Fsimonw%2Fdatasette%22%2C%0A++++++++%22label%22%3A+%22Datasette%22%0A++++%7D%0A%5D%27+as+output)
- [datasette-haversine](https://datasette.io/plugins/datasette-haversine) - Datasette plugin that adds a custom SQL function for haversine distances - [demo](https://lite.datasette.io/?install=datasette-haversine#/fixtures?sql=select+haversine%280%2C+154%2C+1%2C+131%29)
- [datasette-jellyfish](https://datasette.io/plugins/datasette-jellyfish) - Datasette plugin that adds custom SQL functions for fuzzy string matching, built on top of the Jellyfish Python library - [demo](https://lite.datasette.io/?install=datasette-jellyfish#/fixtures?sql=SELECT%0A++++levenshtein_distance%28%3As1%2C+%3As2%29%2C%0A++++damerau_levenshtein_distance%28%3As1%2C+%3As2%29%2C%0A++++hamming_distance%28%3As1%2C+%3As2%29%2C%0A++++jaro_similarity%28%3As1%2C+%3As2%29%2C%0A++++jaro_winkler_similarity%28%3As1%2C+%3As2%29%2C%0A++++match_rating_comparison%28%3As1%2C+%3As2%29%3B&s1=barrack+obama&s2=barrack+h+obama)
- [datasette-pretty-json](https://datasette.io/plugins/datasette-pretty-json) - Datasette plugin that pretty-prints any column values that are valid JSON objects or arrays. - [demo](https://lite.datasette.io/?install=datasette-pretty-json#/fixtures?sql=select+%27%7B%22this%22%3A+%5B%22is%22%2C+%22nested%22%2C+%22json%22%5D%7D%27)
- [datasette-yaml](https://datasette.io/plugins/datasette-yaml) - Export Datasette records as YAML - [demo](https://lite.datasette.io/?install=datasette-yaml#/fixtures/compound_three_primary_keys.yaml)
- [datasette-copyable](https://datasette.io/plugins/datasette-copyable) - Datasette plugin for outputting tables in formats suitable for copy and paste - [demo](https://lite.datasette.io/?install=datasette-copyable#/fixtures/compound_three_primary_keys.copyable?_table_format=github)
- [datasette-mp3-audio](https://datasette.io/plugins/datasette-mp3-audio) - Turn `.mp3` URLs into an audio player in the Datasette interface - [demo](https://lite.datasette.io/?install=datasette-mp3-audio&csv=https://gist.githubusercontent.com/simonw/0a30d52feeb3ff60f7d8636b0bde296b/raw/c078a9e5a0151331e2e46c04c1ebe7edc9f45e8c/scotrail-announcements.csv#/data/scotrail-announcements)
- [datasette-multiline-links](https://datasette.io/plugins/datasette-multiline-links) - Make multiple newline separated URLs clickable in Datasette - [demo](https://lite.datasette.io/?install=datasette-multiline-links&csv=https://docs.google.com/spreadsheets/d/1wZhPLMCHKJvwOkP4juclhjFgqIY8fQFMemwKL2c64vk/export?format=csv#/data?sql=select+edition%2C+headline%2C+text%2C+links%2C+hattips+from+export+where%0Atext+like+'%25'+||+%3Aq+||+'%25'+or+headline+like+'%25'+||+%3Aq+||+'%25'+order+by+edition+desc&q=loans)
- [datasette-copyable](https://datasette.io/plugins/datasette-copyable) - adds an interface for copying out data in CSV, TSV, LaTeX, GitHub Markdown tables and many other formats - [demo](https://lite.datasette.io/?install=datasette-copyable#/content/pypi_releases.copyable?_labels=on&_table_format=github)
- [datasette-statistics](https://datasette.io/plugins/datasette-statistics) - SQL functions for statistical calculations - [demo](https://lite.datasette.io/?install=datasette-statistics#/fixtures?sql=with+numbers+as+%28%0A++++select+1+as+number%0A++++union+all%0A++++select+2%0A++++union+all%0A++++select+3%0A++++union+all%0A++++select+4%0A++++union+all%0A++++select+5%0A%29%0Aselect%0A++statistics_mean%28number%29+as+mean%2C%0A++statistics_median%28number%29+as+median%2C%0A++statistics_stdev%28number%29+as+stdev%0Afrom+numbers%3B)
- [datasette-simple-html](https://datasette.io/plugins/datasette-simple-html) - simple SQL functions for stripping tags and escaping or unescaping HTML strings - [demo](https://lite.datasette.io/?install=datasette-simple-html#/fixtures?sql=select%0A++html_strip_tags%28%27%3Ch1%3EThis+will+have+%3Cem%3Etags+stripped%3C%2Fem%3E%3C%2Fh1%3E%27%29+as+stripped%2C%0A++html_escape%28%27%3Ch1%3EThis+will+have+%3Cem%3Etags+escaped%3C%2Fem%3E%3C%2Fh1%3E%27%29+as+escaped%2C%0A++html_unescape%28%27%26lt%3Bh1%26gt%3BThis+will+have+%26lt%3Bem%26gt%3Btags+unescaped%26lt%3B%2Fem%26gt%3B%26lt%3B%2Fh1%26gt%3B%27%29+as+unescaped)

## Analytics

By default, hits to `https://lite.datasette.io/` are logged using [Plausible](https://plausible.io/).

Plausible is a [privacy-focused](https://plausible.io/privacy-focused-web-analytics), cookie-free, GDPR-compliant analytics system.

Each navigation within Datasette Lite is logged as a separate event to Plausible, capturing the fragment hash and the URL to the currently loaded file.

The site is hosted on GitHub Pages, which does not offer any analytics that are visible to the site owner. GitHub Pages can only log visits to the `https://lite.datasette.io/` root page - it will not have visibility into any subsequent `#` fragment navigation.

To opt out of analytics, you can add `?analytics=off` or `&analytics=off` to the URL. This will prevent any analytics being sent to Plausible.

## Running the tests

Run the tests by running `pytest` after first installing the `dev-requirements.txt` dependencies.

Easy way is to run `./test.sh`. Or do this:

```bash
uv run --python 3.12 \
  --with-requirements dev-requirements.txt \
  python -m playwright install
```
Then run `pytest` like this:
```bash
uv run --python 3.12 \
  --with-requirements dev-requirements.txt \
  python -m pytest
```
