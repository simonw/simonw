# datasette-seaborn

[![PyPI](https://img.shields.io/pypi/v/datasette-seaborn.svg)](https://pypi.org/project/datasette-seaborn/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-seaborn?include_prereleases&label=changelog)](https://github.com/simonw/datasette-seaborn/releases)
[![Tests](https://github.com/simonw/datasette-seaborn/workflows/Test/badge.svg)](https://github.com/simonw/datasette-seaborn/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-seaborn/blob/main/LICENSE)

Statistical visualizations for Datasette using Seaborn

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-seaborn

## Usage

Navigate to the new `.seaborn` extension for any Datasette table.

The `_seaborn` argument specifies a method on `sns` to execute, e.g. `?_seaborn=relplot`.

Extra arguments to those methods can be specified using e.g. `&_seaborn_x=column_name`.

## Configuration

The plugin implements a default rendering time limit of five seconds. You can customize this limit using the `render_time_limit` setting, which accepts a floating point number of seconds. Add this to your `metadata.json`:

```json
{
    "plugins": {
        "datasette-seaborn": {
            "render_time_limit": 1.0
        }
    }
}
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-seaborn
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
