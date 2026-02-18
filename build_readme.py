from python_graphql_client import GraphqlClient
import feedparser
import httpx
import json
import pathlib
import re
import os
import sys

root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")

TOKEN = os.environ.get("SIMONW_TOKEN", "")

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


GRAPHQL_SEARCH_QUERY = """
query {
  search(first: 100, type:REPOSITORY, query:"is:public owner:simonw owner:dogsheep owner:datasette sort:updated") {
    nodes {
      __typename
      ... on Repository {
        name
        description
        url
        owner {
          login
        }
        releases(orderBy: {field: CREATED_AT, direction: DESC}, first: 10) {
          totalCount
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

GRAPHQL_SEARCH_QUERY_PAGINATED = """
query {
  search(first: 100, type:REPOSITORY, query:"is:public owner:simonw owner:dogsheep owner:datasette sort:updated", after: AFTER) {
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


def make_release_entry(repo_name, release_node):
    """Build a release dict from a GraphQL release node."""
    return {
        "release": release_node["name"].replace(repo_name, "").strip(),
        "published_at": release_node["publishedAt"],
        "published_day": release_node["publishedAt"].split("T")[0],
        "url": release_node["url"],
    }


def filter_releases_by_author(repo_name, release_nodes):
    """Return release entries for releases authored by simonw."""
    releases = []
    for node in release_nodes:
        author = (node.get("author") or {}).get("login")
        if author != "simonw":
            continue
        releases.append(make_release_entry(repo_name, node))
    return releases


def fetch_all_repo_releases(oauth_token, owner, name, after_cursor):
    """Paginate through remaining releases for a single repo."""
    releases = []
    has_next_page = True

    while has_next_page:
        query = (
            GRAPHQL_REPO_RELEASES_QUERY.replace("OWNER", owner)
            .replace("NAME", name)
            .replace("AFTER", '"{}"'.format(after_cursor) if after_cursor else "null")
        )
        data = client.execute(
            query=query,
            headers={"Authorization": "Bearer {}".format(oauth_token)},
        )
        releases_data = data["data"]["repository"]["releases"]
        for node in releases_data["nodes"]:
            author = (node.get("author") or {}).get("login")
            if author != "simonw":
                continue
            releases.append(make_release_entry(name, node))

        page_info = releases_data["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        after_cursor = page_info["endCursor"]

    return releases


def load_releases_cache():
    """Load cached releases from JSON file, keyed by repo name."""
    if RELEASES_CACHE_PATH.exists():
        return json.loads(RELEASES_CACHE_PATH.read_text())
    return {}


def save_releases_cache(cache):
    """Save releases cache to JSON file."""
    RELEASES_CACHE_PATH.write_text(json.dumps(cache, indent=2, sort_keys=True))


def seed_releases_cache(oauth_token):
    """Fetch ALL releases via pagination to seed the cache. Run once with --seed."""
    cache = {}
    has_next_page = True
    after_cursor = None

    while has_next_page:
        query = GRAPHQL_SEARCH_QUERY_PAGINATED.replace(
            "AFTER", '"{}"'.format(after_cursor) if after_cursor else "null"
        )
        data = client.execute(
            query=query,
            headers={"Authorization": "Bearer {}".format(oauth_token)},
        )
        print(json.dumps(data, indent=4))

        repo_nodes = data["data"]["search"]["nodes"]
        for repo in repo_nodes:
            if repo["name"] in SKIP_REPOS:
                continue
            if not repo["releases"]["totalCount"]:
                continue

            releases = filter_releases_by_author(
                repo["name"], repo["releases"]["nodes"]
            )

            # Paginate if this repo has more releases
            release_page_info = repo["releases"]["pageInfo"]
            if release_page_info["hasNextPage"]:
                owner = repo["owner"]["login"]
                print(
                    f"  Paginating releases for {owner}/{repo['name']}..."
                )
                releases.extend(
                    fetch_all_repo_releases(
                        oauth_token,
                        owner,
                        repo["name"],
                        release_page_info["endCursor"],
                    )
                )

            if releases:
                cache[repo["name"]] = {
                    "repo": repo["name"],
                    "repo_url": repo["url"],
                    "description": repo["description"],
                    "total_releases": repo["releases"]["totalCount"],
                    "releases": releases,
                }

        after_cursor = data["data"]["search"]["pageInfo"]["endCursor"]
        has_next_page = after_cursor

    save_releases_cache(cache)
    total_releases = sum(len(r["releases"]) for r in cache.values())
    print(f"Seeded cache with {len(cache)} repos, {total_releases} releases")
    return cache


def fetch_and_update_releases(oauth_token):
    """Fetch recent releases and merge into cache. Returns cache dict."""
    # Load existing cache
    cache = load_releases_cache()

    # Fetch the 100 most recently updated repos (single API call)
    data = client.execute(
        query=GRAPHQL_SEARCH_QUERY,
        headers={"Authorization": "Bearer {}".format(oauth_token)},
    )
    print()
    print(json.dumps(data, indent=4))
    print()

    # Update cache with fresh data
    repo_nodes = data["data"]["search"]["nodes"]
    for repo in repo_nodes:
        if repo["name"] in SKIP_REPOS:
            continue
        if not repo["releases"]["totalCount"]:
            continue

        new_releases = filter_releases_by_author(
            repo["name"], repo["releases"]["nodes"]
        )

        if repo["name"] in cache:
            # Merge: add any new releases not already in cache
            existing_urls = {r["url"] for r in cache[repo["name"]]["releases"]}
            for release in new_releases:
                if release["url"] not in existing_urls:
                    cache[repo["name"]]["releases"].append(release)
            # Re-sort by published_at descending
            cache[repo["name"]]["releases"].sort(
                key=lambda r: r["published_at"], reverse=True
            )
            # Update repo metadata
            cache[repo["name"]]["description"] = repo["description"]
            cache[repo["name"]]["total_releases"] = repo["releases"]["totalCount"]
        elif new_releases:
            cache[repo["name"]] = {
                "repo": repo["name"],
                "repo_url": repo["url"],
                "description": repo["description"],
                "total_releases": repo["releases"]["totalCount"],
                "releases": new_releases,
            }

    # Save updated cache
    save_releases_cache(cache)

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

    if "--seed" in sys.argv or not RELEASES_CACHE_PATH.exists():
        print("Seeding releases cache with full pagination...")
        cache = seed_releases_cache(TOKEN)
    else:
        cache = fetch_and_update_releases(TOKEN)

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
