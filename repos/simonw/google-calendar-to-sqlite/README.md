# google-calendar-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/google-calendar-to-sqlite.svg)](https://pypi.org/project/google-calendar-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/google-calendar-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/google-calendar-to-sqlite/releases)
[![Tests](https://github.com/simonw/google-calendar-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/google-calendar-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/google-calendar-to-sqlite/blob/master/LICENSE)

Create a SQLite database containing your data from [Google Calendar](https://www.google.com/calendar)

This lets you use SQL to analyze your Google Calendar data, using [Datasette](https://datasette.io/) or the SQLite command-line tool or any other SQLite database browsing software.

## Installation

Install this tool using `pip`:

    pip install google-calendar-to-sqlite

## Quickstart

Authenticate with Google Calendar by running:

    google-calendar-to-sqlite auth

Now create a SQLite database containing your calendar data with:

    google-calendar-to-sqlite events calendar.db your-email@gmail.com

You can pass one or more calendar IDs - these look like email addresses. Your primary Gmail account corresponds to your personal calendar.

If you pass no calendar IDs this will fetch events from all of your calendars:

    google-calendar-to-sqlite events calendar.db

This command will create an `events` table with a row for each event. Repeating events will appoar only once, with their recurrence rules stored in the `recurrence` column.

You can explore the resulting database using [Datasette](https://datasette.io/):

    $ pip install datasette
    $ datasette calendar.db
    INFO:     Started server process [24661]
    INFO:     Uvicorn running on http://127.0.0.1:8001

## See a list of calendars

You can see a list of your calendars using:

    google-calendar-to-sqlite calendars

This will output their ID and name to the terminal:

    $ google-calendar-to-sqlite calendars             
    Work: 2mcbt9bcthbvsm21j4rp4drhs8@group.calendar.google.com
    Simon Stanford Classes: tsblj5a6il733cd92kv08crkrg@group.calendar.google.com
    Pillar Point Stewards: tqhbk05br2h57kcd0gebbt9nmoq3iebt@import.calendar.google.com
    Holidays in United States: en.usa#holiday@group.v.calendar.google.com

If you add a database filename that list will be used to populate a detailed `calendars` table:

    google-calendar-to-sqlite calendars calendar.db

Events in that same database will have foreign keys back to the calendar they belong to.

## Authentication

> :warning: **This application has not yet been verified by Google** - you may find you are unable to authenticate until that verification is complete.
>
> You can work around this issue by [creating your own OAuth client ID key](https://til.simonwillison.net/googlecloud/google-oauth-cli-application) and passing it to the `auth` command using `--google-client-id` and `--google-client-secret`.

First, authenticate with Google Calendar using the `auth` command:

    $ google-calendar-to-sqlite auth
    Visit the following URL to authenticate with Google Calendar

    https://accounts.google.com/o/oauth2/v2/auth?...

    Then return here and paste in the resulting code:
    Paste code here: 

Follow the link, sign in with Google Calendar and then copy and paste the resulting code back into the tool.

This will save an authentication token to the file called `auth.json` in the current directory.

To specify a different location for that file, use the `--auth` option:

    google-calendar-to-sqlite auth --auth ~/google-calendar-auth.json

Full `--help`:

<!-- [[[cog
import cog
from google_calendar_to_sqlite import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["auth", "--help"])
help = result.output.replace("Usage: cli", "Usage: google-calendar-to-sqlite")
cog.out(
    "```\n{}\n```\n".format(help)
)
]]] -->
```
Usage: google-calendar-to-sqlite auth [OPTIONS]

  Authenticate user and save credentials

Options:
  -a, --auth FILE              Path to save token, defaults to auth.json
  --google-client-id TEXT      Custom Google client ID
  --google-client-secret TEXT  Custom Google client secret
  --scope TEXT                 Custom token scope
  --help                       Show this message and exit.

```
<!-- [[[end]]] -->

To revoke the token that is stored in `auth.json`, such that it cannot be used to access Google Calendar in the future, run the `revoke` command:

    google-calendar-to-sqlite revoke

Or if your token is stored in another location:

    google-calendar-to-sqlite revoke -a ~/google-calendar-auth.json

You will need to obtain a fresh token using the `auth` command in order to continue using this tool.


## Database schema

The database created by this tool has the following schema:

```sql
CREATE TABLE [calendars] (
   [id] TEXT PRIMARY KEY,
   [name] TEXT,
   [description] TEXT,
   [kind] TEXT,
   [etag] TEXT,
   [summary] TEXT,
   [timeZone] TEXT,
   [colorId] TEXT,
   [backgroundColor] TEXT,
   [foregroundColor] TEXT,
   [accessRole] TEXT,
   [defaultReminders] TEXT,
   [conferenceProperties] TEXT,
   [location] TEXT,
   [selected] INTEGER,
   [summaryOverride] TEXT,
   [notificationSettings] TEXT,
   [primary] INTEGER
);
CREATE TABLE [events] (
   [id] TEXT PRIMARY KEY,
   [summary] TEXT,
   [location] TEXT,
   [start_dateTime] TEXT,
   [end_dateTime] TEXT,
   [description] TEXT,
   [calendar_id] TEXT REFERENCES [calendars]([id]),
   [kind] TEXT,
   [etag] TEXT,
   [status] TEXT,
   [htmlLink] TEXT,
   [created] TEXT,
   [updated] TEXT,
   [creator] TEXT,
   [organizer] TEXT,
   [iCalUID] TEXT,
   [sequence] INTEGER,
   [reminders] TEXT,
   [eventType] TEXT,
   [attendees] TEXT,
   [recurringEventId] TEXT,
   [originalStartTime] TEXT,
   [start_date] TEXT,
   [end_date] TEXT,
   [transparency] TEXT,
   [start_timeZone] TEXT,
   [end_timeZone] TEXT,
   [recurrence] TEXT,
   [guestsCanInviteOthers] INTEGER,
   [extendedProperties] TEXT,
   [colorId] TEXT,
   [hangoutLink] TEXT,
   [conferenceData] TEXT,
   [visibility] TEXT,
   [privateCopy] INTEGER,
   [guestsCanSeeOtherGuests] INTEGER,
   [attachments] TEXT
);
```

## Privacy policy

This tool requests access to your Google Calendar account in order to retrieve events from your calendar and store them in a local SQLite database file on your machine.

The credentials used to access your account are stored in the `auth.json` file on your computer. The data retrieved from Google Calendar is also stored only on your own personal computer.

At no point do the developers of this tool gain access to any of your data.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd google-calendar-to-sqlite
    python -m venv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
