# datasette-show-errors

[![PyPI](https://img.shields.io/pypi/v/datasette-show-errors.svg)](https://pypi.org/project/datasette-show-errors/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-show-errors.svg?style=svg)](https://circleci.com/gh/simonw/datasette-show-errors)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-show-errors/blob/master/LICENSE)

Datasette plugin for displaying error tracebacks.

**This plugin does not work with current versions of Datasette.** See [issue #2](https://github.com/simonw/datasette-show-errors/issues/2).

## Installation

    pip install datasette-show-errors

## Usage

Installing the plugin will cause any internal error to be displayed with a full traceback, rather than just a generic 500 page.

Be careful not to use this in a context that might expose sensitive information.
