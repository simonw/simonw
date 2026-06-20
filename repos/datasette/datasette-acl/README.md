# datasette-acl

[![PyPI](https://img.shields.io/pypi/v/datasette-acl.svg)](https://pypi.org/project/datasette-acl/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-acl?include_prereleases&label=changelog)](https://github.com/datasette/datasette-acl/releases)
[![Tests](https://github.com/datasette/datasette-acl/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-acl/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-acl/blob/main/LICENSE)

Advanced permission management for Datasette. **Highly experimental**.

## Installation

Install this plugin in the same environment as Datasette. This plugin requires Datasette 1.0a15 or higher.
```bash
datasette install datasette-acl
```
## Usage

This plugin is under active development. It supports configuring [permissions](https://docs.datasette.io/en/latest/authentication.html#permissions) for individual tables — controlling the following actions — as well as for [any custom resource type](#custom-resource-types) registered by a plugin:

- `insert-row`
- `delete-row`
- `update-row`
- `alter-table`
- `drop-table`

Grants can target individual users, [user groups](#user-groups), or [general-access audiences](#principals-and-general-access) like "any signed-in user".

Permissions are saved in the internal database. This means you should run Datasette with the `--internal path/to/internal.db` option, otherwise your permissions will be reset every time you restart Datasette.

A JSON HTTP API for reading and managing per-resource grants programmatically is documented in [docs/json-api.md](docs/json-api.md).

### Managing permissions for a table

The interface for configuring table permissions lives at `/-/acl/resource/table/<database-name>/<table-name>`. It can be accessed from the table actions menu on the table page.

Permission can be granted for each of the above table actions. They can be assigned to both groups and individual users, who can be added using their `actor["id"]`.

The page also offers a **General access** section for granting table actions to public audiences such as "any signed-in user". See [Principals and general access](#principals-and-general-access).

An audit log tracks which permissions were added and removed, displayed at the bottom of the permissions page.

### Custom resource types

`datasette-acl` is not limited to tables. It can store and resolve grants for *any* resource type defined by a plugin - documents, lists, workbooks, comment spaces, kanban boards and so on.

There is no dedicated hook for this. A plugin makes its resource type manageable by `datasette-acl` simply by registering actions whose `resource_class` is a [Resource](https://docs.datasette.io/en/latest/internals.html) subclass:

```python
from datasette import hookimpl
from datasette.permissions import Action, Resource


class Playlist(Resource):
    name = "playlist"


@hookimpl
def register_actions(datasette):
    return [
        Action(name="playlist-view", description="View a playlist", resource_class=Playlist),
        Action(name="playlist-edit", description="Edit a playlist", resource_class=Playlist),
    ]
```

`datasette-acl` discovers resource types from the actions registered across all plugins (`datasette.actions`). The action set offered for each resource type is derived dynamically from this - nothing is hardcoded.

A generic admin page for any resource type lives at:

```
/-/acl/resource/<resource-type>/<parent>/<child>
```

For example `/-/acl/resource/playlist/workspace-1/playlist-42`. The `<child>` segment is optional for parent-only resource types (`/-/acl/resource/<resource-type>/<parent>`). The page presents group, user, general-access grants and an audit log, with checkboxes for exactly the actions registered for that resource type. Access to this admin page is granted to users with the `datasette-acl` permission described below, or users who can manage that specific resource.

The page also has a **General access** section for exposing a resource without naming individual users — see [Principals and general access](#principals-and-general-access) below.

Grants made here flow through Datasette's permission system: once granted, `await datasette.allowed(actor=..., action="playlist-edit", resource=Playlist("workspace-1", "playlist-42"))` returns `True`.

### Principals and general access

Every grant names exactly one **principal**, recorded in the `principal_type` column on each stored grant. There are five kinds — two identified by an id, and three public audiences identified by the type alone:

| `principal_type` | Grants to | Identified by |
| --- | --- | --- |
| `actor` | An individual user | `actor_id` |
| `group` | All members of a [user group](#user-groups) | `group_id` |
| `everyone` | Anyone, signed in or not | — |
| `authenticated` | Any signed-in actor | — |
| `anonymous` | Signed-out (anonymous) visitors only | — |

The generic resource admin page presents the three audiences as its **General access** section (labelled "Anyone (signed in or not)", "Any signed-in user" and "Signed-out (anonymous) visitors only"), and the audit log's Principal column shows the same labels. Audiences can also be granted programmatically: pass `principal_type` to the [JSON API](docs/json-api.md), or an audience `Principal` (e.g. `Principal.authenticated()`) to the [Python helpers](#python-api-for-managing-grants).

Audience grants store `principal_type` only; their `actor_id` and `group_id` columns are both null. Permission checks match actor grants by `actor_id`, group grants by `group_id`, and general-access grants by `principal_type`. Code writing rows directly to the `acl` table must provide a valid `principal_type` and respect the table's CHECK constraint; prefer the [Python API](#python-api-for-managing-grants).

### Declaring roles

Raw action grants are flexible but users think in roles. A plugin can declare friendly roles for its resource type with the `datasette_acl_roles` hook, mapping each role name to the bundle of actions it grants. Almost every plugin wants the same three cumulative roles - Viewer, Editor and Manager - so rather than declaring them by hand, use the `standard_roles()` factory.

A complete plugin declares its `Resource` subclass, registers an `Action` for each action name, then maps those same names to roles. Define the names once as constants so the two hooks can't drift apart:

```python
from datasette import hookimpl
from datasette.permissions import Action, Resource
from datasette_acl.roles import standard_roles

VIEW = "playlist-view"
EDIT = "playlist-edit"
MANAGE = "playlist-manage"


class Playlist(Resource):
    name = "playlist"


@hookimpl
def register_actions(datasette):
    return [
        Action(name=VIEW, description="View a playlist", resource_class=Playlist),
        Action(name=EDIT, description="Edit a playlist", resource_class=Playlist),
        Action(name=MANAGE, description="Manage playlist sharing", resource_class=Playlist),
    ]


@hookimpl
def datasette_acl_roles(datasette):
    return standard_roles(
        Playlist.name,
        view=VIEW,
        edit=EDIT,
        manage=MANAGE,
    )
```

This returns the canonical triple: **Viewer** (the `view` actions), **Editor** (`view` + `edit`) and **Manager** (`view` + `edit` + `manage`, marked as authorizing re-sharing). Each of `view=`/`edit=`/`manage=` accepts a single action name or a list, and `descriptions=` optionally overrides the default role descriptions by role name:

```python
standard_roles(
    "table",
    view="view-table",
    edit=["insert-row", "update-row", "delete-row"],
    manage="manage-table",
    descriptions={"Manager": "Full control, including sharing"},
)
```

Role names then work everywhere roles are accepted: the `role=` argument to the Python `grant()`/`update_role()` helpers below, and the JSON API. If you need different role names or additional roles, construct `datasette_acl.roles.AclRole` objects directly (or append them to the list returned by `standard_roles()`) - each declares a `resource_type`, `name`, `actions` list, a `rank` for ordering, and `manage=True` on the role whose exclusive actions allow changing sharing.

### Controlling who can edit permissions

Users with the new `datasette-acl` permission will have the ability to access a UI for setting permissions for users and groups on a table.

To configure the root user to have this permission, add the following to your Datasette configuration:

```yaml
permissions:
  datasette-acl:
    id: root
```
Alternatively you can start Datasette running like this:
```bash
datasette mydata.db --root --internal internal.db \
  -s permissions.datasette-acl.id root
```

### User groups

Users can be assigned to groups, and those groups can then be used to quickly assign permissions to all of those users at once.

To manage your groups, visit `/-/acl/groups` or use the "Manage user groups" item in the Datasette application menu.

Add users to a group by typing in their actor ID. Remove them using the remove user button.

The page for each group includes an audit log showing changes made to that group's list of members.

When you delete a group its members will all be removed and it will be marked as deleted. Creating a group with the same name will reuse that group's record and display its existing audit log, but will not re-add the members that were removed.

### Dynamic groups

You may wish to define permission rules against groups of actors based on their actor attributes, without needing to manually add those actors to a group. This can be achieved by defining a dynamic group in the `datasette-acl` configuration.

Dynamic groups are defined in terms of [allow blocks](https://docs.datasette.io/en/stable/authentication.html#defining-permissions-with-allow-blocks). The following configuration defines two dynamic groups - one called `admin` that contains all users with `"is_admin": true` in their attributes, and another called `sales` that explicitly includes users with `"sales"` as one of the values in their `departments` array.

```yaml
plugins:
  datasette-acl:
    dynamic-groups:
      admin:
        is_admin: true
      sales:
        departments: ["sales"]
```

Any time an actor has their permissions checked they will be dynamically added to or removed from these groups based on the current value of their actor attributes.

Dynamic groups are displayed in the list of groups, but their members cannot be manually added or removed.

### Table creator permissions

If you allow regular users to create tables in Datasette, you may want them to maintain a level of "ownership" over those tables, such that other users are unable to modify those tables without the creator's permission.

The `table-creator-permissions` plugin setting can be used to automatically configure permissions for the actor who created a table.

Enable that like this:
```yaml
plugins:
  datasette-acl:
    table-creator-permissions:
    - alter-table
    - drop-table
    - insert-row
    - update-row
    - delete-row
```
### Configuring autocomplete against actor IDs

By default, users of this plugin can assign permissions to any actor ID by entering that ID, whether or not that ID corresponds to a user that exists elsewhere in the current Datasette configuration.

If you are running this plugin in an environment with a fixed, known list of actor IDs you can implement a plugin using the `datasette_acl_valid_actors(datasette)` plugin hook which returns an iterable sequence of string actor IDs or `{"id": "actor-id", "display": "Actor Name"}` dictionaries

These will then be used for both validation and autocomplete, ensuring users do not attach actor IDs that are not in that list.

Example plugin implementation:
```python
from datasette import hookimpl

@hookimpl
def datasette_acl_valid_actors(datasette):
    return ["paulo", "rohan", "simon"]
```
This function can also return an async inner function, for making async calls. This example uses the `[{"id": "actor-id", "display": "Actor Name"}]` format:
```python
from datasette import hookimpl

@hookimpl
def datasette_acl_valid_actors(datasette):
    async def inner():
        db = datasette.get_internal_database()
        return (await db.execute("select id, username as display from users")).dicts()
    return inner
```

### Python API for managing grants

`datasette_acl.grants` provides async helpers so other plugins can read and modify grants without writing raw SQL against the ACL tables. Each call resolves the `(resource_type, parent, child)` resource, writes the `acl` rows, and appends audit entries attributed to `by_actor`.

The principal — who a grant targets — is a `Principal` value object, built via one of its constructors: `Principal.actor(id)`, `Principal.group(id)`, or a [public audience](#principals-and-general-access) `Principal.everyone()` / `Principal.authenticated()` / `Principal.anonymous()`. Pass it as `principal=`, and for `grant()` supply exactly one of `role=` or `actions=`:

```python
from datasette_acl.grants import grant, revoke, update_role, list_grants, Principal

# Any signed-in user becomes a Viewer
await grant(datasette, "doc", "doc1", principal=Principal.authenticated(), role="Viewer")
# A specific user becomes an Editor
await grant(datasette, "doc", "doc1", principal=Principal.actor("alice"), role="Editor")
```

`grant(...)` — give a principal access, by raw actions or by a role (idempotent). Returns the actions now held. Role names come from the `datasette_acl_roles` hook:

```python
await grant(datasette, "table", "mydb", "mytable", principal=Principal.actor("alice"), actions=["insert-row"])
await grant(datasette, "table", "mydb", "mytable", principal=Principal.group(3), actions=["insert-row"], by_actor="root")
```

To remove one action from a principal while keeping others, first `revoke(...)` all grants for that principal on the resource, then call `grant(..., actions=[...])` with the actions that should remain.

`update_role(...)` — atomically swap a principal's actions to exactly those of a registered `role`. Returns the new actions:

```python
await update_role(datasette, "doc", "doc1", principal=Principal.actor("alice"), role="Viewer")
```

`revoke(...)` — remove all of a principal's grants on a resource. Returns the actions that were removed:

```python
await revoke(datasette, "table", "mydb", "mytable", principal=Principal.actor("alice"))
```

`list_grants(...)` — list current grants on a resource as dicts (`{"principal", "actor_id", "group_id", "group_name", "actions"}`, where `principal` is the stored `principal_type`; audience grants carry no id):

```python
grants = await list_grants(datasette, "table", "mydb", "mytable")
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-acl
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```

### Tips for local development

Here's how to run the plugin with all of its features enabled.

First, grab a test database:
```bash
wget https://latest.datasette.io/fixtures.db
```
Install the [datasette-unsafe-actor-debug](https://github.com/datasette/datasette-unsafe-actor-debug) plugin, so you can use the `http://127.0.0.1:8001/-/unsafe-actor` page to quickly imitate any actor for testing purposes:
```bash
datasette install datasette-unsafe-actor-debug
```
And [datasette-visible-internal-db](https://github.com/datasette/datasette-visible-internal-db) to make it easy to see what's going on in the internal database:
```bash
datasette install datasette-visible-internal-db
```
Then start Datasette like this:
```bash
datasette fixtures.db --internal internal.db \
  -s permissions.datasette-acl.id root \
  -s plugins.datasette-unsafe-actor-debug.enabled 1 \
  -s plugins.datasette-acl.table-creator-permissions '["insert-row", "update-row"]' \
  -s plugins.datasette-acl.dynamic-groups.staff.is_staff true \
  --root \
  --secret 1 \
  --reload
```
This configures Datasette to provide a URL for you to sign in as root, which will give you access to the permission editing tool.

It ensures that any user who creates a table (which you can test using the `/-/api` API explorer tool) will be granted initial `insert-row` and `update-row` permissions.

It sets up a dynamic group such that any actor with `{"is_staff": true}` in their JSON will be treated as a member of that group.

`--reload` means Datasette will reload on any code changes to the plugin, and `--secret 1` ensures your Datasette authentication cookies will continue to work across server restarts.
