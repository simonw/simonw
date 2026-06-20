# datasette-transactions

[![PyPI](https://img.shields.io/pypi/v/datasette-transactions.svg)](https://pypi.org/project/datasette-transactions/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-transactions?include_prereleases&label=changelog)](https://github.com/datasette/datasette-transactions/releases)
[![Tests](https://github.com/datasette/datasette-transactions/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-transactions/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-transactions/blob/main/LICENSE)

A Datasette plugin providing an API for executing multiple SQL commands within a single transaction, with support for SQLite authorization callbacks to control table-level read/write access.

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-transactions
```

## Usage

### Begin a Transaction

```http
POST /-/transactions/begin/<database>
Content-Type: application/json

{
  "read": ["table1", "table2"],
  "write": ["table1"],
  "timeout_ms": 5000
}
```

**Parameters:**
- `read`: List of tables the transaction can read from
- `write`: List of tables the transaction can write to
- `timeout_ms`: Optional timeout in milliseconds (transaction auto-rolls back after this time)

**Response:**
```json
{
  "ok": true,
  "transaction_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Required Permissions:**
- `execute-sql` on the database
- `view-table` on each table in the `read` list
- `insert-row` and `update-row` on each table in the `write` list

### Execute SQL

```http
POST /-/transactions/<transaction_id>
Content-Type: application/json

{
  "sql": "INSERT INTO table1 (name) VALUES (:name)",
  "params": {"name": "Alice"}
}
```

**Response:**
```json
{
  "ok": true,
  "rows": [],
  "columns": [],
  "truncated": false
}
```

For SELECT queries, `rows` contains the results as a list of objects.

### Create a Savepoint

```http
POST /-/transactions/<transaction_id>/savepoint
Content-Type: application/json

{
  "name": "before_batch"
}
```

**Response:**
```json
{
  "ok": true,
  "savepoint": "before_batch"
}
```

### Release a Savepoint

```http
POST /-/transactions/<transaction_id>/release
Content-Type: application/json

{
  "name": "before_batch"
}
```

### Rollback to a Savepoint

```http
POST /-/transactions/<transaction_id>/rollback-to
Content-Type: application/json

{
  "name": "before_batch"
}
```

### Commit a Transaction

```http
POST /-/transactions/commit/<transaction_id>
```

**Response:**
```json
{
  "ok": true
}
```

### Rollback a Transaction

```http
POST /-/transactions/rollback/<transaction_id>
```

**Response:**
```json
{
  "ok": true
}
```

## Error Codes

| Status | Meaning |
|--------|---------|
| 400 | Bad request (invalid JSON, missing parameters, SQL error) |
| 403 | Permission denied (missing required permissions, table access denied) |
| 404 | Transaction or savepoint not found |
| 405 | Method not allowed (use POST) |
| 410 | Transaction expired (timed out) |
| 429 | Too many concurrent transactions (max 5 per database) |

## Authorization

The plugin uses SQLite's `set_authorizer()` callback to enforce table-level permissions:

- Reading from tables not in `read` list is blocked
- Writing to tables not in `write` list is blocked
- `ATTACH DATABASE` is always blocked

## Concurrency

- Maximum 5 concurrent transactions per database
- Read-only transactions use `BEGIN DEFERRED` (allows concurrent reads)
- Write transactions use `BEGIN IMMEDIATE` (exclusive lock)

## Example: Batch Insert with Rollback on Error

```python
import httpx

# Begin transaction
response = httpx.post(
    "http://localhost:8001/-/transactions/begin/mydb",
    json={"read": ["users"], "write": ["users"]}
)
tx_id = response.json()["transaction_id"]

try:
    # Insert multiple rows
    for user in users:
        httpx.post(
            f"http://localhost:8001/-/transactions/{tx_id}",
            json={
                "sql": "INSERT INTO users (name, email) VALUES (:name, :email)",
                "params": user
            }
        )

    # Commit if all succeeded
    httpx.post(f"http://localhost:8001/-/transactions/commit/{tx_id}")
except Exception:
    # Rollback on error
    httpx.post(f"http://localhost:8001/-/transactions/rollback/{tx_id}")
    raise
```

## Python Client Library

The plugin includes a Python client library with both synchronous and asynchronous support. The client provides a cleaner API than raw HTTP calls and includes automatic transaction lifecycle management.

### Basic Usage (Sync)

```python
import httpx
from datasette_transactions.client import TransactionsClient

with httpx.Client(base_url="http://localhost:8001") as http:
    client = TransactionsClient(http)

    # Using context manager (recommended) - auto-commits on success, auto-rolls back on exception
    with client.transaction("mydb", read=["users"], write=["users"]) as tx:
        tx.execute("INSERT INTO users (name) VALUES (:name)", {"name": "Alice"})
        result = tx.execute("SELECT * FROM users")
        print(result.rows)  # [{"id": 1, "name": "Alice"}]
```

### Basic Usage (Async)

```python
import httpx
from datasette_transactions.client import AsyncTransactionsClient

async with httpx.AsyncClient(base_url="http://localhost:8001") as http:
    client = AsyncTransactionsClient(http)

    async with client.transaction("mydb", read=["users"], write=["users"]) as tx:
        await tx.execute("INSERT INTO users (name) VALUES (:name)", {"name": "Alice"})
        result = await tx.execute("SELECT * FROM users")
        print(result.rows)
```

### Manual Transaction Management

For finer control, you can manage transactions manually:

```python
import httpx
from datasette_transactions.client import TransactionsClient

with httpx.Client(base_url="http://localhost:8001") as http:
    client = TransactionsClient(http)

    tx_id = client.begin("mydb", read=["users"], write=["users"], timeout_ms=5000)
    try:
        client.execute(tx_id, "INSERT INTO users (name) VALUES ('Bob')")
        client.execute(tx_id, "INSERT INTO users (name) VALUES ('Carol')")
        client.commit(tx_id)
    except Exception:
        client.rollback(tx_id)
        raise
```

### Using Savepoints

Savepoints allow partial rollbacks within a transaction:

```python
with client.transaction("mydb", write=["users"]) as tx:
    tx.execute("INSERT INTO users (name) VALUES ('Alice')")

    tx.savepoint("before_bob")
    tx.execute("INSERT INTO users (name) VALUES ('Bob')")

    # Oops, rollback just Bob's insert
    tx.rollback_to("before_bob")

    tx.execute("INSERT INTO users (name) VALUES ('Carol')")
    # Commits with Alice and Carol, but not Bob
```

### Exception Handling

The client provides specific exception types for different error conditions:

```python
from datasette_transactions.client import (
    TransactionsClient,
    TransactionError,           # Base exception
    TransactionNotFoundError,   # Transaction doesn't exist (404)
    TransactionExpiredError,    # Transaction timed out (410)
    PermissionDeniedError,      # Access denied (403)
    TooManyTransactionsError,   # Max concurrent transactions (429)
    DatabaseNotFoundError,      # Database doesn't exist (404)
    DatabaseImmutableError,     # Database is read-only (400)
    SQLError,                   # SQL execution failed (400)
    SavepointExistsError,       # Savepoint name already used (400)
    SavepointNotFoundError,     # Savepoint doesn't exist (404)
)

try:
    with client.transaction("mydb", write=["users"]) as tx:
        tx.execute("INSERT INTO users (name) VALUES ('Alice')")
except PermissionDeniedError as e:
    print(f"Access denied: {e.message}")
except TransactionExpiredError:
    print("Transaction timed out")
except SQLError as e:
    print(f"SQL error: {e.message}")
```

### ExecuteResult

The `execute()` method returns an `ExecuteResult` dataclass:

```python
result = tx.execute("SELECT * FROM users WHERE active = :active", {"active": True})

result.ok        # True if successful
result.rows      # List of dicts: [{"id": 1, "name": "Alice", "active": True}, ...]
result.columns   # List of column names: ["id", "name", "active"]
result.truncated # True if results were truncated
```

## Development

To set up this plugin locally, first checkout the code:
```bash
cd datasette-transactions
uv run pytest  # Run tests
```

This project follows TDD (Test-Driven Development). See `CLAUDE.md` for development guidelines.
