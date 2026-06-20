# xml-analyser

[![PyPI](https://img.shields.io/pypi/v/xml-analyser.svg)](https://pypi.org/project/xml-analyser/)
[![Changelog](https://img.shields.io/github/v/release/simonw/xml-analyser?include_prereleases&label=changelog)](https://github.com/simonw/xml-analyser/releases)
[![Tests](https://github.com/simonw/xml-analyser/workflows/Test/badge.svg)](https://github.com/simonw/xml-analyser/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/xml-analyser/blob/main/LICENSE)

A tool showing various statistics about element usage in an arbitrary XML file.

## Installation

    pip install xml-analyser

Or using [pipx](https://pypa.github.io/pipx/):

    pipx install xml-analyser

## Usage

    xml-analyser example.xml

If `example.xml` looks like this:

```xml
<example>
  <foo>
    <bar a="1" b="2">
      <baz>This has text</baz>
    </bar>
  </foo>
  <foo>
    <bar a="1" b="2" c="3">
      <baz>More text here</baz>
    </bar>
    <baz d="1" />
  </foo>
</example>
```

`xml-analyzer example.xml` outputs this:

```json
{
    "example": {
        "count": 1,
        "parent_counts": {},
        "attr_counts": {},
        "child_counts": {
            "foo": 2
        }
    },
    "foo": {
        "count": 2,
        "parent_counts": {
            "example": 2
        },
        "attr_counts": {},
        "child_counts": {
            "bar": 2,
            "baz": 1
        }
    },
    "bar": {
        "count": 2,
        "parent_counts": {
            "foo": 2
        },
        "attr_counts": {
            "a": 2,
            "b": 2,
            "c": 1
        },
        "child_counts": {
            "baz": 2
        }
    },
    "baz": {
        "count": 3,
        "parent_counts": {
            "bar": 2,
            "foo": 1
        },
        "attr_counts": {
            "d": 1
        },
        "child_counts": {},
        "count_with_text": 2,
        "max_text_length": 14
    }
}
```

## Truncating the XML instead

The `--truncate` option works differently: the XML file passed to this tool will be truncated, by finding any elements with more than two child elements of the same type and truncating to just those two elements.

This can reduce a large XML file to something that's easier to understand.

Given an example document like this one:

```xml
<example>
  <atop title="Example 1" />
  <atop title="Example 2" />
  <atop title="Example 3" />
  <atop title="Example 4" />
  <foo>
    <bar a="1" b="2">
      <baz>This has text</baz>
    </bar>
    <bar a="2" b="2">
      <baz>This has text</baz>
    </bar>
    <bar a="3" b="2">
      <baz>This has text</baz>
    </bar>
    <bar a="4" b="2">
      <baz>This has text</baz>
    </bar>
  </foo>
  <foo>
    <bar a="1" b="2" c="3">
      <baz>More text here</baz>
    </bar>
    <baz d="1" />
  </foo>
  <foo>
    <bar a="1" b="2" c="3">
      <baz>More text here</baz>
    </bar>
    <baz d="1" />
  </foo>
</example>
```
The following command:

    xml-analyser example.xml --truncate

Will return the following:

```xml
<example>
  <atop title="Example 1" />
  <atop title="Example 2" />
  <foo>
    <bar a="1" b="2">
      <baz>This has text</baz>
    </bar>
    <bar a="2" b="2">
      <baz>This has text</baz>
    </bar>
  </foo>
  <foo>
    <bar a="1" b="2" c="3">
      <baz>More text here</baz>
    </bar>
    <baz d="1" />
  </foo>
</example>
```
