# json-flatten

[![PyPI](https://img.shields.io/pypi/v/json-flatten.svg)](https://pypi.org/project/json-flatten/)
[![Changelog](https://img.shields.io/github/v/release/simonw/json-flatten?include_prereleases&label=changelog)](https://github.com/simonw/json-flatten/releases)
[![Tests](https://github.com/simonw/json-flatten/workflows/Test/badge.svg)](https://github.com/simonw/json-flatten/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/json-flatten/blob/main/LICENSE)


Python functions for flattening a JSON object to a single dictionary of pairs, and unflattening that dictionary back to a JSON object.

This can be useful if you need to represent a JSON object using a regular HTML form or transmit it as a set of query string parameters.

For example:

```pycon
>>> import json_flatten
>>> json_flatten.flatten({"foo": {"bar": [1, True, None]}})
{'foo.bar.[0]$int': '1', 'foo.bar.[1]$bool': 'True', 'foo.bar.[2]$none': 'None'}
>>> json_flatten.unflatten(_)
{'foo': {'bar': [1, True, None]}}
```

The top-level object passed to `flatten()` must be a dictionary.

## JSON flattening format

### Basic principles

1. Keys are constructed using dot notation to represent nesting.
2. Type information is preserved using `$type` suffixes.
3. List indices are represented using `[index]` notation.
4. Empty objects and lists have special representations.

### Nested objects

For nested objects, keys are constructed by joining the nested keys with dots.

Example:

<!-- [[[cog
import cog
import json
from json_flatten import flatten, unflatten

example = {
  "user": {
    "name": "John",
    "age": 30
  }
}

cog.out("```json\n")
cog.out(json.dumps(example, indent=2))
cog.out("\n```\n")
cog.out("Flattened:\n```\n")
for key, value in flatten(example).items():
    cog.out(f"{key}={value}\n")
cog.out("```\n")
]]] -->
```json
{
  "user": {
    "name": "John",
    "age": 30
  }
}
```
Flattened:
```
user.name=John
user.age$int=30
```
<!-- [[[end]]]  -->

### Lists

List items are represented using `[index]` notation.

Example:
<!-- [[[cog
example = {
  "fruits": ["apple", "banana", "cherry"]
}

cog.out("```json\n")
cog.out(json.dumps(example, indent=2))
cog.out("\n```\n")
cog.out("Flattened:\n```\n")
for key, value in flatten(example).items():
    cog.out(f"{key}={value}\n")
cog.out("```\n")
]]] -->
```json
{
  "fruits": [
    "apple",
    "banana",
    "cherry"
  ]
}
```
Flattened:
```
fruits.[0]=apple
fruits.[1]=banana
fruits.[2]=cherry
```
<!-- [[[end]]] -->

### Nested lists

For nested lists, the index notation is repeated.

Example:
<!-- [[[cog
example = {
  "matrix": [[1, 2], [3, 4]]
}

cog.out("```json\n")
cog.out(json.dumps(example))
cog.out("\n```\n")
cog.out("Flattened:\n```\n")
for key, value in flatten(example).items():
    cog.out(f"{key}={value}\n")
cog.out("```\n")
]]] -->
```json
{"matrix": [[1, 2], [3, 4]]}
```
Flattened:
```
matrix.[0].[0]$int=1
matrix.[0].[1]$int=2
matrix.[1].[0]$int=3
matrix.[1].[1]$int=4
```
<!-- [[[end]]] -->

## Type preservation

Types are preserved using `$type` suffixes:

<!-- [[[cog
examples = (
    ("String", "", {"name": "Cleo"}),
    ("Integer", "$int", {"age": 30}),
    ("Float", "$float", {"price": 19.99}),
    ("Boolean", "$bool", {"active": True}),
    ("Null", "$none", {"data": None}),
    ("Empty object", "$empty", {"obj": {}}),
    ("Empty list", "$emptylist", {"list": []}),
)
cog.out("| Type | Suffix | Example |\n")
cog.out("|------|--------|---------|\n")
for type_, suffix, example in (examples):
    key, value = list(flatten(example).items())[0]
    suffix = f'`{suffix}`' if suffix else ''
    cog.out(f"|{type_}|{suffix}|`{key}={value}`|\n")
]]] -->
| Type | Suffix | Example |
|------|--------|---------|
|String||`name=Cleo`|
|Integer|`$int`|`age$int=30`|
|Float|`$float`|`price$float=19.99`|
|Boolean|`$bool`|`active$bool=True`|
|Null|`$none`|`data$none=None`|
|Empty object|`$empty`|`obj$empty={}`|
|Empty list|`$emptylist`|`list$emptylist=[]`|
<!-- [[[end]]] -->

String values do not require a type suffix.

## Example

JSON:
<!-- [[[cog
example = {
  "user": {
    "name": "Alice",
    "age": 28,
    "hobbies": ["reading", "swimming"],
    "address": {
      "street": "123 Main St",
      "city": "Anytown"
    },
    "active": True,
    "salary": 50000.50,
    "spouse": None,
    "more_nesting": {
      "empty_lists": [[], []],
      "empty_objects": [{}, {}]
    }
  }
}

cog.out("```json\n")
cog.out(json.dumps(example, indent=2))
cog.out("\n```\n")
cog.out("\nFlattened with `flattened = flatten(example)`\n```\n")
flattened = flatten(example)
for key, value in flattened.items():
    cog.out(f"{key}={value}\n")
cog.out("```\n")
cog.out("\nUnflattened again with `unflattened = unflatten(flattened)`\n")
cog.out("```json\n")
cog.out(json.dumps(unflatten(flattened), indent=2))
cog.out("\n```\n")
]]] -->
```json
{
  "user": {
    "name": "Alice",
    "age": 28,
    "hobbies": [
      "reading",
      "swimming"
    ],
    "address": {
      "street": "123 Main St",
      "city": "Anytown"
    },
    "active": true,
    "salary": 50000.5,
    "spouse": null,
    "more_nesting": {
      "empty_lists": [
        [],
        []
      ],
      "empty_objects": [
        {},
        {}
      ]
    }
  }
}
```

Flattened with `flattened = flatten(example)`
```
user.name=Alice
user.age$int=28
user.hobbies.[0]=reading
user.hobbies.[1]=swimming
user.address.street=123 Main St
user.address.city=Anytown
user.active$bool=True
user.salary$float=50000.5
user.spouse$none=None
user.more_nesting.empty_lists.[0]$emptylist=[]
user.more_nesting.empty_lists.[1]$emptylist=[]
user.more_nesting.empty_objects.[0]$empty={}
user.more_nesting.empty_objects.[1]$empty={}
```

Unflattened again with `unflattened = unflatten(flattened)`
```json
{
  "user": {
    "name": "Alice",
    "age": 28,
    "hobbies": [
      "reading",
      "swimming"
    ],
    "address": {
      "street": "123 Main St",
      "city": "Anytown"
    },
    "active": true,
    "salary": 50000.5,
    "spouse": null,
    "more_nesting": {
      "empty_lists": [
        [],
        []
      ],
      "empty_objects": [
        {},
        {}
      ]
    }
  }
}
```
<!-- [[[end]]] -->