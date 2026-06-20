# sf-tree-history

Tracking the history of trees in San Francisco.

Background: [Generating a commit log for San Francisco’s official list of trees](https://simonwillison.net/2019/Mar/13/tree-history/). See also [Git Scraping](https://simonwillison.net/2020/Oct/9/git-scraping/) for a description of the general technique.

This repository [uses GitHub Actions](https://github.com/simonw/sf-tree-history/actions) to retrieve the [official CSV file of trees in San Francisco](https://data.sfgov.org/City-Infrastructure/Street-Tree-List/tkzw-k3nq) once a day and track any changes to it over time using the git commit history.

It uses [csv-diff](https://github.com/simonw/csv-diff) to generate human-readable commit messages.

You can see recent changes to the CSV file here: https://github.com/simonw/sf-tree-history/commits/main
