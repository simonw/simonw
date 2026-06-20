# Bandwidther

SwiftUI menu bar app for monitoring application bandwidth use.

> [!NOTE]
> This app was vibe coded using Claude Opus 4.6 and GPT-5.4. I do not have deep knowledge of macOS networking or SwiftUI such that I can confidently evaluate the end result.

![Screenshot of Bandwidther macOS app showing two columns: left side displays overall download/upload speeds, a bandwidth graph over the last 60 seconds, cumulative totals, internet and LAN connection counts, and internet destinations; right side shows per-process bandwidth usage sorted by rate with processes like nsurlsessiond, apsd, rapportd, mDNSResponder, Dropbox, and others listed with their individual download/upload speeds and progress bars.](https://github.com/simonw/bandwidther/raw/main/screenshot.png)

## Features

- Live per-process download/upload rates via `nettop`
- Internet vs LAN connection classification
- Reverse DNS resolution for remote destinations
- Sparkline bandwidth graph (last 60 seconds)
- Two-column popover panel from the menu bar

## How measurement works

Bandwidther uses macOS command-line networking tools rather than packet capture or private APIs.

- Per-process bandwidth comes from `nettop` in per-process summary mode. The app runs `nettop` in delta mode, takes a baseline sample plus a 1-second follow-up sample, and uses that second sample as the current download/upload rate for each process.
- The cumulative byte totals shown in the UI come from the baseline `nettop` sample. Those are process-level totals reported by `nettop`, not totals maintained independently by the app.
- Connection summaries come from `lsof -iTCP -n -P`. The app parses active TCP sockets, attributes them to processes using `lsof` output, and classifies remote endpoints as internet or LAN/local using address heuristics.
- Reverse DNS is done separately in the app using `getnameinfo`, so destination names are best-effort and may be missing even when the raw IP address is shown.

Important limitations:

- The connection view is a snapshot of currently visible TCP sockets. It is not a packet-level audit and it does not currently include UDP traffic in the summary panels.
- LAN vs internet classification is heuristic. Private IPv4 ranges, loopback, link-local IPv6, and unique-local IPv6 are treated as local.
- If `nettop` or `lsof` is unavailable or denied by the system, the app may be unable to collect some measurements. Recent versions of the app surface `nettop` failures in the UI instead of silently showing zero traffic.

## Building

```bash
git clone https://github.com/simonw/bandwidther
cd bandwidther
swiftc -parse-as-library -framework SwiftUI -framework AppKit -o Bandwidther BandwidtherApp.swift
./Bandwidther
```

Requires macOS and Xcode command line tools (`xcode-select --install`).
