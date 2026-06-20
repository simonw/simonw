# sqlite-ast-conformance

A language-independent conformance suite for implementations of a SQLite SELECT query parser.

The `sqlite_ast_conformance/ast-tests/` directory contains JSON files, each defining a SQL query and its expected abstract syntax tree (AST). These test fixtures are generated using the **official SQLite parser** so they represent ground truth for how SQLite parses SELECT statements.

The package is available on PyPI, so you can install it and access the test fixtures programmatically:

```bash
pip install sqlite-ast-conformance
```

```python
from sqlite_ast_conformance import AST_TESTS_DIR

for test_file in sorted(AST_TESTS_DIR.glob("*.json")):
    print(test_file.name)
```

## How it works

The ASTs represent the **raw parse tree** produced by SQLite's Lemon parser, captured *before* any name resolution or `SELECT *` expansion. This means:

- `SELECT *` produces `{"type": "star"}` — no schema knowledge needed
- `SELECT foo.bar` produces a `dot` node with `name` children — no table lookups
- All tests run against an in-memory database with no tables

## Test file format

Each JSON file in `sqlite_ast_conformance/ast-tests/` has two keys:

```json
{
  "sql": "SELECT 1 + 2",
  "ast": {
    "type": "select",
    "distinct": false,
    "all": false,
    "columns": [
      {
        "expr": {
          "type": "binary",
          "op": "+",
          "left": {"type": "integer", "value": 1},
          "right": {"type": "integer", "value": 2}
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
}
```

## Building and running the reference tests

### Prerequisites

- GCC (or compatible C compiler)
- Python 3.10+ and [uv](https://docs.astral.sh/uv/)
- Git

### 1. Clone the SQLite source

```bash
git clone --depth 1 https://github.com/sqlite/sqlite.git sqlite-src
```

### 2. Build the SQLite amalgamation

```bash
cd sqlite-src
./configure
make sqlite3.c
cd ..
```

### 3. Build the `dump_ast` tool

```bash
make
```

This patches the SQLite amalgamation to insert an AST capture hook into the parser's grammar action for `cmd ::= select`, then compiles `dump_ast.c` which includes the patched amalgamation and provides a JSON serializer for the AST.

### 4. Run the conformance tests

```bash
uv run pytest -v
```

This runs `test_ast.py` which loads every JSON file from `sqlite_ast_conformance/ast-tests/`, calls `dump_ast` with the SQL, and compares the output to the expected AST.

### 5. Try individual queries

```bash
./build/dump_ast "SELECT * FROM foo WHERE x > 5 ORDER BY y"
```

## Generating new test fixtures

```bash
python generate_test.py <name> "<sql>"
# Example:
python generate_test.py my_test "SELECT a, b FROM t WHERE a > 1"
```

This creates `sqlite_ast_conformance/ast-tests/my_test.json` using `dump_ast` to generate the expected AST.

## AST node types

### Expressions

| Type | Description | Key fields |
|------|-------------|------------|
| `integer` | Integer literal | `value` |
| `float` | Float literal | `value` (string) |
| `string` | String literal | `value` |
| `blob` | Blob literal | `value` |
| `null` | NULL | — |
| `boolean` | TRUE/FALSE | `value` |
| `name` | Identifier | `name` |
| `star` | Wildcard `*` | — |
| `dot` | Qualified name `a.b` | `left`, `right` |
| `binary` | Binary operator | `op`, `left`, `right` |
| `unary` | Unary operator | `op`, `operand` |
| `function` | Function call | `name`, `args`, `distinct`, optional `over` |
| `cast` | CAST expression | `expr`, `as` |
| `case` | CASE expression | `operand`, `when_clauses`, `else` |
| `between` | BETWEEN | `expr`, `low`, `high` |
| `in` | IN | `expr`, `values` or `select` |
| `exists` | EXISTS | `select` |
| `subquery` | Scalar subquery | `select` |
| `collate` | COLLATE | `expr`, `collation` |
| `isnull` | IS NULL | `operand` |
| `notnull` | IS NOT NULL | `operand` |
| `truth_test` | IS TRUE/FALSE | `op`, `operand` |
| `parameter` | Bind parameter | `name` |

### SELECT

```
type: "select"
├── distinct: bool
├── all: bool
├── with: [...CTEs...]
├── columns: [{expr, alias}, ...]
├── from: [{type: "table"/"subquery", ...}, ...]
├── where: expr
├── group_by: [expr, ...]
├── having: expr
├── window_definitions: [...]
├── order_by: [{expr, direction, nulls}, ...]
├── limit: expr
└── offset: expr
```

Compound selects (`UNION`, `INTERSECT`, `EXCEPT`) use `type: "compound"` with a `body` array.

## Using these tests in your own parser

To test your own SQLite parser implementation:

1. Read each JSON file from `sqlite_ast_conformance/ast-tests/`
2. Parse the `sql` field with your parser
3. Compare your AST output against the `ast` field
4. The exact JSON structure must match — field names, nesting, and values

The test fixtures are pure JSON with no dependencies, so they can be consumed by any programming language.
