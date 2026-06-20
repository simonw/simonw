# higher-lower

[![PyPI](https://img.shields.io/pypi/v/higher-lower.svg)](https://pypi.org/project/higher-lower/)
[![Changelog](https://img.shields.io/github/v/release/simonw/higher-lower?label=changelog)](https://github.com/simonw/higher-lower/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/higher-lower/blob/main/LICENSE)

Functions for finding numbers using higher/lower

## Installation

Install this library using `pip`:

    $ pip install higher-lower

## higher_lower(min_value, max_value, callback)

The `higher_lower()` function searches for a value between `min_value` and `max_value`, calling `callback()` for each candidate value to see if the target is higher or lower.

- `min_value` - the lowest possible value
- `max_value` - the highest possible value
- `callback(candidate)` - a callback function that takes a single integer argument and returns `ActualIs.MATCH`, `ActualIs.HIGHER` or `ActualIs.LOWER`

For example:

```python
from higher_lower import ActualIs

def callback(candidate):
    if candidate == 7:
        return ActualIs.MATCH
    elif candidate > 7:
        return ActualIs.LOWER
    else:
        return ActualIs.HIGHER
```
Given the above callback function, a search can be made for the number between 0 and 100 like so:
```python
from higher_lower import higher_lower

number = higher_lower(0, 100, callback)
# number is now 7
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd higher-lower
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
