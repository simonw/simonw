# datasette-demo-for-llm-accountant

[![PyPI](https://img.shields.io/pypi/v/datasette-demo-for-llm-accountant.svg)](https://pypi.org/project/datasette-demo-for-llm-accountant/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-demo-for-llm-accountant?include_prereleases&label=changelog)](https://github.com/datasette/datasette-demo-for-llm-accountant/releases)
[![Tests](https://github.com/datasette/datasette-demo-for-llm-accountant/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-demo-for-llm-accountant/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-demo-for-llm-accountant/blob/main/LICENSE)

Demo app for LLM accountant

This is a demonstration plugin showing how to use [datasette-llm-accountant](https://github.com/datasette/datasette-llm-accountant) to track and log LLM API costs.

## Features

- **Interactive LLM Form**: Submit prompts to any available LLM model via a web interface
- **Cost Tracking**: All LLM API calls are tracked with nanocent precision
- **Transaction Log**: View a running total of all LLM requests and their costs
- **In-Memory Accountant**: Demonstrates implementing a custom `Accountant` subclass

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-demo-for-llm-accountant
```

## Usage

Once installed, navigate to `/-/llm-accountant` in your Datasette instance.

You'll see:
1. A form to select an LLM model and enter a prompt
2. The response from the LLM
3. A transaction log showing all requests and their costs

Each request reserves $0.50 by default, and the actual cost is calculated based on token usage and settled in the transaction log.

### Running Locally

```bash
datasette
```

Then visit http://127.0.0.1:8001/-/llm-accountant

**Note**: You'll need LLM API keys configured for this to work. See the [llm documentation](https://llm.datasette.io/) for details on configuring API keys.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-demo-for-llm-accountant
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
