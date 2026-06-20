# sqlite-ast

[![PyPI](https://img.shields.io/pypi/v/sqlite-ast.svg)](https://pypi.org/project/sqlite-ast/)
[![Tests](https://github.com/simonw/sqlite-ast/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/sqlite-ast/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-ast?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-ast/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-ast/blob/main/LICENSE)

Python library for parsing SQLite SELECT queries into an AST

## Installation

Install this library using `pip`:
```bash
pip install sqlite-ast
```
## Demo

You can try this library out in your browser (via Pyodide) at [tools.simonwillison.net/sqlite-ast](https://tools.simonwillison.net/sqlite-ast).

## Usage

The main entry point is `parse(sql)`, which returns a nested Python dictionary:

<!-- [[[cog
import io
from pathlib import Path
from contextlib import redirect_stdout

def render_example(path_str: str, output_lang: str = "text") -> None:
    path = Path(path_str)
    code = path.read_text().rstrip()

    cog.outl("```python")
    cog.outl(code)
    cog.outl("```")

    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(compile(code, str(path), "exec"), {})

    cog.outl(f"```{output_lang}")
    cog.outl(buf.getvalue().rstrip())
    cog.outl("```")

render_example("examples/parse_basic.py", "text")
]]] -->
```python
from sqlite_ast import parse

ast = parse("select 1")
print(ast)
```
```text
{'type': 'select', 'distinct': False, 'all': False, 'columns': [{'expr': {'type': 'integer', 'value': 1}, 'alias': None}], 'from': None, 'where': None, 'group_by': None, 'having': None, 'order_by': None, 'limit': None}
```
<!-- [[[end]]] -->

You can pretty-print that dictionary as JSON:

<!-- [[[cog
render_example("examples/parse_json.py", "json")
]]] -->
```python
import json
from sqlite_ast import parse

ast = parse("select 1")
print(json.dumps(ast, indent=2))
```
```json
{
  "type": "select",
  "distinct": false,
  "all": false,
  "columns": [
    {
      "expr": {
        "type": "integer",
        "value": 1
      },
      "alias": null
    }
  ],
  "from": null,
  "where": null,
  "group_by": null,
  "having": null,
  "order_by": null,
  "limit": null
}
```
<!-- [[[end]]] -->

If you want structured dataclass nodes instead of dictionaries, use `parse_ast(sql)`:

<!-- [[[cog
render_example("examples/parse_ast.py", "text")
]]] -->
```python
from pprint import pprint
from sqlite_ast import parse_ast

node = parse_ast("select 1")
pprint(node)
```
```text
Select(distinct=False,
       all=False,
       with_ctes=None,
       columns=[ResultColumn(expr=IntegerLiteral(value=1), alias=None)],
       from_clause=None,
       where=None,
       group_by=None,
       having=None,
       window_definitions=None,
       order_by=None,
       limit=None,
       offset=None,
       _has_limit=False,
       _compound_member=False)
```
<!-- [[[end]]] -->

Parse failures raise `ParseError`:

<!-- [[[cog
render_example("examples/parse_error.py", "text")
]]] -->
```python
from pprint import pprint
from sqlite_ast import parse, ParseError

try:
    parse("select 1 union select")
except ParseError as e:
    print(e)
    print("\nPartial AST:")
    pprint(e.partial_ast)
```
```text
Parse error at position 21: Unexpected token in expression: EOF ('')

Partial AST:
Select(distinct=False,
       all=False,
       with_ctes=None,
       columns=[ResultColumn(expr=IntegerLiteral(value=1), alias=None)],
       from_clause=None,
       where=None,
       group_by=None,
       having=None,
       window_definitions=None,
       order_by=None,
       limit=None,
       offset=None,
       _has_limit=False,
       _compound_member=True)
```
<!-- [[[end]]] -->

## Development

To contribute to this library, first checkout the code. Then run the tests with [uv](https://github.com/astral-sh/uv):
```bash
cd sqlite-ast
uv run pytest
```
