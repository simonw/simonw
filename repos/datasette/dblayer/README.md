# dblayer
Experimental prototype for a new Database backend abstraction

The design is described in [dblayer-prototype-spec.md](dblayer-prototype-spec.md).
Milestone 1 (core API and the in-process SQLite backend) is implemented.

## Running the tests

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12 or later:

```bash
uv run pytest
```

- `tests/test_params.py` covers the placeholder rewriter for every target style.
- `tests/conformance/` is the backend conformance suite. Every test that takes
  the `db`, `make_db`, `backend` or `make_backend` fixture runs once per entry in
  `BACKENDS` in `tests/conftest.py`; add a backend by adding an entry there.
  Mark tests with `@pytest.mark.requires("flag")` or
  `@pytest.mark.requires_not("flag")` to skip by capability flag.
- `tests/conformance/test_sqlite_specific.py` holds tests that only make sense
  for SQLite.

### Timing

The suite must pass on a loaded machine or a shared CI runner, so tests wait
for the event they check (`helpers.wait_until`, an `asyncio.Event`, a hook)
rather than sleeping a fixed time, and idle-timeout tests move the clock by
hand (`helpers.IdleClock`). Hang guards allow `helpers.EVENTUALLY_S` (10 s).

The spec's latency promises (cancel releases the write slot within 50 ms,
DuckDB interrupts within 100 ms of the time limit, deadline expiry) are
checked by `helpers.check_latency`: the operation must complete within the
generous functional bound, and the measured figure is printed (`pytest -s`)
and listed in a "spec latencies" section at the end of the run. The spec's
tight figure is asserted only with `DBLAYER_STRICT_TIMING=1`:

```bash
DBLAYER_STRICT_TIMING=1 uv run --all-extras pytest
```

Use strict mode on a quiet machine when measuring; expect it to fail under
load.

### The C worker (experimental)

`cworker/` is a SQLite worker process written in C that speaks the worker
protocol ([docs/worker-protocol.md](docs/worker-protocol.md)) and starts in a
few milliseconds instead of ~85. Build it once (needs a C compiler, `curl`
and `unzip`; it downloads a pinned, checksummed SQLite amalgamation into the
git-ignored `cworker/vendor/`):

```bash
make -C cworker
```

Its tests (`sqlite-cworker` in the conformance suite, `tests/worker/test_cworker.py`,
the `c-worker` fault tests) skip with that command as the reason until the
binary exists. `DBLAYER_CWORKER=/path/to/dblayer-cworker` points the tests
and `SqliteCWorker` at another build; `make -C cworker SANITIZE=1` builds one
with AddressSanitizer and UBSan in `cworker/build-asan/`, and `make -C cworker
SQLITE=system BUILD=build-system` links the system `libsqlite3` instead.

The same binary has a multi-tenant mode (`--multi`: a thread per open
connection), used by `SqliteCPool(path, pool=CPool(2))` in
`dblayer/backends/sqlite_cpool.py`: a few processes shared by every
database, requests for different databases running concurrently. Its tests
are `sqlite-cpool`, `c-pool`, `tests/worker/test_cworker_multi.py`,
`tests/worker/test_cpool.py` and `tests/faults/test_cpool_blast_radius.py`;
`make -C cworker SANITIZE=thread` builds a ThreadSanitizer binary in
`cworker/build-tsan/`.

