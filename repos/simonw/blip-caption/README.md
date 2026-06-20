# blip-caption

[![PyPI](https://img.shields.io/pypi/v/blip-caption.svg)](https://pypi.org/project/blip-caption/)
[![Changelog](https://img.shields.io/github/v/release/simonw/blip-caption?include_prereleases&label=changelog)](https://github.com/simonw/blip-caption/releases)
[![Tests](https://github.com/simonw/blip-caption/workflows/Test/badge.svg)](https://github.com/simonw/blip-caption/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/blip-caption/blob/main/LICENSE)

A CLI tool for generating captions for images using [Salesforce BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base).

## Installation

Install this tool using `pip` or `pipx`:
```bash
pipx install blip-caption
```
The first time you use the tool it will download the model from the Hugging Face model hub.

The small model is 945MB. The large model is 1.8GB. The models will be downloaded and stored in `~/.cache/huggingface/hub/` the first time you use them.

## Usage

To generate captions for an image using the small model, run:

```bash
blip-caption IMG_5825.jpeg
```
Example output:
```
a lizard is sitting on a branch in the woods
```
To use the larger model, add `--large`:
```bash
blip-caption IMG_5825.jpeg --large
```
Example output:
```
there is a chamelon sitting on a branch in the woods
```
Here's [the image I used](https://static.simonwillison.net/static/2023/IMG_5924.jpeg):

![It is ineded a chameleon](https://static.simonwillison.net/static/2023/IMG_5924.jpeg)

If you pass multiple files the path to each file will be output before its caption:

```bash
blip-caption /tmp/photos/*.jpeg
/tmp/photos/IMG_2146.jpeg
a man holding a bowl of salad and laughing
/tmp/photos/IMG_0151.jpeg
a cat laying on a red blanket
```

## JSON output

The `--json` flag changes the output to look like this:

```
blip-caption /tmp/photos/*.* --json
```
```json
[{"path": "/tmp/photos/IMG_2146.jpeg", "caption": "a man holding a bowl of salad and laughing"},
 {"path": "/tmp/photos/IMG_0151.jpeg", "caption": "a cat laying on a red blanket"},
 {"path": "/tmp/photos/IMG_3099.MOV", "error": "cannot identify image file '/tmp/photos/IMG_3099.MOV'"}]
```
Any errors are returned as a `{"path": "...", "error": "error message"}` object.


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd blip-caption
python3 -m venv venv
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
