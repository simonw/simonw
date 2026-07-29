# @datasette/client

A small TypeScript `fetch()` wrapper for the [Datasette](https://datasette.io/) 1.0 JSON API.
No deps, pure ESM, should world in browser/node/deno/bun etc.

> [!WARNING]
> Alpha — expect breaking changes.

```sh
npm install @datasette/client
```

```ts
import { DatasetteClient } from "@datasette/client";
const client = new DatasetteClient({
  baseUrl: "https://example.com/", // default "/" (same-origin, browser)
  token: "dstok_...",              // optional, sent as Authorization: Bearer
});


const db = client.db("my-database");

// read queries
const pattern = 'abc*';
const rows = await db.sql`select * from kv where key like ${pattern}`;
const rows2 = db.query("select * from kv where key like :pattern", {pattern: "abc*"});

const key = 'sample';
const row = db.queryRow("select value from kv where key = :key", {key});
const value = db.queryValue("select value from kv where key = :key", {key});

// same, different API
const dogs = client.db("content").table("dogs");
await dogs.rows({ where: { age__gt: 4, name__contains: "o" }, sort: "-age" });

// Write API
await dogs.insert([{ name: "Cleo" }, { name: "Pancakes" }]);
await dogs.upsert({ id: 1, age: 6 });
await client.execute(`delete from logs where ts < :cutoff`, { cutoff });
```

## API overview

See [API.md](API.md) for the full API surface, result types, filters,
streaming and wire-protocol details.

## Development

```sh
npm test               # unit tests (mocked fetch)
npm run test:integration   # spins up a real Datasette 1.0a via uvx
npm run build          # tsc (dist/*.js + .d.ts) + esbuild single-file bundle
npm run docs           # TypeDoc API reference into docs/ (git-ignored)
```

`npm run build` emits both the module build (`dist/index.js`, used by the
package `exports`) and `dist/datasette-client.min.js` — a dependency-free
single-file ESM bundle (~12 KB, with sourcemap) for `<script type="module">`
or CDN use, also reachable as the `@datasette/client/bundle` export.


Deeper documentation lives in [`wiki/`](wiki/Home.md): the
[architecture](wiki/Architecture.md), the [wire-protocol
facts](wiki/Wire-Protocol.md) the client is built on, a [design decision
log](wiki/Design-Decisions.md) with the alternatives considered,
[testing notes](wiki/Testing.md) and the [future-work
roadmap](wiki/Future-Work.md).
