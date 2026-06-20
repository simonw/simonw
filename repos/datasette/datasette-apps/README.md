# datasette-apps

[![PyPI](https://img.shields.io/pypi/v/datasette-apps.svg)](https://pypi.org/project/datasette-apps/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-apps?include_prereleases&label=changelog)](https://github.com/datasette/datasette-apps/releases)
[![Tests](https://github.com/datasette/datasette-apps/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-apps/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-apps/blob/main/LICENSE)

Create apps that live inside Datasette

## Installation

Install this plugin in the same environment as Datasette.

Read [Host applications inside Datasette with Datasette Apps](https://datasette.io/blog/2026/datasette-apps/) for more on this project.
```bash
datasette install datasette-apps
```
## Usage

This plugin introduces a new interface at `/-/apps` for browsing and searching available apps.

There are two types of app:

- HTML and JavaScript apps managed by this plugin, which run in a sandbox that limits them to approved Datasette data access and blocks communication with external sites unless those hosts have been explicitly allowed.
- Apps provided by other plugins that are written in Python and HTML/JavaScript which are unrestricted but can do more things

This plugin allows you to create and modify HTML apps, and provides a plugin hook to enable other plugins to add their own Python apps to the system.

- `/-/apps` lets you browse available apps
- `/-/apps/ULID` to interact with a full screen HTML app
- `/-/apps/create` for creating a new app
- `/-/apps/ULID/edit` to edit an existing app

Signed-in users get an "Apps" link in Datasette's top-right menu.

HTML apps managed by this plugin use lowercase monotonic ULIDs as their IDs and track every edit as a new row in `app_revisions`.

### Sandboxed apps

Stored apps are rendered inside a sandboxed iframe. The plugin injects a Content Security Policy into the iframe `srcdoc`.

Direct network access is blocked unless the app has exact `https://` origins configured. Those same origins are allowed for remote images, external script tags, and external stylesheet links/style elements. Localhost origins are never allowed. Local file previews using `data:` and `blob:` image URLs are allowed.

Configuring those origins on an app is restricted, because an origin can be used to leak private data out of the app. Users with the `apps-set-csp` permission can set any valid `https://` origin using a free-form field on the create and edit pages. Other users can only pick from the allow-list configured by the `allowed_csp_origins` plugin setting, if one exists - otherwise they cannot configure network access at all. When editing an app that already has origins outside that allow-list - for example origins added earlier by a privileged user - those existing origins can be kept or removed but new arbitrary origins cannot be added.

To configure the allow-list:

```yaml
plugins:
  datasette-apps:
    allowed_csp_origins:
    - https://cdn.jsdelivr.net
    - cdnjs.cloudflare.com
```

Entries without a scheme are treated as `https://` origins.

The iframe bridge reports JavaScript errors, unhandled promise rejections, CSP violations, failed resources, fetch failures, `console.error()` calls, and failed Datasette data queries back to the parent page. The app page shows these in a small expandable error panel above the iframe. It also captures `console.log()` messages and Datasette data helper calls in a collapsed log panel below the iframe.

The bridge also replaces `history.replaceState()`, `history.pushState()`, `history.back()`, `history.forward()`, and `history.go()` with no-op functions inside the sandboxed iframe, avoiding browser errors from apps that try to manage URL state.

### Data access

Stored apps can query Datasette data using the injected `datasette.query(database, sql, params)` helper.

They can also run allow-listed stored queries using `datasette.storedQuery(database, query, params)`. The iframe sends those requests to the parent page with `postMessage`, and the parent page forwards them to an app-scoped query endpoint.

Apps have allow-lists configured on the edit page. If the requested database or stored query is allowed, the request is forwarded to Datasette's own JSON APIs using the current actor, so Datasette's normal SQL and query permissions still apply.

Failed stored-query attempts, including attempts to call a query that is not allow-listed or that the current actor cannot run, are reported in the app page error panel.

Stored query access is configured using a picker on the create and edit pages. The picker searches Datasette's `/-/queries.json?q=search-term` API and stores selected queries as `database-name/query-name` strings. Removing a query uses the `x` button next to that selected query. Additions and removals are not applied until the page is saved.

### Permissions

The plugin registers Datasette permissions for `create-app`, `view-app`, `edit-app`, `delete-app`, `manage-app-access`, and `apps-set-csp`. Stored app owners can always view, edit, delete, and manage their own apps. Apps marked private are visible only to their owner, even if other users have broad `view-app` permission grants.

Creating stored apps requires an explicit `create-app` permission grant. To grant that to all signed-in users:

```yaml
permissions:
  create-app:
    id: "*"
```

The `apps-set-csp` permission controls who can set arbitrary CSP origins on an app - see [Sandboxed apps](#sandboxed-apps). Nobody has it by default. To grant it to a specific user:

```yaml
permissions:
  apps-set-csp:
    id: admin
```

Deleting a stored app hides it from the catalog and disables access to its pages and query API. Its `app_revisions` rows remain in the database so a database administrator can recover it if needed.

Apps that are not private can be viewed by actors with the `view-app` permission. To let all signed-in users view all non-private apps, configure:

```yaml
permissions:
  view-app:
    id: "*"
```

External apps registered by plugins are not private by default, so they also require `view-app` permission unless the registering plugin supplies its own permission rules.

Signed-in users can pin apps from the catalog and from individual stored app pages. Pinned apps appear first on `/-/apps`, and the three most recently used pinned apps are shown on the Datasette homepage using `top_homepage()`.

The `/-/apps` catalog is searchable and paginated.

### App authoring

The create and edit pages include a copyable prompt for an LLM. The prompt is assembled in the browser from the current form state, so unsaved changes to selected databases, stored queries, and network origins are reflected immediately. It explains the sandbox, the `datasette.query()` and `datasette.storedQuery()` bridges, CSP restrictions, the current schema summary, and only the stored queries selected for that app.

The create and edit pages use Datasette's existing bundled CodeMirror editor for the HTML source textarea.

The edit page includes a private checkbox, SQL query database access, stored query access, and allowed network origins. The network origins control is a free-form list for users with the `apps-set-csp` permission, a set of checkboxes when an `allowed_csp_origins` allow-list is configured, and hidden otherwise.

### External apps from plugins

Datasette plugins can register their own apps that are independent of the HTML sandbox system. This allows apps with more complex requirements to still participate in other features built around the app registry.

Apps that are not stored as HTML are called **external apps**. They can be added and removed using the `Registry` class.

This example registers an additional app on startup:

```python
from datasette import hookimpl
from datasette_apps import Registry


@hookimpl
async def startup(datasette):
    await Registry(datasette).add_app(
        id="myplugin:example",
        name="Example plugin app",
        description="A plugin-owned app that appears in /-/apps",
        path="/-/myplugin-example",
        source="myplugin",
    )
```

Here's how to remove a single external app from the catalog by ID:

```python
await Registry(datasette).remove_app("myplugin:example")
```

## Development

To set up this plugin locally, first checkout the code. You can confirm it is available like this:
```bash
cd datasette-apps
# Confirm the plugin is visible
uv run datasette plugins
```

To run the tests:
```bash
uv run pytest
```
