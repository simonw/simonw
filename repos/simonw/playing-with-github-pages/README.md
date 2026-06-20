# playing-with-github-pages

- https://simonw.github.io/playing-with-github-pages/ serves `index.html`
- https://simonw.github.io/playing-with-github-pages/foo serves `foo.html`
- https://simonw.github.io/playing-with-github-pages/foo.html serves `foo.html`
- https://simonw.github.io/playing-with-github-pages/bar.json serves `bar.json`
- https://simonw.github.io/playing-with-github-pages/bar serves a 404 (actually the custom `404.html` page)

And in a `folder/`:

- https://simonw.github.io/playing-with-github-pages/folder redirects to `/folder/`
- https://simonw.github.io/playing-with-github-pages/folder/ serves `folder/index.html`
- https://simonw.github.io/playing-with-github-pages/folder/index serves `folder/index.html`
- https://simonw.github.io/playing-with-github-pages/folder/index.html serves `folder/index.html`
- https://simonw.github.io/playing-with-github-pages/folder/baz serves `folder/baz.html`
- https://simonw.github.io/playing-with-github-pages/folder/baz.html serves `folder/baz.html`

I created `folder2.html` and `folder2/index.html`:

- https://simonw.github.io/playing-with-github-pages/folder2 serves `folder2.html` (does not redirect)
- https://simonw.github.io/playing-with-github-pages/folder2/ serves `folder2/index.html`
- https://simonw.github.io/playing-with-github-pages/folder2/index serves `folder2/index.html`
- https://simonw.github.io/playing-with-github-pages/folder2/index.html serves `folder2/index.html`

I also created `folder-with-no-index/` without a `index.html` file:

- https://simonw.github.io/playing-with-github-pages/folder-with-no-index redirects to `/folder-with-no-index/`
- https://simonw.github.io/playing-with-github-pages/folder-with-no-index/ serves a 404

`index.json` can act as an index page too:

- https://simonw.github.io/playing-with-github-pages/json redirects to `/json/`
- https://simonw.github.io/playing-with-github-pages/json/ serves `json/index.json`
- https://simonw.github.io/playing-with-github-pages/json/index serves a 404
- https://simonw.github.io/playing-with-github-pages/json/index.json serves `json/index.json`
- https://simonw.github.io/playing-with-github-pages/json/bar serves a 404
- https://simonw.github.io/playing-with-github-pages/json/bar.json serves `json/bar.json`
- https://simonw.github.io/playing-with-github-pages/json/foo redirects to `/json/foo/`
- https://simonw.github.io/playing-with-github-pages/json/foo/ serves `json/foo/index.json`

The existence of the `.nojekyll` file causes GitHub Pages to publish the raw files without attempting to run Jekyll against them first.
