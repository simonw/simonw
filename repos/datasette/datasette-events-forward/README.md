# datasette-events-forward

[![PyPI](https://img.shields.io/pypi/v/datasette-events-forward.svg)](https://pypi.org/project/datasette-events-forward/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-events-forward?include_prereleases&label=changelog)](https://github.com/datasette/datasette-events-forward/releases)
[![Tests](https://github.com/datasette/datasette-events-forward/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-events-forward/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-events-forward/blob/main/LICENSE)

Forward Datasette events to another instance

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-events-forward
```

## Configuration

Configure the plugin like so:

```json
{
    "plugins": {
        "datasette-events-forward": {
            "api_token": "***",
            "api_url": "https://stats.datasette.cloud/data/-/create",
            "instance": "localhost"
        }
    }
}
```
The plugin will then gather all events and forward them to the specified instance, adding them to a table called `datasette_events` which will be created if it does not exist.

The `instance` key can be used to differentiate different instances that report to the same backend. Events are identified with a ULID to ensure they are unique even across different instances.

Events are forwarded in batches of up to 10, no more than once every 10 seconds.

Full list of configuration settings:

- `api_url`: The write API URL of a Datasette instance to forward the events to.
- `api_token`: The API token to use when sending events. Use `{"$env": "FORWARD_TOKEN"}` to read the token from the `FORWARD_TOKEN` environment variable.
- `instance`: A string to identify the instance that is sending the events.

The `api_url` can be either a `https://datasette.example.com/data/datasette_events/-/insert` endpoint for inserting rows, or a `https://datasette.example.com/data/-/create` endpoint for creating a table and inserting rows into it. If the table does not yet exist you should use the `/-/create` variant, otherwise use the `/-/insert` variant.

If you use `/-/insert` your API token just needs `insert-row` permissions. For `/-/create` you will need `create-table` permissions as well.

And to control the rate at which batches of events are sent to the Datasette write API:

- `batch_limit`: The number of events to send in each batch, defaults to 10. The Datasette write API has a 100 row limit by default so this should be set to a value less than that.
- `max_rate`: The maximum number of deliver HTTP requests to send in the specified time period, defaults to 1.
- `time_period`: The time period for the rate limiting in seconds, defaults to 10.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-events-forward
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
