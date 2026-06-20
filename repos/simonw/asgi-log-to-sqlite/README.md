# asgi-log-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/asgi-log-to-sqlite.svg)](https://pypi.org/project/asgi-log-to-sqlite/)
[![CircleCI](https://circleci.com/gh/simonw/asgi-log-to-sqlite.svg?style=svg)](https://circleci.com/gh/simonw/asgi-log-to-sqlite)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/asgi-log-to-sqlite/blob/master/LICENSE)

ASGI middleware for logging traffic to a SQLite database

See [Logging to SQLite using ASGI middleware](https://simonwillison.net/2019/Dec/16/logging-sqlite-asgi-middleware/) for background on this project.

## Installation

    pip install asgi-log-to-sqlite

## Usage

```python
from asgi_log_to_sqlite import AsgiLogToSqlite
from my_asgi_app import app


app = AsgiLogToSqlite(app, "/tmp/log.db")
```

Requests to your ASGI app will now be logged to the SQLite database file at `/tmp/log.db`.

## Schema

The database used to log requests has one key table - `requests` - and 6 lookup tables: `paths`, `user_agents`, `referers`, `accept_languages`, `content_types` and `query_strings`.

The full schema is as follows:

```sql
CREATE TABLE [paths] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT
);
CREATE UNIQUE INDEX idx_paths_name
                ON paths (name);
CREATE TABLE [user_agents] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT
);
CREATE UNIQUE INDEX idx_user_agents_name
                ON user_agents (name);
CREATE TABLE [referers] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT
);
CREATE UNIQUE INDEX idx_referers_name
                ON referers (name);
CREATE TABLE [accept_languages] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT
);
CREATE UNIQUE INDEX idx_accept_languages_name
                ON accept_languages (name);
CREATE TABLE [content_types] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT
);
CREATE UNIQUE INDEX idx_content_types_name
                ON content_types (name);
CREATE TABLE [query_strings] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT
);
CREATE UNIQUE INDEX idx_query_strings_name
                ON query_strings (name);
CREATE TABLE [requests] (
   [start] FLOAT,
   [method] TEXT,
   [path] INTEGER REFERENCES [paths]([id]),
   [query_string] INTEGER REFERENCES [query_strings]([id]),
   [user_agent] INTEGER REFERENCES [user_agents]([id]),
   [referer] INTEGER REFERENCES [referers]([id]),
   [accept_language] INTEGER REFERENCES [accept_languages]([id]),
   [http_status] INTEGER,
   [content_type] INTEGER REFERENCES [content_types]([id]),
   [client_ip] TEXT,
   [duration] FLOAT,
   [body_size] INTEGER
);
```
