# micropython-wasm

[![PyPI](https://img.shields.io/pypi/v/micropython-wasm.svg)](https://pypi.org/project/micropython-wasm/)
[![Tests](https://github.com/simonw/micropython-wasm/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/micropython-wasm/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/micropython-wasm?include_prereleases&label=changelog)](https://github.com/simonw/micropython-wasm/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/micropython-wasm/blob/main/LICENSE)

MicroPython packaged as a WASI WebAssembly module and executed from Python
using Wasmtime.

See [Running Python code in a sandbox with MicroPython and WASM](https://simonwillison.net/2026/Jun/6/micropython-in-a-sandbox/) for background on this project.

This project is an experimental Python package for running small snippets of
MicroPython in a fresh WebAssembly sandbox. It is designed around:

- A custom MicroPython WASI artifact, not the Emscripten browser/Node build.
- The official `wasmtime` Python package.
- A fresh Wasmtime instance for one-shot execution, plus an optional persistent
  session API backed by a background thread.
- No host filesystem access unless an explicit read-only directory is
  preopened.
- No network capability.
- Configurable WebAssembly memory, fuel, and wall-clock controls.

## Installation

Install from PyPI:

```bash
pip install micropython-wasm
```

For local development, use `uv`:

```bash
git clone https://github.com/simonw/micropython-wasm
cd micropython-wasm
uv run pytest
```

## Quick Start

You can run MicroPython in WASM from the command line:

```bash
micropython-wasm -c "print(1 + 1)"
micropython-wasm script.py
micropython-wasm
```
You can also `micropython-wasm` without installing it first using `uvx`:
```bash
uvx micropython-wasm --help
```

The no-argument form starts a simple REPL with persistent state between
prompts. Use `--memory` to set the WebAssembly memory limit in bytes and
`--fuel` to set the Wasmtime fuel budget:

```bash
micropython-wasm --memory 33554432 --fuel 20000000 -c "print('hello')"
```

To use it in Python import code from the `micropython_wasm` package:

```python
from micropython_wasm import run

result = run("print(1 + 1)")
print(result.stdout)
```

Output:

```text
2
```

`run()` returns a `RunResult`:

```python
from micropython_wasm import run

result = run("print('hello')")

print(result.stdout)          # "hello\n"
print(result.stderr)          # ""
print(result.fuel_remaining)  # integer Wasmtime fuel count
```

Each call creates a new engine, store, WASI config, module instance, and
MicroPython process. Globals and imports do not persist between calls.

For stateful usage with real resident MicroPython state, use
`MicroPythonSession`:

```python
from micropython_wasm import MicroPythonSession

with MicroPythonSession() as session:
    print(session.run("x = 10\nprint(x)").stdout)
    print(session.run("x += 5\nprint(x)").stdout)
    print(session.run("print(x * 2)").stdout)
```

Output:

```text
10

15

30
```

You can also use the same object without a context manager, which is convenient
in an interactive Python REPL:

```python
from micropython_wasm import MicroPythonSession

session = MicroPythonSession()
session.run("x = 10")
session.run("print(x)")
session.close()
```

## API

### `run(code, ...)`

Run MicroPython source code using the bundled artifact:

```python
from micropython_wasm import run

result = run(
    "print(sum(range(10)))",
    memory_bytes=16 * 1024 * 1024,
    fuel=20_000_000,
    wall_timeout_seconds=1.0,
    host_result_bytes=256 * 1024,
)
```

Arguments:

- `code`: MicroPython source code passed as `micropython -c <code>`.
- `wasm_path`: optional path to a custom WASI MicroPython artifact. If omitted,
  `micropython_wasm/artifacts/micropython-wasi.wasm` is used.
- `memory_bytes`: maximum WebAssembly linear memory for the store.
- `fuel`: Wasmtime fuel budget. Guest execution traps when it runs out.
- `wall_timeout_seconds`: wall-clock timeout. Pass `None` to disable epoch
  interruption.
- `readonly_dir`: optional host directory to expose inside the guest as
  `/input`, with read-only WASI directory and file permissions.
- `host_functions`: optional mapping of host function names to Python callables.
  This enables the low-level `host.call(name, payload_json)` bridge.
- `host_result_bytes`: maximum serialized host callback response size. The
  default is `256 * 1024`.

### `run_micropython_wasi(code, wasm_path, ...)`

Run code against an explicit `.wasm` artifact:

```python
from micropython_wasm import run_micropython_wasi

result = run_micropython_wasi(
    "print(2 ** 8)",
    "micropython_wasm/artifacts/micropython-wasi.wasm",
)
```

This is useful when testing a locally rebuilt MicroPython artifact before
copying it into the package.

### `MicroPythonSession(...)`

Create a persistent MicroPython VM running in a background Python thread:

```python
from micropython_wasm import MicroPythonSession

session = MicroPythonSession()

session.run("x = 10")
session.run("x += 5")
result = session.run("print(x)")
print(result.stdout)

session.close()
```

`MicroPythonSession` starts lazily on the first `run()`. A bootstrap loop
runs inside MicroPython and repeatedly calls back to the Python host for the
next code snippet. Each snippet is executed with `exec(..., globals())` in the
same MicroPython VM, so variables, imports, functions, classes, and live objects
really stay resident between calls.

`MicroPythonSession` accepts the same resource, filesystem, and host
function arguments as `run()`:

```python
session = MicroPythonSession(
    memory_bytes=16 * 1024 * 1024,
    fuel=20_000_000,
    readonly_dir="fixtures",
    host_functions={"add": lambda a, b: a + b},
    host_result_bytes=256 * 1024,
)
```

Methods and properties:

- `session.run(code)`: run code in the resident VM and return a `RunResult`.
- `session.register_function(func, name=None)`: expose a Python function to
  MicroPython code, optionally under a custom name.
- `session.close()`: send a close message to the guest loop and reject further
  runs.
- `session.closed`: `True` after `close()`.
- `session.host_functions`: copy of registered host functions.
- Context manager support: `with MicroPythonSession() as session: ...`.

Fuel is refreshed for each `session.run()` request. If a snippet exhausts fuel
or otherwise traps the guest, the background VM stops and the session should be
discarded.

### `MicroPythonReplaySession(...)`

Create a transcript-backed session object with the same basic `run()` and
`close()` shape as `MicroPythonSession`, but without keeping a MicroPython VM
running in a background thread.

`MicroPythonReplaySession` does not run a background thread and does not keep a
live MicroPython VM between calls. Each `run()` call executes a fresh Wasmtime
instance and returns when that one command-style execution finishes. To preserve
variables, functions, classes, and imports from the caller's point of view, it
reconstructs state by replaying previous successful snippets before each new
snippet.

```python
from micropython_wasm import MicroPythonReplaySession

session = MicroPythonReplaySession()

session.run("""
import math

def hypotenuse(a, b):
    return math.sqrt(a * a + b * b)
""")

result = session.run("print(hypotenuse(3, 4))")
print(result.stdout)

session.close()
```

`MicroPythonReplaySession` accepts the same resource and filesystem arguments as
`run()`:

```python
session = MicroPythonReplaySession(
    memory_bytes=16 * 1024 * 1024,
    fuel=20_000_000,
    wall_timeout_seconds=1.0,
    readonly_dir="fixtures",
    host_result_bytes=256 * 1024,
)
```

Methods and properties:

- `session.run(code)`: run code and return a `RunResult`.
- `session.close()`: clear the transcript and reject further runs.
- `session.closed`: `True` after `close()`.
- `session.snippets`: tuple of successful snippets currently retained.
- Context manager support: `with MicroPythonReplaySession() as session: ...`.

Only successful snippets are retained. If a snippet exits nonzero or traps, it
is not added to the session transcript:

```python
from micropython_wasm import MicroPythonReplaySession, MicroPythonWasmError

session = MicroPythonReplaySession()
session.run("x = 1")

try:
    session.run("x = 2\nraise ValueError('boom')")
except MicroPythonWasmError:
    pass

print(session.run("print(x)").stdout)  # "1\n"
```

For `MicroPythonReplaySession`, each `session.run()` call creates a fresh guest
instance, replays previous successful snippets, emits an internal marker, then
runs the new snippet and returns only the output after that marker. This
preserves ordinary Python state from the caller's point of view, including
variables, functions, classes, and imports, but previous snippets are
re-executed internally on every call.

That replay behavior matters if previous snippets perform side effects such as
writing files, making time-dependent calculations, consuming randomness, or
mutating external host state. Use `MicroPythonSession` when you want true
resident in-VM persistence.

For example, this calls the Python `record()` function again during the second
`session.run()`, because the first snippet is replayed before `print(count)` is
executed:

```python
from micropython_wasm import MicroPythonReplaySession

calls = []

def record(value):
    calls.append(value)
    return len(calls)

session = MicroPythonReplaySession(host_functions={"record": record})
session.run("count = record('once')")
session.run("print(count)")
session.close()

print(calls)  # ["once", "once"]
```

### Host Functions

`MicroPythonSession` and `MicroPythonReplaySession` can expose regular Python
functions to MicroPython code. Register a function, then call it by name inside
the guest:

```python
from micropython_wasm import MicroPythonSession

def add(a, b):
    return a + b

session = MicroPythonSession()
session.register_function(add)

result = session.run("print(add(2, 3))")
print(result.stdout)
```

Output:

```text
5
```

If the Python callable already has the name you want to expose, pass it
directly:

```python
def shout(value):
    return value.upper() + "!"

session = MicroPythonSession()
session.register_function(shout)

print(session.run("print(shout('hello'))").stdout)
```

To expose a function under a different MicroPython name, pass `name=`:

```python
def add(a, b):
    return a + b

session = MicroPythonSession()
session.register_function(add, name="plus")

print(session.run("print(plus(2, 3))").stdout)
```

You can also provide functions when constructing the session:

```python
def format_name(first, last, uppercase=False):
    result = f"{first} {last}"
    if uppercase:
        result = result.upper()
    return result

session = MicroPythonSession(
    host_functions={"format_name": format_name},
)

print(session.run("print(format_name('Ada', last='Lovelace', uppercase=True))").stdout)
```

Arguments and return values cross the WebAssembly boundary as JSON. Supported
values are therefore JSON-compatible values: `None`, booleans, numbers, strings,
lists, and dictionaries with string keys.

Python-side exceptions are returned to the MicroPython wrapper and raised as
`RuntimeError`, so guest code can catch them:

```python
def fail():
    raise ValueError("bad host value")

session = MicroPythonSession(host_functions={"fail": fail})

result = session.run("""
try:
    fail()
except RuntimeError as ex:
    print(str(ex))
""")

print(result.stdout)
```

Output:

```text
ValueError: bad host value
```

Under the hood the bundled MicroPython artifact includes a tiny built-in module
named `host`. That module imports `micropython_wasm.host_call` from Wasmtime and
exposes a low-level `host.call(name, payload_json)` function. The session API
builds friendly MicroPython wrappers on top of that low-level bridge.

One-shot `run()` and `run_micropython_wasi()` also accept a `host_functions`
mapping, but they do not automatically define friendly wrappers. They expose the
low-level `host` module:

```python
from micropython_wasm import run

def add(a, b):
    return a + b

result = run(
    """
import host
print(host.call("add", '{"args": [2, 3], "kwargs": {}}'))
""",
    host_functions={"add": add},
)

print(result.stdout)
```

### `default_wasm_path()`

Return the package's expected artifact path:

```python
from micropython_wasm import default_wasm_path

print(default_wasm_path())
```

### Exceptions

The package raises:

- `MicroPythonWasmArtifactNotFound` if the configured artifact does not exist.
- `MicroPythonSessionClosed` if `session.run()` is called after
  `session.close()`.
- `MicroPythonWasmError` for guest traps, nonzero guest exits, invalid artifacts,
  missing Wasmtime support, or invalid preopened directories.
- `ValueError` for invalid host-side resource limits.

For example:

```python
from micropython_wasm import MicroPythonWasmError, run

try:
    run('raise ValueError("boom")')
except MicroPythonWasmError as ex:
    print(ex)
```

## Filesystem Access

By default, the guest gets no preopened host directories:

```python
from micropython_wasm import run

run("print('no files by default')")
```

To expose input files, place them in a directory and pass `readonly_dir`:

```python
from pathlib import Path
from micropython_wasm import run

fixtures = Path("fixtures")
fixtures.mkdir(exist_ok=True)
(fixtures / "example.txt").write_text("hello from the host\n")

result = run(
    "print(open('/input/example.txt').read())",
    readonly_dir=fixtures,
)

print(result.stdout)
```

The directory is mounted at `/input` in the WASI guest. The package asks
Wasmtime for read-only directory and file permissions. Attempts to write inside
`/input` should fail.

Do not preopen your project root, home directory, `/`, or a shared temporary
directory when running untrusted code.

## Resource Controls

The host configures these Wasmtime controls for each execution:

- `Store.set_limits(memory_size=...)` limits WebAssembly linear memory.
- `Store.set_fuel(...)` limits CPU-like instruction progress.
- Epoch interruption is enabled when `wall_timeout_seconds` is not `None`.
- `Config.max_wasm_stack` is set to `512 * 1024`.

Example:

```python
from micropython_wasm import MicroPythonWasmError, run

try:
    run(
        "while True:\n    pass",
        fuel=50_000,
        wall_timeout_seconds=None,
    )
except MicroPythonWasmError as ex:
    print("stopped:", ex)
```

`memory_bytes` limits guest linear memory, not total host process RSS. Wasmtime
runtime memory, compiled code, Python process memory, and host callbacks are
outside that limit. For high-risk multi-tenant workloads, run each execution in
a separate worker process with OS-level CPU, memory, and wall-clock limits too.

## Network Access

This package does not expose network imports or host socket functions. The
current MicroPython WASI artifact also has socket and SSL support disabled in
the WASI variant configuration.

If network access is ever added, prefer a narrow host-mediated API such as
`http_get(url)` with explicit allowlists, timeouts, redirect limits, and maximum
response sizes. Do not expose raw sockets to untrusted code.

## Supported Python Behavior

MicroPython is not CPython. It implements a substantial subset of Python, but
there are differences in syntax support, standard-library coverage, object
behavior, and platform details.

The test suite verifies useful behavior including:

- Arithmetic and big integers.
- Strings and bytes.
- Lists, tuples, dictionaries, and sets.
- List, dict, set, and generator comprehensions.
- Functions, default arguments, keyword-only arguments, lambdas, closures, and
  recursion.
- Classes, inheritance, `property`, `isinstance`.
- `try`/`except`/`finally` and context managers.
- `math`, `json`, `re`, `binascii`, `sys`, and `os.listdir('/input')`.
- Fresh execution state between calls.
- Transcript-backed session state across `MicroPythonReplaySession.run()` calls.
- True resident VM state across `MicroPythonSession.run()` calls.
- Host function callbacks through session `register_function()` methods.
- Read-only file preopens.
- Fuel exhaustion.

Known observations from this artifact:

- `sys.platform` reports `linux`.
- `sys.argv` is `['-c']` inside the guest.
- `hashlib.sha256` is not available in the bundled artifact.
- `zlib` is not available in the bundled artifact.

### Listing Available Modules

To see the MicroPython import path and the modules available to the bundled
artifact, run:

```python
from micropython_wasm import run

result = run(
    """
import sys

print("sys.path:")
for path in sys.path:
    print(" ", path)

print()
print("modules:")
help("modules")
"""
)

print(result.stdout)
```

`help("modules")` is the most useful MicroPython-native listing because it
includes built-in and frozen modules as well as modules available on the
filesystem. A plain `os.listdir()` scan of `sys.path` will miss frozen modules
in this artifact.

## Rebuilding the WASI Artifact

The build helper is:

```text
scripts/build_micropython_wasi.py
```

It:

1. Clones MicroPython into `/tmp/micropython-wasm-build/micropython`.
2. Checks out the requested ref, including GitHub PR refs such as
   `pull/13676/head`.
3. Builds `mpy-cross`.
4. Runs `make submodules` for `ports/unix`.
5. Builds `ports/unix VARIANT=wasi`.
6. Includes the bundled `host` user C module by default.
7. Finds the best wasm artifact.
8. Copies it to `micropython_wasm/artifacts/micropython-wasi.wasm`.

### macOS ARM64 Setup

Install Binaryen:

```bash
brew install binaryen
```

Download `wasi-sdk` 25.0 to `/tmp`:

```bash
curl -L -o /tmp/wasi-sdk-25.0-arm64-macos.tar.gz \
  https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-25/wasi-sdk-25.0-arm64-macos.tar.gz
tar -xzf /tmp/wasi-sdk-25.0-arm64-macos.tar.gz -C /tmp
```

Build the artifact:

```bash
uv run python scripts/build_micropython_wasi.py \
  --ref pull/13676/head \
  --wasi-sdk /tmp/wasi-sdk-25.0-arm64-macos
```

Use `--clean` to discard the existing `/tmp` checkout:

```bash
uv run python scripts/build_micropython_wasi.py \
  --clean \
  --ref pull/13676/head \
  --wasi-sdk /tmp/wasi-sdk-25.0-arm64-macos
```

Use `--skip-build` to recopy an already-built artifact from the checkout:

```bash
uv run python scripts/build_micropython_wasi.py \
  --skip-build \
  --ref pull/13676/head \
  --wasi-sdk /tmp/wasi-sdk-25.0-arm64-macos
```

### Useful Build Options

- `--repo-url`: alternate MicroPython repository.
- `--ref`: git ref to build. PR refs like `pull/<number>/head` are supported.
- `--work-dir`: alternate build checkout directory.
- `--output`: alternate destination for the copied artifact.
- `--variant`: alternate Unix variant, defaults to `wasi`.
- `--wasi-sdk`: path to a `wasi-sdk` directory.
- `--user-c-modules`: path to a MicroPython `USER_C_MODULES` directory.
- `--jobs`: parallel build jobs.
- `--extra-make-arg`: additional argument forwarded to the Unix make command.
- `--clean`: remove the checkout before cloning.
- `--skip-build`: find and copy an existing artifact without rebuilding.

On macOS, the script passes
`CFLAGS_EXTRA=-Wno-error=gnu-folding-constant` when building `mpy-cross`, because
the experimental branch currently trips this Apple Clang warning while using
`-Werror`.

### Artifact Selection

The script prefers artifacts in this order:

1. `build-wasi/micropython.spilled.exnref`
2. `build-wasi/micropython.exnref`
3. `build-wasi/micropython.wasm`
4. `build-wasi/micropython`

The current local build produced:

```text
/tmp/micropython-wasm-build/micropython/ports/unix/build-wasi/micropython
/tmp/micropython-wasm-build/micropython/ports/unix/build-wasi/micropython.exnref
micropython_wasm/artifacts/micropython-wasi.wasm
```

The copied package artifact is the `micropython.exnref` output.

## Testing

Run the full test suite:

```bash
uv run pytest
```

The suite includes package tests and runtime integration tests against the
bundled wasm artifact. If the artifact is missing, runtime integration tests are
skipped, but package/build-script tests still run.

To test a custom artifact manually:

```bash
uv run python - <<'PY'
from micropython_wasm import run_micropython_wasi

result = run_micropython_wasi(
    "print(1 + 1)",
    "/path/to/micropython-wasi.wasm",
)
print(result.stdout)
PY
```

## Security Notes

This package is a Wasmtime embedding for a MicroPython WASI command module. It
is a useful sandboxing layer, but it is not a complete security boundary by
itself for high-risk production use.

Reasonable defaults in this package:

- Fresh instance for each run.
- No inherited host environment.
- No preopened host directories by default.
- Optional read-only preopened directory only.
- No network host functions.
- Fuel and memory limits.
- Optional wall-clock timeout.

Additional protections to consider:

- Run executions in separate worker processes.
- Apply OS-level memory and CPU limits.
- Put workers in containers or another isolation boundary.
- Bound stdout/stderr capture size if running untrusted code at scale.
- Avoid host callbacks that expose ambient authority.
- Keep Wasmtime and the MicroPython artifact pinned and regularly tested.

## Implementation Status and Caveats

The repository currently includes a working bundled artifact at:

```text
micropython_wasm/artifacts/micropython-wasi.wasm
```

That artifact was built from MicroPython PR `#13676`, using the PR ref
`pull/13676/head`. MicroPython's WASI Unix variant is still experimental
upstream, so this package should also be treated as experimental.

The test suite verifies the bundled artifact against arithmetic, strings,
bytes, collections, comprehensions, functions, closures, recursion, classes,
exceptions, context managers, a small standard-library subset, fresh instance
isolation, read-only file access, and fuel interruption. It also verifies both
stateful session APIs: the transcript-backed `MicroPythonReplaySession` and the
persistent background-thread `MicroPythonSession`.

One important build caveat: the PR's full post-link Binaryen pipeline currently
fails here at `wasm-opt --spill-pointers` with Binaryen 130. The artifact in this
repository uses the successful `wasm-opt --translate-to-exnref` postprocess
instead. Simple and moderately broad Python execution works under Wasmtime, but
this should be stress-tested before relying on it for hostile or long-running
code.

## License

Apache-2.0
