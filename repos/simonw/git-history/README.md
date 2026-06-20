# git-history

[![PyPI](https://img.shields.io/pypi/v/git-history.svg)](https://pypi.org/project/git-history/)
[![Changelog](https://img.shields.io/github/v/release/simonw/git-history?include_prereleases&label=changelog)](https://github.com/simonw/git-history/releases)
[![Tests](https://github.com/simonw/git-history/workflows/Test/badge.svg)](https://github.com/simonw/git-history/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/git-history/blob/master/LICENSE)

Tools for analyzing Git history using SQLite

For background on this project see [git-history: a tool for analyzing scraped data collected using Git and SQLite](https://simonwillison.net/2021/Dec/7/git-history/).

[Measuring traffic during the Half Moon Bay Pumpkin Festival](https://simonwillison.net/2022/Oct/19/measuring-traffic/) describes a project using this tool in detail.

## Installation

Install this tool using `uv`:
```bash
uv tool install git-history
```
Or run it without installing it:
```bash
uvx git-history --help
```

## Demos

[git-history-demos.datasette.io](http://git-history-demos.datasette.io/) hosts three example databases created using this tool:

- [pge-outages](https://git-history-demos.datasette.io/pge-outages) shows a history of PG&E (the electricity supplier) [outages](https://pgealerts.alerts.pge.com/outagecenter/), using data collected in [simonw/pge-outages](https://github.com/simonw/pge-outages) converted using [pge-outages.sh](https://github.com/simonw/git-history/blob/main/demos/pge-outages.sh)
- [ca-fires](https://git-history-demos.datasette.io/ca-fires) shows a history of fires in California reported on [fire.ca.gov/incidents](https://www.fire.ca.gov/incidents/), from data in [simonw/ca-fires-history](https://github.com/simonw/ca-fires-history) converted using [ca-fires.sh](https://github.com/simonw/git-history/blob/main/demos/ca-fires.sh)

The demos are deployed using [Datasette](https://datasette.io/) on [Google Cloud Run](https://cloud.google.com/run/) by [this GitHub Actions workflow](https://github.com/simonw/git-history/blob/main/.github/workflows/deploy-demos.yml).

## Usage

This tool can be run against a Git repository that holds a file that contains JSON, CSV/TSV or some other format and which has multiple versions tracked in the Git history. Read [Git scraping: track changes over time by scraping to a Git repository](https://simonwillison.net/2020/Oct/9/git-scraping/) to understand how you might create such a repository.

The `file` command analyzes the history of an individual file within the repository, and generates a SQLite database table that represents the different versions of that file over time.

The file is assumed to contain multiple objects - for example, the results of scraping an electricity outage map or a CSV file full of records.

Assuming you have a file called `incidents.json` that is a JSON array of objects, with multiple versions of that file recorded in a repository. Each version of that file might look something like this:

```json
[
    {
        "IncidentID": "abc123",
        "Location": "Corner of 4th and Vermont",
        "Type": "fire"
    },
    {
        "IncidentID": "cde448",
        "Location": "555 West Example Drive",
        "Type": "medical"
    }
]
```

Change directory into the GitHub repository in question and run the following:

    git-history file incidents.db incidents.json

You can also analyze a remote Git repository by passing a URL to the `--repo` option. The repository will be cloned to a temporary directory before processing.

Using an HTTPS URL:

    git-history file incidents.db incidents.json \
      --repo https://github.com/example/repo

Using a git SSH URL:

    git-history file incidents.db incidents.json \
      --repo git@github.com:example/repo

When using a remote URL, the filepath argument should be a relative path within the repository (e.g. `incidents.json` or `data/incidents.json`).

This will create a new SQLite database in the `incidents.db` file with three tables:

- `commits` containing a row for every commit, with a `hash` column, the `commit_at` date and a foreign key to a `namespace`.
- `item` containing a row for every item in every version of the `filename.json` file - with an extra `_commit` column that is a foreign key back to the `commit` table.
- `namespaces` containing a single row. This allows you to build multiple tables for different files, using the `--namespace` option described below.

The database schema for this example will look like this:

<!-- [[[cog
import cog, json
from git_history import cli
from click.testing import CliRunner
from tests.test_git_history import make_repo
import sqlite_utils
import tempfile, pathlib
tmpdir = pathlib.Path(tempfile.mkdtemp())
db_path = str(tmpdir / "data.db")
make_repo(tmpdir)
runner = CliRunner()
result = runner.invoke(cli.cli, [
    "file", db_path, str(tmpdir / "repo" / "incidents.json"), "--repo", str(tmpdir / "repo")
])
cog.out("```sql\n")
cog.out(sqlite_utils.Database(db_path).schema)
cog.out("\n```")
]]] -->
```sql
CREATE TABLE [namespaces] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT
);
CREATE UNIQUE INDEX [idx_namespaces_name]
    ON [namespaces] ([name]);
CREATE TABLE [commits] (
   [id] INTEGER PRIMARY KEY,
   [namespace] INTEGER REFERENCES [namespaces]([id]),
   [hash] TEXT,
   [commit_at] TEXT
);
CREATE UNIQUE INDEX [idx_commits_namespace_hash]
    ON [commits] ([namespace], [hash]);
CREATE TABLE [item] (
   [IncidentID] TEXT,
   [Location] TEXT,
   [Type] TEXT,
   [_commit] INTEGER REFERENCES [commits]([id])
);
```
<!-- [[[end]]] -->

If you have 10 historic versions of the `incidents.json` file and each one contains 30 incidents, you will end up with 10 * 30 = 300 rows in your `item` table.

### Track the history of individual items using IDs

If your objects have a unique identifier - or multiple columns that together form a unique identifier - you can use the `--id` option to de-duplicate and track changes to each of those items over time.

This provides a much more interesting way to apply this tool.

If there is a unique identifier column called `IncidentID` you could run the following:

    git-history file incidents.db incidents.json --id IncidentID

The database schema used here is very different from the one used without the `--id` option.

If you have already imported history, the command will skip any commits that it has seen already and just process new ones. This means that even though an initial import could be slow subsequent imports should run a lot faster.

This command will create six tables - `commits`, `item`, `item_version`, `columns`, `item_changed` and `namespaces`.

Here's the full schema:

<!-- [[[cog
db_path2 = str(tmpdir / "data2.db")
result = runner.invoke(cli.cli, [
    "file", db_path2, str(tmpdir / "repo" / "incidents.json"),
    "--repo", str(tmpdir / "repo"),
    "--id", "IncidentID"
])
cog.out("```sql\n")
cog.out(sqlite_utils.Database(db_path2).schema)
cog.out("\n```")
]]] -->
```sql
CREATE TABLE [namespaces] (
   [id] INTEGER PRIMARY KEY,
   [name] TEXT
);
CREATE UNIQUE INDEX [idx_namespaces_name]
    ON [namespaces] ([name]);
CREATE TABLE [commits] (
   [id] INTEGER PRIMARY KEY,
   [namespace] INTEGER REFERENCES [namespaces]([id]),
   [hash] TEXT,
   [commit_at] TEXT
);
CREATE UNIQUE INDEX [idx_commits_namespace_hash]
    ON [commits] ([namespace], [hash]);
CREATE TABLE [item] (
   [_id] INTEGER PRIMARY KEY,
   [_item_id] TEXT
, [IncidentID] TEXT, [Location] TEXT, [Type] TEXT, [_commit] INTEGER);
CREATE UNIQUE INDEX [idx_item__item_id]
    ON [item] ([_item_id]);
CREATE TABLE [item_version] (
   [_id] INTEGER PRIMARY KEY,
   [_item] INTEGER REFERENCES [item]([_id]),
   [_version] INTEGER,
   [_commit] INTEGER REFERENCES [commits]([id]),
   [IncidentID] TEXT,
   [Location] TEXT,
   [Type] TEXT,
   [_item_full_hash] TEXT
);
CREATE TABLE [columns] (
   [id] INTEGER PRIMARY KEY,
   [namespace] INTEGER REFERENCES [namespaces]([id]),
   [name] TEXT
);
CREATE UNIQUE INDEX [idx_columns_namespace_name]
    ON [columns] ([namespace], [name]);
CREATE TABLE [item_changed] (
   [item_version] INTEGER REFERENCES [item_version]([_id]),
   [column] INTEGER REFERENCES [columns]([id]),
   PRIMARY KEY ([item_version], [column])
);
CREATE VIEW item_version_detail AS select
  commits.commit_at as _commit_at,
  commits.hash as _commit_hash,
  item_version.*,
  (
    select json_group_array(name) from columns
    where id in (
      select column from item_changed
      where item_version = item_version._id
    )
) as _changed_columns
from item_version
  join commits on commits.id = item_version._commit;
CREATE INDEX [idx_item_version__item]
    ON [item_version] ([_item]);
```
<!-- [[[end]]] -->

#### item table

The `item` table will contain the most recent version of each row, de-duplicated by ID, plus the following additional columns:

- `_id` - a numeric integer primary key, used as a foreign key from the `item_version` table.
- `_item_id` - a hash of the values of the columns specified using the `--id` option to the command. This is used for de-duplication when processing new versions.
- `_commit` - a foreign key to the `commit` table, representing the most recent commit to modify this item.

#### item_version table

The `item_version` table will contain a row for each captured differing version of that item, plus the following columns:

- `_id` - a numeric ID for the item version record.
- `_item` - a foreign key to the `item` table.
- `_version` - the numeric version number, starting at 1 and incrementing for each captured version.
- `_commit` - a foreign key to the `commit` table.
- `_item_full_hash` - a hash of this version of the item. This is used internally by the tool to identify items that have changed between commits.

The other columns in this table represent columns in the original data that have changed since the previous version. If the value has not changed, it will be represented by a `null`.

If a value was previously set but has been changed back to `null` it will still be represented as `null` in the `item_version` row. You can identify these using the `item_changed` many-to-many table described below.

You can use the `--full-versions` option to store full copies of the item at each version, rather than just storing the columns that have changed.

#### item_version_detail view

This SQL view joins `item_version` against `commits` to add three further columns: `_commit_at` with the date of the commit, and `_commit_hash` with the Git commit hash.

#### item_changed

This many-to-many table indicates exactly which columns were changed in an `item_version`.

- `item_version` is a foreign key to a row in the `item_version` table.
- `column` is a foreign key to a row in the `columns` table.

This table with have the largest number of rows, which is why it stores just two integers in order to save space.

#### columns

The `columns` table stores column names. It is referenced by `item_changed`.

- `id` - an integer ID.
- `name` - the name of the column.
- `namespace` - a foreign key to `namespaces`, for if multiple file histories are sharing the same database.

#### Reserved column names

<!-- [[[cog
from git_history.utils import RESERVED
cog.out("Note that ")
cog.out(", ".join("`{}`".format(r) for r in RESERVED))
cog.out(" are considered reserved column names for the purposes of this tool.")
]]] -->
Note that `_id`, `_item_full_hash`, `_item`, `_item_id`, `_version`, `_commit`, `_item_id`, `_commit_at`, `_commit_hash`, `_changed_columns`, `rowid` are considered reserved column names for the purposes of this tool.
<!-- [[[end]]] -->

If your data contains any of these they will be renamed to add a trailing underscore, for example `_id_`, `_item_`, `_version_`, to avoid clashing with the reserved columns.

If you have a column with a name such as `_commit_` it will be renamed too, adding an additional trailing underscore, so `_commit_` becomes `_commit__` and `_commit__` becomes `_commit___`.

### Additional options

- `--repo DIRECTORY_OR_URL` - the path to the Git repository, or a URL to clone. If not specified, uses the current working directory. URLs can be HTTPS (e.g. `https://github.com/user/repo`) or SSH (e.g. `git@github.com:user/repo`).
- `--branch TEXT` - the Git branch to analyze - defaults to `main`.
- `--id TEXT` - as described above: pass one or more columns that uniquely identify a record, so that changes to that record can be calculated over time.
- `--full-versions` - instead of recording just the columns that have changed in the `item_version` table record a full copy of each version of theh item.
- `--ignore TEXT` - one or more columns to ignore - they will not be included in the resulting database.
- `--csv` - treat the data is CSV or TSV rather than JSON, and attempt to guess the correct dialect
- `--dialect` - use a spcific CSV dialect. Options are `excel`, `excel-tab` and `unix` - see [the Python CSV documentation](https://docs.python.org/3/library/csv.html#csv.excel) for details.
- `--encoding` - character encoding to use when reading CSV files. Defaults to `utf-8`. Use this for files encoded in other formats such as `latin-1` or `utf-16`.
- `--skip TEXT` - one or more full Git commit hashes that should be skipped. You can use this if some of the data in your revision history is corrupted in a way that prevents this tool from working.
- `--start-at TEXT` - skip commits prior to the specified commit hash.
- `--start-after TEXT` - skip commits up to and including the specified commit hash, then start processing from the following commit.
- `--convert TEXT` - custom Python code for a conversion, described below.
- `--import TEXT` - additional Python modules to import for `--convert`.
- `--ignore-duplicate-ids` - if a single version of a file has the same ID in it more than once, the tool will exit with an error. Use this option to ignore this and instead pick just the first of the two duplicates.
- `--namespace TEXT` - use this if you wish to include the history of multiple different files in the same database. The default is `item` but you can set it to something else, which will produce tables with names like `yournamespace` and `yournamespace_version`.
- `--wal` - Enable WAL mode on the created database file. Use this if you plan to run queries against the database while `git-history` is creating it.
- `--silent` - don't show the progress bar.

### CSV and TSV data

If the data in your repository is a CSV or TSV file you can process it by adding the `--csv` option. This will attempt to detect which delimiter is used by the file, so the same option works for both comma- and tab-separated values.

    git-history file trees.db trees.csv --id TreeID

You can also specify the CSV dialect using the `--dialect` option.

### Custom conversions using --convert

If your data is not already either CSV/TSV or a flat JSON array, you can reshape it using the `--convert` option.

The format needed by this tool is an array of dictionaries, as demonstrated by the `incidents.json` example above.

If your data does not fit this shape, you can provide a snippet of Python code to converts the on-disk content of each stored file into a Python list of dictionaries.

For example, if your stored files each look like this:

```json
{
    "incidents": [
        {
            "id": "552",
            "name": "Hawthorne Fire",
            "engines": 3
        },
        {
            "id": "556",
            "name": "Merlin Fire",
            "engines": 1
        }
    ]
}
```
You could use the following Python snippet to convert them to the required format:

```python
json.loads(content)["incidents"]
```
(The `json` module is exposed to your custom function by default.)

You would then run the tool like this:

    git-history file database.db incidents.json \
      --id id \
      --convert 'json.loads(content)["incidents"]'

The `content` variable is always a `bytes` object representing the content of the file at a specific moment in the repository's history.

You can import additional modules using `--import`. This example shows how you could read a CSV file that uses `;` as the delimiter:

    git-history file trees.db ../sf-tree-history/Street_Tree_List.csv \
      --repo ../sf-tree-history \
      --import csv \
      --import io \
      --convert '
        fp = io.StringIO(content.decode("utf-8"))
        return list(csv.DictReader(fp, delimiter=";"))
        ' \
      --id TreeID

You can import nested modules such as [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)  using `--import xml.etree.ElementTree`, then refer to them in your function body as `xml.etree.ElementTree`. For example, if your tracked data was in an `items.xml` file that looked like this:

```xml
<items>
  <item id="1" name="One" />
  <item id="2" name="Two" />
  <item id="3" name="Three" />
</item>
```
You could load it using the following `--convert` script:
```
git-history file items.xml --convert '
tree = xml.etree.ElementTree.fromstring(content)
return [el.attrib for el in tree.iter("item")]
' --import xml.etree.ElementTree --id id
```

If your Python code spans more than one line it needs to include a `return` statement.

You can also use Python generators in your `--convert` code, for example:

    git-history file stats.db package-stats/stats.json \
        --repo package-stats \
        --convert '
        data = json.loads(content)
        for key, counts in data.items():
            for date, count in counts.items():
                yield {
                    "package": key,
                    "date": date,
                    "count": count
                }
        ' --id package --id date

This conversion function expects data that looks like this:

```json
{
    "airtable-export": {
        "2021-05-18": 66,
        "2021-05-19": 60,
        "2021-05-20": 87
    }
}
```

## Development

To contribute to this tool, first checkout the code. You can run the tests using `uv run`:
```bash
cd git-history
uv run pytest
```
And run your local development copy of the tool like this
```bash
uv run git-history --help
```
To update the schema examples in this README file:
```bash
uv run cog -r README.md
```
