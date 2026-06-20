# strip-tags

[![PyPI](https://img.shields.io/pypi/v/strip-tags.svg)](https://pypi.org/project/strip-tags/)
[![Changelog](https://img.shields.io/github/v/release/simonw/strip-tags?include_prereleases&label=changelog)](https://github.com/simonw/strip-tags/releases)
[![Tests](https://github.com/simonw/strip-tags/workflows/Test/badge.svg)](https://github.com/simonw/strip-tags/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/strip-tags/blob/master/LICENSE)

Strip tags from HTML, optionally from areas identified by CSS selectors

See [llm, ttok and strip-tags—CLI tools for working with ChatGPT and other LLMs](https://simonwillison.net/2023/May/18/cli-tools-for-llms/) for more on this project.

## Installation

Install this tool using `pip`:
```bash
pip install strip-tags
```
## Usage

Pipe content into this tool to strip tags from it:
```bash
cat input.html | strip-tags > output.txt
````
Or pass a filename:
```bash
strip-tags -i input.html > output.txt
```
To run against just specific areas identified by CSS selectors:
```bash
strip-tags '.content' -i input.html > output.txt
```
This can be called with multiple selectors:
```bash
cat input.html | strip-tags '.content' '.sidebar' > output.txt
```
To return just the first element on the page that matches one of the selectors, use `--first`:
```bash
cat input.html | strip-tags .content --first > output.txt
```
To remove content contained by specific selectors - e.g. the `<nav>` section of a page, use `-r` or `--remove`:
```bash
cat input.html | strip-tags -r nav > output.txt
```
To minify whitespace - reducing multiple space and tab characters to a single space, removing any remaining blank lines - add `-m` or `--minify`:
```bash
cat input.html | strip-tags -m > output.txt
```
You can also run this command using `python -m` like this:
```bash
python -m strip_tags --help
```
### Keeping the markup for specified tags

When passing content to a language model, it can sometimes be useful to leave in a subset of HTML tags - `<h1>This is the heading</h1>` for example - to provide extra hints to the model.

The `-t/--keep-tag` option can be passed multiple times to specify tags that should be kept.

This example looks at the `<header>` section of https://datasette.io/ and keeps the tags around the list items and `<h1>` elements:

```
curl -s https://datasette.io/ | strip-tags header -t h1 -t li
```
```html
<li>Uses</li>
<li>Documentation Docs</li>
<li>Tutorials</li>
<li>Examples</li>
<li>Plugins</li>
<li>Tools</li>
<li>News</li>
<h1>
    Datasette
</h1>
Find stories in data
```
All attributes will be removed from the tags, except for the `id=` and `class=` attribute since those may provide further useful hints to the language model.

The `href` attribute on links, the `alt` attribute on images and the `name` and `value` attributes on `meta` tags are kept as well.

You can also specify a bundle of tags. For example, `strip-tags -t hs` will keep the tag markup for all levels of headings.

The following bundles can be used:

<!-- [[[cog
import cog
from strip_tags.lib import BUNDLES
lines = []
for name, tags in BUNDLES.items():
    lines.append("- `-t {}`: {}".format(name, ", ".join("`<{}>`".format(tag) for tag in tags)))
cog.out("\n".join(lines))
]]] -->
- `-t hs`: `<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>`
- `-t metadata`: `<title>`, `<meta>`
- `-t structure`: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`
- `-t tables`: `<table>`, `<tr>`, `<td>`, `<th>`, `<thead>`, `<tbody>`, `<tfoot>`, `<caption>`, `<colgroup>`, `<col>`
- `-t lists`: `<ul>`, `<ol>`, `<li>`, `<dl>`, `<dd>`, `<dt>`
<!-- [[[end]]] -->

## As a Python library

You can use `strip-tags` from Python code too. The function signature looks like this:

<!-- [[[cog
import ast
module = ast.parse(open("strip_tags/lib.py").read())
strip_tags = [
    fn for fn in module.body
    if getattr(fn, 'name', None) == 'strip_tags'
][0]
code = ast.unparse(strip_tags)
defline = code.split("\n")[0]
code = (
    ',\n    '.join(defline.split(', ')).replace(") ->", "\n) ->").replace("strip_tags(", "strip_tags(\n    ")
)
cog.out("```python\n{}\n```".format(code))
]]] -->
```python
def strip_tags(
    input: str,
    selectors: Optional[Iterable[str]]=None,
    *,
    removes: Optional[Iterable[str]]=None,
    minify: bool=False,
    remove_blank_lines: bool=False,
    first: bool=False,
    keep_tags: Optional[Iterable[str]]=None,
    all_attrs: bool=False
) -> str:
```
<!-- [[[end]]] -->

Here's an example:
```python
from strip_tags import strip_tags

html = """
<div>
<h1>This has tags</h1>

<p>And whitespace too</p>
</div>
Ignore this bit.
"""
stripped = strip_tags(html, ["div"], minify=True, keep_tags=["h1"])
print(stripped)
```
Output:
```
<h1>This has tags</h1>

And whitespace too
```
Use `remove_blank_lines=True` to remove any remaining blank lines from the output.

## strip-tags --help

<!-- [[[cog
import cog
from strip_tags import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: strip-tags")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: strip-tags [OPTIONS] [SELECTORS]...

  Strip tags from HTML, optionally from areas identified by CSS selectors

  Example usage:

      cat input.html | strip-tags > output.txt

  To run against just specific areas identified by CSS selectors:

      cat input.html | strip-tags .entry .footer > output.txt

Options:
  --version             Show the version and exit.
  -r, --remove TEXT     Remove content in these selectors
  -i, --input FILENAME  Input file
  -m, --minify          Minify whitespace
  -t, --keep-tag TEXT   Keep these <tags>
  --all-attrs           Include all attributes on kept tags
  --first               First element matching the selectors
  --help                Show this message and exit.

```
<!-- [[[end]]] -->

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd strip-tags
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
