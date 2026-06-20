# tiny-haversine

[![PyPI](https://img.shields.io/pypi/v/tiny-haversine.svg)](https://pypi.org/project/tiny-haversine/)
[![Tests](https://github.com/simonw/tiny-haversine/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/tiny-haversine/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/tiny-haversine?include_prereleases&label=changelog)](https://github.com/simonw/tiny-haversine/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/simonw/tiny-haversine/blob/main/LICENSE)

A tiny, minimal example of a Python C extension that can be built as both a native wheel and a Pyodide wheel.

## Overview

This repo is intentionally small. It demonstrates:

- A minimal C extension module
- The smallest `pyproject.toml` + `setup.py` that works
- Native builds with `uv build`
- Pyodide builds with `./build-for-pyodide.sh`

## Requirements

- Python 3.10+
- A working C toolchain for native builds
- `uv`

## Build Native Wheels

From this directory:

```bash
uv build
```

Artifacts will appear in `dist/`.

## Build Pyodide Wheels

Native wheels are built separately with `uv build` (see above). To build the Pyodide/Emscripten wheel:

```bash
./build-for-pyodide.sh
```

Artifacts will appear in `dist/`.

### Optional environment variables

You can override versions and paths:

```bash
PYTHON_VERSION=3.13 PYODIDE_VERSION=0.29.3 EMSCRIPTEN_VERSION=4.0.9 ./build-for-pyodide.sh
```

## Run Tests

```bash
uv run pytest
```

## Minimal Project Layout

```text
pyproject.toml
setup.py
build-for-pyodide.sh
tests/
  test_haversine.py
src/
  tiny_haversine/
    __init__.py
    _haversine.c
```
