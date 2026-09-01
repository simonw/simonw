# llm-anthropic

[![PyPI](https://img.shields.io/pypi/v/llm-anthropic.svg)](https://pypi.org/project/llm-anthropic/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-anthropic?include_prereleases&label=changelog)](https://github.com/simonw/llm-anthropic/releases)
[![Tests](https://github.com/simonw/llm-anthropic/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-anthropic/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-anthropic/blob/main/LICENSE)

LLM access to models by Anthropic, including the Claude series

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-anthropic
```

## Usage

First, set [an API key](https://console.anthropic.com/settings/keys) for Anthropic:
```bash
llm keys set anthropic
# Paste key here
```

You can also set the key in the environment variable `ANTHROPIC_API_KEY`

Run `llm models` to list the models, and `llm models --options` to include a list of their options.

Run prompts like this:
```bash
llm -m claude-opus-5 'Fun facts about walruses'
llm -m claude-sonnet-5 'Fun facts about pelicans'
llm -m claude-haiku-4.5 'Fun facts about cormorants'
```
Image attachments are supported too:
```bash
llm -m claude-sonnet-5 'describe this image' -a https://static.simonwillison.net/static/2024/pelicans.jpg
llm -m claude-haiku-4.5 'extract text' -a page.png
```
Claude 3.5 and later models can handle PDF files:
```bash
llm -m claude-sonnet-5 'extract text' -a page.pdf
```
Anthropic's models support [schemas](https://llm.datasette.io/en/stable/schemas.html). Here's how to use Claude 4 Sonnet to invent a dog:

```bash
llm -m claude-sonnet-5 --schema 'name,age int,bio: one sentence' 'invent a surprising dog'
```
Example output:
```json
{
  "name": "Whiskers the Mathematical Mastiff",
  "age": 7,
  "bio": "Whiskers is a mastiff who can solve complex calculus problems by barking in binary code and has won three international mathematics competitions against human competitors."
}
```

## Web search

Newer models support Anthropic's [web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) for real-time information, using the `-T WebSearch` server-side tool:

```bash
llm -m claude-sonnet-5 -T WebSearch 'What is the current weather in San Francisco?'
```
The tool accepts optional configuration:

```bash
llm -m claude-sonnet-5 \
  -T 'WebSearch(max_uses=2, user_location={"city": "London", "country": "GB"})' \
  'Recent headlines'
```
Available arguments:

- `max_uses`: maximum number of searches per request
- `allowed_domains` / `blocked_domains`: lists of domains to allow or block (cannot be combined)
- `user_location`: dictionary with optional `city`, `region`, `country` and `timezone` keys to localize results

Note that `user_location` affects the *results* of searches from the web search tool, but location information is not made directly available to the model.

On Claude 4.6 and later models this uses the `web_search_20260318` tool version with dynamic filtering; older models use the basic `web_search_20250305` version.

## Web fetch

Models that support web search can also use Anthropic's [web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool) to retrieve the full content of a URL, using the `-T WebFetch` server-side tool:

```bash
llm -m claude-sonnet-5 -T WebFetch 'Fetch https://www.example.com/ and quote its first heading'
```
For security reasons Claude can only fetch URLs that already appear in the conversation - provided by you or returned by a previous web search or fetch.

The tool accepts optional configuration:

```bash
llm -m claude-sonnet-5 \
  -T 'WebFetch(max_uses=2, max_content_tokens=20000)' \
  'Summarize https://www.example.com/'
```
Available arguments:

- `max_uses`: maximum number of fetches per request
- `allowed_domains` / `blocked_domains`: lists of domains to allow or block (cannot be combined)
- `citations`: set to `True` to enable citations for fetched content
- `max_content_tokens`: approximate cap on fetched content included in the context
- `use_cache`: set to `False` to bypass Anthropic's fetch cache (Claude 4.6 and later models only)

On Claude 4.6 and later models this uses the `web_fetch_20260318` tool version with [dynamic filtering](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool#dynamic-filtering); older models use the basic `web_fetch_20250910` version.

From Python, pass an instance of the `WebFetch` class in `tools=`:

```python
import llm
from llm_anthropic import WebFetch

model = llm.get_model("claude-sonnet-5")
response = model.prompt(
    "Fetch https://www.example.com/ and quote its first heading",
    tools=[WebFetch(max_uses=1)],
)
print(response.text())
```

## MCP connector

Models that support web search can also call tools on remote [MCP servers](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector) using the `AnthropicMCP` server-side tool. Anthropic connects to the server from their own infrastructure - it must be reachable over HTTPS:

```bash
llm -m claude-sonnet-5 \
  -T 'AnthropicMCP(url="https://mcp.deepwiki.com/mcp", name="deepwiki")' \
  'Use the deepwiki tools to say what simonw/llm does, one sentence'
```
Available arguments:

- `url`: the HTTPS URL of the remote MCP server (required)
- `name`: an identifier for the server - defaults to the URL's hostname
- `authorization_token`: OAuth bearer token, for servers that require authentication
- `allowed_tools`: optional list of tool names - if provided, only those tools are enabled

```bash
llm -m claude-sonnet-5 \
  -T 'AnthropicMCP(url="https://mcp.deepwiki.com/mcp", name="deepwiki", allowed_tools=["ask_question"])' \
  'What does simonw/llm do?'
```

You can pass multiple `MCP` tools to connect to more than one server in the same request. Only MCP tool calls are supported - not MCP resources or prompts.

From Python, pass an instance of the `AnthropicMCP` class in `tools=`:

```python
import llm
from llm_anthropic import AnthropicMCP

model = llm.get_model("claude-sonnet-5")
response = model.prompt(
    "Use the deepwiki tools to say what simonw/llm does, one sentence",
    tools=[AnthropicMCP(url="https://mcp.deepwiki.com/mcp", name="deepwiki")],
)
print(response.text())
```

This feature uses Anthropic's `mcp-client-2025-11-20` beta.

## Code execution

Claude 4.5 and later models support Anthropic's [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool), which runs Python and bash in a sandboxed server-side container. Use the `-T CodeExecution` server-side tool:

```bash
llm -m claude-sonnet-4.6 -T CodeExecution \
  'Compute the sha256 hex digest of the string "pelican"'
```
Each response that runs code reports a container ID in its `response_json`, visible with `llm logs --json`. Pass that ID back to reuse the container's files and state in a later prompt (containers expire after a period of inactivity):

```bash
llm -m claude-sonnet-4.6 -T 'CodeExecution(container="container_011CPd...")' \
  'Read /tmp/results.csv and summarize it'
```

## Fast mode

Some models support [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) for lower latency responses. Enable it with the `-o fast 1` option:
```bash
llm -m claude-opus-5 -o fast 1 'Fun facts about walruses'
```

## Usage from Python

Python code can access the models like this:
```python
import llm

model = llm.get_model("claude-haiku-4.5")
print(model.prompt("Fun facts about chipmunks"))
```
Consult [LLM's Python API documentation](https://llm.datasette.io/en/stable/python-api.html) for more details.

You can also import the model classes directly, which is useful if you want to point the `base_url` at a different Anthropic-compatible endpoint:
```python
from llm_anthropic import ClaudeMessages

model = ClaudeMessages(
    "MiniMax-M2",
    base_url="https://api.minimax.io/anthropic"
)

print(model.prompt("Fun facts about pangolins", key="eyJh..."))
```

## Mid-conversation system messages

Claude Opus 4.8 and the Claude 5 family models accept [updated system instructions part-way through a conversation](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages), which preserves prompt cache hits on earlier turns. Pass a `system` message in an explicit `messages=` chain:

```python
import llm
from llm import system, user, assistant

model = llm.get_model("claude-opus-5")
response = model.prompt(messages=[
    system("You are a helpful assistant."),
    user("Say hi to me, briefly"),
    assistant("Hi there!"),
    system("New instruction: reply only in French from now on"),
    user("Say goodbye to me, briefly"),
])
print(response.text())  # Au revoir !
```

The first system message is sent as the top-level system prompt; later ones are sent inline in the messages array, positioned automatically to satisfy the API's placement rules. Models older than Opus 4.8 raise a `ValueError` if a system message appears anywhere other than the start of the chain.

## Extended thinking

Anthropic models can spend [thinking tokens](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) reasoning through a prompt before producing their response. LLM streams that reasoning to standard error as it arrives - pass `-R/--hide-reasoning` to hide it. The reasoning is also logged, available as the `reasoning` field in `llm logs --json`.

**Claude 5 models think by default.** Tune how hard they think with the `thinking_effort` option - one of `low`, `medium`, `high`, `xhigh` or `max`:

```bash
llm -m claude-opus-5 -o thinking_effort max 'Design a fair algorithm for splitting rent between roommates with different sized rooms'
```
Sonnet 5 and Opus 5 can have thinking turned off entirely with `-o thinking 0`. Fable 5 always thinks - disabling it raises an error.

**Claude 4.6 and older models do not think unless asked.** Enable thinking with `-o thinking 1`:

```bash
llm -m claude-sonnet-4.6 -o thinking 1 'Write a convincing speech to congress about the need to protect the California Brown Pelican'
```
Claude 4.6 models (and Opus 4.5) also support `thinking_effort`, which implies `thinking 1`. Older models than that use a fixed 1,024 token thinking budget.

Claude 4.7 and later models leave the thinking trace out of the response by default, so this plugin asks the API for `display: summarized` whenever thinking is on. When `-R/--hide-reasoning` is set it passes `display: omitted` instead, which leaves the thinking trace out of the response entirely - it will not appear in your logs, though thinking tokens are still billed.

The `thinking_budget`, `thinking_display` and `thinking_adaptive` options were removed in llm-anthropic 0.26 - install `llm-anthropic==0.25` if you need them for older models.

## Model options

The following options can be passed using `-o name value` on the CLI or as `keyword=value` arguments to the Python `model.prompt()` method:

<!-- [[[cog
import cog, llm
_type_lookup = {
    "number": "float",
    "integer": "int",
    "string": "str",
    "object": "dict",
}

model = llm.get_model("claude-3.7-sonnet")
output = []
for name, field in model.Options.schema()["properties"].items():
    any_of = field.get("anyOf")
    if any_of is None:
        any_of = [{"type": field["type"]}]
    types = ", ".join(
        [
            _type_lookup.get(item["type"], item["type"])
            for item in any_of
            if item["type"] != "null"
        ]
    )
    bits = ["- **", name, "**: `", types, "`\n"]
    description = field.get("description", "")
    if description:
        bits.append('\n    ' + description + '\n\n')
    output.append("".join(bits))
cog.out("".join(output))
]]] -->
- **max_tokens**: `int`

    The maximum number of tokens to generate before stopping

- **temperature**: `float`

    Amount of randomness injected into the response. Defaults to 1.0. Ranges from 0.0 to 1.0. Use temperature closer to 0.0 for analytical / multiple choice, and closer to 1.0 for creative and generative tasks. Note that even with temperature of 0.0, the results will not be fully deterministic.

- **top_p**: `float`

    Use nucleus sampling. In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by top_p. You should either alter temperature or top_p, but not both. Recommended for advanced use cases only. You usually only need to use temperature.

- **top_k**: `int`

    Only sample from the top K options for each subsequent token. Used to remove 'long tail' low probability responses. Recommended for advanced use cases only. You usually only need to use temperature.

- **user_id**: `str`

    An external identifier for the user who is associated with the request

- **prefill**: `str`

    A prefill to use for the response

- **hide_prefill**: `boolean`

    Do not repeat the prefill value at the start of the response

- **stop_sequences**: `array, str`

    Custom text sequences that will cause the model to stop generating - pass either a list of strings or a single string

- **cache**: `boolean`

    Use Anthropic prompt cache for any attachments or fragments

- **fast**: `boolean`

    Use fast mode for lower latency responses: https://platform.claude.com/docs/en/build-with-claude/fast-mode

- **thinking**: `boolean`

    Enable thinking mode. Claude 5 models think by default - set to false to disable thinking on models that allow it

<!-- [[[end]]] -->

Claude 5 models no longer accept sampling parameters - setting `temperature`, `top_p` or `top_k` on those models returns an error from the Anthropic API.

The `prefill` option can be used to set the first part of the response. To increase the chance of returning JSON, set that to `{`:

```bash
llm -m claude-sonnet-5 'Fun data about pelicans' \
  -o prefill '{'
```
If you do not want the prefill token to be echoed in the response, set `hide_prefill` to `true`:

```bash
llm -m claude-haiku-4.5 'Short python function describing a pelican' \
  -o prefill '```python' \
  -o hide_prefill true \
  -o stop_sequences '```'
```
This example sets `` ``` `` as the stop sequence, so the response will be a Python function without the wrapping Markdown code block.

To pass a single stop sequence, send a string:
```bash
llm -m claude-sonnet-5 'Fun facts about pelicans' \
  -o stop-sequences "beak"
```
For multiple stop sequences, pass a JSON array:

```bash
llm -m claude-sonnet-5 'Fun facts about pelicans' \
  -o stop-sequences '["beak", "feathers"]'
```

When using the Python API, pass a string or an array of strings:

```python
response = llm.query(
    model="claude-sonnet-5",
    query="Fun facts about pelicans",
    stop_sequences=["beak", "feathers"],
)
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-anthropic
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e . --group dev
```
To run the tests:
```bash
pytest
```

Alternatively, if you have [uv](https://github.com/astral-sh/uv) you can run tests without first creating a virtual environment like this:
```bash
uv run pytest
uv run pytest -k test_tools
```

You can also run the `llm` command in a `uv` managed environment like this:
```bash
uv run llm 'your prompt here'
```
To enable debug logs while running ([like this](https://github.com/simonw/llm-anthropic/issues/54#issuecomment-3536842831)), set this environment variable:
```bash
export ANTHROPIC_LOG=debug
```

This project uses [pytest-recording](https://github.com/kiwicom/pytest-recording) to record Anthropic API responses for the tests, and [inline-snapshot](https://15r10nk.github.io/inline-snapshot/) for test assertions.

If you add a new test that calls the API you can capture the API response like this:
```bash
PYTEST_ANTHROPIC_API_KEY="$(llm keys get anthropic)" uv run pytest --record-mode once
```
You will need to have stored a valid Anthropic API key using this command first:
```bash
llm keys set anthropic
# Paste key here
```
To re-record all cassettes and update all inline snapshot assertions in one command:
```bash
rm tests/cassettes/test_anthropic/*.yaml
PYTEST_ANTHROPIC_API_KEY="$(llm keys get anthropic)" uv run pytest --record-mode all --inline-snapshot=fix
```
To re-record a single test:
```bash
rm tests/cassettes/test_anthropic/test_thinking_prompt.yaml
PYTEST_ANTHROPIC_API_KEY="$(llm keys get anthropic)" uv run pytest -k test_thinking_prompt --record-mode once --inline-snapshot=fix
```
