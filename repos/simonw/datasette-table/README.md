# datasette-table

[![npm](https://img.shields.io/npm/v/datasette-table)](https://www.npmjs.com/package/datasette-table)

A (highly experimental) Web Component for embedding a [Datasette](https://datasette.io/) table on a page.

## Demo

Visit [https://simonw.github.io/datasette-table/](https://simonw.github.io/datasette-table/) for a demo of this component.

## Usage

```html
<script type="module" src="https://unpkg.com/datasette-table?module"></script>

<datasette-table
    url="https://global-power-plants.datasettes.com/global-power-plants/global-power-plants.json"
></datasette-table>
```

## Development

Check out this repository, then run:

    cd datasette-table
    npm install

Then to start a local development server (using Vite):

    npm run dev

Then visit `http://localhost:3000/`
