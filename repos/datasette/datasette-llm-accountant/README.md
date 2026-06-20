# datasette-llm-accountant

[![PyPI](https://img.shields.io/pypi/v/datasette-llm-accountant.svg)](https://pypi.org/project/datasette-llm-accountant/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-llm-accountant?include_prereleases&label=changelog)](https://github.com/datasette/datasette-llm-accountant/releases)
[![Tests](https://github.com/datasette/datasette-llm-accountant/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-llm-accountant/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-llm-accountant/blob/main/LICENSE)

Budget management and cost tracking for LLM usage in Datasette.

## Installation

Install this plugin in the same environment as Datasette:

```bash
datasette install datasette-llm-accountant
```

This plugin works alongside [datasette-llm](https://github.com/datasette/datasette-llm) to provide automatic cost tracking and budget enforcement for LLM prompts.

## Overview

This plugin provides:

- **Automatic cost calculation** based on token usage and model pricing
- **Reserve/settle pattern** for budget enforcement
- **Accountant plugin system** for custom spending trackers
- **Custom pricing providers** with access to the full response object
- **Hook integration** with datasette-llm for transparent accounting

When installed, all prompts made through `datasette-llm` are automatically wrapped with accounting logic. Accountants can enforce spending limits, log usage, and track costs.

## How It Works

1. When a prompt is made via `datasette-llm`, this plugin's hooks intercept the call
2. A reservation is made with all registered accountants for the estimated cost
3. The prompt executes
4. The actual cost is calculated via `PricingProvider.calculate_cost_from_response()`
5. Accountants are settled with the real cost (refunding any unused reservation)

## Configuration

Configure reservation amounts in `datasette.yaml`:

```yaml
plugins:
  datasette-llm-accountant:
    # Default reservation for single prompts
    auto_reservation_usd: 0.10

    # Default reservation for grouped prompts
    default_reservation_usd: 0.50

    # Purpose-specific reservations
    purposes:
      enrichments:
        reservation_usd: 5.00
      query-assistant:
        reservation_usd: 0.25
```

## Nanocents

All monetary amounts use the `Nanocents` type — an `int` subclass that makes units explicit and prevents accidentally passing raw dollar amounts where nanocents are expected.

- 1 nanocent = 1/1,000,000,000 of a cent
- 1 USD = 100 cents = 100,000,000,000 nanocents
- This allows tracking costs down to fractions of a cent without floating-point errors

```python
from datasette_llm_accountant import Nanocents

# Create from USD or cents
cost = Nanocents.from_usd(1.50)   # 150,000,000,000
cost = Nanocents.from_cents(50)   # 50,000,000,000

# Convert back
cost.to_usd()    # 1.5
cost.to_cents()  # 150.0

# Works like a regular int for arithmetic
total = cost + Nanocents.from_usd(0.50)
```

## Creating an Accountant Plugin

Accountants track and enforce LLM spending. Create a plugin that implements the `register_llm_accountants` hook:

```python
from datasette import hookimpl
from datasette_llm_accountant import Accountant, Tx, Nanocents, InsufficientBalanceError

class MyAccountant(Accountant):
    """Custom accountant that tracks spending."""

    def __init__(self, datasette):
        self.datasette = datasette

    async def reserve(
        self,
        nanocents: Nanocents,
        model_id: str = None,
        purpose: str = None,
        actor_id: str = None,
    ) -> Tx:
        """Reserve the specified amount. Raise InsufficientBalanceError to block."""
        if not await self.has_sufficient_balance(nanocents):
            raise InsufficientBalanceError("Insufficient balance")
        tx_id = await self.create_reservation(nanocents, model_id, purpose)
        return Tx(tx_id)

    async def settle(
        self,
        tx: Tx,
        nanocents: Nanocents,
        model_id: str = None,
        purpose: str = None,
        actor_id: str = None,
    ):
        """Settle a transaction for the actual amount spent."""
        await self.record_settlement(tx, nanocents, model_id, purpose)

    async def rollback(self, tx: Tx):
        """Optional: Release a reservation without charging."""
        await self.settle(tx, Nanocents(0))

@hookimpl
def register_llm_accountants(datasette):
    return [MyAccountant(datasette)]
```

See [datasette-llm-allowance](https://github.com/datasette/datasette-llm-allowance) for a complete implementation that uses Datasette's internal database to track a spending allowance.

## Multiple Accountants

Multiple accountants can be registered. When a reservation is made:

1. All accountants are called in sequence to reserve the amount
2. If any accountant fails (e.g., `InsufficientBalanceError`), previous reservations are rolled back
3. When the prompt completes, all accountants are settled with the actual cost

This enables layered accounting (per-user limits, per-project budgets, global caps, etc.).

## Custom Pricing Providers

The default pricing provider fetches model prices from [llm-prices.com](https://www.llm-prices.com/). You can register a custom provider to control how costs are calculated:

```python
from datasette import hookimpl
from datasette_llm_accountant import PricingProvider, Nanocents

class MyPricingProvider(PricingProvider):
    async def calculate_cost_from_response(self, model_id, usage, response):
        """
        Calculate cost from a completed response.

        Args:
            model_id: The model identifier
            usage: An llm.Usage object with input/output token counts
            response: The llm.AsyncResponse object — use this to access
                      provider-specific metadata (e.g., generation IDs
                      for exact cost lookups from the provider's API)
        Returns:
            Cost as a Nanocents value
        """
        input_tokens = usage.input or 0
        output_tokens = usage.output or 0
        cost_usd = input_tokens * 0.01 / 1_000_000 + output_tokens * 0.03 / 1_000_000
        return Nanocents.from_usd(cost_usd)

    async def supported_models(self):
        """Return the set of model IDs this provider can price,
        or None to indicate all models are supported.

        Used to filter the model list — models not in this set
        won't be available when accountants are registered.
        """
        return self.known_models

@hookimpl
def register_llm_accountant_pricing(datasette):
    return MyPricingProvider()
```

## API Reference

### Accountant Base Class

```python
class Accountant(ABC):
    @abstractmethod
    async def reserve(
        self,
        nanocents: Nanocents,
        model_id: str = None,
        purpose: str = None,
        actor_id: str = None,
    ) -> Tx:
        """Reserve an amount, return transaction ID."""

    @abstractmethod
    async def settle(
        self,
        tx: Tx,
        nanocents: Nanocents,
        model_id: str = None,
        purpose: str = None,
        actor_id: str = None,
    ):
        """Settle a transaction for the actual amount."""

    async def rollback(self, tx: Tx):
        """Release a reservation (default: settle for 0)."""
        await self.settle(tx, Nanocents(0))
```

### PricingProvider Base Class

```python
class PricingProvider(ABC):
    @abstractmethod
    async def calculate_cost_from_response(
        self, model_id: str, usage: Usage, response: AsyncResponse
    ) -> Nanocents:
        """Calculate cost from a completed response."""

    async def supported_models(self) -> Optional[set[str]]:
        """Return set of supported model IDs, or None for all. Default: None."""
        return None
```

### Exceptions

- `InsufficientBalanceError` - Raised when an accountant cannot reserve the requested amount
- `ReservationExceededError` - Raised when actual cost exceeds the reserved amount
- `ModelPricingNotFoundError` - Raised when pricing data is not available for a model

## Development

```bash
cd datasette-llm-accountant
pip install -e '.[dev]'
pytest
```
