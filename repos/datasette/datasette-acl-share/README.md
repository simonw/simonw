# datasette-acl-share

A reusable, Google-Docs-style **share dialog** for Datasette, shipped as a
framework-agnostic Svelte 5 custom element: `<datasette-acl-share-dialog>`.

One component, embedded by every document plugin (paper, places, sheets, …). It
is the UI layer over the [datasette-acl](https://github.com/datasette/datasette-acl)
JSON API — grants, roles, groups, and "general access" audiences. If
datasette-user-profiles is installed the dialog adds people search and avatars;
without it, it degrades gracefully to initials chips with no People search.

<p align="center"><img src="docs/screenshots/groups.png" alt="The share dialog open on a document, showing a person and two groups with role dropdowns and a General access control" width="560"></p>

## Usage

Drop the tag anywhere — inside a Svelte/Preact app, or in plain server-rendered
HTML (custom elements are just DOM):

```html
<datasette-acl-share-dialog
  resource-type="paper-doc"
  parent="mydb"
  child="42"
  resource-label="Q2 Planning"
></datasette-acl-share-dialog>
```

The element renders a compact **share-icon button**; clicking it opens a modal
`<dialog>` (dismiss with the × button, the backdrop, or `Esc`). The resource is
fetched lazily on first open, so a page can carry many share buttons cheaply.

Once open, the dialog shows "people with access" (avatars, role dropdowns,
remove buttons) and a "General access" section. The **last row of the roster is
an inline add-row**: one unified box searches people (profiles) *and* groups
(acl) together, stages your picks as pills, then a role dropdown + **Add**
confirm them — all in place, no separate add panel. Each action is its own fetch
— grant / update / revoke — matching Google Docs' incremental behaviour. Actors
who cannot manage the resource (`can_manage: false`) get a read-only roster:
roles as tags, no add-row, no remove buttons.

**General access** lists each public audience as its own row with its own role
and a remove button — so a resource can be, say, Editor for *Anyone signed in*
and Viewer for *Anyone signed out* at once. Its add-row offers the two
non-overlapping audiences (`authenticated`, `anonymous`); adding one takes an
explicit confirm (exposing a resource publicly is the one risky action), while
role changes and removes apply instantly. A pre-existing `everyone` ("Anyone")
grant still renders as a removable row.

<table>
<tr>
<td width="50%"><img src="docs/screenshots/search-unified.png" alt="The inline add-row's search open, results split into People and Groups sub-sections"></td>
<td width="50%"><img src="docs/screenshots/people-selected.png" alt="A searched person staged as a removable pill inside the add-row, with a role dropdown and Add button, before confirming"></td>
</tr>
<tr>
<td align="center"><em>One search, people <strong>and</strong> groups together</em></td>
<td align="center"><em>Picks staged inline with a role, before hitting Add</em></td>
</tr>
<tr>
<td width="50%"><img src="docs/screenshots/public.png" alt="The General access section with an 'Anyone' row at Viewer plus a remove button, and an add-row offering 'Anyone signed in' with a role and Add button"></td>
<td width="50%"></td>
</tr>
<tr>
<td align="center"><em>General access: a row per public audience, each with its own role</em></td>
<td align="center"></td>
</tr>
</table>

### Attributes

| Attribute | Req | Purpose |
|---|---|---|
| `resource-type` | yes | acl resource type, e.g. `paper-doc`, `places-list`, `sheets-workbook` |
| `parent` | yes | resource identity part 1 (e.g. database name) |
| `child` | – | resource identity part 2 (e.g. row id); omit for parent-only resources |
| `resource-label` | – | display title shown in the dialog header |
| `actor-json` | – | current actor as JSON (`{"id":"alice","kind":"user"}`) — used to mark "(you)" |
| `features` | – | comma list of sections to show (`people,groups,public`); empty/missing = all available |
| `api-base` | – | override the acl API prefix (default `/-/acl/api`) |
| `open` | – | when set (any value other than `false`), open the modal on mount instead of waiting for a trigger click |
| `trigger-label` | – | text shown next to the share icon on the trigger button (icon-only if omitted) |
| `disabled` | – | when set (any value other than `false`), disable the trigger so the dialog can't open (e.g. the actor can't share this resource) |

