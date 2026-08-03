# condense-json

[![PyPI](https://img.shields.io/pypi/v/condense-json.svg)](https://pypi.org/project/condense-json/)
[![Tests](https://github.com/simonw/condense-json/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/condense-json/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/condense-json?include_prereleases&label=changelog)](https://github.com/simonw/condense-json/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/condense-json/blob/main/LICENSE)

Python function for condensing JSON using replacement strings and values

## Installation

Install this library using `pip`:
```bash
pip install condense-json
```
## Usage

The `condense_json` function searches a JSON-like object for content that matches entries in a replacements mapping: strings that contain replacement substrings, subtrees that are structurally equal to replacement dicts or lists, and dicts that are *close* to a replacement dict, which are stored as that base plus a patch. It replaces each with a compact reference, making the JSON more concise.  The `uncondense_json` function reverses this process.

**`condense_json(obj: JSONInput, replacements: Mapping[str, Any]) -> Any`**

*   **`obj`**: The JSON value to condense - any nesting of dictionaries, lists, strings, numbers, booleans and `None`. Top-level lists and strings work too, not just dictionaries.
*   **`replacements`**: A mapping where keys are replacement IDs (e.g., "1", "2") and values are the content they represent - strings, which match as substrings, or dicts and lists, which match whole subtrees (see [Structural replacements](#structural-replacements-for-dicts-and-lists)); dict values additionally serve as bases for near-matches (see [Merge references](#merge-references-a-base-object-plus-a-patch)). Entries with empty values (`None`, `""`, `{}`, `[]`) or non-string scalar values are ignored.

`JSONInput` is a recursive type alias covering anything representable in JSON, built from covariant container types so that narrowly typed values such as `dict[str, str]` are accepted without any extra annotation. Results are typed `Any`, so they can be indexed, iterated and serialized without narrowing.

```python
JSONInput = Union[
    str, int, float, bool, None, "Sequence[JSONInput]", "Mapping[str, JSONInput]"
]
```

The function returns a modified version of the input `obj` with matches replaced by references. Three reference forms appear in the output:

- `{"$": replacement_id}` - a whole value that matched: a string consisting *entirely* of a replacement string, or a dict or list structurally equal to a replacement value.
- `{"$r": [ ...segments... ]}` - a string that *contains* one or more replacement strings, broken into literal segments and `{"$": id}` references.
- `{"$": {"m": base_id, "u": {...}, "d": [...]}}` - a dict stored as a replacement dict plus a patch (see [Merge references](#merge-references-a-base-object-plus-a-patch)).

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

**`uncondense_json(obj: JSONInput, replacements: Mapping[str, Any]) -> Any`**

*   **`obj`**: The condensed JSON value.
*   **`replacements`**: The same `replacements` mapping used for condensing.

This function reverses the `condense_json` operation. It finds the reference forms listed above and substitutes the original content from the `replacements` mapping: strings for string references, deep copies for dict and list references, and base-plus-patch reconstruction for merge references.

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

`uncondense_json` is strict: it raises `condense_json.UncondenseError` (a subclass of `ValueError`) if the condensed input is malformed rather than silently producing corrupted output. This covers markers referencing a replacement ID that is missing from `replacements` (or one with an empty value, which `condense_json` never emits markers for), a `$r` value that is not a list, `$r` segments that are not strings or `{"$": id}` dictionaries, `$r` segments referencing a dict or list replacement - a reference inside a string must resolve to a string - and malformed [merge references](#merge-references-a-base-object-plus-a-patch).

```python
from condense_json import uncondense_json, UncondenseError

try:
    uncondense_json({"query": {"$": "gt"}}, {"1": "with foxes in it"})
except UncondenseError as ex:
    print(ex)  # Unknown replacement id: 'gt'
```

### Structural replacements for dicts and lists

A replacement value can also be a dict or a list. These match **structurally**: any subtree of the input that is equal to the value - compared in canonical JSON form, so key order and formatting never matter - is replaced whole with `{"$": replacement_id}`. This is useful when a payload embeds a known blob of JSON, such as an API response that echoes back the JSON schema or tool definitions it was called with:

```python
from condense_json import condense_json, uncondense_json

schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"],
}
response = {
    "output": {"name": "Cleo"},
    "format": {
        # Same schema, different key order - still matches
        "schema": {
            "required": ["name"],
            "type": "object",
            "properties": {"name": {"type": "string"}},
        }
    },
}
condensed = condense_json(response, {"s": schema})
# {'output': {'name': 'Cleo'}, 'format': {'schema': {'$': 's'}}}
assert uncondense_json(condensed, {"s": schema}) == response
```

The rules:

- **Matching is outermost-wins.** Once a subtree matches, its interior is not searched further. Inner replacements still match anywhere an outer one does not.
- **Matching is strictly structural.** A *string* that happens to contain the JSON serialization of a replacement value is never matched - a reference in string context must resolve to a string. String and structural replacements compose freely in a single call.
- **Resolution substitutes an independent copy.** Each `{"$": id}` for a dict or list resolves to a deep copy, so mutating the result never aliases the `replacements` mapping or the value behind another marker.
- **Round-trips are structural, not byte-identical.** `uncondense_json(condense_json(obj, r), r) == obj` always holds, but a matched subtree comes back with the *replacement's* key order, since the original ordering is not recorded. If you re-serialize the result, bytes may differ even though the value is equal.
- **Non-string scalars never participate.** A replacement of `42` or `True` is ignored rather than riddling the output with markers, as are empty dicts and lists.

### Merge references: a base object plus a patch

Dict replacement values also act as **merge bases**. A dict in the input that is *mostly* equal to a base - some keys added, changed or missing - can be stored as a reference to the base plus a patch, using a dict-valued `$` marker:

```json
{"$": {"m": "base_id", "u": {"added or changed": "keys"}, "d": ["keys the input lacks"]}}
```

`m` names the base entry in `replacements`, `u` holds keys to apply on top of it, and `d` lists base keys to remove first. Uncondensing deep-copies the base, deletes the `d` keys, then applies the `u` entries - which are themselves uncondensed, so they may contain markers of their own. This suits data with a large static envelope and a few varying fields, such as API response metadata:

```python
from condense_json import condense_json, uncondense_json

env = {
    "object": "response",
    "status": "completed",
    "service_tier": "default",
    "truncation": "disabled",
    "store": False,
    "tools": [],
}
response = dict(env, id="resp_123", usage={"total_tokens": 27})
condensed = condense_json(response, {"env": env})
# {'$': {'m': 'env', 'u': {'id': 'resp_123', 'usage': {'total_tokens': 27}}}}
assert uncondense_json(condensed, {"env": env}) == response
```

How condensing decides:

- **A byte-cost comparison, not a similarity heuristic.** For each base, the patch is computed and both encodings are measured; the merge reference is emitted only when it is smaller than writing the dict out. An unrelated base produces a patch bigger than the dict itself, so it prices itself out. Among competing bases the smallest encoding wins, with ties going to the earlier entry in the mapping.
- **An exact match takes priority.** A dict equal to a base condenses to the plain `{"$": id}` form, never a merge reference.
- **Per-key equality is canonical**, like structural matching - key order inside values never matters, and `True`/`1`/`1.0` are always distinct.
- **Deletion is the explicit `d` list, never a `null` sentinel** (as in JSON Merge Patch), because `null` is a legitimate value in real payloads.
- **Patches are flat.** If a nested value differs from the base's version at all, the whole value travels in `u` - though it is condensed recursively on the way, so a nested dict may itself become a reference or merge against another base.
- The structural caveats apply here too: resolution substitutes independent deep copies, and round-trips are structurally equal rather than byte-identical.

`uncondense_json` validates merge references strictly: an unknown or non-dict base, unexpected fields, a non-list `d`, deletion of a key the base does not have, or a non-dict `u` all raise `UncondenseError`.

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

`uncondense_json` removes exactly one `$raw` wrapper layer and restores the contents without interpreting them as a marker. Because `$raw` itself is escaped in the same way, this works even if your data already contains `$raw` keys, and round-trips of `condense_json` followed by `uncondense_json` are always lossless - including when applied more than once. A marker-shaped dict that structurally matches a replacement value is referenced rather than escaped, and restores identically either way.

## Development

To contribute to this library, checkout the code and run the tests with `uv run pytest`:
```bash
cd condense-json
uv run pytest
```
