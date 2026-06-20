# justjshtml

Dependency-free JavaScript HTML5 parser (browser + Node.js) built as a port of the Python project [JustHTML](https://github.com/EmilStenstrom/justhtml).

Primary goal: pass the full [html5lib-tests](https://github.com/html5lib/html5lib-tests) suite (tokenizer, tree-construction, encoding, serializer fixtures) using only plain JavaScript.

Background on this project: [I ported JustHTML from Python to JavaScript with Codex CLI and GPT-5.2 in 4.5 hours](https://simonwillison.net/2025/Dec/15/porting-justhtml/).

## Status

- No runtime dependencies (no npm deps)
- Works in modern browsers (ES modules) and Node.js (ESM)
- html5lib-tests:
  - Tokenizer: passing
  - Tree construction: passing (skips `#script-on` fixtures; no JS execution)
  - Encoding: passing (skips the `encoding/scripted` fixture that requires JS execution)
  - Serializer fixtures: passing

## Quickstart (Node.js)

This repo is ESM (`"type": "module"` in `package.json`).

Create `example.mjs`:

```js
import { JustHTML, stream } from "./src/index.js";

const doc = new JustHTML("<p class='intro'>Hello <b>world</b></p>");

console.log(doc.toText()); // "Hello world"
console.log(doc.query("p.intro")[0].to_html()); // pretty-printed HTML for the matching node

for (const [event, data] of stream("<div>Hi</div>")) {
  console.log(event, data);
}
```

Run it:

```bash
node example.mjs
```

## Quickstart (Browser / HTML)

This project is intentionally “just ES modules”: import directly from `./src/`.

Create `example.html`:

```html
<!doctype html>
<meta charset="utf-8" />
<script type="module">
  import { JustHTML } from "./src/index.js";

  const doc = new JustHTML("<p>Hello <b>browser</b></p>");
  console.log(doc.toText()); // "Hello browser"
  console.log(doc.query("b")[0].to_html({ pretty: false })); // "<b>browser</b>"
</script>
```

Serve the directory (ES modules generally won’t work from `file://`):

```bash
python3 -m http.server
```

Then open `http://localhost:8000/example.html`.

## Playground

You can access the interactive playground at https://simonw.github.io/justjshtml/playground.html

`playground.html` is a browser UI equivalent to the Pyodide-based JustHTML playground at `https://tools.simonwillison.net/justhtml`, but powered by this JavaScript library.

TO run locally:

```bash
python3 -m http.server
```

Open:

- `http://localhost:8000/playground.html`

## API overview

### `new JustHTML(input, options?)`

```js
import { JustHTML } from "./src/index.js";

const doc = new JustHTML("<p>Hello</p>");
console.log(doc.root.name); // "#document"
```

Input can be:

- `string`
- `Uint8Array` / `ArrayBuffer` (bytes are decoded using HTML encoding sniffing; `options.encoding` can override transport encoding)

Useful options (see `src/justhtml.js`):

- `strict: boolean` – throws `StrictModeError` on the first collected parse error
- `collectErrors: boolean` – populate `doc.errors`
- `encoding: string | null` – transport override for byte input
- `fragmentContext: FragmentContext | null` – fragment parsing context
- `iframeSrcdoc: boolean` – test directive support
- `tokenizerOpts: object | null` – advanced options (primarily for tests/debugging)

### Nodes

Nodes are simple plain objects with a small DOM-like API:

- Properties: `name`, `attrs`, `children`, `parent`, `data`, `namespace`
- Template support: `templateContent` for `<template>` in the HTML namespace
- Methods:
  - `node.query(selector)`
  - `node.toText({ separator, strip })`
  - `node.toHTML({ indent, indentSize, pretty })` / `node.to_html(...)`
  - `node.toMarkdown()` / `node.to_markdown()`

### CSS selectors

```js
import { JustHTML } from "./src/index.js";

const doc = new JustHTML("<ul><li>One</li><li>Two</li></ul>");
console.log(doc.query("li:first-child")[0].toText()); // "One"
```

Standalone helpers:

```js
import { query, matches } from "./src/index.js";

const nodes = query(doc.root, "li");
console.log(matches(nodes[0], "li:first-child"));
```

### Streaming

`stream(html)` yields a simplified event stream from the tokenizer:

```js
import { stream } from "./src/index.js";

for (const [event, data] of stream("<div>Hello</div>")) {
  console.log(event, data);
}
```

Events:

- `["start", [tagName, attrs]]`
- `["end", tagName]`
- `["text", text]` (coalesced)
- `["comment", text]`
- `["doctype", [name, publicId, systemId]]`

## How this was built

This repository was developed as a test-driven port of `justhtml`:

- Ported the architecture module-by-module (`encoding`, `tokenizer`, `treebuilder`, serialization helpers)
- Added dependency-free Node.js runners for the upstream html5lib fixtures (`scripts/run-*-tests.js`)
- Used the official `html5lib-tests` data as the main correctness target, with GitHub Actions running the suite on every push/PR (`.github/workflows/test.yml`)
- Added a browser playground (`playground.html`) that imports the raw ES modules directly from `./src/`

The library was built using OpenAI Codex CLI and GPT-5.2. See [issue #1](https://github.com/simonw/justjshtml/issues/1) for prompts and transcripts.

## Running tests locally

Check out fixtures:

```bash
git clone https://github.com/html5lib/html5lib-tests tests/html5lib-tests
```
You can run the tests with [Just](https://github.com/casey/just):

```bash
just
```
Or manually like this:

```bash
node scripts/smoke.js
node scripts/run-selector-tests.js
node scripts/run-stream-tests.js
node scripts/run-markdown-tests.js
node scripts/run-encoding-tests.js
node scripts/run-tokenizer-tests.js
node scripts/run-tree-construction-tests.js
node scripts/run-serializer-tests.js
```

Or point at an existing checkout:

```bash
HTML5LIB_TESTS_DIR=/path/to/html5lib-tests node scripts/run-tokenizer-tests.js
```

## Attribution / Acknowledgements

- **JustHTML** (Python) by Emil Stenström: `justjshtml` is a JavaScript port intended to match its behavior and API surface where practical.
- **html5lib-tests** by the html5lib project: used as the primary conformance test suite.
- **html5ever** by the Servo project: JustHTML started as a Python port of html5ever, and that architecture heavily influenced this port as well.
- **Playground UI**: `playground.html` is adapted from the UI of `https://tools.simonwillison.net/justhtml`, but runs entirely in JavaScript (no Pyodide).

