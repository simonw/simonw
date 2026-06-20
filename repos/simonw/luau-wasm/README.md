# luau-wasm

[![PyPI](https://img.shields.io/pypi/v/luau-wasm.svg)](https://pypi.org/project/luau-wasm/)
[![Tests](https://github.com/simonw/luau-wasm/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/luau-wasm/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/luau-wasm?include_prereleases&label=changelog)](https://github.com/simonw/luau-wasm/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/simonw/luau-wasm/blob/main/LICENSE)

Luau packaged as a Python extension for Pyodide.

This project demonstrates publishing a WebAssembly wheel to PyPI. The wheel contains a compiled CPython extension module that embeds the [Luau](https://luau.org/) compiler and VM. In Pyodide 314, `micropip` can install that PyPI wheel directly in the browser.

Try the playground: <https://simonw.github.io/luau-wasm/>

Based on [this initial research project](https://github.com/simonw/research/tree/main/pluau-wasm-pyodide#readme).

## Installation

In Pyodide:

```python
import micropip

await micropip.install("luau-wasm")

import luau_wasm

print(luau_wasm.execute('print("Hello from Luau")'))
```

In JavaScript with Pyodide:

```javascript
await pyodide.loadPackage("micropip");
await pyodide.runPythonAsync(`
import micropip
await micropip.install("luau-wasm")
import luau_wasm
`);

pyodide.globals.set("source", 'print("Hello from Luau")');
const output = pyodide.runPython("luau_wasm.execute(source)");
```

## Python API

```python
import luau_wasm

output = luau_wasm.execute("""
local name = "Luau"
print(`Hello from {name}`)
""")
assert output == "Hello from Luau\n"
```

`execute(source)` creates a fresh sandboxed Luau state, runs the source, captures `print()` output, and returns that output as a Python string.

Compile and runtime failures raise `luau_wasm.LuauError`:

```python
try:
    luau_wasm.execute('error("boom")')
except luau_wasm.LuauError as ex:
    print(ex)
```

`run` is an alias for `execute`.

## Building

This repository vendors the minimal Luau source needed by the extension in `vendor/luau/`.

To update the vendored Luau source:

```bash
scripts/vendor-luau.sh
```

To run native tests (which use a native build, not the WASM build):

```bash
uv run python -m pytest
```

To build the Pyodide WebAssembly wheel:

```bash
scripts/build-pyodide-wheel.sh
```

That runs:

```bash
uv run --with pyodide-build pyodide build .
```

The expected wheel target for Pyodide 314 / Python 3.14 is:

```text
cp314-cp314-pyemscripten_2026_0_wasm32
```

To build using `cibuildwheel`:

```bash
CIBW_PLATFORM=pyodide uv run --with cibuildwheel cibuildwheel
```

## Publishing

Pyodide 314 implements the standardized PyEmscripten platform tags described by [PEP 783](https://peps.python.org/pep-0783/).

The GitHub Actions publish workflow builds the Pyodide wheel with [cibuildwheel](https://github.com/pypa/cibuildwheel).

## Development Notes

The extension is intentionally small:

- `native/_luau.cpp` provides the CPython wrapper and output capture.
- `setup.py` compiles Luau.Common, Luau.Ast, Luau.Bytecode, Luau.Compiler, and Luau.VM into the extension.
- `docs/index.html` is a GitHub Pages playground that loads Pyodide, installs `luau-wasm` from PyPI with `micropip`, and executes Luau code through Python.
