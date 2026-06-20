# llm-pdf-to-images

[![PyPI](https://img.shields.io/pypi/v/llm-pdf-to-images.svg)](https://pypi.org/project/llm-pdf-to-images/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-pdf-to-images?include_prereleases&label=changelog)](https://github.com/simonw/llm-pdf-to-images/releases)
[![Tests](https://github.com/simonw/llm-pdf-to-images/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-pdf-to-images/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-pdf-to-images/blob/main/LICENSE)

LLM fragment plugin to load a PDF as a sequence of images

This plugin uses the [PyMuPDF library](https://github.com/pymupdf/PyMuPDF) which is licensed under the AGPL.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-pdf-to-images
```
The `llm-pdf-to-images` plugin provides a [fragment loader](https://llm.datasette.io/en/stable/fragments.html#using-fragments-from-plugins) that converts each page of a PDF document into an image attachment.

You can use the `pdf-to-images:` fragment prefix to convert a PDF file into a series of image attachments which can be sent to a model.

Example usage:

```bash
llm -f pdf-to-images:path/to/document.pdf 'Summarize this document'
```

### Fragment syntax

```
pdf-to-images:<path>?dpi=N&format=jpg|png&quality=Q
```

- `<path>`: Path to the PDF file accessible to the environment where LLM runs.
- `dpi=N`: (optional) Dots per inch to use when rendering the PDF pages, which affects the resolution of the output images. Defaults to `300` if omitted.
- `format=jpg|png`: (optional) Image format to use for the output. Can be either `jpg` (default) or `png`.
- `quality=Q`: (optional) JPEG quality factor between 1 and 100. Only applies when using JPG format. Defaults to `30` if omitted. Higher values produce better quality but larger file sizes.

### More examples

Convert a PDF file to images with default settings (300 DPI, JPG format, quality 30):

```bash
llm -f pdf-to-images:document.pdf 'summarize this document'
```

Convert a PDF with higher resolution (600 DPI):

```bash
llm -f 'pdf-to-images:document.pdf?dpi=600' 'summarize'
```

Convert a PDF to PNG format:

```bash
llm -f 'pdf-to-images:document.pdf?format=png' 'describe all figures'
```

Convert a PDF with high-quality JPG images:

```bash
llm -f 'pdf-to-images:document.pdf?quality=90' 'extract all visible text'
```

Combine multiple parameters:

```bash
llm -f 'pdf-to-images:document.pdf?dpi=450&format=jpg&quality=75' 'OCR'
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-pdf-to-images
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
