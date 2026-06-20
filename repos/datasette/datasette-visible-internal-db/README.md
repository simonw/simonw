# datasette-visible-internal-db

[![PyPI](https://img.shields.io/pypi/v/datasette-visible-internal-db.svg)](https://pypi.org/project/datasette-visible-internal-db/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-visible-internal-db?include_prereleases&label=changelog)](https://github.com/datasette/datasette-visible-internal-db/releases)
[![Tests](https://github.com/datasette/datasette-visible-internal-db/workflows/Test/badge.svg)](https://github.com/datasette/datasette-visible-internal-db/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-visible-internal-db/blob/main/LICENSE)

Datasette plugin for making the internal database visible for debugging

Datasette 1.0a5 made [the internal database](https://docs.datasette.io/en/1.0a5/internals.html#datasette-s-internal-database) no longer visible through the Datasette interface.

This plugin brings it back, for debugging purposes.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-visible-internal-db
```

The internal database will now be publicly visible at `/_internal` in your Datasette instance.

## Controlling access to the internal database

You can use Datasette's [permissions mechanism](https://docs.datasette.io/en/stable/authentication.html#permissions) to control who is allowed to interact with the internal database.

To restrict access to just the `root` actor, drop this into your configuration:

```yaml
databases:
  _internal:
    allow:
      id: root
```
