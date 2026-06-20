# datasette-ics

[![PyPI](https://img.shields.io/pypi/v/datasette-ics.svg)](https://pypi.org/project/datasette-ics/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-ics?include_prereleases&label=changelog)](https://github.com/simonw/datasette-ics/releases)
[![Tests](https://github.com/simonw/datasette-ics/workflows/Test/badge.svg)](https://github.com/simonw/datasette-ics/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-ics/blob/main/LICENSE)

Datasette plugin that adds support for generating [iCalendar .ics files](https://tools.ietf.org/html/rfc5545) with the results of a SQL query.

## Installation

Install this plugin in the same environment as Datasette to enable the `.ics` output extension.

    $ pip install datasette-ics

## Usage

To create an iCalendar file you need to define a custom SQL query that returns a required set of columns:

* `event_name` - the short name for the event
* `event_dtstart` - when the event starts

The following columns are optional:

* `event_dtend` - when the event ends
* `event_duration` - the duration of the event (use instead of `dtend`)
* `event_description` - a longer description of the event
* `event_uid` - a globally unique identifier for this event
* `event_tzid` - the timezone for the event, e.g. `America/Chicago`

A query that returns these columns can then be returned as an ics feed by adding the `.ics` extension.

## Demo

[This SQL query]([https://www.rockybeaches.com/data?sql=with+inner+as+(%0D%0A++select%0D%0A++++datetime%2C%0D%0A++++substr(datetime%2C+0%2C+11)+as+date%2C%0D%0A++++mllw_feet%2C%0D%0A++++lag(mllw_feet)+over+win+as+previous_mllw_feet%2C%0D%0A++++lead(mllw_feet)+over+win+as+next_mllw_feet%0D%0A++from%0D%0A++++tide_predictions%0D%0A++where%0D%0A++++station_id+%3D+%3Astation_id%0D%0A++++and+datetime+%3E%3D+date()%0D%0A++++window+win+as+(%0D%0A++++++order+by%0D%0A++++++++datetime%0D%0A++++)%0D%0A++order+by%0D%0A++++datetime%0D%0A)%2C%0D%0Alowest_tide_per_day+as+(%0D%0A++select%0D%0A++++date%2C%0D%0A++++datetime%2C%0D%0A++++mllw_feet%0D%0A++from%0D%0A++++inner%0D%0A++where%0D%0A++++mllw_feet+%3C%3D+previous_mllw_feet%0D%0A++++and+mllw_feet+%3C%3D+next_mllw_feet%0D%0A)%0D%0Aselect%0D%0A++min(datetime)+as+event_dtstart%2C%0D%0A++%27Low+tide%3A+%27+||+mllw_feet+||+%27+feet%27+as+event_name%2C%0D%0A++%27America%2FLos_Angeles%27+as+event_tzid%0D%0Afrom%0D%0A++lowest_tide_per_day%0D%0Agroup+by%0D%0A++date%0D%0Aorder+by%0D%0A++date&station_id=9414131) calculates the lowest tide per day at Pillar Point in Half Moon Bay, California.

Since the query returns `event_name`, `event_dtstart` and `event_tzid` columns it produces [this ICS feed](https://www.rockybeaches.com/data.ics?sql=with+inner+as+(%0D%0A++select%0D%0A++++datetime%2C%0D%0A++++substr(datetime%2C+0%2C+11)+as+date%2C%0D%0A++++mllw_feet%2C%0D%0A++++lag(mllw_feet)+over+win+as+previous_mllw_feet%2C%0D%0A++++lead(mllw_feet)+over+win+as+next_mllw_feet%0D%0A++from%0D%0A++++tide_predictions%0D%0A++where%0D%0A++++station_id+%3D+%3Astation_id%0D%0A++++and+datetime+%3E%3D+date()%0D%0A++++window+win+as+(%0D%0A++++++order+by%0D%0A++++++++datetime%0D%0A++++)%0D%0A++order+by%0D%0A++++datetime%0D%0A)%2C%0D%0Alowest_tide_per_day+as+(%0D%0A++select%0D%0A++++date%2C%0D%0A++++datetime%2C%0D%0A++++mllw_feet%0D%0A++from%0D%0A++++inner%0D%0A++where%0D%0A++++mllw_feet+%3C%3D+previous_mllw_feet%0D%0A++++and+mllw_feet+%3C%3D+next_mllw_feet%0D%0A)%0D%0Aselect%0D%0A++min(datetime)+as+event_dtstart%2C%0D%0A++%27Low+tide%3A+%27+||+mllw_feet+||+%27+feet%27+as+event_name%2C%0D%0A++%27America%2FLos_Angeles%27+as+event_tzid%0D%0Afrom%0D%0A++lowest_tide_per_day%0D%0Agroup+by%0D%0A++date%0D%0Aorder+by%0D%0A++date&station_id=9414131). If you subscribe to that in a calendar application such as Apple Calendar you get something that looks like this:

![Apple Calendar showing low tides at Pillar Point during a week](https://user-images.githubusercontent.com/9599/173158984-e5ec6bd0-33fc-4fc0-ba9d-17ae674f310a.jpg)

## Using a canned query

Datasette's [canned query mechanism](https://datasette.readthedocs.io/en/stable/sql_queries.html#canned-queries) can be used to configure calendars. If a canned query definition has a `title` that will be used as the title of the calendar.

Here's an example, defined using a `metadata.yaml` file:

```yaml
databases:
  mydatabase:
    queries:
      calendar:
        title: My Calendar
        sql: |-
          select
            title as event_name,
            start as event_dtstart,
            description as event_description
          from
            events
          order by
            start
          limit
            100
```
This will result in a calendar feed at `http://localhost:8001/mydatabase/calendar.ics`
