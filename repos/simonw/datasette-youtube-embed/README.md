# datasette-youtube-embed

[![PyPI](https://img.shields.io/pypi/v/datasette-youtube-embed.svg)](https://pypi.org/project/datasette-youtube-embed/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-youtube-embed?include_prereleases&label=changelog)](https://github.com/simonw/datasette-youtube-embed/releases)
[![Tests](https://github.com/simonw/datasette-youtube-embed/workflows/Test/badge.svg)](https://github.com/simonw/datasette-youtube-embed/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-youtube-embed/blob/main/LICENSE)

Turn YouTube URLs into embedded players in Datasette

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-youtube-embed

## Usage

Once installed, any columns containing URLs that look like one of these:

- `https://www.youtube.com/watch?v=xyz`
- `https://www.youtube.com/watch?v=xyz&start=30`
- `https://www.youtube.com/watch?v=xyz&start=30&end=50`

Will be turned into YouTube embeds like this:

```html
<lite-youtube videoid="xyz" params="start=30" style="min-width: 200px"></lite-youtube>
```
These will then be rendered using [Lite YouTube Embed](https://github.com/paulirish/lite-youtube-embed), which avoids loading the full YouTube embed until someone interacts with it.

## Development

To set up this plugin locally, first checkout the code. Then run the tests with `uv`:

    cd datasette-youtube-embed
    uv run pytest
