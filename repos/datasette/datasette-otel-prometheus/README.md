# datasette-otel-prometheus

Serve [Datasette's builtin OpenTelemetry metrics](https://docs.datasette.io/en/latest/internals.html#internals-telemetry) on a dedicated port for [Prometheus](https://prometheus.io/) to scrape.

Datasette records metrics like SQL query durations, SQL thread pool usage and write queue depth through OpenTelemetry. `datasette-otel-prometheus` collects them and serves them in the Prometheus text format on a separate port, so you can graph and alert on them with Prometheus, Grafana, or anything else that speaks the format. It works the same way [Litestream](https://litestream.io/reference/metrics/) and node_exporter expose their metrics.

## Installing

This plugin requires [Datasette 1.0a41](https://github.com/simonw/datasette/releases/tag/1.0a41) or higher.

```bash
uv add datasette-otel-prometheus
```

## Usage

A one-liner with [`uvx`](https://docs.astral.sh/uv/guides/tools/):

```bash
uvx --prerelease=allow \
  --with datasette-otel-prometheus \
  --with 'datasette>=1a41' \
  datasette \
    -s plugins.datasette-otel-prometheus.port 9464 \
    my_data.db
```

Datasette serves pages on its usual port, and metrics are served at `http://127.0.0.1:9464/metrics`:

```
› curl -s localhost:9464/metrics | grep -v _bucket
# HELP db_client_operation_duration_seconds Duration of a SQL operation issued by Datasette
# TYPE db_client_operation_duration_seconds histogram
db_client_operation_duration_seconds_count{datasette_operation="read",db_namespace="my_data",db_system="sqlite",error_type="",...} 100.0
db_client_operation_duration_seconds_sum{datasette_operation="read",db_namespace="my_data",db_system="sqlite",error_type="",...} 0.0169599649925658
# HELP datasette_sql_threads_queue_depth Read queries waiting for a free thread in the shared SQL pool
# TYPE datasette_sql_threads_queue_depth gauge
datasette_sql_threads_queue_depth{...} 0.0
# HELP datasette_connections_open Open SQLite connections tracked for closing
# TYPE datasette_connections_open gauge
datasette_connections_open{db_namespace="my_data",...} 3.0
...
```

(Output trimmed. Every series also carries `otel_scope_*` labels.)

Point Prometheus at it with a scrape config:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: datasette
    static_configs:
      - targets: ["localhost:9464"]
```

To scrape from another machine, bind to a reachable interface with the `host` option. The listener has no authentication, so only do this on a private network:

```bash
datasette my_data.db \
  -s plugins.datasette-otel-prometheus.port 9464 \
  -s plugins.datasette-otel-prometheus.host 0.0.0.0
```

The service name comes from the standard `OTEL_SERVICE_NAME` environment variable and shows up in the `target_info` series:

```bash
OTEL_SERVICE_NAME=my-datasette datasette my_data.db \
  -s plugins.datasette-otel-prometheus.port 9464
```

More details are in the [Reference](#reference) below.

## Security

Anyone who can reach the metrics port can read every metric, with no login required. Datasette's own metrics include database names and error types, but never query text or parameter values. Metrics recorded by other plugins could include anything those plugins choose to record. The listener binds to `127.0.0.1` by default, so only processes on the same machine can reach it until you change `host`.

## Reference

### Options

```yaml
# datasette.yaml
plugins:
  datasette-otel-prometheus:
    port: 9464
    host: 127.0.0.1
```

| option | default | description |
|---|---|---|
| `port` | | Port for the metrics listener, 1-65535. Required: without it, no listener starts. |
| `host` | `127.0.0.1` | Interface to bind to. Use `0.0.0.0` to accept scrapes from other machines. |

Some behavior to be aware of:

- If `port` isn't set, the plugin does nothing.
- Unknown options and invalid values fail at startup, e.g. `Error: Invalid datasette-otel-prometheus plugin config - prot: Extra inputs are not permitted`.
- If the port is already in use, Datasette still starts and serves pages. The plugin prints `could not listen on <host>:<port>` to stderr and no metrics are served.
- The listener starts once Datasette's server is running and stops when it shuts down. One-off commands such as `datasette --get`, `inspect` and `publish` never bind the port.
- Any path on the listener serves the metrics. Prometheus's default `/metrics` is the conventional one.
- Prometheus can request the OpenMetrics format and gzip compression, and the listener supports both.

### Service name

The `service.name` resource attribute appears as `service_name` on the `target_info` series. It's set from the standard OpenTelemetry environment variables:

1. `OTEL_SERVICE_NAME`
2. `service.name` in `OTEL_RESOURCE_ATTRIBUTES`
3. Otherwise `datasette`

### Why a separate port?

Metrics are served by their own small HTTP server in a background thread, not by a Datasette route:

- Access is controlled by where the listener binds, so there's no Datasette permission or token to set up for your scraper.
- Scrapes are answered even while Datasette's event loop is busy or stuck, which is when you most want the numbers.
- Scrapes never show up in Datasette's own request metrics.

The catch is that platforms which expose a single port, such as Google Cloud Run via `datasette publish cloudrun`, can't be scraped this way.

### Using alongside other OpenTelemetry setups

The plugin installs its own OpenTelemetry `MeterProvider` when it is first imported. OpenTelemetry allows only one provider per process, and the Prometheus reader can't be added to an existing one. So if another provider is already installed, for example because Datasette runs under `opentelemetry-instrument`, the plugin prints a warning to stderr. The listener still starts but serves no Datasette metrics; they go to the other provider instead.
