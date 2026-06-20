# llm-prices

Site is published to https://www.llm-prices.com/ using Cloudflare Pages.

[Background on this project](https://simonwillison.net/2025/May/7/llm-prices/)

## JSON APIs

The pricing data is available as JSON at the following URLs:

### Current prices

**https://www.llm-prices.com/current-v1.json**

An object containing:

- `updated_at`: Date when the pricing data was last updated (ISO 8601 format)
- `prices`: Array of objects representing the current pricing for each model

Each price object contains:

- `id`: Unique identifier for the model
- `vendor`: The vendor/provider name
- `name`: Human-readable model name
- `input`: Price per million input tokens (in USD)
- `output`: Price per million output tokens (in USD)
- `input_cached`: Price per million cached input tokens (in USD), or `null` if the model does not offer cached token pricing

Example:

```json
{
  "updated_at": "2025-10-10",
  "prices": [
    {
      "id": "amazon-nova-micro",
      "vendor": "amazon",
      "name": "Amazon Nova Micro",
      "input": 0.035,
      "output": 0.14,
      "input_cached": null
    },
    {
      "id": "amazon-nova-lite",
      "vendor": "amazon",
      "name": "Amazon Nova Lite",
      "input": 0.06,
      "output": 0.24,
      "input_cached": null
    }
  ]
}
```

### Historical prices

**https://www.llm-prices.com/historical-v1.json**

An object containing:

- `prices`: Array of objects representing all pricing records including historical changes

Each price object contains the same fields as current prices plus:

- `from_date`: Start date for this pricing (ISO 8601 format, or `null` for current prices). This date is inclusive.
- `to_date`: End date for this pricing (ISO 8601 format, or `null` for current prices). This date is exclusive - the price was valid up to but not including this date.

Example:

```json
{
  "prices": [
    {
      "id": "amazon-nova-lite",
      "vendor": "amazon",
      "name": "Amazon Nova Lite",
      "input": 0.06,
      "output": 0.24,
      "input_cached": null,
      "from_date": null,
      "to_date": null
    },
    {
      "id": "amazon-nova-micro",
      "vendor": "amazon",
      "name": "Amazon Nova Micro",
      "input": 0.035,
      "output": 0.14,
      "input_cached": null,
      "from_date": null,
      "to_date": null
    }
  ]
}
```

## How the data files work

The pricing data is maintained in individual JSON files in the `data/` directory, with one file per vendor (e.g., `data/anthropic.json`, `data/openai.json`).

Each vendor file has the following structure:

```json
{
  "vendor": "anthropic",
  "models": [
    {
      "id": "claude-3.7-sonnet",
      "name": "Claude 3.7 Sonnet",
      "price_history": [
        {
          "input": 3,
          "output": 15,
          "input_cached": null,
          "from_date": null,
          "to_date": null
        }
      ]
    }
  ]
}
```

### Fields

- `vendor`: The vendor identifier (lowercase, used to group models)
- `models`: Array of model objects, each containing:
  - `id`: Unique identifier for the model (used in URLs and as a key)
  - `name`: Human-readable display name for the model
  - `price_history`: Array of pricing records over time, each with:
    - `input`: Price per million input tokens (in USD)
    - `output`: Price per million output tokens (in USD)
    - `input_cached`: Price per million cached input tokens (in USD), or `null` if the model does not offer cached token pricing
    - `from_date`: Start date for this pricing (ISO 8601 format, or `null` for current/initial prices)
    - `to_date`: End date for this pricing (ISO 8601 format, or `null` for current prices)

### Price history

When a model's price changes, add a new entry to the `price_history` array:
- Set the `to_date` on the previous entry to the date the old price ended
- Add a new entry with the new prices, setting `from_date` to when the new price starts and `to_date` to `null`

#### Date semantics

- `from_date`: Inclusive start date (price is effective starting from this date)
- `to_date`: Exclusive end date (price is effective up to but NOT including this date)
- `null` dates: `from_date: null` means "from the beginning", `to_date: null` means "current price"

### Building the JSON files

After editing vendor files in `data/`, run:

```bash
python scripts/build.py
```

This generates `current-v1.json` and `historical-v1.json` files that are served on the website.
