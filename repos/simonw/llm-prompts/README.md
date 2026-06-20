# llm-prompts

A collection of prompts for use with the LLM CLI tool

Relevant:

- [LLM documentation](https://llm.datasette.io/)
- [llm, ttok and strip-tags—CLI tools for working with ChatGPT and other LLMs](https://simonwillison.net/2023/May/18/cli-tools-for-llms/)
- [symbex: search Python code for functions and classes, then pipe them into a LLM](https://simonwillison.net/2023/Jun/18/symbex/)

Many of these are "system prompts" - where content is piped to the tool along with a `--system prompt` that tells the tool how it should process that data.

## Using symbex

[symbex](https://github.com/simonw/symbex) is a CLI tool for searching for and outputting subsets of Python code based on search criteria. The tool is designed to help extract content for passing to `llm`.

## Features derived from tests

> Detailed bullet point list of features of this software

Running this in a fresh checkout of [simonw/symbex](https://github.com/simonw/symbex) with `3.5-16k` - the 3.5 turbo model with a 16,000 token context:

```bash
symbex 'test_*' | llm --system 'Detailed bullet point list of features of this software' -m 3.5-16k
```
Output:

> Features of this software include:
> 
> 1. Testing of command-line interface to ensure it shows help when no arguments are provided.
> 2. Testing of command-line interface to ensure it returns the expected output for different argument combinations.
> 3. Testing of command-line interface to ensure it shows errors when necessary.
> 4. Testing of reading a file with a specific encoding to ensure correct text is read.
> 5. Testing of formatting quoted strings to ensure they are properly escaped and formatted.
> 6. Testing of symbol extraction to ensure correct symbols are identified from the given code.
> 7. Testing of method symbols to ensure correct methods are identified from the given code.
> 8. Testing of retrieving symbols with documented and undocumented filters to ensure correct symbols are returned.
> 9. Testing of filtering symbols based on various options such as function, class, async, typed, untyped, partially-typed, fully-typed, documented, and undocumented.
> 10. Testing of counting the number of symbols returned by the filters.

The "Testing of" bits there indicate it didn't fully understand the idea of describing the software, not the tests.

GPT-4 handled this much better:

```bash
symbex 'test_*' | llm --system 'Detailed bullet point list of features of this software' -m 4
```
> - Search for symbols (functions, classes, etc.) in a given codebase
> - Show detailed information on the selected symbol (e.g. function signature)
> - Filter symbols based on various criteria such as:
>   - Function
>   - Class
>   - Async
>   - Typed
>   - Partially typed
>   - Fully typed
>   - Documented
>   - Undocumented
> - Support file and directory filtering
> - Handle different Python versions and file encodings
> - Include tests for functionality and CLI behavior
> - Quoted string support for single and multiline strings
> - Count the number of matching symbols
> - CLI Runner to execute command line interface tests
> - Parametrized testing for multiple input-output combinations
> - Display line numbers for symbol, classes, methods, etc.

