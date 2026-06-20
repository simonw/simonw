# llm-echo

[![PyPI](https://img.shields.io/pypi/v/llm-echo.svg)](https://pypi.org/project/llm-echo/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-echo?include_prereleases&label=changelog)](https://github.com/simonw/llm-echo/releases)
[![Tests](https://github.com/simonw/llm-echo/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-echo/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-echo/blob/main/LICENSE)

Debug plugin for LLM. Adds a model which echos its input without hitting an API or executing a local LLM.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-echo
```
## Usage

The plugin adds a `echo` model which simply echos the prompt details back to you as JSON.

```bash
llm -m echo prompt -s 'system prompt'
```
Output:
```json
{
  "prompt": "prompt",
  "system": "system prompt",
  "attachments": [],
  "stream": true,
  "previous": []
}
```
You can also add one example option like this:
```bash
llm -m echo prompt -o example_bool 1
```
Output:
```json
{
  "prompt": "prompt",
  "system": "",
  "attachments": [],
  "stream": true,
  "previous": [],
  "options": {
    "example_bool": true
  }
}
```

## Reasoning chunks

Pass `-o thinking 1` to make the model emit two canned reasoning chunks before its normal JSON output. Useful for testing code that handles streaming reasoning tokens or persists `ReasoningPart`s.

```bash
llm -m echo 'hello' -o thinking 1
```

The two reasoning chunks are `"First I consider the prompt, "` and `"then I decide what to say."`, followed by the usual echo JSON as a text part.

## Tool calling

You can use `llm-echo` to test tool calling without needing to run prompts through an actual LLM. In your prompt, send something like this:

```json
{
  "prompt": "This will be treated as the prompt",
  "tool_calls": [
    {
      "name": "example",
      "arguments": {
        "input": "Hello, world!"
      }
    }
  ]
}
```
You can assemble a test that looks like this:
```python
def example(input: str) -> str:
    return f"Example output for {input}"

model = llm.get_model("echo")
chain_response = model.chain(
    json.dumps(
        {
            "tool_calls": [
                {
                    "name": "example",
                    "arguments": {"input": "test"},
                }
            ],
            "prompt": "prompt",
        }
    ),
    system="system",
    tools=[example],
)
responses = list(chain_response.responses())
tool_calls = responses[0].tool_calls()
assert tool_calls == [
    llm.ToolCall(name="example", arguments={"input": "test"}, tool_call_id=None)
]
assert responses[1].prompt.tool_results == [
    llm.models.ToolResult(
        name="example", output="Example output for test", tool_call_id=None
    )
]
```
Or you can read the JSON from the last response in the chain:
```python
response_info = json.loads(responses[-1].text())
```
And run assertions against the `"tool_results"` key, which should look something like this:
```python
{
  "prompt": "",
  "system": "",
  "...": "...",
  "tool_results": [
    {
      "name": "example",
      "output": "Example output for test",
      "tool_call_id": null
    }
  ]
}
```
Take a look at the [test suite for llm-tools-simpleeval](https://github.com/simonw/llm-tools-simpleeval/blob/main/tests/test_tools_simpleeval.py) for an example of how to write tests against tools.

## echo-needs-key model

The plugin also provides an `echo-needs-key` model which behaves identically to `echo` but requires an API key. This is useful for testing key resolution logic in plugins like [datasette-llm](https://github.com/datasette/datasette-llm).

The resolved key is included in the JSON output:

```bash
LLM_ECHO_NEEDS_KEY_KEY=sk-test-123 llm -m echo-needs-key 'hello'
```
Output:
```json
{
  "prompt": "hello",
  "system": "",
  "attachments": [],
  "stream": true,
  "previous": [],
  "key": "sk-test-123"
}
```

The model's `needs_key` is `"echo-needs-key"` and its `key_env_var` is `LLM_ECHO_NEEDS_KEY_KEY`.

## Raw responses

Sometimes it can be useful to output an exact string, for example if you are testing the `--extract` option in LLM.

If your prompt is JSON with a `"raw"` key that string is the only thing that will be returned. For example:
```json
{
  "raw": "This is the raw response"
}
```
Will return:
```
This is the raw response
```

## Development

To set up this plugin locally, first checkout the code. Then run the tests:
```bash
cd llm-echo
uv run pytest
```
