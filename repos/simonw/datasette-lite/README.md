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

Datasette's pages are displayed in a full-window `<iframe>` pointing at URLs under `/app/<session>/`. Those URLs don't exist on the server: a [service worker](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) (`sw.js`) intercepts every request for them - link clicks, GET and POST form submissions, `fetch()` calls made by JavaScript, static assets - and the page relays each one to Datasette's [ASGI](https://asgi.readthedocs.io/) application running in Pyodide. This means Datasette's own JavaScript and the JavaScript and CSS provided by plugins work, as do POST forms, CSRF protection, sign-in cookies, file uploads and downloads.

![Diagram of one request in Datasette Lite. The page you opened contains an iframe showing Datasette and the shell.js script. 1: the iframe requests /app/&lt;session&gt;/fixtures. 2: the sw.js service worker intercepts it and posts it to the owning tab. 3: shell.js forwards it to the Web Worker. 4: Python in Pyodide adds cookies and calls the Datasette ASGI app, which queries SQLite. 5 to 7: the response returns through shell.js and sw.js to the iframe.](diagrams/request-flow.svg)

The page you are on mirrors the iframe's location into its `#fragment`, so URLs like `https://lite.datasette.io/?url=...#/fixtures/facetable?_facet=state` can be bookmarked and shared, and the back button works. Links to other sites open in a new window, with `noopener` so the linked site gets no reference back to the Datasette Lite page. Each tab gets its own random `<session>` so multiple Datasette Lite tabs with different data can be open at once.

A response that Datasette sends over time - [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events), a streaming CSV export - reaches the page as it is produced rather than once it is complete. If the page stops reading one, by navigating away or aborting the `fetch()`, Datasette is told the client has disconnected.

Cookies are kept in a cookie jar inside the Python ASGI bridge (service workers cannot read or set cookies), so they last until the tab is closed or reloaded - as does all of the data.

If the tab that owns a session goes away, requests for that session fail with an error rather than hanging: a `503` if the tab has already been closed or reloaded, a `504` if it stops answering part way through a request (after four minutes, to leave room for slow SQL queries) and a `500` if the Pyodide worker itself fails. A tab that was opened before Datasette Lite was updated to an incompatible release gets a `409` asking for a reload.

