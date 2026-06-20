# llm-python

[![PyPI](https://img.shields.io/pypi/v/llm-python.svg)](https://pypi.org/project/llm-python/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-python?include_prereleases&label=changelog)](https://github.com/simonw/llm-python/releases)
[![Tests](https://github.com/simonw/llm-python/workflows/Test/badge.svg)](https://github.com/simonw/llm-python/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-python/blob/main/LICENSE)

Run a Python interpreter in the LLM virtual environment

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-python
```
## Usage

This plugin adds a new `python` command to LLM. This executes Python in the same virtual environment as LLM itself.

You can use this to check the Python version

```bash
llm python --version
# Should output 'Python 3.10.10' or similar
```
Or to start a Python shell. In that shell you can import `llm` and use it to interact with models:
```bash
llm python
```
```pycon
Python 3.10.10 (main, Mar 21 2023, 13:41:05) [Clang 14.0.6 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import llm
>>> m = llm.get_model("mistral-7b-instruct-v0")
>>> print(m.prompt("Three fun facts about pelicans"))
1. Pelicans have a unique method of hunting for food. They fly high above the water and then fold their wings into a disc shape, creating a large scoop that they use to catch fish. This technique is called “plunge diving” and it allows them to catch up to six pounds of fish in one dive!
2. Pelicans have an incredible memory when it comes to finding food. They can remember the location of every single fishing spot they’ve ever visited, even if it’s been years since they last went there. This is because they use a combination of visual cues and the earth’s magnetic field to navigate.
3. Pelicans are incredibly social birds that form large flocks called “rookeries.” These rookeries can contain thousands of pelicans, and they are often found in areas with abundant food sources such as coastlines or offshore islands. In these groups, pelicans will engage in a variety of behaviors, including preening, grooming, and even playing with one another.
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-python
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest
```
