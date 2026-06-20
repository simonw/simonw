# Big Opportunities in Small Data

This is the handout for my keynote at [Citus Con 2023](https://www.citusdata.com/cituscon/2023/)

- https://datasette.io/ is the Datasette homepage
- https://datasette.io/plugins lists all of the plugins

## City Facilities

Here's the City Facilities data for San Francisco I used:

- https://data.sfgov.org/City-Infrastructure/City-Facilities/nc68-ngbr

I imported it into https://datasette.cloud/ with the https://datasette.io/plugins/datasette-socrata plugin and visualized it with https://datasette.io/plugins/datasette-cluster-map

## Read-only SQL queries

- https://simonwillison.net/ is my blog
- https://simonw.substack.com/ is my newsletter
- https://datasette.simonwillison.net/ is my Datasette backup of my blog
- https://observablehq.com/@simonw/blog-to-newsletter is the Observable notebook
- https://simonwillison.net/2023/Apr/4/substack-observable/ describes how it works in detail

## Baked Data

I wrote more about the Baked Data pattern here:

- https://simonwillison.net/2021/Jul/28/baked-data/

## SQL as an integration language

For the Niche Museums Atom demo:

- https://www.niche-museums.com/
- The Atom feed is defined by https://www.niche-museums.com/browse/feed
- I return it as Atom using https://datasette.io/plugins/datasette-atom
- Another similar plugin is https://datasette.io/plugins/datasette-ics

## Datasette Lite

- https://lite.datasette.io/
- https://data.together.xyz/redpajama-data-1T/v1.0.0/urls.txt is the training data
- https://gist.github.com/simonw/73d15c0dd1025d1196829740bacf4464 as JSON
- Loaded into Datasette Lite: https://lite.datasette.io/?json=https://gist.github.com/simonw/73d15c0dd1025d1196829740bacf4464#/data/raw?_facet=top_folders
- More about Datasette Lite: https://simonwillison.net/2022/May/4/datasette-lite/
- Crunchy Data PostgreSQL tutorial (with PostgreSQL as WebAssembly): https://www.crunchydata.com/developers/playground/basics-of-postgis
- How they built that: https://www.crunchydata.com/blog/crazy-idea-to-postgres-in-the-web-browser
