# browser-compare-db

A SQLite copy of [mdn/browser-compat-data](https://github.com/mdn/browser-compat-data).

The built (~66MB) database file [is available here](https://github.com/simonw/browser-compat-db/blob/db/browser-compat.db).

**[Explore it in Datasette Lite](https://lite.datasette.io/?url=https://github.com/simonw/browser-compat-db/blob/db/browser-compat.db#/browser-compat/releases_tree)**.

## Building it yourself

This project uses [uv](https://docs.astral.sh/uv/).

```bash
# Get a copy of the data
git clone https://github.com/mdn/browser-compat-data /tmp/browser-compat-data

# Build (or refresh) the database
uv run build_db.py /tmp/browser-compat-data --db browser-compat.db
```

The importer is idempotent. Pull the latest `main` in the data repo and run it
again against the same database file: features, releases and browsers that were
added, changed or removed upstream are all synced in place.

[`build_db.py`](build_db.py) loads a checkout of the MDN browser-compat-data
repository into a normalized SQLite database. Every record is validated
through [Pydantic models](models.py) first, so if MDN changes the shape of the
data the import fails loudly.

## Running the tests

```bash
uv run pytest
```

## Data freshness

<!-- [[[cog
import cog, cog_helpers
cog.outl(cog_helpers.metadata_block())
]]] -->
- **Data last updated:** 2026-06-24T11:36:39+00:00
- **Source commit:** `8fd53ab0162c64de185e2f64a3b7cead81c7a1d9`
- **browser-compat-data version:** 8.0.4
- **Imported at:** 2026-06-24T18:46:01.935101+00:00
<!-- [[[end]]] -->

## Tables and row counts

<!-- [[[cog
import cog, cog_helpers
cog.outl(cog_helpers.table_counts())
]]] -->
| Table | Rows |
| --- | --- |
| `browsers` | 17 |
| `browser_releases` | 1,599 |
| `features` | 19,834 |
| `feature_tags` | 16,210 |
| `feature_spec_urls` | 17,321 |
| `support` | 260,715 |
| `support_flags` | 885 |
| `metadata` | 4 |
<!-- [[[end]]] -->

## Database schema

<!-- [[[cog
import cog, cog_helpers
cog.outl("```sql")
cog.outl(cog_helpers.schema())
cog.outl("```")
]]] -->
```sql
CREATE TABLE "browsers" (
   "id" TEXT PRIMARY KEY,
   "name" TEXT,
   "type" TEXT,
   "upstream" TEXT,
   "preview_name" TEXT,
   "pref_url" TEXT,
   "accepts_flags" INTEGER,
   "accepts_webextensions" INTEGER
);
CREATE TABLE "browser_releases" (
   "browser_id" TEXT REFERENCES "browsers"("id"),
   "version" TEXT,
   "release_date" TEXT,
   "release_notes" TEXT,
   "status" TEXT,
   "engine" TEXT,
   "engine_version" TEXT,
   PRIMARY KEY ("browser_id", "version")
);
CREATE TABLE "features" (
   "id" TEXT PRIMARY KEY,
   "category" TEXT,
   "name" TEXT,
   "parent_id" TEXT REFERENCES "features"("id"),
   "depth" INTEGER,
   "description" TEXT,
   "mdn_url" TEXT,
   "source_file" TEXT,
   "experimental" INTEGER,
   "standard_track" INTEGER,
   "deprecated" INTEGER
);
CREATE TABLE "feature_tags" (
   "feature_id" TEXT REFERENCES "features"("id"),
   "tag" TEXT,
   PRIMARY KEY ("feature_id", "tag")
);
CREATE TABLE "feature_spec_urls" (
   "feature_id" TEXT REFERENCES "features"("id"),
   "spec_url" TEXT,
   PRIMARY KEY ("feature_id", "spec_url")
);
CREATE TABLE "support" (
   "feature_id" TEXT REFERENCES "features"("id"),
   "browser_id" TEXT REFERENCES "browsers"("id"),
   "statement_index" INTEGER,
   "is_mirror" INTEGER,
   "version_added" TEXT,
   "version_removed" TEXT,
   "supported" INTEGER,
   "prefix" TEXT,
   "alternative_name" TEXT,
   "partial_implementation" INTEGER,
   "impl_url" TEXT,
   "notes" TEXT,
   PRIMARY KEY ("feature_id", "browser_id", "statement_index")
);
CREATE TABLE "support_flags" (
   "feature_id" TEXT REFERENCES "features"("id"),
   "browser_id" TEXT,
   "statement_index" INTEGER,
   "flag_index" INTEGER,
   "type" TEXT,
   "name" TEXT,
   "value_to_set" TEXT,
   PRIMARY KEY ("feature_id", "browser_id", "statement_index", "flag_index")
);
CREATE TABLE "metadata" (
   "key" TEXT PRIMARY KEY,
   "value" TEXT
);
CREATE INDEX "idx_features_category"
    ON "features" ("category");
CREATE INDEX "idx_features_deprecated"
    ON "features" ("deprecated");
CREATE INDEX "idx_features_experimental"
    ON "features" ("experimental");
CREATE INDEX "idx_browser_releases_release_date"
    ON "browser_releases" ("release_date");
CREATE INDEX "idx_browser_releases_status"
    ON "browser_releases" ("status");
CREATE INDEX "idx_support_browser_id"
    ON "support" ("browser_id");
CREATE INDEX "idx_support_version_added"
    ON "support" ("version_added");
CREATE INDEX "idx_support_supported"
    ON "support" ("supported");
CREATE INDEX "idx_browser_releases_browser_id"
    ON "browser_releases" ("browser_id");
CREATE INDEX "idx_features_parent_id"
    ON "features" ("parent_id");
CREATE INDEX "idx_feature_tags_feature_id"
    ON "feature_tags" ("feature_id");
CREATE INDEX "idx_feature_spec_urls_feature_id"
    ON "feature_spec_urls" ("feature_id");
CREATE INDEX "idx_support_feature_id"
    ON "support" ("feature_id");
CREATE INDEX "idx_support_flags_feature_id"
    ON "support_flags" ("feature_id");
```
<!-- [[[end]]] -->

## How the data is modelled

See [notes.md](notes.md) for detailed notes on the upstream data shape. In
brief:

- **`browsers`** / **`browser_releases`** — browser metadata and full release
  histories (version, date, status, engine).
- **`features`** — one row per `__compat` node, identified by its dotted path
  (e.g. `css.properties.grid`). `parent_id` links each feature to its nearest
  ancestor feature, and `status` flags (`experimental`, `standard_track`,
  `deprecated`) are stored as columns.
- **`feature_tags`** / **`feature_spec_urls`** — the multi-valued `tags` and
  `spec_url` fields, normalized into child tables.
- **`support`** — one row per browser support statement. `version_added` is
  normalized so the column holds version strings (`"57"`, `"≤10"`, `"preview"`)
  while a `supported` column captures the `true`/`false`/unknown cases. The
  `"mirror"` shorthand is preserved as `is_mirror = 1`.
- **`support_flags`** — preference / runtime flags attached to a support
  statement.
- **`metadata`** — key/value provenance: upstream version, git commit and its
  date, and when the import ran.

The README sections above are generated with
[cog](https://cog.readthedocs.io/); regenerate them after a build with:

```bash
uv run cog -r README.md
```
