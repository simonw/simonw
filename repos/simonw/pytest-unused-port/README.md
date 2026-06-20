# pytest-unused-port

[![PyPI](https://img.shields.io/pypi/v/pytest-unused-port.svg)](https://pypi.org/project/pytest-unused-port/)
[![Tests](https://github.com/simonw/pytest-unused-port/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/pytest-unused-port/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/pytest-unused-port?include_prereleases&label=changelog)](https://github.com/simonw/pytest-unused-port/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/pytest-unused-port/blob/main/LICENSE)

pytest fixture finding an unused local port, built [using Claude Code](https://gistpreview.github.io/?9ffa45bc69a545427009ca6283e2e672)

## Installation

Install this library using `pip`:
```bash
pip install pytest-unused-port
```
Or with `uv`:
```bash
uv add pytest-unused-port
```
Or as a tool (to get the `uport` command):
```bash
uv tool install pytest-unused-port
```
## Usage

### Command-line Interface

You can use pytest-unused-port as a standalone tool to serve a directory on an unused port:

```bash
# Serve a specific directory
pytest-unused-port /tmp/blah

# Or use the shorter alias
uport /tmp/blah

# Or using uvx
uvx pytest-unused-port /tmp/blah

# Or as a Python module
python -m pytest_unused_port /tmp/blah

# Serve the current directory (default)
pytest-unused-port
uport
```

This will start Python's `http.server` serving the specified directory on an automatically-selected unused port. The server will print the URL and run until you press Ctrl+C.

### Pytest Fixtures

This pytest plugin provides a `unused_port` fixture that returns an available TCP port on localhost that your tests can use.

### Basic Example

```python
def test_my_server(unused_port):
    # unused_port is an integer containing an available port number
    server = start_my_server(port=unused_port)
    assert server.is_running()
```

### Starting an HTTP Server

```python
import http.server

def test_http_server(unused_port):
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(('127.0.0.1', unused_port), handler)
    # Now you can test your server on the unused port
    assert server.server_port == unused_port
```

### Using with Socket Programming

```python
import socket

def test_socket_server(unused_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', unused_port))
    sock.listen(1)
    # Your test code here
    sock.close()
```

The fixture automatically finds an available port by binding to port 0 (which tells the OS to assign any available port), getting the assigned port number, and then releasing it for your test to use.

### The `unused_port_server` fixture

For convenience, this plugin also provides an `unused_port_server` fixture that manages an HTTP server for you. This is especially useful for testing applications that need to fetch content from a local server.

#### Basic Example

```python
def test_fetch_from_server(unused_port_server, tmp_path):
    # Create a test file
    test_file = tmp_path / "index.html"
    test_file.write_text("<h1>Hello</h1>")

    # Start the server serving the directory
    unused_port_server.start(tmp_path)

    # Make requests to http://127.0.0.1:{unused_port_server.port}/
    # Server automatically stops at the end of the test
```

#### Features

- **Automatic cleanup**: The server automatically stops when the test ends
- **Explicit control**: Call `.stop()` to stop the server manually if needed
- **Port access**: Access the port number via `unused_port_server.port`
- **Method chaining**: `.start()` returns self for convenience

#### Example with explicit stop

```python
def test_server_lifecycle(unused_port_server, tmp_path):
    unused_port_server.start(tmp_path)

    # Do some testing...

    # Explicitly stop the server
    unused_port_server.stop()

    # Server is now stopped
```

#### Example fetching a file

```python
from urllib.request import urlopen

def test_fetch_file(unused_port_server, tmp_path):
    # Create a test file
    (tmp_path / "data.txt").write_text("test data")

    # Start server
    unused_port_server.start(tmp_path)

    # Fetch the file
    url = f"http://127.0.0.1:{unused_port_server.port}/data.txt"
    response = urlopen(url)
    assert response.read().decode() == "test data"
```

#### Using as a context manager

You can also use `StaticServer` directly as a context manager if you need more control:

```python
from pytest_unused_port import StaticServer

def test_with_context_manager(unused_port, tmp_path):
    with StaticServer(unused_port) as server:
        server.start(tmp_path)
        # Server runs here
        # ... your test code ...
    # Server automatically stops when exiting the context
```

The server runs `python -m http.server` in a subprocess, serving static files from the specified directory.

## Development

To contribute to this library, first checkout the code. Then install the dependencies using `uv`:
```bash
cd pytest-unused-port
uv pip install -e '.[test]'
```
To run the tests:
```bash
uv run pytest
```
