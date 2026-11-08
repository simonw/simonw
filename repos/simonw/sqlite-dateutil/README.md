# sqlite-dateutil-parse

A SQLite extension, written in C, that ports [python-dateutil](https://github.com/dateutil/dateutil)'s
`dateutil.parser.parse()` to a set of SQL functions.

```sql
select dateutil_parse('Thu, 25 Sep 2003 10:49:41 -0300');
-- 2003-09-25T10:49:41-03:00

select dateutil_parse_fuzzy('Today is January 1, 2047 at 8:21:00AM');
-- 2047-01-01T08:21:00

select dateutil_parse('10/09/2003'), dateutil_parse_dayfirst('10/09/2003');
-- 2003-10-09T00:00:00 | 2003-09-10T00:00:00

select dateutil_parse('not a date');
-- NULL
```

| SQL function | Python equivalent |
| --- | --- |
| `dateutil_parse(text)` | `parse(text).isoformat()` |
| `dateutil_parse_fuzzy(text)` | `parse(text, fuzzy=True).isoformat()` |
| `dateutil_parse_dayfirst(text)` | `parse(text, dayfirst=True).isoformat()` |
| `dateutil_parse_fuzzy_dayfirst(text)` | `parse(text, fuzzy=True, dayfirst=True).isoformat()` |

The function names match the [datasette-dateutil](https://github.com/simonw/datasette-dateutil) plugin.
Where dateutil raises an exception, these functions return `NULL`. Missing fields come from
today's local date at midnight, as in dateutil (so `dateutil_parse('10:30')` is today at 10:30).
That also means the functions aren't marked deterministic.

## Building

```bash
uv run python tools/build.py    # or just: make
```

This builds `dateutil_parse.dylib` on macOS, `.so` on Linux, or `.dll` on Windows. The
build script uses only the Python standard library and picks the compiler from `$CC`, or
falls back to `cc`. On Windows it uses MSVC `cl` from a Native Tools prompt, or MinGW `gcc` /
`clang`. It compiles against the SQLite headers in `vendor/sqlite/`, never the system
headers, because some system copies (notably the macOS SDK's `sqlite3ext.h`) turn off the
loadable-extension API.

```
sqlite> .load ./dateutil_parse
sqlite> select dateutil_parse('Sep 25 2003 5pm');
2003-09-25T17:00:00
```

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
db.load_extension("./dateutil_parse")
```

The extension is `dateutil_parse.c` plus the generated `dateutil_unicode.h`. It has no
dependencies beyond the SQLite headers. The entry point is `sqlite3_dateutilparse_init`.

## Tests

```bash
uv run pytest
```

That is all you need: uv creates the environment, and the test suite compiles the extension
first whenever it is missing or older than its sources. The project is set to use only
uv-managed Pythons, because some system Pythons, such as Apple's `/usr/bin/python3`, are
built without `enable_load_extension()`. The sanitizer tests are skipped when ASan/UBSan
isn't available (for example with MSVC).

The test suite (`tests/`) is differential: for every input it checks that the SQL functions
return exactly what `dateutil.parser.parse(...).isoformat()` returns, or `NULL` where dateutil
raises. It covers:

- 190 hand-picked inputs (ISO 8601, RFC 2822, Unix `date`, numeric ambiguity, am/pm,
  `10h36m`, `GMT+3`, `-0300 (BRST)`, fuzzy sentences, NUL bytes, Unicode whitespace and
  punctuation, and many inputs that should fail), across all four functions.
- 40,000 generated inputs (token soup plus datetime-shaped strings with out-of-range parts).
- The parser core built with **AddressSanitizer + UBSan** (`tools/du_cli.c`). This runs the
  same corpus against fixed default dates (Jan 31, Feb 29, 9999-12-28, ...) to test month-end
  clamping and weekday arithmetic, plus 20,000 random byte strings with invalid UTF-8.
- Property-based tests with [Hypothesis](https://hypothesis.readthedocs.io/) (`tests/test_properties.py`):
  arbitrary Unicode, token soup, real datetimes rendered in about 20 `strftime` formats, and fuzzy
  sentences must all match dateutil. Any result must be valid ISO 8601 that parses back to itself,
  and arbitrary BLOBs must never raise an error. Failures shrink to a minimal input. Run them for
  longer with `HYPOTHESIS_PROFILE=thorough uv run pytest tests/test_properties.py`
  (20,000 examples per property).
- Limits on input size and running time, behavior in SQL queries, and the known differences below.

The parser core is also fuzzed with libFuzzer + ASan + UBSan on Linux, for 3 minutes on every
push and 30 minutes nightly in CI. See [fuzz/README.md](fuzz/README.md).

During development, a further 1.35 million generated comparisons found zero mismatches with
dateutil 2.9.0.

## Safety and performance

- **Bounded memory, no overflow.** Every token lookahead is bounds-checked. Integer parsing
  is strict and saturates at 10^15, so arithmetic can't overflow. Output goes into a
  fixed buffer through `snprintf`. There is no recursion.
- **Linear time.** One pass tokenizes and one pass parses. Inputs up to 256 bytes need no heap
  allocation. Longer inputs use one allocation, sized to the input.
- **Size cap.** Inputs over 64 KiB return `NULL` (compile with `-DDATEUTIL_MAX_INPUT=...`
  to change this).
- **Arbitrary bytes are safe.** Embedded NULs are skipped, as dateutil does. Invalid UTF-8
  is handled.
- **Exact numbers.** dateutil uses `Decimal` to avoid float rounding (its GH #427). This port
  does the same arithmetic on the decimal digits, so `1.7h` is 1:42, not 1:41.
- Registered as `SQLITE_INNOCUOUS`.

One machine, 100,000 mixed inputs with `fuzzy=True`: **~1.1 million rows/second**,
about 38x faster than calling dateutil from Python.

## Known differences from dateutil

These are deliberate:

1. **No `tzinfos`, and no local time zone names.** As in dateutil without `tzinfos`, a zone
   name it can't resolve (e.g. `EST`) gives a naive result. dateutil also maps names in
   `time.tzname` (the server's own zone) to `tzlocal()`. This port doesn't, so results never
   depend on the server's `TZ` setting. `UTC`, `GMT`, `Z` and numeric offsets work as in dateutil.
2. **Only ASCII digits form numbers.** Characters are classified exactly as Python's
   `isalpha()`, `isdigit()` and `isspace()` do (table generated by `tools/gen_unicode.py`).
   Python's `float()`/`int()` also accept other Unicode decimal digits, such as full-width
   `２００３`. Those inputs return `NULL` here.
3. **Numeric extremes.** dateutil's `Decimal` arithmetic uses 28 significant digits.
   Fractions longer than that may round differently. Absurdly long numbers make dateutil raise
   `decimal.InvalidOperation`; here they return `NULL`.
4. **Inputs over 64 KiB** return `NULL`.

## Layout

```
dateutil_parse.c        the extension (port of dateutil/parser/_parser.py)
dateutil_unicode.h      generated character-class table
tools/gen_unicode.py    regenerates the table from Python's Unicode data
tools/du_cli.c          SQLite-free driver used for sanitizer tests
tools/build.py          cross-platform build script (used by the tests)
fuzz/                   libFuzzer harness, dictionary and seed generator
vendor/sqlite/          SQLite 3.53.2 public-domain headers
tests/                  pytest differential test suite
```
