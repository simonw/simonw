# guidepup-macos-prototype
A prototype of running Guidepup on macOS in GitHub Actions

> [!CAUTION]
> Everything in this repo, both text and code, was built by Codex (with GPT-5.5 xhigh) and is unreviewed.

## VoiceOver media smoke experiment

This repo contains a GitHub Actions experiment that tries to run
Guidepup on a pinned GitHub-hosted macOS runner, drive VoiceOver against a
small WebKit page, record the desktop session, probe ScreenCaptureKit system
audio capture, and upload all outputs as an Actions artifact.
The smoke test runs real VoiceOver speech at `180%`, twice Guidepup's default
`90%` test rate. Override it with `VOICEOVER_RATE_AS_PERCENT` or
`--voiceover-rate-percent`.

It runs automatically on push. You can also run it manually from
**Actions -> voiceover-media-smoke -> Run workflow**.

To run the same experiment locally on macOS:

```sh
npm run test:voiceover:media:local
```

The local script writes timestamped output under `local-runs/`. The GitHub
Actions workflow and the local command both use
`scripts/run-voiceover-media-smoke.sh`; the only difference is that Actions uses
`guidepup/setup-action`, while the local path runs `npx @guidepup/setup`.
If local setup reports remaining manual steps, follow the linked Guidepup
VoiceOver setup guide and rerun the command.

## AppleScript VoiceOver CLI

`scripts/voctl.mjs` is a small AppleScript-first CLI for probing and driving
VoiceOver without Guidepup's support check:

```sh
npm run voctl -- detect --pretty
npm run voctl -- read --pretty
npm run voctl -- perform "move right" --read-after --pretty
npm run voctl -- sequence actions.json --read-after --pretty
```

Every `voctl` invocation appends a JSON object to `voice-over.jsonl` in the
current directory. Use `-f other-file.jsonl` or `--log-file other-file.jsonl` to
write somewhere else. Each JSONL record includes the parsed input, raw argv,
output payload, exit code, timestamp, and duration.

Sequence files can be arrays or objects with an `actions` array. Supported
actions include `perform`, `move`, `output`, `open`, `open-url`,
`browser-state`, `activate-app`, `keystroke`, `type`, `key-code`, `action`,
`select`, `wait`, and `read`.

The workflow uploads:

- `artifacts/voiceover-transcript.json`
- `artifacts/voiceover-subtitles.srt`
- `artifacts/system-audio-probe.wav`
- `artifacts/system-audio-probe-report.json`
- `artifacts/summary.md`
- `recordings/guidepup-session.mov`
- any setup recordings emitted by `guidepup/setup-action`

The default runner is `macos-14`, with `macos-15` available as a manual
comparison. The `require_audio` input is enabled by default, so the job fails if
the ScreenCaptureKit probe cannot produce a non-silent audio artifact; the
artifact upload still runs so failures are inspectable.
