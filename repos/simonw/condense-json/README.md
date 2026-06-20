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

**`condense_json(obj: Dict, replacements: Dict[str, str]) -> Any`**

*   **`obj`**: The JSON-like object (nested dictionaries, lists, and strings) to condense.
*   **`replacements`**: A dictionary where keys are replacement IDs (e.g., "1", "2") and values are the strings they represent.

The function returns a modified version of the input `obj` where matching substrings are replaced.  If a string consists *entirely* of a replacement string, it's replaced with `{"$": replacement_id}`. If a string contains one or more replacement strings, it's replaced with `{"$r": [ ...segments...]}` where segments are the parts of the original string and replacement IDs.

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

**`uncondense_json(obj: Dict, replacements: Dict[str, str]) -> Any`**

*   **`obj`**: The condensed JSON-like object.
*   **`replacements`**: The same `replacements` dictionary used for condensing.

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

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd condense-json
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
