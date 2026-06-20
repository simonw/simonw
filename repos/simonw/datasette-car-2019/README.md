# Publish the data behind your stories with SQLite and Datasette

_NICAR 2019 workshop, 8th March 2019_

## Some introductory information

* [Datasette](https://datasette.readthedocs.io/)
* [The Datasette Ecosystem](https://datasette.readthedocs.io/en/stable/ecosystem.html)

Two of my projects:

* [Exploring the UK Register of Members Interests with SQL and Datasette](https://simonwillison.net/2018/Apr/25/register-members-interests/) - resulting in https://register-of-members-interests.datasettes.com/
* [Analyzing US Election Russian Facebook Ads](https://simonwillison.net/2018/Aug/6/russian-facebook-ads/) - resulting in https://russian-ira-facebook-ads.datasettes.com/

Two projects by other people:

* [Baltimore Sun Public Salary Records](https://salaries.news.baltimoresun.com/)
* [db.OffeneRegister.de](https://db.offeneregister.de/) - German Trade Registrer data released by Open Knowledge Foundation Deutschland e.V.

## Getting started

First we need to install some software. Assuming you have a working Python 3 environment I recommend using pipenv:

    $ pip3 install pipenv
    $ mkdir car-2019-datasette
    $ cd car-2019-datasette
    $ pipenv shell

`pipenv shell` creates and activates a new Python virtual environment for that directory. We can install software in that environment like so:

    $ pip install datasette csvs-to-sqlite

To confirm that the correct software is installed, run these commands:

    $ datasette --version
    datasette, version 0.27
    $ csvs-to-sqlite --version
    csvs-to-sqlite, version 0.9

## Building our first Datasette

We're going to start by building this: 
https://nicar-2019.herokuapp.com/nicar-459dd1d/sessions

Datasette documentation is at https://datasette.readthedocs.io/

The `csvs-to-sqlite` documentation is at  https://github.com/simonw/csvs-to-sqlite

## Creating our first SQLite database

The NICAR schedule is available as a CSV! You can download the file from https://raw.githubusercontent.com/ireapps/nicar-2019-schedule/master/car19guide.csv

Let's turn that into a SQLite database:

    $ curl -O https://raw.githubusercontent.com/ireapps/nicar-2019-schedule/master/car19guide.csv
    $ csvs-to-sqlite car19guide.csv nicar.db
    Loaded 1 dataframes
    Created nicar.db from 1 CSV file

Now we can use the `sqlite3` command to run queries against it:

    $ sqlite3 nicar.db "select count(*) from car19guide"
    257
    $ sqlite3 nicar.db "select * from car19guide limit 1"
    4178|(Generally) painless collaboration with the greater newsroom|Traditional reporters and editors often view the data team as a one-stop service desk, a group of unapproachable nerds who will shoot down all their ideas, or full-stack programmers who can magically visualize all the data bouncing around in their heads. In this panel, we’ll discuss ways to revamp your newsroom reputation, change perceptions of your team and open up the lines of communication with your colleagues. |Salon A&B|2019-03-09|2019-03-09 15:30:00|2019-03-09 16:30:00|0|0|0|Ryann Grochowski Jones, ProPublica (moderator); Ariana Giorgi, The Dallas Morning News; Yan Wu, NJ Advance Media|Panel||General interest|(Generally) painless collaboration with the greater newsroom

Let's use Datasette to browse this new database:

    $ datasette nicar.db 
    Serve! files=('nicar.db',) on port 8001
    [2019-03-08 08:08:52 -0800] [56417] [INFO] Goin' Fast @ http://127.0.0.1:8001
    [2019-03-08 08:08:52 -0800] [56417] [INFO] Starting worker [56417]

Now visit http://127.0.0.1:8001/ and start browsing the data! Make sure to play with the facets.

### Let's make this searchable

It would be useful if we could run a search against the titles, descriptions and speakers.

SQLite has built-in full-text search. `csvs-to-sqlite` knows how to set that up, and Datasette knows how to run searches against it.

The `-f` option means "set up full-text search against this column" - you can specify as many columns as you like.

    $ csvs-to-sqlite car19guide.csv nicar2.db -f name -f clean_description -f speakers_cleaned -f keywords
    Loaded 1 dataframes
    Created nicar2.db from 1 CSV file
    $ datasette nicar2.db 
    Serve! files=('nicar2.db',) on port 8001
    [2019-03-08 08:08:52 -0800] [56417] [INFO] Goin' Fast @ http://127.0.0.1:8001
    [2019-03-08 08:08:52 -0800] [56417] [INFO] Starting worker [56417]

Now the Datasette interface will include a search box, which you can use to search the data.

You can pass multiple database files to Datasette - so we can look at the differences between these two like so:

    $ datasette nicar.db nicar2.db

### Extracting columns

A big downside of CSV files as a way of distributing data is that they encourage a great deal of data duplication. Our NICAR database has the same value copied many times in the `location_room` and `session_type` columns.

Since SQLite is a relational database, these can be better modelled as separate tables. `csvs-to-sqlite` has an option for extracting the contents of a specific column out into a separate table: `-c`. We can use that like this:

    $ csvs-to-sqlite car19guide.csv nicar.db -f name -f clean_description -f speakers_cleaned -f keywords -c location_room -c session_type -c skill_level -t sessions

We've also added `-t sessions` at the end to tell it that we would like the main resulting table to be called `sessions`.

Run `datasette nicar.db` to see the result. In particular, note that the sessions table still shows the correct data but each room, session type and skill level now links through to another page - and that page has links back to all rows relating to that item.

### Publishing this to the internet

All of this currently just lives on your local machine. How about publishing it to the internet?

Datasette is designed to be run on servers. You can set up your own server for this, but by far the easiest way to get your data live is to use [Heroku](https://www.heroku.com/). Datasette has a built-in command [for publishing using Heroku](https://datasette.readthedocs.io/en/stable/publish.html#publishing-to-heroku) which looks like this:

    datasette publish heroku nicar.db --title "CAR 2019 schedule" --source_url=https://www.ire.org/events-and-training/conferences/nicar-2019

Before you can run this you'll need to be signed in with a Heroku account on your machine. You can do that by running `heroku login`.

This will publish your database and return a new URL where you can browse it online. The `--title` and `--source_url` options can be used to attach metadata to the new deployment, see [the docs](https://datasette.readthedocs.io/en/stable/publish.html#publishing-to-heroku) for additional options.

## California Civic Data

https://www.californiacivicdata.org/ offers CSV downloads of the latest California campaign finance data. You can download it from https://calaccess.download/latest/flat.zip

    $ unzip flat.zip
    $ ls
    BallotMeasures.csv
    Candidates.csv
    RecallMeasures.csv
    flat.zip

We can convert all three CSV files into a SQLite database like this:

    $ csvs-to-sqlite *.csv ca.db

This will create a new table for each CSV file.

Then run Datasette:

    $ datasette ca.db

This data is a really good fit for Datasette's faceting feature. Try these:

* http://127.0.0.1:8001/ca-f58a921/BallotMeasures?_facet=classification&_facet=election_name
* http://127.0.0.1:8001/ca-f58a921/Candidates?_facet=election_name&_facet=party_name

### Geographic data

There is a CSV file of facilities managed by the city of San Francisco, available from the San Francisco open data portal at https://data.sfgov.org/City-Infrastructure/City-Facilities/nc68-ngbr

We can use this data to demonstrate Datasette's plugins functionality. The plugin we are going to use is called `datasette-cluster-map`. You can install ot like this:

    $ pip install datasette-cluster-map

You can see what plugins are installed using the `datasette plugins` command:

    $ datasette plugins
    [
        {
            "name": "datasette_cluster_map",
            "static": true,
            "templates": false,
            "version": "0.5"
        }
    ]

This plugin scans the current table for `latitude` and `longitude` columns and, if found, renders the data on a clustered marker map.

So we can convert the city facilities CSV to a SQLite database like this:

    $ csvs-to-sqlite City_Facilities.csv facilities.db

Then load it using Datasette:

    $ datasette facilities.db

Now if you navigate to the corresponding table page, Datasette will render it on a map! Try clicking the "load all" button to load everything (not just the first 1,000 items). I've run this successfully against 200,000 items, so it works for visualizing quite large datasets.

### datasette-vega

Another plugin: this one does charts. You can install it with `pip install datasette-vega`

Example: [avail_seat_km_per_week for different airlines](https://fivethirtyeight.datasettes.com/fivethirtyeight-b76415d/airline-safety%2Fairline-safety#g.mark=bar&g.x_column=airline&g.x_type=ordinal&g.y_column=avail_seat_km_per_week&g.y_type=quantitative) from FiveThirtyEight's airline safety data.

This illustrates a pattern where a plugin can persist its settings in the `#fragment` section of the URL. This means it's possible to bookmark graphs based on the options that were fed into the plugin.

## Bonus exercise: sqlite-utils

Not every interesting dataset is published as CSV.

`sqlite-utils` is a Python library and command-line tool aimed at making it as easy as possible to create SQLite databases from JSON or other data sources.

[sqlite-utils: a Python library and CLI tool for building SQLite databases](https://simonwillison.net/2019/Feb/25/sqlite-utils/) is a tutorial on how to use it.
