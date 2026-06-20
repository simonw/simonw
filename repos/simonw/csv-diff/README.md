# csv-diff

[![PyPI](https://img.shields.io/pypi/v/csv-diff.svg)](https://pypi.org/project/csv-diff/)
[![Changelog](https://img.shields.io/github/v/release/simonw/csv-diff?include_prereleases&label=changelog)](https://github.com/simonw/csv-diff/releases)
[![Tests](https://github.com/simonw/csv-diff/workflows/Test/badge.svg)](https://github.com/simonw/csv-diff/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/csv-diff/blob/main/LICENSE)

Tool for viewing the difference between two CSV, TSV or JSON files. See [Generating a commit log for San Francisco’s official list of trees](https://simonwillison.net/2019/Mar/13/tree-history/) (and the [sf-tree-history repo commit log](https://github.com/simonw/sf-tree-history/commits)) for background information on this project.

## Installation

    pip install csv-diff

## Usage

Consider two CSV files:

`one.csv`

    id,name,age
    1,Cleo,4
    2,Pancakes,2

`two.csv`

    id,name,age
    1,Cleo,5
    3,Bailey,1

`csv-diff` can show a human-readable summary of differences between the files:

    $ csv-diff one.csv two.csv --key=id
    1 row changed, 1 row added, 1 row removed

    1 row changed

      Row 1
        age: "4" => "5"

    1 row added

      id: 3
      name: Bailey
      age: 1

    1 row removed

      id: 2
      name: Pancakes
      age: 2

The `--key=id` option means that the `id` column should be treated as the unique key, to identify which records have changed.

The tool will automatically detect if your files are comma- or tab-separated. You can over-ride this automatic detection and force the tool to use a specific format using `--format=tsv` or `--format=csv`.

You can also feed it JSON files, provided they are a JSON array of objects where each object has the same keys. Use `--format=json` if your input files are JSON.

Use `--show-unchanged` to include full details of the unchanged values for rows with at least one change in the diff output:

    % csv-diff one.csv two.csv --key=id --show-unchanged
    1 row changed

      id: 1
        age: "4" => "5"

        Unchanged:
          name: "Cleo"

### JSON output

You can use the `--json` option to get a machine-readable difference:

    $ csv-diff one.csv two.csv --key=id --json
    {
        "added": [
            {
                "id": "3",
                "name": "Bailey",
                "age": "1"
            }
        ],
        "removed": [
            {
                "id": "2",
                "name": "Pancakes",
                "age": "2"
            }
        ],
        "changed": [
            {
                "key": "1",
                "changes": {
                    "age": [
                        "4",
                        "5"
                    ]
                }
            }
        ],
        "columns_added": [],
        "columns_removed": []
    }

### Adding templated extras

You can specify additional keys to be displayed in the human-readable format using the `--extra` option:

    --extra name "Python format string with {id} for variables"

For example, to output a link to `https://news.ycombinator.com/latest?id={id}` for each item with an ID, you could use this:

```bash
csv-diff one.csv two.csv --key=id \
  --extra latest "https://news.ycombinator.com/latest?id={id}"
```
These extras display something like this:
```
1 row changed

  id: 41459472
    points: "24" => "25"
    numComments: "5" => "6"
  extras:
    latest: https://news.ycombinator.com/latest?id=41459472
```

## As a Python library

You can also import the Python library into your own code like so:

    from csv_diff import load_csv, compare
    diff = compare(
        load_csv(open("one.csv"), key="id"),
        load_csv(open("two.csv"), key="id")
    )

`diff` will now contain the same data structure as the output in the `--json` example above.

If the columns in the CSV have changed, those added or removed columns will be ignored when calculating changes made to specific rows.

## As a Docker container

### Build the image

    $ docker build -t csvdiff .

### Run the container

    $ docker run --rm -v $(pwd):/files csvdiff

Suppose current directory contains two csv files : one.csv two.csv

    $ docker run --rm -v $(pwd):/files csvdiff one.csv two.csv
    
## Alternatives

- [csvdiff](https://github.com/aswinkarthik/csvdiff) is a "fast diff tool for comparing CSV files" - you may get better results from this than from `csv-diff` against larger files.
