# scrape-github-actions-package-versions

[Git scraper](https://simonwillison.net/2020/Oct/9/git-scraping/) recording the package versions installed on the defaul GitHub Actions ubuntu-latest worker

Once a day this repo runs the following command:

    apt list --installed > ubuntu-latest-installed.txt

And commits any changes back to the repository.
