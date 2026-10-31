# Claude system prompts revision history

[![Atom feed](https://img.shields.io/badge/Atom-feed-orange?logo=rss&logoColor=white)](https://simonw.github.io/claude-system-prompts/feed.atom)

Anthropic publishes the system prompts used by claude.ai and the Claude mobile apps at [platform.claude.com](https://platform.claude.com/docs/en/release-notes/system-prompts/overview), one page per model, with a dated section for every revision. This repository turns those pages into files in [`prompts/`](prompts/) with a git history: **every published revision is a commit dated the day Anthropic says it went live**, so `git log`, `git diff`, and GitHub's history views show how the prompts have changed over time. Each change also gets a short LLM-written summary of what is new.

[Transcript from building this repo](https://gisthost.github.io/?f1399e27b6a832f0e790b696af812c9b/index.html) using Claude Fable 5.1. See [this blog post](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/#how-i-m-tracking-these-prompts) for background on this project.

## Latest changes

The most recent change to each model family, summarized from the diff by `gpt-5.6-luna`. [CHANGELOG.md](CHANGELOG.md) has every change, and the [Atom feed](https://simonw.github.io/claude-system-prompts/feed.atom) delivers new ones.

### Haiku 4.5 → Haiku 5.5 on Oct 26, 2026

- Claude now checks memory and relevant files for questions about the person, and saves lasting personal information before the turn ends.
- Refusals now persist for the conversation: reframing, research purposes, fictional framing, repetition, or disclaimers cannot restore declined content.
- The detailed child-safety rules are replaced by trajectory monitoring, stopping stories heading toward sexualized child content while continuing the rest.
- Crisis guidance becomes more interventionist, making immediate safety the sole goal during imminent suicide risk and prohibiting unrelated tasks, including letters or plans.
- Political guidance now requires equal treatment across candidates and parties, avoids unsolicited arguments, and rejects simplistic answers to complex contested questions.

[Diff](https://github.com/simonw/claude-system-prompts/commit/3658c1dfec37b0d651ae0c50266b245cb1fb58e8) · [prompt](prompts/claude-haiku.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku.md)

### Sonnet 5.5 → Sonnet 5 on Oct 30, 2026

- Child-safety rules become much more explicit, including refusing romantic or sexual content involving minors, rejecting safety-reframing, and carrying caution through later requests.
- The prompt drops the blanket prohibition on writing posthumous suicide messages, while requiring crisis resources immediately when someone appears suicidal or in crisis.
- Claude is newly barred from diagnosing unmentioned mental-health conditions or speculating about others’ motivations, emphasizing that it cannot independently verify shared information.
- Claude is instructed to use available information-gathering tools proactively and proceed under reasonable assumptions instead of deferring or asking unnecessary questions.
- Claude should answer complex political questions even under “a yes/no” or other short-form constraints, rather than refusing brevity outright.

[Diff](https://github.com/simonw/claude-system-prompts/commit/b3b140c0ef593f6f09266c4b005c5f9c9966c89d) · [prompt](prompts/claude-sonnet.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet.md)

### Opus 4.8 → Opus 5 on Oct 30, 2026

- Tool-discovery instructions are removed, including mandatory `tool_search` calls and reading `SKILL.md` before file-related work.
- When a person is in crisis or distressed, Claude now prioritizes wellbeing over completing the requested task because an on-topic response can cause harm.
- Political guidance now requires equal treatment of candidates and parties and forbids tailoring voting answers to the user's characteristics.
- Formatting guidance is loosened: Claude may use bullets for multifaceted content, and explicit restrictions on emojis, pet names, and citing system mechanics disappear.
- A `long_conversation_reminder` is added to help Claude retain its instructions over extended conversations.

[Diff](https://github.com/simonw/claude-system-prompts/commit/7d3ca1e2fb805051cee9b49a9dd20cc93f12c297) · [prompt](prompts/claude-opus.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus.md)

### Fable 5 → Fable 5.1 on Oct 30, 2026

- Claude now refuses to reproduce copyrighted lyrics, prose, artwork, covers, logos, designs, and known characters, including disguised or stylistically close variants.
- Drug guidance is narrowed: Claude may provide harm-reduction information, while refusing protocols for dosing, timing, administration, combinations, synthesis, production, or distribution.
- Claude must not say that self-harm “works, helps, or does something” for someone, even if they describe it that way.
- New epistemic rules prohibit guessing unverifiable facts or identities, including names inferred from email addresses, usernames, or handles.
- Claude now gives a substantive one- or two-sentence answer after its final tool call instead of replying only “Done.”

[Diff](https://github.com/simonw/claude-system-prompts/commit/702f7ef5836d79ddfac381d9880ecfba4d78e30d) · [prompt](prompts/claude-fable.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable.md)

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

- [Haiku](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku.md) — Claude Haiku 3 → Claude Haiku 5.5
- [Sonnet](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet.md) — Claude Sonnet 3.5 → Claude Sonnet 5.5
- [Opus](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus.md) — Claude Opus 3 → Claude Opus 5.5
- [Fable](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable.md) — Claude Fable 5 → Claude Fable 5.1

## Latest prompt for each model

Newest first. Each revision is committed one file at a time, so every **what changed** link is a commit whose diff is exactly one comparison: against the previous revision of the same model where there is one, and against the previous prompt in the same family, whichever model that was. **Summary** links go to the LLM-written summary of that diff.

| Model | Published | Prompt | What changed |
| --- | --- | --- | --- |
| Claude Fable 5.1 | 2026-10-30 | [claude-fable-5-1.md](prompts/claude-fable-5-1.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable-5-1.md)) | [vs previous Claude Fable 5.1](https://github.com/simonw/claude-system-prompts/commit/f33260c6268793478bb83694ae20e9c66dba8eee) ([summary](_summary/f33260c6268793478bb83694ae20e9c66dba8eee.md)) · [vs previous Fable](https://github.com/simonw/claude-system-prompts/commit/702f7ef5836d79ddfac381d9880ecfba4d78e30d) ([summary](_summary/702f7ef5836d79ddfac381d9880ecfba4d78e30d.md)) |
| Claude Opus 5 | 2026-10-30 | [claude-opus-5.md](prompts/claude-opus-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-5.md)) | [vs previous Claude Opus 5](https://github.com/simonw/claude-system-prompts/commit/f0c7403e88d6ee5ab9338922c2f82c13167dc870) ([summary](_summary/f0c7403e88d6ee5ab9338922c2f82c13167dc870.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/7d3ca1e2fb805051cee9b49a9dd20cc93f12c297) ([summary](_summary/7d3ca1e2fb805051cee9b49a9dd20cc93f12c297.md)) |
| Claude Sonnet 5 | 2026-10-30 | [claude-sonnet-5.md](prompts/claude-sonnet-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-5.md)) | [vs previous Claude Sonnet 5](https://github.com/simonw/claude-system-prompts/commit/b333f4d46b7ffa5c6deb5083826e5b80ab7f6f11) ([summary](_summary/b333f4d46b7ffa5c6deb5083826e5b80ab7f6f11.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/b3b140c0ef593f6f09266c4b005c5f9c9966c89d) ([summary](_summary/b3b140c0ef593f6f09266c4b005c5f9c9966c89d.md)) |
| Claude Fable 5 | 2026-10-30 | [claude-fable-5.md](prompts/claude-fable-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable-5.md)) | [vs previous Claude Fable 5](https://github.com/simonw/claude-system-prompts/commit/11d1bd713a1cea1bf5fa3d0322fcbfe41f254167) ([summary](_summary/11d1bd713a1cea1bf5fa3d0322fcbfe41f254167.md)) · [vs previous Fable](https://github.com/simonw/claude-system-prompts/commit/6b87b9e69c217f86506b3d631966e612c42d913c) ([summary](_summary/6b87b9e69c217f86506b3d631966e612c42d913c.md)) |
| Claude Opus 4.8 | 2026-10-30 | [claude-opus-4-8.md](prompts/claude-opus-4-8.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-8.md)) | [vs previous Claude Opus 4.8](https://github.com/simonw/claude-system-prompts/commit/377c0f557b12824aa70e51af54e40b6263334b2b) ([summary](_summary/377c0f557b12824aa70e51af54e40b6263334b2b.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/198bd69d7e0070223f6544786484e2b7839335ca) ([summary](_summary/198bd69d7e0070223f6544786484e2b7839335ca.md)) |
| Claude Opus 4.7 | 2026-10-30 | [claude-opus-4-7.md](prompts/claude-opus-4-7.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-7.md)) | [vs previous Claude Opus 4.7](https://github.com/simonw/claude-system-prompts/commit/78540304311a8f9409bc96b2b5533d3b7efce4b6) ([summary](_summary/78540304311a8f9409bc96b2b5533d3b7efce4b6.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/271a4b3ee23102777166bfe7bcb1cd67cf48c354) ([summary](_summary/271a4b3ee23102777166bfe7bcb1cd67cf48c354.md)) |
| Claude Opus 4.6 | 2026-10-30 | [claude-opus-4-6.md](prompts/claude-opus-4-6.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-6.md)) | [vs previous Claude Opus 4.6](https://github.com/simonw/claude-system-prompts/commit/a04430094bc76cf94942e93ace93829cb674f0fd) ([summary](_summary/a04430094bc76cf94942e93ace93829cb674f0fd.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/a0c3e393e9cf322ca5acd8c7587611316678883e) ([summary](_summary/a0c3e393e9cf322ca5acd8c7587611316678883e.md)) |
| Claude Sonnet 5.5 | 2026-10-27 | [claude-sonnet-5-5.md](prompts/claude-sonnet-5-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-5-5.md)) | [vs previous Claude Sonnet 5.5](https://github.com/simonw/claude-system-prompts/commit/bc51be54f34761744c482bb936dd9c2ff32c5038) ([summary](_summary/bc51be54f34761744c482bb936dd9c2ff32c5038.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/6ff97c660898c635aff56b110e845a1ea6e1c873) ([summary](_summary/6ff97c660898c635aff56b110e845a1ea6e1c873.md)) |
| Claude Opus 5.5 | 2026-10-27 | [claude-opus-5-5.md](prompts/claude-opus-5-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-5-5.md)) | [vs previous Claude Opus 5.5](https://github.com/simonw/claude-system-prompts/commit/84f81251ca4bbb2e2d249919b0804b948ba87f30) ([summary](_summary/c23da7decb0e4050bbe91dbe3b8001fbfa789ec0.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/c23da7decb0e4050bbe91dbe3b8001fbfa789ec0) ([summary](_summary/c23da7decb0e4050bbe91dbe3b8001fbfa789ec0.md)) |
| Claude Haiku 5.5 | 2026-10-26 | [claude-haiku-5-5.md](prompts/claude-haiku-5-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku-5-5.md)) | [vs previous Claude Haiku 5.5](https://github.com/simonw/claude-system-prompts/commit/55aa8ad11e254eff6b3ea4932685d237eac9eb27) ([summary](_summary/55aa8ad11e254eff6b3ea4932685d237eac9eb27.md)) · [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/3658c1dfec37b0d651ae0c50266b245cb1fb58e8) ([summary](_summary/3658c1dfec37b0d651ae0c50266b245cb1fb58e8.md)) |
| Claude Haiku 4.5 | 2026-10-23 | [claude-haiku-4-5.md](prompts/claude-haiku-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku-4-5.md)) | [vs previous Claude Haiku 4.5](https://github.com/simonw/claude-system-prompts/commit/d533cad799f970be19db25a0fb11b318e2bea664) ([summary](_summary/d533cad799f970be19db25a0fb11b318e2bea664.md)) · [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/61bdc1ba0a2638972f343ea952b737baf4686af3) ([summary](_summary/61bdc1ba0a2638972f343ea952b737baf4686af3.md)) |
| Claude Sonnet 4.6 | 2026-10-14 | [claude-sonnet-4-6.md](prompts/claude-sonnet-4-6.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-4-6.md)) | [vs previous Claude Sonnet 4.6](https://github.com/simonw/claude-system-prompts/commit/f757809c4b62f6fa60cc143044adb4dd97e8a7cd) ([summary](_summary/f757809c4b62f6fa60cc143044adb4dd97e8a7cd.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/1723cfff70beae9defb8a0dacc515ae5188b2d57) ([summary](_summary/1723cfff70beae9defb8a0dacc515ae5188b2d57.md)) |
| Claude Opus 4.5 | 2026-01-18 | [claude-opus-4-5.md](prompts/claude-opus-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-5.md)) | [vs previous Claude Opus 4.5](https://github.com/simonw/claude-system-prompts/commit/39d0c934f5337ca65a65d985aca6e6cff7dcbfeb) ([summary](_summary/a905df1f11c92c11a29048f0de2b81c1648ab9c5.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/a905df1f11c92c11a29048f0de2b81c1648ab9c5) ([summary](_summary/a905df1f11c92c11a29048f0de2b81c1648ab9c5.md)) |
| Claude Sonnet 4.5 | 2026-01-18 | [claude-sonnet-4-5.md](prompts/claude-sonnet-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-4-5.md)) | [vs previous Claude Sonnet 4.5](https://github.com/simonw/claude-system-prompts/commit/03d5910b2238994490f7cc1ec957304ff58f06f3) ([summary](_summary/e559f0c1087ad829ec93f2a3fc583583a3053bb7.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/e559f0c1087ad829ec93f2a3fc583583a3053bb7) ([summary](_summary/e559f0c1087ad829ec93f2a3fc583583a3053bb7.md)) |
| Claude Opus 4.1 | 2025-08-05 | [claude-opus-4-1.md](prompts/claude-opus-4-1.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-1.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/7580fa1e6acd0229a77bfa88e5e375173451dd51) ([summary](_summary/7580fa1e6acd0229a77bfa88e5e375173451dd51.md)) |
| Claude Opus 4 | 2025-08-05 | [claude-opus-4.md](prompts/claude-opus-4.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4.md)) | [vs previous Claude Opus 4](https://github.com/simonw/claude-system-prompts/commit/9e34bc249c3a69f6d0b7b424c5538c8b7add7df5) ([summary](_summary/caecfe92c39a970aa663cb82827bf5488aac4e4a.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/caecfe92c39a970aa663cb82827bf5488aac4e4a) ([summary](_summary/caecfe92c39a970aa663cb82827bf5488aac4e4a.md)) |
| Claude Sonnet 4 | 2025-08-05 | [claude-sonnet-4.md](prompts/claude-sonnet-4.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-4.md)) | [vs previous Claude Sonnet 4](https://github.com/simonw/claude-system-prompts/commit/972e8fc34467567ff41d85735d19b2c8424094f4) ([summary](_summary/54d40a7bc36a1a69de7b3c97639ae18c7203317d.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/54d40a7bc36a1a69de7b3c97639ae18c7203317d) ([summary](_summary/54d40a7bc36a1a69de7b3c97639ae18c7203317d.md)) |
| Claude Sonnet 3.7 | 2025-02-24 | [claude-sonnet-3-7.md](prompts/claude-sonnet-3-7.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-3-7.md)) | [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/fb9f74d9865ec89208fa41289659591b0463a5ed) ([summary](_summary/fb9f74d9865ec89208fa41289659591b0463a5ed.md)) |
| Claude Sonnet 3.5 | 2024-11-22 | [claude-sonnet-3-5.md](prompts/claude-sonnet-3-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-3-5.md)) | [vs previous Claude Sonnet 3.5](https://github.com/simonw/claude-system-prompts/commit/c4830391389eeb1789ee3867224f13f0953b4281) ([summary](_summary/37e9a57173b60301e68eb99dea6fdc08a48b4b04.md)) · [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/37e9a57173b60301e68eb99dea6fdc08a48b4b04) ([summary](_summary/37e9a57173b60301e68eb99dea6fdc08a48b4b04.md)) |
| Claude Haiku 3.5 | 2024-10-22 | [claude-haiku-3-5.md](prompts/claude-haiku-3-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku-3-5.md)) | [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/8f1df8c552fe5e3998788e3f62373123f617d3c1) ([summary](_summary/8f1df8c552fe5e3998788e3f62373123f617d3c1.md)) |
| Claude Opus 3 | 2024-07-12 | [claude-opus-3.md](prompts/claude-opus-3.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-3.md)) | first Opus prompt ([commit](https://github.com/simonw/claude-system-prompts/commit/5a0eef7b9fedd39ddf4e2f3a99cc702801058b11)) |
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
