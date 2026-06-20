# asgi-gzip

[![PyPI](https://img.shields.io/pypi/v/asgi-gzip.svg)](https://pypi.org/project/asgi-gzip/)
[![Changelog](https://img.shields.io/github/v/release/simonw/asgi-gzip?include_prereleases&label=changelog)](https://github.com/simonw/asgi-gzip/releases)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://github.com/simonw/asgi-gzip/blob/main/LICENSE)

gzip middleware for ASGI applications, extracted from Starlette

## Installation

Install this library using `pip`:

    pip install asgi-gzip

## Usage

```python
from asgi_gzip import GZipMiddleware
from my_asgi_app import app

gzip_app = GZipMiddleware(app)
```
Consult the [Starlette GZipMiddleware documentation](https://www.starlette.io/middleware/#gzipmiddleware) for full details.

## Should you use this package?

This package exists purely for use by ASGI applications that want to add gzip support without adding the whole of [Starlette](https://www.starlette.io/) as a dependency.

But... Starlette is actually a very light dependency! It's a small codebase and it only depends on two other small libraries - check its `install_requires` in the Starlette [setup.py module](https://github.com/encode/starlette/blob/master/setup.py).

So if you don't mind adding Starlette as a dependency, you should consider using that directly instead.

## Tracking Starlette

Since this code is extracted from Starlette, it's important to keep watch for changes and bug fixes to the Starlette implementation that should be replicated here.

The GitHub repository for this library uses [Git scraping](https://simonwillison.net/2020/Oct/9/git-scraping/) to track changes to a copy of the Starlette `gzip.py` module, which is kept in the `tracking/` folder.

Any time a change to that file is detected, an issue will be automatically created in the repository. This issue should be closed once the change to Starlette has been applied here, if necessary.

For more details on how this works, see [Automatically opening issues when tracked file content changes](https://simonwillison.net/2022/Apr/28/issue-on-changes/).

## Development

To contribute to this library, first checkout the code. Then run the tests with `uv`:

    cd asgi-gzip
    uv run pytest
