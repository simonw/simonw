# datasette-test

[![PyPI](https://img.shields.io/pypi/v/datasette-test.svg)](https://pypi.org/project/datasette-test/)
[![Tests](https://github.com/datasette/datasette-test/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-test/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-test?include_prereleases&label=changelog)](https://github.com/datasette/datasette-test/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-test/blob/main/LICENSE)

Utilities to help write tests for Datasette plugins and applications

## Installation

Install this library using `pip`:
```bash
pip install datasette-test
```
## Tests that use plugin configuration

Datasette 1.0a8 enforced a configuration change where plugins are no longer configured in metadata, but instead use a configuration file.

This can result in test failures in projects that use the `Datasette(metadata={"plugins": {"...": "..."}})` pattern to test out plugin configuration.

You can solve this using `datasette_test.Datasette`, a subclass that works with Datasette versions both before and after this breaking change:

```python
from datasette_test import Datasette
import pytest

@pytest.mark.asyncio
async def test_datasette():
    ds = Datasette(plugin_config={"my-plugin": {"config": "goes here"})
```
This subclass detects if the underlying plugin needs configuration in metadata or config and instantiates the class correctly either way.

You can also use this class while continuing to pass `metadata={"plugins": ...}` - the class will move that configuration to config when necessary.

## permissions= convenience argument

Datasette 1.0a introduces a [more convenient way](https://docs.datasette.io/en/1.0a13/authentication.html#other-permissions-in-datasette-yaml) of defining permissions directly in the configuration:
```python
ds = Datasette(config={"permissions": {"view-instance": {"id": "root"}}})
```
This is not supported by Datasette pre 1.0 - but you can use the `permissions=` argument in `datasette_test.Datasette` to achieve the same effect:
```python
ds = Datasette(permissions={"view-instance": {"id": "root"}})
```
This will work across both major Datasette versions.

## wait_until_responds(url, timeout=5.0)

Some Datasette plugin test suites launch a Datasette server and then need to wait for that server to become available before continuing.

Call this function to wait until the server becomes available, or raise an error if it takes longer than the timeout:

```python
from datasette_test import wait_until_responds

def test_server():
    # ... start server ...
    wait_until_responds("http://localhost:8001")
    # Now run tests
```

## actor_cookie(datasette, actor)

Equivalent to `datasette.client.actor_cookie()` in Datasette 1.0a+. Example usage:

```python
@pytest.mark.asyncio
async def test_permissions():
    ds = Datasette(permissions={"view-instance": {"id": "root"}})
    response = await ds.client.get("/")
    assert response.status_code == 403
    response = await ds.client.get(
        "/", cookies={"ds_actor": actor_cookie(ds, {"id": "root"})}
    )
    assert response.status_code == 200
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-test
python -m venv venv
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
