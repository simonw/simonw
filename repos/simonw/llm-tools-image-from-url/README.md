# llm-tools-image-from-url

[![PyPI](https://img.shields.io/pypi/v/llm-tools-image-from-url.svg)](https://pypi.org/project/llm-tools-image-from-url/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-tools-image-from-url?include_prereleases&label=changelog)](https://github.com/simonw/llm-tools-image-from-url/releases)
[![Tests](https://github.com/simonw/llm-tools-image-from-url/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-tools-image-from-url/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-image-from-url/blob/main/LICENSE)

Tool for fetching images from URLs as attachments

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-image-from-url
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm --tool fetch_image_from_url "Example prompt goes here" --tools-debug
```

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_image_from_url import fetch_image_from_url

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "Example prompt goes here",
    tools=[fetch_image_from_url]
).text()
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-image-from-url
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
