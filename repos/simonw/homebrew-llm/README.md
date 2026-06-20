# homebrew-llm

Homebrew formulas for installing the [LLM](https://llm.datasette.io/) family of tools.

If you have previously installed packages from this repository you may need to run `brew update` to ensure you have the latest versions of the formulas:

```bash
brew update
```

## Installing llm

[LLM](https://llm.datasette.io/) lets you run prompts against large language models from the command-line.
```bash
brew install simonw/llm/llm
```
Example:
```bash
llm 'Ten great names for a pet pelican'
```
## Installing strip-tags

[strip-tags](https://github.com/simonw/strip-tags) strip tags from HTML, useful for feeding content to a large language model while keeping the token count down.
```bash
brew install simonw/llm/strip-tags
```
Example:
```bash
curl -s 'https://www.nytimes.com/' | strip-tags | llm --system 'Summarize headlines'
```
## Installing symbex

[symbex](https://github.com/simonw/symbex) is a tool for finding Python functions and classes within a codebase. It can also output just the signatures or docstrings of code that it finds.
```bash
brew install simonw/llm/symbex
```
Example - this finds the `def inspect_hash()` function and explains what it does:
```bash
symbex inspect_hash | llm --system 'explain this code'
```
## Installing ttok

[ttok](https://github.com/simonw/ttok) is a tool for counting tokens. This is useful if you want to check that your content is not going to exceed the size limits for different LLM models.
```bash
brew install simonw/llm/ttok
```
This installation will also bring in a copy of Rust, if one is not yet available in your Homebrew setup.

Example, counting the total number of tokens in all of your test functions.
```bash
symbex 'test_*' | ttok
```
