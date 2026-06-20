# claude-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/claude-to-sqlite.svg)](https://pypi.org/project/claude-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/claude-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/claude-to-sqlite/releases)
[![Tests](https://github.com/simonw/claude-to-sqlite/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/claude-to-sqlite/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/claude-to-sqlite/blob/master/LICENSE)

Convert a [Claude.ai](https://claude.ai/) export to SQLite

## Installation

Install this tool using `pip`:
```bash
pip install claude-to-sqlite
```
## Usage

Start by [exporting your Claude data](https://support.anthropic.com/en/articles/9450526-how-can-i-export-my-claude-ai-data). You will be emailed a link to a zip file (though it may be missing the `.zip` extension).

Run the command like this:

```bash
claude-to-sqlite claude-export.zip claude.db
```
Now `claude.db` will be a SQLite containing the `conversations` and `messages` from your Claude export.

You can explore that using [Datasette](https://datasette.io/):

```bash
datasette claude.db
```
## Database schema

Assuming the Claude export JSON has not changed since this tool was last released on 20th October 2024 the database tables should look like this:

<!-- [[[cog
import tempfile, pathlib, sqlite_utils
from click.testing import CliRunner
from claude_to_sqlite import cli

tmpdir = pathlib.Path(tempfile.mkdtemp())
db_path = str(tmpdir / "claude.db")
runner = CliRunner()
runner.invoke(cli.cli, ["tests/artifacts.json", db_path])
cog.out("```sql\n")
schema = sqlite_utils.Database(db_path).schema
cog.out(schema)
cog.out("\n```")
]]] -->
```sql
CREATE TABLE [conversations] (
   [uuid] TEXT PRIMARY KEY,
   [name] TEXT,
   [created_at] TEXT,
   [updated_at] TEXT,
   [account_id] TEXT
);
CREATE TABLE [messages] (
   [uuid] TEXT PRIMARY KEY,
   [text] TEXT,
   [sender] TEXT,
   [created_at] TEXT,
   [updated_at] TEXT,
   [attachments] TEXT,
   [files] TEXT,
   [conversation_id] TEXT REFERENCES [conversations]([uuid])
);
CREATE TABLE [artifacts] (
   [id] TEXT PRIMARY KEY,
   [artifact] TEXT,
   [identifier] TEXT,
   [version] INTEGER,
   [type] TEXT,
   [language] TEXT,
   [title] TEXT,
   [content] TEXT,
   [thinking] TEXT,
   [conversation_id] TEXT REFERENCES [conversations]([uuid]),
   [message_id] TEXT REFERENCES [messages]([uuid])
);
```
<!-- [[[end]]] -->

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd claude-to-sqlite
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
