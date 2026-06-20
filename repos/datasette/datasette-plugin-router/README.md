# datasette-plugin-router

[![PyPI](https://img.shields.io/pypi/v/datasette-plugin-router.svg)](https://pypi.org/project/datasette-plugin-router/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-plugin-router?include_prereleases&label=changelog)](https://github.com/datasette/datasette-plugin-router/releases)
[![Tests](https://github.com/datasette/datasette-plugin-router/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-plugin-router/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-plugin-router/blob/main/LICENSE)

WIP router for Datasette plugins

Datasette plugins that have a lot of [custom API endpoints](https://docs.datasette.io/en/stable/plugin_hooks.html#register-routes-datasette) can get tiresome to write by hand.  `datasette-plugin-router` aims to be a small Python library that adds a FastAPI-like API for defining custom Datasette plugin endpoints.

- Define routes with familiar GET/POST decorators
- Define Pydantic-backed input/output schemas on JSON endpoints
- `register_routes()` compatability
- export to OpenAPI schema for codegen'ing clients


Sample usage:

```python
from datasette import Response, hookimpl
from datasette_plugin_router import Router, Body
from pydantic import BaseModel

router = Router()

class Input(BaseModel):
    id: int
    name: str

class Output(BaseModel):
    id_negative: int
    name_upper: str

@router.POST(r"/-/demo1$", output=Output)
async def demo1(params: Body[Input]) -> Output:
    output = Output(
        id_negative=-1 * params.id,
        name_upper=params.name.upper(),
    )
    return Response.json(output.model_dump())


@router.GET(r"/-/hello/(?P<name>.*)$")
async def hello(name: str):
    return Response.html(f"<h1>Hello, {name}!</h1>")


@hookimpl
def register_routes():
    return router.routes()

```