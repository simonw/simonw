# datasette-openai

[![PyPI](https://img.shields.io/pypi/v/datasette-openai.svg)](https://pypi.org/project/datasette-openai/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-openai?include_prereleases&label=changelog)](https://github.com/simonw/datasette-openai/releases)
[![Tests](https://github.com/simonw/datasette-openai/workflows/Test/badge.svg)](https://github.com/simonw/datasette-openai/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-openai/blob/main/LICENSE)

SQL functions for calling OpenAI APIs

See [Semantic search answers: Q&A against documentation with GPT3 + OpenAI embeddings](https://simonwillison.net/2023/Jan/13/semantic-search-answers/) for background on this project.

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-openai

## ⚠️ Warning ⚠️

This plugin allows you to call a commercial, priced API using SQL queries.

Use this with care! You could accidentally spend a lot of money.

For example, the following query:

```sql
select
  openai_davinci(
    'Summarize this text: ' || content, 200, 1, :api_key
) as summary
from documents
```
Would execute one paid API call for every item in the `documents` database. This could become very expensive.

Be sure to familiarize yourself with [OpenAI pricing](https://openai.com/api/pricing/). You will need to obtain an [API key](https://beta.openai.com/account/api-keys).

## Usage

This extension provides three new SQL functions:

### openai_davinci(prompt, max_tokens, temperature, api_key)

This function runs a `text-davinci-003` completion against the provided prompt, with the specified values for max tokens and temperature.

Da Vinci is currently 2 cents per thousand tokens.

### openai_embedding(text, api_key)

This calls the OpenAI embedding endpoint and returns a binary object representing the floating point embedding for the provided text.

```sql
select openai_embedding(:query, :api_key)
```
An embedding is an array of 1536 floating point values. The returned value from this is a `blob` encoding of those values.

It's mainly useful for using with the `openai_embedding_similarity()` function.

The embedding API is very inexpensive: at time of writing, $0.0004 cents per thousand tokens, where a token is more-or-less a single word.

### openai_embedding_similarity(a, b)

This function does not make any API calls. It takes two embedding blobs and returns the cosine similarity between the two.

This function is particularly useful if you have stored embeddings of documents in a database table, and you want to find the most similar documents to a query or to another document.

A simple search query could look like this:
```sql
with query as (
  select
    openai_embedding(:query, :token) as q
)
select
  id,
  title,
  openai_embedding_similarity(query.q, embedding) as score
from
  content, query
order by
  score desc
limit 10
```

### openai_build_prompt(text, prefix, suffix, completion_tokens, token_limit=4000)

This aggregate function helps build a prompt from a number of inputs in a way that fits the GPT-3 prompt size limit.

It takes the following argument:

- `text` - this is the column that is being aggregated, so the function expects to have multiple values for this. All other arguments will only be read the first time they are passed, so should be consistent across all calls to the function.
- `prefix` - text to use for the prefix of the prompt
- `suffix` - text to use for the suffix of the prompt
- `completion_tokens` - the number of tokens to reserve for the prompt response - this will be subtracted from the token limit
- `token_limit` - this value is optional (there are 4-argument and 5-argument versions of the function registered). It defaults to the GPT-3 Da Vinci size limit of 4,000 tokens but can be changed if the model the prompt is being used with has a different size limit.

Here's an example usage of this function, adapted from [this article](https://simonwillison.net/2023/Jan/13/semantic-search-answers/):

```sql
with top_n as (
  select body from blog_entry order by id desc limit 3
)
select openai_build_prompt(body, 'Context:
------------
', '
------------
Given the above context, answer the following question: ' || :question,
  500,
  2000
  ) from top_n
```
[Try that here](https://datasette.simonwillison.net/simonwillisonblog?sql=with+top_n+as+%28%0D%0A++select+body+from+blog_entry+order+by+id+desc+limit+5%0D%0A%29%0D%0Aselect+openai_build_prompt%28body%2C+%27Context%3A%0D%0A------------%0D%0A%27%2C+%27%0D%0A------------%0D%0AGiven+the+above+context%2C+answer+the+following+question%3A+%27+%7C%7C+%3Aquestion%2C%0D%0A++500%2C%0D%0A++2000%0D%0A++%29+from+top_n&question=Examples+of+a+language+model%3F).

This query first retrieves the three most recent blog entries, then constructs a prompt that with the provided prefix and suffix designed to fit 1500 tokens (2000 total, minus 500 reserved for the response).

The output looks something like this (truncated for space):

```
Context:
------------
< p > If you 've spent any time with GPT - 3 or ChatGPT , you 've likely thought about how ...
I release Datasette 0 . 64 this morning . This release is mainly a response to the realization that it 's not safe to run Datasette with the SpatiaLite extension loaded if that Datasette instance is configured to enable arbitrary SQL queries from untrusted users ...
In lieu of my regular weeknotes ( I took two weeks off for the holidays ) here 's a look back at 2022 , mainly in terms of projects and things I 've written about ...
------------
Given the above context, answer the following question: Examples of a language model?
```
The body of each entry has been truncated to the number of tokens that will allow examples from all three entries to be included in the generated prompt.

### openai_strip_tags(text)

Sometimes it can be useful to strip HTML tags from text in order to reduce the number of tokens used. This function does a very simple version of tag stripping - just removing anything that matches `<...>`.

### openai_tokenize(text)

Returns a JSON array of tokens for the provided text.

This uses a regular expression [extracted from OpenAI's GPT-2](https://github.com/openai/gpt-2/blob/a74da5d99abaaba920de8131d64da2862a8f213b/src/encoder.py#L53).

### openai_count_tokens(text)

Returns a count of the number of tokens in the provided text.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-openai
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
