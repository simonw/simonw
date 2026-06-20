# git-scraper-template

Template repository for setting up a new [Git scraper](https://simonwillison.net/2020/Oct/9/git-scraping/) using GitHub Actions.

## How to use this

Visit https://github.com/simonw/git-scraper-template/generate

Pick a name for your new repository, then paste **the URL** of the page you would like to take scrape into the **description field** (including the `http://` or `https://`). JSON works best, but any URL will be fetched and saved.

Then click **Create repository from template**.

Your new repository will be created, and a script will run which will do the following:

- Add a `scrape.sh` script to your repository which uses `curl` via the `./download.sh` script to fetch and save the URL you requested
- Run that `./scrape.sh` command and commit the result to the repository
- Configure a schedule to run this script once every 24 hours

You can edit `scrape.sh` to customize what is scraped, and you can edit `.github/workflows/scrape.yml` to change how often the scraping happens.

If you want to use Python in your scraper you can uncomment the relevant block in `scrape.yml` and add a `requirements.txt` file to your repository containing any dependencies you need.
