# help-scraper

[![Scrape latest help](https://github.com/simonw/help-scraper/actions/workflows/scrape.yml/badge.svg)](https://github.com/simonw/help-scraper/actions/workflows/scrape.yml)

Record a history of `--help` for various commands

See [Help scraping: track changes to CLI tools by recording their --help using Git](https://simonwillison.net/2022/Feb/2/help-scraping/) for the background of this project.

This repository installs tools and records the output of their `--help` commands, to track changes made to them over time.

- [flyctl/](flyctl/) - the [flyctl](https://github.com/superfly/flyctl/) management tool by [Fly.io](https://fly.io/)
- [aws/](aws/) - the Amazon Web Services [CLI interface](https://aws.amazon.com/cli/)
- [azure/](azure/) - the Azure [CLI tool](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli). Scraper contributed by [@techknowlogick](https://github.com/techknowlogick).
- [vercel/](vercel/) - the `vercel` management tool by [Vercel](https://vercel.com/)
- [sqlite3-help.md](sqlite3-help.md) - the output of `.help` in the `sqlite3` CLI tool

The repo also tracks changes made to some GraphQL schemas:

- [flyctl/fly.graphql](flyctl/fly.graphql) ([history](https://github.com/simonw/help-scraper/commits/main/flyctl/fly.graphql)) for `https://api.fly.io/graphql`
- [github/github.graphql](github/github.graphql) ([history](https://github.com/simonw/help-scraper/commits/main/github/github.graphql)) for `https://api.github.com/graphql`

## More help scrapers

- Jason Hall has a help scraper for the `gcloud` CLI tool at https://github.com/imjasonh/gcloud-help
- Michael Warkentin has a help scraper for the `sentry-cli` CLI tool at https://github.com/mwarkentin/sentry-cli-help
