# condense-json

[![PyPI](https://img.shields.io/pypi/v/condense-json.svg)](https://pypi.org/project/condense-json/)
[![Tests](https://github.com/simonw/condense-json/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/condense-json/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/condense-json?include_prereleases&label=changelog)](https://github.com/simonw/condense-json/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/condense-json/blob/main/LICENSE)

Python function for condensing JSON using replacement strings

## Installation

Install this library using `pip`:
```bash
pip install condense-json
```
## Usage

The `condense_json` function searches a JSON-like object for strings that contain specified replacement substrings. It replaces these substrings with a compact representation, making the JSON more concise.  The `uncondense_json` function reverses this process.

**`condense_json(obj: JSONInput, replacements: Mapping[str, Optional[str]]) -> Any`**

*   **`obj`**: The JSON value to condense - any nesting of dictionaries, lists, strings, numbers, booleans and `None`. Top-level lists and strings work too, not just dictionaries.
*   **`replacements`**: A mapping where keys are replacement IDs (e.g., "1", "2") and values are the strings they represent. Entries with blank values (`None` or `""`) are ignored.

`JSONInput` is a recursive type alias covering anything representable in JSON, built from covariant container types so that narrowly typed values such as `dict[str, str]` are accepted without any extra annotation. Results are typed `Any`, so they can be indexed, iterated and serialized without narrowing.

```python
JSONInput = Union[
    str, int, float, bool, None, "Sequence[JSONInput]", "Mapping[str, JSONInput]"
]
```

The function returns a modified version of the input `obj` where matching substrings are replaced.  If a string consists *entirely* of a replacement string, it's replaced with `{"$": replacement_id}`. If a string contains one or more replacement strings, it's replaced with `{"$r": [ ...segments...]}` where segments are the parts of the original string and replacement IDs.

Matches are found scanning left to right. Where replacement substrings overlap - for example `"quick"` and `"quick brown fox"` - the longest match wins, regardless of the order of the `replacements` dictionary, so output is deterministic for equivalent inputs.

**Example:**

```python
from condense_json import condense_json

input_json = {
    "foo": {
        "bar": {
            "string": "This is a string with foxes in it",
            "nested": {
                "more": ["Here is a string", "another with foxes in it too"]
            },
        }
    }
}

replacements = {"1": "with foxes in it"}

condensed_output = condense_json(input_json, replacements)
print(condensed_output)
# Expected output:
# {
#     "foo": {
#         "bar": {
#             "string": {"$r": ["This is a string ", {"$": "1"}]},
#             "nested": {
#                 "more": [
#                     "Here is a string",
#                     {"$r": ["another ", {"$": "1"}, " too"]}
#                 ]
#             }
#         }
#     }
# }

```

**`uncondense_json(obj: JSONInput, replacements: Mapping[str, Optional[str]]) -> Any`**

*   **`obj`**: The condensed JSON value.
*   **`replacements`**: The same `replacements` mapping used for condensing.

This function reverses the `condense_json` operation. It finds the  `{"$": replacement_id}` and `{"$r": [ ...segments...]}` structures and replaces them with the original strings from the `replacements` dictionary.

**Example:**

```python
from condense_json import uncondense_json, condense_json  # Import both

original = {
    "sentence": "The quick brown fox jumps over the lazy dog",
    "nested": {"list": ["fast fox", "lazy dog", "just some text"]},
}
replacements = {"1": "quick brown fox", "2": "lazy dog"}
condensed = condense_json(original, replacements)
uncondensed = uncondense_json(condensed, replacements)
assert uncondensed == original

```
If the input `obj` to `uncondense_json` doesn't contain any condensed structures, it returns the input unchanged.

`uncondense_json` is strict: it raises `condense_json.UncondenseError` (a subclass of `ValueError`) if the condensed input is malformed rather than silently producing corrupted output. This covers markers referencing a replacement ID that is missing from `replacements` (or one with a blank value, which `condense_json` never emits markers for), a `$r` value that is not a list, and `$r` segments that are not strings or `{"$": id}` dictionaries.

```python
from condense_json import uncondense_json, UncondenseError

try:
    uncondense_json({"query": {"$": "gt"}}, {"1": "with foxes in it"})
except UncondenseError as ex:
    print(ex)  # Unknown replacement id: 'gt'
```

### Escaping of `$`, `$r` and `$raw` keys

The condensed format gives special meaning to single-key dictionaries with a `$` or `$r` key. If your input data already contains dictionaries of that shape - for example `{"price": {"$": "100"}}` - they could be misinterpreted when uncondensing.

To prevent this, `condense_json` escapes any single-key dictionary whose sole key is `$`, `$r` or `$raw` by wrapping it in `{"$raw": ...}`:

```python
from condense_json import condense_json, uncondense_json

original = {"price": {"$": "100"}}
condensed = condense_json(original, {"1": "with foxes"})
# {'price': {'$raw': {'$': '100'}}}
assert uncondense_json(condensed, {"1": "with foxes"}) == original
```

`uncondense_json` removes exactly one `$raw` wrapper layer and restores the contents without interpreting them as a marker. Because `$raw` itself is escaped in the same way, this works even if your data already contains `$raw` keys, and round-trips of `condense_json` followed by `uncondense_json` are always lossless - including when applied more than once.

## Development

To contribute to this library, checkout the code and run the tests with `uv run pytest`:
```bash
cd condense-json
uv run pytest
```