A Rust port of that worker, `sqlite-rs-worker/` (experimental; Rust and
cargo, no crates: it compiles the same pinned amalgamation with the C
worker's own compile options), runs under the same pool code as
`SqliteRustPool(path)` (`sqlite-rspool`, `dblayer/backends/sqlite_rspool.py`):

```bash
make -C sqlite-rs-worker          # also: test, clippy; nightly: tsan, asan, miri
```

`DBLAYER_RSWORKER` points at another build. The C worker's own tests
(`test_cworker.py`, `test_cworker_multi.py`, `test_cpool.py`, the blast
radius tests) run on both binaries through `tests/native_impl.py`;
`benchmarks/rspool_bench.py` compares the two.

### Exports: `db.export()` (experimental)

`db.export(sql, format="csv"|"tsv"|"json"|"ndjson")` streams a result as
bytes in the formats of [docs/export-formats.md](docs/export-formats.md).
The C worker, in-process DuckDB and PostgreSQL on psycopg serialise
natively; every other backend uses the Python fallback. Tests:
`tests/conformance/test_export.py` (every backend, native and fallback),
`tests/test_export_parity.py` (native against fallback, byte for byte),
`tests/worker/test_cworker_export.py` and `tests/worker/test_cworker_handoff.py`
(the C worker's transports, including the socket handoff). Their timing
checks are hang guards (10 s or more) and counts, never tight bounds.
Benchmark: `uv run --all-extras python -m benchmarks.export` (`--http` for
curl against the handoff server and the demo app).

### The DuckDB C++ worker (experimental)

`duckdb-cpp-worker/` is a DuckDB worker process in C++ on the official
prebuilt libduckdb (downloaded once, checksummed, into the git-ignored
`duckdb-cpp-worker/vendor/`), used by `DuckDBCppWorker`. Build it with
`make -C duckdb-cpp-worker`; its tests (`duckdb-cppworker` in the
conformance suite, `tests/worker/test_duckdb_cppworker.py`, the DuckDB
worker fault and value-type tests) skip until then.
`DBLAYER_DUCKDB_CPP_WORKER` points them at another build, such as the
sanitized one from `make -C duckdb-cpp-worker SANITIZE=1`. See
`duckdb-cpp-worker/README.md`.

### ClickHouse on chDB (experimental)

`ClickHouse` (`dblayer/backends/clickhouse.py`, extra `clickhouse`) runs
ClickHouse 26.11 embedded in the Python process through
[chDB](https://github.com/chdb-io/chdb) 4.5. chDB has no build for Python
3.15 yet (it loads a per-version pybind11 library), so use
`uv run --python 3.14 --all-extras ...`; on 3.15 its tests skip and the
demo lists it as unavailable. One chDB server per process: every
`ClickHouse` backend of a process is one ClickHouse database in one shared
data directory, and the server stops when the last connection closes.

What differs, all declared as capability flags: no transactions
(`transactions`: statements apply as they run; a rolled-back block's
writes are kept and logged), no enforced keys (`unique_constraints`: named
operations check keys themselves, plain SQL `INSERT` accepts duplicates),
no foreign keys, no separate blob type, no duplicate result column names,
no snapshot reads. Read connections run with `readonly=1`, plus dblayer's
own refusal of `INTO OUTFILE`, the scalar `file()` function and every
table function or engine that reaches files, programs or the network
(write connections too unless `allow_host_access=True`). Every database of
the process can read the others: use it for data you would put in one
server. Time limits and cancellation use `KILL QUERY`.
`engine_export=True` lets ClickHouse write CSV and JSON exports itself
(about 8x faster, parse-equal rather than byte-identical to the Python
encoder). Tests: `clickhouse` in the conformance suite and
`tests/test_clickhouse_backend.py`. `benchmarks/clickhouse.py` compares it
with DuckDB and SQLite (provisional, under load: group by over 10 million
rows 48 ms against DuckDB's 24 ms and SQLite's 3.2 s; a point read 4 ms
against 1.5 and 0.8 ms).

### In-process SQLite on apsw (experimental)

`SqliteApsw` (`dblayer/backends/sqlite_apsw.py`, extra `apsw`) is the
in-process backend on [apsw](https://rogerbinns.github.io/apsw/), which
bundles its own current SQLite. It adds declared result column types, exact
change counts, an opt-in `untrusted=True` lockdown for user SQL, a heap limit
(process-wide), and opt-in `inline_reads=True`, which runs cheap reads on the
event loop thread instead of hopping to the executor. Its tests are
`sqlite-apsw` in the conformance suite and `tests/test_sqlite_apsw.py`; both
skip without apsw. `DBLAYER_APSW_INLINE=1 uv run --all-extras pytest` runs the
suite with inline reads on.

### SQLite in WebAssembly (experimental)

`SqliteWasm(path, memory_limit_mb=...)` (`dblayer/backends/sqlite_wasm.py`,
extra `wasm`) runs the C worker's code and SQLite compiled to WebAssembly,
in this process under wasmtime: an exact memory cap per instance and a
hard stop for queries no progress handler can reach, without a process.
Build the module (downloads a pinned, checksummed wasi-sdk into
`cworker/vendor/` the first time, then about 10 s):

```bash
make -C cworker wasm
```

Its tests are `sqlite-wasm` in the conformance suite, `tests/test_sqlite_wasm.py`,
`tests/faults/test_wasm_faults.py` and `tests/faults/test_wasm_locking.py`;
they skip until the module is built. How locking works without WASI file
locks, and what is given up (WAL), is in `docs/sqlite-wasm.md`;
`benchmarks/wasm_overhead.py` measures it against the other SQLite backends.

### DuckDB in a Rust worker (experimental)

`duckdb-rs-worker/` is a DuckDB worker process written in Rust, linked
against the official prebuilt libduckdb 2.0.1 (the version of the Python
`duckdb` package, so files are interchangeable). It starts in about 10 ms
and costs about 2 MB before it opens a database, against about 140 ms and
45 MB for the Python DuckDB worker, and runs each connection on its own
thread. Build it (needs cargo and `curl`; it downloads the library once
into the git-ignored `duckdb-rs-worker/vendor/`, checked against a pinned
SHA-256):

```bash
make -C duckdb-rs-worker
```

`DuckDBRustWorker(path)` (`dblayer/backends/duckdb_rsworker.py`) uses it;
its tests are `duckdb-rsworker` in the conformance suite,
`tests/worker/test_duckdb_rsworker.py` and the `duckdb-rsworker` DuckDB
fault and value-type tests, which skip until the binary exists.
`DBLAYER_DUCKDB_RS_WORKER=/path/to/binary` points them at another build;
`make -C duckdb-rs-worker test` runs the Rust unit tests, including a
seeded fuzz of the frame reader and both decoders
(`DBLAYER_RS_FUZZ_ITERS` raises its count);
`benchmarks/duckdb_memory.py native` compares it with the Python and C++
workers. It passes the whole conformance suite with the same skips as
in-process DuckDB. `unsafe` is confined to `src/ffi.rs`
(`#![deny(unsafe_code)]` elsewhere). Streamed results start at once
because each connection gets a 16KB `streaming_buffer_size` (DuckDB's
10 MB default makes the C API wait seconds for an unbounded recursive
CTE's first rows); the C++ worker does the same.

### SQLite-WASM in a Node.js process (experimental)

`SqliteNodeWorker(path)` (`dblayer/backends/sqlite_nodeworker.py`) runs the
official SQLite WebAssembly build in a Node.js worker process (`nodeworker/`,
Node 22+): the WebAssembly sandbox with a memory cap, inside a process the
parent can kill. Install its pinned npm package once (no build step, no
global install):

```bash
npm ci --prefix nodeworker
```

One Node process serves every connection of a database, a thread each,
because Node cannot take the file locks native SQLite uses. While it has the
file open it holds a native `node:sqlite` lock on it, so any other SQLite
process gets `database is locked` instead of a writer it cannot see. Its tests (`sqlite-nodeworker`,
`tests/worker/test_nodeworker.py`, `tests/worker/test_nodeworker_locking.py`,
the `node-worker` fault tests) skip until the packages are installed;
`DBLAYER_NODE` and `DBLAYER_NODEWORKER` point at another `node` or script.
`benchmarks/nodeworker_bench.py` measures its start-up and memory. Details,
including what a time limit can stop inside the process, are in
[docs/worker-protocol.md](docs/worker-protocol.md#node-worker-nodeworker-sqlite-wasm).

### PostgreSQL in WebAssembly: PGlite (experimental)

`PGliteWorker(path)` (`dblayer/backends/pglite_worker.py`) is a real
PostgreSQL (PGlite 0.5.17, PostgreSQL 18.7) with no server: `path` is a data
directory, opened by a Node.js worker process (`pglite-worker/`) when the
database wakes and released when it sleeps. Install its pinned npm package
once:

```bash
npm ci --prefix pglite-worker
```

PGlite is one PostgreSQL backend in single-user mode, so a database has one
session: its pooled connections are names for it, and while one has a
transaction open the others wait (capability `concurrent_sessions` false; a
statement through `db` from the task holding the transaction raises
`NestedWriteError`). Nothing can stop a running query (it blocks Node's only
thread; `statement_timeout` never fires), so a time limit or cancel kills
the process: the open transaction is lost, requests queued behind it run on
the next process, and WAL recovery runs on the next open. An `flock` on
`path/dblayer.lock` keeps a second process out. Pass `template=` (a data
directory to copy) to create new databases in about 0.3 s instead of 1 s of
initdb. An awake database costs about 115 MB (more after big queries;
WebAssembly memory never shrinks), an empty one 40 MB of disk.

Its tests (`pglite`, `tests/worker/test_pglite_worker.py`, the `pglite` fault
and scale tests) skip until the packages are installed; `DBLAYER_NODE` and
`DBLAYER_PGLITE_WORKER` point at another `node` or script.
`benchmarks/pglite_bench.py` compares it with the psycopg backend and the
SQLite Node and C workers; the module docstring has the details.

## Demo app

`dblayer_demo/` is a small Datasette-like Starlette app built only on
dblayer's public API: a homepage listing four databases (in-process SQLite,
SQLite in a worker process, PostgreSQL, DuckDB) holding the same seeded
dataset, a page per database, paginated table pages and a read-only SQL box
(`/<database>/-/query?sql=...`, with `:name` parameters).

```bash
uv run --all-extras --group demo python -m dblayer_demo   # http://127.0.0.1:8001/
```

Options: `--port`, `--host`, `--data-dir` (default `demo-data/`, git-ignored),
`--postgres-dsn` and `--fleet-size`. PostgreSQL uses `--postgres-dsn`, else
`$DBLAYER_TEST_POSTGRES`, else `postgresql:///dblayer_test?host=/tmp` (which
connects as the current OS user, so a GUI-launched process may need the
option). It refuses any database other than `dblayer_test`, and touches only
the `dblayer_demo` schema and the fleet's `dblayer_demo_fleet_NNN` schemas. A
backend that cannot run here is listed as unavailable, with the reason.

### The fleet: 1,000 databases behind one Registry

`/-/fleet` (linked from the homepage) lists a further 1,000 databases served
through one `Registry`: 500 in-process SQLite, 200 SQLite in a C worker
process, 100 SQLite on the multi-tenant C pool (two shared processes, a
thread per connection), 100 in-process DuckDB, 50 DuckDB in a worker
process, 30 PostgreSQL schemas and 20 SQLite in a Python worker process. The
C worker and C pool members show
as unavailable, with the build command, until `make -C cworker` has run. They
share a global cap of 40 open connections, 8 threads and a 12 s idle timeout.
Every database starts cold and is built in `on_wake` on first use (a copy
of a seeded template file, or a newly seeded schema, each with its own
branch name and slice of reviews), so startup takes well under a second
once the templates exist. Each one browses like the featured four.

- The homepage, fleet page and `/-/fanout` show live stats from
  `registry.stats()` and the process (threads, open fds, RSS), also at
  `/-/stats.json`.
- `/-/fanout?n=200` runs 200 concurrent reads on databases picked with a
  Zipf-like skew and reports latency, the peak open connections against the
  cap, and how the stats moved (`n` is capped at 500; `/-/fanout.json` for
  JSON). `/-/fanout?n=100&action=evict` makes 100 asleep databases cold
  again.

Tests are in `tests/demo/`:
`uv run --all-extras --group demo pytest tests/demo`.
