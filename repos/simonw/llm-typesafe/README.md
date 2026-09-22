# llm-typesafe

[![PyPI](https://img.shields.io/pypi/v/llm-typesafe.svg)](https://pypi.org/project/llm-typesafe/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-typesafe?include_prereleases&label=changelog)](https://github.com/simonw/llm-typesafe/releases)
[![Tests](https://github.com/simonw/llm-typesafe/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-typesafe/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-typesafe/blob/main/LICENSE)

Use [TypeSafe](https://typesafe.ai/) classification and scoring models with [LLM](https://llm.datasette.io/).

## Installation

```bash
llm install llm-typesafe
# Set an API key:
llm keys set typesafe
```

This plugin adds a model called `typesafe/jev-latest`, with the alias `jev`.

## Yes/no

```bash
llm -m jev 'Please refund my last payment.' \
  -s 'Does this message explicitly request a refund?'
```
Example output:
```json
{"type": "noul", "noul": 0.99}
```

You can add `-o answer_type noul`, but that is the default if no answer type is specified. "Noul" means a yes/no answer (from "Bernoulli distribution"), and returns the probability of yes between 0 and 1.

Optional definitions can be supplied using `-o criteria '...'`, like this:
```bash
llm -m jev 'Please refund my last payment.' \
  -s 'Does this message explicitly request a refund?' \
  -o criteria '{
    "true":"Explicit request for money back",
    "false":"No explicit refund request"
  }'
```
## Categories

Use an answer type of "choice" for an answer from one of several provided categories:

```bash
cat message.txt | llm -m jev \
  -s 'Which team should handle this message? If billing and technical issues both occur, choose billing.' \
  -o answer_type choice \
  -o criteria '{
    "billing":"Charges, invoices, payments, or refunds",
    "technical":"Problems installing or using the product",
    "other":"Neither category fits"
  }'
```

Example output:
```json
{
  "type": "choice",
  "choice": "technical",
  "confidence": 0.97,
  "probabilities": {
    "technical": 0.98,
    "other": 0.02,
    "billing": 0.0
  }
}
```

Supply at least two category names with descriptions; a description may be `null` when the name alone is sufficient.

## Ratings

A rating is floating point number on a scale that you define.

```bash
cat report.txt | llm -m jev \
  -s 'How reproducible is the problem described in this report?' \
  -o answer_type score \
  -o criteria '[
    "No reproduction instructions",
    "Some instructions, but important steps are missing",
    "Complete steps with expected and actual results"
  ]'
```

Returns `score`, `legend`, `probabilities`, and `confidence`. Supply 2–10 ordered descriptions, lowest to highest. With three levels, scores range from 0 to 2 and may be fractional; they measure degree on the rubric, not probability of yes.

## Structured input

```bash
llm -m jev '{"subject":"Refund","body":"Please return my payment"}' \
  -s 'Does body explicitly request a refund?' \
  -o input_format json
```

Text is never automatically interpreted as JSON. With `input_format=json`, the entire prompt must parse as a JSON string, object, or array. Duplicate keys and non-finite numbers are rejected. An array is one input state, not a request to evaluate each item separately.

## Reusable templates

```bash
llm -m jev -s 'Does this message explicitly request a refund?' \
  -o answer_type noul --save refund-request
cat message.txt | uv llm -t refund-request
```

Templates, text fragments, stdin, standard key management, and LLM's normal logging work through the regular model API.

## Python

```python
import json
import llm

model = llm.get_model("jev")
response = model.prompt(
    "Please refund my last payment.",
    system="Does this message explicitly request a refund?",
)
answer = json.loads(response.text())
print(answer["noul"])
print(response.json())  # Full provider response, including model and usage
print(response.usage())
```

Or in asynchronous Python code:

```python
import asyncio
import llm

async def main():
    model = llm.get_async_model("jev")
    response = model.prompt(
        '{"body":"I was charged twice"}',
        system="Which team should handle body?",
        input_format="json",
        answer_type="choice",
        criteria={"billing": "Charges and payments", "other": "Anything else"},
    )
    print(await response.text())
    print(await response.json())

asyncio.run(main())
```

## Development

Clone the repository and run the tests like this:

```bash
uv run pytest
```
