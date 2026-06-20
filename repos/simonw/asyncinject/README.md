# asyncinject

[![PyPI](https://img.shields.io/pypi/v/asyncinject.svg)](https://pypi.org/project/asyncinject/)
[![Changelog](https://img.shields.io/github/v/release/simonw/asyncinject?include_prereleases&label=changelog)](https://github.com/simonw/asyncinject/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/asyncinject/blob/main/LICENSE)

Run async workflows using pytest-fixtures-style dependency injection

## Installation

Install this library using `pip`:

    $ pip install asyncinject

## Usage

This library is inspired by [pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html).

The idea is to simplify executing parallel `asyncio` operations by allowing them to be defined using a collection of functions, where the function arguments represent dependent functions that need to be executed first.

The library can then create and execute a plan for executing the required functions in parallel in the most efficient sequence possible.

Here's an example, using the [httpx](https://www.python-httpx.org/) HTTP library.

```python
from asyncinject import Registry
import httpx


async def get(url):
    async with httpx.AsyncClient() as client:
        return (await client.get(url)).text

async def example():
    return await get("http://www.example.com/")

async def simonwillison():
    return await get("https://simonwillison.net/search/?tag=empty")

async def both(example, simonwillison):
    return example + "\n\n" + simonwillison

registry = Registry(example, simonwillison, both)
combined = await registry.resolve(both)
print(combined)
```
If you run this in `ipython` or `python -m asyncio` (to enable top-level await in the console) you will see output that combines HTML from both of those pages.

The HTTP requests to `www.example.com` and `simonwillison.net` will be performed in parallel.

The library notices that `both()` takes two arguments which are the names of other registered `async def` functions, and will construct an execution plan that executes those two functions in parallel, then passes their results to the `both()` method.

### Registry.from_dict()

Passing a list of functions to the `Registry` constructor will register each function under their introspected function name, using `fn.__name__`.

You can set explicit names instead using a dictionary:

```python
registry = Registry.from_dict({
    "example": example,
    "simonwillison": simonwillison,
    "both": both
})
```
Those string names will be used to match parameters, so each function will need to accept parameters named after the keys used in that dictionary.

### Registering additional functions

Functions that are registered can be regular functions or `async def` functions.

In addition to registering functions by passing them to the constructor, you can also add them to a registry using the `.register()` method:

```python
async def another():
    return "another"

registry.register(another)
```
To register them with a name other than the name of the function, pass the `name=` argument:
```python
async def another():
    return "another 2"

registry.register(another, name="another_2")
```

### Resolving an unregistered function

You don't need to register the final function that you pass to `.resolve()` - if you pass an unregistered function, the library will introspect the function's parameters and resolve them directly.

This works with both regular and async functions:

```python
async def one():
    return 1

async def two():
    return 2

registry = Registry(one, two)

# async def works here too:
def three(one, two):
    return one + two

print(await registry.resolve(three))
# Prints 3
```

### Parameters are passed through

Your dependent functions can require keyword arguments which have been passed to the `.resolve()` call:

```python
async def get_param_1(param1):
    return await get(param1)

async def get_param_2(param2):
    return await get(param2)

async def both(get_param_1, get_param_2):
    return get_param_1 + "\n\n" + get_param_2


combined = await Registry(get_param_1, get_param_2, both).resolve(
    both,
    param1 = "http://www.example.com/",
    param2 = "https://simonwillison.net/search/?tag=empty"
)
print(combined)
```
### Parameters with default values are ignored

You can opt a parameter out of the dependency injection mechanism by assigning it a default value:

```python
async def go(calc1, x=5):
    return calc1 + x

async def calc1():
    return 5

print(await Registry(calc1, go).resolve(go))
# Prints 10
```

### Tracking with a timer

You can pass a `timer=` callable to the `Registry` constructor to gather timing information about executed tasks..  Your function should take three positional arguments:

- `name` - the name of the function that is being timed
- `start` - the time that it started executing, using `time.perf_counter()` ([perf_counter() docs](https://docs.python.org/3/library/time.html#time.perf_counter))
- `end` - the time that it finished executing

You can use `print` here too:

```python
combined = await Registry(
    get_param_1, get_param_2, both, timer=print
).resolve(
    both,
    param1 = "http://www.example.com/",
    param2 = "https://simonwillison.net/search/?tag=empty"
)
```
This will output:
```
get_param_1 436633.584580685 436633.797921747
get_param_2 436633.641832699 436634.196364347
both 436634.196570217 436634.196575639
```
### Turning off parallel execution

By default, functions that can run in parallel according to the execution plan will run in parallel using `asyncio.gather()`.

You can disable this parallel exection by passing `parallel=False` to the `Registry` constructor, or by setting `registry.parallel = False` after the registry object has been created.

This is mainly useful for benchmarking the difference between parallel and serial execution for your project.

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd asyncinject
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
