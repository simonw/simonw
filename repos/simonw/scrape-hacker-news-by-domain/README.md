# scrape-hacker-news-by-domain

Scrape HN to track links from specific domains

See [Scraping web pages from the command-line with shot-scraper](https://simonwillison.net/2022/Mar/14/scraping-web-pages-shot-scraper/) for details of how this works.

Recently scraped data from this repo is also published to this Datasette table:

https://simon.datasette.cloud/data/hacker_news_posts?_sort_desc=dt

More about how that works in [Datasette’s new JSON write API: The first alpha of Datasette 1.0](https://simonwillison.net/2022/Dec/2/datasette-write-api/).

## Analysis with git-history

To analyze data over time from the commit logs, run [git-history](https://github.com/simonw/git-history) like this:
```bash
uvx git-history file --repo https://github.com/simonw/scrape-hacker-news-by-domain \
  hacker-news.db simonwillison-net.json --id id
```
Then open in [Datasette](https://datasette.io/):
```bash
uvx datasette data.db
```
This is an interesting starting point:

    http://127.0.0.1:8001/data/item?_facet=submitter&_facet_date=dt&dt__gte=2025&_sort_desc=dt

This one helps filter for rows where a column was changed beyond the first version:

    /data/item_changed?_facet=column&_where=item_version+not+in+(select+_id+from+item_version+where+_version+%3D+1)

