# datasette-jq

[![PyPI](https://img.shields.io/pypi/v/datasette-jq.svg)](https://pypi.org/project/datasette-jq/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-jq.svg?style=svg)](https://circleci.com/gh/simonw/datasette-jq)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-jq/blob/master/LICENSE)

Datasette plugin that adds custom SQL functions for executing [jq](https://stedolan.github.io/jq/) expressions against JSON values.

Install this plugin in the same environment as Datasette to enable the `jq()` SQL function.

Usage:

    select jq(
        column_with_json,
        "{top_3: .classifiers[:3], v: .version}"
    )

See [the jq manual](https://stedolan.github.io/jq/manual/#Basicfilters) for full details of supported expression syntax.

## Interactive demo

You can try this plugin out at [datasette-jq-demo.datasette.io](https://datasette-jq-demo.datasette.io/)

Sample query:

    select package, "https://pypi.org/project/" || package || "/" as url,
    jq(info, "{summary: .info.summary, author: .info.author, versions: .releases|keys|reverse}")
    from packages

[Try this query out](https://datasette-jq-demo.datasette.io/demo?sql=select+package%2C+%22https%3A%2F%2Fpypi.org%2Fproject%2F%22+%7C%7C+package+%7C%7C+%22%2F%22+as+url%2C%0D%0Ajq%28info%2C+%22%7Bsummary%3A+.info.summary%2C+author%3A+.info.author%2C+versions%3A+.releases%7Ckeys%7Creverse%7D%22%29%0D%0Afrom+packages) in the interactive demo.
