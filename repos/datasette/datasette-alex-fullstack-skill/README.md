# `datasette-alex-fullstack-skill`

This is a skill that contains an opinionated approach in buiding "full-stack" Datasette plugins.

I create a lot of Datasette plugins. Some are pure Python, some are pure-frontend. Some are "full-stack", meaning they have complex frontend code (typically Svelte or Preact) that call custom the "backend" via custom Datasette routes.

After much trial and error, I've come up with a comprehensive approach to build these plugins. In short, they involve:

- Svelte and TypeScript via [`datasette-vite`](https://github.com/datasette/datasette-vite)
- Generated type sharing with Pydantic, [`openapi-fetch`](https://www.npmjs.com/package/openapi-fetch), and [`datasette-plugin-router`](https://github.com/datasette/datasette-plugin-router)
- Various `Justfile` recipes and targets


I got tired of explaing this over and over again to various agents, so I've consoldiated it all to this one "skill". Feel free to use as you wish!