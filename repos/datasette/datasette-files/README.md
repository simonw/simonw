# datasette-files

[![PyPI](https://img.shields.io/pypi/v/datasette-files.svg)](https://pypi.org/project/datasette-files/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-files?include_prereleases&label=changelog)](https://github.com/datasette/datasette-files/releases)
[![Tests](https://github.com/datasette/datasette-files/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-files/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-files/blob/main/LICENSE)

File management for Datasette. Upload, serve, search and manage files through a pluggable storage backend system. Ships with built-in filesystem storage and a plugin hook for adding custom backends (S3, Google Cloud Storage, etc.).

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-files
```

## Usage

datasette-files manages files through **sources** — named connections to storage backends. Each source has a slug, a storage type, and backend-specific configuration.

The default `filesystem` source stores files in a directory on disk. You can install additional plugins to add support for extra sources such as [datasette-files-s3](https://github.com/datasette/datasette-files-s3).

### Configuring sources

Define sources in your `datasette.yaml` under the `datasette-files` plugin config:

```yaml
plugins:
  datasette-files:
    sources:
      my-files:
        storage: filesystem
        config:
          root: /data/uploads
```

This creates a source called `my-files` backed by a local directory at `/data/uploads`. The directory will be created if it doesn't exist.

You can configure multiple sources:

```yaml
plugins:
  datasette-files:
    sources:
      photos:
        storage: filesystem
        config:
          root: /data/photos
      documents:
        storage: filesystem
        config:
          root: /data/documents
```

### Permissions

All access is **denied by default**. You must explicitly grant permissions in the `permissions:` block of your `datasette.yaml`.

There are four permission actions:

| Action | Description | Scoped to |
|--------|-------------|-----------|
| `files-browse` | Browse, search, view, and download files | Source |
| `files-upload` | Upload files to a source | Source |
| `files-edit` | Edit file metadata (e.g. search text) | File |
| `files-delete` | Delete files from a source | File |

`files-browse` and `files-upload` are scoped to a source — granting them allows the action on all files in that source. `files-edit` and `files-delete` are scoped to individual files, but a source-level grant cascades to all files within it.

CSV/TSV import also requires Datasette's built-in `create-table` and `insert-row` permissions on the target database. See [Built-in CSV import action](#built-in-csv-import-action) for details.

**Grant access to everyone (all sources):**

```yaml
permissions:
  files-browse: true
  files-upload: true
```

**Grant access to a specific user:**

```yaml
permissions:
  files-browse:
    id: alice
  files-upload:
    id: alice
```

**Per-source permissions:**

```yaml
permissions:
  files-browse:
    public-files:
      allow: true
    private-files:
      allow:
        id: alice
  files-upload:
    public-files:
      allow:
        id: alice
```

#### Owner permissions

By default, anyone with `files-edit` or `files-delete` permission on a source can edit or delete any file in that source. You can restrict edit and delete so that users can only act on files they uploaded themselves:

```yaml
plugins:
  datasette-files:
    owners_can_edit: true
    owners_can_delete: true
    sources:
      my-files:
        storage: filesystem
        config:
          root: /data/uploads
```

With these settings, the uploader of each file gains edit or delete permission on their own files — without needing a source-level `files-edit` or `files-delete` grant. Actors who *do* have a source-level grant (e.g. admins) can still act on any file in that source.

Files uploaded without an authenticated actor have no owner, so they can only be managed by actors with source-level grants.

### Uploading files

Visit `/-/files/upload/{source_slug}` for a dedicated drag-and-drop upload page. It supports multiple files, per-file progress bars, and SVG file-type previews.

The same upload component is shown on `/-/files/source/{source_slug}` when you have `files-upload` permission for that source.

#### Upload API

The upload UI and the file picker dialog both use a three-step flow: **prepare**, **upload**, **complete**. For the built-in `filesystem` backend, step 2 uploads the file bytes to Datasette.

**Step 1: Prepare**

```bash
curl -X POST "http://localhost:8001/-/files/upload/my-files/-/prepare" \
  -H "Content-Type: application/json" \
  -d '{"filename": "photo.jpg", "content_type": "image/jpeg", "size": 48210}'
```

Returns upload instructions:

```json
{
  "ok": true,
  "upload_token": "tok_01j5...",
  "upload_url": "/-/files/upload/my-files/-/upload",
  "upload_method": "POST",
  "upload_headers": {},
  "upload_fields": {"upload_token": "tok_01j5..."}
}
```

**Step 2: Upload** — send the file to the `upload_url` from step 1:

```bash
curl -X POST "http://localhost:8001/-/files/upload/my-files/-/upload" \
  -F "upload_token=tok_01j5..." \
  -F "file=@photo.jpg"
```

**Step 3: Complete** — finalize the upload and register the file:

```bash
curl -X POST "http://localhost:8001/-/files/upload/my-files/-/complete" \
  -H "Content-Type: application/json" \
  -d '{"upload_token": "tok_01j5..."}'
```

Returns the registered file:

```json
{
  "ok": true,
  "file": {
    "id": "df-01j5a3b4c5d6e7f8g9h0jkmnpq",
    "filename": "photo.jpg",
    "content_type": "image/jpeg",
    "content_hash": "sha256:...",
    "size": 48210,
    "width": null,
    "height": null,
    "source_slug": "my-files",
    "uploaded_by": null,
    "created_at": "2026-03-13 23:23:24",
    "url": "/-/files/df-01j5a3b4c5d6e7f8g9h0jkmnpq",
    "download_url": "/-/files/df-01j5a3b4c5d6e7f8g9h0jkmnpq/download",
    "thumbnail_url": "/-/files/df-01j5a3b4c5d6e7f8g9h0jkmnpq/thumbnail"
  }
}
```

File IDs use the format `df-{ULID}` — the `df-` prefix makes them recognizable when stored in database columns.

### Deleting files

```bash
curl -X POST "http://localhost:8001/-/files/df-01j5.../-/delete" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Requires `files-delete` permission on the file (or a source-level `files-delete` grant).

Deletion also depends on the storage backend supporting `can_delete`.

### Updating file metadata

```bash
curl -X POST "http://localhost:8001/-/files/df-01j5.../-/update" \
  -H "Content-Type: application/json" \
  -d '{"update": {"search_text": "Annual report 2025"}}'
```

Requires `files-edit` permission on the file (or a source-level `files-edit` grant). Only `search_text` can be updated through this endpoint for now, and the response returns the updated file record.

### Viewing files

Each file has an HTML info page at `/-/files/{file_id}` showing its metadata, a preview (for images), and a download link.

Download the file content directly at `/-/files/{file_id}/download`.

Get file metadata as JSON at `/-/files/{file_id}.json`.

### Searching files

Visit `/-/files/search` to search across all files you have permission to browse. The search page supports full-text search over filenames, content types, and custom search text.

The search endpoint is also available as JSON at `/-/files/search.json?q=query&source=source-slug`.

Each file has an editable `search_text` field (requires `files-edit` permission) that is included in the full-text search index. This can be used to add descriptions, tags, or transcriptions to make files more discoverable.

### Batch metadata

Fetch metadata for multiple files in a single request:

```
GET /-/files/batch.json?id=df-abc123&id=df-def456
```

This returns metadata for all requested files that the current user has permission to browse. This endpoint is used internally by the `render_cell` web component to efficiently load file information for table views.

### Listing sources

View all configured sources and their capabilities:

```
GET /-/files/sources.json
```

This returns each source's `slug`, `storage_type`, and capability flags such as `can_upload`, `can_delete`, `can_list`, `can_generate_signed_urls`, and `requires_proxy_download`.

### Table cell integration

`datasette-files` uses Datasette's [column_types system](https://docs.datasette.io/en/latest/configuration.html#column-types) to decide which columns should be treated as files.

Columns assigned the `file` column type will render `df-...` file IDs as rich file references in Datasette's table and row views. The plugin registers a `file` column type and uses that assignment to replace matching values with a `<datasette-file>` web component that displays the filename, content type, and a thumbnail. Built-in Pillow thumbnails are used for common raster image formats, plugins can register thumbnail generators for any file type, and files with no generated thumbnail fall back to an SVG file-type icon.

The `file` column type is intended for `TEXT` columns. You can assign it in `datasette.yaml` like this:

```yaml
databases:
  mydb:
    tables:
      mytable:
        column_types:
          attachment: file
```

You can also assign it at runtime using Datasette 1.0a26+'s column type UI: open the table page, use the `Column actions` menu for that column, then choose the `file` type. This requires the `set-column-type` permission.

Once a column is assigned the `file` type, store a `df-...` ID returned from the upload endpoint in that column and it will render as a file link automatically. If the column is not assigned the `file` type, Datasette will show the raw `df-...` text instead.

## Endpoint reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/-/files` | Files index page (HTML) |
| `GET` | `/-/files/source/{source_slug}` | Source file listing page, with upload UI if allowed (HTML) |
| `GET` | `/-/files/search` | Search files (HTML) |
| `GET` | `/-/files/search.json?q=&source=` | Search files (JSON) |
| `GET` | `/-/files/sources.json` | List configured sources |
| `GET` | `/-/files/batch.json?id=df-...&id=df-...` | Bulk file metadata |
| `GET` | `/-/files/upload/{source_slug}` | Dedicated upload page (HTML) |
| `POST` | `/-/files/upload/{source_slug}/-/prepare` | Prepare upload (get instructions) |
| `POST` | `/-/files/upload/{source_slug}/-/upload` | Upload file content |
| `POST` | `/-/files/upload/{source_slug}/-/complete` | Complete upload (register file) |
| `POST` | `/-/files/{file_id}/-/delete` | Delete a file |
| `POST` | `/-/files/{file_id}/-/update` | Update file metadata |
| `GET` | `/-/files/{file_id}` | File info page (HTML) |
| `GET` | `/-/files/{file_id}.json` | File metadata (JSON) |
| `GET` | `/-/files/{file_id}/thumbnail` | Generated thumbnail or SVG file-type icon |
| `GET` | `/-/files/{file_id}/download` | Download file content |
| `GET` | `/-/files/import/{file_id}` | CSV import preview page |
| `POST` | `/-/files/import/{file_id}` | Start CSV import job |
| `GET` | `/-/files/import/{file_id}/{import_id}` | Import progress page (HTML) |
| `GET` | `/-/files/import/{file_id}/{import_id}.json` | Import progress (JSON) |

## Python API

Other Datasette plugins can use the `get_file()` function to access files managed by datasette-files.

### `get_file(datasette, file_id)`

Look up a file by its ID and return a `File` object, or `None` if the file was not found.

```python
from datasette_files import get_file

file = await get_file(datasette, "df-01j5a3b4c5d6e7f8g9h0jkmnpq")
if file is None:
    # File not found
    ...
```

The `File` object has the following attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `str` | The file ID |
| `filename` | `str` | Original filename |
| `content_type` | `str` | MIME type |
| `size` | `int` | File size in bytes |
| `source_slug` | `str` | The source this file belongs to |
| `uploaded_by` | `str` or `None` | Actor ID of the uploader |
| `created_at` | `datetime` | UTC timezone-aware datetime of upload |
| `metadata` | `dict` | Arbitrary metadata dict |

### `file.read(max_bytes=None)`

Read file content as bytes. Pass `max_bytes` to limit how much is read — useful to avoid loading very large files into memory.

```python
# Read the entire file
content = await file.read()

# Read at most 1MB
content = await file.read(max_bytes=1_000_000)
```

### `file.open()`

Open the file for streaming reads. Returns an async context manager that yields an async iterator of bytes chunks. Use this for large files where you want to avoid loading the entire content into memory.

```python
async with file.open() as stream:
    async for chunk in stream:
        process(chunk)
```

### Example: using `get_file()` from another plugin

```python
from datasette_files import get_file

async def my_view(datasette, request):
    file = await get_file(datasette, request.args["file_id"])
    if file is None:
        raise NotFound("File not found")

    if file.content_type.startswith("image/"):
        image_bytes = await file.read(max_bytes=20_000_000)
        # Process image...
    elif file.size and file.size > 10_000_000:
        # Stream large files
        async with file.open() as stream:
            async for chunk in stream:
                ...
    else:
        content = await file.read()
        text = content.decode("utf-8")
```

Note: `get_file()` does not perform any permission checks — the calling plugin is responsible for its own authorization.

## Plugin hook: `file_actions`

The `file_actions` hook lets plugins add custom action links to the file info page. These appear in a "File actions" dropdown menu below the filename heading.

### Hook signature

```python
def file_actions(datasette, actor, file, preview_bytes):
    ...
```

| Parameter | Description |
|-----------|-------------|
| `datasette` | The Datasette instance |
| `actor` | The current actor dict (or `None`) |
| `file` | A dict with the file's metadata: `id`, `filename`, `content_type`, `size`, `content_hash`, `source_id`, etc. |
| `preview_bytes` | The first 2048 bytes of the file content (useful for sniffing file type) |

Return a list of dicts, each with:

| Key | Required | Description |
|-----|----------|-------------|
| `href` | Yes | URL the action links to |
| `label` | Yes | Display text for the action |
| `description` | No | Short description shown below the label |

Return an empty list (or `None`) if your plugin has no actions for this file.

The hook can be a regular function or an `async` function.

### Example: add a "Convert to PDF" action for text files

```python
from datasette import hookimpl

@hookimpl
def file_actions(datasette, actor, file, preview_bytes):
    if file["content_type"] and file["content_type"].startswith("text/"):
        return [
            {
                "href": f"/-/convert-pdf/{file['id']}",
                "label": "Convert to PDF",
                "description": "Convert this text file to PDF format",
            }
        ]
    return []
```

### Built-in CSV import action

datasette-files ships with a built-in `file_actions` implementation that adds an "Import as table" action for CSV files. When a file has a `text/csv` content type or a `.csv` filename extension, the dropdown will include a link to `/-/files/import/{file_id}` which provides:

1. A preview page showing detected columns and sample rows
2. A POST endpoint that imports the CSV into a new database table with automatic type detection (integers, floats, and text)
3. A progress page showing import status

Importing requires `files-browse` permission on the file's source **plus** Datasette's `create-table` and `insert-row` permissions on the target database. The import will be rejected if the target table already exists.

## Plugin hook: `register_files_storage_types`

datasette-files uses a plugin hook to allow other Datasette plugins to provide custom storage backends. This is how you would build plugins like `datasette-files-s3` or `datasette-files-gcs`.

### How it works

Your plugin returns a list of `Storage` subclasses (not instances). datasette-files handles instantiation, configuration, and lifecycle management.

```python
from datasette import hookimpl

@hookimpl
def register_files_storage_types(datasette):
    from my_plugin.storage import S3Storage
    return [S3Storage]
```

When a source in `datasette.yaml` references your storage type, datasette-files will:

1. Instantiate your class (calling `S3Storage()`)
2. Call `await storage.configure(config, get_secret)` with the source's config dict
3. Use your storage instance for all file operations on that source

## Plugin hook: `register_thumbnail_generators`

datasette-files uses a second plugin hook to allow plugins to provide thumbnail generators for files. The built-in Pillow generator handles common raster image formats, and other plugins can add generators for PDFs, videos, office documents, or any other file type.

### How it works

Your plugin returns a list of thumbnail generator instances.

```python
from datasette import hookimpl

@hookimpl
def register_thumbnail_generators(datasette):
    from my_plugin.thumbnails import PdfThumbnailGenerator
    return [PdfThumbnailGenerator()]
```

When `/-/files/{file_id}/thumbnail` is requested, datasette-files will:

1. Check the internal thumbnail cache table for an existing thumbnail
2. Ask each registered generator if it can handle the file's `content_type` and `filename`
3. Read the source file once and try matching generators in order
4. Cache the first successful thumbnail result in the internal database
5. Fall back to an SVG file-type icon if no generator returns a thumbnail

The same generation path is also attempted eagerly after uploads complete, so generators can populate the cache before the first thumbnail request.

### The `ThumbnailGenerator` base class

Import the base class and result dataclass from `datasette_files.base`:

```python
from datasette_files.base import ThumbnailGenerator, ThumbnailResult
```

Implement these methods:

```python
class ThumbnailGenerator(ABC):
    name: str

    async def can_generate(self, content_type: str, filename: str) -> bool:
        ...

    async def generate(
        self,
        file_bytes: bytes,
        content_type: str,
        filename: str,
        max_width: int = 200,
        max_height: int = 200,
    ) -> Optional[ThumbnailResult]:
        ...
```

`generate()` returns a `ThumbnailResult` dataclass or `None`:

```python
@dataclass
class ThumbnailResult:
    thumb_bytes: bytes
    content_type: str
    width: int
    height: int
```

- `name`: Short identifier stored alongside generated thumbnails in the cache table
- `can_generate(content_type, filename)`: Return `True` if this generator can handle the file
- `generate(file_bytes, content_type, filename, max_width, max_height)`: Return a `ThumbnailResult` or `None`

### Example: PDF thumbnail generator

```python
from datasette import hookimpl
from datasette_files.base import ThumbnailGenerator, ThumbnailResult


class PdfThumbnailGenerator(ThumbnailGenerator):
    name = "pdf-preview"

    async def can_generate(self, content_type, filename):
        return content_type == "application/pdf" or filename.lower().endswith(".pdf")

    async def generate(
        self, file_bytes, content_type, filename, max_width=200, max_height=200
    ):
        # Render the first page and return PNG or JPEG bytes
        return ThumbnailResult(
            thumb_bytes=thumbnail_bytes,
            content_type="image/png",
            width=width,
            height=height,
        )


@hookimpl
def register_thumbnail_generators(datasette):
    return [PdfThumbnailGenerator()]
```

### The `Storage` base class

Import the base class and supporting dataclasses from `datasette_files.base`:

```python
from datasette_files.base import Storage, StorageCapabilities, FileMetadata
```

#### `StorageCapabilities`

A dataclass declaring what your storage backend supports:

```python
@dataclass
class StorageCapabilities:
    can_upload: bool = False
    can_delete: bool = False
    can_list: bool = False
    can_generate_signed_urls: bool = False
    requires_proxy_download: bool = False
    max_file_size: Optional[int] = None
```

- `can_upload`: The backend can receive file uploads via `receive_upload()`
- `can_delete`: The backend can delete files via `delete_file()`
- `can_list`: The backend can list files via `list_files()`
- `can_generate_signed_urls`: The backend can produce expiring download URLs via `download_url()` — if `True`, file downloads will use a 302 redirect to the signed URL instead of proxying content through Datasette
- `requires_proxy_download`: File content must be proxied through Datasette (e.g. filesystem storage) rather than redirecting to an external URL
- `max_file_size`: Optional maximum file size in bytes (defaults to 100 MB)

#### `FileMetadata`

Returned by several storage methods to describe a file:

```python
@dataclass
class FileMetadata:
    path: str                              # Path within the storage backend
    filename: str                          # Human-readable filename
    content_type: Optional[str] = None     # MIME type
    content_hash: Optional[str] = None     # e.g. "sha256:abcdef..."
    size: Optional[int] = None             # Size in bytes
    width: Optional[int] = None            # Image width in pixels
    height: Optional[int] = None           # Image height in pixels
    created_at: Optional[str] = None
    metadata: dict = field(default_factory=dict)
```

#### Required methods

Every `Storage` subclass must implement these:

**`storage_type`** (property) — A unique string identifier for this storage type, used in source configuration. This is how datasette-files matches a source's `storage: s3` to your class.

```python
@property
def storage_type(self) -> str:
    return "s3"
```

**`capabilities`** (property) — Return a `StorageCapabilities` instance declaring what this backend supports.

```python
@property
def capabilities(self) -> StorageCapabilities:
    return StorageCapabilities(
        can_upload=True,
        can_delete=True,
        can_generate_signed_urls=True,
    )
```

**`configure(config, get_secret)`** — Called once at startup with the source's `config` dict from `datasette.yaml` and a `get_secret` callable for retrieving secrets from `datasette-secrets`.

```python
async def configure(self, config: dict, get_secret) -> None:
    self.bucket = config["bucket"]
    self.prefix = config.get("prefix", "")
    self.region = config.get("region", "us-east-1")
```

**`get_file_metadata(path)`** — Return a `FileMetadata` for the given path, or `None` if the file doesn't exist.

```python
async def get_file_metadata(self, path: str) -> Optional[FileMetadata]:
    # Check if the file exists in your backend and return its metadata
    ...
```

**`read_file(path)`** — Return the full content of a file as bytes. Raise `FileNotFoundError` if missing.

```python
async def read_file(self, path: str) -> bytes:
    # Read and return the file content
    ...
```

#### Optional methods

Override these based on the capabilities you declared:

**`receive_upload(path, stream, content_type)`** — Store file content streamed as chunks. `stream` is an `AsyncIterator[bytes]` — consume it incrementally to avoid buffering the entire file in memory. Return a `FileMetadata` with at least the `content_hash` and `size` populated. Required if `can_upload` is `True`.

```python
async def receive_upload(self, path: str, stream: AsyncIterator[bytes], content_type: str) -> FileMetadata:
    # Consume stream chunks, store the file, and return metadata
    sha256 = hashlib.sha256()
    size = 0
    async for chunk in stream:
        # write chunk to storage
        sha256.update(chunk)
        size += len(chunk)
    ...
```

**`delete_file(path)`** — Delete a file. Required if `can_delete` is `True`.

**`list_files(prefix, cursor, limit)`** — List files, returning `(files, next_cursor)`. Required if `can_list` is `True`.

**`download_url(path, expires_in)`** — Return a signed/expiring download URL. Required if `can_generate_signed_urls` is `True`.

**`read_bytes(path, num_bytes)`** — Return up to `num_bytes` from the start of a file. The default implementation reads the full file with `read_file()` and slices it. Storage backends should override this to avoid downloading entire files — for example, S3 backends can use an HTTP `Range` header to fetch only the requested bytes. Used by the file info page to provide `preview_bytes` to `file_actions` hooks.

**`stream_file(path)`** — Yield file content in chunks as an async iterator. This method is used by the file download endpoint to stream files to clients without loading the entire file into memory. The default implementation reads the entire file with `read_file()` and yields it as a single chunk — storage backends should override this to yield smaller chunks for efficient memory usage with large files.

### Full example: S3 storage plugin

Here's a complete example of what a `datasette-files-s3` plugin would look like:

```python
# datasette_files_s3/__init__.py
from datasette import hookimpl
from datasette_files.base import Storage, StorageCapabilities, FileMetadata
import boto3
import hashlib
from typing import Optional


class S3Storage(Storage):
    storage_type = "s3"
    capabilities = StorageCapabilities(
        can_upload=True,
        can_delete=True,
        can_list=True,
        can_generate_signed_urls=True,
        requires_proxy_download=False,
    )

    async def configure(self, config: dict, get_secret) -> None:
        self.bucket = config["bucket"]
        self.prefix = config.get("prefix", "")
        self.region = config.get("region", "us-east-1")
        self.client = boto3.client("s3", region_name=self.region)

    def _key(self, path: str) -> str:
        return f"{self.prefix}{path}" if self.prefix else path

    async def get_file_metadata(self, path: str) -> Optional[FileMetadata]:
        try:
            resp = self.client.head_object(
                Bucket=self.bucket, Key=self._key(path)
            )
            return FileMetadata(
                path=path,
                filename=path.split("/")[-1],
                content_type=resp.get("ContentType"),
                size=resp.get("ContentLength"),
            )
        except self.client.exceptions.ClientError:
            return None

    async def read_file(self, path: str) -> bytes:
        resp = self.client.get_object(
            Bucket=self.bucket, Key=self._key(path)
        )
        return resp["Body"].read()

    async def read_bytes(self, path: str, num_bytes: int = 2048) -> bytes:
        resp = self.client.get_object(
            Bucket=self.bucket,
            Key=self._key(path),
            Range=f"bytes=0-{num_bytes - 1}",
        )
        return resp["Body"].read()

    async def stream_file(self, path: str):
        resp = self.client.get_object(
            Bucket=self.bucket, Key=self._key(path)
        )
        for chunk in resp["Body"].iter_chunks(chunk_size=65536):
            yield chunk

    async def receive_upload(
        self, path: str, stream, content_type: str
    ) -> FileMetadata:
        # Collect chunks, computing hash incrementally
        chunks = []
        sha256 = hashlib.sha256()
        size = 0
        async for chunk in stream:
            chunks.append(chunk)
            sha256.update(chunk)
            size += len(chunk)
        content = b"".join(chunks)
        self.client.put_object(
            Bucket=self.bucket,
            Key=self._key(path),
            Body=content,
            ContentType=content_type,
        )
        return FileMetadata(
            path=path,
            filename=path.split("/")[-1],
            content_type=content_type,
            content_hash="sha256:" + sha256.hexdigest(),
            size=size,
        )

    async def download_url(self, path: str, expires_in: int = 300) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": self._key(path)},
            ExpiresIn=expires_in,
        )

    async def delete_file(self, path: str) -> None:
        self.client.delete_object(
            Bucket=self.bucket, Key=self._key(path)
        )

    async def list_files(
        self, prefix: str = "", cursor: Optional[str] = None, limit: int = 100
    ) -> tuple[list[FileMetadata], Optional[str]]:
        kwargs = {
            "Bucket": self.bucket,
            "Prefix": self._key(prefix),
            "MaxKeys": limit,
        }
        if cursor:
            kwargs["ContinuationToken"] = cursor
        resp = self.client.list_objects_v2(**kwargs)
        files = [
            FileMetadata(
                path=obj["Key"].removeprefix(self.prefix),
                filename=obj["Key"].split("/")[-1],
                size=obj["Size"],
            )
            for obj in resp.get("Contents", [])
        ]
        next_cursor = resp.get("NextContinuationToken")
        return files, next_cursor


@hookimpl
def register_files_storage_types(datasette):
    return [S3Storage]
```

The plugin's `pyproject.toml` would register itself as a Datasette plugin:

```toml
[project.entry-points.datasette]
files_s3 = "datasette_files_s3"
```

Then configure it in `datasette.yaml`:

```yaml
plugins:
  datasette-files:
    sources:
      product-images:
        storage: s3
        config:
          bucket: my-photos-bucket
          prefix: "uploads/"
          region: us-west-2
```

### Built-in filesystem storage reference

The built-in `FilesystemStorage` stores files on the local filesystem. It supports upload, delete, and listing but does not support signed URLs — file downloads are proxied through Datasette.

**Configuration options:**

| Key | Required | Description |
|-----|----------|-------------|
| `root` | Yes | Absolute path to the directory where files are stored |
| `max_file_size` | No | Maximum upload size in bytes (defaults to 100 MB) |

**Capabilities:**

| Capability | Value |
|-----------|-------|
| `can_upload` | `True` |
| `can_delete` | `True` |
| `can_list` | `True` |
| `can_generate_signed_urls` | `False` |
| `requires_proxy_download` | `True` |

## Development

To set up this plugin locally, first checkout the code. Run the tests with `uv`:
```bash
cd datasette-files
uv run pytest
```

Recommendation to run a test server:
```bash
./dev-server.sh
```
