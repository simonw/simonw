# datasette-css-properties

[![PyPI](https://img.shields.io/pypi/v/datasette-css-properties.svg)](https://pypi.org/project/datasette-css-properties/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-css-properties?include_prereleases&label=changelog)](https://github.com/simonw/datasette-css-properties/releases)
[![Tests](https://github.com/simonw/datasette-css-properties/workflows/Test/badge.svg)](https://github.com/simonw/datasette-css-properties/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-css-properties/blob/main/LICENSE)

Extremely experimental Datasette output plugin using CSS properties, inspired by [Custom Properties as State](https://css-tricks.com/custom-properties-as-state/) by Chris Coyier.

More about this project: [APIs from CSS without JavaScript: the datasette-css-properties plugin](https://simonwillison.net/2021/Jan/7/css-apis-no-javascript/)

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-css-properties

## Usage

Once installed, this plugin adds a `.css` output format to every query result. This will return the first row in the query as a valid CSS file, defining each column as a custom property:

Example: https://latest-with-plugins.datasette.io/fixtures/roadside_attractions.css produces:

```css
:root {
  --pk: '1';
  --name: 'The Mystery Spot';
  --address: '465 Mystery Spot Road, Santa Cruz, CA 95065';
  --latitude: '37.0167';
  --longitude: '-122.0024';
}
```

If you link this stylesheet to your page you can then do things like this:

```html
<link rel="stylesheet" href="https://latest-with-plugins.datasette.io/fixtures/roadside_attractions.css">
<style>
.attraction-name:after { content: var(--name); }
</style>
<p class="attraction-name">Attraction name: </p>
```

Values will be quoted as CSS strings by default. If you want to return a "raw" value without the quotes - for example to set a CSS property that is numeric or a color, you can specify that column name using the `?_raw=column-name` parameter. This can be passed multiple times.

Consider [this example query](https://latest-with-plugins.datasette.io/github?sql=select%0D%0A++%27%23%27+||+substr(sha%2C+0%2C+6)+as+[custom-bg]%0D%0Afrom%0D%0A++commits%0D%0Aorder+by%0D%0A++author_date+desc%0D%0Alimit%0D%0A++1%3B):

```sql
select
  '#' || substr(sha, 0, 6) as [custom-bg]
from
  commits
order by
  author_date desc
limit
  1;
```

This returns the first 6 characters of the most recently authored commit with a `#` prefix. The `.css` [output rendered version](https://latest-with-plugins.datasette.io/github.css?sql=select%0D%0A++%27%23%27+||+substr(sha%2C+0%2C+6)+as+[custom-bg]%0D%0Afrom%0D%0A++commits%0D%0Aorder+by%0D%0A++author_date+desc%0D%0Alimit%0D%0A++1%3B) looks like this:

```css
:root {
  --custom-bg: '#97fb1';
}
```

Adding `?_raw=custom-bg` to the URL produces [this instead](https://latest-with-plugins.datasette.io/github.css?sql=select%0D%0A++%27%23%27+||+substr(sha%2C+0%2C+6)+as+[custom-bg]%0D%0Afrom%0D%0A++commits%0D%0Aorder+by%0D%0A++author_date+desc%0D%0Alimit%0D%0A++1%3B&_raw=custom-bg):

```css
:root {
  --custom-bg: #97fb1;
}
```

This can then be used as a color value like so:

```css
h1 {
    background-color: var(--custom-bg);
}
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-css-properties
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
