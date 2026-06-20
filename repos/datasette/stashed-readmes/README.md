# stashed-readmes

The [Datasette](https://datasette.io/) website displays rendered READMEs for all of the plugins and tools in the Datasette ecosystem.

GitHub rate limits rendering these, so this repo keeps stashed copies of the Markdown and HTML for all of them.

It also rewrites image references in them to avoid unstable references to `camo.githubusercontent.com`.

## What the fetch_all.py script does

- Accepts a URL that returns a JSON structure specifying a list of GitHub repositories, each with:
  - `repo`: repository name in the form `owner/repo`
  - `pushed_at`: ISO timestamp of the last push to the repository
  
- Loads a local snapshot from a file called `repos.json` (if present) to compare previous timestamps.

- Fetches and parses the live list of repositories and their last pushed dates from the given URL.

- Identifies which repositories have changed since the last run by comparing `pushed_at` timestamps.

- For each changed (or new) repository:
  - Downloads the raw `README.md` file from the GitHub API.
  - Downloads the rendered HTML version of the same README.
  - Saves both files under directory structure `owner/repo/README.md` and `owner/repo/README.html`.

- Updates `repos.json` with the current repository list and timestamps so subsequent runs only fetch changed repos.

- Respects a configurable delay between HTTP requests to avoid hitting rate limits or overloading servers (`--sleep`, defaults to 1 second).
