# simonwillisonblog

[![GitHub Actions](https://github.com/simonw/simonwillisonblog/actions/workflows/ci.yml/badge.svg)](https://github.com/simonw/simonwillisonblog/actions)

The code that runs my weblog, https://simonwillison.net/

## Search Engine

This blog includes a built-in search engine. Here's how it works:

1. The search functionality is implemented in the `search` function in `blog/search.py`.
2. It uses a combination of full-text search and tag-based filtering.
3. The search index is built and updated automatically when new content is added to the blog.
4. Users can search for content using keywords, which are matched against the full text of blog entries and blogmarks.
5. The search results are ranked based on relevance and can be further filtered by tags.
6. The search interface is integrated into the blog's user interface, allowing for a seamless user experience.

For more details on the implementation, refer to the `search` function in `blog/search.py`.

## S3 Manager

The admin tools include `/tools/s3/`, backed by `s3-web-manager-django`, for browsing and uploading files to the configured S3 bucket. `S3_WEB_MANAGER_PUBLIC_URL_BASE` is set to `https://static.simonwillison.net/` so copied and viewed object URLs use the public static host plus the path in the bucket.
