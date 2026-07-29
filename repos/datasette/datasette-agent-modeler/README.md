# datasette-agent-modeler

[![PyPI](https://img.shields.io/pypi/v/datasette-agent-modeler.svg)](https://pypi.org/project/datasette-agent-modeler/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-agent-modeler?include_prereleases&label=changelog)](https://github.com/datasette/datasette-agent-modeler/releases)
[![Tests](https://github.com/datasette/datasette-agent-modeler/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-agent-modeler/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-agent-modeler/blob/main/LICENSE)

3D modelling tools for Datasette Agent - create and edit 3D models from chat

## Screenshot

![A Datasette Agent chat session - user has prompted "put the cat in the pot" - result is a 3D rendered cat sitting in a pot in a panel that allows for rotation of the model.](https://raw.githubusercontent.com/datasette/datasette-agent-modeler/refs/heads/main/cat-in-a-pot.webp)

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-agent-modeler
```
## Usage

This plugin adds 3D modelling tools to [Datasette Agent](https://github.com/datasette/datasette-agent). Ask the agent to build something - "make me a 3D model of a rocket ship" - and it will assemble one from primitive shapes and display it inline in the chat in an interactive viewer (drag to orbit, scroll to zoom, right-drag to pan). Then ask for changes - "make the fins purple and twice as tall" - and the agent edits the stored model and shows the updated result.

Four tools are registered with the agent:

- `create_model(name, objects, background?)` - creates a model from a list of primitive shapes (`box`, `sphere`, `cylinder`, `cone`, `torus`, `capsule`, `plane`), each with optional `position`, `rotation` (degrees), `scale`, `color` and `opacity`. Returns a `model_id`.
- `edit_model(model_id, operations)` - applies an ordered list of edit operations atomically: `add_object`, `update_object` (changed fields only - params are merged), `remove_object`, `set_name`, `set_background`.
- `get_model(model_id)` - returns the current JSON document and revision number.
- `list_models()` - lists stored models.

Models are stored in Datasette's internal database. Every edit saves a full snapshot as a new revision, and each viewer embedded in the chat transcript shows the model as it was at that revision, so the conversation doubles as a visual edit history.

The viewer is a `<datasette-model-3d>` custom element that renders with [three.js](https://threejs.org/) (loaded from esm.sh), so browsing models requires internet access from the browser.

### Permissions

The plugin registers a `datasette-agent-modeler` permission which gates all four tools - actors without it never see them. The `--root` user holds it by default:

```bash
datasette mydata.db --internal internal.db --root
```

See [DESIGN.md](DESIGN.md) for the full design notes, including the model document format and the 3D library research.

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-agent-modeler
# Confirm the plugin is visible
uv run datasette plugins
```
To run the tests:
```bash
uv run pytest
```
