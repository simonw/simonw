# datasette-agent-frontend

Experimential Svelte/TypeScript frontend for [datasette-agent](https://github.com/datasette/datasette-agent).
Overrides the `agent_index.html` and `agent_conversation.html` templates to mount Svelte
apps built with Vite, using [datasette-vite](https://github.com/datasette/datasette-vite)
for HMR-friendly development.

Totally an experiment, may merge a version of this directly into `datasette-agent`. 

## Setup

```
just frontend-install
just frontend          # build into datasette_agent_frontend/static + manifest.json
just dev               # datasette at http://localhost:5171
```

For HMR (two terminals):

```
just frontend-dev      # vite on :5180
just dev-with-hmr      # datasette pointed at the vite dev server
```
