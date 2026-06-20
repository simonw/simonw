# ospeak

[![PyPI](https://img.shields.io/pypi/v/ospeak.svg)](https://pypi.org/project/ospeak/)
[![Changelog](https://img.shields.io/github/v/release/simonw/ospeak?include_prereleases&label=changelog)](https://github.com/simonw/ospeak/releases)
[![Tests](https://github.com/simonw/ospeak/workflows/Test/badge.svg)](https://github.com/simonw/ospeak/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/ospeak/blob/master/LICENSE)

CLI tool for running text through the [OpenAI Text to speech](https://platform.openai.com/docs/guides/text-to-speech) API and speaking or saving the result

See [ospeak: a CLI tool for speaking text in the terminal via OpenAI](https://simonwillison.net/2023/Nov/7/ospeak/) for background on this project.

## Installation

Install this tool using `pipx`:
```bash
pipx install ospeak
```
Note, on MacOS there's a [broken dependency](https://github.com/simonw/ospeak/issues/4) with Python 3.12 so instead run:
```bash 
pipx install --python /path/to/python3.11 ospeak
```

This tool also depends on `ffmpeg`. You can install that on macOS using [Homebrew](https://brew.sh/) like this:
```bash
brew install ffmpeg
```
Note that `ospeak` has dependencies that are currently incompatible with [LLM](https://llm.datasette.io) (see [this issue](https://github.com/simonw/llm/issues/325)) so the two tools need to be installed in different virtual environments, hence the recommendation to use [pipx](https://pypa.github.io/pipx/).

## Usage

To get your computer to say something, run:
```bash
ospeak "Hello there"
```
You will need an OpenAI API key. You can set that as an environment variable:
```bash
export OPENAI_API_KEY="..."
```
Or you can pass it using `--token`:
```bash
ospeak --token "..." "Hello there"
```
You can pipe content into the tool:
```bash
echo "Hello there" | ospeak
```
Use `-v/--voice VOICE` to select a voice. The default is `alloy`. The other options are:

- `echo`
- `fable`
- `onyx`
- `nova`
- `shimmer`

You can pass `-v all` to hear all of the voices, each with the name of the voice spoken first.
```bash
ospeak "This is my voice" -v all
```
The `-m/--model` option can be used to select a different model. The default is `tts-1`. Use `-m tts-1-hd` for a higher quality model that takes slightly longer to generate audio:
```bash
ospeak "This is higher quality" -m tts-1-hd
```
To adjust the speed, pass `-x/--speed` with a value between 0.25 and 4 (the default is 1.0):
```bash
ospeak "This is my fast voice" -x 2
```
To write the audio to a file, pass `-o/--output` with a filename ending in either `.mp3` or `.wav`:
```bash
ospeak "This is my voice" -o voice.mp3
```
This will not speak out loud. If you want it to also speak, add the `-s/--speak` option:
```bash
ospeak "This is my voice" -o voice.mp3 -s
```

## ospeak --help

<!-- [[[cog
import cog
from ospeak import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: ospeak")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: ospeak [OPTIONS] [TEXT]

  CLI tool for running text through OpenAI Text to speech

  Set the OPENAI_API_KEY environment variable to your OpenAI API key to avoid
  using the --token option every time.

  Example usage:

      ospeak "Everyone deserves a pelican" --voice alloy -x 1.5

Options:
  --version                       Show the version and exit.
  -v, --voice [alloy|echo|fable|onyx|nova|shimmer|all]
                                  Voice to use
  -m, --model TEXT                Model to use - defaults to tts-1
  -o, --output FILE               Save audio to this file on disk
  -x, --speed FLOAT RANGE         Speed of the voice  [0.25<=x<=4.0]
  -s, --speak                     Speak the text even when saving to a file
  --token TEXT                    OpenAI API key
  --help                          Show this message and exit.

```
<!-- [[[end]]] -->

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd ospeak
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
