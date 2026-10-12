# actions-latest

Keeping track of the latest versions of various GitHub Actions

https://simonw.github.io/actions-latest/versions.txt

Access that URL for a list of all of the official Actions belonging to the [GitHub Actions](https://github.com/actions) organization along with their latest version tags.

You can point coding agents such as Claude Code and Codex CLI at this URL so they know the most recent Actions versions to use in their workflow files.

The daily update authenticates GitHub API requests using the workflow's `GITHUB_TOKEN`. To update locally, set `GITHUB_TOKEN` (or `GH_TOKEN`) in your environment and run `uv run fetch_versions.py`.

Every repository is checked on each run. `unversioned.txt` records repositories with no matching tags; it is not used to skip future checks. API errors or an empty version list stop the update before any generated files are overwritten.

<!-- VERSIONS_START -->
## Latest versions

```
actions/actions-sync@v202610071604
actions/add-to-project@v2
actions/ai-inference@v3
actions/attest@v4
actions/attest-build-provenance@v4
actions/attest-sbom@v4
actions/cache@v6
actions/checkout@v7
actions/configure-pages@v6
actions/create-github-app-token@v3
actions/create-release@v1
actions/delete-package-versions@v5
actions/dependency-review-action@v3
actions/deploy-pages@v5
actions/download-artifact@v8
actions/first-interaction@v3
actions/github-script@v9
actions/go-dependency-submission@v2
actions/hello-world-docker-action@v2
actions/hello-world-javascript-action@v1
actions/javascript-action@v1
actions/jekyll-build-pages@v1
actions/labeler@v7
actions/publish-immutable-action@v0
actions/setup-dotnet@v6
actions/setup-elixir@v1
actions/setup-go@v7
actions/setup-haskell@v1
actions/setup-java@v6
actions/setup-node@v7
actions/setup-python@v7
actions/setup-ruby@v1
actions/stale@v11
actions/upload-artifact@v7
actions/upload-code-coverage@v1
actions/upload-pages-artifact@v5
actions/upload-release-asset@v1
```
<!-- VERSIONS_END -->
