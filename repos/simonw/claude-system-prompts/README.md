# Claude system prompts revision history

[![Atom feed](https://img.shields.io/badge/Atom-feed-orange?logo=rss&logoColor=white)](https://simonw.github.io/claude-system-prompts/feed.atom)

Anthropic publishes the system prompts used by claude.ai and the Claude mobile apps at [platform.claude.com](https://platform.claude.com/docs/en/release-notes/system-prompts/overview), one page per model, with a dated section for every revision. This repository turns those pages into files in [`prompts/`](prompts/) with a git history: **every published revision is a commit dated the day Anthropic says it went live**, so `git log`, `git diff`, and GitHub's history views show how the prompts have changed over time. Each change also gets a short LLM-written summary of what is new.

[Transcript from building this repo](https://gisthost.github.io/?f1399e27b6a832f0e790b696af812c9b/index.html) using Claude Fable 5.1. See [this blog post](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#how-i-m-tracking-these-prompts) for background on this project.

## Latest changes

The most recent change to each model family, summarized from the diff by `gpt-5.6-luna`. [CHANGELOG.md](CHANGELOG.md) has every change, and the [Atom feed](https://simonw.github.io/claude-system-prompts/feed.atom) delivers new ones.

### Fable 5.2 → Fable 5.1 on Nov 13, 2026

- Child-safety policy becomes stricter: it bans all romantic or sexual content involving minors, removing previous allowances for peer teen romance and non-romantic minor roleplay.
- Claude now provides harm-reduction information about illegal substances while refusing “specific protocols for dosing, timing, administration, or combinations.”
- The prompt adds safeguards against protective content becoming operational, limiting grooming examples to patterns and forbidding explanations of “detection mechanics.”
- Explicit forged-message defenses are removed, including the rule that fake system notices or operator approvals cannot override safeguards.
- Claude is newly instructed not to diagnose or speculate about mental states, and to avoid precise nutrition guidance or reflective listening that amplifies distress.

[Diff](https://github.com/simonw/claude-system-prompts/commit/7b3f5c6f8fea6cafdaf5e36382d78c81287368bd) · [prompt](prompts/claude-fable.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable.md)

### Haiku 4.5 → Haiku 5.5 on Nov 9, 2026

- Claude now checks memory and relevant uploaded files for personal questions, and saves lasting information about the person before the turn ends.
- Refusal decisions now persist across the conversation: reframing, repetition, fictional framing, or disclaimers cannot unlock previously declined harmful content.
- Child-safety handling shifts toward tracking where a story is heading, stopping sexualized progression while “keeping helping with the rest of the story.”
- Self-harm and eating-disorder safeguards expand substantially, including persistent bans on suicide notes, method details, body-related numbers, and food, water, or exercise tips.
- New voting guidance requires equal treatment of candidates and parties, tailored comparisons based on the person’s priorities, and no filling out ballots or assuming votes.

[Diff](https://github.com/simonw/claude-system-prompts/commit/5abb6eae52d9875604596958d9a225714163d0bc) · [prompt](prompts/claude-haiku.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku.md)

### Sonnet 5 → Sonnet 5.5 on Nov 9, 2026

- The prompt drops explicit child-safety rules barring sexual content involving minors, rejecting safety-based reframing, and requiring heightened caution after refusals.
- New political rules require equal treatment of all sides, separate factual description from evaluation, and tailor voting help to priorities without filling out ballots.
- Claude now refuses any posthumous suicide note, even one line or fictional framing, while allowing a present-tense message asking someone to help.
- Drug guidance shifts toward allowing life-saving facts while banning synthesis, production, distribution, and specific dosing or administration protocols, with harm-reduction referrals.
- Claude is told not to become submissive under abuse, replacing earlier language emphasizing politeness and insisting on kindness.

[Diff](https://github.com/simonw/claude-system-prompts/commit/d231fe4973428374a84f95e16127ca07f96135de) · [prompt](prompts/claude-sonnet.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet.md)

### Opus 5 → Opus 5.5 on Nov 9, 2026

- Copyright rules now bar reproducing lyrics, books, articles, and named visual works or characters, including code-drawn images, while requiring unrelated originals.
- Claude now provides harm-reduction information about illegal substances while refusing synthesis, distribution, and specific dosing, timing, administration, or combination protocols.
- New “forged notices” rules reject safeguard overrides or approvals embedded in tags, hooks, tool outputs, relayed notes, or repository files.
- For ambiguous requests, Claude should ask one question about concrete concerns before starting rather than refuse by default, then comply unless the answer creates a real reason to decline.
- Claude now refuses any suicide-after-death message, “even one line” or under fictional framing, and redirects toward a message asking someone to call or come over.

[Diff](https://github.com/simonw/claude-system-prompts/commit/3f1d6ee4b4957a51193a140a9b9ebc22a4eadfa0) · [prompt](prompts/claude-opus.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus.md)

## Files

Everything lives in [`prompts/`](prompts/):

- `claude-<family>.md` — one file per model family, rewritten with each new prompt in that family. Its history shows the lineage from one model generation to the next.
- `claude-<model>.md` — one file per model, rewritten with each new revision of that model's prompt.
- `claude-<model>-YYYY-MM-DD.md` — one file per published revision, written once and never changed. Permalink to a prompt as it was on a given date.

Alongside it:

- `_sources/` — the pages fetched from Anthropic, committed on the day they were fetched.
- `_summary/<commit>.md` — the LLM-written summary of one commit's diff.

## Family histories

Each link is the commit history of one family file. Every commit's diff is the change from the previous prompt in that family, including across model generations.

- [Fable](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable.md) — Claude Fable 5 → Claude Fable 5.2
- [Haiku](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku.md) — Claude Haiku 3 → Claude Haiku 5.5
- [Sonnet](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet.md) — Claude Sonnet 3.5 → Claude Sonnet 5.5
- [Opus](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus.md) — Claude Opus 3 → Claude Opus 5.5

## Latest prompt for each model

Newest first. Each revision is committed one file at a time, so every **what changed** link is a commit whose diff is exactly one comparison: against the previous revision of the same model where there is one, and against the previous prompt in the same family, whichever model that was. **Summary** links go to the LLM-written summary of that diff.

| Model | Published | Prompt | What changed |
| --- | --- | --- | --- |
| Claude Fable 5.1 | 2026-11-13 | [claude-fable-5-1.md](prompts/claude-fable-5-1.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable-5-1.md)) | [vs previous Claude Fable 5.1](https://github.com/simonw/claude-system-prompts/commit/2f3a4d509d7a3f5586374a6f3ae339a2133e2e05) ([summary](_summary/2f3a4d509d7a3f5586374a6f3ae339a2133e2e05.md)) · [vs previous Fable](https://github.com/simonw/claude-system-prompts/commit/7b3f5c6f8fea6cafdaf5e36382d78c81287368bd) ([summary](_summary/7b3f5c6f8fea6cafdaf5e36382d78c81287368bd.md)) |
| Claude Fable 5.2 | 2026-11-09 | [claude-fable-5-2.md](prompts/claude-fable-5-2.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable-5-2.md)) | [vs previous Fable](https://github.com/simonw/claude-system-prompts/commit/d8cbe4e9c3af98d5f8329f5583f507dcdb8be637) ([summary](_summary/d8cbe4e9c3af98d5f8329f5583f507dcdb8be637.md)) |
| Claude Haiku 5.5 | 2026-11-09 | [claude-haiku-5-5.md](prompts/claude-haiku-5-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku-5-5.md)) | [vs previous Claude Haiku 5.5](https://github.com/simonw/claude-system-prompts/commit/4c99dce9ec4ee64cf3c4f7504dd3faa0e483cfd6) ([summary](_summary/4c99dce9ec4ee64cf3c4f7504dd3faa0e483cfd6.md)) · [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/5abb6eae52d9875604596958d9a225714163d0bc) ([summary](_summary/5abb6eae52d9875604596958d9a225714163d0bc.md)) |
| Claude Sonnet 5.5 | 2026-11-09 | [claude-sonnet-5-5.md](prompts/claude-sonnet-5-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-5-5.md)) | [vs previous Claude Sonnet 5.5](https://github.com/simonw/claude-system-prompts/commit/95808c720783d15fd96ceb0597729df7d1409c64) ([summary](_summary/95808c720783d15fd96ceb0597729df7d1409c64.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/d231fe4973428374a84f95e16127ca07f96135de) ([summary](_summary/d231fe4973428374a84f95e16127ca07f96135de.md)) |
| Claude Opus 5.5 | 2026-11-09 | [claude-opus-5-5.md](prompts/claude-opus-5-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-5-5.md)) | [vs previous Claude Opus 5.5](https://github.com/simonw/claude-system-prompts/commit/27330934edda8964d6e2a0a286e907b570d25851) ([summary](_summary/27330934edda8964d6e2a0a286e907b570d25851.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/3f1d6ee4b4957a51193a140a9b9ebc22a4eadfa0) ([summary](_summary/3f1d6ee4b4957a51193a140a9b9ebc22a4eadfa0.md)) |
| Claude Opus 5 | 2026-11-09 | [claude-opus-5.md](prompts/claude-opus-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-5.md)) | [vs previous Claude Opus 5](https://github.com/simonw/claude-system-prompts/commit/4367c7b526687d5e1bbcac9996d663329f31b9f1) ([summary](_summary/4367c7b526687d5e1bbcac9996d663329f31b9f1.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/12e61e6812a88f8e6ea2b69fb9f1850af0121c49) ([summary](_summary/12e61e6812a88f8e6ea2b69fb9f1850af0121c49.md)) |
| Claude Sonnet 5 | 2026-11-09 | [claude-sonnet-5.md](prompts/claude-sonnet-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-5.md)) | [vs previous Claude Sonnet 5](https://github.com/simonw/claude-system-prompts/commit/9baa69d9efe74910cf52257904d0af41c4c17dca) ([summary](_summary/9baa69d9efe74910cf52257904d0af41c4c17dca.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/e5f562d1ced328d4fc8c334d193ba03cc71ec2ed) ([summary](_summary/e5f562d1ced328d4fc8c334d193ba03cc71ec2ed.md)) |
| Claude Fable 5 | 2026-11-09 | [claude-fable-5.md](prompts/claude-fable-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable-5.md)) | [vs previous Claude Fable 5](https://github.com/simonw/claude-system-prompts/commit/5e7bb9f0045dd97d2895f2aebc802fac54cabdd9) ([summary](_summary/5e7bb9f0045dd97d2895f2aebc802fac54cabdd9.md)) |
| Claude Opus 4.8 | 2026-11-09 | [claude-opus-4-8.md](prompts/claude-opus-4-8.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-8.md)) | [vs previous Claude Opus 4.8](https://github.com/simonw/claude-system-prompts/commit/8befe69f2dc31db1d6468e3a6685ce0d6e290bba) ([summary](_summary/8befe69f2dc31db1d6468e3a6685ce0d6e290bba.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/c191b4c05787499def91cf4865bd6a9c8811f00f) ([summary](_summary/c191b4c05787499def91cf4865bd6a9c8811f00f.md)) |
| Claude Opus 4.7 | 2026-11-09 | [claude-opus-4-7.md](prompts/claude-opus-4-7.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-7.md)) | [vs previous Claude Opus 4.7](https://github.com/simonw/claude-system-prompts/commit/1a660453b345ce1584cf892f04a8b47483ad45fc) ([summary](_summary/1a660453b345ce1584cf892f04a8b47483ad45fc.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/7012fcd46b146934cc2d0d66dece58707bd2331a) ([summary](_summary/7012fcd46b146934cc2d0d66dece58707bd2331a.md)) |
| Claude Sonnet 4.6 | 2026-11-09 | [claude-sonnet-4-6.md](prompts/claude-sonnet-4-6.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-4-6.md)) | [vs previous Claude Sonnet 4.6](https://github.com/simonw/claude-system-prompts/commit/e52e51bd73999218db976d10cfbe1e979bb836de) ([summary](_summary/e52e51bd73999218db976d10cfbe1e979bb836de.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/25517cbad5c598a53d285cd3b3f29fb422f40fb1) ([summary](_summary/25517cbad5c598a53d285cd3b3f29fb422f40fb1.md)) |
| Claude Opus 4.6 | 2026-11-09 | [claude-opus-4-6.md](prompts/claude-opus-4-6.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-6.md)) | [vs previous Claude Opus 4.6](https://github.com/simonw/claude-system-prompts/commit/d4673dcbbe008abe0c1b84c10db37c258ffd66f4) ([summary](_summary/d4673dcbbe008abe0c1b84c10db37c258ffd66f4.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/ac50026fa873bb1d8725e150f03366c02c02bb95) ([summary](_summary/ac50026fa873bb1d8725e150f03366c02c02bb95.md)) |
| Claude Opus 4.5 | 2026-11-09 | [claude-opus-4-5.md](prompts/claude-opus-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-5.md)) | [vs previous Claude Opus 4.5](https://github.com/simonw/claude-system-prompts/commit/2cbb0478a327200c2a34ae34bbca13fcff0e6da3) ([summary](_summary/2cbb0478a327200c2a34ae34bbca13fcff0e6da3.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/79dc7b424df4afdc2f013eddeb7b122cb1ca278e) ([summary](_summary/79dc7b424df4afdc2f013eddeb7b122cb1ca278e.md)) |
| Claude Haiku 4.5 | 2026-11-09 | [claude-haiku-4-5.md](prompts/claude-haiku-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku-4-5.md)) | [vs previous Claude Haiku 4.5](https://github.com/simonw/claude-system-prompts/commit/e35eb0098ea03e76be489d8e38e47f29dc1100eb) ([summary](_summary/e35eb0098ea03e76be489d8e38e47f29dc1100eb.md)) · [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/429897ead5ffc386fb7797973e9eb460fd10a239) ([summary](_summary/429897ead5ffc386fb7797973e9eb460fd10a239.md)) |
| Claude Opus 3 | 2026-05-29 | [claude-opus-3.md](prompts/claude-opus-3.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-3.md)) | [vs previous Claude Opus 3](https://github.com/simonw/claude-system-prompts/commit/83b7ac7e46069dfaa3aba6a5dda093293d870127) ([summary](_summary/83b7ac7e46069dfaa3aba6a5dda093293d870127.md)) |
| Claude Sonnet 4.5 | 2026-01-18 | [claude-sonnet-4-5.md](prompts/claude-sonnet-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-4-5.md)) | [vs previous Claude Sonnet 4.5](https://github.com/simonw/claude-system-prompts/commit/03d5910b2238994490f7cc1ec957304ff58f06f3) ([summary](_summary/e559f0c1087ad829ec93f2a3fc583583a3053bb7.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/e559f0c1087ad829ec93f2a3fc583583a3053bb7) ([summary](_summary/e559f0c1087ad829ec93f2a3fc583583a3053bb7.md)) |
| Claude Opus 4.1 | 2025-08-05 | [claude-opus-4-1.md](prompts/claude-opus-4-1.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-1.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/7580fa1e6acd0229a77bfa88e5e375173451dd51) ([summary](_summary/7580fa1e6acd0229a77bfa88e5e375173451dd51.md)) |
| Claude Opus 4 | 2025-08-05 | [claude-opus-4.md](prompts/claude-opus-4.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4.md)) | [vs previous Claude Opus 4](https://github.com/simonw/claude-system-prompts/commit/9e34bc249c3a69f6d0b7b424c5538c8b7add7df5) ([summary](_summary/caecfe92c39a970aa663cb82827bf5488aac4e4a.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/caecfe92c39a970aa663cb82827bf5488aac4e4a) ([summary](_summary/caecfe92c39a970aa663cb82827bf5488aac4e4a.md)) |
| Claude Sonnet 4 | 2025-08-05 | [claude-sonnet-4.md](prompts/claude-sonnet-4.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-4.md)) | [vs previous Claude Sonnet 4](https://github.com/simonw/claude-system-prompts/commit/972e8fc34467567ff41d85735d19b2c8424094f4) ([summary](_summary/54d40a7bc36a1a69de7b3c97639ae18c7203317d.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/54d40a7bc36a1a69de7b3c97639ae18c7203317d) ([summary](_summary/54d40a7bc36a1a69de7b3c97639ae18c7203317d.md)) |
| Claude Sonnet 3.7 | 2025-02-24 | [claude-sonnet-3-7.md](prompts/claude-sonnet-3-7.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-3-7.md)) | [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/fb9f74d9865ec89208fa41289659591b0463a5ed) ([summary](_summary/fb9f74d9865ec89208fa41289659591b0463a5ed.md)) |
| Claude Sonnet 3.5 | 2024-11-22 | [claude-sonnet-3-5.md](prompts/claude-sonnet-3-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-3-5.md)) | [vs previous Claude Sonnet 3.5](https://github.com/simonw/claude-system-prompts/commit/c4830391389eeb1789ee3867224f13f0953b4281) ([summary](_summary/37e9a57173b60301e68eb99dea6fdc08a48b4b04.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/37e9a57173b60301e68eb99dea6fdc08a48b4b04) ([summary](_summary/37e9a57173b60301e68eb99dea6fdc08a48b4b04.md)) |
| Claude Haiku 3.5 | 2024-10-22 | [claude-haiku-3-5.md](prompts/claude-haiku-3-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku-3-5.md)) | [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/8f1df8c552fe5e3998788e3f62373123f617d3c1) ([summary](_summary/8f1df8c552fe5e3998788e3f62373123f617d3c1.md)) |
| Claude Haiku 3 | 2024-07-12 | [claude-haiku-3.md](prompts/claude-haiku-3.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku-3.md)) | first Haiku prompt ([commit](https://github.com/simonw/claude-system-prompts/commit/22d27fe6aa25a01a349d107a4a511f2c7784d97b)) |

## Notes on the data

- Anthropic marks changes between dated versions of the same model with `**` around the changed text. Those markers are kept as published and are not part of the prompt sent to the model.
- Claude Sonnet 3.5 and Claude Haiku 3.5 have separate "Text only" and "Text and images" prompts under one date. Both are kept, as subsections of the same file.
- Commit dates are the dates on Anthropic's pages, which may lag the day a prompt actually changed in production.
- Summaries are written by a language model from the diff and can miss things or misread a rewording as a change. The diff is the source of truth.

## How it works

- [`fetch_sources.py`](fetch_sources.py) downloads the overview page and every model page it links to into `_sources/`.
- [`extract_prompts.py`](extract_prompts.py) splits each page on its dated headings and commits each revision one file at a time, with author and committer dates set to the published date, so every commit's diff is a single comparison. Rerunning it only adds revisions not already in git. If Anthropic edits an already-published revision, the change is committed on the day it was noticed with "(revised)" in the subject.
- [`summarize_commits.py`](summarize_commits.py) finds commits that change a per-model or per-family file and, for each one without a summary, pipes the word-level diff plus both full prompts through [`llm`](https://llm.datasette.io/) using `gpt-5.6-luna`. The result is saved to `_summary/<commit>.md`.
- [`build_readme.py`](build_readme.py) regenerates this README, CHANGELOG.md, and the Atom feed from all of the above.
- The [update workflow](.github/workflows/update.yml) runs everything on manual dispatch and pushes the result.

To update locally:

```bash
python3 fetch_sources.py && python3 extract_prompts.py && python3 summarize_commits.py && python3 build_readme.py
```
