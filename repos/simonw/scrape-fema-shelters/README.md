# scrape-fema-shelters

A [Git scraper](https://simonwillison.net/2020/Oct/9/git-scraping/) tracking the official feed of FEMA emergency shelters.

To convert this to SQLite using [git-history](https://github.com/simonw/git-history):

```bash
git-history file fema.db fema-shelters.json --convert '
geojson = json.loads(content)
for feature in geojson["features"]:
    yield feature["properties"]
' --ignore objectid --id SHELTER_ID
```
