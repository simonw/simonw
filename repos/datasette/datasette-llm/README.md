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

Anywhere a model name string is accepted in configuration (`default_model`, `purposes.<name>.model`, or entries in `purposes.<name>.models`), you can use a dictionary instead.

The dictionary supports these fields:

- **`model`**: Required model ID, e.g. `"gpt-5.4-mini"`.
- **`key`**: Optional [datasette-secrets](https://github.com/datasette/datasette-secrets) secret name to use as the API key for that model.
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

The `key` field is resolved through datasette-secrets, so you can set it via environment variables:

```bash
export DATASETTE_SECRETS_QUERY_ASSISTANT_KEY=sk-...
export DATASETTE_SECRETS_ENRICHMENTS_NANO_KEY=sk-...
```

When a model is used for a purpose, key resolution follows this order:

1. Key from the purpose's configuration (a matching dict in `model` or `models`)
2. Key from the `default_model` config (if it's a dict and matches)
3. Standard datasette-secrets resolution (`<PROVIDER>_API_KEY`)
4. llm's key resolution (keys.json, environment variables)

The `models` (global allowlist) and `blocked_models` fields remain plain string lists — custom keys and options are only supported in `default_model`, `purposes.<name>.model`, and `purposes.<name>.models`.

Model options use the same configuration resolution order as custom keys: the matching purpose-specific model reference is checked first, then the global `default_model` reference if it names the same model.

### Model filtering

The `models` and `blocked_models` keys control which models are available. Use `models` to define an allowlist (only these models will be available) or `blocked_models` to define a blocklist (all models except these will be available). If both are set, the allowlist is applied first and the blocklist removes from the result. The `default_model` is automatically included in the allowlist, so you don't need to repeat it there.

### Purpose-specific configuration

Plugins register **purposes** to describe what they use LLM models for (e.g. `"extract"`, `"enrichments"`, `"sql-assistant"`). Each purpose can have its own configuration under `purposes.<name>`:

- **`model`**: The default model for this purpose, used when a plugin calls `await llm.model(purpose="extract")` without specifying a model ID.
- **`models`**: An allowlist of models for this purpose. When set, this **overrides** the global `models` allowlist — so a model can be available for a specific purpose even if it is not in the global list. The purpose's default `model` is automatically included in this allowlist, so you don't need to repeat it. This filtering is applied when a plugin calls `await llm.models(purpose="extract")`.
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
    model_id: Optional[str] = None,
    purpose: Optional[str] = None,
    actor: Optional[dict] = None,
) -> WrappedAsyncModel
```

Get an async model wrapped with hook support. Returns a `WrappedAsyncModel` that invokes hooks around prompts.

Parameters:

- **`model_id`** (`Optional[str]`): The model to use, e.g. `"gpt-5.4-mini"` or `"claude-sonnet-4.6"`. If not provided, the default model is resolved from configuration — first checking the purpose-specific `model` setting, then the global `default_model`.
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
- **`purpose`** (`Optional[str]`): When provided, purpose-specific `models` and `blocked_models` configuration is applied. A purpose-specific `models` allowlist **overrides** the global allowlist, so models can be made available for a specific purpose even if they aren't globally listed.

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
