# pwasm

[![PyPI](https://img.shields.io/pypi/v/pwasm.svg)](https://pypi.org/project/pwasm/)
[![Tests](https://github.com/simonw/pwasm/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/pwasm/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/pwasm?include_prereleases&label=changelog)](https://github.com/simonw/pwasm/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/pwasm/blob/main/LICENSE)

A pure Python WebAssembly runtime.

> **Warning:** This is alpha software. It is significantly slower than WebAssembly runtimes with native extensions like [wasmtime-py](https://github.com/bytecodealliance/wasmtime-py).

## Overview

`pwasm` is a WebAssembly runtime written entirely in Python with zero external dependencies. It can load and execute `.wasm` binary modules without requiring any C extensions.

It is complete enough to run real programs compiled from C: pwasm bundles builds of [MicroPython](https://micropython.org/), [QuickJS](https://github.com/quickjs-ng/quickjs) and [Micro QuickJS](https://github.com/bellard/mquickjs), so you can run untrusted Python or JavaScript code in a sandbox with memory, CPU and time limits - using nothing but Python.

```python
from pwasm.guests import MicroPython, QuickJS

mp = MicroPython(timeout=2.0)
print(mp.exec("print([x * x for x in range(5)])"))  # [0, 1, 4, 9, 16]

js = QuickJS(max_memory=32 * 1024 * 1024)
print(js.eval("[1, 2, 3].map(x => x * 2)"))  # [2, 4, 6]
```

## Features

- **Pure Python** - No external dependencies or C extensions required
- **WebAssembly 2.0 core instructions** - everything except SIMD: integer and floating point arithmetic, conversions, sign extension, saturating truncation, multi-value blocks and functions, bulk memory and reference types
- **Passes the spec test suite** - the non-SIMD WebAssembly 2.0 core tests run in CI (validation-only tests are skipped)
- **Pythonic API** - Access exported functions directly as Python methods
- **Imports and linking** - Python functions, memories, globals and tables can be imported, including from other instances
- **Memories, tables and globals** accessible from Python
- **Resource limits** - fuel (deterministic CPU budgets), wall-clock timeouts and memory caps
- **WASI** - a small WASI preview1 subset (stdio, clocks, randomness, no filesystem)
- **Emscripten-style setjmp/longjmp** - the `invoke_*` trampolines C code needs for exceptions
- **Bundled guest interpreters** - MicroPython, QuickJS and Micro QuickJS

## Installation

```bash
pip install pwasm
```

Or with uv:

```bash
uv add pwasm
```

## Requirements

- Python 3.10+

## Usage

### Loading and Running a WebAssembly Module

```python
from pwasm import decode_module, instantiate

# Load a WASM module from bytes
with open("module.wasm", "rb") as f:
    wasm_bytes = f.read()

module = decode_module(wasm_bytes)
instance = instantiate(module)

# Call exported functions directly
result = instance.exports.add(2, 3)
print(result)  # 5
```

### Working with Multiple Functions

```python
from pwasm import decode_module, instantiate

module = decode_module(wasm_bytes)
instance = instantiate(module)

# Arithmetic operations
print(instance.exports.add(10, 20))       # 30
print(instance.exports.sub(50, 8))        # 42
print(instance.exports.mul(6, 7))         # 42
```

### Importing Python Functions

Functions a module imports can be supplied as Python callables, grouped by module name:

```python
from pwasm import decode_module, instantiate

def log(value):
    print("wasm says", value)

instance = instantiate(module, {"env": {"log": log}})
```

Host functions receive i32 and i64 arguments as signed Python integers and floats for f32 and f64. They can return `None`, a single value, or a tuple for functions with multiple results. Exceptions raised by a host function propagate out through the WebAssembly code to the Python caller.

An exported function from one instance can be imported by another:

```python
app = instantiate(app_module, {"lib": {"square": lib.exports.square}})
```

### Memories, Globals and Tables

Exported memories, globals and tables are available as objects:

```python
memory = instance.exports.memory
data = memory.read(ptr, 16)       # bytes
memory.write(ptr, b"hello")
memory.data                       # the underlying bytearray
memory.size                       # size in 64 KiB pages

counter = instance.exports.counter
counter.value                     # i32/i64 globals read as signed ints
counter.value = 5                 # mutable globals only

table = instance.exports.table
func = table.get(0)               # a function reference
func(1, 2)                        # function references can be called
```

Modules can also import memories, globals and tables, either created in Python or exported by another instance:

```python
from pwasm.runtime import GlobalInstance, MemoryInstance, TableInstance
from pwasm.types import GlobalType

memory = MemoryInstance(1, 10)  # min and max pages
instance = instantiate(module, {
    "env": {
        "memory": memory,
        "limit": 100,  # a plain number can supply an immutable global
        "counter": GlobalInstance(GlobalType("i32", mutable=True), 0),
        "table": TableInstance("funcref", 4),
    }
})
```

Host functions can call back into the instance that called them, and a Python exception raised inside a host function unwinds any WebAssembly frames in between.

### Resource Limits

Pass a `Limits` object to `instantiate()` to cap the work and memory an instance can use - useful for running untrusted code:

```python
import time
from pwasm import OutOfFuel, Timeout, instantiate
from pwasm.runtime import Limits

limits = Limits(fuel=10_000_000, max_memory=64 * 1024 * 1024)
instance = instantiate(module, imports, limits=limits)

limits.set_deadline(time.monotonic() + 2.0)  # wall-clock limit
try:
    instance.exports.run()
except (OutOfFuel, Timeout) as e:
    print("stopped:", e)
print(limits.fuel_consumed)
```

One unit of fuel is charged for every function call and every loop iteration, so the fuel a given call uses is deterministic. `max_memory` caps how far `memory.grow` can grow each memory. Instances without limits pay no overhead for these checks. `OutOfFuel` and `Timeout` are subclasses of `TrapError`.

### Running Untrusted Python and JavaScript

`pwasm.guests` wraps three interpreters compiled to WebAssembly (see [src/pwasm/guests/README.md](src/pwasm/guests/README.md) for where they came from). None of them can reach the filesystem or network.

**MicroPython:**

```python
from pwasm import OutOfFuel, Timeout
from pwasm.guests import MicroPython, PythonError

mp = MicroPython(max_memory=32 * 1024 * 1024, timeout=5.0)
mp.exec("x = 21")                # globals persist between calls
print(mp.exec("print(x * 2)"))   # "42\n" - exec() returns what was printed

# Python functions the guest can call, with JSON-serializable arguments
mp.register("lookup", lambda key: {"key": key, "value": 42})
print(mp.exec("import host\nprint(host.call('lookup', 'a'))"))

try:
    mp.exec("raise ValueError('boom')")
except PythonError as e:
    print(e)  # the guest traceback

try:
    mp.exec("while True:\n    pass", timeout=0.5)
except Timeout:
    print("stopped")
```

**QuickJS** (quickjs-ng, modern JavaScript):

```python
from pwasm.guests import QuickJS, JSError

js = QuickJS(max_memory=32 * 1024 * 1024, timeout=5.0)

@js.function
def add(a, b):
    return a + b

print(js.eval("host.add(40, 2)"))           # 42
print(js.eval("({a: [1, 2], b: 'hi'})"))    # {'a': [1, 2], 'b': 'hi'}
js.eval("console.log('hello')")
print(js.take_output())                      # "hello\n"
```

`eval()` returns the completion value (decoded from JSON). JavaScript exceptions raise `JSError`. `soft_timeout=` stops runaway code using QuickJS's interrupt handler, leaving the interpreter in a consistent state.

**Micro QuickJS** (an ES5-style subset in a fixed-size heap, fast to start):

```python
from pwasm.guests import MQuickJS

js = MQuickJS(memory_limit=1024 * 1024)
print(js.eval("Math.max(3, 7)"))  # 7
```

All three accept `fuel=`, `timeout=` and `max_memory=` limits. After a hard limit (`Timeout`, `OutOfFuel`) stops a guest mid-execution its internal state may be inconsistent, so the safest option is to discard it and start a new one.

Rough timings on CPython 3.11 (`benchmarks/guests.py`):

| | MicroPython | QuickJS | Micro QuickJS |
|---|---|---|---|
| Start up and evaluate `1 + 1`, first time | 145 ms | 1.3 s | 200 ms |
| The same in a later process (compiled code cached on disk) | 40 ms | 115 ms | 50 ms |
| Recursive `fib(15)` | 90 ms | 70 ms | 35 ms |
| 1,000 iteration loop | 40 ms | 25 ms | 15 ms |

Guests compile their busiest functions to Python as they run (see [Compiling to Python](#compiling-to-python)), so the first run of new code also pays to compile what it uses. pwasm also runs on [PyPy](https://pypy.org/): once warmed up, MicroPython and QuickJS run 1.5 to 2 times as fast there as on CPython, and Micro QuickJS a little slower.

### Sandbox, WASI and setjmp/longjmp

The guests are built from pieces you can use for your own modules:

```python
from pwasm.sandbox import Sandbox

sb = Sandbox(
    "program.wasm",
    imports={"env": {"log": print}},  # or a resolver(module, name, import)
    max_memory=64 * 1024 * 1024,
    fuel=10_000_000,
    timeout=2.0,
    args=["program", "--flag"],
)
ptr = sb.alloc(b"some input", nul=True)  # copied in using the guest's malloc
result = sb.call("process", ptr)
print(sb.stdout)
sb.free(ptr)
```

`Sandbox` serves WASI imports with `pwasm.wasi.WasiLite`: captured stdout and stderr, stdin from bytes, clocks, randomness, arguments and environment variables. It provides no filesystem or network access. `pwasm.emscripten.EmscriptenSjLj` implements the `invoke_*` trampolines that C code compiled with emscripten-style setjmp/longjmp (used for C++ exceptions and MicroPython's error handling) imports.

Since every WebAssembly function call is a Python function call, `Sandbox` raises Python's recursion limit (to 20,000, or 8,000 on Python 3.10 and PyPy).

### Error Handling

```python
from pwasm import decode_module, instantiate
from pwasm.errors import TrapError, DecodeError

# Handle runtime traps (e.g., division by zero)
try:
    instance.exports.div_s(10, 0)
except TrapError as e:
    print(f"Runtime trap: {e}")

# Handle malformed WASM
try:
    module = decode_module(b"invalid wasm")
except DecodeError as e:
    print(f"Decode error: {e}")
```

## Architecture

### Components

- **decoder.py** - Parses WebAssembly binary format with LEB128 decoding. Function bodies are decoded lazily, the first time they are needed
- **types.py** - WebAssembly type system (i32, i64, f32, f64, funcref, externref)
- **compiler.py** - Compiles each function, on its first call, into flat lists of internal opcodes and immediates
- **executor.py** - The interpreter loop, module instantiation and exports
- **codegen.py** - Compiles functions to Python source code
- **runtime.py** - Memories, tables, globals, function instances and resource limits
- **sandbox.py**, **wasi.py**, **emscripten.py** - Running real programs: import resolution, WASI and setjmp/longjmp
- **guests/** - MicroPython, QuickJS and Micro QuickJS guests
- **numeric.py** - Numeric helpers (integer and floating point semantics)
- **errors.py** - Exception hierarchy (WasmError, DecodeError, ValidationError, TrapError, LinkError)

### Execution Model

Structured control flow is compiled away before execution: `block`, `loop` and `end` produce no code, and every branch becomes a jump to a precomputed instruction index. Operand stack heights are static in valid WebAssembly, so the compiler also knows exactly which values each branch needs to discard - the interpreter keeps no label stack.

Internally i32 and i64 values are stored as unsigned Python integers. Values are converted to signed integers when they are returned to Python code.

Each WebAssembly function call is a Python call, so exceptions raised by Python code propagate through WebAssembly frames.

### Compiling to Python

pwasm can also translate a WebAssembly function into Python source code (`codegen.py`), which CPython then runs directly - typically 8 to 14 times faster than the interpreter. The operand stack disappears: pure instructions are folded into Python expressions over local variables, and masking to 32 or 64 bits is delayed until a value needs to be exact. Structured control flow becomes `while True:` loops and `if` statements. C `switch` statements compile to blocks nested more deeply than CPython allows, so a chain of consecutive blocks becomes a single loop that dispatches on a segment variable (a `br_table` into the chain is a tuple lookup); the rare function that is still too deep becomes a state machine over basic blocks instead. Memory is a `bytearray`: aligned 16, 32 and 64-bit loads read from `memoryview`s of it, which is about twice as fast as `struct`.

`instantiate()` takes a `mode`:

- `"auto"` (the default) interprets each function until it has been called twice, then compiles it - code that only runs once is not worth compiling. On PyPy, functions of more than 8,000 instructions stay in the interpreter (`pwasm.executor.AUTO_MAX_SIZE`): PyPy's JIT handles pwasm's interpreter loop well but huge generated functions badly, and QuickJS's compiled interpreter loop ran 15 times slower there
- `"compile"` compiles every function to Python on its first call
- `"interpret"` never compiles

```python
instance = instantiate(module, mode="compile")
instance.exports.run()

from pwasm.codegen import python_source
print(python_source(instance.functions[0]))  # the generated Python
```

Compiled code objects are cached on the module, so further instances of the same module reuse them.

Compiled code is also cached on disk, so a new process does not have to generate and compile it again: QuickJS starts up and evaluates its first expression in about 0.1s instead of 1.3s, and MicroPython in 40ms instead of 145ms. The cache lives in `~/.cache/pwasm` (or `$XDG_CACHE_HOME/pwasm`), in a directory for each module (by its SHA-256), Python version and version of the code generator; each function's generated source is kept next to its code, for tracebacks. Set the `PWASM_CACHE_DIR` environment variable to use another directory, or to an empty string to turn the cache off (`pwasm.codegen.CACHE_DIR = None` does the same from Python).

## Development

```bash
# Clone and setup
git clone https://github.com/simonw/pwasm
cd pwasm

# Run tests (including the WebAssembly spec test suite in tests/spec)
uv run pytest

# Summarize spec test results for some files
uv run python tests/spec_runner.py tests/spec/i32.wast tests/spec/f64.wast

# Time the guest interpreters
uv run python benchmarks/guests.py

# Format code
uv run black .
```

## License

Apache 2.0
