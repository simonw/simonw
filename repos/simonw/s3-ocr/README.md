# s3-ocr

[![PyPI](https://img.shields.io/pypi/v/s3-ocr.svg)](https://pypi.org/project/s3-ocr/)
[![Changelog](https://img.shields.io/github/v/release/simonw/s3-ocr?include_prereleases&label=changelog)](https://github.com/simonw/s3-ocr/releases)
[![Tests](https://github.com/simonw/s3-ocr/workflows/Test/badge.svg)](https://github.com/simonw/s3-ocr/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/s3-ocr/blob/master/LICENSE)

Tools for running OCR against files stored in S3

Background on this project: [s3-ocr: Extract text from PDF files stored in an S3 bucket](https://simonwillison.net/2022/Jun/30/s3-ocr/)

## Installation

Install this tool using `pip`:

    pip install s3-ocr

## Demo

You can see the results of running this tool against three PDFs from the Internet Archive ([one](https://archive.org/details/unmaskingrobert00houdgoog), [two](https://archive.org/details/practicalmagicia00harr), [three](https://archive.org/details/latestmagicbeing00hoff)) in [this example table](https://s3-ocr-demo.datasette.io/pages/pages?_facet=path#facet-path) hosted using [Datasette](https://datasette.io/).

## Starting OCR against PDFs in a bucket

The `start` command takes a list of keys and submits them to [Textract](https://aws.amazon.com/textract/) for OCR processing.

You need to have AWS configured using environment variables, credentials file in your home directory or a JSON or INI file generated using [s3-credentials](https://datasette.io/tools/s3-credentials).

You can start the process running like this:

    s3-ocr start name-of-your-bucket my-pdf-file.pdf

The paths you specify should be paths within the bucket. If you stored your PDF files in folders inside the bucket it should look like this:

    s3-ocr start name-of-your-bucket path/to/one.pdf path/to/two.pdf

OCR can take some time. The results of the OCR will be stored in `textract-output` in your bucket.

To process every file in the bucket with a `.pdf` extension use `--all`:

    s3-ocr start name-of-bucket --all

To process every file with a `.pdf` extension within a specific folder, use `--prefix`:

    s3-ocr start name-of-bucket --prefix path/to/folder

### s3-ocr start --help

<!-- [[[cog
import cog
from s3_ocr import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["start", "--help"])
help = result.output.replace("Usage: cli", "Usage: s3-ocr")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: s3-ocr start [OPTIONS] BUCKET [KEYS]...

  Start OCR tasks for PDF files in an S3 bucket

      s3-ocr start name-of-bucket path/to/one.pdf path/to/two.pdf

  To process every file with a .pdf extension:

      s3-ocr start name-of-bucket --all

  To process every .pdf in the PUBLIC/ folder:

      s3-ocr start name-of-bucket --prefix PUBLIC/

Options:
  --all                 Process all PDF files in the bucket
  --prefix TEXT         Process all PDF files within this prefix
  --dry-run             Show what this would do, but don't actually do it
  --no-retry            Don't retry failed requests
  --access-key TEXT     AWS access key ID
  --secret-key TEXT     AWS secret access key
  --session-token TEXT  AWS session token
  --endpoint-url TEXT   Custom endpoint URL
  -a, --auth FILENAME   Path to JSON/INI file containing credentials
  --help                Show this message and exit.

```
<!-- [[[end]]] -->

## Checking status

The `s3-ocr status <bucket-name>` command shows a rough indication of progress through the tasks:

```
% s3-ocr status sfms-history
153 complete out of 532 jobs
```
It compares the jobs that have been submitted, based on `.s3-ocr.json` files, to the jobs that have their results written to the `textract-output/` folder.

### s3-ocr status --help

<!-- [[[cog
result = runner.invoke(cli.cli, ["status", "--help"])
help = result.output.replace("Usage: cli", "Usage: s3-ocr")
cog.out(
    "```\n{}\n```".format(help.split("--access-key")[0] + "--access-key ...")
)
]]] -->
```
Usage: s3-ocr status [OPTIONS] BUCKET

  Show status of OCR jobs for a bucket

Options:
  --access-key ...
```
<!-- [[[end]]] -->

## Inspecting a job

The `s3-ocr inspect-job <job_id>` command can be used to check the status of a specific job ID:
```
% s3-ocr inspect-job b267282745685226339b7e0d4366c4ff6887b7e293ed4b304dc8bb8b991c7864
{
  "DocumentMetadata": {
    "Pages": 583
  },
  "JobStatus": "SUCCEEDED",
  "DetectDocumentTextModelVersion": "1.0"
}
```

### s3-ocr inspect-job --help

<!-- [[[cog
result = runner.invoke(cli.cli, ["inspect-job", "--help"])
help = result.output.replace("Usage: cli", "Usage: s3-ocr")
cog.out(
    "```\n{}\n```".format(help.split("--access-key")[0] + "--access-key ...")
)
]]] -->
```
Usage: s3-ocr inspect-job [OPTIONS] JOB_ID

  Show the current status of an OCR job

      s3-ocr inspect-job <job_id>

Options:
  --access-key ...
```
<!-- [[[end]]] -->

## Fetching the results

Once an OCR job has completed you can download the resulting JSON using the `fetch` command:

    s3-ocr fetch name-of-bucket path/to/file.pdf

This will save files in the current directory with names like this:

- `4d9b5cf580e761fdb16fd24edce14737ebc562972526ef6617554adfa11d6038-1.json`
- `4d9b5cf580e761fdb16fd24edce14737ebc562972526ef6617554adfa11d6038-2.json`

The number of files will vary depending on the length of the document.

If you don't want separate files you can combine them together using the `-c/--combine` option:

    s3-ocr fetch name-of-bucket path/to/file.pdf --combine output.json

The `output.json` file will then contain data that looks something like this:

```
{
  "Blocks": [
    {
      "BlockType": "PAGE",
      "Geometry": {...}
      "Page": 1,
      ...
    },
    {
      "BlockType": "LINE",
      "Page": 1,
      ...
      "Text": "Barry",
    },
```
### s3-ocr fetch --help

<!-- [[[cog
result = runner.invoke(cli.cli, ["fetch", "--help"])
help = result.output.replace("Usage: cli", "Usage: s3-ocr")
cog.out(
    "```\n{}\n```".format(help.split("--access-key")[0] + "--access-key ...")
)
]]] -->
```
Usage: s3-ocr fetch [OPTIONS] BUCKET KEY

  Fetch the OCR results for a specified file

      s3-ocr fetch name-of-bucket path/to/key.pdf

  This will save files in the current directory called things like

      a806e67e504fc15f...48314e-1.json     a806e67e504fc15f...48314e-2.json

  To combine these together into a single JSON file with a specified name, use:

      s3-ocr fetch name-of-bucket path/to/key.pdf --combine output.json

  Use "--output -" to print the combined JSON to standard output instead.

Options:
  -c, --combine FILENAME  Write combined JSON to file
  --access-key ...
```
<!-- [[[end]]] -->

## Fetching just the text of a page

If you don't want to deal with the JSON directly, you can use the `text` command to retrieve just the text extracted from a PDF:

    s3-ocr text name-of-bucket path/to/file.pdf

This will output plain text to standard output.

To save that to a file, use this:

    s3-ocr text name-of-bucket path/to/file.pdf > text.txt

Separate pages will be separated by three newlines. To separate them using a `----` horizontal divider instead add `--divider`:

    s3-ocr text name-of-bucket path/to/file.pdf --divider

### s3-ocr text --help

<!-- [[[cog
result = runner.invoke(cli.cli, ["text", "--help"])
help = result.output.replace("Usage: cli", "Usage: s3-ocr")
cog.out(
    "```\n{}\n```".format(help.split("--access-key")[0] + "--access-key ...")
)
]]] -->
```
Usage: s3-ocr text [OPTIONS] BUCKET KEY

  Retrieve the text from an OCRd PDF file

      s3-ocr text name-of-bucket path/to/key.pdf

Options:
  --divider             Add ---- between pages
  --access-key ...
```
<!-- [[[end]]] -->

## Avoiding processing duplicates

If you move files around within your S3 bucket `s3-ocr` can lose track of which files have already been processed. This can lead to additional Textract charges for processing should you run `s3-ocr start` against those new files.

The `s3-ocr dedupe` command addresses this by scanning your bucket for files that have a new name but have previously been processed. It does this by looking at the `ETag` for each file, which represents the MD5 hash of the file contents.

The command will write out new `.s3ocr.json` files for each detected duplicate. This will avoid those duplicates being run those duplicates through OCR a second time should yo run `s3-ocr start`.

    s3-ocr dedupe name-of-bucket

Add `--dry-run` for a preview of the changes that will be made to your bucket.

### s3-ocr dedupe --help

<!-- [[[cog
result = runner.invoke(cli.cli, ["dedupe", "--help"])
help = result.output.replace("Usage: cli", "Usage: s3-ocr")
cog.out(
    "```\n{}\n```".format(help.split("--access-key")[0] + "--access-key ...")
)
]]] -->
```
Usage: s3-ocr dedupe [OPTIONS] BUCKET

  Scan every file in the bucket checking for duplicates - files that have not
  yet been OCRd but that have the same contents (based on ETag) as a file that
  HAS been OCRd.

      s3-ocr dedupe name-of-bucket

Options:
  --dry-run             Show output without writing anything to S3
  --access-key ...
```
<!-- [[[end]]] -->

## Changes made to your bucket

To keep track of which files have been submitted for processing, `s3-ocr` will create a JSON file for every file that it adds to the OCR queue.

This file will be called:

    path-to-file/name-of-file.pdf.s3-ocr.json

Each of these JSON files contains data that looks like this:

```json
{
  "job_id": "a34eb4e8dc7e70aa9668f7272aa403e85997364199a654422340bc5ada43affe",
  "etag": "\"b0c77472e15500347ebf46032a454e8e\""
}
```
The recorded `job_id` can be used later to associate the file with the results of the OCR task in `textract-output/`.

The `etag` is the ETag of the S3 object at the time it was submitted. This can be used later to determine if a file has changed since it last had OCR run against it.

This design for the tool, with the `.s3-ocr.json` files tracking jobs that have been submitted, means that it is safe to run `s3-ocr start` against the same bucket multiple times without the risk of starting duplicate OCR jobs.

## Creating a SQLite index of your OCR results

The `s3-ocr index <bucket> <database_file>` command creates a SQLite database containing the results of the OCR, and configures SQLite full-text search against the text:

```
% s3-ocr index sfms-history index.db
Fetching job details  [####################################]  100%
Populating pages table  [####################----------------]   55%  00:03:18
```
The schema of the resulting database looks like this (excluding the FTS tables):
```sql
CREATE TABLE [pages] (
   [path] TEXT,
   [page] INTEGER,
   [folder] TEXT,
   [text] TEXT,
   PRIMARY KEY ([path], [page])
);
CREATE TABLE [ocr_jobs] (
   [key] TEXT PRIMARY KEY,
   [job_id] TEXT,
   [etag] TEXT,
   [s3_ocr_etag] TEXT
);
CREATE TABLE [fetched_jobs] (
   [job_id] TEXT PRIMARY KEY
);
```
The database is designed to be used with [Datasette](https://datasette.io).

### s3-ocr index --help

<!-- [[[cog
result = runner.invoke(cli.cli, ["index", "--help"])
help = result.output.replace("Usage: cli", "Usage: s3-ocr")
cog.out(
    "```\n{}\n```".format(help.split("--access-key")[0] + "--access-key ...")
)
]]] -->
```
Usage: s3-ocr index [OPTIONS] BUCKET DATABASE

  Create a SQLite database with OCR results for files in a bucket

Options:
  --access-key ...
```
<!-- [[[end]]] -->

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd s3-ocr
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest

To regenerate the README file with the latest `--help`:

    cog -r README.md
