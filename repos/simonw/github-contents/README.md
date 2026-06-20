# github-contents

[![PyPI](https://img.shields.io/pypi/v/github-contents.svg)](https://pypi.org/project/github-contents/)
[![Changelog](https://img.shields.io/github/v/release/simonw/github-contents?include_prereleases&label=changelog)](https://github.com/simonw/github-contents/releases)
[![Tests](https://github.com/simonw/github-contents/workflows/Test/badge.svg)](https://github.com/simonw/github-contents/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/github-contents/blob/main/LICENSE)

Read and write both small and large files to Github.

The regular [GitHub Contents API](https://developer.github.com/v3/repos/contents/) can't handle files larger than 1MB - this class knows how to spot that problem and switch to the large-file-supporting low level [Git Data API](https://developer.github.com/v3/git/) instead.

Note that file contents is passed and returned as bytestrings, not regular strings.

## Installation

    pip install github-contents

## Usage

You will need a GitHub OAuth token with full repository access.

The easiest way to create one of these is using [https://github.com/settings/tokens](https://github.com/settings/tokens)

```python
from github_contents import GithubContents

# For repo simonw/disaster-data:
github = GithubContents(
    "simonw",
    "disaster-data",
    token=GITHUB_OAUTH_TOKEN,
    branch="main"
)
```
To read a file:
```python
content_in_bytes, sha = github.read(path_within_repo)
```
To write a file:
```python
content_sha, commit_sha = github.write(
    filepath=path_within_repo,
    content_bytes=contents_in_bytes,
    sha=previous_sha, # Optional
    commit_message=commit_message,
    committer={
        "name": COMMITTER_NAME,
        "email": COMMITTER_EMAIL,
    },
)
```
