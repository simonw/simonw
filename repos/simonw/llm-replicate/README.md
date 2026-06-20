# llm-replicate

[![PyPI](https://img.shields.io/pypi/v/llm-replicate.svg)](https://pypi.org/project/llm-replicate/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-replicate?include_prereleases&label=changelog)](https://github.com/simonw/llm-replicate/releases)
[![Tests](https://github.com/simonw/llm-replicate/workflows/Test/badge.svg)](https://github.com/simonw/llm-replicate/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-replicate/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for models hosted on [Replicate](https://replicate.com/)

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM.
```bash
llm install llm-replicate
```
## Configuration

You will need an API key from Replicate. You can [obtain one here](https://replicate.com/account/api-tokens).

You can set that as an environment variable called `REPLICATE_API_TOKEN`, or add it to the `llm` set of saved keys using:

```bash
llm keys set replicate
```
```
Enter key: <paste key here>
```
To fetch and save details of [the default collection](https://replicate.com/collections/language-models) of language models hosted on Replicate, run this:
```bash
llm replicate fetch-models
```
To add specific models that aren't listed in that collection, use the `llm replicate add` command.

For the Llama 2 model from [a16z-infra/llama13b-v2-chat](https://replicate.com/a16z-infra/llama13b-v2-chat) run this:

```bash
llm replicate add a16z-infra/llama13b-v2-chat \
  --chat --alias llama2
```
The `--chat` flag indicates that this is a chat model, which means it will be able to work with `-c` continue mode.

Here's the [70b version](https://replicate.com/replicate/llama70b-v2-chat) of that model:
```bash
llm replicate add \
  replicate/llama70b-v2-chat \
  --chat --alias llama70b
```
## Usage

To run a prompt against a model, pass its name or an alias to `llm -m`:
```bash
llm -m llama2 "Ten great names for a pet pelican"
```

> Sure, here are ten great names for a pet pelican:
>
> 1. Pelty
> 2. Peanut
> 3. Puddles
> 4. Nibbles
> 5. Fuzzy
> 6. Gizmo
> 7. Hank
> 8. Luna
> 9. Scooter
> 10. Splishy
>
> I hope these suggestions help you find the perfect name for your pet pelican! Do you have any other questions?


Chat models can support continuing conversations, for example:
```bash
llm -c "Five more and make them more nautical"
```
> Ahoy matey! Here be five more nautical-themed names for yer pet pelican:
>
> 1. Captain Hook
> 2. Anchoryn
> 3. Seadog
> 4. Plunder
> 5. Pointe Pelican
>
> I hope these suggestions help ye find the perfect name for yer feathered friend! Do ye have any other questions, matey?

Run `llm models list` to see the full list of models:

```bash
llm models list
```
You should see something like this:
```
Replicate: replicate-flan-t5-xl
Replicate: replicate-llama-7b
Replicate: replicate-gpt-j-6b
Replicate: replicate-dolly-v2-12b
Replicate: replicate-oasst-sft-1-pythia-12b
Replicate: replicate-stability-ai-stablelm-tuned-alpha-7b
Replicate: replicate-vicuna-13b
Replicate: replicate-replit-code-v1-3b
Replicate: replicate-replit-replit-code-v1-3b
Replicate: replicate-joehoover-falcon-40b-instruct (aliases: falcon)
Replicate (chat): replicate-a16z-infra-llama13b-v2-chat (aliases: llama2)
```
Then run a prompt through a specific model like this:
```bash
llm -m replicate-vicuna-13b "Five great names for a pet llama"
```

## Registering extra models

To register additional models that are not included in the default [Language models collection](https://replicate.com/collections/language-models), find their ID on Replicate and use the `llm replicate add` command.

For example, to add the [joehoover/falcon-40b-instruct](https://replicate.com/joehoover/falcon-40b-instruct) model, run this:

```bash
llm replicate add joehoover/falcon-40b-instruct \
  --alias falcon
```
This adds the model with the alias `falcon` - you can have 0 or more aliases for a model.

Now you can run it like this:
```bash
llm -m replicate-joehoover-falcon-40b-instruct \
  "Three reasons to get a pet falcon"
```
Or using the alias like this:
```bash
llm -m falcon "Three reasons to get a pet falcon"
```
You can edit the list of models you have registered using the default `$EDITOR` like this:
```bash
llm replicate edit-models
```
If you register a model using the `--chat` option that model will be treated slightly differently. Prompts sent to the model will be formatted like this:
```
User: user input here
Assistant:
```
If you use `-c` [conversation mode](https://llm.datasette.io/en/stable/usage.html#continuing-a-conversation) the prompt will include previous messages in the conversation, like this:
```
User: Ten great names for a pet pelican
Assistant: Sure, here are ten great names for a pet pelican:

1. Pelty
2. Peanut
3. Puddles
4. Nibbles
5. Fuzzy
6. Gizmo
7. Hank
8. Luna
9. Scooter
10. Splishy

I hope these suggestions help you find the perfect name for your pet pelican! Do you have any other questions?
User: Five more and make them more nautical
Assistant:
```

## Fetching all Replicate predictions

Replicate logs all predictions made against models. You can fetch all of these predictions using the `llm replicate fetch-predictions` command:

```bash
llm replicate fetch-predictions
```
This will create or populate a table in your LLM `logs.db` database called `replicate_predictions`.

The data in this table will cover ALL Replicate models, not just language models that have been queried using this tool.

Running `llm replicate fetch-predictions` multiple times will only fetch predictions that have been created since the last time the command was run.

To browse the resulting data in [Datasette](https://datasette.io/), run this:
```bash
datasette "$(llm logs path)"
```
The schema for that table will look like this:
```sql
CREATE TABLE [replicate_predictions] (
   [id] TEXT PRIMARY KEY,
   [_model_guess] TEXT,
   [completed_at] TEXT,
   [created_at] TEXT,
   [error] TEXT,
   [input] TEXT,
   [logs] TEXT,
   [metrics] TEXT,
   [output] TEXT,
   [started_at] TEXT,
   [status] TEXT,
   [urls] TEXT,
   [version] TEXT,
   [webhook_completed] TEXT
)
```
This schema may change if the Replicate API adds new fields in the future.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-replicate
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
