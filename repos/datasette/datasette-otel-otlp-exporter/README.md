# datasette-otel-otlp-exporter

Send [Datasette's builtin OpenTelemetry traces](https://docs.datasette.io/en/latest/internals.html#internals-telemetry) to any OTLP backend: Jaeger, Grafana Cloud, Honeycomb, an OpenTelemetry Collector, and so on.

Datasette records a span for every request and SQL query, but it doesn't send them anywhere on its own. `datasette-otel-otlp-exporter` sends them over OTLP/HTTP, the protocol nearly every tracing backend accepts, so you can see where a slow page spends its time, down to individual SQL queries. You configure it with a single plugin setting; there's no `opentelemetry-instrument` wrapper to run.

## Installing

This plugin requires [Datasette 1.0a41](https://github.com/simonw/datasette/releases/tag/1.0a41) or higher.

```bash
uv add datasette-otel-otlp-exporter
```

## Usage

A one-liner with [`uvx`](https://docs.astral.sh/uv/guides/tools/), sending traces to an OTLP endpoint on `localhost:4318`:

```bash
uvx --prerelease=allow \
  --with datasette-otel-otlp-exporter \
  --with 'datasette>=1a41' \
  datasette \
    -s plugins.datasette-otel-otlp-exporter.endpoint http://localhost:4318 \
    my_data.db
```

To try this locally, run [Jaeger](https://www.jaegertracing.io/download/), which ships as a single binary and accepts OTLP on port 4318. Load a few Datasette pages, wait about five seconds for the next batch to go out, then open the Jaeger UI at `http://localhost:16686` and pick the `datasette` service:

![A Jaeger trace of one Datasette table page: a GET request span with 53 child spans, mostly db.query spans a few hundred microseconds each](https://raw.githubusercontent.com/datasette/datasette-otel-otlp-exporter/main/.github/jaeger-trace.png)

Hosted backends usually want an API key in a header. Keep the key out of your config file with Datasette's `$env` substitution:

```yaml
# datasette.yaml
plugins:
  datasette-otel-otlp-exporter:
    endpoint: https://api.honeycomb.io
    headers:
      x-honeycomb-team:
        $env: HONEYCOMB_API_KEY
```

```bash
HONEYCOMB_API_KEY=... datasette my_data.db -c datasette.yaml
```

### Grafana Cloud

[Grafana Cloud's free tier](https://grafana.com/docs/grafana-cloud/send-data/otlp/) is a cheap way to get a hosted trace UI, for example for a Datasette instance on Fly.io. Its OTLP gateway needs a specific URL and a basic-auth header, so the plugin builds both from a `grafana_cloud` block:

```yaml
# datasette.yaml
plugins:
  datasette-otel-otlp-exporter:
    grafana_cloud:
      region: prod-us-east-0
      instance_id: "123456"
      api_token:
        $env: GRAFANA_CLOUD_TOKEN
```

All three values come from the **OpenTelemetry** tile on your stack's page at grafana.com, and the token needs the `traces:write` scope ([creating one](https://grafana.com/docs/grafana-cloud/send-data/traces/set-up/add-access-policy/)). Newer Grafana Cloud regions use a different gateway hostname than `otlp-gateway-<region>.grafana.net`. If yours does, replace `region` with `endpoint` set to the full URL from the tile, ending in `/otlp/v1/traces`.

### Service name and sampling

These use the standard OpenTelemetry environment variables:

```bash
OTEL_SERVICE_NAME=my-datasette \
OTEL_TRACES_SAMPLER=parentbased_traceidratio \
OTEL_TRACES_SAMPLER_ARG=0.25 \
  datasette my_data.db -c datasette.yaml
```

This labels the instance `my-datasette` in your tracing UI and keeps a quarter of traces. By default every trace is kept and the service name is `datasette`.

More details are in the [Reference](#reference) below.

## Privacy

Spans include the text of every SQL query Datasette runs, in the `db.query.text` attribute. On a public instance that includes any SQL visitors type into the query editor or send with `?sql=`. Parameter values are never recorded, but table names, column names and literal values written into the SQL are. Everything goes to the endpoint you configure, so if that's a third-party service, you are sending it your users' queries. Treat your tracing backend with the same care as the database itself.

## Reference

### Options

```yaml
# datasette.yaml
plugins:
  datasette-otel-otlp-exporter:
    endpoint: http://localhost:4318
    headers:
      x-api-key:
        $env: TRACING_API_KEY
```

| option | default | description |
|---|---|---|
| `endpoint` | | Base OTLP/HTTP URL, e.g. `http://localhost:4318`. `/v1/traces` is appended when the URL has no path. Without an endpoint, nothing is exported. |
| `headers` | `{}` | HTTP headers sent with every export, usually a vendor API key. |
| `grafana_cloud` | | Grafana Cloud settings (see below). Sets a default `endpoint` and `Authorization` header. |

`grafana_cloud` takes:

| option | description |
|---|---|
| `instance_id` | Required. Your stack's instance ID, sent as the basic-auth username. |
| `api_token` | Required. An access policy token with the `traces:write` scope, sent as the basic-auth password. |
| `region` | Your stack's region, e.g. `prod-us-east-0`, used to build the URL `https://otlp-gateway-<region>.grafana.net/otlp/v1/traces`. |
| `endpoint` | The full gateway URL, ending in `/otlp/v1/traces`. Use this instead of `region` when your stack's hostname doesn't follow that pattern. |

Some behavior to be aware of:

- Without an `endpoint` (or `grafana_cloud` block), the plugin prints `no endpoint configured - OpenTelemetry export is disabled` to stderr at startup and sends nothing.
- Unknown options and invalid values fail at startup, listing every problem:
  ```
  Error: datasette-otel-otlp-exporter: invalid plugin config
    endpiont: Extra inputs are not permitted
  ```
- An explicit `endpoint` takes precedence over the one `grafana_cloud` builds. Explicit `headers` are merged over its `Authorization` header, key by key.
- Spans are sent in batches, about every five seconds, and once more when Datasette exits.
- If the backend is unreachable, Datasette keeps serving pages as normal. Each batch is retried for a few seconds, then dropped with a `Failed to export span batch` log message.

### Environment variables

The standard OpenTelemetry environment variables are supported, and they take precedence over plugin config:

| variable | description |
|---|---|
| `OTEL_SERVICE_NAME` | The `service.name` shown in your tracing UI. Defaults to `datasette`. `service.name` in `OTEL_RESOURCE_ATTRIBUTES` works too. |
| `OTEL_TRACES_SAMPLER`, `OTEL_TRACES_SAMPLER_ARG` | Which traces to keep. Defaults to keeping all of them. |
| `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Override `endpoint`. |
| `OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_EXPORTER_OTLP_TRACES_HEADERS` | Override `headers`. |

The service name and sampler are read when Datasette loads its plugins, so they also apply to the `datasette.startup` trace.

### What gets exported

Whatever Datasette records. The plugin adds no spans of its own. That's one span per HTTP request named after the method and the route that matched it, one per SQL query with its text, database and timing, spans for writes, and a `datasette.startup` trace covering plugin hooks and loading the internal catalog. The full list of spans and attributes is in [Datasette's telemetry documentation](https://docs.datasette.io/en/latest/internals.html#internals-telemetry).

Only traces are exported. For metrics, see [datasette-otel-prometheus](https://github.com/datasette/datasette-otel-prometheus).

### Using alongside other OpenTelemetry setups

OpenTelemetry allows one tracer provider per process. The plugin installs its own when it is first imported, unless one already exists. If Datasette runs under `opentelemetry-instrument`, inside an application that set up tracing, or alongside another exporter plugin such as [datasette-otel-file-exporter](https://github.com/datasette/datasette-otel-file-exporter), the plugin adds its exporter to that provider instead. Both get every span, whichever loaded first. In that case the other provider's sampler and service name apply.

If the existing provider isn't the OpenTelemetry SDK's (for example a `NoOpTracerProvider`, which turns tracing off), the plugin can't attach to it. It prints a warning to stderr and exports nothing.
