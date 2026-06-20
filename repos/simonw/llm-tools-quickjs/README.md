# llm-tools-quickjs

[![PyPI](https://img.shields.io/pypi/v/llm-tools-quickjs.svg)](https://pypi.org/project/llm-tools-quickjs/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-tools-quickjs?include_prereleases&label=changelog)](https://github.com/simonw/llm-tools-quickjs/releases)
[![Tests](https://github.com/simonw/llm-tools-quickjs/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-tools-quickjs/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-quickjs/blob/main/LICENSE)

JavaScript execution as a tool for LLM

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-quickjs
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm --tool QuickJS "Calculate 123 * 98742" --tools-debug
```

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_quickjs import QuickJS

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "Calculate 123 * 98742",
    tools=[QuickJS()]
).text()
print(result)
```
The `QuickJS()` instance maintains interpreter state between calls, so this kind of thing works:
```python
quickjs = QuickJS()
conversation = model.conversation(tools=[quickjs])
print(conversation.chain("set a to 'rabbit'").text())
print(conversation.chain("calculate length of a times 50").text())
print(quickjs._get_context().eval("a"))
# Outputs 'rabbit'
```

Something a bit more fun:

```bash
llm -T QuickJS 'Draw a 40 character wide mandelbrot with JavaScript' --td
```
I tried this and got:

`Tool call: QuickJS_execute_javascript({'javascript': "function mandelbrot(width, height, max_iter) {\n  let result = '';\n  for (let y = 0; y < height; y++) {\n    for (let x = 0; x < width; x++) {\n      let cx = (x / width) * 3.5 - 2.5;\n      let cy = (y / height) * 2 - 1;\n      let zx = 0, zy = 0, iter = 0;\n      while (zx * zx + zy * zy < 4 && iter < max_iter) {\n        let xtemp = zx * zx - zy * zy + cx;\n        zy = 2 * zx * zy + cy;\n        zx = xtemp;\n        iter++;\n      }\n      if (iter === max_iter) {\n        result += '#';\n      } else {\n        result += ' ';\n      }\n    }\n    result += '\\n';\n  }\n  return result;\n}\n\nmandelbrot(40, 20, 100);"})`
````                                        
Here is a 40 character wide Mandelbrot set visualization in text form using JavaScript:

```
                                        
                                        
                           ##           
                          ###           
                       # ######         
                       ##########       
                      ###########       
                     ############       
                #### #############      
               ##### ############       
      ##########################        
               ##### ############       
                #### #############      
                     ############       
                      ###########       
                       ##########       
                       # ######         
                          ###           
                           ##           
                                        
```

If you'd like, I can provide the JavaScript code used to generate this.
````

## Function alternative

The `QuickJS` tool is a Toolbox - it persists state in between calls.

This plugin also provides a function variant with no persisted state. That can be used like this:

```python
llm -T quickjs 'Calculate 123 * 98742' --td
```

Or in Python like this:
```python
import llm
from llm_tools_quickjs import quickjs

model = llm.get_model("gpt-4.1-mini")

chain = model.chain(
    "Draw a 40 character wide mandelbrot with JavaScript",
    tools=[quickjs]
)
print(chain.text())
```
Some models [that have trouble](https://github.com/simonw/llm/issues/1105) with class-based tools may work better with the function variant.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-quickjs
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
