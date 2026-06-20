# datasette-cron

[![PyPI](https://img.shields.io/pypi/v/datasette-cron.svg)](https://pypi.org/project/datasette-cron/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-cron?include_prereleases&label=changelog)](https://github.com/datasette/datasette-cron/releases)
[![Tests](https://github.com/datasette/datasette-cron/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-cron/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-cron/blob/main/LICENSE)

Database-backed scheduled tasks for Datasette.

Plugins can register handler functions, then create tasks that run on a
schedule. Tasks persist across restarts, support cron expressions and intervals,
and record execution history.

## Installation

```bash
pip install datasette-cron
```

## Quick Start

A plugin registers a handler function and creates a task that runs on a
schedule:

```python
from datasette import hookimpl

@hookimpl
def cron_register_handlers(datasette):
    async def my_handler(datasette, config):
        db = datasette.get_database(config["database"])
        await db.execute_write("INSERT INTO log (message) VALUES ('tick')")

    return {"my-handler": my_handler}

@hookimpl
def startup(datasette):
    async def inner():
        scheduler = datasette._cron_scheduler
        await scheduler.add_task(
            name="log-every-minute",
            handler="myplugin:my-handler",
            schedule={"interval": 60},
            config={"database": "mydb"},
        )
    return inner
```

## How It Works

1. **Startup**: datasette-cron creates a `Scheduler` at
   `datasette._cron_scheduler` and collects handlers from all plugins via the
   `cron_register_handlers` hook
2. **First request**: The scheduler loop starts (via `asgi_wrapper`), ticking
   every ~1 second
3. **Each tick**: Queries `datasette_cron_tasks` for tasks where
   `next_run_at <= now` and `enabled = 1`
4. **Execution**: Looks up the handler function, calls it with
   `(datasette, config)`, records the result in `datasette_cron_runs`
5. **Next run**: Advances `next_run_at` based on the schedule

## Plugin Hook

### `cron_register_handlers(datasette)`

Return a dict mapping handler names to callable functions:

```python
@hookimpl
def cron_register_handlers(datasette):
    return {
        "check-feeds": check_feeds_handler,
        "cleanup": cleanup_handler,
    }
```

Handlers are registered with a plugin-derived prefix. If your plugin module is
`datasette_myplugin`, handlers are accessible as `myplugin:check-feeds` and
`myplugin:cleanup`.

### Handler Signature

```python
async def my_handler(datasette, config):
    """
    datasette: the Datasette instance
    config: dict from the task's config field
    """
    pass
```

Handlers can be sync or async.

## Scheduler API

Access the scheduler via `datasette._cron_scheduler` after startup.

### `add_task()`

Create or update a task (idempotent upsert). If the task already exists,
`next_run_at` is preserved.

```python
await scheduler.add_task(
    name="my-task",
    handler="myplugin:my-handler",
    schedule={"interval": 300},          # every 5 minutes
    config={"key": "value"},             # passed to handler
    timezone="America/New_York",         # optional
    overlap="skip",                      # "skip" prevents overlapping runs
    retry={"max_retries": 3, "backoff": "exponential"},
)
```

### Schedule Types

**Interval** (seconds):

```python
schedule={"interval": 60}        # every 60 seconds
schedule={"interval": 1}         # every second
```

**Cron expression**:

```python
schedule="0 8 * * *"             # daily at 8am
schedule="*/5 * * * *"           # every 5 minutes
```

**RFC 5545 RRULE**:

```python
schedule={"rrule": "FREQ=WEEKLY;BYDAY=MO"}
```

### Other Methods

```python
await scheduler.remove_task("my-task")
await scheduler.trigger_task("my-task")       # run immediately
await scheduler.enable_task("my-task")
await scheduler.disable_task("my-task")
await scheduler.update_task("my-task", schedule={"interval": 10})
```

## Data Models

Query results from `InternalDB` return typed dataclasses:

```python
from datasette_cron.models import CronTask, CronRun

task: CronTask = await scheduler.internal_db.get_task("my-task")
print(task.name, task.handler, task.next_run_at, task.last_status)

runs: list[CronRun] = await scheduler.internal_db.get_runs("my-task")
for run in runs:
    print(run.started_at, run.status, run.duration_ms)
```

### `CronTask`

| Field             | Type          | Description                                       |
| ----------------- | ------------- | ------------------------------------------------- |
| `name`            | `str`         | Unique task identifier                            |
| `handler`         | `str`         | Handler reference (e.g., `"myplugin:my-handler"`) |
| `config`          | `dict`        | JSON config passed to handler                     |
| `schedule_type`   | `str`         | `"interval"`, `"cron"`, or `"rrule"`              |
| `schedule_config` | `str`         | JSON schedule parameters                          |
| `timezone`        | `str \| None` | IANA timezone                                     |
| `overlap_policy`  | `str`         | `"skip"` or `"allow"`                             |
| `retry_max`       | `int`         | Max retry attempts                                |
| `retry_backoff`   | `str`         | `"exponential"` or `"linear"`                     |
| `enabled`         | `bool`        | Whether task is active                            |
| `next_run_at`     | `str \| None` | ISO timestamp of next scheduled run               |
| `last_run_at`     | `str \| None` | ISO timestamp of last run                         |
| `last_status`     | `str \| None` | `"success"` or `"error"`                          |

### `CronRun`

| Field           | Type          | Description                            |
| --------------- | ------------- | -------------------------------------- |
| `id`            | `int`         | Auto-increment ID                      |
| `task_name`     | `str`         | Which task this run belongs to         |
| `started_at`    | `str`         | ISO timestamp                          |
| `finished_at`   | `str \| None` | ISO timestamp                          |
| `status`        | `str`         | `"running"`, `"success"`, or `"error"` |
| `error_message` | `str \| None` | Error details on failure               |
| `attempt`       | `int`         | Retry attempt number                   |
| `duration_ms`   | `int \| None` | Execution time in milliseconds         |

## REST API

| Method | Endpoint                           | Description           |
| ------ | ---------------------------------- | --------------------- |
| GET    | `/-/api/cron/tasks`                | List all tasks        |
| GET    | `/-/api/cron/tasks/{name}`         | Task detail           |
| GET    | `/-/api/cron/tasks/{name}/runs`    | Run history           |
| POST   | `/-/api/cron/tasks/{name}/trigger` | Trigger immediate run |
| POST   | `/-/api/cron/tasks/{name}/enable`  | Enable/disable task   |

All endpoints require the `datasette-cron-access` permission.

## Database Tables

Stored in Datasette's internal database:

**`datasette_cron_tasks`** — task definitions and scheduling state

**`datasette_cron_runs`** — execution history with timing, status, and errors

## Development

```bash
just dev           # start dev server
just test          # run tests
just format        # format code (backend + frontend)
just check         # lint + type check (backend + frontend)
```
