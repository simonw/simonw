# puppeteer-screenshot

Vercel app for taking screenshots of web pages using Puppeteer

Original code by [@styfle](https://github.com/styfle) in [this pull request](https://github.com/vercel/now-examples/pull/207).

I upgraded the code to work with the latest Vercel and added a `?key=` mechanism to protect it from unauthorized access.

## Usage

Set a Vercel secret called `SECRET_KEY` with a random string in it (I generated mine by running `uuidgen | md5`), then deploy.

You can access screenshots for pages using:

    https:/.../zeit.co/blog?type=png&key=...

Screenshots can take several seconds to generate so it's a good idea to cache them somewhere.

## Querystring arguments

- `?viewportWidth=` sets the browser viewport width in pixels. This defaults to 800.
- `?viewportHeight=` sets the browser viewport height in pixels. This defaults to 600.
- `?type=` set the output type to `png` or `jpeg`. Default is `png`.
- `?quality=75` set the JPEG output qualit. Ignored for PNG.
- `?fullPage=true` fetch a screenshot of the full page, not just the browser viewport.