### Events

The element dispatches bubbling, composed `CustomEvent`s so hosts can react
(e.g. paper re-running its SSE subscriber sweep after a revoke):

| Event | `detail` |
|---|---|
| `share-granted` | `{principal, id, role}` |
| `share-updated` | `{principal, id, role}` |
| `share-revoked` | `{principal, id}` |
| `share-changed` | `{}` — fired after any mutation (coarse) |

`principal` is `"actor"`, `"group"`, or `"public"`; `id` is the actor id, group
id, or a general-access audience name (`everyone` / `authenticated`).

## Including the bundle (opt-in)

The bundle is built with and served via
[datasette-vite](https://github.com/datasette/datasette-vite). It is **not**
injected site-wide — a host plugin opts in from its own asset hooks so the
dialog only loads on pages that use it:

```python
from datasette import hookimpl
from datasette_acl_share import datasette_share_assets

@hookimpl
def extra_js_urls(datasette, request):
    # gate on your own page(s) so it doesn't load everywhere
    if not _is_my_page(request):
        return []
    return datasette_share_assets(datasette)["js"]

@hookimpl
def extra_css_urls(datasette, request):
    if not _is_my_page(request):
        return []
    return datasette_share_assets(datasette)["css"]
```

The helper returns `{"js": [{"url": …, "module": True}], "css": [url, …]}`,
ready for Datasette's `extra_js_urls` / `extra_css_urls` hooks. In
datasette-vite dev mode the `js` list includes the Vite client (HMR) and `css`
is empty — your plugin code is identical in dev and prod. Hosts that own their
own Vite build can instead splice the URLs into their page template.

## Capability probe

So a host can set `features` without guessing which optional backends exist:

```
GET /-/share/capabilities  →  {"people": true, "groups": true, "public": true}
```

`people` reflects whether
[datasette-user-profiles](https://github.com/datasette/datasette-user-profiles)
is installed (search + avatars); `groups` and `public` are intrinsic to
datasette-acl. `share_capabilities()` is also importable if you prefer to
compute the `features` string server-side.

## Embedding in apps

A Svelte app (paper, places, sheets) renders the tag directly — attributes
bind, and `onshare-*` props receive the events:

```svelte
<datasette-acl-share-dialog
  resource-type="paper-doc"
  parent={dbName}
  child={docId}
  resource-label={docTitle}
  actor-json={JSON.stringify(actor)}
  onshare-revoked={onShareRevoked}
></datasette-acl-share-dialog>
```

Preact hosts (datasette-comments) and plain Jinja pages embed the same tag
unchanged, wiring events with `addEventListener`.

> For a full walkthrough — modelling the acl resource type / actions / roles,
> seeding grants, gating pages, plus web-component tips and a minimal end-to-end
> plugin — see [`docs/integration-guide.md`](docs/integration-guide.md).

## Development

```sh
just frontend-install   # one-time npm install
just frontend           # production build (writes static/gen + manifest.json)
just dev                # datasette + the sample-resources demo at :5171

# Or with Vite HMR:
just frontend-dev       # terminal 1: vite dev server (port 5180)
just dev-with-hmr       # terminal 2: datasette pointed at the dev server
```

`just dev` loads a throwaway demo plugin (`tests/sample_plugins`, with templates
in `tests/templates`) plus datasette-debug-gotham / datasette-user-profiles /
datasette-debug-bar. Visit <http://localhost:5171/sample-resources>, switch
characters with the debug bar (start as Clark — he manages one of every type),
and exercise the dialog — see `CLAUDE.md` for the full demo walkthrough.

Built assets (`datasette_acl_share/static/`, `manifest.json`) are gitignored and
produced by the build.

### Tests

```sh
npm --prefix frontend run test    # vitest (node + browser suites)
npm --prefix frontend run check   # svelte-check + tsc
uv run pytest                     # Python: asset helper + capability probe
```
