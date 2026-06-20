# chonkers-alert

Sightings of Chonkers — the very large Steller sea lion currently hanging
out at Pier 39 in San Francisco — scraped from iNaturalist.

- **Webpage**: https://simonw.github.io/chonkers-alert/
- **Atom feed**: https://simonw.github.io/chonkers-alert/atom.xml

## How it works

A GitHub Actions workflow runs once daily at 22:15 UTC (and on push / manual
dispatch) and:

1. Calls the [iNaturalist API](https://api.inaturalist.org/v1/observations)
   for Steller sea lion (*Eumetopias jubatus*, taxon `41755`) observations
   with `quality_grade=research` inside the SF waterfront bounding box
   (`37.795,-122.420 → 37.815,-122.388`).
2. Saves the pretty-printed JSON to this repo (so the commit history
   doubles as a sightings log).
3. Renders `index.html` (most recent sightings first, with photos) and
   `atom.xml` and deploys both to GitHub Pages.

## Files

- `scrape.sh` — calls `download.sh` with the API URL.
- `download.sh` — fetches the URL, pretty-prints + filters JSON with `jq`,
  saves to a filename derived from the URL.
- `to_atom.py` — JSON → Atom feed (stdlib only).
- `to_html.py` — JSON → static `index.html` (stdlib only).
- `.github/workflows/scrape.yml` — the scheduled workflow.

## Running locally

```bash
./scrape.sh
mkdir -p _site
cat *.json | python3 to_atom.py > _site/atom.xml
cat *.json | python3 to_html.py > _site/index.html
```

Open `_site/index.html` in a browser.

Inspired by
[simonw/recent-california-brown-pelicans](https://github.com/simonw/recent-california-brown-pelicans).
