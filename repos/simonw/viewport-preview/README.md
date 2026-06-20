# viewport-preview

A tool for previewing a web page in a number of different viewport widths, using iframes.

Hosted here: https://viewport-preview.simonwillison.net/

Add the URL to the page to preview as the `?url=` parameter, for example:

- https://viewport-preview.simonwillison.net/?url=https%3A%2F%2Fwww.example.com%2F

The supported widths and devices are taken from the table on this page: [Adobe Experience League: Mobile viewports for responsive experiences](https://experienceleague.adobe.com/docs/target/using/experiences/vec/mobile-viewports.html).

## Scraping the sizes

I generated the JSON data structure in `index.html` that lists the different widths and device names by scraping the Adobe page using Pandas like this:


```python
import pandas as pd
import json

tables = pd.read_html(
    "https://experienceleague.adobe.com/docs/target/using/experiences/vec/mobile-viewports.html"
)
table = tables[0]
table["w"] = (
    table["Viewport Size (width x height)"]
    .str.replace("w", "")
    .str.split(" x ")
    .str[0]
    .astype(int)
)

by_widths = {}
for index, row in table.iterrows():
    width = row["w"]
    device = row["Device"]
    by_widths.setdefault(width, []).append(device)

print(json.dumps(sorted(by_widths.items()), indent=2))
```

I had to `pip install pandas lxml` before running this.
