# docs-for-llms

This repo contains single file concatenated documentation for every released version of [LLM](https://llm.datasette.io/) and several other tools.

It's designed to work with the [llm-docs](https://github.com/simonw/llm-docs) plugin:

```bash
llm install llm-docs
llm -f docs:llm 'how do I embed a binary file?'
```
Asking more questions about the same documentation - or asking follow-up questions using `llm -c` or even `llm chat -c` - will benefit from OpenAI's token cache pricing.

Projects represented here:

- [datasette](https://github.com/simonw/datasette) (this is a large one)
- `datasette-plugins` is the subset of that documentation needed for writing Datasette plugins
- [llm](https://github.com/simonw/llm)
- [s3-credentials](https://github.com/simonw/s3-credentials)
- [shot-scraper](https://github.com/simonw/shot-scraper)
- [sqlite-utils](https://github.com/simonw/sqlite-utils)

Note that some of these files are a little large though:

```bash
curl -s 'https://raw.githubusercontent.com/simonw/docs-for-llms/refs/heads/main/datasette/1.0a16.txt' \
  | ttok
```
> 152131

That's 152,000 tokens - too large for `gpt-4o-mini` and potentially quite expensive to process (but fits easily within the 1 million token limits of both the Gemini and the GPT-4.1 models).
