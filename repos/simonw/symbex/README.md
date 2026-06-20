# Symbex

[![PyPI](https://img.shields.io/pypi/v/symbex.svg)](https://pypi.org/project/symbex/)
[![Changelog](https://img.shields.io/github/v/release/simonw/symbex?include_prereleases&label=changelog)](https://github.com/simonw/symbex/releases)
[![Tests](https://github.com/simonw/symbex/workflows/Test/badge.svg)](https://github.com/simonw/symbex/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/symbex/blob/master/LICENSE)

Find the Python code for specified symbols

Read [Symbex: search Python code for functions and classes, then pipe them into a LLM](https://simonwillison.net/2023/Jun/18/symbex/) for background on this project.

## Installation

Install this tool using `pip`:
```bash
pip install symbex
```
Or using Homebrew:
```bash
brew install simonw/llm/symbex
```
## Usage

`symbex` can search for names of functions and classes that occur at the top level of a Python file.

To search every `.py` file in your current directory and all subdirectories, run like this:

```bash
symbex my_function
```
You can search for more than one symbol at a time:
```bash
symbex my_function MyClass
```
Wildcards are supported - to search for every `test_` function run this (note the single quotes to avoid the shell interpreting the `*` as a wildcard):
```bash
symbex 'test_*'
```
To search for methods within classes, use `class.method` notation:
```bash
symbex Entry.get_absolute_url
```
Wildcards are supported here as well:
```bash
symbex 'Entry.*'
symbex '*.get_absolute_url'
symbex '*.get_*'
```
Or to view every method of every class:
```bash
symbex '*.*'
```
To search within a specific file, pass that file using the `-f` option. You can pass this more than once to search multiple files.

```bash
symbex MyClass -f my_file.py
```
To search within a specific directory and all of its subdirectories, use the `-d/--directory` option:
```bash
symbex Database -d ~/projects/datasette
```
If you know that you want to inspect one or more modules that can be imported by Python, you can use the `-m/--module name` option. This example shows the signatures for every symbol available in the `asyncio` package:
```bash
symbex -m asyncio -s --imports
```
You can search the directory containing the Python standard library using `--stdlib`. This can be useful for quickly looking up the source code for specific Python library functions:
```bash
symbex --stdlib -in to_thread
```
`-in` is explained below. If you provide `--stdlib` without any `-d` or `-f` options then `--silent` will be turned on automatically, since the standard library otherwise produces a number of different warnings.

The output starts like this:
```python
# from asyncio.threads import to_thread
async def to_thread(func, /, *args, **kwargs):
    """Asynchronously run function *func* in a separate thread.
    # ...
```
You can exclude files in specified directories using the `-x/--exclude` option:
```bash
symbex Database -d ~/projects/datasette -x ~/projects/datasette/tests
```
If `symbex` encounters any Python code that it cannot parse, it will print a warning message and continue searching:
```
# Syntax error in path/badcode.py: expected ':' (<unknown>, line 1)
```
Pass `--silent` to suppress these warnings:
```bash
symbex MyClass --silent
```
### Filters

In addition to searching for symbols, you can apply filters to the results.

The following filters are available:

- `--function` - only functions
- `--class` - only classes
- `--async` - only `async def` functions
- `--unasync` - only non-async functions
- `--documented` - functions/classes that have a docstring
- `--undocumented` - functions/classes that do not have a docstring
- `--public` - functions/classes that are public - don't have a `_name` prefix (or are `__*__` methods)
- `--private` - functions/classes that are private - have a `_name` prefix and are not `__*__`
- `--dunder` - functions matching `__*__` - this should usually be used with `*.*` to find all dunder methods
- `--typed` - functions that have at least one type annotation
- `--untyped` - functions that have no type annotations
- `--partially-typed` - functions that have some type annotations but not all
- `--fully-typed` - functions that have type annotations for every argument and the return value
- `--no-init` - Exclude `__init__(self)` methods. This is useful when combined with `--fully-typed '*.*'` to avoid returning `__init__(self)` methods that would otherwise be classified as fully typed, since `__init__` doesn't need argument or return type annotations.

For example, to see the signatures of every `async def` function in your project that doesn't have any type annotations:

```bash
symbex -s --async --untyped
```

For class methods instead of functions, you can combine filters with a symbol search argument of `*.*`.

This example shows the full source code of every class method in the Python standard library that has type annotations for all of the arguments and the return value:

```bash
symbex --fully-typed --no-init '*.*' --stdlib
```

To find all public functions and methods that lack documentation, just showing the signature of each one:

```bash
symbex '*' '*.*' --public --undocumented --signatures
```

### Example output

In a fresh checkout of [Datasette](https://github.com/simonw/datasette) I ran this command:

```bash
symbex MessagesDebugView get_long_description
```
Here's the output of the command:
```python
# File: setup.py Line: 5
def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()

# File: datasette/views/special.py Line: 60
class PatternPortfolioView(View):
    async def get(self, request, datasette):
        await datasette.ensure_permissions(request.actor, ["view-instance"])
        return Response.html(
            await datasette.render_template(
                "patterns.html",
                request=request,
                view_name="patterns",
            )
        )
```
### Just the signatures

The `-s/--signatures` option will list just the signatures of the functions and classes, for example:
```bash
symbex -s -f symbex/lib.py
```
<!-- [[[cog
import cog
from click.testing import CliRunner
import pathlib
from symbex.cli import cli

def sorted_chunks(text):
    chunks = text.strip().split("\n\n")
    chunks.sort()
    return "\n\n".join(chunks)

path = pathlib.Path("symbex").resolve()
runner = CliRunner()
result = runner.invoke(cli, ["-s", "-f", str(path / "lib.py")])
cog.out(
    "```python\n{}\n```\n".format(sorted_chunks(result.output))
)
]]] -->
```python
# File: symbex/lib.py Line: 107
def function_definition(function_node: AST):

# File: symbex/lib.py Line: 13
def find_symbol_nodes(code: str, filename: str, symbols: Iterable[str]) -> List[Tuple[(AST, Optional[str])]]:

# File: symbex/lib.py Line: 175
def class_definition(class_def):

# File: symbex/lib.py Line: 209
def annotation_definition(annotation: AST) -> str:

# File: symbex/lib.py Line: 227
def read_file(path):

# File: symbex/lib.py Line: 253
class TypeSummary:

# File: symbex/lib.py Line: 258
def type_summary(node: AST) -> Optional[TypeSummary]:

# File: symbex/lib.py Line: 304
def quoted_string(s):

# File: symbex/lib.py Line: 315
def import_line_for_function(function_name: str, filepath: str, possible_root_dirs: List[str]) -> str:

# File: symbex/lib.py Line: 37
def code_for_node(code: str, node: AST, class_name: str, signatures: bool, docstrings: bool) -> Tuple[(str, int)]:

# File: symbex/lib.py Line: 71
def add_docstring(definition: str, node: AST, docstrings: bool, is_method: bool) -> str:

# File: symbex/lib.py Line: 82
def match(name: str, symbols: Iterable[str]) -> bool:
```
<!-- [[[end]]] -->
This can be combined with other options, or you can run `symbex -s` to see every symbol in the current directory and its subdirectories.

To include estimated import paths, such as `# from symbex.lib import match`, use `--imports`. These will be calculated relative to the directory you specified, or you can pass one or more `--sys-path` options to request that imports are calculated relative to those directories as if they were on `sys.path`:

```bash
~/dev/symbex/symbex match --imports -s --sys-path ~/dev/symbex
```
Example output:
<!-- [[[cog
result = runner.invoke(cli, [
    "--imports", "-d", str(path), "match", "-s", "--sys-path", str(path.parent)
])
cog.out(
    "```python\n{}\n```\n".format(result.stdout.strip())
)
]]] -->
```python
# File: symbex/lib.py Line: 82
# from symbex.lib import match
def match(name: str, symbols: Iterable[str]) -> bool:
```
<!-- [[[end]]] -->
To suppress the `# File: ...` comments, use `--no-file` or `-n`.

So to both show import paths and suppress File comments, use `-in` as a shortcut:
```bash
symbex -in match
```
Output:
<!-- [[[cog
result = runner.invoke(cli, [
    "-in", "-d", str(path), "match", "-s", "--sys-path", str(path.parent)
])
cog.out(
    "```python\n{}\n```\n".format(result.stdout.strip())
)
]]] -->
```python
# from symbex.lib import match
def match(name: str, symbols: Iterable[str]) -> bool:
```
<!-- [[[end]]] -->

To include docstrings in those signatures, use `--docstrings`:
```bash
symbex match --docstrings -f symbex/lib.py
```
Example output:
<!-- [[[cog
result = runner.invoke(cli, ["match", "--docstrings", "-f", str(path / "lib.py")])
cog.out(
    "```python\n{}\n```\n".format(result.stdout.strip())
)
]]] -->
```python
# File: symbex/lib.py Line: 82
def match(name: str, symbols: Iterable[str]) -> bool:
    "Returns True if name matches any of the symbols, resolving wildcards"
```
<!-- [[[end]]] -->

## Counting symbols

If you just want to count the number of functions and classes that match your filters, use the `--count` option. Here's how to count your classes:

```bash
symbex --class --count
```
Or to count every async test function:
```bash
symbex --async 'test_*' --count
```
## Structured output

LLM defaults to outputting plain text (actually valid Python code, thanks to the way it uses comments).

You can request output in CSV, TSV, JSON or newline-delimited JSON instead, using the following options:

- `--json`: a JSON array, `[{"id": "...", "code": "..."}]`
- `--nl`: newline-delimited JSON, `{"id": "...", "code": "..."}` per line
- `--csv`: CSV with `id,code` as the heading row
- `--tsv`: TSV with `id\tcode` as the heading row

In each case the ID will be the path to the file containing the symbol, followed by a colon, followed by the line number of the symbol, for example:

```json
{
  "id": "symbex/lib.py:82",
  "code": "def match(name: str, symbols: Iterable[str]) -> bool:"
}
```
If you pass `-i/--imports` the ID will be the import line instead:
```json
{
  "id": "from symbex.lib import match",
  "code": "def match(name: str, symbols: Iterable[str]) -> bool:"
}
```
Pass `--id-prefix 'something:'` to add the specified prefix to the start of each ID.

This example will generate a CSV file of all of your test functions, using the import style of IDs and a prefix of `test:`:

```bash
symbex 'test_*' \
  --function \
  --imports \
  --csv > tests.csv
```

## Using with LLM

This tool is primarily designed to be used with [LLM](https://llm.datasette.io/), a CLI tool for working with Large Language Models.

`symbex` makes it easy to grab a specific class or function and pass it to the `llm` command.

For example, I ran this in the Datasette repository root:

```bash
symbex Response | llm --system 'Explain this code, succinctly'
```
And got back this:

> This code defines a custom `Response` class with methods for returning HTTP responses. It includes methods for setting cookies, returning HTML, text, and JSON responses, and redirecting to a different URL. The `asgi_send` method sends the response to the client using the ASGI (Asynchronous Server Gateway Interface) protocol.

The structured output feature is designed to be used with [LLM embeddings](https://llm.datasette.io/en/stable/embeddings/index.html). You can generate embeddings for every symbol in your codebase using [llm embed-multi](https://llm.datasette.io/en/stable/embeddings/cli.html#llm-embed-multi) like this:

```bash
symbex '*' '*:*' --nl | \
  llm embed-multi symbols - \
  --format nl --database embeddings.db --store
```
This creates a database in `embeddings.db` containing all of your symbols along with embedding vectors.

You can then search your code like this:
```bash
llm similar symbols -d embeddings.db -c 'test csv' | jq
```

## Replacing a matched symbol

The `--replace` option can be used to replace a single matched symbol with content piped in to standard input.

Given a file called `my_code.py` with the following content:
```python
def first_function():
    # This will be ignored
    pass

def second_function():
    # This will be replaced
    pass
```
Run the following:
```bash
echo "def second_function(a, b):
    # This is a replacement implementation
    return a + b + 3
" | symbex second_function --replace
```
The result will be an updated-in-place `my_code.py` containing the following:

```python
def first_function():
    # This will be ignored
    pass

def second_function(a, b):
    # This is a replacement implementation
    return a + b + 3
```
This feature should be used with care! I recommend only using this feature against code that is already checked into Git, so you can review changes it makes using `git diff` and revert them using `git checkout my_code.py`.

## Replacing a matched symbol by running a command

The `--rexec COMMAND` option can be used to replace a single matched symbol by running a command and using its output.

The command will be run with the matched symbol's definition piped to its standard input. The output of that command will be used as the replacement text.

Here's an example that uses `sed` to add a `# ` to the beginning of each matching line, effectively commenting out the matched function:

```bash
symbex first_function --rexec "sed 's/^/# /'"
```
This modified the first function in place to look like this:
```python
# def first_function():
#    # This will be ignored
#    pass
```
A much more exciting example uses LLM. This example will use the `gpt-3.5-turbo` model to add type hints and generate a docstring:

```bash
symbex second_function \
  --rexec "llm --system 'add type hints and a docstring'"
```
I ran this against this code:
```python
def first_function():
    # This will be ignored
    pass

def second_function(a, b):
    return a + b + 3
```
And the second function was updated in place to look like this:
```python
def second_function(a: int, b: int) -> int:
    """
    Returns the sum of two integers (a and b) plus 3.

    Parameters:
    a (int): The first integer.
    b (int): The second integer.

    Returns:
    int: The sum of a and b plus 3.
    """
    return a + b + 3
```
## Using in CI

The `--check` option causes `symbex` to return a non-zero exit code if any matches are found for your query.

You can use this in CI to guard against things like public functions being added without documentation:

```bash
symbex --function --public --undocumented --check
```
This will fail silently but set a `1` exit code if there are any undocumented functions.

Using this as a step in a CI tool such as GitHub Actions should result in a test failure.

Run this to see the exit code from the last command:
```bash
echo $?
```

`--check` will not output anything by default. Add `--count` to output a count of matching symbols, or `-s/--signatures` to output the signatures of the matching symbols, for example:
```bash
symbex --function --public --undocumented --check --count
```

## Similar tools

- [pyastgrep](https://github.com/spookylukey/pyastgrep) by Luke Plant offers advanced capabilities for viewing and searching through Python ASTs using XPath.
- [cq](https://github.com/fullstackio/cq) is a tool thet lets you "extract code snippets using CSS-like selectors", built using [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) and primarily targetting JavaScript and TypeScript.

## symbex --help

<!-- [[[cog
result2 = runner.invoke(cli, ["--help"])
help = result2.output.replace("Usage: cli", "Usage: symbex")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: symbex [OPTIONS] [SYMBOLS]...

  Find symbols in Python code and print the code for them.

  Example usage:

      # Search current directory and subdirectories
      symbex my_function MyClass

      # Search using a wildcard
      symbex 'test_*'

      # Find a specific class method
      symbex 'MyClass.my_method'

      # Find class methods using wildcards
      symbex '*View.handle_*'

      # Search a specific file
      symbex MyClass -f my_file.py

      # Search within a specific directory and its subdirectories
      symbex Database -d ~/projects/datasette

      # View signatures for all symbols in current directory and subdirectories
      symbex -s

      # View signatures for all test functions
      symbex 'test_*' -s

      # View signatures for all async functions with type definitions
      symbex --async --typed -s

      # Count the number of --async functions in the project
      symbex --async --count

      # Replace my_function with a new implementation:
      echo "def my_function(a, b):
          # This is a replacement implementation
          return a + b + 3
      " | symbex my_function --replace

      # Replace my_function with the output of a command:
      symbex first_function --rexec "sed 's/^/# /'"
      # This uses sed to comment out the function body

Options:
  --version                  Show the version and exit.
  -f, --file FILE            Files to search
  -d, --directory DIRECTORY  Directories to search
  --stdlib                   Search the Python standard library
  -x, --exclude DIRECTORY    Directories to exclude
  -s, --signatures           Show just function and class signatures
  -n, --no-file              Don't include the # File: comments in the output
  -i, --imports              Show 'from x import y' lines for imported symbols
  -m, --module TEXT          Modules to search within
  --sys-path TEXT            Calculate imports relative to these on sys.path
  --docs, --docstrings       Show function and class signatures plus docstrings
  --count                    Show count of matching symbols
  --silent                   Silently ignore Python files with parse errors
  --function                 Filter functions
  --async                    Filter async functions
  --unasync                  Filter non-async functions
  --class                    Filter classes
  --documented               Filter functions with docstrings
  --undocumented             Filter functions without docstrings
  --public                   Filter for symbols without a _ prefix
  --private                  Filter for symbols with a _ prefix
  --dunder                   Filter for symbols matching __*__
  --typed                    Filter functions with type annotations
  --untyped                  Filter functions without type annotations
  --partially-typed          Filter functions with partial type annotations
  --fully-typed              Filter functions with full type annotations
  --no-init                  Filter to exclude any __init__ methods
  --check                    Exit with non-zero code if any matches found
  --replace                  Replace matching symbol with text from stdin
  --rexec TEXT               Replace with the result of piping to this tool
  --csv                      Output as CSV
  --tsv                      Output as TSV
  --json                     Output as JSON
  --nl                       Output as newline-delimited JSON
  --id-prefix TEXT           Prefix to use for symbol IDs
  --help                     Show this message and exit.

```
<!-- [[[end]]] -->

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd symbex
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
### just

You can also install [just](https://github.com/casey/just) and use it to run the tests and linters like this:

```bash
just
```
Or to list commands:
```bash
just -l
```
```
Available recipes:
    black         # Apply Black
    cog           # Rebuild docs with cog
    default       # Run tests and linters
    lint          # Run linters
    test *options # Run pytest with supplied options
```
