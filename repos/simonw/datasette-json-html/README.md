# datasette-json-html

[![PyPI](https://img.shields.io/pypi/v/datasette-json-html.svg)](https://pypi.org/project/datasette-json-html/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-json-html?include_prereleases&label=changelog)](https://github.com/simonw/datasette-json-html/releases)
[![Tests](https://github.com/simonw/datasette-json-html/workflows/Test/badge.svg)](https://github.com/simonw/datasette-remote-metadata/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-json-html/blob/main/LICENSE)

Datasette plugin for rendering HTML based on JSON values, using the [render_cell plugin hook](https://docs.datasette.io/en/stable/plugin_hooks.html#render-cell-value-column-table-database-datasette).

This plugin looks for cell values that match a very specific JSON format and converts them into HTML when they are rendered by the Datasette interface.

## Links

    {
        "href": "https://simonwillison.net/",
        "label": "Simon Willison"
    }

Will be rendered as an `<a href="">` link:

    <a href="https://simonwillison.net/">Simon Willison</a>

You can set a tooltip on the link using a `"title"` key:


    {
        "href": "https://simonwillison.net/",
        "label": "Simon Willison",
        "title": "My blog"
    }

Produces:

    <a href="https://simonwillison.net/" title="My blog">Simon Willison</a>

You can also include a description, which will be displayed below the link. If descriptions include newlines they will be converted to `<br>` elements:

    select json_object(
        "href", "https://simonwillison.net/",
        "label", "Simon Willison",
        "description", "This can contain" || x'0a' || "newlines"
    )

Produces:

    <strong><a href="https://simonwillison.net/">Simon Willison</a></strong><br>This can contain<br>newlines

* [Literal JSON link demo](https://datasette-json-html.datasette.io/demo?sql=select+%27%7B%0D%0A++++%22href%22%3A+%22https%3A%2F%2Fsimonwillison.net%2F%22%2C%0D%0A++++%22label%22%3A+%22Simon+Willison%22%2C%0D%0A++++%22title%22%3A+%22My+blog%22%0D%0A%7D%27)

## List of links

    [
        {
            "href": "https://simonwillison.net/",
            "label": "Simon Willison"
        },
        {
            "href": "https://github.com/simonw/datasette",
            "label": "Datasette"
        }
    ]

Will be rendered as a comma-separated list of `<a href="">` links:

    <a href="https://simonwillison.net/">Simon Willison</a>,
    <a href="https://github.com/simonw/datasette">Datasette</a>

The `href` property must begin with `https://` or `http://` or `/`, to avoid potential XSS injection attacks (for example URLs that begin with `javascript:`).

Lists of links cannot include `"description"` keys.

* [Literal list of links demo](https://datasette-json-html.datasette.io/demo?sql=select+%27%5B%0D%0A++++%7B%0D%0A++++++++%22href%22%3A+%22https%3A%2F%2Fsimonwillison.net%2F%22%2C%0D%0A++++++++%22label%22%3A+%22Simon+Willison%22%0D%0A++++%7D%2C%0D%0A++++%7B%0D%0A++++++++%22href%22%3A+%22https%3A%2F%2Fgithub.com%2Fsimonw%2Fdatasette%22%2C%0D%0A++++++++%22label%22%3A+%22Datasette%22%0D%0A++++%7D%0D%0A%5D%27)

## Images

The image tag is more complex. The most basic version looks like this:

    {
        "img_src": "https://placekitten.com/200/300"
    }

This will render as:

    <img src="https://placekitten.com/200/300">

But you can also include one or more of `alt`, `caption`, `width` and `href`.

If you include width or alt, they will be added as attributes:

    {
        "img_src": "https://placekitten.com/200/300",
        "alt": "Kitten",
        "width": 200
    }

Produces:

    <img src="https://placekitten.com/200/300"
        alt="Kitten" width="200">

* [Literal image demo](https://datasette-json-html.datasette.io/demo?sql=select+%27%7B%0D%0A++++%22img_src%22%3A+%22https%3A%2F%2Fplacekitten.com%2F200%2F300%22%2C%0D%0A++++%22alt%22%3A+%22Kitten%22%2C%0D%0A++++%22width%22%3A+200%0D%0A%7D%27)

The `href` key will cause the image to be wrapped in a link:

    {
        "img_src": "https://placekitten.com/200/300",
        "href": "http://www.example.com"
    }

Produces:

    <a href="http://www.example.com">
        <img src="https://placekitten.com/200/300">
    </a>

The `caption` key wraps everything in a fancy figure/figcaption block:

    {
        "img_src": "https://placekitten.com/200/300",
        "caption": "Kitten caption"
    }

Produces:

    <figure>
        <img src="https://placekitten.com/200/300"></a>
        <figcaption>Kitten caption</figcaption>
    </figure>

## Preformatted text

You can use `{"pre": "text"}` to render text in a `<pre>` HTML tag:

    {
        "pre": "This\nhas\nnewlines"
    }

Produces:

    <pre>This
    has
    newlines</pre>

If the value attached to the `"pre"` key is itself a JSON object, that JSON will be pretty-printed:

    {
        "pre": {
            "this": {
                "object": ["is", "nested"]
            }
        }
    }

Produces:

    <pre>{
      &#34;this&#34;: {
        &#34;object&#34;: [
          &#34;is&#34;,
          &#34;nested&#34;
        ]
      }
    }</pre>

* [Preformatted text with JSON demo](https://datasette-json-html.datasette.io/demo?sql=select+%27%7B%0D%0A++++%22pre%22%3A+%7B%0D%0A++++++++%22this%22%3A+%7B%0D%0A++++++++++++%22object%22%3A+%5B%22is%22%2C+%22nested%22%5D%0D%0A++++++++%7D%0D%0A++++%7D%0D%0A%7D%27)
* [Preformatted text demo showing the Mandelbrot Set](https://datasette-json-html.datasette.io/demo?sql=WITH+RECURSIVE%0D%0A++xaxis%28x%29+AS+%28VALUES%28-2.0%29+UNION+ALL+SELECT+x%2B0.05+FROM+xaxis+WHERE+x%3C1.2%29%2C%0D%0A++yaxis%28y%29+AS+%28VALUES%28-1.0%29+UNION+ALL+SELECT+y%2B0.1+FROM+yaxis+WHERE+y%3C1.0%29%2C%0D%0A++m%28iter%2C+cx%2C+cy%2C+x%2C+y%29+AS+%28%0D%0A++++SELECT+0%2C+x%2C+y%2C+0.0%2C+0.0+FROM+xaxis%2C+yaxis%0D%0A++++UNION+ALL%0D%0A++++SELECT+iter%2B1%2C+cx%2C+cy%2C+x*x-y*y+%2B+cx%2C+2.0*x*y+%2B+cy+FROM+m+%0D%0A+++++WHERE+%28x*x+%2B+y*y%29+%3C+4.0+AND+iter%3C28%0D%0A++%29%2C%0D%0A++m2%28iter%2C+cx%2C+cy%29+AS+%28%0D%0A++++SELECT+max%28iter%29%2C+cx%2C+cy+FROM+m+GROUP+BY+cx%2C+cy%0D%0A++%29%2C%0D%0A++a%28t%29+AS+%28%0D%0A++++SELECT+group_concat%28+substr%28%27+.%2B*%23%27%2C+1%2Bmin%28iter%2F7%2C4%29%2C+1%29%2C+%27%27%29+%0D%0A++++FROM+m2+GROUP+BY+cy%0D%0A++%29%0D%0ASELECT+json_object%28%27pre%27%2C+group_concat%28rtrim%28t%29%2Cx%270a%27%29%29+FROM+a%3B) using [this example](https://www.sqlite.org/lang_with.html#outlandish_recursive_query_examples) from the SQLite documentation

## Using these with SQLite JSON functions

The most powerful way to make use of this plugin is in conjunction with SQLite's [JSON functions](https://www.sqlite.org/json1.html). For example:

    select json_object(
        "href", "https://simonwillison.net/",
        "label", "Simon Willison"
    );

* [json_object() link demo](https://datasette-json-html.datasette.io/demo?sql=select+json_object%28%0D%0A++++%22href%22%2C+%22https%3A%2F%2Fsimonwillison.net%2F%22%2C%0D%0A++++%22label%22%2C+%22Simon+Willison%22%0D%0A%29%3B)

You can use these functions to construct JSON objects that work with the plugin from data in a table:

    select id, json_object(
        "href", url, "label", text
    ) from mytable;

* [Demo that builds links against a table](https://datasette-json-html.datasette.io/demo?sql=select+json_object%28%22href%22%2C+url%2C+%22label%22%2C+package%2C+%22title%22%2C+package+%7C%7C+%22+%22+%7C%7C+url%29+as+package+from+packages)

The `json_group_array()` function is an aggregate function similar to `group_concat()` - it allows you to construct lists of JSON objects in conjunction with a `GROUP BY` clause.

This means you can use it to construct dynamic lists of links, for example:

    select
        substr(package, 0, 12) as prefix,
        json_group_array(
            json_object(
                "href", url,
                "label", package
            )
        ) as package_links
    from packages
    group by prefix

* [Demo of json_group_array()](https://datasette-json-html.datasette.io/demo?sql=select%0D%0A++++substr%28package%2C+0%2C+12%29+as+prefix%2C%0D%0A++++json_group_array%28%0D%0A++++++++json_object%28%0D%0A++++++++++++%22href%22%2C+url%2C%0D%0A++++++++++++%22label%22%2C+package%0D%0A++++++++%29%0D%0A++++%29+as+package_links%0D%0Afrom+packages%0D%0Agroup+by+prefix)

## The `urllib_quote_plus()` SQL function

Since this plugin is designed to be used with SQL that constructs the underlying JSON structure, it is likely you will need to construct dynamic URLs from results returned by a SQL query.

This plugin registers a custom SQLite function called `urllib_quote_plus()` to help you do that. It lets you use Python's [urllib.parse.quote\_plus() function](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote_plus) from within a SQL query.

Here's an example of how you might use it:

    select id, json_object(
        "href",
        "/mydatabase/other_table?_search=" || urllib_quote_plus(text),
        "label", text
    ) from mytable;
