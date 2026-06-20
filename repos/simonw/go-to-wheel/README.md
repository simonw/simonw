# go-to-wheel

[![PyPI](https://img.shields.io/pypi/v/go-to-wheel.svg)](https://pypi.org/project/go-to-wheel/)
[![Changelog](https://img.shields.io/github/v/release/simonw/go-to-wheel?include_prereleases&label=changelog)](https://github.com/simonw/go-to-wheel/releases)
[![Tests](https://github.com/simonw/go-to-wheel/workflows/Test/badge.svg)](https://github.com/simonw/go-to-wheel/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/go-to-wheel/blob/main/LICENSE)

Compile Go CLI programs into Python wheels.

This tool takes a Go module directory, cross-compiles it for multiple platforms, and produces properly-tagged Python wheels that can be installed via `pip` or `pipx` to get the Go binary on your PATH.

See [Distributing Go binaries like sqlite-scanner through PyPI using go-to-wheel](https://simonwillison.net/2026/Feb/4/distributing-go-binaries/) for background on this project.

## Installation

```bash
pip install go-to-wheel
# or
pipx install go-to-wheel
```

Requires Go to be installed and available in your PATH.

## Quick start

Build wheels for all platforms from a Go module:

```bash
go-to-wheel path/to/go-module
```

This will create wheels in a `./dist` directory for Linux (glibc and musl), macOS (Intel and Apple Silicon), and Windows (amd64 and arm64).

## Usage

```bash
go-to-wheel path/to/go-folder [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--name NAME` | Python package name | Directory basename |
| `--version VERSION` | Package version | `0.1.0` |
| `--output-dir DIR` | Directory for built wheels | `./dist` |
| `--entry-point NAME` | CLI command name | Same as package name |
| `--platforms PLATFORMS` | Comma-separated list of targets | All supported platforms |
| `--go-binary PATH` | Path to Go binary | `go` |
| `--description TEXT` | Package description | `"Go binary packaged as Python wheel"` |
| `--license LICENSE` | License identifier | None |
| `--author AUTHOR` | Author name | None |
| `--author-email EMAIL` | Author email | None |
| `--url URL` | Project URL | None |
| `--requires-python VERSION` | Python version requirement | `>=3.10` |
| `--readme PATH` | Path to README markdown file for PyPI long description | None |
| `--set-version-var VAR` | Go variable to set to `--version` value via `-X` ldflag | None |
| `--ldflags FLAGS` | Additional Go linker flags (appended to default `-s -w`) | None |

### Examples

Build wheels with a custom package name:

```bash
go-to-wheel ./mytool --name my-python-tool
```

Build for specific platforms only:

```bash
go-to-wheel ./mytool --platforms linux-amd64,darwin-arm64
```

Embed the wheel version into the Go binary at compile time (requires a `var version` in your Go source):

```bash
go-to-wheel ./mytool --version 2.0.0 --set-version-var main.version
```

This passes `-X main.version=2.0.0` to the Go linker, so the compiled binary knows its own version without hardcoding it in the Go source. A typical Go pattern for this:

```go
var version = "dev"

func main() {
    if os.Args[1] == "--version" {
        fmt.Println(version) // prints "2.0.0" when built with --set-version-var
    }
}
```

Pass arbitrary Go linker flags with `--ldflags`:

```bash
go-to-wheel ./mytool --version 2.0.0 \
  --ldflags "-X main.version=2.0.0 -X main.commit=abc123"
```

The flags are appended to the default `-s -w`, so the full linker invocation becomes `-ldflags="-s -w -X main.version=2.0.0 -X main.commit=abc123"`.

Build with full metadata for PyPI:

```bash
go-to-wheel ./mytool \
  --name mytool-bin \
  --version 2.0.0 \
  --description "My awesome tool" \
  --license MIT \
  --author "Jane Doe" \
  --author-email "jane@example.com" \
  --url "https://github.com/jane/mytool" \
  --readme README.md
```

## Supported platforms

| Platform | Wheel Tag |
|----------|-----------|
| `linux-amd64` | `manylinux_2_17_x86_64` |
| `linux-arm64` | `manylinux_2_17_aarch64` |
| `linux-amd64-musl` | `musllinux_1_2_x86_64` |
| `linux-arm64-musl` | `musllinux_1_2_aarch64` |
| `darwin-amd64` | `macosx_10_9_x86_64` |
| `darwin-arm64` | `macosx_11_0_arm64` |
| `windows-amd64` | `win_amd64` |
| `windows-arm64` | `win_arm64` |

## How it works

1. Cross-compiles the Go binary using `GOOS` and `GOARCH` environment variables with `CGO_ENABLED=0` for static binaries
2. Creates a Python package with a thin wrapper that `exec`s the bundled binary
3. Packages everything into a wheel with the correct platform tag

The resulting wheel can be installed with pip:

```bash
pip install ./dist/mytool-1.0.0-py3-none-manylinux_2_17_x86_64.whl
```

Or tested directly with uv:

```bash
uv run --with ./dist/mytool-1.0.0-py3-none-manylinux_2_17_x86_64.whl mytool --help
```

## Development

Clone the repository:

```bash
git clone https://github.com/simonw/go-to-wheel
cd go-to-wheel
```

Run tests:

```bash
uv run pytest
```

## See also

- [maturin](https://github.com/PyO3/maturin) - The Rust equivalent that inspired this tool
- [pip-binary-factory](https://github.com/Bing-su/pip-binary-factory) - Template for packaging pre-built binaries
