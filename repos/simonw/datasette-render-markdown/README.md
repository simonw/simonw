# datasette-render-markdown

[![PyPI](https://img.shields.io/pypi/v/datasette-render-markdown.svg)](https://pypi.org/project/datasette-render-markdown/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-render-markdown?include_prereleases&label=changelog)](https://github.com/simonw/datasette-render-markdown/releases)
[![Tests](https://github.com/simonw/datasette-render-markdown/workflows/Test/badge.svg)](https://github.com/simonw/datasette-render-markdown/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-render-markdown/blob/main/LICENSE)

[Datasette](https://datasette.io/) plugin for rendering Markdown.

## Installation

Install this plugin in the same environment as Datasette to enable this new functionality:
```bash
datasette install datasette-render-markdown
```
## Usage

You can explicitly list the columns you would like to treat as Markdown using [plugin configuration](https://datasette.readthedocs.io/en/stable/plugins.html#plugin-configuration) in a `metadata.json` file.

Add a `"datasette-render-markdown"` configuration block and use a `"columns"` key to list the columns you would like to treat as Markdown values:

```json
{
    "plugins": {
        "datasette-render-markdown": {
            "columns": ["body"]
        }
    }
}
```

This will cause any `body` column in any table to be treated as markdown and safely rendered using [Python-Markdown](https://python-markdown.github.io/). The resulting HTML is then run through [Bleach](https://bleach.readthedocs.io/) to avoid the risk of XSS security problems.

Save this to `metadata.json` and run Datasette with the `--metadata` flag to load this configuration:

    $ datasette serve mydata.db --metadata metadata.json

The configuration block can be used at the top level, or it can be applied just to specific databases or tables. Here's how to apply it to just the `entries` table in the `news.db` database:

```json
{
    "databases": {
        "news": {
            "tables": {
                "entries": {
                    "plugins": {
                        "datasette-render-markdown": {
                            "columns": ["body"]
                        }
                    }
                }
            }
        }
    }
}
```

And here's how to apply it to every `body` column in every table in the `news.db` database:

```json
{
    "databases": {
        "news": {
            "plugins": {
                "datasette-render-markdown": {
                    "columns": ["body"]
                }
            }
        }
    }
}
```

## Columns that match a naming convention

This plugin can also render markdown in any columns that match a specific naming convention.

By default, columns that have a name ending in `_markdown` will be rendered.

You can try this out using the following query:

```sql
select '# Hello there

* This is a list
* of items

[And a link](https://github.com/simonw/datasette-render-markdown).'
as demo_markdown
```

You can configure a different list of wildcard patterns using the `"patterns"` configuration key. Here's how to render columns that end in either `_markdown` or `_md`:

```json
{
    "plugins": {
        "datasette-render-markdown": {
            "patterns": ["*_markdown", "*_md"]
        }
    }
}
```

To disable wildcard column matching entirely, set `"patterns": []` in your plugin metadata configuration.

## Markdown extensions

The [Python-Markdown library](https://python-markdown.github.io/) that powers this plugin supports extensions, both [bundled](https://python-markdown.github.io/extensions/) and [third-party](https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions). These can be used to enable additional Markdown features such as [table support](https://python-markdown.github.io/extensions/tables/).

You can configure support for extensions using the `"extensions"` key in your plugin metadata configuration.

Since extensions may introduce new HTML tags, you will also need to add those tags to the list of tags that are allowed by the [Bleach](https://bleach.readthedocs.io/) sanitizer. You can do that using the `"extra_tags"` key, and you can allow-list additional HTML attributes using `"extra_attrs"`. See [the Bleach documentation](https://bleach.readthedocs.io/en/latest/clean.html#allowed-tags-tags) for more information on this.

Here's how to enable support for [Markdown tables](https://python-markdown.github.io/extensions/tables/):

```json
{
    "plugins": {
        "datasette-render-markdown": {
            "extensions": ["tables"],
            "extra_tags": ["table", "thead", "tr", "th", "td", "tbody"]
        }
    }
}
```

### GitHub-Flavored Markdown

Enabling [GitHub-Flavored Markdown](https://help.github.com/en/github/writing-on-github) (useful for if you are working with data imported from GitHub using [github-to-sqlite](https://github.com/dogsheep/github-to-sqlite)) is a little more complicated.

First, you will need to install the [py-gfm](https://py-gfm.readthedocs.io) package:

    $ pip install py-gfm

Note that `py-gfm` has [a bug](https://github.com/Zopieux/py-gfm/issues/13) that causes it to pin to `Markdown<3.0` - so if you are using it you should install it _before_ installing `datasette-render-markdown` to ensure you get a compatibly version of that dependency.

Now you can configure it like this. Note that the extension name is `mdx_gfm:GithubFlavoredMarkdownExtension` and you need to allow-list several extra HTML tags and attributes:

```json
{
    "plugins": {
        "datasette-render-markdown": {
            "extra_tags": [
                "hr",
                "br",
                "details",
                "summary",
                "input"
            ],
            "extra_attrs": {
                "input": [
                    "type",
                    "disabled",
                    "checked"
                ],
            },
            "extensions": [
                "mdx_gfm:GithubFlavoredMarkdownExtension"
            ]
        }
    }
}
```

The `<input type="" checked disabled>` attributes are needed to support rendering checkboxes in issue descriptions.

## Markdown in templates

The plugin introduces a new template tag: `{% markdown %}...{% endmarkdown %}` - which can be used to render Markdown in your Jinja templates.

```html+jinja
{% markdown %}
# This will be rendered as markdown
{% endmarkdown %}
```
You can use attributes on the `{% markdown %}` tag to enable extensions and allow-list additional tags and attributes:
```html+jinja
{% markdown
  extensions="tables"
  extra_tags="table thead tr th td tbody" 
  extra_attrs="p:id,class a:name,href" %}
## Markdown table

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

<a href="https://www.example.com/" name="namehere">Example</a>
<p id="paragraph" class="klass">Paragraph</p>
{% endmarkdown %}
```
The `extensions=` and `extra_tags=` attributes accept a space-separated list of values.

The `extra_attrs=` attribute accepts a space-separated list of `tag:attr1,attr2` values - each tag can specify one or more attributes that should be allowed.

You can also use the `{{ render_markdown(...) }}` function, like this:

```html+jinja
{{ render_markdown("""
## Markdown table

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
""", extensions=["tables"],
    extra_tags=["table", "thead", "tr", "th", "td", "tbody"])) }}
```

The `{% markdown %}` tag is recommended, as it avoids the need to `\"` escape quotes in your Markdown content.
