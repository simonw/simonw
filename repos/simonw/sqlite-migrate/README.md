# sqlite-migrate

[![PyPI](https://img.shields.io/pypi/v/sqlite-migrate.svg)](https://pypi.org/project/sqlite-migrate/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-migrate?include_prereleases&label=changelog)](https://sqlite-migrate.datasette.io/en/stable/changelog.html)
[![Tests](https://github.com/simonw/sqlite-migrate/workflows/Test/badge.svg)](https://github.com/simonw/sqlite-migrate/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-migrate/blob/main/LICENSE)

Deprecated compatibility package for `sqlite-utils` migrations.

Migration support is now built into `sqlite-utils` 4. Install and use `sqlite-utils` directly for new projects:

```bash
pip install sqlite-utils
```

New code should import `Migrations` from `sqlite_utils`:

```python
from sqlite_utils import Migrations
```

This package depends on `sqlite-utils>=4` and re-exports that class so existing migration files can continue to use their old import:

```python
from sqlite_migrate import Migrations
```

Run migrations using the `sqlite-utils migrate` command:

```bash
sqlite-utils migrate creatures.db path/to/migrations.py
```

See the [`sqlite-utils` migrations documentation](https://sqlite-utils.datasette.io/en/stable/migrations.html) for the full Python API and CLI usage.
