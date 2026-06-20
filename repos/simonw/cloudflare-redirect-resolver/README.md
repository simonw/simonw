# Cloudflare Redirect Resolver

A small Cloudflare Worker that serves an HTML form, accepts a URL, follows up to 10 HTTP redirects with `GET`, and reports the full redirect chain plus the eventual location.

The Worker uses `redirect: "manual"` and cancels each response body as soon as headers are available, so it does not intentionally download page content.

Built by Codex Desktop and GPT-5.5 xhigh. [Full codex transcript](https://gist.github.com/simonw/264bd6b8a39fc34c91c9c867454c64b9).

Initial prompt:

> Build a cloudflare worker app I can deploy using wrangler which provides an HTML form where I can paste a URL, it then follows redirects on that URL up to 10 times to report back the full redirect chain and the eventual location. It does this with HTTP GET that it cuts off as soon as headers have all come back.

## Local Development

```bash
npm install
npm run dev
```

Open the local Wrangler URL, paste a URL, and submit the form.

## Deploy

```bash
npm run deploy
```

Or you can deploy a version that will work [for 60 minutes for free](https://blog.cloudflare.com/temporary-accounts/) without even creating a Cloudflare account using:

```bash
npx wrangler deploy --temporary
```

## JSON API

You can also call:

```text
/api/resolve?url=https%3A%2F%2Fexample.com
```

The JSON response contains `chain`, `finalUrl`, `redirectCount`, and any terminal error, for example:
```json
{
  "inputUrl": "http://google.com/",
  "finalUrl": "http://www.google.com/",
  "redirectCount": 1,
  "reachedLimit": false,
  "chain": [
    {
      "url": "http://google.com/",
      "status": 301,
      "statusText": "Moved Permanently",
      "location": "http://www.google.com/",
      "resolvedLocation": "http://www.google.com/"
    },
    {
      "url": "http://www.google.com/",
      "status": 200,
      "statusText": "OK",
      "location": null,
      "resolvedLocation": null
    }
  ],
  "terminalStatus": 200,
  "terminalStatusText": "OK",
  "error": null
}
```
