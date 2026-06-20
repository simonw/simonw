# scan-for-secrets

[![PyPI](https://img.shields.io/pypi/v/scan-for-secrets.svg)](https://pypi.org/project/scan-for-secrets/)
[![Changelog](https://img.shields.io/github/v/release/simonw/scan-for-secrets?include_prereleases&label=changelog)](https://github.com/simonw/scan-for-secrets/releases)
[![Tests](https://github.com/simonw/scan-for-secrets/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/scan-for-secrets/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/scan-for-secrets/blob/master/LICENSE)

Scan for secrets in files you plan to share

## Installation

Install this tool using `pip`:
```bash
pip install scan-for-secrets
```
Or `uv`:
```bash
uv tool install scan-for-secrets
```
Or use without installing via `uvx`:
```bash
uvx scan-for-secrets --help
```

## Usage

This tool helps scan all of the text files in a directory (ignoring binary files) to see if they include specified secret strings. For example, run this if you want to publish the logs from a coding agent session after first confirming no secrets from environment variables are exposed in those logs.

Basic usage looks like this:
```bash
scan-for-secrets $OPENAI_API_KEY $ANTHROPIC_API_KEY
```
This will scan text files in the current folder and all sub-folders looking for the values that were passed as positional arguments, including common escaping schemes that might mean a direct string match misses them.

To scan for a secret that can be accessed using another command, use `$(command)` syntax:
```bash
scan-for-secrets "$(llm keys get openai)"
```
Add `-d/--directory` to specify a different directory to scan. This can be passed multiple times:
```bash
scan-for-secrets $OPENAI_API_KEY -d ~/my-project
scan-for-secrets $OPENAI_API_KEY -d ~/project-a -d ~/project-b
```
Use `-f/--file` to scan specific files instead of (or in addition to) directories. This can also be passed multiple times. Missing files are silently ignored.
```bash
scan-for-secrets $OPENAI_API_KEY -f output.log -f debug.json
scan-for-secrets $OPENAI_API_KEY -d ~/project -f ~/extra-log.txt
```
If neither `-d` nor `-f` is provided, the current directory is scanned.

You can also pipe a list of newline-separated secrets to the tool:
```bash
cat secrets.txt | scan-for-secrets
```
This can be combined with secrets passed as positional arguments.

Add `-v/--verbose` to see which directories are being scanned (output goes to stderr). In verbose mode, any matches found are repeated at the end of the output so they aren't lost in the directory listing:
```bash
scan-for-secrets $OPENAI_API_KEY -v
```

### Redacting secrets

Use `-r/--redact` to replace found secrets with `REDACTED` directly in the scanned files. The tool will show all matches first, then ask for confirmation before rewriting anything:
```bash
scan-for-secrets $OPENAI_API_KEY -r
```
Example interaction:
```
logs/2024-03-15.jsonl:42: sk-a... (literal)
logs/2024-03-15.jsonl:108: sk-a... (json)

Replace 2 occurrences in 1 file with REDACTED?
Proceed? [y/N]: y
Replaced 2 occurrences.
```
All escaped variants of the secret (JSON, URL-encoded, etc.) are replaced as well. If no secrets are found, no prompt is shown. If you decline the prompt, the tool exits with code 1 (same as finding secrets without `--redact`).

Note: when using `--redact`, secrets cannot be piped via stdin since stdin is reserved for the confirmation prompt. Pass secrets as arguments or use a config file instead.

## Output

If no secrets are found, the tool will terminate with an exit code 0 and output nothing. If secrets are found it will return an exit code 1 and list the files, line numbers and the first few characters of each secret that was spotted.

Example output:

```
logs/2024-03-15.jsonl:42: sk-a... (literal)
logs/2024-03-15.jsonl:108: sk-a... (json)
config/debug.html:7: ghp_... (html)
```

## Configuration file

If you run `scan-for-secrets` without any extra arguments or piped data the command will look for a default configuration file to tell it what to scan for instead.

This file lives at `~/.scan-for-secrets.conf.sh` and contains commands that will be executed to retrieve secrets. Each line should be a shell command that outputs a single secret to stdout (or a blank line or a comment).

```bash
# API keys
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# AWS (using xargs to strip whitespace)
awk -F= '/aws_secret_access_key/{print $2}' ~/.aws/credentials | xargs

# 1Password
op read "op://Vault/API Key/password"

# LLM keys
llm keys get gemini
```

Blank lines and lines starting with `#` are ignored. By default the file is executed with `sh`. Add a shebang line (e.g. `#!/bin/bash` or `#!/usr/bin/env python3`) to use a different interpreter.

With a configuration file setup you can run `scan-for-secrets` like this:

```bash
cd agent-logs/
scan-for-secrets
```
Or this:
```bash
scan-for-secrets -d agent-logs
```
You can also pass a path to a configuration file using the `-c/--config` option:

```bash
scan-for-secrets -c scan.sh
```
Unlike the default configuration behavior, this `-c` option will be combined with any piped data or additional positional arguments.

## Using this as a Python library

This package can also be used as a Python library. Add `scan-for-secrets` as a dependency and use it like this:

```python
from scan_for_secrets import scan_directory

result = scan_directory("./logs", ["sk-abc123...", "ghp_secret..."])

if result.has_secrets:
    for match in result.matches:
        print(f"{match.file_path}:{match.line_number}: {match.secret_hint} ({match.encoding})")
```

### API reference

#### `scan_directory(directory: str | Path, secrets: list[str]) -> ScanResult`

Recursively scans all text files in `directory` for the given `secrets`, checking both literal matches and common escaped variants (JSON, URL percent-encoding, HTML entities, backslash-doubled and Unicode escapes). Returns a `ScanResult` with all matches collected.

- **`directory`**: Root directory to scan. Can be a string path or a `pathlib.Path`.
- **`secrets`**: List of secret strings to search for. Empty strings are ignored.

Binary files (detected by null bytes in the first 8192 bytes) are skipped. The following directories are also skipped: `.git`, `.hg`, `.svn`, `node_modules`, `__pycache__`, `.venv`, `venv`.

#### `scan_directory_iter(directory, secrets, on_enter_directory=None) -> Iterator[Match]`

```python
def scan_directory_iter(
    directory: str | Path,
    secrets: list[str],
    on_enter_directory: Callable[[str], None] | None = None,
) -> Iterator[Match]:
```

Streaming version of `scan_directory` — yields `Match` objects as they are found instead of collecting them. Useful for large directory trees where you want to display results immediately.

The optional `on_enter_directory` callback is called with the relative path of each directory as it is entered.

```python
from scan_for_secrets import scan_directory_iter

for match in scan_directory_iter("./logs", ["sk-abc123...", "ghp_secret..."]):
    print(f"{match.file_path}:{match.line_number}: {match.secret_hint} ({match.encoding})")
```

#### `scan_file(file_path: str | Path, secrets: list[str]) -> ScanResult`

Scan a single file for secrets. Returns a `ScanResult` with `files_scanned` always set to 1. The `file_path` field on each match will be the file's basename.

```python
from scan_for_secrets import scan_file

result = scan_file("/path/to/output.log", ["sk-abc123..."])
if result.has_secrets:
    for match in result.matches:
        print(f"{match.file_path}:{match.line_number}: {match.secret_hint}")
```

#### `redact_file(file_path: str | Path, secrets: list[str], replacement: str = "REDACTED") -> int`

Replace all occurrences of the given secrets (including escaped variants) in a single file. Returns the number of replacements made. The file is only rewritten if at least one replacement occurs.

```python
from scan_for_secrets import redact_file

count = redact_file("/path/to/output.log", ["sk-abc123..."])
print(f"Replaced {count} occurrences")
```

#### `scan_file_iter(file_path: str | Path, secrets: list[str]) -> Iterator[Match]`

Streaming version of `scan_file` — yields `Match` objects as they are found. The `file_path` field on each match will be the file's basename.

```python
from scan_for_secrets import scan_file_iter

for match in scan_file_iter("/path/to/output.log", ["sk-abc123..."]):
    print(f"{match.file_path}:{match.line_number}: {match.secret_hint} ({match.encoding})")
```

#### `ScanResult`

```python
@dataclass
class ScanResult:
    matches: list[Match]  # All matches found across all files
    files_scanned: int    # Number of text files checked

    @property
    def has_secrets(self) -> bool:
        """True if any matches were found."""
```

#### `Match`

```python
@dataclass
class Match:
    file_path: str     # Path relative to the scanned directory
    line_number: int   # 1-based line number where the match was found
    secret_hint: str   # First 4 characters of the original secret + "..."
    encoding: str      # How the secret was encoded: "literal", "json", "url",
                       # "html", "backslash-doubled", or "unicode-escape"
```

## Escaping schemes

In addition to literal string matching, `scan-for-secrets` checks for these escaped forms of each secret:

- **JSON** (`json`) — Characters are escaped as they would appear inside a JSON string: `\"`, `\\`, `\/`, `\n`, `\t`, and `\uXXXX` for non-ASCII characters. Catches secrets embedded in JSON files, API responses, and log output from JSON-based tools.
- **URL percent-encoding** (`url`) — Every non-alphanumeric character is replaced with `%XX` hex encoding (e.g. `=` becomes `%3D`, `&` becomes `%26`). Catches secrets in URLs, query strings, and form data.
- **HTML entities** (`html`) — `&` `<` `>` `"` are replaced with named entities (`&amp;`, `&lt;`, `&gt;`, `&quot;`), and non-ASCII characters become numeric references like `&#xC3;`. Catches secrets embedded in HTML pages and XML documents.
- **Backslash-doubled** (`backslash-doubled`) — Every `\` is replaced with `\\`. Catches secrets in configuration files, YAML, TOML, and other formats that escape backslashes.
- **Unicode escape** (`unicode-escape`) — Non-ASCII characters are replaced with Python-style escape sequences like `\xe9` or `\u00e9`. Catches secrets in source code and debug output.

If an encoding produces the same string as the literal secret (for example, URL-encoding a plain alphanumeric string), that redundant variant is skipped.

## Development

To contribute to this tool, first checkout the code. Then run the tests:
```bash
cd scan-for-secrets
uv run pytest
```
To run the development version of the command itself:
```bash
uv run scan-for-secrets --help
```
