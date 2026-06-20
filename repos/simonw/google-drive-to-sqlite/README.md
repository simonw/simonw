# google-drive-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/google-drive-to-sqlite.svg)](https://pypi.org/project/google-drive-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/google-drive-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/google-drive-to-sqlite/releases)
[![Tests](https://github.com/simonw/google-drive-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/google-drive-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/google-drive-to-sqlite/blob/master/LICENSE)

> [!WARNING]  
> This tool no longer works due to Google deprecating the authentication mechanism it uses. See [issue #40](https://github.com/simonw/google-drive-to-sqlite/issues/40).

Create a SQLite database containing metadata from [Google Drive](https://www.google.com/drive)

For background on this project, see [Google Drive to SQLite](https://simonwillison.net/2022/Feb/20/google-drive-to-sqlite/) on my blog.

If you use Google Drive, and especially if you have shared drives with other people there's a good chance you have hundreds or even thousands of files that you may not be fully aware of.

This tool can download metadata about those files - their names, sizes, folders, content types, permissions, creation dates and more - and store them in a SQLite database.

This lets you use SQL to analyze your Google Drive contents, using [Datasette](https://datasette.io/) or the SQLite command-line tool or any other SQLite database browsing software.

## Installation

Install this tool using `pip`:

    pip install google-drive-to-sqlite

## Quickstart

Authenticate with Google Drive by running:

    google-drive-to-sqlite auth

Now create a SQLite database with metadata about all of the files you have starred using:

    google-drive-to-sqlite files starred.db --starred

You can explore the resulting database using [Datasette](https://datasette.io/):

    $ pip install datasette
    $ datasette starred.db
    INFO:     Started server process [24661]
    INFO:     Uvicorn running on http://127.0.0.1:8001

## Authentication

> :warning: **This application has not yet been verified by Google** - you may find you are unable to authenticate until that verification is complete. [#10](https://github.com/simonw/google-drive-to-sqlite/issues/10)
>
> You can work around this issue by [creating your own OAuth client ID key](https://til.simonwillison.net/googlecloud/google-oauth-cli-application) and passing it to the `auth` command using `--google-client-id` and `--google-client-secret`.

First, authenticate with Google Drive using the `auth` command:

    $ google-drive-to-sqlite auth
    Visit the following URL to authenticate with Google Drive

    https://accounts.google.com/o/oauth2/v2/auth?...

    Then return here and paste in the resulting code:
    Paste code here: 

Follow the link, sign in with Google Drive and then copy and paste the resulting code back into the tool.

This will save an authentication token to the file called `auth.json` in the current directory.

To specify a different location for that file, use the `--auth` option:

    google-drive-to-sqlite auth --auth ~/google-drive-auth.json

The `auth` command also provides options for using a different scope, Google client ID and Google client secret. You can use these to create your own custom authentication tokens that can work with other Google APIs, see [issue #5](https://github.com/simonw/google-drive-to-sqlite/issues/5) for details.

Full `--help`:

<!-- [[[cog
import cog
from google_drive_to_sqlite import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["auth", "--help"])
help = result.output.replace("Usage: cli", "Usage: google-drive-to-sqlite")
cog.out(
    "```\n{}\n```\n".format(help)
)
]]] -->
```
Usage: google-drive-to-sqlite auth [OPTIONS]

  Authenticate user and save credentials

Options:
  -a, --auth FILE              Path to save token, defaults to auth.json
  --google-client-id TEXT      Custom Google client ID
  --google-client-secret TEXT  Custom Google client secret
  --scope TEXT                 Custom token scope
  --help                       Show this message and exit.

```
<!-- [[[end]]] -->

To revoke the token that is stored in `auth.json`, such that it cannot be used to access Google Drive in the future, run the `revoke` command:

    google-drive-to-sqlite revoke

Or if your token is stored in another location:

    google-drive-to-sqlite revoke -a ~/google-drive-auth.json

You will need to obtain a fresh token using the `auth` command in order to continue using this tool.

## google-drive-to-sqlite files

To retrieve metadata about the files in your Google Drive, or a folder or search within it, use the `google-drive-to-sqlite files` command.

This will default to writing details about every file in your Google Drive to a SQLite database:

    google-drive-to-sqlite files files.db

Files and folders will be written to databases tables, which will be created if they do not yet exist. The database schema is [shown below](#database-schema).

If a file or folder already exists, based on a matching `id`, it will be replaced with fresh data.

Instead of writing to SQLite you can use `--json` to output as JSON, or `--nl` to output as newline-delimited JSON:

    google-drive-to-sqlite files --nl

Use `--folder ID` to retrieve everything in a specified folder and its sub-folders:

    google-drive-to-sqlite files files.db --folder 1E6Zg2X2bjjtPzVfX8YqdXZDCoB3AVA7i

Use `--q QUERY` to use a [custom search query](https://developers.google.com/drive/api/v3/reference/query-ref):

    google-drive-to-sqlite files files.db -q "viewedByMeTime > '2022-01-01'"

The following shortcut options help build queries:

- `--full-text TEXT` to search for files where the full text matches a search term
- `--starred` for files and folders you have starred
- `--trashed` for files and folders in the trash
- `--shared-with-me` for files and folders that have been shared with you
- `--apps` for Google Apps documents, spreadsheets, presentations and drawings (equivalent to setting all  of the next four options)
- `--docs` for Google Apps documents
- `--sheets` for Google Apps spreadsheets
- `--presentations` for Google Apps presentations
- `--drawings` for Google Apps drawings

You can combine these - for example, this returns all files that you have starred and that were shared with you:

    google-drive-to-sqlite files highlights.db \
      --starred --shared-with-me

Multiple options are treated as AND, with the exception of the Google Apps options which are treated as OR - so the following would retrieve all spreadsheets and presentations that have also been starred:

    google-drive-to-sqlite files highlights.db \
      --starred --sheets --presentations

You can use `--stop-after X` to stop after retrieving X files, useful for trying out a new search pattern and seeing results straight away.

The `--import-json` and `--import-nl` options are mainly useful for testing and developing this tool. They allow you to replay the JSON or newline-delimited JSON that was previously fetched using `--json` or `--nl` and use it to create a fresh SQLite database, without needing to make any outbound API calls:

    # Fetch all starred files from the API, write to starred.json
    google-drive-to-sqlite files -q 'starred = true' --json > starred.json
    # Now import that data into a new SQLite database file
    google-drive-to-sqlite files starred.db --import-json starred.json

Full `--help`:

<!-- [[[cog
result = runner.invoke(cli.cli, ["files", "--help"])
help = result.output.replace("Usage: cli", "Usage: google-drive-to-sqlite")
cog.out(
    "```\n{}\n```\n".format(help)
)
]]] -->
```
Usage: google-drive-to-sqlite files [OPTIONS] [DATABASE]

  Retrieve metadata for files in Google Drive, and write to a SQLite database or
  output as JSON.

      google-drive-to-sqlite files files.db

  Use --json to output JSON, --nl for newline-delimited JSON:

      google-drive-to-sqlite files files.db --json

  Use a folder ID to recursively fetch every file in that folder and its sub-
  folders:

      google-drive-to-sqlite files files.db --folder
      1E6Zg2X2bjjtPzVfX8YqdXZDCoB3AVA7i

  Fetch files you have starred:

      google-drive-to-sqlite files starred.db --starred

Options:
  -a, --auth FILE       Path to auth.json token file
  --folder TEXT         Files in this folder ID and its sub-folders
  -q TEXT               Files matching this query
  --full-text TEXT      Search for files with text match
  --starred             Files you have starred
  --trashed             Files in the trash
  --shared-with-me      Files that have been shared with you
  --apps                Google Apps docs, spreadsheets, presentations and
                        drawings
  --docs                Google Apps docs
  --sheets              Google Apps spreadsheets
  --presentations       Google Apps presentations
  --drawings            Google Apps drawings
  --json                Output JSON rather than write to DB
  --nl                  Output newline-delimited JSON rather than write to DB
  --stop-after INTEGER  Stop paginating after X results
  --import-json FILE    Import from this JSON file instead of the API
  --import-nl FILE      Import from this newline-delimited JSON file
  -v, --verbose         Send verbose output to stderr
  --help                Show this message and exit.

```
<!-- [[[end]]] -->

## google-drive-to-sqlite download FILE_ID

The `download` command can be used to download files from Google Drive.

You'll need one or more file IDs, which look something like `0B32uDVNZfiEKLUtIT1gzYWN2NDI4SzVQYTFWWWxCWUtvVGNB`.

To download the file, run this:

    google-drive-to-sqlite download 0B32uDVNZfiEKLUtIT1gzYWN2NDI4SzVQYTFWWWxCWUtvVGNB

This will detect the content type of the file and use that as the extension - so if this file is a JPEG the file would be downloaded as:

    0B32uDVNZfiEKLUtIT1gzYWN2NDI4SzVQYTFWWWxCWUtvVGNB.jpeg

You can pass multiple file IDs to the command at once.

To hide the progress bar and filename output, use `-s` or `--silent`.

If you are downloading a single file you can use the `-o` output to specify a filename and location:

    google-drive-to-sqlite download 0B32uDVNZfiEKLUtIT1gzYWN2NDI4SzVQYTFWWWxCWUtvVGNB \
      -o my-image.jpeg

Use `-o -` to write the file contents to standard output:

    google-drive-to-sqlite download 0B32uDVNZfiEKLUtIT1gzYWN2NDI4SzVQYTFWWWxCWUtvVGNB \
      -o - > my-image.jpeg

Full `--help`:

<!-- [[[cog
result = runner.invoke(cli.cli, ["download", "--help"])
help = result.output.replace("Usage: cli", "Usage: google-drive-to-sqlite")
cog.out(
    "```\n{}\n```\n".format(help)
)
]]] -->
```
Usage: google-drive-to-sqlite download [OPTIONS] FILE_IDS...

  Download one or more files to disk, based on their file IDs.

  The file content will be saved to a file with the name:

      FILE_ID.ext

  Where the extension is automatically picked based on the type of file.

  If you are downloading a single file you can specify a filename with -o:

      google-drive-to-sqlite download MY_FILE_ID -o myfile.txt

Options:
  -a, --auth FILE    Path to auth.json token file
  -o, --output FILE  File to write to, or - for standard output
  -s, --silent       Hide progress bar and filename
  --help             Show this message and exit.

```
<!-- [[[end]]] -->

## google-drive-to-sqlite export FORMAT FILE_ID

The `export` command can be used to export Google Docs documents, spreadsheets and presentations in a number of different formats.

You'll need one or more document IDs, which look something like `10BOHGDUYa7lBjUSo26YFCHTpgEmtXabdVFaopCTh1vU`. You can find these by looking at the URL of your document on the Google Docs site.

To export that document as PDF, run this:

    google-drive-to-sqlite export pdf 10BOHGDUYa7lBjUSo26YFCHTpgEmtXabdVFaopCTh1vU

The file will be exported as:

    10BOHGDUYa7lBjUSo26YFCHTpgEmtXabdVFaopCTh1vU-export.pdf

You can pass multiple file IDs to the command at once.

For the `FORMAT` option you can use any of the mime type options listed [on this page](https://developers.google.com/drive/api/v3/ref-export-formats) - for example, to export as an Open Office document you could use:

    google-drive-to-sqlite export \
     application/vnd.oasis.opendocument.text \
     10BOHGDUYa7lBjUSo26YFCHTpgEmtXabdVFaopCTh1vU

For convenience the following shortcuts for common file formats are provided:

- Google Docs: `html`, `txt`, `rtf`, `pdf`, `doc`, `zip`, `epub`
- Google Sheets: `xls`, `pdf`, `csv`, `tsv`, `zip`
- Presentations: `ppt`, `pdf`, `txt`
- Drawings: `jpeg`, `png`, `svg`

The `zip` option returns a zip file of HTML. `txt` returns plain text. The others should be self-evident.

To hide the filename output, use `-s` or `--silent`.

If you are exporting a single file you can use the `-o` output to specify a filename and location:

    google-drive-to-sqlite export pdf 10BOHGDUYa7lBjUSo26YFCHTpgEmtXabdVFaopCTh1vU \
      -o my-document.pdf

Use `-o -` to write the file contents to standard output:

    google-drive-to-sqlite export pdf 10BOHGDUYa7lBjUSo26YFCHTpgEmtXabdVFaopCTh1vU \
      -o - > my-document.pdf

Full `--help`:

<!-- [[[cog
result = runner.invoke(cli.cli, ["export", "--help"])
help = result.output.replace("Usage: cli", "Usage: google-drive-to-sqlite")
cog.out(
    "```\n{}\n```\n".format(help)
)
]]] -->
```
Usage: google-drive-to-sqlite export [OPTIONS] FORMAT FILE_IDS...

  Export one or more files to the specified format.

  Usage:

      google-drive-to-sqlite export pdf FILE_ID_1 FILE_ID_2

  The file content will be saved to a file with the name:

      FILE_ID-export.ext

  Where the extension is based on the format you specified.

  Available export formats can be seen here:
  https://developers.google.com/drive/api/v3/ref-export-formats

  Or you can use one of the following shortcuts:

  - Google Docs: html, txt, rtf, pdf, doc, zip, epub
  - Google Sheets: xls, pdf, csv, tsv, zip
  - Presentations: ppt, pdf, txt
  - Drawings: jpeg, png, svg

  "zip" returns a zip file of HTML.

  If you are exporting a single file you can specify a filename with -o:

      google-drive-to-sqlite export zip MY_FILE_ID -o myfile.zip

Options:
  -a, --auth FILE    Path to auth.json token file
  -o, --output FILE  File to write to, or - for standard output
  -s, --silent       Hide progress bar and filename
  --help             Show this message and exit.

```
<!-- [[[end]]] -->

## google-drive-to-sqlite get URL

The `get` command makes authenticated requests to the specified URL, using credentials derived from the `auth.json` file.

For example:

    $ google-drive-to-sqlite get 'https://www.googleapis.com/drive/v3/about?fields=*'
    {
        "kind": "drive#about",
        "user": {
            "kind": "drive#user",
            "displayName": "Simon Willison",
    # ...

If the resource you are fetching supports pagination you can use `--paginate key` to paginate through all of the rows in a specified key. For example, the following API has a `nextPageToken` key and a `files` list, suggesting it supports pagination:

    $ google-drive-to-sqlite get https://www.googleapis.com/drive/v3/files
    {
        "kind": "drive#fileList",
        "nextPageToken": "~!!~AI9...wogHHYlc=",
        "incompleteSearch": false,
        "files": [
            {
                "kind": "drive#file",
                "id": "1YEsITp_X8PtDUJWHGM0osT-TXAU1nr0e7RSWRM2Jpyg",
                "name": "Title of a spreadsheet",
                "mimeType": "application/vnd.google-apps.spreadsheet"
            },

To paginate through everything in the `files` list you would use `--paginate files` like this:

    $ google-drive-to-sqlite get https://www.googleapis.com/drive/v3/files --paginate files
    [
      {
        "kind": "drive#file",
        "id": "1YEsITp_X8PtDUJWHGM0osT-TXAU1nr0e7RSWRM2Jpyg",
        "name": "Title of a spreadsheet",
        "mimeType": "application/vnd.google-apps.spreadsheet"
      },
      # ...

Add `--nl` to stream paginated data as newline-delimited JSON:

    $ google-drive-to-sqlite get https://www.googleapis.com/drive/v3/files --paginate files --nl
    {"kind": "drive#file", "id": "1YEsITp_X8PtDUJWHGM0osT-TXAU1nr0e7RSWRM2Jpyg", "name": "Title of a spreadsheet", "mimeType": "application/vnd.google-apps.spreadsheet"}
    {"kind": "drive#file", "id": "1E6Zg2X2bjjtPzVfX8YqdXZDCoB3AVA7i", "name": "Subfolder", "mimeType": "application/vnd.google-apps.folder"}

Add `--stop-after 5` to stop after 5 records - useful for testing.

Full `--help`:

<!-- [[[cog
result = runner.invoke(cli.cli, ["get", "--help"])
help = result.output.replace("Usage: cli", "Usage: google-drive-to-sqlite")
cog.out(
    "```\n{}\n```\n".format(help)
)
]]] -->
```
Usage: google-drive-to-sqlite get [OPTIONS] URL

  Make an authenticated HTTP GET to the specified URL

Options:
  -a, --auth FILE       Path to auth.json token file
  --paginate TEXT       Paginate through all results in this key
  --nl                  Output paginated data as newline-delimited JSON
  --stop-after INTEGER  Stop paginating after X results
  -v, --verbose         Send verbose output to stderr
  --help                Show this message and exit.

```
<!-- [[[end]]] -->


## Database schema

The database created by this tool has the following schema:

<!-- [[[cog
import tempfile, pathlib, sqlite_utils
tmpdir = pathlib.Path(tempfile.mkdtemp())
db_path = str(tmpdir / "docs.db")
result = runner.invoke(cli.cli, [
    "files", db_path, "--import-json", "tests/folder-and-children.json"
])
cog.out("```sql\n")
schema = sqlite_utils.Database(db_path).schema
# Tidy up some formatting
schema = schema.replace(", [", ",\n   [")
schema = schema.replace("\n,\n", ",\n")
schema = schema.replace("TEXT);", "TEXT\n);")
cog.out(schema)
cog.out("\n```")
]]] -->
```sql
CREATE TABLE [drive_users] (
   [permissionId] TEXT PRIMARY KEY,
   [kind] TEXT,
   [displayName] TEXT,
   [photoLink] TEXT,
   [me] INTEGER,
   [emailAddress] TEXT
);
CREATE TABLE [drive_folders] (
   [id] TEXT PRIMARY KEY,
   [_parent] TEXT,
   [_owner] TEXT,
   [lastModifyingUser] TEXT,
   [kind] TEXT,
   [name] TEXT,
   [mimeType] TEXT,
   [starred] INTEGER,
   [trashed] INTEGER,
   [explicitlyTrashed] INTEGER,
   [parents] TEXT,
   [spaces] TEXT,
   [version] TEXT,
   [webViewLink] TEXT,
   [iconLink] TEXT,
   [hasThumbnail] INTEGER,
   [thumbnailVersion] TEXT,
   [viewedByMe] INTEGER,
   [createdTime] TEXT,
   [modifiedTime] TEXT,
   [modifiedByMe] INTEGER,
   [shared] INTEGER,
   [ownedByMe] INTEGER,
   [viewersCanCopyContent] INTEGER,
   [copyRequiresWriterPermission] INTEGER,
   [writersCanShare] INTEGER,
   [folderColorRgb] TEXT,
   [quotaBytesUsed] TEXT,
   [isAppAuthorized] INTEGER,
   [linkShareMetadata] TEXT,
   FOREIGN KEY([_parent]) REFERENCES [drive_folders]([id]),
   FOREIGN KEY([_owner]) REFERENCES [drive_users]([permissionId]),
   FOREIGN KEY([lastModifyingUser]) REFERENCES [drive_users]([permissionId])
);
CREATE TABLE [drive_files] (
   [id] TEXT PRIMARY KEY,
   [_parent] TEXT,
   [_owner] TEXT,
   [lastModifyingUser] TEXT,
   [kind] TEXT,
   [name] TEXT,
   [mimeType] TEXT,
   [starred] INTEGER,
   [trashed] INTEGER,
   [explicitlyTrashed] INTEGER,
   [parents] TEXT,
   [spaces] TEXT,
   [version] TEXT,
   [webViewLink] TEXT,
   [iconLink] TEXT,
   [hasThumbnail] INTEGER,
   [thumbnailVersion] TEXT,
   [viewedByMe] INTEGER,
   [createdTime] TEXT,
   [modifiedTime] TEXT,
   [modifiedByMe] INTEGER,
   [shared] INTEGER,
   [ownedByMe] INTEGER,
   [viewersCanCopyContent] INTEGER,
   [copyRequiresWriterPermission] INTEGER,
   [writersCanShare] INTEGER,
   [quotaBytesUsed] TEXT,
   [isAppAuthorized] INTEGER,
   [linkShareMetadata] TEXT,
   FOREIGN KEY([_parent]) REFERENCES [drive_folders]([id]),
   FOREIGN KEY([_owner]) REFERENCES [drive_users]([permissionId]),
   FOREIGN KEY([lastModifyingUser]) REFERENCES [drive_users]([permissionId])
);
```
<!-- [[[end]]] -->

## Thumbnails

You can construct a thumbnail image for a known file ID using the following URL:

    https://drive.google.com/thumbnail?sz=w800-h800&id=FILE_ID

Users who are signed into Google Drive and have permission to view a file will be redirected to a thumbnail version of that file. You can tweak the `w800` and `h800` parameters to request different thumbnail sizes.

## Privacy policy

This tool requests access to your Google Drive account in order to retrieve metadata about your files there. It also offers a feature that can download the content of those files.

The credentials used to access your account are stored in the `auth.json` file on your computer. The metadata and content retrieved from Google Drive is also stored only on your own personal computer.

At no point do the developers of this tool gain access to any of your data.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd google-drive-to-sqlite
    python -m venv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
