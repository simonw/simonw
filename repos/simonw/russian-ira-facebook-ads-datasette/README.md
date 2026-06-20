# Converting irads JSON to Datasette

The House Intelligence Committee released 3,517 Facebook ads that were
reported to have been bought by the Russian Internet Research Agency as a set
of redacted PDF files.

Companion blog post: [Analyzing US Election Russian Facebook Ads](https://simonwillison.net/2018/Aug/6/russian-facebook-ads/)

Ed Summers wrote a parser that converts those PDFs into a JSON file:
https://github.com/umd-mith/irads

The script in this repository downloads that JSON file and converts it into a
SQLite database for use with Datasette. Use it like this:

    pip3 install sqlite-utils
    python3 fetch_and_build_russian_ads.py \
        https://raw.githubusercontent.com/umd-mith/irads/master/site/index.json \
        russian-ads.db

This will produce a SQLite database called `ads.db`. You can then explore it
locally with [Datasette](https://github.com/simonw/datasette) like so:

    pip3 install datasette
    datasette ads.db

To see the full customized interface you will need to install a custom branch of
Datasette plus a custom Datasette plugin. See the Dockerfile, or do this:

    pip3 install https://github.com/simonw/datasette/archive/filter-plugin-hook.zip
    pip3 install datasette-json-html pyyaml
    python3 build_metadata.py
    datasette russian-ads.db \
      -m russian-ads-metadata.json \
      --config default_page_size:50 --config sql_time_limit_ms:3000 \
      --config num_sql_threads:10 --config facet_time_limit_ms:3000 \
      --config allow_sql:off --config force_https_urls:1 \
      --plugins-dir=plugins --static static:static
