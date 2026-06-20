# pwasm

[![PyPI](https://img.shields.io/pypi/v/pwasm.svg)](https://pypi.org/project/pwasm/)
[![Tests](https://github.com/simonw/pwasm/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/pwasm/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/pwasm?include_prereleases&label=changelog)](https://github.com/simonw/pwasm/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/pwasm/blob/main/LICENSE)

A pure Python WebAssembly runtime.

> **Warning:** This is alpha software. It is significantly slower than WebAssembly runtimes with native extensions like [wasmtime-py](https://github.com/bytecodealliance/wasmtime-py).

## Overview

`pwasm` is a WebAssembly runtime written entirely in Python with zero external dependencies. It can load and execute `.wasm` binary modules without requiring any C extensions.

## Features

- **Pure Python** - No external dependencies or C extensions required
- **WebAssembly MVP support** - Parses and executes WebAssembly 1.0 binary format
- **Pythonic API** - Access exported functions directly as Python methods
- **i32 arithmetic** - Full support for 32-bit integer operations
- **Control flow** - Blocks, loops, conditionals, and branching instructions
- **Local and global variables** - Get, set, and tee operations with mutability checking
- **Memory support** - Linear memory with data segment initialization

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

- **decoder.py** - Parses WebAssembly binary format with LEB128 decoding
- **types.py** - WebAssembly type system (i32, i64, f32, f64, funcref, externref)
- **executor.py** - Stack-based bytecode interpreter
- **errors.py** - Exception hierarchy (WasmError, DecodeError, ValidationError, TrapError, LinkError)

### Execution Model

pwasm uses a stack-based execution model faithful to the WebAssembly specification:

1. **Value Stack** - Operand values for instructions
2. **Call Stack** - Function frames with locals and return addresses
3. **Control Flow** - Pre-computed block/loop/if targets for branching

## Development

```bash
# Clone and setup
git clone https://github.com/simonw/pwasm
cd pwasm

# Run tests
uv run pytest

# Format code
uv run black .
```

## License

Apache 2.0
