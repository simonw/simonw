# openai-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/openai-to-sqlite.svg)](https://pypi.org/project/openai-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/openai-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/openai-to-sqlite/releases)
[![Tests](https://github.com/simonw/openai-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/openai-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/openai-to-sqlite/blob/main/LICENSE)

This tool provides utilities for interacting with OpenAI APIs and storing the results in a SQLite database.

See [Semantic search answers: Q&A against documentation with GPT3 + OpenAI embeddings](https://simonwillison.net/2023/Jan/13/semantic-search-answers/) for background on this project.

For a tutorial on using this for related content, see [Storing and serving related documents with openai-to-sqlite and embeddings](https://til.simonwillison.net/llms/openai-embeddings-related-content).

## Installation

Install this tool using `pip`:
```bash
pip install openai-to-sqlite
```
## Configuration

You will need an OpenAI API key to use this tool.

You can create one at https://beta.openai.com/account/api-keys

You can then either set the API key as an environment variable:
```bash
export OPENAI_API_KEY=sk-...
```
Or pass it to each command using the `--token sk-...` option.

## Calling OpenAI APIs with SQL functions

The `openai-to-sqlite query` command can be used to execute SQL queries that call OpenAI APIs.

Functions available are:

- `chatgpt(prompt)` - call the OpenAI Chat API using model `gpt-3.5-turbo` with the specified prompt.
- `chatgpt(prompt, system)` - call that API with the prompt and the specified system prompt.

More functions are planned in the future.

Here's how to use this command to run basic sentiment analysis against content in a table:
```bash
openai-to-sqlite query database.db "
  update messages set sentiment = chatgpt(
    'Sentiment analysis for this message: ' || message ||
    ' - ONLY return a lowercase string from: positive, negative, neutral, unknown'
  )
  where sentiment not in ('positive', 'negative', 'neutral', 'unknown')
    or sentiment is null
"
```
This updates the `sentiment` column in a table called `messages`. It populates it with the response from the specified prompt.

The command will display a progress bar indicating how many rows are being processed.

You can add an empty `sentiment` column to a table using [sqlite-utils](https://sqlite-utils.datasette.io/) like this:

```bash
sqlite-utils add-column database.db messages sentiment
```

## Embeddings

The `embeddings` command can be used to calculate and store [OpenAI embeddings](https://beta.openai.com/docs/guides/embeddings) for strings of text.

Each embedding has a cost, so be sure to familiarize yourself with [the pricing](https://openai.com/api/pricing/) for the embedding model.

The command can accept data in four different ways:

- As a JSON file containing a list of objects
- As a CSV file
- As a TSV file
- By running queries against a SQLite database

For all of these formats there should be an `id` column, followed by one or more text columns.

The ID will be stored as the content ID. Any other columns will be concatenated together and used as the text to be embedded.

The embeddings from the API will then be saved as binary blobs in the `embeddings` table of the specified SQLite database - or another table, if you pass the `-t/--table` option.

### JSON, CSV and TSV

Given a CSV file like this:
```csv
id,content
1,This is a test
2,This is another test
```
Embeddings can be stored like so:
```bash
openai-to-sqlite embeddings embeddings.db data.csv
```
The resulting schema looks like this:
```sql
CREATE TABLE [embeddings] (
   [id] TEXT PRIMARY KEY,
   [embedding] BLOB
);
```
The same data can be provided as TSV data:
```
id    content
1     This is a test
2     This is another test
```
Then imported like this:
```bash
openai-to-sqlite embeddings embeddings.db data.tsv
```
Or as JSON data:
```json
[
  {"id": 1, "content": "This is a test"},
  {"id": 2, "content": "This is another test"}
]
```
Imported like this:
```bash
openai-to-sqlite embeddings embeddings.db data.json
```
In each of these cases the tool automatically detects the format of the data. It does this by inspecting the data itself - it does not consider the file extension.

If the automatic detection is not working, you can pass `--format json`, `csv` or `tsv` to explicitly specify a format:

```bash
openai-to-sqlite embeddings embeddings.db data.tsv --format tsv
```
### Importing data from standard input

You can use a filename of `-` to pipe data in to standard input:

```bash
cat data.tsv | openai-to-sqlite embeddings embeddings.db -
```

### Data from a SQL query

The `--sql` option can be used to read data to be embedded from the attached SQLite database. The query must return an `id` column and one or more text columns to be embedded.

```bash
openai-to-sqlite embeddings content.db \
  --sql "select id, title from documents"
```
This will create a `embeddings` table in the `content.db` database and populate it with embeddings calculated from the `title` column in that query.

You can also store embeddings in one database while reading data from another database, using the `--attach alias filename.db` option:

```bash
openai-to-sqlite embeddings embeddings.db \
  --attach documents documents.db \
  --sql "select id, title from documents.documents"
```
A progress bar will be displayed when using `--sql` that indicates how long the embeddings are likely to take to calculate.

The CSV/TSV/JSON options do not correctly display the progress bar. You can work around this by importing your data into SQLite first (e.g. [using sqlite-utils](https://sqlite-utils.datasette.io/en/stable/cli.html#inserting-json-data)) and then running the embeddings using `--sql`.

### Batching

Embeddings will be sent to the OpenAI embeddings API in batches of 100. If you know that your data is short strings you can increase the batch size, up to 2048, using the `--batch-size` option:

```bash
openai-to-sqlite embeddings embeddings.db data.csv --batch-size 2048
```

### Working with the stored embeddings

The `embedding` column is a SQLite blob containing 1536 floating point numbers encoded as a sequence of 4 byte values.

You can extract them back to an array of floating point values in Python like this:
```python
import struct

vector = struct.unpack(
    "f" * 1536, binary_embedding
)
```

### Searching embeddings with the search command

Having saved the embeddings for content, you can run searches using the `search` command:
```bash
openai-to-sqlite search embeddings.db 'this is my search term'
```
The output will be a list of cosine similarity scores and content IDs:
```bash
openai-to-sqlite search blog.db 'cool datasette demo'
```
```
0.843 7849
0.830 8036
0.828 8195
0.826 8098
0.818 8086
0.817 8171
0.816 8121
0.815 7860
0.815 7872
0.814 8169
```

Add the `-t/--table` option if your embeddings are stored in a different table:
```bash
openai-to-sqlite search content.db 'this is my search term' -t documents

Add `--count 20` to retrieve 20 results (the default is 10).
```

### Search for similar content with the similar command

Having saved the embeddings for content, you can search for similar content with the `similar` command:
```bash
oopenai-to-sqlite similar embeddings.db '<content identifier>'
```
The output will be a list of cosine similarity scores and content IDs:
```bash
openai-to-sqlite similar embeddings-bjcp-2021.db '23G Gose'
```
```
23G Gose
  1.000 23G Gose
  0.929 24A Witbier
  0.921 23A Berliner Weisse
  0.909 05B Kölsch
  0.907 01D American Wheat Beer
  0.906 27 Historical Beer: Lichtenhainer
  0.905 23D Lambic
  0.905 10A Weissbier
  0.904 04B Festbier
  0.904 01B American Lager
```
You can pass more than one IDs to see similarities calculated for each one:
```bash
openai-to-sqlite similar embeddings-bjcp-2021.db \
  '23G Gose' '01A American Light Lager'
```
Or pass `--all` to run similarity for every item in the database. This runs similarity calculations for the number of items squared so it can be quite a long running operation:
```bash
openai-to-sqlite similar embeddings-bjcp-2021.db --all
```

### Saving similarity calculations to the database

To save these calculations to a `similarities` table in the database, use the `--save` option:
```bash
openai-to-sqlite similar embeddings-bjcp-2021.db --all --save
```
The `--save` option disables output. You can re-enable output with `--print`:
```bash
openai-to-sqlite similar embeddings-bjcp-2021.db --all --save --print
```
To save to a database table with a name other than `similarities`, use `--table`:
```bash
openai-to-sqlite similar embeddings-bjcp-2021.db \
  --all --save --table my_similarities
```

### --recalculate-for-matches

Re-calculating similarities for every row in the database can be quite a lengthy operation.

If you know which rows have just been added, you can speed things up using `--recalculate-for-matches`.

This tells `openai-to-sqlite similar` to only re-calculate similarities for rows that are close matches to the specified rows.

This means you can add one or two additional records and then trigger an update of the saved similarity scores for just those new records plus for the twenty closest matches to those new records like this:

```bash
openai-to-sqlite similar embeddings-bjcp-2021.db \
  --save '23G Gose' '01A American Light Lager' \
  --recalculate-for-matches \
  --count 20 \
  --print
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd openai-to-sqlite
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