A browser with service worker support is required. Some private browsing modes (Firefox private windows for example) disable service workers. The Web Worker is a [module worker](https://developer.mozilla.org/en-US/docs/Web/API/Worker/Worker#type), which Pyodide needs: Chrome 80, Safari 15 and Firefox 114 or later.

Python is version 3.14, from Pyodide 314.0.8.

## Load a different Datasette version

Datasette Lite uses the most recent Datasette release [from PyPI](https://pypi.org/project/datasette/), including alpha and beta preview releases. At the moment that means the Datasette 1.0 alphas.

To use the most recent stable release instead, add `?ref=stable`:

- https://lite.datasette.io/?ref=stable

Or for a specific release pass the version number as `?ref=`:

- https://lite.datasette.io/?ref=0.64.2
- https://lite.datasette.io/?ref=1.0a11

`?ref=pre` used to be how you asked for a preview release. It still works, and is now the same as leaving `?ref=` out.

### Unreleased code: a branch, tag or commit

Any other `?ref=` is treated as a branch, tag or commit in the [simonw/datasette](https://github.com/simonw/datasette) repository on GitHub, and Datasette is run from that source code instead of from a PyPI release:

- https://lite.datasette.io/?ref=main - the latest development code
- https://lite.datasette.io/?ref=dfeec630f86b4cbd06d24a090e654bd130344b71 - an exact commit

To try out a pull request, use the SHA of its most recent commit - this works for pull requests from forks too. A short SHA made up only of digits would be read as a version number, so use the full 40 character SHA.

A `?ref=` that looks like a version number, such as `1.0a11`, is always installed from PyPI, even though the repository has a tag of the same name.

The loading screen shows the version number and commit that was loaded. `?install=` plugins work as usual, and get their most recent preview releases.

This needs a commit that has a `pyproject.toml`, so it does not work for old releases - use their version number instead.

GitHub does not serve its source zip files with CORS headers, so Datasette Lite downloads them through a small Cloudflare Worker that adds those headers - for `?ref=`, and for [plugins installed from a GitHub repository](#plugins-from-a-github-repository). The proxy only serves repositories owned by `simonw` or `datasette`, and only to pages on `lite.datasette.io` and `localhost`. If you host your own copy of Datasette Lite on another domain you will need your own proxy: change `GITHUB_ZIP_PROXY` at the top of `webworker.js`.

## Load a different SQLite version

Datasette Lite uses the SQLite that is built into Pyodide, which is version 3.39.0. Add `?sqlite=` with a version number to use a different version of SQLite:

- https://lite.datasette.io/?sqlite=3.54.1

The versions you can use are listed on https://datasette.github.io/pysqlite3-wasm-wheels/. Each is a [pysqlite3](https://github.com/coleifer/pysqlite3) wheel with that version of SQLite compiled in, built for Pyodide by [datasette/pysqlite3-wasm-wheels](https://github.com/datasette/pysqlite3-wasm-wheels). Asking for a version that is not there shows an error that lists the versions that are.

The chosen version is used for everything: by Datasette, by plugins that `import sqlite3`, and for loading `?csv=`, `?json=`, `?parquet=` and `?sql=` files. `/-/versions` and `select sqlite_version()` both report it. It can be combined with any of the other options, for example to run a specific Datasette release on a specific SQLite:

- https://lite.datasette.io/?ref=stable&sqlite=3.54.1

Old versions of SQLite are not blocked. If Datasette cannot run on one, you will see the error from Datasette.

## The "Load" buttons

Every page has buttons at the bottom for loading a SQLite database, CSV, JSON, Parquet or SQL file by its URL. Once Datasette is running these load the file into it without reloading the page - a CSV becomes another table in the `data` database, a SQLite file another database - and show you what was loaded.

The matching parameter (`?url=`, `?csv=`, `?json=`, `?parquet=` or `?sql=`, each described below) is then added to the URL in your browser's address bar, after anything already there, so that URL is still a link to exactly what you are looking at.

The `fixtures` and `content` databases you get when a URL does not say what to load are removed the first time you load something, since the new URL would not load them. In the rare case where adding a file would change the name of a database or table that is already loaded, the page reloads with the new URL instead.

While Datasette is still starting up - or if it failed to start - the buttons start again with just the file you picked.

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
In this case it will search for the key that contains the most objects.

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

Pass `url` more than once to load multiple databases. Each database is named after its file, without the extension - `chinook.sqlite` becomes `chinook` - and repeated names are suffixed with `_2`, `_3`, and so on:

    https://lite.datasette.io/?url=https://example.com/data.db&url=https://other.example.com/data.db

Some examples to try out:

- [Global Power Plants](https://lite.datasette.io/?url=https://datasette.io/global-power-plants.db) - 33,000 power plants around the world
- [United States members of congress](https://lite.datasette.io/?url=https://datasette.io/legislators.db) - the example database from the [Learn SQL with Datasette](https://datasette.io/tutorials/learn-sql) tutorial

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

## Loading configuration

Datasette 1.0 alphas take [configuration](https://docs.datasette.io/en/latest/configuration.html) - plugin settings, permissions, `settings:` and more - from a `datasette.yaml` or `datasette.json` file. Pass a URL to one using `?config=`:

    https://lite.datasette.io/?config=https://example.com/datasette.yml

This needs Datasette 1.0a8 or later, so it does not work with `?ref=stable` while the stable release is 0.65.

You can also set individual configuration values in the URL using `?s.key=value`, the equivalent of the `datasette -s key value` [command-line option](https://docs.datasette.io/en/latest/configuration.html#configuration-via-the-command-line). This can be used multiple times. A setting can be given by its name:

    https://lite.datasette.io/?s.template_debug=1&s.default_page_size=10

Other keys are a path into the configuration, with values that are valid JSON treated as JSON:

    https://lite.datasette.io/?s.settings.sql_time_limit_ms=3500&s.plugins.datasette-cluster-map.latitude_column=lat

These are applied on top of any `?config=` file, and also need Datasette 1.0a8 or later.

Datasette Lite always sets the `base_url` and `num_sql_threads` settings itself.

## Signing in as root

Add `?root=1` to sign in as the `root` actor, the equivalent of running `datasette --root`. This is needed by plugins that write to the database, and for the Datasette 1.0 alpha [write API](https://docs.datasette.io/en/latest/json_api.html#the-json-write-api) and table editing features:

    https://lite.datasette.io/?root=1

Use "Log out" from the menu to return to being an anonymous user.

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

Plugins that load their own JavaScript and CSS now work, as do plugins that accept POST requests - for example [datasette-cluster-map](https://datasette.io/plugins/datasette-cluster-map), [datasette-vega](https://datasette.io/plugins/datasette-vega), [datasette-write](https://datasette.io/plugins/datasette-write), [datasette-edit-schema](https://datasette.io/plugins/datasette-edit-schema), [datasette-upload-csvs](https://datasette.io/plugins/datasette-upload-csvs) and [datasette-auth-passwords](https://datasette.io/plugins/datasette-auth-passwords). Plugins need to be pure Python (or available as Pyodide packages) and must not require threads or subprocesses.

Because Datasette Lite runs a preview release of Datasette by default, `?install=` also picks the most recent preview release of each plugin - that is where plugin authors publish support for the Datasette alphas. Some plugins do not work with the latest alpha yet. If one misbehaves, add `?ref=stable` to run it against the stable Datasette release, which installs the plugin's stable release too.

### The Manage plugins dialog

Datasette's menu - the icon at the top right of every page - has a **Manage plugins** item. It opens a dialog that lists the plugins that are installed, with a checkbox next to each one that you can untick to remove it, some suggested plugins to tick, and a text box for the name of any other plugin. That box accepts anything `?install=` does, such as `plugin-name==0.3` for a specific version.

Applying your changes does not reload the page. The `?install=` parameters in the URL are updated to match, so the URL in your browser can still be bookmarked or shared.

Where it can, the Datasette that is already running makes the change itself: a new plugin is installed and registered, a removed one is unregistered, and Datasette restarts over the same database files. That takes a second or two, nothing is downloaded again, you stay signed in and changes you made to the data are kept - other than to the in-memory `_memory` database, which starts out empty again. A plugin that was removed stays installed, unused, until the page is reloaded.

Python cannot replace code it has already imported, so a change that would need that - a different version of a plugin that is installed, for example - starts Python and Datasette again from nothing instead, loading your data again from where it came from. The Datasette you were using keeps running until the new one is ready. Either way, if a plugin cannot be installed the dialog says why and nothing changes.

The dialog is built with the JavaScript API for modal dialogs that was added in Datasette 1.0a41, so the menu item is not shown for older versions, such as `?ref=stable`.

### Plugins from a GitHub repository

To try a plugin's unreleased code, give `?install=` its GitHub repository instead of its name on PyPI - either as `owner/repo` or as the URL of the repository:

- https://lite.datasette.io/?install=simonw/datasette-cluster-map
- https://lite.datasette.io/?install=https://github.com/simonw/datasette-cluster-map

Both run the plugin from the source on the repository's default branch - usually `main`.

This only works for repositories owned by `simonw` or `datasette` on GitHub - see [the proxy](#the-github-proxy) below.

To use a different branch, a tag or a commit, add `@` and its name to either form:

- https://lite.datasette.io/?install=simonw/datasette-cluster-map@0.19 - a tag
- https://lite.datasette.io/?install=simonw/datasette-cluster-map@ca51346 - a commit
- https://lite.datasette.io/?install=https://github.com/simonw/datasette-cluster-map@main - a branch

The URLs of GitHub's own pages for a branch, tag, commit or pull request work as well, so you can paste one in from your browser's address bar:

- `?install=https://github.com/simonw/datasette-cluster-map/tree/main` - a branch or tag
- `?install=https://github.com/simonw/datasette-cluster-map/commit/ca513469392a4facd267267728cd7ab0252a7583` - a commit
- `?install=https://github.com/simonw/datasette-cluster-map/pull/58` - the most recent commit in a pull request, including one from a fork

The loading screen shows the version number and commit that was loaded. The plugin's dependencies are installed from PyPI as usual, and this can be combined with other `?install=` parameters and with `?ref=`.

Nothing is built, so this works for plugins where the code in the repository is the code that runs:

- The repository needs a `pyproject.toml` with a `[project]` table - a plugin that only has a `setup.py` cannot be installed this way. That includes older tags and commits, from before a plugin switched to `pyproject.toml`.
- The code needs to be a package or module named after the project - `datasette_cluster_map/` or `datasette_cluster_map.py` for `datasette-cluster-map` - at the top of the repository or in `src/`.
- A plugin that compiles its JavaScript or CSS when it is packaged will be missing those files.

#### The GitHub proxy

The source is downloaded through the same proxy that `?ref=` uses, [described above](#unreleased-code-a-branch-tag-or-commit). That proxy only serves repositories owned by `simonw` or `datasette`, so those are the only plugins that can be installed from GitHub this way: `?install=simonw/datasette-cluster-map` and `?install=datasette/datasette-enrichments` work, a repository belonging to anyone else is an error. To install plugins from other repositories you need to host your own copy of Datasette Lite with your own proxy.

Some plugins hardcode root-relative URLs such as `/-/password-tool` rather than respecting Datasette's `base_url` setting. Datasette Lite rewrites those in HTML attributes and routes requests for them back to the right tab, including links that a plugin's JavaScript adds to the page. One case is handled less smoothly in Firefox and Safari: when JavaScript navigates to such a URL (`location.href = "/-/..."`) from a table, row or query page, those browsers give the service worker no way to tell which tab the navigation came from. The request reaches the web server first, and Datasette Lite then loads the right page itself - so it works, but a form submitted that way loses its POST data.

- [datasette-cluster-map](https://datasette.io/plugins/datasette-cluster-map) - Datasette plugin that shows a map for any data with latitude/longitude columns - [demo](https://lite.datasette.io/?install=datasette-cluster-map&url=https://datasette.io/global-power-plants.db#/global-power-plants/global-power-plants)
- [datasette-write](https://datasette.io/plugins/datasette-write) - Datasette plugin providing a UI for executing SQL writes against the database (needs `?root=1`) - [demo](https://lite.datasette.io/?root=1&install=datasette-write#/fixtures/-/write)
- [datasette-edit-schema](https://datasette.io/plugins/datasette-edit-schema) - Datasette plugin for modifying table schemas (needs `?root=1`) - [demo](https://lite.datasette.io/?root=1&install=datasette-edit-schema#/-/edit-schema/fixtures/facetable)
- [datasette-upload-csvs](https://datasette.io/plugins/datasette-upload-csvs) - Datasette plugin for uploading CSV files and converting them to database tables (needs `?root=1`) - [demo](https://lite.datasette.io/?root=1&memory=1&csv=https://raw.githubusercontent.com/fivethirtyeight/data/master/fight-songs/fight-songs.csv&install=datasette-upload-csvs#/-/upload-csvs)

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
- `tests/test_bridge.py` - fast pure-Python tests of the ASGI bridge, cookie jar and `base_url` workarounds, extracted from `webworker.js`. Install `datasette` to also run them against a real Datasette.
- `tests/test_datasette_lite.py` - the original browser tests, loading the default databases.
- `tests/test_url_patterns.py` - every supported `?` option and `#` URL pattern, using the small files in `tests/fixtures/`.
- `tests/test_plugins_and_post.py` - JavaScript (core and plugins), POST forms, CSRF, sign-in, uploads, downloads, the 1.0 alpha write API, multiple tabs, other pages open on the same origin, worker failures, a cross-origin page in the iframe and service worker restarts.
- `tests/test_manage_plugins.py` - the Manage plugins dialog: installing and removing plugins in the running Datasette, and starting again in a new worker when that is not possible.
- `tests/test_streaming.py` - responses that arrive over time, using the plugin in `tests/plugins/`.

Tests that download from third-party hosts beyond Pyodide, PyPI and the default databases are marked `network`; skip them with `-m "not network"`. To use an existing Chromium binary set `CHROMIUM_EXECUTABLE=/path/to/chrome`. If the browser needs an HTTPS proxy set `DATASETTE_LITE_TEST_PROXY` (or `HTTPS_PROXY`).
