# cdc-vaccination-history

> **Project retired** as of 25th October 2023

A [git scraper](https://simonwillison.net/2020/Oct/9/git-scraping/) recording the CDC's [Covid Data Tracker](https://covid.cdc.gov/covid-data-tracker/#vaccinations) numbers on number of vaccinations per state.

Archives the JSON from https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_data every time it changes, checking three times an hour.

Watch [Git scraping, the five minute lightning talk](https://simonwillison.net/2021/Mar/5/git-scraping/) to see me live-code the creation of this repository.

## This data as CSV

If you want to grab the entire dataset I'm now publishing it as two CSV files here:

- https://cdc-vaccination-history-csv.datasette.io/daily_reports.csv - ~5.5MB
- https://cdc-vaccination-history-csv.datasette.io/daily_reports_counties.csv - ~90MB

## This data in Datasette

The `build_database.py` script loops through the full commit history and uses it to build a SQLite database with a row for every daily report, mainly as a demonstration of how Python code can be used to extract data from a git scraped repository.

That database is then deployed using [Datasette](https://datasette.io/) - you can browse the data at https://cdc-vaccination-history.datasette.io/cdc/daily_reports

You can filter down to individual states like so:

- https://cdc-vaccination-history.datasette.io/cdc/daily_reports?_sort=id&Location__exact=CA

Take a look at the [scrape.yml](https://github.com/simonw/cdc-vaccination-history/blob/main/.github/workflows/scrape.yml) GitHub Actions workflow to see how the scraper runs, and how the data is then built into a database and published to Vercel using `datasette publish`.

## Should you trust these numbers?

I honestly don't know. These are not coming from a documented API - I found it using the Firefox developer tools network pane. I don't know how the CDC are sourcing these. I don't know if they themselves consider them to be accurate.

All I know is that these are the numbers they are displaying on their own site - so you should treat this repository as tracking "numbers that were displayed on the CDC's website" as opposed to assuming it represents the full truth on the ground.
