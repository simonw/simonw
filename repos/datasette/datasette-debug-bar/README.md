# datasette-debug-bar

[![PyPI](https://img.shields.io/pypi/v/datasette-debug-bar.svg)](https://pypi.org/project/datasette-debug-bar/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-debug-bar?include_prereleases&label=changelog)](https://github.com/datasette/datasette-debug-bar/releases)
[![Tests](https://github.com/datasette/datasette-debug-bar/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-debug-bar/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-debug-bar/blob/main/LICENSE)

A generic debug bar for Datasette that other plugins can add items to. The bar is fixed to the bottom-right corner of every page and can be minimized/expanded (state persists in localStorage).

## Installation

```bash
datasette install datasette-debug-bar
```

## Writing a debug-bar plugin

Any Datasette plugin can add a section to the debug bar by defining a `debug_bar_items` function at the top level of its module.

### API

```python
def debug_bar_items(datasette):
    return {
        "label": "My Section",
        "entrypoint": """function(el) {
            // el is an empty HTMLElement — append your UI to it
            el.textContent = 'Hello from my plugin!';
        }""",
    }
```

| Key | Type | Description |
|-----|------|-------------|
| `label` | `str` | Heading displayed above the section in the bar. |
| `entrypoint` | `str` | A JavaScript function body as a string. It receives a single argument `el` (an `HTMLElement`). Append whatever DOM you want to `el`. |

You can return a single dict or a list of dicts to register multiple sections.

### Complete example

Here is a minimal but complete Datasette plugin that adds a "Request Info" section to the debug bar. This is a single Python file that can be used directly with `datasette --plugins-dir`.

```python
# debug_request_info.py

def debug_bar_items(datasette):
    return {
        "label": "Request Info",
        "entrypoint": """function(el) {
            var items = [
                ['Path', location.pathname],
                ['Query', location.search || '(none)'],
                ['Hash', location.hash || '(none)'],
            ];
            var table = document.createElement('table');
            table.style.cssText = 'border-collapse:collapse;font-size:12px;width:100%;';
            items.forEach(function(row) {
                var tr = document.createElement('tr');
                var td1 = document.createElement('td');
                td1.textContent = row[0];
                td1.style.cssText = 'padding:2px 8px 2px 0;color:#666;white-space:nowrap;';
                var td2 = document.createElement('td');
                td2.textContent = row[1];
                td2.style.cssText = 'padding:2px 0;font-family:monospace;word-break:break-all;';
                tr.appendChild(td1);
                tr.appendChild(td2);
                table.appendChild(tr);
            });
            el.appendChild(table);
        }""",
    }
```

### Using it as a package

For installable plugins, add `datasette-debug-bar` as a dependency in your `pyproject.toml`:

```toml
[project]
dependencies = [
    "datasette",
    "datasette-debug-bar",
]

[project.entry-points.datasette]
my_debug_plugin = "my_debug_plugin"
```

Then define `debug_bar_items` in your package's `__init__.py`. The function will be discovered automatically when both plugins are installed.

### Entrypoint tips

- The `el` argument is a `<div>` inside the bar panel. Append DOM nodes to it.
- The function runs once on page load. If you need live updates, use `setInterval` or event listeners inside the function.
- You have access to the full browser environment: `document`, `window`, `fetch`, `localStorage`, `location`, cookies, etc.
- Keep the UI compact — the bar is meant for quick-glance debugging info.

## Sample plugins

The `sample/` directory contains two working example plugins that can be used with `--plugins-dir`:

- `debug_request_info.py` — displays current URL path, query string, and hash
- `debug_performance.py` — displays page performance timing (DNS, connect, response, DOM ready, load, transfer size)

Run them:

```bash
DATASETTE_SECRET=abc123 datasette --plugins-dir sample
```

## Development

```bash
cd datasette-debug-bar

# Run tests
uv run pytest

# Run dev server with sample plugins
just dev
```
