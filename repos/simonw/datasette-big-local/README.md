# datasette-big-local

[![Tests](https://github.com/simonw/datasette-big-local/workflows/Test/badge.svg)](https://github.com/simonw/datasette-big-local/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-big-local/blob/main/LICENSE)

This plugin is not useful to anyone outside of the Big Local News team. This repo is public so that the code can be consulted by anyone who wants to know how it works.

## Installation

Install this plugin in the same environment as Datasette, using the URL to the zip file for this repo:

    datasette install https://github.com/simonw/datasette-big-local/archive/refs/heads/main.zip

## Configuration

This plugin takes a single plugin configuration option: the path to the directory where the databases it creates should be stored. In `metadata.yml` that looks like this:

```yaml
plugins:
  datasette-big-local:
    root_dir: /path/to/directory
```
Then start Datasette with `datasette -m metadata.yml`.

### Additional plugin options

- `graphql_url` - the URL to the GraphQL API that this communicates with. This defaults to `https://api.biglocalnews.org/graphql` - you can change this to point at a development instance.
- `csv_size_limit_mb` - the maximum size of CSV file that can be imported, as an integer number of MBs. This defaults to 100MB.
- `login_redirect_url` - the URL that users should be redirected to if they do not have permission to access as page. This will have `project_id=...&redirect_path=/...` appended to it - so it should end in either a `?` or a `#`. This defaults to `https://biglocalnews.org/#/datasette?`.

Example `metadata.yml` with all of these options:

```yaml
plugins:
  datasette-big-local:
    root_dir: /path/to/directory
    graphql_url: https://api.biglocalnews.dev/graphql
    csv_size_limit_mb: 50
    login_redirect_url: https://biglocalnews.dev/#/datasette
```

## Endpoints

This plugin adds some endpoints which are designed to be called from the Big Local News web application.

### /-/big-local-open

When a user clicks "open in Datasette" on a CSV file within Big Local, their browser should submit an HTTP POST to this endpoint with the three following form parameters:

- `project_id` - the Base 64 encoded ID of the project on Big Local, e.g. `UHJvamVjdDpmZjAxNTBjNi1iNjM0LTQ3MmEtODFiMi1lZjJlMGMwMWQyMjQ=`
- `filename` - the name of the CSV file within that project, e.g. `universities_final.csv`
- `remember_token` - a Big Local authentication token for the user who is opening that file - the same value that is stored in that user's `remember_token` cookie

The endpoint will use that `remember_token` cookie to confirm that the user has access to that project.

If they do, Datasette will fetch the content of the CSV file and import it into a SQLite database dedicated to that project.

The database will use the UUID of the project as its name. It will be created on disk if it does not already exist.

The user will also get a signed cookie signing them into the Datasette instance.

Datasette will cache the fact that the user has permission to access that project for five minutes. After five minutes another call will be made to the Big Local GraphQL API to confirm that the user still has permissions for that project.

### /-/big-local-project

There are some situations in which a user may want to open a project directly in Datasette without first selecting a file. This POST endpoint provides that capability.

It takes two required form parameters:

- `project_id` - the Base 64 encoded ID of the project
- `remember_token` - a Big Local authentication token for the user

And one optional parameter:

- `redirect_path` - the path to redirect to after the user has been signed in. This must start with a `/` - it defaults to the database page for the project database.

If the user has permission to access that project, they will be signed in and redirected to the `redirect_path`.

As a convenience, this endpoint also fetches and caches a list of files within the project. Any CSV files that are within the CSV size limit and that have not been previously imported will be listed on the database page, with a button to trigger an import.

## Implementing login redirects

The usual path for this system is that a user signs into Big Local News, finds a file in a project, clicks "open in Datasette" and is seamlessly transferred to the Datasette instance and signed in with the correct permissions.

There's one other path that needs considering: what happens if a user bookmarks a link to a page within Datasette, or shares such a link with a coworker who should also have access.

If a user who is not signed into the Datasette instance visits the following page:

`https://the-datasette-instance.biglocalnews.org/ff0150c6-b634-472a-81b2-ef2e0c01d224/universities_5f_final_2e_csv`

They will be redirected back to Big Local News, with the project ID that they attempted to access (converted from UUID to base64) and the path they are trying to visit passed as arguments in the URL.

By default, that redirect will go to:

`https://biglocalnews.org/#/datasette?project_id=UHJvamVjdDpmZjAxNTBjNi1iNjM0LTQ3MmEtODFiMi1lZjJlMGMwMWQyMjQ=&redirect_path=/ff0150c6-b634-472a-81b2-ef2e0c01d224/universities_5f_final_2e_csv`

This can be customized using the `login_redirect_url` plugin configuration option.

Big Local News should implement code that matches that URL (or some other configured URL - even a `/database.html` page would work for this), extracts the `project_id` and `redirect_path` arguments, looks up the user's `remember_token` cookie and then constructs an HTTP POST to the `/-/big-local-project` endpoint documented above.

The page could contain something like this:

```html
<form action="https://the-datasette-instance.biglocalnews.org/-/big-local-project" method="post">
  <input type="hidden" name="project_id" value="">
  <input type="hidden" name="remember_token" value="">
  <input type="hidden" name="redirect_path" value="">
  <input type="submit" value="Visit this page in Datasette">
</form>
<script>
var remember_token = document.cookie.split(';').find(
    c => c.trim().startsWith('remember_token=')
)?.split('=')[1];
if (remember_token) {
    var params = new URLSearchParams(location.href.split("?")[1]);
    document.querySelector('input[name="project_id"]').value = params.get('project_id');
    document.querySelector('input[name="redirect_path"]').value = params.get('redirect_path');
    document.querySelector('input[name="remember_token"]').value = remember_token;
    document.querySelector('form').submit();
} else {
    // Redirect the user through the Big Local login flow, such that they will be redirected back
    // to this page when they have signed in
    let redirect_to = location.href;
    location.href = '... whatever this needs to be ...';
}
</script>
```
This will ensure that users who have bookmarked or shared links to pages in Datasette will be able to access those pages, provided they have the cookie on Big Local News that gives them access to that project.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-big-local
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
