# micro-javascript

[![PyPI](https://img.shields.io/pypi/v/micro-javascript.svg)](https://pypi.org/project/micro-javascript/)
[![Changelog](https://img.shields.io/github/v/release/simonw/micro-javascript?include_prereleases&label=changelog)](https://github.com/simonw/micro-javascript/releases)
[![Tests](https://github.com/simonw/micro-javascript/workflows/Test/badge.svg)](https://github.com/simonw/micro-javascript/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/simonw/micro-javascript/blob/main/LICENSE)

A pure Python JavaScript engine, inspired by [MicroQuickJS](https://github.com/bellard/mquickjs).

## Overview

This project provides a JavaScript execution environment with:

- **Memory limits** - Configurable maximum memory usage
- **Time limits** - Configurable execution timeout
- **Pure Python** - No C extensions or external dependencies
- **Broad ES5+ support** - Variables, functions, closures, classes, iterators, promises, regex, and more

> [!WARNING]
> The sandbox is **not production ready**. Malicious code can still exhaust memory and has not been fully audited against escapes that could allow JavaScript to run arbitrary Python. See the [sandbox issue label](https://github.com/simonw/micro-javascript/issues?q=label%3A%22sandbox%22) for more.

## Interactive demos

Try [playground.html](https://simonw.github.io/micro-javascript/playground.html) in your browser to execute JavaScript using this Python library run via [Pyodide](https://pyodide.org/) (so JavaScript in Python in WebAssembly in JavaScript).

Use [parser-playground.html](https://simonw.github.io/micro-javascript/parser-playground.html) to see how the `micro-javascript` tokenizer and parser works with different JavaScript code.

## How it was built

Most of this library was built using Claude Code for web - [here is the 15+ hour transcript](https://static.simonwillison.net/static/2025/claude-code-microjs/index.html).

## Installation

```bash
pip install micro-javascript
```

## Usage

```python
from microjs import Context

# Create a context with optional limits
ctx = Context(memory_limit=1024*1024, time_limit=5.0)

# Evaluate JavaScript code
result = ctx.eval("1 + 2")  # Returns 3

# Functions and closures
ctx.eval("""
    function makeCounter() {
        var count = 0;
        return function() { return ++count; };
    }
    var counter = makeCounter();
""")
assert ctx.eval("counter()") == 1
assert ctx.eval("counter()") == 2

# Regular expressions
result = ctx.eval('/hello (\\w+)/.exec("hello world")')
# Returns ['hello world', 'world']

# Error handling with line/column tracking
ctx.eval("""
try {
    throw new Error("oops");
} catch (e) {
    // e.lineNumber and e.columnNumber are set
}
""")
```

## Setting and Getting Variables

Use `set()` and `get()` to pass values between Python and JavaScript:

```python
ctx = Context()

# Set a Python value as a JavaScript global variable
ctx.set("x", 42)
ctx.set("name", "Alice")
ctx.set("items", [1, 2, 3])

# Use the variable in JavaScript
result = ctx.eval("x * 2")  # Returns 84
result = ctx.eval("'Hello, ' + name")  # Returns 'Hello, Alice'
result = ctx.eval("items.map(n => n * 2)")  # Returns [2, 4, 6]

# Get a JavaScript variable back into Python
ctx.eval("var total = items.reduce((a, b) => a + b, 0)")
total = ctx.get("total")  # Returns 6
```

## Exposing Python Functions to JavaScript

You can expose Python functions to JavaScript by setting them as global variables:

```python
ctx = Context()

# Define a Python function
def add(a, b):
    return a + b

# Expose it to JavaScript
ctx.set("add", add)

# Call it from JavaScript
result = ctx.eval("add(2, 3)")  # Returns 5
```

Primitive values (numbers, strings, booleans) are passed directly as Python types, and primitives returned from Python functions work in JavaScript.

Arrays and objects are passed as internal JavaScript types (`JSArray`, `JSObject`). To return objects that JavaScript can use, return `JSObject` instances:

```python
from microjs.values import JSObject, JSArray

ctx = Context()

# Access array elements via ._elements
def sum_array(arr):
    return sum(arr._elements)

ctx.set("sumArray", sum_array)
result = ctx.eval("sumArray([1, 2, 3, 4, 5])")  # Returns 15

# Return a JSObject for JavaScript to use
def make_point(x, y):
    obj = JSObject()
    obj.set("x", x)
    obj.set("y", y)
    return obj

ctx.set("makePoint", make_point)
result = ctx.eval("var p = makePoint(10, 20); p.x + p.y;")  # Returns 30
```

## Supported Features

- **Core**: variables, operators, control flow, functions, closures
- **Objects**: object literals, prototypes, getters/setters, JSON
- **Arrays**: literals, methods (map, filter, reduce, etc.), typed arrays
- **Functions**: arrow functions, rest/spread, default parameters
- **Classes**: class syntax, inheritance, static methods
- **Iteration**: for-of, iterators, generators
- **Async**: Promises, async/await
- **Regex**: Full regex support with capture groups, lookahead/lookbehind
- **Error handling**: try/catch/finally with stack traces

## Known Limitations

See [open-problems.md](https://github.com/simonw/micro-javascript/blob/main/open-problems.md) for details on:
- Deep nesting limits (parser uses recursion)
- Some regex edge cases with optional lookahead captures
- Error constructor location tracking

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Run tests
uv run pytest
```

## License

MIT License - see [LICENSE](https://github.com/simonw/micro-javascript/blob/main/LICENSE) file.

Based on MicroQuickJS by Fabrice Bellard.
