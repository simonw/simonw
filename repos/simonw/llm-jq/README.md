# llm-jq

[![PyPI](https://img.shields.io/pypi/v/llm-jq.svg)](https://pypi.org/project/llm-jq/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-jq?include_prereleases&label=changelog)](https://github.com/simonw/llm-jq/releases)
[![Tests](https://github.com/simonw/llm-jq/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-jq/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-jq/blob/main/LICENSE)

Write and execute jq programs with the help of LLM

See [Run a prompt to generate and execute jq programs using llm-jq](https://simonwillison.net/2024/Oct/27/llm-jq/) for background on this project.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-jq
```
## Usage

Pipe JSON directly into `llm jq` and describe the result you would like:

```bash
curl -s https://api.github.com/repos/simonw/datasette/issues | \
  llm jq 'count by user.login, top 3'
```
Output:
```json
[
  {
    "login": "simonw",
    "count": 11
  },
  {
    "login": "king7532",
    "count": 5
  },
  {
    "login": "dependabot[bot]",
    "count": 2
  }
]
```
```
group_by(.user.login) | map({login: .[0].user.login, count: length}) | sort_by(-.count) | .[0:3]
```
The JSON is printed to standard output, the jq program is printed to standard error.

Options:

- `-s/--silent`: Do not print the jq program to standard error
- `-o/--output`: Output just the jq program, do not run it
- `-v/--verbose`: Show the prompt sent to the model and the response
- `-m/--model X`: Use a model other than the configured LLM default model
- `-l/--length X`: Use a length of the input other than 1024 as the example

By default, the first 1024 bytes of JSON will be sent to the model as an example along with your description. You can use `-l` to send more or less example data.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-jq
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
