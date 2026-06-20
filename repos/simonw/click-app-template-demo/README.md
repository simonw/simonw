# click-app-template-demo

[![PyPI](https://img.shields.io/pypi/v/click-app-template-demo.svg)](https://pypi.org/project/click-app-template-demo/)
[![Changelog](https://img.shields.io/github/v/release/simonw/click-app-template-demo?include_prereleases&label=changelog)](https://github.com/simonw/click-app-template-demo/releases)
[![Tests](https://github.com/simonw/click-app-template-demo/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/click-app-template-demo/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/click-app-template-demo/blob/master/LICENSE)

Demonstrating https://github.com/simonw/click-app

## Installation

Install this tool using `pip`:
```bash
pip install click-app-template-demo
```
## Usage

For help, run:
```bash
click-app-template-demo --help
```
You can also use:
```bash
python -m click_app_template_demo --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd click-app-template-demo
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
