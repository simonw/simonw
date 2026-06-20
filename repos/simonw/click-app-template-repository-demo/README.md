# click-app-template-repository-demo

[![PyPI](https://img.shields.io/pypi/v/click-app-template-repository-demo.svg)](https://pypi.org/project/click-app-template-repository-demo/)
[![Changelog](https://img.shields.io/github/v/release/simonw/click-app-template-repository-demo?include_prereleases&label=changelog)](https://github.com/simonw/click-app-template-repository-demo/releases)
[![Tests](https://github.com/simonw/click-app-template-repository-demo/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/click-app-template-repository-demo/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/click-app-template-repository-demo/blob/master/LICENSE)

Demo of click-app-template-repository

## Installation

Install this tool using `pip`:
```bash
pip install click-app-template-repository-demo
```
## Usage

For help, run:
```bash
click-app-template-repository-demo --help
```
You can also use:
```bash
python -m click_app_template_repository_demo --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd click-app-template-repository-demo
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
