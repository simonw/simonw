from python_graphql_client import GraphqlClient
from datetime import datetime, timedelta, timezone
import feedparser
import httpx
import json
import pathlib
import re
import os
import sys
import time
import requests

root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")

# GitHub's GraphQL API intermittently returns these when a query is briefly
# overloaded or times out server-side. They're transient, so we retry.
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
MAX_RETRIES = 5


def execute_query(query):
    """Run a GraphQL query, retrying transient gateway errors with backoff."""
    for attempt in range(MAX_RETRIES):
        try:
            return client.execute(
                query=query,
                headers={"Authorization": "Bearer {}".format(TOKEN)},
            )
        except requests.exceptions.HTTPError as error:
            response = error.response
            status = response.status_code if response is not None else None
            if status not in RETRYABLE_STATUS or attempt == MAX_RETRIES - 1:
                raise
            print("  GraphQL {} error, retrying...".format(status))
        except requests.exceptions.RequestException:
            if attempt == MAX_RETRIES - 1:
                raise
            print("  GraphQL network error, retrying...")
        time.sleep(2**attempt)

TOKEN = os.environ.get("SIMONW_TOKEN", "")

OWNERS = "owner:simonw owner:dogsheep owner:datasette"

# How many hours back the scheduled (incremental) run looks at. The workflow
# runs hourly, so 3 hours gives a comfortable overlap in case a run is skipped.
INCREMENTAL_HOURS = 3

SKIP_REPOS = {
    "playing-with-actions",
    "simonw-readthedocs-experiments",
    "datasette-comments",
    "datasette-plot",
    "datasette-write-ui",
    "datasette-litestream",
    "datasette-metadata-editable",
    "datasette-short-links",
}


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


# Single search query template. QUERY_STRING and AFTER are substituted in. Each
# repo node carries its README (a few common filename spellings are requested as
# aliases) so we never need a second fetch to mirror it.
GRAPHQL_SEARCH_QUERY = """
query {
  search(first: 100, type: REPOSITORY, query: "QUERY_STRING", after: AFTER) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      __typename
      ... on Repository {
        name
        description
        url
        owner {
          login
        }
        readme_md: object(expression: "HEAD:README.md") { ... on Blob { text } }
        readme_markdown: object(expression: "HEAD:README.markdown") { ... on Blob { text } }
        readme_lower: object(expression: "HEAD:readme.md") { ... on Blob { text } }
        readme_rst: object(expression: "HEAD:README.rst") { ... on Blob { text } }
        readme_plain: object(expression: "HEAD:README") { ... on Blob { text } }
        releases(orderBy: {field: CREATED_AT, direction: DESC}, first: 100) {
          totalCount
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            name
            publishedAt
            url
            author {
              login
            }
          }
        }
      }
    }
  }
}
"""

RELEASES_CACHE_PATH = root / "releases_cache.json"
REPOS_DIR = root / "repos"

GRAPHQL_REPO_RELEASES_QUERY = """
query {
  repository(owner: "OWNER", name: "NAME") {
    releases(orderBy: {field: CREATED_AT, direction: DESC}, first: 100, after: AFTER) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        publishedAt
        url
        author {
          login
        }
      }
    }
  }
}
"""


def everything_query():
    """Search query matching every public repo across the owners."""
    return "is:public {} sort:updated".format(OWNERS)


def incremental_query(hours=INCREMENTAL_HOURS):
    """Search query limited to repos pushed within the last `hours` hours."""
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return "is:public {} pushed:>{} sort:updated".format(OWNERS, since)


def build_search_query(query_string, after_cursor):
    return GRAPHQL_SEARCH_QUERY.replace("QUERY_STRING", query_string).replace(
        "AFTER", '"{}"'.format(after_cursor) if after_cursor else "null"
    )


def make_release_entry(repo_name, release_node):
    """Build a release dict from a GraphQL release node."""
    return {
        "release": release_node["name"].replace(repo_name, "").strip(),
        "published_at": release_node["publishedAt"],
        "published_day": release_node["publishedAt"].split("T")[0],
        "url": release_node["url"],
    }


def make_release_entry_with_author(repo_name, release_node):
    """Release dict including the author login, for the per-repo releases.json."""
    entry = make_release_entry(repo_name, release_node)
    entry["author"] = (release_node.get("author") or {}).get("login")
    return entry


