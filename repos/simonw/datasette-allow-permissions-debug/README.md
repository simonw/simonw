# datasette-allow-permissions-debug

[![PyPI](https://img.shields.io/pypi/v/datasette-allow-permissions-debug.svg)](https://pypi.org/project/datasette-allow-permissions-debug/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-allow-permissions-debug?label=changelog)](https://github.com/simonw/datasette-allow-permissions-debug/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-allow-permissions-debug/blob/master/LICENSE)

Always allow access to `/-/permissions`, for debugging.

## Installation

Install this plugin in the same environment as Datasette.

    $ pip install datasette-allow-permissions-debug

## Usage

Once installed, all access to `/-/permissions` will be allowed even if you are not signed in.
