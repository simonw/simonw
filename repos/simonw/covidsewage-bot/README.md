# covidsewage-bot

- [@covidsewage@simonwillison.net](https://fedi.simonwillison.net/@covidsewage) on Mastodon
- [@covidsewage](https://twitter.com/covidsewage) on Twitter, which is no longer updated.

Posts a daily image of the charts from the County of Santa Clara [SARS-CoV-2 Sewage Monitoring Data](https://covid19.sccgov.org/dashboard-wastewater).

Background on this project:

- [Building a Covid sewage Twitter bot](https://simonwillison.net/2022/Apr/18/covid-sewage/)
- [Building Mastodon bots with GitHub Actions and toot](https://til.simonwillison.net/mastodon/mastodon-bots-github-actions)

## How it works

The bot runs using [scheduled GitHub Actions workflows](https://github.com/simonw/covidsewage-bot/tree/main/.github/workflows).

It uses these three tools:

- [shot-scraper](https://datasette.io/tools/shot-scraper) to take the screenshot
- [tweet-images](https://github.com/simonw/tweet-images) to send the tweet
- [toot](https://toot.readthedocs.io/) to post to Mastodon

I wrote notes on [how to get credentials for a Twitter bot](https://til.simonwillison.net/twitter/credentials-twitter-bot).
