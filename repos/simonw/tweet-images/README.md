# tweet-images

[![PyPI](https://img.shields.io/pypi/v/tweet-images.svg)](https://pypi.org/project/tweet-images/)
[![Changelog](https://img.shields.io/github/v/release/simonw/tweet-images?include_prereleases&label=changelog)](https://github.com/simonw/tweet-images/releases)
[![Tests](https://github.com/simonw/tweet-images/workflows/Test/badge.svg)](https://github.com/simonw/tweet-images/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/tweet-images/blob/master/LICENSE)

Send tweets with images from the command line

## Installation

Install this tool using `pip`:

    pip install tweet-images

## Example

This tool is used by the [@covidsewage](https://twitter.com/covidsewage) bot on Twitter, see [simonw/covidsewage-bot](https://github.com/simonw/covidsewage-bot) and [Building a Covid sewage Twitter bot](https://simonwillison.net/2022/Apr/18/covid-sewage/).

## Usage

You'll need a consumer key, consumer secret, access token key and access token secret for a Twitter account that you wish to tweet from. See [How to get credentials for a new Twitter bot](https://til.simonwillison.net/twitter/credentials-twitter-bot) for tips on obtaining these.

You can pass those as the `--consumer-key`, `--consumer-secret`, `--access-token-key`, `--access-token-secret` options to the command, or you can set them as environment variables like this:
```
export TWITTER_CONSUMER_KEY="..."
export TWITTER_CONSUMER_SECRET="..."
export TWITTER_ACCESS_TOKEN_KEY="..."
export TWITTER_ACCESS_TOKEN_SECRET=".."
```

You can then send a tweet like this:

    tweet-images "This is my tweet"

Or attach between one and four images to that tweet by passing their file paths:

    tweet-images "Three pictures attached" one.jpg two.jpg three.jpg

You can pass `--alt "alt text"` one or more times to attach alt text to your images:

    tweet-images "Three pictures attached" one.jpg two.jpg \
      --alt "Alt text for one" --alt "Alt text for two"

## Using this with GitHub Actions

Here's an example fragment from [a GitHub Actions workflow](https://github.com/simonw/covidsewage-bot/blob/bd9dcae5bcf020047955283971608507f3cd3169/.github/workflows/tweet.yml#L40-L48) that uses this tool. The repository has four repository secrets configured with the necessary credentials, and a previous step has already installed the `tweet-images` Python package:

```yaml
    - name: Tweet the new image
      env:
        TWITTER_CONSUMER_KEY: ${{ secrets.TWITTER_CONSUMER_KEY }}
        TWITTER_CONSUMER_SECRET: ${{ secrets.TWITTER_CONSUMER_SECRET }}
        TWITTER_ACCESS_TOKEN_KEY: ${{ secrets.TWITTER_ACCESS_TOKEN_KEY }}
        TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
      run: |-
        tweet-images "Latest Covid sewage charts for the SF Bay Area" \
          /tmp/covid.png --alt "Screenshot of the charts"
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd tweet-images
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
