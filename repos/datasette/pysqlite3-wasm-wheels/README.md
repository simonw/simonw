# pysqlite3-wasm-wheels

[pysqlite3](https://github.com/coleifer/pysqlite3) wheels for [Pyodide](https://pyodide.org/), one for every tagged SQLite 3 release in the [SQLite GitHub mirror](https://github.com/sqlite/sqlite).

- **Try them**: https://datasette.github.io/pysqlite3-wasm-wheels/ runs SQL against one or more SQLite versions in your browser and shows where their results differ
- **Index**: [wheels.json](https://datasette.github.io/pysqlite3-wasm-wheels/wheels.json) lists every wheel
- **Wheels**: the [wheels/](wheels/) folder

## Using a wheel

Wheels are named `pysqlite3-{pysqlite3 version}-{SQLite version}-{python}-{abi}-{platform}.whl`. The SQLite version sits in the wheel filename's build tag slot. The last three parts say which Python and Pyodide ABI the wheel works with.

```python
import micropip
await micropip.install(
    "https://datasette.github.io/pysqlite3-wasm-wheels/wheels/"
    "pysqlite3-0.6.2-3.54.1-cp314-cp314-pyemscripten_2026_0_wasm32.whl"
)
import pysqlite3
print(pysqlite3.sqlite_version)
```

`pyodide.loadPackage(url)` works too. Each wheel has its SQLite compiled in with hidden symbols, so it does not clash with the older SQLite that is built into Pyodide.

## wheels.json

```json
{
  "wheels": [
    {
      "sqlite_version": "3.54.1",
      "filename": "pysqlite3-0.6.2-3.54.1-cp314-cp314-pyemscripten_2026_0_wasm32.whl",
      "path": "wheels/pysqlite3-0.6.2-3.54.1-cp314-cp314-pyemscripten_2026_0_wasm32.whl",
      "pysqlite3_version": "0.6.2",
      "pyodide_version": "314.0.8",
      "python_tag": "cp314",
      "abi_tag": "cp314",
      "platform_tag": "pyemscripten_2026_0_wasm32",
      "size": 422393,
      "sha256": "...",
      "built": "2026-11-16T06:52:46Z"
    }
  ]
}
```

Newest SQLite version first. `path` is relative to `wheels.json`. `pyodide_version` is the Pyodide release the wheel was built and tested against.

## How it works

[.github/workflows/build.yml](.github/workflows/build.yml) runs every hour. It lists the `version-3.*` tags in the SQLite mirror, works out which have no wheel yet and builds up to 10 of them, newest first. Each wheel is tested in Pyodide under Node.js and then committed along with an updated `wheels.json`. A version that fails to build or fails its test is recorded in `failures.json` and not tried again until the pysqlite3 or Pyodide version in `scripts/build_missing.py` changes.

To build locally you need uv, Node.js, git, make, a C compiler and tclsh:

```bash
npm ci
scripts/build_missing.py list              # versions with no wheel yet
scripts/build_missing.py build 3.54.1      # build and test one version
scripts/build_missing.py build --max 10    # build the 10 newest missing versions
```

- `scripts/build.sh` builds one wheel: it generates the SQLite amalgamation from the tagged source, drops it into the pysqlite3 source and runs `pyodide build`
- `scripts/test.mjs` installs a wheel into Pyodide and checks `sqlite_version()`
- `scripts/build_missing.py` finds missing versions, runs the other two and maintains `wheels.json`

[research.md](research.md) has the original notes on the build recipe.
