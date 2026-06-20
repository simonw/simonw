# datasette-sqlite-fts4

[![PyPI](https://img.shields.io/pypi/v/datasette-sqlite-fts4.svg)](https://pypi.org/project/datasette-sqlite-fts4/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-sqlite-fts4?include_prereleases&label=changelog)](https://github.com/simonw/datasette-sqlite-fts4/releases)
[![Tests](https://github.com/simonw/datasette-sqlite-fts4/workflows/Test/badge.svg)](https://github.com/simonw/datasette-sqlite-fts4/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-sqlite-fts4/blob/main/LICENSE)

Datasette plugin that exposes the custom SQL functions from [sqlite-fts4](https://github.com/simonw/sqlite-fts4).

[Interactive demo](https://datasette-sqlite-fts4.datasette.io/24ways-fts4?sql=select%0D%0A++++json_object%28%0D%0A++++++++"label"%2C+articles.title%2C+"href"%2C+articles.url%0D%0A++++%29+as+article%2C%0D%0A++++articles.author%2C%0D%0A++++rank_score%28matchinfo%28articles_fts%2C+"pcx"%29%29+as+score%2C%0D%0A++++rank_bm25%28matchinfo%28articles_fts%2C+"pcnalx"%29%29+as+bm25%2C%0D%0A++++json_object%28%0D%0A++++++++"pre"%2C+annotate_matchinfo%28matchinfo%28articles_fts%2C+"pcxnalyb"%29%2C+"pcxnalyb"%29%0D%0A++++%29+as+annotated_matchinfo%2C%0D%0A++++matchinfo%28articles_fts%2C+"pcxnalyb"%29+as+matchinfo%2C%0D%0A++++decode_matchinfo%28matchinfo%28articles_fts%2C+"pcxnalyb"%29%29+as+decoded_matchinfo%0D%0Afrom%0D%0A++++articles_fts+join+articles+on+articles.rowid+%3D+articles_fts.rowid%0D%0Awhere%0D%0A++++articles_fts+match+%3Asearch%0D%0Aorder+by+bm25&search=jquery+maps). Read [Exploring search relevance algorithms with SQLite](https://simonwillison.net/2019/Jan/7/exploring-search-relevance-algorithms-sqlite/) for further details on this project.

## Installation

    pip install datasette-sqlite-fts4

If you are deploying a database using `datasette publish` you can include this plugin using the `--install` option:

    datasette publish now mydb.db --install=datasette-sqlite-fts4
