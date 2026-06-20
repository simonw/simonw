# datasette-remote-actors

[![PyPI](https://img.shields.io/pypi/v/datasette-remote-actors.svg)](https://pypi.org/project/datasette-remote-actors/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-remote-actors?include_prereleases&label=changelog)](https://github.com/datasette/datasette-remote-actors/releases)
[![Test](https://github.com/datasette/datasette-remote-actors/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-remote-actors/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-remote-actors/blob/main/LICENSE)

A Datasette plugin for fetching details of actors (users or API clients) from a remote, centralized JSON endpoint.

See [Datasette issue #2180](https://github.com/simonw/datasette/issues/2180) for background on this plugin.

## Installation

```bash
datasette install datasette-remote-actors
```

## API Endpoint Requirements

Configure this plugin with a URL pointing to an API endpoint that provides actor information.

This endpoint **must**:

1. Accept a GET request.
2. Accept a query string parameter `ids` containing a comma-separated list of actor IDs (e.g., `?ids=1,a2,b3`).
3. Return a JSON response with a `200 OK` status code upon success.
4. The JSON response body **must** be a dictionary where the keys are the **string representations** of the actor IDs requested, and the values are dictionaries containing the details for each actor.

**Example Request:**

`GET /path/to/your/endpoint?ids=1,2`

**Example Successful JSON Response:**

```json
{
  "1": {
    "id": "1",
    "name": "Cleopatra",
    "email": "cleo@example.com"
  },
  "2": {
    "id": 2,
    "name": "Julius Caesar",
    "username": "jcaesar"
  }
}
```

**Important Notes:**

* The **keys** in the returned JSON object (`"1"`, `"2"` in the example) **must be strings**, even if the original IDs are integers.
* Each actor dictionary value **must** contain an `id` field, which can be a string or an integer matching the requested ID. Other fields (like `name`, `username`, `email`) are flexible and defined by your endpoint.
* **Small Actor Sets:** If you have a small, fixed number of actors, your endpoint can optionally ignore the `?ids=` parameter and always return the *entire* dictionary of all known actors. The plugin will cache these and use the cached data for subsequent lookups (if `ttl` is configured).
* **Error Handling:** If the remote endpoint returns a non-200 status code, times out, or returns invalid JSON, this plugin will log an error (if Datasette logging is configured) and will not return actor data for the requested IDs for that request.

## Configuration

You configure the plugin using Datasette's `metadata.json` or `metadata.yaml` file.

**Minimal Configuration:**

```yaml
plugins:
  datasette-remote-actors:
    url: https://example.com/actors.json
```

**Full Configuration Example:**

```yaml
plugins:
  datasette-remote-actors:
    # (Required) URL to the remote actor endpoint
    url: https://example.com/actors.json

    # (Optional) Cache Time-To-Live in seconds.
    # If set, actor details will be cached in memory.
    # Uses cachetools.TTLCache with a default maxsize of 1000.
    # Omit for no caching.
    ttl: 60

    # (Optional) Bearer token for authentication.
    # If set, adds an "Authorization: Bearer <token>" header to the request.
    token: your-secret-api-token

    # (Optional) Enable integration with datasette-profiles.
    # Requires datasette-profiles plugin to be installed.
    # See section below for details.
    datasette-profiles: true
```

**Configuration Options:**

* `url` (string, **required**): The URL to the endpoint that can resolve actor IDs into JSON actor dictionaries.
* `ttl` (integer, optional): The number of seconds to cache the result for a specific actor ID. Uses an in-memory `TTLCache` (default `maxsize=1000`). Omit this or set to `0` for no caching.
* `token` (string, optional): An authentication token. If provided, it will be sent in the `Authorization: Bearer <token>` HTTP header when calling the `url`.
* `datasette-profiles` (boolean, optional): Set to `true` to enable integration with the [datasette-profiles](https://github.com/datasette/datasette-profiles) plugin. Defaults to `false`.

## Integration with datasette-profiles

If you want to allow users to override or supplement the actor details fetched from the remote endpoint with their own profile information stored within Datasette, you can use the [datasette-profiles](https://github.com/datasette/datasette-profiles) plugin.

1.  Install the companion plugin:
    ```bash
    datasette install datasette-profiles
    ```
2.  Enable the integration in the `datasette-remote-actors` configuration:
    ```yaml
    plugins:
      datasette-remote-actors:
        url: https://example.com/actors.json
        datasette-profiles: true
        # other options...
    ```

When enabled:

* The plugin will first fetch actor details from the configured `url`.
* It will then query the `profiles` table (created by `datasette-profiles`) in Datasette's internal database for matching actor IDs.
* If a profile exists for an actor ID, the data from the `profiles` table will be merged into the actor dictionary fetched from the remote URL. Any non-null values in the `profiles` table (except the `id` column itself) will overwrite corresponding keys from the remote data.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd datasette-remote-actors
python3 -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install -e '.[test]'
```

To run the tests:

```bash
pytest
```
