# Battle Drones

Battle Drones is a mobile-friendly real-time strategy (RTS) game inspired by Command & Conquer: two armies of drones — flying and ground-based — battle for territory and resources.

Read [Battle Drones—a vibe coded RTS with audio-based multiplayer](https://simonwillison.net/2026/Oct/20/battledrones/) for background details on this project and how it was built.

**Play it here: <https://simonw.github.io/battledrones/>**

*The rest of this README is written by Claude.*

## Duel a friend online

Play a 1v1 skirmish against a friend, phone to phone or on any two browsers:

1. On the **Skirmish** tab, choose a map and any mutators, then tap
   **🌐 Duel a friend online**.
2. Send your friend the invite link (`…/battledrones/#vs=<code>`). You can
   use the share sheet or Copy, or let them scan the QR code with their
   camera.
3. When they open it you're both in the lobby. You play blue and they play
   red, and each of you picks an opener. **Rematch** swaps sides.

No accounts and no lobby browser. Both browsers run the whole simulation in
lockstep and only your orders cross the internet, about one small message
every 100–200 ms. They go through a tiny WebSocket relay on Fly that pairs
the two pages by room code and stores nothing
([`relay/README.md`](relay/README.md)). If a phone drops its connection, it
reconnects to its seat and the match carries on.

Every end screen, for online duels and every other mode, has a
**📋 Copy replay JSON** button. Paste the record into **🎬 Watch a replay**
on the menu to watch the match again, or open it in the
[battle record viewer](https://simonw.github.io/battledrones/record-viewer.html).

## Watch AI models play it

AI models can play Battle Drones against each other, through tools that show each side only what it could see (**[AGENT-BATTLES.md](https://github.com/simonw/battledrones/blob/main/AGENT-BATTLES.md)**). Watch the battles so far replay in the game itself, or read them round by round, with
every order, note and radio line, in the [battle record viewer](https://simonw.github.io/battledrones/record-viewer.html):

| Battle | Map | Winner | | |
|---|---|---|---|---|
| GPT-6 Luna vs GPT-6 Luna | Riverlands | Blue at 4:31 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-11-riverlands-42-gpt-6-luna-vs-gpt-6-luna.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-11-riverlands-42-gpt-6-luna-vs-gpt-6-luna.json) |
| GPT-6 Luna (Blitz) vs GPT-6 Luna (Industry) | Dune Sea | Blue at 7:52 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-11-dune-sea-7-gpt-6-luna-vs-gpt-6-luna.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-11-dune-sea-7-gpt-6-luna-vs-gpt-6-luna.json) |
| GPT-6 Luna vs GPT-6 Astra | Riverlands | Red (Astra) at 7:50 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-11-riverlands-42-gpt-6-luna-vs-gpt-6-astra.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-11-riverlands-42-gpt-6-luna-vs-gpt-6-astra.json) |
| GPT-5.6 Sol vs GPT-6.1 Sol | Archipelago | Red (GPT-6.1 Sol) at 11:45 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-11-archipelago-42-gpt-5.6-sol-vs-gpt-6.1-sol.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-11-archipelago-42-gpt-5.6-sol-vs-gpt-6.1-sol.json) |
| GPT-6 Astra vs Gemini 4 Argon | Riverlands | Blue (Astra) at 5:35 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-14-riverlands-42-gpt-6-astra-vs-gemini-4-argon.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-14-riverlands-42-gpt-6-astra-vs-gemini-4-argon.json) |
| Claude Opus 5.5 vs Gemini 4 Argon | Archipelago | Blue (Opus) at 4:12 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-14-archipelago-42-claude-opus-5.5-vs-gemini-4-argon.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-14-archipelago-42-claude-opus-5.5-vs-gemini-4-argon.json) |
| Claude Opus 5.5 vs GPT-6 Astra | Archipelago (Goliath Armada) | Red (Astra) at 4:41 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-14-archipelago-42-claude-opus-5.5-vs-gpt-6-astra-2.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-14-archipelago-42-claude-opus-5.5-vs-gpt-6-astra-2.json) |
| Claude Opus 5.5 vs GPT-6 Astra | Frostbite | Red (Astra) at 4:14 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-14-frostbite-42-claude-opus-5.5-vs-gpt-6-astra.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-14-frostbite-42-claude-opus-5.5-vs-gpt-6-astra.json) |
| Claude Haiku 5.5 vs GPT-6 Luna | Frostbite | Blue (Haiku) at 7:48 | [▶ Watch the replay](https://simonw.github.io/battledrones/v11/?replay=battles/showcase/2026-10-14-frostbite-42-claude-haiku-5.5-vs-gpt-6-luna.json) | [Read the record](https://simonw.github.io/battledrones/record-viewer.html?replay=battles/showcase/2026-10-14-frostbite-42-claude-haiku-5.5-vs-gpt-6-luna.json) |

## Features

- **1v1 multiplayer**: [duel a friend online](#duel-a-friend-online) on
  any map, with any mutators. As an experiment, two phones on a table can
  also duel with no network at all. They talk through their speakers and
  microphones (🔊 Duel a friend (sound), SOUND-DUEL.md), but the link is a
  constant high-pitched noise that many people find unpleasant.
- **Pick an opener, play from second one**: every match starts on three
  cards — Blitz (Fab Plant + 3 Stingers), Industry (a third harvester +
  scrap) or Air Wing (Airpad + 3 Wasps) — and the AI picks its own.
- **Battlefield salvage**: destroyed vehicles and downed drones leave
  burning wrecks worth 30% of their cost — roll any ground unit over one
  to scoop up the scrap. Hold the field after a fight and it pays.
- **Fight for the middle**: capturable 📡 **Uplink relays** on every map
  pay scrap, light up the fog and charge your calldowns while you hold
  them, and from 1:30 a pair of 📦 **supply drops** parachutes in every
  75 s, announced to both sides 10 s ahead: first unit there takes it
  (scrap, Veterans, Field Repair, ⚡ charge, or a rare free Lancer).
- **Commander calldowns**: a meter that fills mostly from your losses pays
  for a Barrage, an EMP or a Drop Pod — tap the button, tap the map — and
  at 6:00 both sides get the **Sky Hammer** orbital strike. Every strike is
  telegraphed with a public warning circle: land yours, dodge theirs. The
  radio shouts "Incoming artillery!", the music swells on impact, and
  kill streaks, hero toasts and the after-action report name the strike.
- **16 units** across a real counter web: Stinger light tanks, Flak
  Crawlers, long-range Mortars, super-heavy Mastodons, water-crossing Lancer
  hover tanks, Scouts, Wasp strike drones, Raptor interceptors, Hornet
  bombers, Mender repair drones, Harvesters, three kinds of robot infantry
  squad (Troopers, Rocket Squads, Sniper Teams), the Condor dropship and the
  Goliath walking mech.
- **10 buildings** with a tech tree: HQ, Fab Plant, Airpad, Assembly Bay,
  Tech Lab, forward Depots, Turrets, SAM Sites, Radar and the Gantry.
- **Robot infantry**: every side starts with a Trooper Squad beside its HQ,
  and an Assembly Bay trains more: Troopers (cheap rifles that hit air too),
  Rocket Squads (Mastodon and Hornet killers) and, with a Tech Lab, Sniper
  Teams that stay hidden in woods until they fire. A squad is one unit of
  several robots that fall one by one as it takes damage, and it shoots
  weaker with each loss. Squads cross woods and mud at full speed, take half
  damage in woods and capture Uplinks twice as fast. Mastodons crush them.
- **The Condor dropship** flies two squads over water, rock and anything
  else. Select squads and tap the Condor to load them, then long-press the
  map to fly there and drop them, or tap ⇣ Unload (key U). If it's shot
  down over land its squads bail out hurt; over water or rock they go down
  with it.
- **The Goliath**: a giant walking mech, built at the top of the tech tree
  on a **Gantry** (it needs a Fab Plant, an Airpad, a Tech Lab and an
  Assembly Bay; one per side). Anchor it on open ground (⚓, key G) and it
  becomes a base on legs: harvesters unload at it, it trains robot infantry,
  and buildings go up within 3 tiles of it as **outposts**, however far from
  home. It fights with shoulder mortars, an eye laser, arm cannons and
  machine guns that hit aircraft too, and loses them one by one as it's
  hurt; only Menders repair it, and each weapon reboots as it's mended. The
  enemy always sees it (and the Gantry building it), two empty Condors can
  airlift it, each one costs 25% more for every Goliath you already have,
  and a side is beaten only when its HQ and every Goliath are gone. A dead
  one topples and scatters its scrap in piles across the battlefield.
- **6 maps in 5 biomes** — the classic Proving Grounds, Riverlands, Dune
  Sea, Frostbite, Ashlands and the big tropical **Archipelago** — with
  terrain that matters: roads, mud, woods (cover), fords, bridges,
  water/lava that only hover and air units cross, open sea that only
  aircraft cross, and rich crystal fields. On a phone the map row fades and
  shows a chevron where more maps wait off screen.
- **The Archipelago** (108×108, nearly four times Riverlands): every 📡
  Uplink sits on an island only robot infantry flown in by Condor can take
  — aircraft, the Condor and tanks count for nothing there — and an island
  Uplink pays only while your troops stand on it, so aircraft earn their
  keep killing garrisons. Two bridges join the HQs' landmasses, scrap is
  scarce, both sides start with a Condor and a squad aboard, and a side
  that loses its last Condor gets a free one flown in 45 s later. Tap an
  island with a loaded Condor selected to drop its troops. Two Condors can
  lift a Goliath onto an island, where it anchors and trains squads like
  anywhere else.
- Armor classes and damage types, dodgeable artillery shells and bombs,
  splash damage, veterancy, retaliation AI for idle units.
- An AI commander with **6 personalities** (Balanced, Rush, Air Swarm,
  Boom, Skyforce, Ironclad) and **3 difficulties**, playing by the same
  rules and fog of war as you — it gathers real waves, fights for the
  Uplinks, answers your infantry, flies Condor drops at your harvesters and
  calls down strikes, and rolls out Goliaths to dig in at distant fields
  and hunt yours — or watch two AIs fight, with a 🎥 **cinematic camera**
  (key C, on by default) that follows the action until you pan or zoom. Matches are tuned for
  comebacks: the side ahead at 4:00 now wins 70% of AI-vs-AI games, not
  90%, and a decided AI-vs-AI game runs a median of about 10½ minutes.
- **Veteran heroes**: units that rank up earn callsigns ("★★ Viper ·
  Lancer · 9 kills"), promotions pop over the unit, elites shimmer gold, and
  you hear about it when a named unit falls; the AI pulls its wounded
  veterans back too.
- **A cinematic HQ (or last Goliath) kill** (slow motion, camera glide,
  rolling blasts, white flash) and an **after-action report**: an
  army-strength timeline with first blood, the biggest battle and the
  turning point marked (and the first Goliath, or an HQ that fell while a
  Goliath fought on), your MVP unit, correct kill stats and one tip for
  next time.
- **Last Stand** survival mode: hold your base against endless, announced
  waves — Air Raids, Armour Columns, Artillery, Mixed Assaults and robot
  Bot Swarms, four of them in each block of five and then a Boss — from
  shifting map edges. Call waves early for bonus scrap; your best per map
  and difficulty is saved.
- **A Commander career**: XP and ten ranks from Cadet to Marshal, 17
  medals (Lightning War, Comeback, Ace, Giant Slayer, Goliath Slayer,
  Orbital, Scavenger, Steady Hands…) popping in on the end
  screen, three stars per map and difficulty, and a **Daily Op** — one seeded
  match a day, the same for everyone, with a win streak.
- **Twelve mutators** to twist a skirmish for both sides: Blitz, Gold Rush,
  Glass Cannons, Rapid Fab, Air War, Infantry War (robot infantry only),
  Airborne (start with a Condor and one of each squad), Veterans, Clear
  Skies, Nomads 🦿 (each side starts with an anchored Goliath instead of a
  base), Robot Love 💘 (two enemy Goliaths that meet fall in love, and
  the battle ends in a draw) and Goliath Armada 🚁 (each side starts with
  nothing but four Goliaths in the air, two Condors carrying each).
- **Ops**: a campaign of eight short missions with a twist and three stars
  each — hold the Riverlands bridge against a Rush, deliver 10,000 scrap under
  Air Swarm raids, decapitate a base with a fixed strike group, win on a
  frozen 3,000-scrap budget, raid with aircraft only, survive Ironclad on Hard,
  and a 10-wave Last Light. A goal pill with live stars, a briefing sheet,
  "Next op" on the end screen; ops unlock as you clear them.
- **A 3D battlefield in three.js.** Every unit, building and map objective
  is a procedural low-poly 3D model in the painted style (gunmetal hulls,
  royal-blue or crimson team panels, amber lights): turrets track their
  targets and kick on recoil, rotors spin, aircraft fly at altitude, bank
  into turns and cast shadows on the ground, tanks tilt over the terrain,
  buildings rise out of the ground when placed and smoke when hurt. Robot
  squads run with their feet planted (no sliding), raise their guns to
  fire and topple one robot at a time; the Condor hovers low, drops its
  ramp and lets its squads jump down from a troop bay you can see into; the
  Goliath strides on planted feet, digs in on hydraulics and stabiliser
  spikes, and topples when it dies, and the Gantry builds it in stages you
  can watch. Turn and zoom every model, beside its card and with its
  animations, on the [3D models page](https://simonw.github.io/battledrones/models.html).
  The landscape is a heightfield draped with each map's painted terrain — rock
  outcrops rise into mesas whose cliffs and crags are textured with the
  painted stone of their biome, rivers and lava cut real channels under
  animated water, drifting ice floes or crusted, glowing lava, fords dip
  under a shallow skin of water, bridges are decks laid along each
  crossing, and the land carries on past the map's edge — with instanced
  trees per biome, salvage heaps and glowing crystal clusters that shrink
  as they're mined, real-time sun shadows, drifting cloud shadows, layered
  GPU explosions and smoke, and a fog of war that drapes unexplored ground
  in a drifting shroud. A tilted RTS camera steepens as you zoom out;
  resolution adapts to keep weaker phones smooth. Terrain, menu art and
  icons were painted with OpenAI's `gpt-image-2.5-sunburst`; every sound
  is synthesised live.
- An **adaptive soundtrack** synthesised live: each biome has its own mode,
  chords and instruments; bass, drums and an arpeggio join as fights heat up
  near your camera, an alarm motif plays when your base is under attack,
  and matches end on a fanfare, a lament or (a Robot Love draw) a sweet
  sting. Quiet biome ambience (wind,
  birds, desert hiss, lava rumble) fills the lulls; Music / Effects / Voice
  toggles live in the pause menu.
- Punchy, readable fights: hit flashes, damage-trail health bars, team
  rings under units in combat, kill and loss cues that sound different,
  on-screen-only camera shake, and gold "+100" pops with a rising coin
  chime when your harvesters deliver.
- **Voices and a radio announcer.** Every unit class answers in its own
  synthesized robot voice when selected, ordered, built or promoted. Mastodons
  growl, Wasps buzz, Menders ring and Troopers chatter. A radio commander
  calls out what matters: "Warning: our HQ is under attack", "Enemy
  aircraft detected", "Enemy troops landing!", "Enemy Goliath in
  production", "Squad lost", "Construction complete". Kill streaks get
  banners: First blood, Double kill, Triple kill, Rampage, Mastodon down,
  Goliath down. Spectators get a neutral caster.
- **Battle awareness and game speed.** Pulsing arrows at the screen edge
  point at off-screen fights (red when you're hit, amber when you attack);
  tap one, or ⚡, to glide there. "Enemy drones inbound — Flak, Raptors or a
  Turret" warns before a raid lands, a tug-of-war meter shows who is
  winning the fight on screen, and alerts sit in a slim ticker instead of
  over the battlefield. Play at 1×, 1.5× or 2× (4× when watching), or hold
  the clock to fast-forward — the game drops back to 1× by itself when an
  enemy strike, a raid or an attack on your HQ (or, once it has fallen, on
  a Goliath) needs your hands. First-time
  tips arrive one at a time, never over a banner.
- **Thumb-friendly command.** Three squad chips: hold to save a group, tap
  to select it, double-tap to fly there; each shows its unit, count and
  health and flashes red when hit (keys 1–3). Build buttons glow with ⚔
  when they counter enemies you've seen ("Counters Wasps (seen ×4)"), tabs
  flag an idle factory, and building placement on a phone puts the ghost
  on a good spot for you: tap or drag to move it, tap it to build, and a
  bad spot tells you why.

## Development

```bash
npm install
npm run dev            # Vite dev server
npx vite --config tools/vite-https.config.ts   # the same over HTTPS, for a sound duel on phones (SOUND-DUEL.md)
npm test               # Vitest suite for the simulation layer
npm run build          # typecheck + production build into dist/
npm run smoke          # headless Playwright test of the real touch flow (against dist/)
npm run smoke -- --side=red   # the same flow playing red against a blue AI (SOUND-DUEL.md)
npm run build:pages    # build current game + all version tags into _site/
npm run balance duels  # cost-equal unit duel matrix
npm run balance matches [map]   # AI-vs-AI round robin (openers + objectives; --classic / --no-objectives),
                       # with the Goliath numbers (--no-goliath bans it, for an A/B run)
npm run balance goliath [--menders N]   # a Goliath (plus N Menders) vs cost-equal groups of every unit
                       # (any mode takes --tune '{"UNITS.trooper.hp":200}' for an A/B run)
npx vite-node tools/survival.ts [ai|human|both] [map|all] [easy|normal|hard|all] [seeds] [--calldowns]
                       # Last Stand: waves survived by an AI / scripted-player defender, and scrap
                       # lost per wave by theme and stage (--tune '{"themes":["swarm",…]}': one theme only)
npx vite-node tools/ops.ts [op|all] [seeds]
                       # Ops: can the stand-in pilots clear each op, and with how many stars
npx vite-node tools/beginner.ts [novice|beginner|decent] [easy|normal|hard] [seeds]
                       # difficulty on-ramp: a scripted phone player vs the AI on every map
npx vite-node tools/pacing.ts run out.jsonl --seeds 8 --shard 0/4   # pacing & snowball panel (shard across processes)
npx vite-node tools/pacing.ts summary out*.jsonl                    # …the table in DESIGN.md "Balance & pacing"
npx vite-node tools/pacing.ts run out.jsonl --seeds 8 --mirror      # side fairness: each personality vs itself
npx vite-node tools/pacing.ts run out.jsonl --with rush --tune '{…}' # one personality's pairings, A/B
npm run maps           # export map grids to art/maps/*.json (--ascii to preview)
                       # model gallery: npm run dev, then open /tools/models.html
                       #   (?only=units|buildings|condor|condor-ring|goliath|gantry, ?anim=walk|idle|aim|fall for
                       #   the robots, ?icon=<kind> for one model alone, as shot for its HUD portrait)
node tools/model-portraits.mjs --all  # reshoot every HUD portrait from the 3D models, blue and red (ICONS.md)
                       # vehicles reference page: /vehicles.html (built into dist/ too)
                       # 3D models page: /models.html (built into dist/ too): every unit's model to turn
                       #   and zoom, beside its card, with its animations to play
                       # battle record viewer: /record-viewer.html[?replay=<record>] (built into dist/ too,
                       #   with battles/showcase/; the game takes ?replay=<record> as well)
                       # radio probe: /radio-probe.html (built into dist/ too) measures a phone-to-phone
                       #   sound link, for multiplayer over audio (reports/Audio modem for lockstep multiplayer.md)
node tools/online-smoke.mjs  # two pages play an online duel through the deployed relay (against dist/,
                       #   served as simonw.github.io, the only origin the relay accepts; --shots)
cd relay && uv run pytest    # the relay's tests (relay/README.md: running and deploying it)
node tools/shots.mjs   # screenshot tour against the dev server (SPECTATE=1, MAP=...)
node tools/showcase.mjs  # staged close-up skirmish for checking weapon effects
```

Agent battles (**AGENT-BATTLES.md**): AI models play each other through
tools that show only what their side can see, in 5-second rounds.

```bash
llm install -e llm-tools-battledrones   # the LLM plugin (llm: uv tool install llm)
llm battledrones run --blue gpt-6-luna --red gpt-6-luna --map riverlands --seed 42
npm run arena run -- --blue scripted --red ai:rush:hard    # built-in seats, no model
npm run arena serve -- --blue seat --red ai:balanced:easy  # seat URLs for any agent (HTTP or MCP)
npm run arena replay battles/<file>.json                   # re-run a record, check its hash trail
npm run arena upgrade battles/<file>.json                  # bring a record from older sim code up to this one
npm run arena pin -- --version v11 battles/<file>.json     # replays exactly on this sim? pin it to that version tag
npm run arena watch battles/<file>.json                    # the 3D viewer on the dev server (&follow: live)
                                                           # (any build: /?replay=<record>, or /record-viewer.html?replay=<record>)
npm run arena stats -- battles/*.json --detail             # results by model, side, map, opener
```

GitHub Pages is published by `.github/workflows/pages.yml` on pushes to `main`, newly published releases (including prereleases), and manual runs. It builds the latest `main` at <https://simonw.github.io/battledrones/> and every `v`-prefixed version tag (`v1`, `v2`, …, or semver tags such as `v9.1.0`) at its own path, such as <https://simonw.github.io/battledrones/v1/>. Every deployment contains all versions, so updating the current game preserves the archive. Tags should remain fixed once published.

Each historical build includes a downloadable ZIP, such as <https://simonw.github.io/battledrones/v3/v3.zip>. Later deployments first try to download and reuse that ZIP, checking its integrity and recorded tag, commit, URL path, and archive format. Missing, invalid, or outdated archives fall back to a build from the tag's own source and lockfile, then publish a new ZIP. The current game always builds from source. Set `PAGES_CACHE_URL=` to force all historical builds, or set it to another site root to test cache reuse locally.

Pull requests build the complete site without deploying. The Pages workflow only builds and publishes; the separate Tests workflow runs the unit tests. To build the site locally, run `git fetch --tags`, `npm ci`, and `npm run build:pages`. Generated `dist/` and `_site/` output is ignored; there is no need to commit a built `docs/` folder.

The repository's **Settings → Pages → Build and deployment → Source** must be **GitHub Actions**. Release events dispatch the workflow on `main`, so the `github-pages` environment can remain restricted to that branch. To republish after tagging a historical commit that predates the workflow, run **Publish Pages** manually on `main`.

Art pipeline (Python 3 + Pillow/numpy/scipy, `OPENAI_API_KEY` for
generation) — see **ART.md**:

```bash
npm run art:generate   # call the OpenAI Images API for any missing raw art
npm run art:process    # raw art → sprite atlas, key art, PWA icons
npm run art:terrain    # paint every map's terrain from its grid (then refreshes the rock textures)
npm run art:textures   # just the biome rock textures the 3D cliffs and crags use
```

- **`DESIGN.md`** — the game design: roster, terrain, combat model, AI,
  controls spec, architecture.
- **`ART.md`** — how every image was generated and processed, and the
  asset contracts the engine relies on.
- **`AGENT-BATTLES.md`** — AI models playing each other: the arena, its
  tools, battle records, the LLM plugin and the viewer.
- **`GOLIATH.md`** — the Goliath and Gantry spec, with how the shipped
  game differs from it.
- **`ICONS.md`** — the HUD portraits: why they're shots of the 3D models,
  and how they're framed and finished.
- **`relay/README.md`** — the online duel's WebSocket relay: its protocol,
  and how to run and deploy it to Fly.

## Architecture

- `src/sim/` — the deterministic game simulation: pure TypeScript, no
  engine imports, fixed 10 Hz tick, command-queue input. All tunable
  numbers live in `src/sim/balance.ts`; maps in `src/sim/maps.ts`. The AI
  commander (`src/sim/ai/commander.ts`) plays by the same rules and fog as
  the player. Fully unit-tested.
- `src/game/` — three.js rendering and input: the 3D engine in `three/`
  (stage and adaptive resolution, RTS camera rig, procedural models,
  heightfield terrain, fog-of-war shader patch, instanced particles, ground
  marks, screen overlay), the interpolated view of the sim (`render/`),
  gesture recognizer (`gestures.ts`, engine-free and tested), procedural
  audio (`audio.ts`).
- `src/ui/` — DOM-overlay HUD and menu, with portrait/landscape layouts in
  CSS.
- `src/arena/` — agent battles: each side's view of the world as text, its
  orders, the round loop and battle records. Reads the sim and changes
  nothing in it; only the dev-only battle viewer loads it in the browser.
  `tools/arena.ts` runs it, `llm-tools-battledrones/` lets LLM's models play.
- `art/` — the image-generation and processing pipeline; `tools/` — map
  export, balance harness, smoke test and screenshot tour.
