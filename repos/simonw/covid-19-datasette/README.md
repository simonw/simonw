# covid-19-datasette

[![Fetch latest data and deploy with Datasette](https://github.com/simonw/covid-19-datasette/workflows/Fetch%20latest%20data%20and%20deploy%20with%20Datasette/badge.svg)](https://github.com/simonw/covid-19-datasette/actions?query=workflow%3A%22Fetch+latest+data+and+deploy+with+Datasette%22)

Deploys a Datasette instance with data from the following sources:

* [CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19) by Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE)
* [nytimes/covid-19-data](https://github.com/nytimes/covid-19-data) by The New York Times
* [datadesk/california-coronavirus-data](https://github.com/datadesk/california-coronavirus-data) by The Los Angeles Times
* [TheEconomist/covid-19-excess-deaths-tracker](https://github.com/TheEconomist/covid-19-excess-deaths-tracker) by The Economist
* State and county population estimates from the [US Census](https://www.census.gov/programs-surveys/popest.html)

The Datasette instance lives at https://covid-19.datasettes.com/ and is updated hourly using [a scheduled GitHub Action](https://github.com/simonw/covid-19-datasette/blob/main/.github/workflows/scheduled.yml).

More about this project on my blog: [COVID-19 numbers in Datasette](https://simonwillison.net/2020/Mar/11/covid-19/).

This repository uses the deployment pattern described in [Deploying a data API using GitHub Actions and Cloud Run](https://simonwillison.net/2020/Jan/21/github-actions-cloud-run/).

## Using this data responsibly

Please **do not** use this tool to share information about COVID-19 without making absolutely sure you understand how the data is structured and sourced.

Recommended reading:

* [Why It’s So Freaking Hard To Make A Good COVID-19 Model](https://fivethirtyeight.com/features/why-its-so-freaking-hard-to-make-a-good-covid-19-model/)
* [Ten Considerations Before You Create Another Chart About COVID-19](https://medium.com/nightingale/ten-considerations-before-you-create-another-chart-about-covid-19-27d3bd691be8)

## Johns Hopkins

The database is partly built from the daily report CSV files in the Johns Hopkins CSSE `csse_covid_19_data` folder - be sure to consult [their README](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data) for documentation of the fields.

They are actively making changes to how they report data. You should [follow their issues](https://github.com/CSSEGISandData/COVID-19/issues) closely for updates - for example [this issue](https://github.com/CSSEGISandData/COVID-19/issues/382) about switching from reporting USA data at the county to the state level.

The [build script for the database](https://github.com/simonw/covid-19-datasette/blob/main/build_database.py) makes one alteration to their data: it attempts to fill any missing  `latitude` and `longitude` columns with values from similar rows.

If you are going to make use of those columns, make sure you understand how that backfill mechanism works in case it affects your calculations in some way.

## The New York Times

The New York Times has [a comprehensive README](https://github.com/nytimes/covid-19-data/blob/master/README.md) describing how their data is sourced. You should read it! They announced their data in [We’re Sharing Coronavirus Case Data for Every U.S. County](https://www.nytimes.com/article/coronavirus-county-data-us.html).

They are using the data for their [Coronavirus in the U.S.: Latest Map and Case Count](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html) article.

## The Los Angeles Times

The Los Angeles Time [comprehensive README](https://github.com/datadesk/california-coronavirus-data/blob/master/README.md) describes the data in the [latimes_agency_totals](https://covid-19.datasettes.com/covid/latimes_agency_totals), [latimes_county_totals](https://covid-19.datasettes.com/covid/latimes_county_totals), [latimes_place_totals](https://covid-19.datasettes.com/covid/latimes_place_totals) and [latimes_state_totals](https://covid-19.datasettes.com/covid/latimes_state_totals) tables.

See [To aid coronavirus fight, The Times releases database of California cases](https://www.latimes.com/california/story/2020-04-06/coronavirus-fight-la-times-releases-its-california-cases-database) for background on the release of this data.

The data is used for their [Tracking coronavirus in California](https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/) page, which is constantly updated.

## The Economist

The Economist publish the data behind their ongoing interactive [Tracking covid-19 excess deaths across countries](https://www.economist.com/graphic-detail/2020/04/16/tracking-covid-19-excess-deaths-across-countries). Their [README](https://github.com/TheEconomist/covid-19-excess-deaths-tracker/blob/master/README.md) describes the data sources they use for individual countries in detail.

This data is imported into the [economist_excess_deaths](https://covid-19.datasettes.com/covid/economist_excess_deaths) and  [economist_historical_deaths](https://covid-19.datasettes.com/covid/economist_historical_deaths) tables, with one alteration: a `cadence` column is added showing if each row is being collected on either a `weekly` or `monthly` basis.

## US Census

Two additional tables contain population data from the US Census.

* [us_census_state_populations_2019](https://covid-19.datasettes.com/covid/us_census_state_populations_2019) has data on the estimated 2019 population of different US States, derived from their [state population totals](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
* [us_census_county_populations_2019](https://covid-19.datasettes.com/covid/us_census_county_populations_2019) has data on estimated 2019 population of different US counties, keyed against county FIPS codes. This data was compiled [by Aaron King](https://github.com/nytimes/covid-19-data/pull/155) using [U.S. Census Bureau, Population Division, "Annual Estimates of the Resident Population for Counties in the United States: April 1, 2010 to July 1, 2019 (CO-EST2019-ANNRES)](https://www2.census.gov/programs-surveys/popest/tables/2010-2019/counties/totals/co-est2019-annres.xlsx).

This repository includes CSV data for both of these tables.

The [latest_ny_times_counties_with_populations](https://covid-19.datasettes.com/covid/latest_ny_times_counties_with_populations) view uses this data to calculate cases and deaths per million for US counties, based on the latest county figures from the New York Times.

## Example issues

* Remember: the number of reported cases is very heavily influenced by the availability of testing.
* [This Twitter thread](https://twitter.com/politicalmath/status/1243950120598556672) is an excellent overview of the challenges involved in comparing numbers from different states and countries.
* On the 23rd March 2020 Johns Hopkins [added four new columns](https://github.com/CSSEGISandData/COVID-19/commit/e748b6d8a55e4a88371af56b129ababe1712522d) to the daily CSV file: `admin2`, `fips`, `active` and `combined_key`. These are not present in older CSV files. [#4](https://github.com/simonw/covid-19-datasette/issues/4).
* Some countries (like Italy) are represented by [just the rows](https://covid-19.datasettes.com/covid/johns_hopkins_csse_daily_reports?country_or_region=Italy&_sort_desc=confirmed#g.mark=bar&g.x_column=day&g.x_type=ordinal&g.y_column=confirmed&g.y_type=quantitative) with `country_or_region` set to `Italy` (and `province_or_state` set to `null`). Larger countries such as the United States have multiple rows for each day divided into separate `province_or_state` values - [example](https://covid-19.datasettes.com/covid/johns_hopkins_csse_daily_reports?_size=1000&country_or_region__exact=US&_sort_desc=day#g.mark=bar&g.x_column=day&g.x_type=ordinal&g.y_column=confirmed&g.y_type=quantitative&g.color_column=province_or_state).
* Santa Clara County appears to be represented as `Santa Clara, CA` in some records and `Santa Clara County, CA` in others - [example](https://covid-19.datasettes.com/covid/johns_hopkins_csse_daily_reports?province_or_state__contains=santa+clara&_sort_desc=day#g.mark=bar&g.x_column=day&g.x_type=ordinal&g.y_column=confirmed&g.y_type=quantitative).
* Passengers from the Diamond Princess cruise are represented by a number of different rows with "From Diamond Princess" in their `province_or_state` column - [example](https://covid-19.datasettes.com/covid/johns_hopkins_csse_daily_reports?_facet=province_or_state&_facet=country_or_region&province_or_state__contains=from+diamond&_sort_desc=day).
* The [latest_ny_times_counties_with_populations](https://covid-19.datasettes.com/covid/latest_ny_times_counties_with_populations) view omits some counties, notably all New York City counties, because the New York Times groups all New York City data into rows with `county` equal to "New York City" and an empty `fips` column. Thus total cases represented in [latest_ny_times_counties_with_populations](https://covid-19.datasettes.com/covid/latest_ny_times_counties_with_populations) are lower than total cases represented in [ny_times_us_states](https://covid-19.datasettes.com/covid/ny_times_us_states) by at least the number of cases in New York City.
