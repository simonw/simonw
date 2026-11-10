# beep-locator

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/beep-locator/blob/main/LICENSE)

For background on this project, see [Locating the source of a mysterious beep with Claude](https://simonwillison.net/2026/Nov/9/mysterious-beeps/).

*The rest of this README was written by Claude.*

Locate annoying beeps. Laptops, phones and tablets around a room become a
microphone array: they find each other by playing chirps (two-way acoustic
ranging, see [problem.md](problem.md)), then work out where a mystery beep
came from using time-difference-of-arrival.

Everything runs in the browser (WebAudio + WebSockets) against a Python
server. Code running on the listeners can be replaced remotely without
reloading their pages, so experiments can continue after the devices are set
up.

## Running it

You need [uv](https://docs.astral.sh/uv/) and, to give phones the https they
need for microphone access, [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
(`brew install cloudflared`).

```bash
git clone https://github.com/simonw/beep-locator
cd beep-locator
uv run beep-locator serve --tunnel
```

It prints:

- a **coordinator URL** (contains the admin token - open it on your laptop)
- a **join URL** plus a QR code: open it on each phone/tablet and tap
  *Start listening*
- `BEEP_URL=... BEEP_TOKEN=...` for driving it from elsewhere; locally,
  `uv run beep-locator ctl ...` finds the server and token automatically

Then:

1. Put 3 or more listeners around the room (volume up, silent mode off, no
   Bluetooth speakers, plugged in, screen left on with the page in front).
   The coordinator laptop can join too: *Also listen on this device*.
2. Press **Calibrate**. Each device chirps in turn; the map shows where they
   are. Use rotate/flip to match the map to the room (distances can't tell a
   room from its mirror image).
3. **Test beep** makes one device play a fake beep, which should be located
   on top of that device - a quick accuracy check.
4. Leave **Listen for beeps** on. When a beep is heard, one device plays a
   short sync chirp, every device uploads the audio around it, and the
   estimate appears on the map. More beeps sharpen the shaded region.

`/sim` runs a simulated room (fake listeners hearing a virtual beeper) for
testing without hardware: `/sim?n=5&every=10&bx=3&by=2`.

## Remote hacking

With `--auto-update` the server polls `origin` for new commits on its branch,
fast-forwards and restarts itself; listener pages reconnect automatically and
keep their audio running. Leave it off if you don't want code from the branch
running on your machine without review.

Independently of that, JavaScript can be sent straight to the browsers:

```bash
export BEEP_URL=https://....trycloudflare.com BEEP_TOKEN=...
uv run beep-locator ctl state                      # devices, levels, layout
uv run beep-locator ctl eval 'return rt.info()' --to Red
uv run beep-locator ctl push listener myexp exp.js  # install a module everywhere
uv run beep-locator ctl unpush listener myexp
uv run beep-locator ctl run selftest               # does each device hear itself?
uv run beep-locator ctl run calibrate
uv run beep-locator ctl run testbeep device=Blue
uv run beep-locator ctl results                    # calibrations and beep estimates
uv run beep-locator ctl clips / clip 42 -o x.wav  # recorded audio
uv run beep-locator ctl events --follow           # logs, detections, errors
uv run beep-locator ctl settings '{"detector": {"threshold_db": 10}}'
uv run beep-locator ctl sql 'select topic, count(*) from events group by topic'
uv run beep-locator ctl update                     # git pull + restart now
```

A module is an ES module whose default export receives a context object:

```js
export default function setup(ctx) {
  ctx.onAudio((frame, samples) => { /* every mic chunk, with its frame number */ });
  ctx.method("myexp.hello", (args) => ({ hi: ctx.deviceName }));  // callable via ctl rpc
  ctx.send("my_topic", { some: "data" });  // stored as an event on the server
  ctx.ui.textContent = "shown on the device's page";
  return { teardown() {} };  // optional; timers/handlers registered via ctx are cleaned up automatically
}
```

Modules on disk in `beep_locator/modules/{listener,coordinator}/` are the
defaults (the coordinator UI is itself a module). Pushed modules override
them. If a pushed version fails to load, devices keep running the previous one
and report the error.

## How it works

- `beep_locator/static/runtime.js`: the stable part of every page. Owns
  the AudioContext, a 60 second ring buffer of microphone audio indexed by
  AudioContext frame number (each device's own clock), the WebSocket, RPC and
  the module loader.
- `beep_locator/hub.py`: connections, RPC, module distribution, a rough
  (tens of ms) server-time to device-frame mapping from ping/pong, used only to
  know where to look in recordings.
- `beep_locator/procedures.py`: calibration (devices chirp in turn, upload
  recordings), locating (sync chirp right after a beep, upload, solve) and
  test beeps.
- `beep_locator/analysis.py` + `dsp.py`: matched-filter chirp detection with
  first-arrival logic, BeepBeep two-way ranging (only intervals within one
  device's recording are used, so clock offsets and audio latencies cancel),
  MDS + SMACOF layout with outlier rejection, onset detection, TDOA grid search
  + Gauss-Newton.
- `beep_locator/sim.py` and `static/sim-io.js`: simulated rooms with random
  sample rates, clock drift, latencies and a reflection, used by the tests.

Data (SQLite database, WAV clips, token) lives in `beep-data/`.

## Tests

```bash
uv run pytest
```
