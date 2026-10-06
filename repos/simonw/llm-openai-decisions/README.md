# llm-openai-decisions

[![PyPI](https://img.shields.io/pypi/v/llm-openai-decisions.svg)](https://pypi.org/project/llm-openai-decisions/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-openai-decisions?include_prereleases&label=changelog)](https://github.com/simonw/llm-openai-decisions/releases)
[![Tests](https://github.com/simonw/llm-openai-decisions/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-openai-decisions/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-openai-decisions/blob/main/LICENSE)

Use the [OpenAI Decisions API](https://developers.openai.com/api/docs/guides/decisions) with [LLM](https://llm.datasette.io/) to evaluate text and images with predicates, choices, and scores.

## Installation

```bash
llm install llm-openai-decisions
llm keys set openai
```

You can also set the `OPENAI_API_KEY` environment variable, or use LLM's `--key` option.

## Yes/no questions

Supply the input as the prompt or on stdin, and the question using `-s`:

```bash
llm -m openai-decisions/gpt-6-luna 'Please refund my last payment.' \
  -s 'Does this message explicitly request a refund?'
```
Example output:
```json
{"name": "evaluation", "type": "predicate", "probability": 0.99}
```

The default `answer_type` is `predicate`. Its `probability` is an estimate from 0 to 1 that the condition is true. Use `-o name refund` to change the question name from `evaluation`.

## Categories

Use `answer_type choice` and supply a JSON object mapping category names to descriptions:

```bash
llm -m openai-decisions/gpt-6-luna 'I was charged twice.' \
  -s 'Which department should handle this message?' \
  -o answer_type choice \
  -o choices '{
    "billing": "Charges, invoices, and refunds",
    "technical": "Problems using the product",
    "other": null
  }'
```
Example output:
```json
{
  "type": "choice",
  "name": "evaluation",
  "choice": "billing",
  "probabilities": [
    {
      "value": "billing",
      "probability": 1.0
    },
    {
      "value": "technical",
      "probability": 0.0
    },
    {
      "value": "other",
      "probability": 0.0
    }
  ],
  "confidence": 1.0
}
```

A `null` description means the name alone is sufficient. The output includes `choice`, `confidence`, and a `probabilities` array.

For boolean choices, supply an array of objects with descriptions for `true` and `false`:

```bash
llm -m openai-decisions/gpt-6-luna 'I was charged twice.' \
  -s 'Does this require billing support?' \
  -o answer_type choice \
  -o choices '[
    {"value": true,"description": "Billing issue"},
    {"value": false,"description" :"Anything else"}
  ]'
```
Example output:
```json
{
  "type": "choice",
  "name": "evaluation",
  "choice": true,
  "probabilities": [
    {
      "value": true,
      "probability": 1.0
    },
    {
      "value": false,
      "probability": 0.0
    }
  ],
  "confidence": 1.0
}
```
## Ratings

Use `answer_type score` with ordered level labels, lowest to highest:

```bash
llm -m openai-decisions/gpt-6-luna 'Export fails in Safari but works in Chrome.' \
  -s 'How severe is this issue?' \
  -o answer_type score \
  -o levels '["Cosmetic","Workaround available","Fully blocked"]'
```

You can also supply objects with `label` and `description` fields:

```bash
llm -m openai-decisions/gpt-6-luna 'Export fails in Safari but works in Chrome.' \
  -s 'How severe is this issue?' \
  -o answer_type score \
  -o levels '[{"label":"Cosmetic","description":"Appearance only"},{"label":"Workaround","description":"Another way works"},{"label":"Blocked","description":"No workaround"}]'
```
Example output:
```json
{
  "type": "score",
  "name": "evaluation",
  "score": 0.96,
  "probabilities": [
    {
      "value": 0,
      "label": "Cosmetic",
      "probability": 0.04
    },
    {
      "value": 1,
      "label": "Workaround",
      "probability": 0.96
    },
    {
      "value": 2,
      "label": "Blocked",
      "probability": 0.0
    }
  ],
  "confidence": 0.94
}
```

Supply at least two levels. The returned `score` is the probability-weighted average of the zero-based level indices: with three levels it can range from 0 to 2. The answer also includes `confidence` and per-level `probabilities`.

## Images

Attach an image using LLM's `-a` option. Text alongside the image is optional:

```bash
llm -m openai-decisions/gpt-6-luna -a https://static.simonwillison.net/static/2025/two-pelicans.jpg \
  -s 'Does this image contain any mammals?'
```
Example outpt:
```json
{"type": "predicate", "name": "evaluation", "probability": 0.0}
```

PNG, JPEG, WebP, and GIF attachments are supported, with at most 128 images per request. You can pass a URL or a path to a local file.

## Multiple questions

Use `-o questions` with a JSON array to ask several named questions about shared input. Each question needs a unique `name`, a `type`, and `instructions`; choice questions also need `choices`, and score questions need `levels`, using the native array-of-objects formats:

```bash
llm -m openai-decisions/gpt-6-luna 'I was charged twice and need my money back.' \
  -o questions '[
    {
      "name": "refund",
      "type": "predicate",
      "instructions": "Does this request a refund?"
    },
    {
      "name": "department",
      "type": "choice",
      "instructions": "Which department should handle this?",
      "choices": [
        {
          "value": "billing"
        },
        {
          "value": "other"
        }
      ]
    }
  ]'
```
Example output:
```json
[
  {
    "type": "predicate",
    "name": "refund",
    "probability": 0.94
  },
  {
    "type": "choice",
    "name": "department",
    "choice": "billing",
    "probabilities": [
      {
        "value": "billing",
        "probability": 1.0
      },
      {
        "value": "other",
        "probability": 0.0
      }
    ],
    "confidence": 1.0
  }
]
```
This returns a JSON array of answers in question order, even if only one question is supplied. Do not combine `questions` with a system prompt, `choices`, `levels`, or non-default `answer_type` or `name` options. Put the instructions in each question instead.

A single question normally returns one JSON object. If the API declines a question, its answer is preserved as `{"name":"...","type":"refusal"}`.

## Reusable templates

```bash
llm -m openai-decisions/gpt-6-luna \
  -s 'Does this message explicitly request a refund?' --save refund-request
cat message.txt | llm -t refund-request
```

Templates, fragments, stdin, key management, and LLM's normal logging work through the regular model API.

## Python

```python
import json
import llm

model = llm.get_model("openai-decisions/gpt-6-luna")
response = model.prompt(
    "Please refund my last payment.",
    system="Does this message explicitly request a refund?",
)
print(json.loads(response.text())["probability"])
print(response.json())  # Complete provider response
print(response.usage())  # Token counts and details
```

Options accept Python lists and dictionaries as well as JSON strings. For asynchronous use:

```python
import asyncio
import llm

async def main():
    model = llm.get_async_model("openai-decisions/gpt-6-luna")
    response = model.prompt(
        "I was charged twice.",
        system="Which department should handle this?",
        answer_type="choice",
        choices={"billing": "Payments and refunds", "other": None},
    )
    print(await response.text())
    print(await response.json())

asyncio.run(main())
```

For an image in Python, pass `attachments=[llm.Attachment(path="product.png")]` to `model.prompt()`. Raw image bytes can be supplied using `llm.Attachment(content=image_bytes, type="image/png")`.

## Development

```bash
cd llm-openai-decisions
uv run pytest
uv run llm models -m openai-decisions/gpt-6-luna --options
```
