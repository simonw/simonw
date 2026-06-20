# Multipart Form-Data Conformance Test Suite

> **⚠️ EARLY ALPHA - DO NOT USE**
>
> This test suite is in very early development and has not been verified against real-world implementations. The test cases, expected results, and tooling may contain errors. Do not rely on this for validating parser conformance until it has been thoroughly reviewed and tested.

A language-independent test suite for validating HTTP `multipart/form-data` parsers and generators.

## Goals

1. **Language-independent** - Raw binary test files with JSON metadata
2. **Bidirectional** - Test both parsing and generation
3. **Comprehensive** - Cover spec requirements, edge cases, and browser variations
4. **Self-describing** - Each test case explains what it's testing

## Quick Start

### Running Tests Against Your Implementation

1. Iterate through test directories in `tests/`
2. For each test:
   - Read `headers.json` to get the Content-Type header with boundary
   - Read `input.raw` as binary data (the HTTP request body)
   - Parse using your implementation
   - Compare results against `expected` in `test.json`

### Test Case Structure

Each test case is a directory containing:

```
tests/category/NNN-test-name/
├── test.json      # Metadata and expected results
├── headers.json   # HTTP headers (Content-Type with boundary)
└── input.raw      # Raw HTTP body bytes (binary)
```

## Test Categories

| Category | ID Range | Description |
|----------|----------|-------------|
| basic | 001-019 | Essential parsing tests |
| filenames | 020-039 | Filename parameter handling |
| boundaries | 040-059 | Boundary detection and edge cases |
| line-endings | 060-079 | CRLF/LF handling |
| content-types | 080-099 | Content-Type and header parsing |
| edge-cases | 100-199 | Unusual but valid scenarios |
| malformed | 200-299 | Invalid input error handling |
| browser-variations | 300-399 | Real browser output patterns |

## File Formats

### test.json

```json
{
  "id": "001-single-text-field",
  "name": "Single text field",
  "description": "Basic test with one text form field",
  "spec_references": ["RFC 7578 Section 4.2"],
  "category": "basic",
  "tags": ["required", "parsing"],
  "expected": {
    "valid": true,
    "parts": [
      {
        "name": "username",
        "filename": null,
        "content_type": null,
        "body_text": "john_doe"
      }
    ]
  }
}
```

### headers.json

```json
{
  "content-type": "multipart/form-data; boundary=----TestBoundary123"
}
```

### input.raw

Binary file containing exact HTTP body bytes. Use a hex editor or the provided tools to inspect.

## Tools

- `tools/generate-raw.py` - Create .raw files programmatically
- `tools/validate-suite.py` - Validate test suite integrity
- `tools/run-reference.py` - Reference parser implementation

## Spec References

- [RFC 7578](https://tools.ietf.org/html/rfc7578) - Returning Values from Forms: multipart/form-data
- [RFC 2046](https://tools.ietf.org/html/rfc2046) - MIME Part Two: Media Types (multipart definition)
- [RFC 5987](https://tools.ietf.org/html/rfc5987) - Character Set and Language Encoding (filename*)
- [HTML Living Standard](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#multipart-form-data) - Form submission

## License

This test suite is released under the MIT License. See [LICENSE](LICENSE) for details.