def filter_releases_by_author(repo_name, release_nodes):
    """Return release entries for releases authored by simonw."""
    releases = []
    for node in release_nodes:
        author = (node.get("author") or {}).get("login")
        if author != "simonw":
            continue
        releases.append(make_release_entry(repo_name, node))
    return releases


def paginate_repo_releases(oauth_token, owner, name, after_cursor):
    """Return all remaining raw release nodes for a single repo."""
    nodes = []
    has_next_page = True

    while has_next_page:
        query = (
            GRAPHQL_REPO_RELEASES_QUERY.replace("OWNER", owner)
            .replace("NAME", name)
            .replace("AFTER", '"{}"'.format(after_cursor) if after_cursor else "null")
        )
        data = execute_query(query)
        releases_data = data["data"]["repository"]["releases"]
        nodes.extend(releases_data["nodes"])

        page_info = releases_data["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        after_cursor = page_info["endCursor"]

    return nodes


def fetch_all_repo_releases(oauth_token, owner, name, after_cursor):
    """Paginate remaining releases for a repo, keeping only simonw-authored ones."""
    nodes = paginate_repo_releases(oauth_token, owner, name, after_cursor)
    return [
        make_release_entry(name, node)
        for node in nodes
        if (node.get("author") or {}).get("login") == "simonw"
    ]


def collect_all_releases(repo):
    """All releases (every author) for a repo, fully paginated, for releases.json."""
    rel = repo["releases"]
    if not rel["totalCount"]:
        return []
    nodes = list(rel["nodes"])
    if rel["pageInfo"]["hasNextPage"]:
        nodes.extend(
            paginate_repo_releases(
                TOKEN, repo["owner"]["login"], repo["name"], rel["pageInfo"]["endCursor"]
            )
        )
    return [make_release_entry_with_author(repo["name"], node) for node in nodes]


def load_releases_cache():
    """Load cached releases from JSON file, keyed by repo name."""
    if RELEASES_CACHE_PATH.exists():
        return json.loads(RELEASES_CACHE_PATH.read_text())
    return {}


def save_releases_cache(cache):
    """Save releases cache to JSON file."""
    RELEASES_CACHE_PATH.write_text(json.dumps(cache, indent=2, sort_keys=True))


def pick_readme(repo):
    """Return the first available README text from the aliased blob fields."""
    for key in ("readme_md", "readme_markdown", "readme_lower", "readme_rst", "readme_plain"):
        obj = repo.get(key)
        if obj and obj.get("text"):
            return obj["text"]
    return None


def update_cache_releases(cache, repo, full_release_pagination):
    """Merge a repo's releases into the cache. Returns nothing; mutates cache."""
    name = repo["name"]
    total = repo["releases"]["totalCount"]
    if not total:
        return

    new_releases = filter_releases_by_author(name, repo["releases"]["nodes"])

    # Only the seed/full run deep-paginates repos with >100 releases; the
    # incremental run relies on the cache already holding the older ones.
    if full_release_pagination and repo["releases"]["pageInfo"]["hasNextPage"]:
        new_releases.extend(
            fetch_all_repo_releases(
                TOKEN,
                repo["owner"]["login"],
                name,
                repo["releases"]["pageInfo"]["endCursor"],
            )
        )

    if name in cache:
        existing_urls = {r["url"] for r in cache[name]["releases"]}
        for release in new_releases:
            if release["url"] not in existing_urls:
                cache[name]["releases"].append(release)
        cache[name]["releases"].sort(key=lambda r: r["published_at"], reverse=True)
        cache[name]["description"] = repo["description"]
        cache[name]["total_releases"] = total
    elif new_releases:
        cache[name] = {
            "repo": name,
            "repo_url": repo["url"],
            "description": repo["description"],
            "total_releases": total,
            "releases": new_releases,
        }


def write_repo_files(repo, all_releases):
    """Write repos/<owner>/<repo>/README.md and releases.json for one repo."""
    owner = repo["owner"]["login"]
    name = repo["name"]
    repo_dir = REPOS_DIR / owner / name
    repo_dir.mkdir(parents=True, exist_ok=True)

    readme_text = pick_readme(repo)
    if readme_text is not None:
        (repo_dir / "README.md").write_text(readme_text)

    releases_json = {
        "repo": name,
        "owner": owner,
        "url": repo["url"],
        "description": repo["description"],
        "total_releases": repo["releases"]["totalCount"],
        "releases": all_releases,
    }
    (repo_dir / "releases.json").write_text(
        json.dumps(releases_json, indent=2, sort_keys=True)
    )


def fetch_repos(query_string):
    """Paginate the repo search and return every matching repo node."""
    nodes = []
    after_cursor = None
    has_next_page = True

    while has_next_page:
        data = execute_query(build_search_query(query_string, after_cursor))
        search = data["data"]["search"]
        nodes.extend(search["nodes"])
        page_info = search["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        after_cursor = page_info["endCursor"]

    return nodes


def build(query_string, full_release_pagination):
    """Scan repos matching query_string, mirror their files, update the cache."""
    cache = load_releases_cache()
    repo_nodes = fetch_repos(query_string)

    written = 0
    for repo in repo_nodes:
        if repo["name"] in SKIP_REPOS:
            continue
        update_cache_releases(cache, repo, full_release_pagination)
        write_repo_files(repo, collect_all_releases(repo))
        written += 1

    save_releases_cache(cache)
    print("Scanned {} repos, wrote files for {}".format(len(repo_nodes), written))
    return cache


def most_recent_releases(cache):
    """Extract the most recent release per repo from the cache, for display."""
    releases = []
    for repo_data in cache.values():
        if not repo_data["releases"]:
            continue
        latest = repo_data["releases"][0]
        releases.append(
            {
                "repo": repo_data["repo"],
                "repo_url": repo_data["repo_url"],
                "description": repo_data["description"],
                "total_releases": repo_data["total_releases"],
                **latest,
            }
        )
    return releases


def fetch_tils():
    sql = """
        select path, replace(title, '_', '\_') as title, url, topic, slug, created_utc
        from til order by created_utc desc limit 6
    """.strip()
    return httpx.get(
        "https://til.simonwillison.net/tils.json",
        params={
            "sql": sql,
            "_shape": "array",
        },
    ).json()


def fetch_blog_entries():
    entries = feedparser.parse("https://simonwillison.net/atom/entries/")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = root / "README.md"
    project_releases = root / "releases.md"

    # --all (or --seed) scans every repo; an empty cache forces a full scan too.
    # Otherwise the scheduled run only looks at repos pushed in the last few hours.
    if (
        "--all" in sys.argv
        or "--seed" in sys.argv
        or not RELEASES_CACHE_PATH.exists()
    ):
        print("Running full scan against every repo...")
        cache = build(everything_query(), full_release_pagination=True)
    else:
        print(
            "Running incremental scan (repos pushed in the last {} hours)...".format(
                INCREMENTAL_HOURS
            )
        )
        cache = build(incremental_query(), full_release_pagination=False)

    releases = most_recent_releases(cache)
    releases.sort(key=lambda r: r["published_at"], reverse=True)
    md = "\n\n".join(
        [
            "[{repo} {release}]({url}) - {published_day}".format(**release)
            for release in releases[:8]
        ]
    )
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "recent_releases", md)

    # Write out full project-releases.md file
    project_releases_md = "\n".join(
        [
            (
                "* **[{repo}]({repo_url})**: [{release}]({url}) {total_releases_md}- {published_day}\n"
                "<br />{description}"
            ).format(
                total_releases_md="- ([{} releases total]({}/releases)) ".format(
                    release["total_releases"], release["repo_url"]
                )
                if release["total_releases"] > 1
                else "",
                **release
            )
            for release in releases
        ]
    )
    project_releases_content = project_releases.open().read()
    project_releases_content = replace_chunk(
        project_releases_content, "recent_releases", project_releases_md
    )
    project_releases_content = replace_chunk(
        project_releases_content, "project_count", f"{len(releases):,}", inline=True
    )
    project_releases_content = replace_chunk(
        project_releases_content,
        "releases_count",
        "{:,}".format(sum(r["total_releases"] for r in releases)),
        inline=True,
    )
    project_releases.open("w").write(project_releases_content)

    tils = fetch_tils()
    tils_md = "\n\n".join(
        [
            "[{title}](https://til.simonwillison.net/{topic}/{slug}) - {created_at}".format(
                title=til["title"],
                topic=til["topic"],
                slug=til["slug"],
                created_at=til["created_utc"].split("T")[0],
            )
            for til in tils
        ]
    )
    rewritten = replace_chunk(rewritten, "tils", tils_md)

    entries = fetch_blog_entries()[:6]
    entries_md = "\n\n".join(
        ["[{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(rewritten, "blog", entries_md)

    readme.open("w").write(rewritten)
