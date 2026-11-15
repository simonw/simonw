# datasette-llm

[![PyPI](https://img.shields.io/pypi/v/datasette-llm.svg)](https://pypi.org/project/datasette-llm/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-llm?include_prereleases&label=changelog)](https://github.com/datasette/datasette-llm/releases)
[![Tests](https://github.com/datasette/datasette-llm/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-llm/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-llm/blob/main/LICENSE)

LLM integration for Datasette plugins.

This plugin provides a standard interface for Datasette plugins to use LLM models via the [llm](https://llm.datasette.io/) library, with:

- **Model management**: Control which models are available, with filtering, defaults, and model options
- **API key management**: Integration with [datasette-secrets](https://github.com/datasette/datasette-secrets) for secure key storage
- **Hooks for extensibility**: Track usage, enforce policies, implement accounting

See the [unreleased changes and compatibility notes](CHANGELOG.md#unreleased) before upgrading.

## Installation

Install this plugin in the same environment as Datasette:

```bash
datasette install datasette-llm
```

You'll also need at least one LLM model plugin installed:

```bash
# For OpenAI models
datasette install llm

# For Anthropic models
datasette install llm-anthropic

# For testing without API calls
datasette install llm-echo
```

## Configuration

Configure the plugin in your `datasette.yaml`:

```yaml
plugins:
  datasette-llm:
    # Default model when none specified
    default_model: gpt-5.4-mini

    # Purpose-specific configuration
    purposes:
      enrichments:
        model: gpt-5.4-nano      # Default model for bulk operations
      sql-assistant:
        model: gpt-5.4           # Smarter for complex queries
        models:                  # Only these models for SQL assistance
        - gpt-5.4
        - gpt-5.4-mini
      extract:
        model: claude-sonnet-4.6
        blocked_models:          # Block specific models for extraction
        - gpt-5.4-pro
      chat:
        model: claude-sonnet-4.6

    # Model availability (optional)
    models:                      # Allowlist - only these models available
    - gpt-5.4
    - gpt-5.4-mini
    - gpt-5.4-nano
    - claude-sonnet-4.6

    # Or use a blocklist instead
    blocked_models:
    - gpt-5.4-pro                # Too expensive

    # Only show models with API keys configured (default: true)
    require_keys: true
```

### Model references with custom API keys and options

Anywhere a model name string is accepted in configuration (`default_model`, `purposes.<name>.model`, or entries in global or purpose-specific `models` lists), you can use a dictionary instead. Use global or purpose-specific `endpoints` lists to register additional endpoint dictionaries without enabling an allowlist. Dictionaries are also accepted by `llm.model()` and `llm.group()`.

The dictionary supports these fields:

- **`model`**: Required model ID, e.g. `"gpt-5.4-mini"`.
- **`key`**: Optional [datasette-secrets](https://github.com/datasette/datasette-secrets) secret name or stored LLM key alias to use as the API key for that model.
- **`options`**: Optional dictionary of default prompt options for that model. These are passed through to the underlying [llm](https://llm.datasette.io/) model plugin, so supported option names depend on the selected model.

```yaml
plugins:
  datasette-llm:
    # Default model with a custom key and default options
    default_model:
      model: gpt-5.4-mini
      key: CUSTOM_OPENAI_KEY
      options:
        temperature: 0.2

    purposes:
      # Pin a purpose to one model with its own billing key and options
      query-assistant:
        model:
          model: gpt-5.4-mini
          key: QUERY_ASSISTANT_KEY
          options:
            temperature: 0

      # Multiple models, each with their own key and/or options
      enrichments:
        model:
          model: gpt-5.4-nano
          key: ENRICHMENTS_NANO_KEY
          options:
            max_tokens: 1000
        models:
          - model: gpt-5.4
            key: ENRICHMENTS_GPT5_KEY
          - model: gpt-5.4-mini
            key: ENRICHMENTS_MINI_KEY
            options:
              temperature: 0.1
          - claude-sonnet-4.6      # Falls through to default key resolution
```

Configured `options` become defaults for calls made through `await llm.model()` or `llm.group()`. Per-call options override configured defaults:

```python
model = await llm.model()

# Uses temperature: 0.2 from datasette.yaml
response = await model.prompt("Suggest three tags")

# Overrides the configured temperature for this one prompt
response = await model.prompt("Suggest three tags", temperature=0.7)
```

For chained prompts, pass per-call overrides in the `options=` dictionary:

```python
responses = model.chain(
    "Suggest three tags",
    options={"temperature": 0.7},
)
```

The `key` field is resolved through datasette-secrets first, so you can set it via environment variables:

```bash
export DATASETTE_SECRETS_QUERY_ASSISTANT_KEY=sk-...
export DATASETTE_SECRETS_ENRICHMENTS_NANO_KEY=sk-...
```

If that secret is unavailable, the same name is looked up in LLM's stored keys. For example, `key: openrouter` uses the key saved with `llm keys set openrouter`. An explicitly named key that is missing from both sources raises `llm.NeedsKeyException` when selected, and the model is excluded from lists when `require_keys` is true. A missing alias is never sent as a literal key and never falls back to another provider credential.

The configured key name and default options are selected from the first matching reference that supplies the setting:

1. A dictionary passed directly to `llm.model()` or `llm.group()`
2. A matching dictionary in the purpose's `models` list
3. The purpose's default `model` dictionary
4. A matching dictionary in the purpose's `endpoints` list
5. The global `default_model` dictionary
6. A matching dictionary in the global `models` list
7. A matching dictionary in the global `endpoints` list

For installed models without an explicit key name, standard provider key resolution applies: datasette-secrets (`<PROVIDER>_API_KEY`), then LLM's stored provider key or environment variable.

The `blocked_models` fields remain lists of model ID strings.

### OpenAI-compatible endpoints

Add `api_base` to a model reference to use an arbitrary OpenAI-compatible Chat Completions or Responses endpoint. This requires no additional LLM plugin or changes to LLM's model configuration file. For example, use Qwen3.8 27B served by LM Studio through its local Responses API:

```yaml
plugins:
  datasette-llm:
    default_model: lmstudio-qwen

    endpoints:
      - model: lmstudio-qwen
        model_name: qwen/qwen3.8-27b
        api_base: http://localhost:1234/v1
        responses: true
      - model: hosted-assistant
        model_name: organization/assistant
        api_base: https://models.example.com/v1
        responses: true
        key: openrouter
        options:
          temperature: 0.2

    purposes:
      sql-assistant:
        model: hosted-assistant
```

`endpoints` registers models without restricting the installed models available to Datasette. The `models` setting remains an allowlist: if you configure it, registered endpoints must be allowed there or selected as the configured default. You can also place an endpoint dictionary directly in a default or a `models` list when those filtering semantics are intended. A purpose-specific `endpoints` list registers models only for that purpose.

`model` is the local ID used by Datasette model pickers, hooks, allowlists and blocklists. `model_name` is the ID sent to the endpoint and defaults to `model`. Use distinct local IDs for different endpoints serving the same remote model, or to avoid a collision with an installed model or alias.

`api_base` is the HTTP or HTTPS base URL, including any required path prefix such as `/v1`. Chat Completions requests append `/chat/completions`; set `responses: true` to append `/responses` instead. URLs with embedded credentials, query strings or fragments are rejected.

Endpoint models support tool calling by default. Pass tools through the existing chain API:

```python
def double(number: int) -> int:
    return number * 2

model = await llm.model("hosted-assistant")
chain = model.chain("What is double 21?", tools=[double])
async for response in chain.responses():
    print(await response.text())
```

The endpoint must support the selected protocol and any capabilities you use. Additional endpoint fields follow LLM's configuration conventions: `supports_tools` and `can_stream` default to true; `supports_schema`, `vision`, `audio` and `reasoning` default to false. Set `can_stream: false` for a server that requires non-streaming requests. `headers` accepts a dictionary of extra HTTP headers. Reasoning summaries are only requested when explicitly selected through prompt options.

Put credentials in `key`, using a Datasette secret or stored LLM key alias. Do not put credentials such as `Authorization: Bearer ...` in `headers`: those values can be visible to anonymous users at `/-/config.json`.

An endpoint without `key` is treated as unauthenticated and remains available with `require_keys: true`. It never receives the default OpenAI key. To use an existing stored LLM key, set `key` to its alias, such as `openrouter` after running `llm keys set openrouter`. Setting `key: openai` deliberately selects that named key; it is never selected implicitly. Datasette-secrets takes precedence over the stored LLM alias.

Definitions in global `endpoints`, the global default or the global `models` list are available globally. Definitions appearing only under a purpose are available for that purpose. A model defined in the active configuration can be selected by its local ID, including from an `llm_default_model` hook. Repeated definitions of an ID must agree on endpoint, remote model name, protocol and capabilities; keys and prompt options can vary by purpose. An invalid reference raises `ModelConfigurationError` from the lookups that use it: every lookup if it is global, or only that purpose's lookups if it appears under a purpose. It does not prevent other plugins from using datasette-secrets. Conflicting endpoints, including IDs that clash with an installed alias, are omitted from listings; selecting that endpoint raises `ModelConfigurationError`. Other installed models remain usable.

You can also provide an endpoint directly in Python:

```python
model = await llm.model({
    "model": "lmstudio-qwen",
    "model_name": "qwen/qwen3.8-27b",
    "api_base": "http://localhost:1234/v1",
    "responses": True,
})
```

The same dictionary works with `llm.group()`. Direct definitions apply to that call and are not registered with LLM or added to later model listings. All model selection paths apply the configured allowlists, blocklists, key requirements and filter hooks.

### Falling back to LLM's default model

If neither `default_model` nor a purpose-specific `model` is configured, datasette-llm falls back to [LLM's own default model](https://llm.datasette.io/en/stable/setup.html#setting-a-custom-default-model) - the model set using `llm models default <model>`, or LLM's built-in default if none has been set.

This fallback is only used if that model is available to Datasette: it must have an API key (unless `require_keys` is `false`) and must not be excluded by the `models` or `blocked_models` settings or by an `llm_filter_models` hook. Unlike `default_model`, LLM's default model is not automatically added to the `models` allowlist. If the fallback model is not available, calling `await llm.model()` without a model ID raises a `ModelNotFoundError`.

### Model filtering

The `models` and `blocked_models` keys control which models are available. Use `models` to define an allowlist (only these models will be available) or `blocked_models` to define a blocklist (all models except these will be available). If both are set, the allowlist is applied first and the blocklist removes from the result. The `default_model` is automatically included in the allowlist, so you don't need to repeat it there. These restrictions and `llm_filter_models` hooks apply to both listing and selecting models, including explicit IDs and configured defaults. Selecting an excluded model raises `ModelNotFoundError`.

### Purpose-specific configuration

Plugins register **purposes** to describe what they use LLM models for (e.g. `"extract"`, `"enrichments"`, `"sql-assistant"`). Each purpose can have its own configuration under `purposes.<name>`:

- **`model`**: The default model for this purpose, used when a plugin calls `await llm.model(purpose="extract")` without specifying a model ID.
- **`models`**: Additional allowed models for this purpose, combined with the global `models` allowlist. A model can be available for a specific purpose even if it is not in the global list. The purpose's default `model` and global `default_model` are automatically included, so you don't need to repeat them. Purpose models are listed before remaining global models, with the selected default first.
- **`blocked_models`**: A blocklist of models for this purpose. These are removed even if the model is globally allowed.

When no purpose-specific `models` list is set, the global `models` allowlist applies. The global `blocked_models` always applies regardless of purpose configuration.

## API Key Management

datasette-llm integrates with [datasette-secrets](https://github.com/datasette/datasette-secrets) for API key management. Keys are automatically registered for all installed model providers.

### Setting up keys

1. **Via environment variables** (recommended for deployment):
   ```bash
   export DATASETTE_SECRETS_OPENAI_API_KEY=sk-...
   export DATASETTE_SECRETS_ANTHROPIC_API_KEY=sk-ant-...
   ```

2. **Via the web interface**: Navigate to `/-/secrets` (requires `manage-secrets` permission)

3. **Via llm CLI** (fallback): Keys set with `llm keys set openai` are also used

### Key resolution order

1. datasette-secrets (env var `DATASETTE_SECRETS_<PROVIDER>_API_KEY` or encrypted database)
2. llm's keys.json (`~/.config/io.datasette.llm/keys.json`)
3. llm's environment variables (e.g., `OPENAI_API_KEY`)

## Usage

All examples below assume you have created an `LLM` instance:

```python
from datasette_llm import LLM

llm = LLM(datasette)
```

### `llm.model()`

```python
async def model(
    model_id: Optional[str | dict] = None,
    purpose: Optional[str] = None,
    actor: Optional[dict] = None,
) -> WrappedAsyncModel
```

Get an async model wrapped with hook support. Returns a `WrappedAsyncModel` that invokes hooks around prompts.

Parameters:

- **`model_id`** (`Optional[str | dict]`): The model ID or model-reference dictionary to use, e.g. `"gpt-5.4-mini"` or an [endpoint reference](#openai-compatible-endpoints). If not provided, the default model is resolved from configuration — first checking the purpose-specific `model` setting, then the global `default_model`, then [LLM's own default model](#falling-back-to-llms-default-model).
- **`purpose`** (`Optional[str]`): Identifies what this model will be used for, e.g. `"enrichments"`, `"sql-assistant"`. This selects the purpose-specific default model and is passed through to hooks like `llm_prompt_context` for auditing and accounting.
- **`actor`** (`Optional[dict]`): The Datasette actor dictionary for the current user. Pass this to enable two things: **per-user model filtering**, where plugins using the `llm_filter_models` or `llm_default_model` hooks can restrict or customize models based on who is making the request; and **audit logging**, where auditing plugins that implement `llm_prompt_context` can record which actor ran which prompts.

```python
async def my_plugin_view(datasette, request):
    llm = LLM(datasette)

    # Get the default model
    model = await llm.model()

    # Specify a model explicitly
    model = await llm.model("gpt-5.4-mini")

    # With purpose and actor for auditing and filtering
    model = await llm.model(
        purpose="sql-assistant",
        actor=request.actor,
    )

    # Execute a prompt
    response = await model.prompt("What is the capital of France?")
    text = await response.text()
```

### `llm.models()`

```python
async def models(
    actor: Optional[dict] = None,
    purpose: Optional[str] = None,
) -> List
```

Get available models, filtered by configuration, API key availability, and hooks. Returns a list of model objects.

Parameters:

- **`actor`** (`Optional[dict]`): The Datasette actor dictionary. When provided, the `llm_filter_models` hook can use this to return only models the actor is allowed to use — for example, restricting anonymous users to cheaper models, or looking up per-user model allowlists in a database. Auditing plugins can also use this to log which actors are querying model availability.
- **`purpose`** (`Optional[str]`): When provided, purpose-specific `models` and `blocked_models` configuration is applied. A purpose-specific `models` allowlist is combined with the global allowlist, so models can be made available for a specific purpose even if they aren't globally listed.

```python
llm = LLM(datasette)

# Get all available models (filtered by config and key availability)
models = await llm.models()
for model in models:
    print(model.model_id)

# Filter by actor (for per-user permissions)
models = await llm.models(actor=request.actor)

# Filter by purpose (applies purpose-specific models/blocked_models config)
models = await llm.models(purpose="enrichments")

# Both together — e.g. to populate a model picker for the current user
models = await llm.models(actor=request.actor, purpose="sql-assistant")
```

### Streaming responses

```python
model = await llm.model("gpt-5.4-mini")
response = await model.prompt("Tell me a story")

# Non-streaming - wait for complete response
text = await response.text()

# Streaming - process chunks as they arrive
async for chunk in response:
    print(chunk, end="", flush=True)
```

### Grouping prompts

Use `group()` for batch operations where multiple prompts are logically related:

```python
async def enrich_rows(datasette, rows):
    llm = LLM(datasette)

    # Model determined by purpose configuration
    async with llm.group(purpose="enrichments") as model:
        results = []
        for row in rows:
            response = await model.prompt(f"Summarize: {row['content']}")
            text = await response.text()
            results.append(text)

    # All responses guaranteed complete here
    return results
```

Benefits of `group()`:
- **Transactional semantics**: All responses forced to complete on exit
- **Shared context**: Hooks can treat grouped prompts together (e.g., shared budget reservation)
- **Cleanup**: The `llm_group_exit` hook is called for settlement/logging

## Plugin Hooks

datasette-llm provides hooks for other plugins to extend LLM operations.

### `llm_prompt_context`

Wrap prompt execution with custom logic. The same hook is used for direct
`prompt()` calls and for each response yielded by `chain()`:

```python
from datasette import hookimpl
from contextlib import asynccontextmanager

@hookimpl
def llm_prompt_context(datasette, model_id, prompt, purpose, actor):
    @asynccontextmanager
    async def wrapper(result):
        # Before the prompt executes
        actor_id = actor.get("id") if actor else None
        print(f"Starting prompt to {model_id} by {actor_id}")

        yield

        # After prompt() returns or chain() is initialized
        async def on_complete(response):
            usage = await response.usage()
            print(f"Used {usage.input} input, {usage.output} output tokens")

        await result.on_response_done(on_complete)

    return wrapper
```

`prompt` is the text of the new input. When a caller passes its whole input
as `messages=` with no prompt text, `prompt` is the text of the final
message, provided that is a user message. It is `None` when there is no new
user input, for example a chain resumed from a history that ends in
unresolved tool calls.

`result.response` continues to expose the first response, while
`result.responses` contains all responses seen so far. The
`await result.on_response_done(callback)` helper attaches a callback to all
existing responses and any future responses produced by a chain.

### `llm_group_exit`

Called when a `group()` context manager exits:

```python
@hookimpl
def llm_group_exit(datasette, group):
    # Can return a coroutine for async cleanup
    async def cleanup():
        print(f"Group for {group.purpose} completed")
        print(f"Processed {len(group._responses)} prompts")
    return cleanup()
```

### `register_llm_purposes`

Register purpose strings that your plugin uses, along with documentation explaining what they mean.

```python
from datasette import hookimpl
from datasette_llm import Purpose

@hookimpl
def register_llm_purposes(datasette):
    return [
        Purpose(
            name="query-assistant",
            description="Assists users with writing SQL queries",
        ),
        Purpose(
            name="suggest-table-names",
            description="Suggests names for tables based on imported CSV files",
        ),
    ]
```

Registered purposes can be retrieved by other plugins (e.g., to build an admin UI for model assignment):

```python
from datasette_llm import get_purposes

purposes = get_purposes(datasette)
for purpose in purposes:
    print(f"{purpose.name}: {purpose.description}")
```

If multiple plugins register the same purpose name, the first registration wins.

### `llm_filter_models`

Influence the models that are returned from the `await llm.models()` method. Plugins can use this to add custom logic informing which models are available, taking into account both the actor and the purpose of the prompt.

- `models` is a list of available model objects from all of the installed [LLM plugins](https://llm.datasette.io/en/stable/plugins/directory.html).
- `actor` is an actor dictionary or `None`
- `purpose` is a purpose string or `None`

The `actor` and `purpose` are the ones that were passed to the `llm.models(actor=..., purpose=...)` method.

All filter hooks receive the same initial list of models after API key filtering. Their returned lists are intersected by model ID, so a model must be allowed by every hook that returns a list. Return `None` to leave availability unchanged, or an empty list to make no models available. A hook cannot restore a model excluded by another hook.

```python
@hookimpl
async def llm_filter_models(datasette, models, actor, purpose):
    if not actor:
        # Anonymous users get limited models
        return [m for m in models if m.model_id == "gpt-5.4-mini"]

    # Check database for user's allowed models
    db = datasette.get_database()
    result = await db.execute(
        "SELECT model_id FROM user_models WHERE user_id = ?",
        [actor["id"]]
    )
    allowed = {row["model_id"] for row in result.rows}
    return [m for m in models if m.model_id in allowed]
```

### `llm_default_model`

This plugin hook is used when `await llm.model()` is called without any arguments - or with a `purpose` and/or `actor` specified. Plugins can use this to control which default model is used, including for a given purpose.

```python
@hookimpl
async def llm_default_model(datasette, purpose, actor):
    if actor:
        # Check user's preferred model
        db = datasette.get_database()
        result = await db.execute(
            "SELECT preferred_model FROM user_prefs WHERE user_id = ?",
            [actor["id"]]
        )
        row = result.first()
        if row:
            return row["preferred_model"]
    return None  # Use config defaults
```

## Related Plugins

- **[datasette-secrets](https://github.com/datasette/datasette-secrets)**: Secure API key storage (required dependency)
- **[datasette-llm-accountant](https://github.com/datasette/datasette-llm-accountant)**: Budget management and cost tracking

## Development

To set up this plugin locally:

```bash
cd datasette-llm
uv sync

# Confirm the plugin is visible
uv run datasette plugins
```

To run the tests:

```bash
uv run pytest
```

The test suite uses the `llm-echo` model which echoes back prompts without making API calls.
