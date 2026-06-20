# datasette-publish-fly

[![PyPI](https://img.shields.io/pypi/v/datasette-publish-fly.svg)](https://pypi.org/project/datasette-publish-fly/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-publish-fly?include_prereleases&label=changelog)](https://github.com/simonw/datasette-publish-fly/releases)
[![Tests](https://github.com/simonw/datasette-publish-fly/workflows/Test/badge.svg)](https://github.com/simonw/datasette-publish-fly/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-publish-fly/blob/main/LICENSE)

[Datasette](https://datasette.io/) plugin for deploying Datasette instances to [Fly.io](https://fly.io/).

Project background: [Using SQLite and Datasette with Fly Volumes](https://simonwillison.net/2022/Feb/15/fly-volumes/)

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-publish-fly

## Deploying read-only data

First, install the `flyctl` command-line tool by [following their instructions](https://fly.io/docs/getting-started/installing-flyctl/).

Run `flyctl auth signup` to create an account there, or `flyctl auth login` if you already have one.

You can now use `datasette publish fly` to publish one or more SQLite database files:

    datasette publish fly my-database.db --app="my-data-app"

The argument you pass to `--app` will be used for the URL of your application: `my-data-app.fly.dev`.

To update an application, run the publish command passing the same application name to the `--app` option.

Fly have [a free tier](https://fly.io/docs/about/pricing/#free-allowances), beyond which they will charge you monthly for each application you have live.  Details of their pricing can be [found on their site](https://fly.io/docs/pricing/).

Your application will be deployed at `https://your-app-name.fly.io/` - be aware that it may take several minutes to start working the first time you deploy it.

## Using Fly volumes for writable databases

Fly [Volumes](https://fly.io/docs/reference/volumes/) provide persistant disk storage for Fly applications. Volumes can be 1GB or more in size and the Fly free tier includes 3GB of volume space.

Datasette plugins such as [datasette-uploads-csvs](https://datasette.io/plugins/datasette-upload-csvs) and [datasette-tiddlywiki](https://datasette.io/plugins/datasette-tiddlywiki) can be deployed to Fly and store their mutable data in a volume.

> :warning: **You should only run a single instance of your application** if your database accepts writes. Fly has excellent support for running multiple instances in different geographical regions, but `datasette-publish-fly` with volumes is not yet compatible with that model. You should probably [use Fly PostgreSQL instead](https://fly.io/blog/globally-distributed-postgres/).

Here's how to deploy `datasette-tiddlywiki` with authentication provided by `datasette-auth-passwords`.

First, you'll need to create a root password hash to use to sign into the instance.

You can do that by installing the plugin and running the `datasette hash-password` command, or by using [this hosted tool](https://datasette-auth-passwords-demo.datasette.io/-/password-tool).

The hash should look like `pbkdf2_sha256$...` - you'll need this for the next step.

In this example we're also deploying a read-only database called `content.db`.

Pick a name for your new application, then run the following:

    datasette publish fly \
    content.db \
    --app your-application-name \
    --create-volume 1 \
    --create-db tiddlywiki \
    --install datasette-auth-passwords \
    --install datasette-tiddlywiki \
    --plugin-secret datasette-auth-passwords root_password_hash 'pbkdf2_sha256$...'

This will create the new application, deploy the `content.db` read-only database, create a 1GB volume for that application, create a new database in that volume called `tiddlywiki.db`, then install the two plugins and configure the password you specified.

### Updating applications that use a volume

Once you have deployed an application using a volume, you can update that application without needing the `--create-volume` or `--create-db` options. To add the [datasette-graphq](https://datasette.io/plugins/datasette-graphql) plugin to your deployed application you would run the following:

    datasette publish fly \
    content.db \
    --app your-application-name \
    --install datasette-auth-passwords \
    --install datasette-tiddlywiki \
    --install datasette-graphql \
    --plugin-secret datasette-auth-passwords root_password_hash 'pbkdf2_sha256$...' \

Since the application name is the same you don't need the `--create-volume` or `--create-db` options - these are persisted automatically between deploys.

You do need to specify the full list of plugins that you want to have installed, and any plugin secrets.

You also need to include any read-only database files that are part of the instance - `content.db` in this example - otherwise the new deployment will not include them.

### Advanced volume usage

`datasette publish fly` will add a volume called `datasette` to your Fly application. You can customize the name using the `--volume name custom_name` option.

Fly can be used to scale applications to run multiple instances in multiple regions around the world. This works well with read-only Datasette but is not currently recommended using Datasette with volumes, since each Fly replica would need its own volume and data stored in one instance would not be visible in others.

If you want to use multiple instances with volumes you will need to switch to using the `flyctl` command directly. The `--generate-dir` option, described below, can help with this.

## Generating without deploying

Use the `--generate-dir` option to generate a directory that can be deployed to Fly rather than deploying directly:

    datasette publish fly my-database.db \
      --app="my-generated-app" \
      --generate-dir /tmp/deploy-this

You can then manually deploy your generated application using the following:

    cd /tmp/deploy-this
    flyctl apps create my-generated-app
    flyctl deploy

## datasette publish fly --help

<!-- [[[cog
import cog
from datasette import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["publish", "fly", "--help"])
help = result.output.replace("Usage: cli", "Usage: datasette")
cog.out(
    "```\n{}```".format(help)
)
]]] -->
```
Usage: datasette publish fly [OPTIONS] [FILES]...

  Deploy an application to Fly that runs Datasette against the provided database
  files.

  Usage example:

      datasette publish fly my-database.db --app="my-data-app"

  Full documentation: https://datasette.io/plugins/datasette-publish-fly

Options:
  -m, --metadata FILENAME         Path to JSON/YAML file containing metadata to
                                  publish
  --extra-options TEXT            Extra options to pass to datasette serve
  --branch TEXT                   Install datasette from a GitHub branch e.g.
                                  main
  --template-dir DIRECTORY        Path to directory containing custom templates
  --plugins-dir DIRECTORY         Path to directory containing custom plugins
  --static MOUNT:DIRECTORY        Serve static files from this directory at
                                  /MOUNT/...
  --install TEXT                  Additional packages (e.g. plugins) to install
  --plugin-secret <TEXT TEXT TEXT>...
                                  Secrets to pass to plugins, e.g. --plugin-
                                  secret datasette-auth-github client_id xxx
  --version-note TEXT             Additional note to show on /-/versions
  --secret TEXT                   Secret used for signing secure values, such as
                                  signed cookies
  --title TEXT                    Title for metadata
  --license TEXT                  License label for metadata
  --license_url TEXT              License URL for metadata
  --source TEXT                   Source label for metadata
  --source_url TEXT               Source URL for metadata
  --about TEXT                    About label for metadata
  --about_url TEXT                About URL for metadata
  --spatialite                    Enable SpatialLite extension
  --region TEXT                   Fly region to deploy to, e.g sjc - see
                                  https://fly.io/docs/reference/regions/
  --create-volume INTEGER RANGE   Create and attach volume of this size in GB
                                  [x>=1]
  --create-db TEXT                Names of read-write database files to create
  --volume-name TEXT              Volume name to use
  -a, --app TEXT                  Name of Fly app to deploy  [required]
  -o, --org TEXT                  Name of Fly org to deploy to
  --generate-dir DIRECTORY        Output generated application files and stop
                                  without deploying
  --show-files                    Output the generated Dockerfile, metadata.json
                                  and fly.toml
  --setting SETTING...            Setting, see
                                  docs.datasette.io/en/stable/settings.html
  --crossdb                       Enable cross-database SQL queries
  --help                          Show this message and exit.
```
<!-- [[[end]]] -->

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd datasette-publish-fly
    python -m venv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest

### Integration tests

The tests in `tests/test_integration.py` make actual calls to Fly to deploy a test application.

These tests are skipped by default. If you have `flyctl` installed and configured, you can run the integration tests like this:

    pytest --integration -s

The `-s` option here ensures that output from the deploys will be visible to you - otherwise it can look like the tests have hung.

The tests will create applications on Fly that start with the prefix `publish-fly-temp-` and then delete them at the end of the run.
