# fetch-github-issues

[![PyPI](https://img.shields.io/pypi/v/fetch-github-issues.svg)](https://pypi.org/project/fetch-github-issues/)
[![Changelog](https://img.shields.io/github/v/release/simonw/fetch-github-issues?include_prereleases&label=changelog)](https://github.com/simonw/fetch-github-issues/releases)
[![Tests](https://github.com/simonw/fetch-github-issues/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/fetch-github-issues/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/fetch-github-issues/blob/master/LICENSE)

Fetch all GitHub issues for a repository and save them as JSON

## Installation

Install this tool using `pip`:

```bash
pip install fetch-github-issues
```

## Usage

To fetch all issues from a GitHub repository:

```bash
fetch-github-issues owner/repo --all
```
Or for just specific issues:
```bash
fetch-github-issues owner/repo 1 2 3
```

Other options:

- `--key xxx`: GitHub API key - will use the `GITHUB_TOKEN` environment variable if this is not set.
- `--output path/to/dir`: Output directory to save JSON. Default is the current directory.

For more help, run:

```bash
fetch-github-issues --help
```

You can also use:

```bash
python -m fetch_github_issues --help
```
## Issue format

Issues will be saved in files called `1.json` and `2.json` and so on, where the filename is the issue number.

Each file will look like this:

```json
{
    "issue": {
        "GitHub API issue representation": "..."
    },
    "comments": [
        {
            "GitHub API comment representation": "..."
        }
    ]
}
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

```bash
cd fetch-github-issues
python -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install -e '.[test]'
```

To run the tests:

```bash
pytest
```
