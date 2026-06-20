# llm-fragments-github

[![PyPI](https://img.shields.io/pypi/v/llm-fragments-github.svg)](https://pypi.org/project/llm-fragments-github/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-fragments-github?include_prereleases&label=changelog)](https://github.com/simonw/llm-fragments-github/releases)
[![Tests](https://github.com/simonw/llm-fragments-github/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-fragments-github/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-fragments-github/blob/main/LICENSE)

Load GitHub repository contents as fragments

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-fragments-github
```
## Usage

Use `-f github:user/repo` to include every text file from the specified GitHub repo as a fragment. For example:
```bash
llm -f github:simonw/files-to-prompt 'suggest new features for this tool'
```
Use `-f issue:user/repo/number` to include the combined Markdown text of a specific issue. For example:
```bash
llm -f https://raw.githubusercontent.com/simonw/llm-fragments-github/refs/tags/0.1/llm_fragments_github.py \
  -f issue:simonw/llm-fragments-github/3 \
  'Propose an implementation for this issue'
```
The `issue:` prefix can also accept a URL to a GitHub issue, for example:
```bash
llm -f issue:https://github.com/simonw/llm-fragments-github/issues/3 \
  'muse on this a bit'
```
Set an API token in the environment variable `GITHUB_TOKEN` to access private repositories or increase your rate limit.

Use` -f pr:user/repo/number` to load the Markdown text and diff for a specified pull request. This also accepts a URL to a pull request.

```bash
llm -f pr:simonw/llm-fragments-github/9 'code review'
```
Both `issue:` and `pr:` will attempt to expand any URLs to code blocks to include that code as part of the exported Markdown. [#12](https://github.com/simonw/llm-fragments-github/issues/12)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-fragments-github
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
