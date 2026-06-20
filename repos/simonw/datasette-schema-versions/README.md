# datasette-schema-versions

[![PyPI](https://img.shields.io/pypi/v/datasette-schema-versions.svg)](https://pypi.org/project/datasette-schema-versions/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-schema-versions?include_prereleases&label=changelog)](https://github.com/simonw/datasette-schema-versions/releases)
[![Tests](https://github.com/simonw/datasette-schema-versions/workflows/Test/badge.svg)](https://github.com/simonw/datasette-schema-versions/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-schema-versions/blob/main/LICENSE)

Datasette plugin that shows the schema version of every attached database

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-schema-versions
```
## Usage

Visit `/-/schema-versions` on your Datasette instance to see a numeric version for the schema for each of your databases.

Any changes you make to the schema will increase this version number.
