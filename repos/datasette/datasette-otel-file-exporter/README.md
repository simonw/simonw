# datasette-otel-file-exporter

Export [Datasette's builtin OpenTelemetry data](https://docs.datasette.io/en/latest/internals.html#internals-telemetry) into NDJSON or Parquet files, to the disk or to S3.

Many tools that read OTel data can be expensive or impractical to run for small Datasette deployments. You *could* run [Honeycomb](https://www.honeycomb.io/platform/opentelemetry) or [Grafana](https://grafana.com/docs/opentelemetry/collector/) alongside your Datasette instances, but a constantly-running service adds up. The `datasette-otel-file-exporter` plugin sidesteps this, saving OTel data cheaply to your filesystem or S3. If you need to debug a slow Datasette instance or inspect some logs, you can retrieve your traces from the exported files.

## Installing

This plugin requires [Datasette 1.0a41](https://github.com/simonw/datasette/releases/tag/1.0a41) or higher.

```bash
uv add datasette-otel-file-exporter

# parquet support, default is gzip'ed NDJSON files
uv add datasette-otel-file-exporter[parquet]

# S3 support, default is filesystem
uv add datasette-otel-file-exporter[obstore]
```

## Usage

A one-liner with [`uvx`](https://docs.astral.sh/uv/guides/tools/):
```bash
uvx --prerelease=allow \
  --with datasette-otel-file-exporter \
  --with 'datasette>=1a41' \
  datasette \
    -s plugins.datasette-otel-file-exporter.path ./telemetry \
    my_data.db
```

After a few seconds of traffic, `datasette-otel-file-exporter` will begin to export OpenTelemetry traces as gzip'ed NDJSON files to the `telemetry/` directory.

```
› tree telemetry
telemetry
└── traces
    └── 2026
        └── 09
            └── 24
                └── 21
                    ├── 1790284044926-96db28b2.ndjson.gz
                    ├── 1790284064949-6c93d218.ndjson.gz
                    └── 1790284567838-5cfff753.ndjson.gz
```

You can query this data with any analytical tool. Here's an example query with DuckDB:

```text
> from read_json_auto('telemetry/traces/**/*.ndjson.gz');
┌────────────────┬─────────────────────────────────┬──────────────────┬──────────────────┬───┬──────────────────────┬──────────────────────┬────────┬────────┐
│ schema_version │            trace_id             │     span_id      │  parent_span_id  │ … │      attributes      │       resource       │ events │ links  │
│     int64      │             varchar             │     varchar      │     varchar      │ … │ struct("db.system" … │ struct("telemetry.s… │ json[] │ json[] │
├────────────────┼─────────────────────────────────┼──────────────────┼──────────────────┼───┼──────────────────────┼──────────────────────┼────────┼────────┤
│              1 │ 268abc18c6dbb29f746d196df9d404… │ 1ee8e06fb218a279 │ eb9aa742efee8c68 │ … │ {'db.system': NULL,… │ {'telemetry.sdk.lan… │ []     │ []     │
│              1 │ 268abc18c6dbb29f746d196df9d404… │ eb9aa742efee8c68 │ NULL             │ … │ {'db.system': sqlit… │ {'telemetry.sdk.lan… │ []     │ []     │
│              · │                ·                │        ·         │        ·         │ … │ ·                    │          ·           │ ·      │ ·      │
│              1 │ 9b2a6a045305ebe32ce0c9107c3512… │ 7cf2943e9b815d56 │ NULL             │ … │ {'db.system': NULL,… │ {'telemetry.sdk.lan… │ []     │ []     │
└────────────────┴─────────────────────────────────┴──────────────────┴──────────────────┴───┴──────────────────────┴──────────────────────┴────────┴────────┘
```

Parquet files are supported as well, but require the `[parquet]` extra and the `format` config option:

```bash
uvx --prerelease=allow \
  --with datasette-otel-file-exporter[parquet] \
  --with 'datasette>=1a41' \
  datasette \
    -s plugins.datasette-otel-file-exporter.path ./telemetry \
    -s plugins.datasette-otel-file-exporter.format parquet \
    my_data.db
```

And instead of writing to the filesystem, you can opt-in and configure `datasette-otel-file-exporter` to write to an S3 bucket, with the `[obstore]` extra and the `url` config option:

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=...
uvx --prerelease=allow \
  --with datasette-otel-file-exporter[parquet,obstore] \
  --with 'datasette>=1a41' \
  datasette \
    -s plugins.datasette-otel-file-exporter.url s3://my-bucket/telemetry \
    -s plugins.datasette-otel-file-exporter.format parquet \
    my_data.db
```

More configuration options, including setting access keys in configuration instead of environment variables, are in the [Configuration Reference](./DOCUMENTATION.md#configuration-reference).

## Privacy

The exported files include the text of SQL queries Datasette runs, and on a public instance that includes SQL sent by visitors. Parameter values are never recorded. Treat the telemetry directory or bucket with the same care as the database itself. See [Privacy](./DOCUMENTATION.md#privacy).

## More

- [Documentation](./DOCUMENTATION.md): file format, schema and every configuration option
- [Cookbook](./COOKBOOK.md): `jq` and DuckDB recipes for slow queries, request rates, trace trees and more
