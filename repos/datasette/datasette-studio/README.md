# datasette-studio

[![PyPI](https://img.shields.io/pypi/v/datasette-studio.svg)](https://pypi.org/project/datasette-studio/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-studio?include_prereleases&label=changelog)](https://github.com/datasette/datasette-studio/releases)
[![Tests](https://github.com/datasette/datasette-studio/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-studio/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-studio/blob/master/LICENSE)

Datasette pre-configured with useful plugins.

**Experimental alpha release**. This is an early experiment at the moment.

[Try this out in GitHub Codespaces](https://github.com/codespaces/new?repo=datasette/studio)

## Installation

This tool makes Datasette (currently the 1.0 alpha series) available as `datasette-studio` with a set of useful plugins pre-installed.

It is _strongly_ recommended to install this using [pipx](https://pipx.pypa.io/), since doing so will ensure that this version of Datasette has its own isolated environment.

```bash
pipx install datasette-studio
```

## Usage

For help, run:
```bash
datasette-studio --help
```
To list available plugins run:
```bash
datasette-studio plugins
```
To install additional plugins use:
```bash
datasette-studio install datasette-graphql
```
The `datasette-studio` command is an alias for regular `datasette`, so [consult the Datasette documentation](https://docs.datasette.io/en/latest/) for more information on how to use it.
