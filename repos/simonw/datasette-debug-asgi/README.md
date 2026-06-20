# datasette-debug-asgi

[![PyPI](https://img.shields.io/pypi/v/datasette-debug-asgi.svg)](https://pypi.org/project/datasette-debug-asgi/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-debug-asgi?include_prereleases&label=changelog)](https://github.com/simonw/datasette-debug-asgi/releases)
[![Tests](https://github.com/simonw/datasette-debug-asgi/workflows/Test/badge.svg)](https://github.com/simonw/datasette-debug-asgi/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-debug-asgi/blob/main/LICENSE)

Datasette plugin for dumping out the ASGI scope.

Adds a new URL at `/-/asgi-scope` which shows the current ASGI scope. Demo here: https://datasette.io/-/asgi-scope

## Installation

    pip install datasette-debug-asgi

## Usage

Visit `/-/asgi-scope` to see debug output showing the ASGI scope.

You can add query string parameters such as `/-/asgi-scope?q=hello`.

You can also add extra path components such as `/-/asgi-scope/more/path/here`.
