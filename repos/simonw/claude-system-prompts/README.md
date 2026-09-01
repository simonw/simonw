# Claude system prompts revision history

[![Atom feed](https://img.shields.io/badge/Atom-feed-orange?logo=rss&logoColor=white)](https://simonw.github.io/claude-system-prompts/feed.atom)

Anthropic publishes the system prompts used by claude.ai and the Claude mobile apps at [platform.claude.com](https://platform.claude.com/docs/en/release-notes/system-prompts/overview), one page per model, with a dated section for every revision. This repository turns those pages into files in [`prompts/`](prompts/) with a git history: **every published revision is a commit dated the day Anthropic says it went live**, so `git log`, `git diff`, and GitHub's history views show how the prompts have changed over time. Each change also gets a short LLM-written summary of what is new.

[Transcript from building this repo](https://gisthost.github.io/?f1399e27b6a832f0e790b696af812c9b/index.html) using Claude Fable 5.1.

## Latest changes

The most recent change to each model family, summarized from the diff by `gpt-5.6-luna`. [CHANGELOG.md](CHANGELOG.md) has every change, and the [Atom feed](https://simonw.github.io/claude-system-prompts/feed.atom) delivers new ones.

### Fable 5 → Fable 5.1 on Sep 1, 2026

- Claude now refuses reproduction of protected visual works and recognizable characters, including code-generated art, while offering genuinely unrelated originals.
- Copyright restrictions now expressly ban reproducing lyrics, poems, and book passages in any amount, with persistent refusal after an initial decline.
- Drug guidance is reframed: Claude may provide overdose signs, dangerous interactions, and harm-reduction sources while refusing dosing and production protocols.
- The prompt drops explicit anti-dependency rules against thanking users for reaching out, inviting continued conversation, or reiterating willingness to talk.
- Claude need not apologize to unnecessarily rude users or become submissive, replacing the prior warning-and-end-conversation procedure.

[Diff](https://github.com/simonw/claude-system-prompts/commit/837a418b5888207b1b11b27d2f5471970da6f99b) · [prompt](prompts/claude-fable.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable.md)

### Opus 4.8 → Opus 5 on Jul 24, 2026

- Adds explicit Fable-to-Opus safeguards routing, noting harmless requests may be caught “in less than 5% of sessions,” and mandates factual handling of the export-control suspension.
- Drops tool-discovery rules requiring `tool_search` and pre-file `SKILL.md` viewing, and removes the instruction not to attribute behavior to the system prompt.
- In crisis or distress, Claude now prioritizes wellbeing over task completion; it also drops explicit anti-overreliance rules such as never asking users to keep talking.
- Replaces extensive anti-formatting rules with permission to use lists when helpful, while dropping restrictions on emojis and pet names.
- Unless it suspects a minor, Claude now assumes the person is a capable adult and treats them as such.

[Diff](https://github.com/simonw/claude-system-prompts/commit/26d66c827d2e847bf0b302207481576a4ba39fa0) · [prompt](prompts/claude-opus.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus.md)

### Sonnet 4.5 → Sonnet 4.6 on Feb 17, 2026

- Self-harm guidance now bans pain-based coping techniques, requires crisis resources without safety assessments, and says not to reinforce reluctance toward professional help.
- Claude must avoid fostering dependence: it should not thank users for reaching out, ask them to keep talking, or encourage continued engagement.
- Weapon-safety rules now cover harmful substances and weapons broadly, requiring refusal of enabling technical details regardless of public availability or claimed research intent.
- A new criticism policy tells Claude to acknowledge mistakes without excessive apology or self-abasement, maintaining “steady, honest helpfulness” and self-respect.

[Diff](https://github.com/simonw/claude-system-prompts/commit/1ad6d1b9d7d3d3b747e38e8a47bb907694f03f50) · [prompt](prompts/claude-sonnet.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet.md)

### Haiku 4.5 (Nov 19, 2025) → Haiku 4.5 (Jan 18, 2026)

- Claude may proactively tell users about customizable settings and features when useful, including web search, memory, preferences, and writing styles.

[Diff](https://github.com/simonw/claude-system-prompts/commit/5af9089640e454255b8a76fb0167d2a405e1e71c) · [prompt](prompts/claude-haiku.md) · [history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku.md)

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

- [Fable](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable.md) — Claude Fable 5 → Claude Fable 5.1
- [Opus](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus.md) — Claude Opus 3 → Claude Opus 5
- [Sonnet](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet.md) — Claude Sonnet 3.5 → Claude Sonnet 4.6
- [Haiku](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku.md) — Claude Haiku 3 → Claude Haiku 4.5

## Latest prompt for each model

Newest first. Each revision is committed one file at a time, so every **what changed** link is a commit whose diff is exactly one comparison: against the previous revision of the same model where there is one, and against the previous prompt in the same family, whichever model that was. **Summary** links go to the LLM-written summary of that diff.

| Model | Published | Prompt | What changed |
| --- | --- | --- | --- |
| Claude Fable 5.1 | 2026-09-01 | [claude-fable-5-1.md](prompts/claude-fable-5-1.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable-5-1.md)) | [vs previous Fable](https://github.com/simonw/claude-system-prompts/commit/837a418b5888207b1b11b27d2f5471970da6f99b) ([summary](_summary/837a418b5888207b1b11b27d2f5471970da6f99b.md)) |
| Claude Opus 5 | 2026-07-24 | [claude-opus-5.md](prompts/claude-opus-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-5.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/26d66c827d2e847bf0b302207481576a4ba39fa0) ([summary](_summary/26d66c827d2e847bf0b302207481576a4ba39fa0.md)) |
| Claude Fable 5 | 2026-06-09 | [claude-fable-5.md](prompts/claude-fable-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-fable-5.md)) | first Fable prompt ([commit](https://github.com/simonw/claude-system-prompts/commit/0fd7b3316ec3d7da93789351689fea6d5807a6be)) |
| Claude Opus 4.8 | 2026-05-28 | [claude-opus-4-8.md](prompts/claude-opus-4-8.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-8.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/c76eb467e2916a853f39d0832ebdb52c42735c8c) ([summary](_summary/c76eb467e2916a853f39d0832ebdb52c42735c8c.md)) |
| Claude Opus 4.7 | 2026-04-16 | [claude-opus-4-7.md](prompts/claude-opus-4-7.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-7.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/e281bbce1ad418c61380cb86873fd8fdf7822afc) ([summary](_summary/e281bbce1ad418c61380cb86873fd8fdf7822afc.md)) |
| Claude Sonnet 4.6 | 2026-02-17 | [claude-sonnet-4-6.md](prompts/claude-sonnet-4-6.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-sonnet-4-6.md)) | [vs previous Sonnet](https://github.com/simonw/claude-system-prompts/commit/1ad6d1b9d7d3d3b747e38e8a47bb907694f03f50) ([summary](_summary/1ad6d1b9d7d3d3b747e38e8a47bb907694f03f50.md)) |
| Claude Opus 4.6 | 2026-02-05 | [claude-opus-4-6.md](prompts/claude-opus-4-6.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-6.md)) | [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/1aa3fc2145f262ae5fa9676f1d71fc5f6b7c147a) ([summary](_summary/1aa3fc2145f262ae5fa9676f1d71fc5f6b7c147a.md)) |
| Claude Opus 4.5 | 2026-01-18 | [claude-opus-4-5.md](prompts/claude-opus-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-opus-4-5.md)) | [vs previous Claude Opus 4.5](https://github.com/simonw/claude-system-prompts/commit/39d0c934f5337ca65a65d985aca6e6cff7dcbfeb) ([summary](_summary/a905df1f11c92c11a29048f0de2b81c1648ab9c5.md)) · [vs previous Opus](https://github.com/simonw/claude-system-prompts/commit/a905df1f11c92c11a29048f0de2b81c1648ab9c5) ([summary](_summary/a905df1f11c92c11a29048f0de2b81c1648ab9c5.md)) |
| Claude Haiku 4.5 | 2026-01-18 | [claude-haiku-4-5.md](prompts/claude-haiku-4-5.md) ([history](https://github.com/simonw/claude-system-prompts/commits/main/prompts/claude-haiku-4-5.md)) | [vs previous Claude Haiku 4.5](https://github.com/simonw/claude-system-prompts/commit/defcf92d14e064bb17abddc308e2aa58446d5eb5) ([summary](_summary/5af9089640e454255b8a76fb0167d2a405e1e71c.md)) · [vs previous Haiku](https://github.com/simonw/claude-system-prompts/commit/5af9089640e454255b8a76fb0167d2a405e1e71c) ([summary](_summary/5af9089640e454255b8a76fb0167d2a405e1e71c.md)) |
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
