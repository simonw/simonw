# research-llm-apis

Curl-based examples and captured responses for the HTTP APIs of OpenAI, Anthropic, Gemini and Mistral. Intended as reference material for understanding how these APIs work.

## What's in here

- **`openai.sh`**, **`anthropic.sh`**, **`gemini.sh`**, **`mistral.sh`** — bash scripts that exercise each provider's API using `curl` and save the raw responses.
- **`responses/`** — captured JSON and streaming responses from each provider, covering text completion, streaming, vision, tool calling, reasoning/thinking, and web search.
- **`notes-*.md`** — LLM-generated reference notes for each provider: endpoints, authentication, request/response formats, and feature-specific details (tool calling, streaming, vision, thinking, etc.).
- **`client-libraries/`** — Git submodules of the official Python client libraries for each provider ([openai-python](https://github.com/openai/openai-python), [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python), [python-genai](https://github.com/googleapis/python-genai), [client-python](https://github.com/mistralai/client-python)) - these were used by Claude Code to help build the `curl` scripts and API notes.

## Running the scripts

Each script hits one provider's API and saves raw responses to `responses/`.

Set the appropriate environment variable for the provider you want to test:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."
export MISTRAL_API_KEY="..."
```

Then run the script:

```bash
bash openai.sh
bash anthropic.sh
bash gemini.sh
bash mistral.sh
```

If no environment variable is set, the scripts will fall back to [`llm keys get`](https://llm.datasette.io/en/stable/setup.html#saving-and-using-api-keys) to retrieve the key. If neither is available, the script will exit with an error.

## Cloning the client libraries

Clone with submodules to pull down the client library source code:

```bash
git clone --recurse-submodules <url>
```

Or if you've already cloned the repo:

```bash
git submodule update --init
```
