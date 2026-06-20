# datasette-mp3-audio

[![PyPI](https://img.shields.io/pypi/v/datasette-mp3-audio.svg)](https://pypi.org/project/datasette-mp3-audio/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-mp3-audio?include_prereleases&label=changelog)](https://github.com/simonw/datasette-mp3-audio/releases)
[![Tests](https://github.com/simonw/datasette-mp3-audio/workflows/Test/badge.svg)](https://github.com/simonw/datasette-mp3-audio/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-mp3-audio/blob/main/LICENSE)

Turn .mp3 URLs into an audio player in the Datasette interface

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-mp3-audio

## Demo

Try this plugin at [https://scotrail.datasette.io/scotrail/announcements](https://scotrail.datasette.io/scotrail/announcements)

The demo uses ScotRail train announcements from [matteason/scotrail-announcements-june-2022](https://github.com/matteason/scotrail-announcements-june-2022).

## Usage

Once installed, any cells with a value that ends in `.mp3` and starts with either `http://` or `/` or `https://` will be turned into an embedded HTML audio element like this:

```html
<audio controls src="... value ..."><a href="...">Download MP3</a></audio>
```

A "Play X MP3s on this page" button will be added to athe top of any table page listing more than one MP3.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-mp3-audio
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
