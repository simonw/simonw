# datasette-cors

[![PyPI](https://img.shields.io/pypi/v/datasette-cors.svg)](https://pypi.org/project/datasette-cors/)
[![Tests](https://github.com/simonw/datasette-cors/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/datasette-cors/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-cors?include_prereleases&label=changelog)](https://github.com/simonw/datasette-cors/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-cors/blob/main/LICENSE)

Datasette plugin for configuring CORS headers, based on [asgi-cors](https://github.com/simonw/asgi-cors).

You can use this plugin to allow JavaScript running on an allowlisted set of domains to make `fetch()` calls to the JSON API provided by your Datasette instance.

## Installation
```bash
datasette install datasette-cors
```
## Configuration

You need to add some plugin configuration for this plugin to take effect.

To allowlist specific domains, use this:

```json
{
    "plugins": {
        "datasette-cors": {
            "hosts": ["https://www.example.com"]
        }
    }
}
```
This affects the `access-control-allow-origin` header.

You can also allowlist host patterns like this:

```json
{
    "plugins": {
        "datasette-cors": {
            "host_wildcards": ["https://*.example.com"]
        }
    }
}
```

To allow all origins, use:

```json
{
    "plugins": {
        "datasette-cors": {
            "allow_all": true
        }
    }
}
```
This sets the `access-control-allow-origin` header to `*`.

You can specify allowed headers - with the `access-control-allow-headers` header - using the `headers` option:

```json
{
    "plugins": {
        "datasette-cors": {
            "allow_all": true,
            "headers": ["Authorization", "Content-Type"]
        }
    }
}
```

To allow specific HTTP methods with the `access-control-allow-methods` header, use the `methods` option:

```json
{
    "plugins": {
        "datasette-cors": {
            "allow_all": true,
            "methods": ["GET", "POST", "OPTIONS"]
        }
    }
}
```

You can set the `access-control-max-age` header using the `max_age` option:

```json
{
    "plugins": {
        "datasette-cors": {
            "allow_all": true,
            "max_age": 3600
        }
    }
}
```

## Testing it

To test this plugin out, run it locally by saving one of the above examples as `metadata.json` and running this:
```bash
datasette -m metadata.json
```
With Datasette 1.0 use `-c config.json` instead, or try this:
```bash
datasette -s plugins.datasette-cors.allow_all true
```

Now visit https://www.example.com/ in your browser, open the browser developer console and paste in the following:

```javascript
fetch("http://127.0.0.1:8001/_memory.json?sql=select+sqlite_version%28%29").then(r => r.json()).then(console.log)
```

If the plugin is working correctly, you will see the JSON response output to the console.
