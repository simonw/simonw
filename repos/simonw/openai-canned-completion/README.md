# openai-canned-completion

Tiny app running on Vercel for simulating a portion of the OpenAI API

This is running at `https://openai-canned-completion.vercel.app/` - but visiting that URL directly is a bad idea as it will just download a weird file.

The only purpose of this app is to support the following mechanism for testing [LLM](https://llm.datasette.io/):

```bash
OPENAI_API_KEY='x' \
OPENAI_API_BASE='https://openai-canned-completion.vercel.app/v1' \
llm 'hello'
```
This will output:
```
Hello! How can I assist you today?
```
I built this to support submitting LLM to Homebrew, since I needed a test that could be included in the Homebrew Formula:

- [Submit LLM to Homebrew](https://github.com/simonw/llm/issues/124)
- [llm 0.6 (new formula)](https://github.com/Homebrew/homebrew-core/pull/137353)

## Deployment

Run this in the directory:
```
vercel --prod
```
It is deployed to the Datasette scope.
