# datasette-alerts

[![PyPI](https://img.shields.io/pypi/v/datasette-alerts.svg)](https://pypi.org/project/datasette-alerts/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-alerts?include_prereleases&label=changelog)](https://github.com/datasette/datasette-alerts/releases)
[![Tests](https://github.com/datasette/datasette-alerts/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-alerts/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-alerts/blob/main/LICENSE)

Alerts and notifications for Datasette. Supports row-based alerts (new rows in a table) and custom alert types defined by plugins.

## How It Works

datasette-alerts uses [datasette-cron](https://github.com/datasette/datasette-cron) for scheduling. When an alert is created, a cron task is registered that periodically checks for new data and sends notifications through configured destinations.

**Built-in alert types:**
- **Cursor alerts** — poll a table for rows newer than a timestamp cursor
- **Trigger alerts** — SQLite INSERT trigger queues new rows for processing

**Custom alert types** — plugins can register their own alert logic via the `datasette_alerts_register_alert_types` hook.

## Notifier Plugins

| Plugin | Description |
| ------ | ----------- |
| [`datasette-alerts-slack`](https://github.com/datasette/datasette-alerts-slack) | Send Slack messages |
| [`datasette-alerts-discord`](https://github.com/datasette/datasette-alerts-discord) | Send Discord messages |
| [`datasette-alerts-ntfy`](https://github.com/datasette/datasette-alerts-ntfy) | Send ntfy.sh notifications |
| [`datasette-alerts-desktop`](https://github.com/datasette/datasette-alerts-desktop) | Local desktop notifications |

## Writing a Notifier Plugin

Notifier plugins implement the `datasette_alerts_register_notifiers` hook and return subclasses of `Notifier`.

```python
from datasette import hookimpl
from datasette_alerts import Notifier, Message
from wtforms import Form, StringField


@hookimpl
def datasette_alerts_register_notifiers(datasette):
    return [MyNotifier()]


class MyNotifier(Notifier):
    slug = "my-notifier"
    name = "My Notifier"
    description = "Send alerts somewhere"

    async def get_config_form(self):
        class ConfigForm(Form):
            webhook_url = StringField("Webhook URL")
        return ConfigForm

    async def send(self, config: dict, message: Message):
        url = config["webhook_url"]
        # deliver message.text (and optionally message.subject)
```

### Notifier API

#### `Notifier` (abstract base class)

| Property / Method | Description |
| ----------------- | ----------- |
| `slug` | Unique identifier (required) |
| `name` | Display name (required) |
| `description` | Short description |
| `icon` | SVG string for the UI |
| `get_config_form()` | Return a WTForms `Form` class for destination config |
| `get_config_element()` | Return a `ConfigElement` for web component config UI |
| `send(config, message)` | Deliver a `Message` to the destination described by `config` |

#### `Message`

```python
Message(text: str, *, subject: str | None = None)
```

## Writing a Custom Alert Type

Custom alert types let plugins define their own checking logic. datasette-alerts handles the scheduling, notification delivery, and logging.

### Minimal Example

```python
from datasette import hookimpl
from datasette_alerts import AlertType, Message


class MyAlertType(AlertType):
    slug = "my-check"
    name = "My Custom Check"
    description = "Checks something and alerts when it finds results"

    async def check(self, datasette, alert_config, database_name, last_check_at):
        db = datasette.get_database(database_name)
        # Your custom logic here — query tables, check conditions, etc.
        result = await db.execute("SELECT * FROM my_queue WHERE status = 'pending'")
        
        messages = []
        ids = []
        for row in result.rows:
            ids.append(row[0])
            messages.append(Message(f"New item: {row[1]}"))
        
        # Mark as processed
        if ids:
            placeholders = ",".join("?" for _ in ids)
            await db.execute_write(
                f"UPDATE my_queue SET status = 'done' WHERE id IN ({placeholders})",
                ids,
            )
        
        return messages


@hookimpl
def datasette_alerts_register_alert_types(datasette):
    return [MyAlertType()]
```

### AlertType API

#### `AlertType` (abstract base class)

| Property / Method | Description |
| ----------------- | ----------- |
| `slug` | Unique identifier (required) |
| `name` | Display name (required) |
| `description` | Short description |
| `icon` | SVG string for the UI |
| `check(datasette, alert_config, database_name, last_check_at)` | Run check logic, return `list[Message]` |
| `get_config_element()` | Optional web component for alert configuration UI |
| `get_config_form()` | Optional WTForms form for configuration |

#### `check()` Method

```python
async def check(
    self,
    datasette,           # Datasette instance
    alert_config: dict,  # from the alert's custom_config column
    database_name: str,  # which database this alert is scoped to
    last_check_at: str | None,  # ISO timestamp of last check, or None on first run
) -> list[Message]:
```

Return a list of `Message` objects to send. Empty list means nothing to report. The handler calls `check()` on the schedule defined by the alert's frequency, sends any returned messages through the alert's subscriptions, and updates `last_check_at`.

### How Custom Alerts Get Scheduled

When a custom alert is created (via the API or a plugin's own routes):

1. A row is inserted into `datasette_alerts_alerts` with `alert_type="custom:{slug}"`
2. A cron task is registered with `datasette-cron` at the alert's frequency
3. Each tick, the `custom_alert_handler` looks up the `AlertType` by slug via the plugin hook
4. Calls `check()` with the alert's config and database
5. Sends any returned messages to all subscriptions
6. Updates `last_check_at` and logs the check

### Creating Custom Alerts Programmatically

```python
from datasette_alerts.internal_db import InternalDB, NewAlertRouteParameters, NewSubscription

internal_db = InternalDB(datasette.get_internal_database())

params = NewAlertRouteParameters(
    database_name="mydb",
    alert_type="custom:my-check",
    frequency="+1 second",
    custom_config={"key": "value"},
    subscriptions=[
        NewSubscription(destination_id="dest-id", meta={"aggregate": True})
    ],
)
alert_id = await internal_db.new_alert(params)

# Register the cron task
from datasette_alerts import _register_cron_task_for_alert
from types import SimpleNamespace

await _register_cron_task_for_alert(datasette, SimpleNamespace(
    id=alert_id,
    alert_type="custom:my-check",
    frequency="+1 second",
))
```

## Public API

### `send_to_destination()`

Send a message through a configured destination without creating an alert:

```python
from datasette_alerts import send_to_destination, Message

await send_to_destination(datasette, destination_id, Message("Hello!"))
```

Raises `DestinationNotFound` or `NotifierNotFound` on errors.

### `trigger_alert_check()`

Trigger an immediate check for an alert, outside its normal schedule:

```python
from datasette_alerts import trigger_alert_check

await trigger_alert_check(datasette, alert_id)
```

### API Endpoint: List Alert Types

```
GET /-/{database}/datasette-alerts/api/alert-types
```

Returns registered custom alert types with their slug, name, description, and config element info.

## Data Models

Query results from `InternalDB` return typed dataclasses:

```python
from datasette_alerts.models import AlertRecord, AlertForCheck, AlertDetail
```

### `AlertRecord`

Returned by `get_all_alerts()`. Fields: `id`, `database_name`, `table_name`, `id_columns`, `timestamp_column`, `frequency`, `alert_type`, `custom_config`, `last_check_at`.

### `AlertForCheck`

Returned by `get_alert_for_check()`. Same as `AlertRecord` plus `cursor`.

### `AlertDetail`

Returned by `get_alert_detail()`. Full alert info including nested `subscriptions: list[SubscriptionDetail]` and `logs: list[AlertLogEntry]`, plus `custom_config`, `last_check_at`, `next_deadline`, `alert_created_at`.

### `AlertCleanupInfo`

Returned by `delete_alert()`. Fields: `alert_type`, `database_name`, `table_name`.

## Config: WTForms vs Web Components

There are two ways to provide a destination (or alert type) configuration UI:

#### WTForms (simple)

Override `get_config_form()` and return a WTForms `Form` class.

#### `ConfigElement` (rich UI)

Return a `ConfigElement` that declares a custom HTML element:

```python
from datasette_alerts import ConfigElement

def get_config_element(self):
    return ConfigElement(
        tag="my-config-form",
        scripts=["/-/my-plugin/config.js"],
    )
```

Web component contract:
- **Inputs**: `config` property, `datasette-base-url` attribute, `database-name` attribute
- **Output**: `config-change` CustomEvent with `detail: { config: {...}, valid: boolean }`

## Sidebar Integration

If [`datasette-sidebar`](https://github.com/datasette/datasette-sidebar) is installed, datasette-alerts automatically registers itself as a sidebar app.

## Development

```bash
just dev           # start dev server
just test          # run tests (uv run pytest)
just format        # format code (backend + frontend)
just check         # lint + type check (backend + frontend)
just frontend      # build frontend
just frontend-dev  # start Vite dev server
```
