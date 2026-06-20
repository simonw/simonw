# datasette-os-info

[![PyPI](https://img.shields.io/pypi/v/datasette-os-info.svg)](https://pypi.org/project/datasette-os-info/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-os-info?include_prereleases&label=changelog)](https://github.com/datasette/datasette-os-info/releases)
[![Tests](https://github.com/datasette/datasette-os-info/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-os-info/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-os-info/blob/main/LICENSE)

Provide information about the current OS at `/-/os`

See [Claude can write complete Datasette plugins now](https://simonwillison.net/2025/Oct/8/claude-datasette-plugins/) for background on this project.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-os-info
```
## Usage

This plugin adds a `/-/os` page to your Datasette instance that returns detailed information about the operating system, formatted as pretty-printed JSON.

**⚠️ Security Warning**: This endpoint exposes system information including hostnames, usernames, filesystem paths, and environment variables. Review the output before deploying on a public instance.

Visit `/-/os` on your Datasette instance to see comprehensive OS information including:

- **Platform details**: System type, release, version, machine architecture, processor
- **Python information**: Version, implementation, executable path
- **Container detection**: Docker, Kubernetes, LXC detection
- **Linux-specific information** (when running on Linux):
  - Distribution details from `/etc/os-release` (name, version, codename)
  - Debian/Alpine/RedHat version information
  - Kernel information
  - CPU model and count
  - Memory statistics
  - Docker base image detection
- **macOS-specific information** (when running on macOS):
  - macOS version details
- **Windows-specific information** (when running on Windows):
  - Windows version and edition
- **Environment variables**: Useful variables like SHELL, TERM, USER, HOME, PATH, LANG, VIRTUAL_ENV

Example:
```bash
datasette install datasette-os-info
datasette
# Then visit http://localhost:8001/-/os
```

You can also view the output from the command line:
```bash
datasette --get /-/os
```

The JSON output is automatically pretty-printed for easy reading.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-os-info
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
