# stream-delay

[![PyPI](https://img.shields.io/pypi/v/stream-delay.svg)](https://pypi.org/project/stream-delay/)
[![Changelog](https://img.shields.io/github/v/release/simonw/stream-delay?include_prereleases&label=changelog)](https://github.com/simonw/stream-delay/releases)
[![Tests](https://github.com/simonw/stream-delay/workflows/Test/badge.svg)](https://github.com/simonw/stream-delay/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/stream-delay/blob/master/LICENSE)

Stream a file or stdin one line at a time with a delay

## Installation

Install this tool using `pip`:

    $ pip install stream-delay

## Usage

Feed content to this tool either by piping to standard input or using one or more filenames.

The tool will output the data from those inputs one line at a time with a 100ms delay between each line.

You can use `-d 500` to change the delay to another value expressed in milliseconds.

Examples:

- `cat myfile.txt | stream-delay` - will stream from that file with a 100ms delay between each line
- `stream-delay myfile.txt` - same as above, this time using the filename
- `stream-delay myfile.txt myfile2.txt` - streams from the first file, then the second file
- `stream-delay myfile.txt -d 1000` - streams from that file with a one second delay between each line

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd stream-delay
    python -m venv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
