# textract-cli

[![PyPI](https://img.shields.io/pypi/v/textract-cli.svg)](https://pypi.org/project/textract-cli/)
[![Changelog](https://img.shields.io/github/v/release/simonw/textract-cli?include_prereleases&label=changelog)](https://github.com/simonw/textract-cli/releases)
[![Tests](https://github.com/simonw/textract-cli/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/textract-cli/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/textract-cli/blob/master/LICENSE)

CLI for running files through AWS Textract

## Installation

Install this tool using `pip`:
```bash
pip install textract-cli
```
## Configuration

Any of the [methods for configuring](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) `boto3` will work with this tool. Environment variables or a `~/.aws/config` file are good options here.

## Usage

To run Textract OCR against a JPEG or PNG file (must be smaller than 5MB):
```bash
textract-cli image.jpeg
```
This will output to standard out. To save to a file use this:
```bash
textract-cli image.jpeg > output.txt
```
Or use the `-o/--output` option like this:
```bash
textract-cli image.jpeg -o output.txt
```

For help, run:
```bash
textract-cli --help
```
You can also use:
```bash
python -m textract_cli --help
```
## Alternatives

[amazon-textract-textractor](https://aws-samples.github.io/amazon-textract-textractor/commandline.html) an Amazon project offering a similar but much more comprehensive CLI.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd textract-cli
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
