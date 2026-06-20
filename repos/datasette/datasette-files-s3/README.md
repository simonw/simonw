# datasette-files-s3

[![PyPI](https://img.shields.io/pypi/v/datasette-files-s3.svg)](https://pypi.org/project/datasette-files-s3/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-files-s3?include_prereleases&label=changelog)](https://github.com/datasette/datasette-files-s3/releases)
[![Tests](https://github.com/datasette/datasette-files-s3/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-files-s3/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-files-s3/blob/main/LICENSE)

S3 storage backend for [datasette-files](https://github.com/datasette/datasette-files).

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-files-s3
```

## Usage

Configure a datasette-files source to use S3 storage by setting `"storage": "s3"` and providing the required configuration options:

```yaml
plugins:
  datasette-files:
    sources:
      my-s3-files:
        storage: s3
        config:
          bucket: my-bucket-name
          region: us-east-1
          access_key_id: AKIAIOSFODNN7EXAMPLE
          secret_access_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Or using Datasette's `-s` flag:

```bash
datasette data.db \
    -s plugins.datasette-files.sources.my-s3-files.storage s3 \
    -s plugins.datasette-files.sources.my-s3-files.config.bucket my-bucket-name \
    -s plugins.datasette-files.sources.my-s3-files.config.region us-east-1
```

You can also use a credentials broker that returns temporary AWS credentials plus the S3 folder to use:

```yaml
plugins:
  datasette-files:
    sources:
      my-s3-files:
        storage: s3
        config:
          credentials_url: https://example.com/api/s3-credentials
          credentials_url_secret: shared-secret
          region: us-east-1
```

### Credentials Broker Response

When `credentials_url` is configured, the plugin sends a `POST` request with
`secret=...` as form-encoded data and expects a JSON response shaped like this:

```json
{
  "AccessKeyId": "ASIAWXFXAIOZGGVU5O6Y",
  "SecretAccessKey": "...",
  "SessionToken": "...",
  "Expiration": "2026-03-20T11:56:23Z",
  "S3Folder": "s3://datasettecloud-dev-files/team-1/"
}
```

### Configuration options

- **bucket** (required unless `credentials_url` is used): The name of the S3 bucket.
- **region** (optional, default `us-east-1`): The AWS region.
- **prefix** (optional): A prefix to add to all S3 object keys. This allows you to store files under a specific path within the bucket. A trailing slash will be added automatically if not provided - `"uploads"` and `"uploads/"` are equivalent.
- **endpoint_url** (optional): A custom S3 endpoint URL, for use with S3-compatible services.
- **access_key_id** (optional): AWS access key ID.
- **secret_access_key** (optional): AWS secret access key.
- **session_token** (optional): AWS session token, for temporary credentials supplied directly in config.
- **credentials_url** (optional): URL to `POST` to for temporary credentials. The plugin sends `secret=...` as form-encoded data and expects a JSON response containing `AccessKeyId`, `SecretAccessKey`, `SessionToken`, `Expiration`, and `S3Folder`.
- **credentials_url_secret** (required with `credentials_url`): Shared secret sent to the credentials endpoint as the form field `secret`.

### Authentication

The plugin resolves AWS credentials using the following priority:

1. **Credentials broker**: If `credentials_url` is configured, the plugin fetches temporary credentials by `POST`ing `secret=...` to that URL. It stores the returned `AccessKeyId`, `SecretAccessKey`, `SessionToken`, `Expiration`, and `S3Folder`, and automatically fetches a fresh set after the expiration time passes. The returned `S3Folder` also sets the active bucket and prefix for the source.
2. **Direct configuration**: `access_key_id`, `secret_access_key`, and optional `session_token` in the config block.
3. **Default AWS credential chain**: If no credentials are provided through the above methods, the plugin falls back to the default AWS credential chain (environment variables, IAM roles, etc.).

### Prefix

The `prefix` option lets you scope all files to a specific path within the bucket. For example, with `prefix: "uploads/"`, a file uploaded as `photo.jpg` will be stored at the S3 key `uploads/photo.jpg`.

It does not matter whether you include a trailing slash or not - `"uploads"` and `"uploads/"` will both result in files stored under `uploads/`.

When using `credentials_url`, the returned `S3Folder` behaves like a dynamically supplied bucket + prefix. For example, `s3://datasettecloud-dev-files/team-1/` means the plugin will use bucket `datasettecloud-dev-files` and prefix `team-1/`.

## Development

To set up this plugin locally, first checkout the code.
```bash
cd datasette-files-s3
```

Run tests like this:
```bash
uv run pytest
```

You can use [SeaweedFS](https://github.com/seaweedfs/seaweedfs) to run a local development server against a local imitation of the S3 API:
```bash
brew install seaweedfs
./dev-server.sh
```
To run a local development server against a real S3 bucket, create a `dev-s3.sh` script (this file is in `.gitignore`):

```bash
#!/bin/bash
set -e

BUCKET="your-bucket-name"
REGION="us-east-1"
ACCESS_KEY="your-access-key-id"
SECRET_KEY="your-secret-access-key"

uv run datasette data.db --create --internal internal.db --root --secret 1 --reload \
    -s plugins.datasette-files.sources.s3-live.storage s3 \
    -s plugins.datasette-files.sources.s3-live.config.bucket "$BUCKET" \
    -s plugins.datasette-files.sources.s3-live.config.region "$REGION" \
    -s plugins.datasette-files.sources.s3-live.config.access_key_id "$ACCESS_KEY" \
    -s plugins.datasette-files.sources.s3-live.config.secret_access_key "$SECRET_KEY" \
    -s plugins.datasette-files.sources.s3-live.config.prefix "demo-prefix/" \
    -s permissions.files-browse true \
    -s permissions.files-upload true \
    -s permissions.files-edit true
```

Then run it with `bash dev-s3.sh` and follow the login token URL printed to the console.
