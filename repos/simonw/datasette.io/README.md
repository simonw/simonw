# datasette.io

The official project website for [Datasette](https://github.com/simonw/datasette).

https://datasette.io/

The site is itself a customized installation of Datasette, using custom templates and plugins to implement the site's functionality.

Take a look at [.github/workflows/deploy.yml](https://github.com/simonw/datasette.io/blob/main/.github/workflows/deploy.yml) to see how the site is built and deployed to Google Cloud Run using GitHub Actions.

More background:

- [datasette.io, an official project website for Datasette](https://simonwillison.net/2020/Dec/13/datasette-io/)
- [Building a search engine for datasette.io](https://simonwillison.net/2020/Dec/19/dogsheep-beta/)
- [The Baked Data architectural pattern](https://simonwillison.net/2021/Jul/28/baked-data/)

## Development

Dependencies are managed with [uv](https://docs.astral.sh/uv/). Check out this repository and install them like this:

    uv sync

If you don't want to build the database files from scratch, run this to download them:

    ./refresh-from-production.sh

To build the database files used by the site you will first need to set an environment variable containing a GitHub personal access token. You can create a token at https://github.com/settings/tokens - then set it as the `GITHUB_TOKEN` environment variable like so:

    export GITHUB_TOKEN="token-here"

Now you can build the databases like this:

    uv run scripts/build.sh

Then to run the tests (which check that certain pages do not return errors):

    uv run pytest
    uv run scripts/test.sh

To see the site in your browser:

    ./dev-server.sh

This will run a server at `http://localhost:9008/`, restarting when plugins or configuration change.

### Blog posts

Blog posts live as Markdown files in `blog-content/`. After adding or editing one, rebuild the `blog_posts` table in `content.db` with:

    ./build-blog.sh
