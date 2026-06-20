# llm-video-frames

[![PyPI](https://img.shields.io/pypi/v/llm-video-frames.svg)](https://pypi.org/project/llm-video-frames/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-video-frames?include_prereleases&label=changelog)](https://github.com/simonw/llm-video-frames/releases)
[![Tests](https://github.com/simonw/llm-video-frames/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-video-frames/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-video-frames/blob/main/LICENSE)

LLM plugin to turn a video into individual frames

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-video-frames
```
Requires `ffmpeg` installed and available on the system `PATH`. On macOS, you can install it using Homebrew:
```bash
brew install ffmpeg
```

## Usage

The `llm-video-frames` plugin provides a [fragment loader](https://llm.datasette.io/en/stable/fragments.html#using-fragments-from-plugins) that extracts individual frames from a video file using `ffmpeg`.

You can use the `video-frames:` fragment prefix to turn a video into a series of image attachments.

### Fragment syntax

```
video-frames:<path>?fps=N&timestamps=1
```

- `<path>`: Path to the video file accessible to the environment where LLM runs.
- `fps=N`: (optional) Number of frames per second to extract. Defaults to `1` if omitted.
- `timestamps=1`: (optional) If set to `1`, overlays the filename and timestamp on each extracted frame in the bottom-right corner.

### Examples

Extract 1 frame per second (default) from `video.mp4`:

```bash
llm -f video-frames:video.mp4 'describe the key scenes in this video'
```

Extract 5 frames per second:

```bash
llm -f 'video-frames:video.mp4?fps=5' 'summarize the video'
```

Extract 2 frames per second with filename and timestamps overlayed on frames:

```bash
llm -f 'video-frames:video.mp4?fps=2&timestamps=1' 'list notable events with timestamps'
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-video-frames
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
