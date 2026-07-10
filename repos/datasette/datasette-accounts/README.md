# datasette-accounts

> [!WARNING]
> This plugin is experimental!


Username/password authentication for [Datasette](https://datasette.io) with
**accounts stored in the internal database** (not in plugin config). Provisioning,
password resets, disabling, and admin management all happen at runtime through an
admin UI, a `datasette accounts` CLI, and a JSON API, guarded by a real Datasette
1.0 permission.

> **"Basic" as in database-backed basic login — not HTTP Basic auth.**

Users log in at `/-/login`:

![The login page: a Log in heading with username and password fields, and a help note reading "Trouble signing in? Email data-help@example.com."](docs/screenshots/login.png)

Admins manage accounts at `/-/admin/users` — create accounts and disable, lock,
reset, promote, or delete existing ones:

![The admin accounts table listing users with admin, status, and lock columns and per-user action buttons.](docs/screenshots/admin.png)

## Features

- **Database-backed accounts** in Datasette's internal DB (create / disable /
  delete / reset-password / toggle-admin / unlock at runtime).
- **Server-side sessions** — revocable per-device, with "log out everywhere" and
  an admin session list. Disabling an account or revoking a session takes effect
  on the next request.
- **A registered admin action** (`datasette-accounts-admin`) that is
  self-answered for `root` and enabled admins, and composes with config `allow`
  blocks.
- **A `datasette accounts` CLI** for provisioning and managing accounts from the
  shell — the same audited, guarded code path as the web admin UI.
- **Security hardening** built in: timing-safe login (no username enumeration),
  PBKDF2 run off the event loop, unconditional CSRF gates, strict `?next=`
  validation, brute-force lockout (shared by login and change-password), forced
  first-password-change, audit logging, and retention/pruning.
- **A Svelte/TS frontend** for the login, account, and admin pages.
- **Integrates with `datasette-user-profiles`** (a required dependency) — emits a
  stable actor `id` and seeds the profiles directory, so every account can view
  and edit their profile once granted the `profile_access` permission.

## Installation

```bash
datasette install datasette-accounts
```

Requires Datasette **1.0a23+** and Python 3.10+.

## Getting started

### 1. Persist accounts with `--internal`

Accounts live in the internal database, which is an **ephemeral temp file unless
you pass `--internal`**. The plugin prints a loud startup warning when it is
ephemeral. For any real use:

```bash
datasette mydata.db --internal accounts.db
```

### 2. Create the first admin

There is no admin until you make one. The quickest way is the CLI, which writes
directly to the internal database — point it at the same `accounts.db`:

```bash
datasette accounts bootstrap-admin alice --generate -i accounts.db
# Created admin alice.
# Password (shown once): …
```

`bootstrap-admin` is **idempotent** — if an enabled admin already exists it prints
`admin already exists — skipping` and exits `0`, so it is safe to drop into a
container entrypoint or provisioning script. Pass `--password-stdin` to feed a
password without exposing it in argv, or `--generate` to mint one.

Prefer to bootstrap from the browser? Start Datasette with `--root`:

```bash
datasette mydata.db --internal accounts.db --root
```

Datasette prints a one-time `http://…/-/auth-token?token=…` URL that logs you in
as `root`, who is always allowed the admin action. Open **`/-/admin/users`**,
create your first admin account, then restart without `--root`.

### 3. Day-to-day

- Users log in at **`/-/login`** and manage their own password at **`/-/account`**.
- Admins manage accounts at **`/-/admin/users`**.
- The Datasette menu gains **Log in** / **Log out** / **Your account** entries,
  and an **Accounts** link for admins.

## Managing accounts from the shell

The `datasette accounts` command group is the CLI counterpart to the admin UI. It
does not touch the internal tables directly — every command reconstructs a
Datasette instance and calls the same audited, guarded `db.*` functions the web
routes use, so last-admin guards, session revocation, and the audit trail all
apply identically. Every mutating command requires `-i/--internal PATH`
(a persistent DB); every data-emitting command supports `--json`.

```
datasette accounts create USERNAME       # --admin, --generate, --password-stdin, --must-change
datasette accounts invite USERNAME        # create + one-time invite link (--admin, --ttl-hours, --base-url)
datasette accounts bootstrap-admin NAME   # idempotent first-admin creation
datasette accounts list                   # --admins / --pending / --locked / --disabled / --expired / --awaiting-approval
datasette accounts approve USERNAME       # approve a self-registered account request
datasette accounts reject USERNAME        # reject (delete) a pending account request
datasette accounts reset-password USERNAME
datasette accounts reset-link USERNAME    # one-time password-reset link (--ttl-hours, --base-url)
datasette accounts expire USERNAME        # set/clear an expiry deadline (--at, --in-days, --clear)
datasette accounts promote / demote USERNAME
datasette accounts disable / enable USERNAME
datasette accounts unlock USERNAME        # clear lockout counters
datasette accounts logout USERNAME        # revoke all of a user's sessions
datasette accounts delete USERNAME --yes
datasette accounts registration on|off|status  # open/close self-registration (runtime toggle)
datasette accounts audit                  # the admin-audit trail
datasette accounts login-attempts         # the login-attempt audit
datasette accounts hash-password [PASSWORD]
```

Run `datasette accounts COMMAND --help` for the full options of each. Generated
passwords are printed once to stdout and never written to the audit trail or
logs.

## Messages

Admins can write optional help text at **`/-/admin/messages`** — a sign-in prompt
shown on the homepage to signed-out visitors, and a help/contact note shown below
the login form. Blank hides a message. Bodies are admin-authored HTML rendered
verbatim, so you can include links and `mailto:` contacts (only admins can edit
them).

## Configuration

All options live under the `datasette-accounts` plugin block and have safe
defaults (a zero-config install works — it just warns about persistence):

| option | type | default | meaning |
|--------|------|---------|---------|
| `session_ttl_days` | int | `14` | absolute session lifetime |
| `password_min_length` | int | `8` | minimum new-password length (max is fixed at 1024) |
| `lockout_threshold` | int | `5` | consecutive failures before lock; `0` disables lockout |
| `lockout_minutes` | int | `15` | auto-unlock window after a lock |
| `secure_cookie` | `"auto"` / `true` / `false` | `"auto"` | Secure flag on the session cookie; set `true` when serving over HTTPS |
| `audit_retention_days` | int | `90` | delete `login_audit` rows older than this; `0` = keep forever |
| `admin_audit_retention_days` | int | `0` (keep forever) | delete admin-audit rows older than this |
| `invite_ttl_hours` | int | `72` | invite-link lifetime |
| `reset_link_ttl_hours` | int | `24` | reset-link lifetime |
| `max_pending_registrations` | int | `20` | refuse new self-registrations while the pending-approval queue is at this size |
| `registrations_per_ip_per_day` | int | `5` | per-IP daily self-registration cap (uses the client IP, so `trust_proxy_headers` applies) |

```yaml
plugins:
  datasette-accounts:
    session_ttl_days: 30
    password_min_length: 12
    secure_cookie: true
    audit_retention_days: 30
```

### User profiles

Accounts are seeded into [`datasette-user-profiles`](https://github.com/simonw/datasette-user-profiles)
automatically, but its profile pages are gated by the `profile_access`
permission, which denies by default. Grant it to every signed-in account so they
can view and edit their own profile:

```yaml
permissions:
  profile_access:
    id: "*"        # any actor with an id — i.e. any signed-in account
```

or on the command line:

```bash
datasette mydata.db --internal accounts.db -s permissions.profile_access.id '*'
```

## Development

See [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) for the security model, setup,
and the dev loop.

## License

Apache-2.0
