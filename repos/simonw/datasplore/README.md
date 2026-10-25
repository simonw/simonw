# Datasplore

Walk through a SQLite database in first person.

**Try it:** open `index.html?url=https://datasette.io/content.db`

Pass `?url=` pointing at any SQLite file served with CORS headers (`Access-Control-Allow-Origin`). The whole file is downloaded and opened in the browser with [sql.js](https://sql.js.org/), then rendered with [three.js](https://threejs.org/). You can also open or drag-and-drop a local `.db` file.

## The world

- **The lobby** is a ring of glowing portals, one per table. Foreign keys between tables are drawn as arcs of light overhead, with data packets flowing from the referencing table to the referenced one.
- **A table hall** is a corridor lined with row cards, 20 rows per page, with the table schema on the wall by the entrance and a portal to the next page at the far end.
- **A row room** shows the full record on the front wall. Doorways on the left follow this row's foreign keys to the rows they point at. Doorways on the right lead to the rows that point back at this one: straight to the row if there's only one, or to a filtered hall if there are several. Rows with an image URL (like GitHub avatars) show the picture.

Your location is kept in the URL hash, so you can share a link to a specific row, and the browser back button works.

## Controls

| | |
|---|---|
| `W` `A` `S` `D` / arrows | move (left/right arrows turn) |
| mouse | look around (click to capture the pointer) |
| `shift` | run |
| `space` | jump |
| click / `E` | open the row card or portal you're pointing at, or inspect a record in full |
| walk into a portal | travel through it |
| `backspace` | go back |
| `H` | return to the lobby |
| `M` | toggle sound |

On touch devices there's a joystick in the bottom-left corner, drag anywhere else to look, and tap things to open them.

## Development

`index.html` is the entire app — no build step. Libraries load from CDNs (three.js via an import map, sql.js via a script tag). Serve the directory with any static server, e.g. `python3 -m http.server`.
