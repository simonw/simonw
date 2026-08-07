# Moonlight & Mayhem

A tiny, mobile-friendly 3D raccoon heist for the browser. Free the crew, dodge the museum's cameras and BroomBot, steal the suspiciously enormous Golden Sardine, and make it back to the getaway dumpster.

## Run locally

Serve the repository as static files and open `index.html` through HTTP. For example:

```bash
uv run python -m http.server 8000
```

Then visit <http://localhost:8000>.

## Controls

- Desktop: WASD or arrow keys to move, E to interact, Space or Shift to dash, Escape to pause.
- Mobile: left touch stick to move, paw button to interact, lightning button to dash.

No build step is required. Three.js is vendored locally, and the gpt-image-2 material textures are committed with the game.
