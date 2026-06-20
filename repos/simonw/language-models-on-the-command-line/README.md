# Language models on the command-line

Notes for a talk I gave at [Mastering LLMs: A Conference For Developers & Data Scientists](https://maven.com/parlance-labs/fine-tuning).

Here is the [full 67 minute talk video](https://twitter.com/hamelhusain/status/1800741994899394612).

- [Datasette](https://datasette.io/)
- [My blog](https://simonwillison.net/)
- [LLM](https://llm.datasette.io/en/stable/)

## Getting started 

```bash
brew install llm # or pipx or pip
llm keys set openai
# paste key here
llm "Say hello in Spanish"
```
## Installing Claude 3
```bash
llm install llm-claude-3
llm keys set claude
# Paste key here
llm -m haiku 'Say hello from Claude Haiku'
```

## Local model with llm-gpt4all

```bash
llm install llm-gpt4all
llm models
llm chat -m mistral-7b-instruct-v0
```
## Browsing logs with Datasette

https://datasette.io/

```bash
pipx install datasette # or brew or pip
datasette "$(llm logs path)"
# Browse at http://127.0.0.1:8001/
```
### Templates
```bash
llm --system 'You are a sentient cheesecake' -m gpt-4o --save cheesecake
```
Now you can chat with a cheesecake:
```bash
llm chat -t cheesecake
```

More plugins: https://llm.datasette.io/en/stable/plugins/directory.html

### llm-cmd

Help with shell commands. Blog entry is here: https://simonwillison.net/2024/Mar/26/llm-cmd/

### files-to-prompt and shot-scraper

`files-to-prompt` is described here: 
https://simonwillison.net/2024/Apr/8/files-to-prompt/

`shot-scraper javascript` documentation: https://shot-scraper.datasette.io/en/stable/javascript.html

JSON output for Google search results:

```bash
shot-scraper javascript 'https://www.google.com/search?q=nytimes+slop' '
Array.from(
  document.querySelectorAll("h3"),
  el => ({href: el.parentNode.href, title: el.innerText})
)'
```
This version gets the HTML that includes the snippet summaries, then pipes it to LLM to answer a question:
```bash
shot-scraper javascript 'https://www.google.com/search?q=nytimes+slop' '
() => {
    function findParentWithHveid(element) {
        while (element && !element.hasAttribute("data-hveid")) {
            element = element.parentElement;
        }
        return element;
    }
    return Array.from(
        document.querySelectorAll("h3"),
        el => findParentWithHveid(el).innerText
    );
}' | llm -s 'describe slop'
```
### Hacker news summary

https://til.simonwillison.net/llms/claude-hacker-news-themes describes my Hacker News summary script in detail.

### Embeddings

Full documentation: https://llm.datasette.io/en/stable/embeddings/index.html

I ran this:

```bash
curl -O https://datasette.simonwillison.net/simonwillisonblog.db
llm embed-multi links \
  -d simonwillisonblog.db \
  --sql 'select id, link_url, link_title, commentary from blog_blogmark' \
  -m 3-small --store
```
Then looked for items most similar to a string like this:
```bash
llm similar links \
  -d simonwillisonblog.db \
  -c 'things that make me angry'
```

### More links

- [Coping strategies for the serial project hoarder](https://simonwillison.net/2022/Nov/26/productivity/) talk about personal productivity on different projects
- [Figure out how to serve an AWS Lambda function with a Function URL from a custom subdomain](https://github.com/simonw/public-notes/issues/1) as an example of how I use GitHub Issues
