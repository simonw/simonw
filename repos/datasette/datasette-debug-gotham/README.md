# datasette-debug-gotham

[![PyPI](https://img.shields.io/pypi/v/datasette-debug-gotham.svg)](https://pypi.org/project/datasette-debug-gotham/)
[![Changelog](https://img.shields.io/github/v/release/datasette/datasette-debug-gotham?include_prereleases&label=changelog)](https://github.com/datasette/datasette-debug-gotham/releases)
[![Tests](https://github.com/datasette/datasette-debug-gotham/actions/workflows/test.yml/badge.svg)](https://github.com/datasette/datasette-debug-gotham/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/datasette/datasette-debug-gotham/blob/main/LICENSE)

A debugging utility for testing actor permissions/actions with DC Superheros (superman, Batman, Daily Planet, etc.)

It can be hard to test or debug Datasette plugins that use the new permissions system. This plugin offers a few builtin actors and a small widget for switching between actors:

![](https://private-user-images.githubusercontent.com/15178711/565209545-6e760b88-1c8a-43b9-a186-6af5543e3eca.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzM3OTI4NTIsIm5iZiI6MTc3Mzc5MjU1MiwicGF0aCI6Ii8xNTE3ODcxMS81NjUyMDk1NDUtNmU3NjBiODgtMWM4YS00M2I5LWExODYtNmFmNTU0M2UzZWNhLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAzMTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMzE4VDAwMDkxMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTJiMzNmZGMwYjVmM2VmODRjZjRlODhhMDA5NGM0YzllYzhjMzc5MTc2NzUxNDY1YmMwMWEwODFjNTkyNTI5MDAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.TZqLS5Xp8QGbRwaaJ9kv5LmHrovOZdNFutHKju6zT2s)

Once you select an actor like "Clark Kent" or "Bruce Wayne", the page will refresh and Datasette will recognize the actor in `request.actor`. You can change actors however you like:


![](https://private-user-images.githubusercontent.com/15178711/565209598-0853e911-bd89-46c5-9bbe-270626a482de.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzM3OTI4NjYsIm5iZiI6MTc3Mzc5MjU2NiwicGF0aCI6Ii8xNTE3ODcxMS81NjUyMDk1OTgtMDg1M2U5MTEtYmQ4OS00NmM1LTliYmUtMjcwNjI2YTQ4MmRlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAzMTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMzE4VDAwMDkyNlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWY3ZDZlYzIzODJjMDQwOGIyZTYyZjc4YjEyMTYxM2RkMGM4N2ZhYTQ5ZGVhYjMxMzhhM2JhNTU3NTA0YWZkNzEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.Ym3sgnkoIXgA8Z8K48cxFInkeyETISx7o8wjP7lGh-s)

The pre-configured actors have some attributes you can use for debugging or "group permissions":

```python
# https://github.com/datasette/datasette-debug-gotham/blob/main/datasette_debug_gotham/__init__.py#L8-L21
ACTORS = {
    ###### DAILY PLANET ######
    "clark": {
        "id": "clark",
        "name": "Clark Kent",
        "newsroom": "daily-planet",
        "profile_picture_url": pfp("C", bg="blue"),
    },
    "lois": {
        "id": "lois",
        "name": "Lois Lane",
        "newsroom": "daily-planet",
        "profile_picture_url": pfp("L", bg="red"),
    },
    ... # many more
}
```

Or access the actors with Python:

```python
from dataseette_debug_gotham import ACTORS
print(ACTORS["clark"])
```


Personally I use this with `uv` for dynamic permissions testing:

```bash
uvx \
  --from 'datasette>=1a' \
  --with datasette-debug-gotham \
  datasette \
    --default-deny \
    -s permissions.view-instance.newsroom daily-planet \
    --memory
```

Here `--default-deny` means that by default everyone will see a `Forbidden view-instance` error when visiting dataset.

But, if you use the debug widget and select `clark`/`lois`/`jimmy`, since they have `newsroom: daily-planet` in their actor config, they will be able to see the instance!

And if you change to `bruce`/`alfred`/`selina`, who have `newsroom: gotham-gazette`, they will be blocked!