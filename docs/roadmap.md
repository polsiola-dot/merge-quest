# Merge Quest roadmap

Build a level mode on the existing engine first, with small boards that grow from 2×2 to 5×7 and teach one idea at a time. Add a light story layer only once the levels are fun. The full research and plan live in the "Merge Blaster Roadmap" doc.

| Phase | What | Gate to move on |
| --- | --- | --- |
| Now | Endless quick wins: bag randomiser, ∞ pays coins, two-tile preview, free rescue *(done)* | none |
| Now | **Endless sliding pool** *(done)*: 6 block types that slide up instead of jumping a tier at 4K. At 4K the 2s and 4s retire, then 2 more types per doubling (never closer than 64x below the biggest block); a type retires only once none of its blocks remain; nothing launched exceeds the biggest block. Bot from a 4K board: ~650 shots survived vs ~90 before, typical score 1.4M vs 419K | Runs past 4K feel like a steady climb |
| 1 | **Level mode MVP** *(built, now in playtesting)*: variable board size, 24 teaching levels, goals + shot limits + 1–3 stars, level map, free helper samples | Bot wins levels 1–6 every time; a new player finishes 1–12 without help |
| 2 | **Rewards** *(built)*: win-streak ladder (3 wins → free Hammer, 5 → + free Swap; a loss costs 2 steps), chests on levels 10 and 20 (coins + banked helpers), one-time bounties for the first 2048 / 4K / 4M / ∞, and a home screen to pick a mode | Players replay levels for 3 stars |
| 3 | **Variety** *(built, now in playtesting)*: World 2 "Stone Quarry" (levels 25–36) with stone blockers, a seeded daily challenge, and 4 tile/board skins as coin sinks | New worlds still feel fresh |
| 3b | **World 3: Frost Peaks** *(built, now in playtesting)*: levels 37–48 with frozen blocks (merge beside one to thaw it into a normal block), snowfall, ice + stones together, a free Heater booster sample on level 42, a Frost skin and a "thaw 50 blocks" milestone. Hard: 42; Super Hard: 47 | Tutorial levels 37–38 always won; finale about 50% for the bot |
| 3c | **Audio** *(home music and placeholder SFX done, see below)*: home-screen music loop with Music/Sound toggles in Settings *(done)*, then a gameplay ambient loop and sound effects | Sound never covers up the next move; muting persists |
| 4 | Story: spend stars to restore an illustrated scene, one caption at a time | none |
| 6 | **Quest Log: lifetime challenges** *(planned, see below)*: a growing list of long-term challenges with an overall % bar, rewards at completion milestones and hidden challenges that reveal themselves | Players check the Quest Log between levels |
| 5 | **Store release (final polish)**: swap in the real art, monetisation, Android and iOS builds, store listings | Closed testing passes; both stores approve |

## Economy and difficulty (v2, from the coin research)

- **Earn less:** a first clear pays 30 coins (×2 🔥 Hard, ×3 💀 Super Hard, 150 for a world finale) plus 2 per shot left; combo coins halved. Chests, milestones and ∞ stay as rare celebrations. A full run of the 36 levels earns about 5,000 coins, down from about 12,000.
- **Spend more, mostly on progress** (the big games' main sinks): +5 shots when out of shots (300, then 600, 900… in the same attempt; a continued win scores 1 star), pre-level boosters (+3 Shots 150, 🌈 Wild Tile 300, Hammer 250), and stock bought ahead in the Shop.
- **Cosmetics as the long-term sink:** 6 board skins, Tile Buddies faces, 4 merge effects, 4 shot trails (about 12,600 coins in all).
- **Bot balance check (25 Nov, after group merges and economy v2):** all 48 levels plus 28 days of dailies, no errors. Tutorials 1–6, 25, 37–38 always won. Retuned outliers: 15 Hard (70% → ~47%: survive 40 shots, tiles up to 128), 35 Super Hard (7% → ~25%: 35 shots), 36 Quarry finale (100% → ~33%: now 110 shots), 40–41 (90–97% → ~65%: fewer shots), 42 Hard (67% → ~52%: 5 shots), 44–46 (83–100% → ~35–65%), 47 Super Hard (7% → ~17–33%: snow every 6). 43 stays an easy breather (~93%). Daily goals average 38–73%.
- **Difficulty tiers:** normal levels carry no label. 🔥 Hard (red-orange) and 💀 Super Hard (purple, skull) are flagged on the map, the start screen, the board frame and the goal bar. Current tiers: Hard 15, 30, 34, 42; Super Hard 20, 35, 47. Assign from bot win rates (Super Hard ≈ under 25%).

## Design rules from the research

- One new idea per level; levels 1–6 use a fixed tile queue and can't be lost.
- Limit shots, not time. Difficulty is a sawtooth: a Hard level about every 10, then an easy one.
- 2×2 only works with scripted tiles; random tiles start at 3×3. "Clear all blocks" is impossible, so use "leave ≤ N blocks".
- Each helper is introduced with free uses before it costs coins.
- Never: lives or energy timers, piggy banks, loot boxes, streaks that reset to zero, guilt notifications.

## Audio plan

**Done:** `music/home.mp3` ("Sunny Kingdom Walk", 59 s, 128 kbps). The end is crossfaded into the start so the loop has no seam. It plays through Web Audio, starting on the first tap (browsers block sound before one), fades in on the home screen and level map, fades out when a game starts, and pauses when the app is in the background. Settings has **Music** and **Sound** on/off toggles, saved in `mergeQuest.audio.v1`. The service worker caches the file for offline play.

**Next music:** a calm, sparse ambient gameplay loop (prompt already written) at about 40–50% of the home volume, crossfading from the home theme when a level starts. World variants for Stone Quarry and Frost Peaks can follow later.

### Sound effects: approach
- **One mixer.** Music and SFX each get their own gain node into a master gain, so each toggle is independent. Effects briefly duck the music by about 30% for big moments only (win, chest, 1024+).
- **Short files, preloaded.** All effects are decoded once into memory after the first tap. Target 0.1–1.5 s each, mono OGG/MP3 at 96 kbps, about 300 KB in total. A tiny synthesised fallback (oscillator blips) covers each sound until its file exists, so the plan can be built and tuned now and the real sounds dropped in later with no code changes.
- **Pitch tells the story.** Merge sounds rise in pitch with the tile value and with each step of a chain combo (about +2 semitones per step, capped), so players can *hear* a good move. Each play gets a little random pitch (±3%) so repeats never sound robotic.
- **Limits.** At most 2 copies of the same sound at once and at most 6 voices in total; very quiet sounds are skipped while a big one plays.
- **Haptics (in the app builds).** Light tap on fire, medium on merge, success pattern on win, through Capacitor Haptics in Phase 5. Linked to the Sound toggle, with its own toggle later if players ask.

### Sound list (priority order)
| # | Moment | Sound idea | Notes |
| --- | --- | --- | --- |
| 1 | **Fire / tile lands** | soft wooden "tok" or plop | Plays most often, so keep it the quietest and shortest |
| 2 | **Merge** | bright pop + marimba note | Pitch rises with tile value |
| 3 | **Chain combo** | same pop, stepping up a scale | Each extra step in a chain climbs higher; 4+ adds a sparkle |
| 4 | **Group merge (3+ blocks)** | chord stab instead of a single note | Bigger group → fuller chord |
| 5 | **Big tile (1024, 2048, K/M)** | short fanfare + shimmer | Ducks the music |
| 6 | **Level won** | 2–3 s jingle (horn + glockenspiel, same key as the home theme) | Stars pop in one by one with rising "ding"s |
| 7 | **Level lost / out of shots** | gentle descending "womp" on pizzicato | Sad but friendly, never harsh |
| 8 | **Coins earned / coin fly-in** | coin clinks, one per flying coin, capped | Satisfying payoff; matches the coin animation |
| 9 | **Button tap / menu** | very soft click | Used everywhere in the UI |
| 10 | **Open card / close (✕)** | soft whoosh in, softer whoosh out | Also the goal card |
| 11 | **Stone crack / break** | rock crack, then crumble | Stone Quarry |
| 12 | **Ice thaw** | crystalline crack + drip | Frost Peaks; snowfall gets a soft "whump" |
| 13 | **Boosters** | Hammer: thunk; Swap: whoosh; Undo: rewind blip; Wild Tile: magic sparkle; Heater: warm sizzle | Locked helper tap: dull "bonk" |
| 14 | **Shop purchase** | cash-register "ka-ching" | Equip a cosmetic: soft sparkle |
| 15 | **Chest open / daily reward** | lid creak + treasure shimmer | Ducks the music |
| 16 | **Milestone / streak reward** | short rising arpeggio | Streak broken: no sound (don't rub it in) |
| 17 | **Low shots warning (≤3 left)** | soft heartbeat tick per shot | Builds tension without stress |

### Build order
1. *(done)* Mixer + `sfx.play(name, {v, group, step})` with synthesised placeholders, wired to sounds 1–9: land, merge (pitch follows the tile value and climbs with each chain step; 3+ block groups play a chord with climbing "gulps"; 4+ chains add a sparkle), big tile fanfare, win jingle, lose "womp", coin clinks and button taps. Big moments duck the music. Real sounds drop into `sfx/` and are listed in `sfx/index.json` (`{"merge": "merge.mp3"}`), replacing the synth with no code change. Next: balance volumes on a phone.
2. Generate the real sounds (ElevenLabs Sound Effects, or a free CC0 pack), trim, normalise to about −16 LUFS, and drop them into `sfx/`.
3. Sounds 10–17, plus the gameplay ambient loop.
4. Phase 5: haptics and a volume slider.

## Phase 5: store release

Target: first release next month. The game stays fully playable offline and in the browser; the stores are an extra.

**Scope for 1.0:** Phases 1 and 2 plus the trimmed parts of 3 (one blocker world, coin sinks). The story layer (Phase 4) ships later as an update, so it doesn't delay the release.

**Art:** prompts are in [art-prompts.md](art-prompts.md). The code placeholders stay until the images exist; swapping them in is a small change.

**Monetisation (decided direction, still to confirm):**
- Optional rewarded ads only: watch a clip for extra coins or a helper. Never forced, never between levels.
- A one-time "Remove ads / supporter" purchase and fixed coin packs. Contents are shown up front, nothing random.
- Still no lives or energy, no countdown timers, no loot boxes, no guilt notifications. Coins stay earnable in play.

**Steps**
1. Accounts: Google Play Console (one-off $25) and Apple Developer Program ($99 a year). Start both early, because verification takes days.
2. Wrap the web app with Capacitor for Android and iOS; keep the browser version too.
3. Ads and purchases: AdMob for rewarded ads, Play Billing and Apple in-app purchase through a Capacitor plugin. Ad consent prompt for the EU/UK, and ad/analytics settings that suit the age rating.
4. Compliance: privacy policy page (hosted on GitHub Pages), Data safety form (Google), App Privacy answers (Apple), age rating questionnaires, support email.
5. Store listings: icon, feature graphic, 4-8 screenshots, short and full description, keywords.
6. Testing: Google requires a closed test (new personal accounts: around 12 testers for 14 days; check the current rule) before production access. Apple TestFlight for iOS. Plan to start this at the beginning of December for a late-December release.
7. Review: Apple usually takes 1-3 days and may reject a plain wrapped website, so make sure the app works offline, has its own icon and splash screen, and feels native (haptics, no browser chrome).
8. Launch checklist: crash-free run on real iPhone, Android phone and tablet; restore-purchases button; save data survives updates.

## Phase 6 (planned): Quest Log, lifetime challenges

A home-screen **Quest Log** for long-term goals that build up over all of play. It replaces and absorbs today's Milestones screen.

**What the player sees**
- An **overall completion bar** at the top: "Quest Log 37%". Hidden challenges count toward the total, so 100% really means everything.
- Challenges grouped by theme, each with its **own progress bar** (e.g. "Thaw frozen blocks: 132 / 250").
- **Hidden challenges** show as "❓ Hidden challenge" (optionally with a vague hint) and reveal themselves when a related challenge is done, a new world opens, or the player stumbles on them.
- A red dot on the home-screen button when a challenge is completed and its reward hasn't been collected.

**Themes (first set)**
- *Merging:* total merges; a 5-block merge; combos of 5 / 8 / 10.
- *Blocks:* first 2048 / 4K / 4M / ∞ (today's milestones move here).
- *Levels:* stars earned; each world cleared; all 3 stars in a world; Hard and Super Hard levels cleared.
- *Worlds:* stones broken; blocks thawed (today's "thaw 50" moves here); one set per new world (e.g. Honey Hive: honey stopped).
- *Endless:* score 10K / 100K / 1M; ∞ blocks made.
- *Daily:* dailies won (no streaks; a missed day never resets anything).
- *Collection:* skins and style items owned.
- *Hidden examples:* win a Super Hard level without boosters; win with exactly 0 shots left; thaw 3 blocks with one merge; make a 10-merge combo.

**Tiers and rewards**
- Many challenges have bronze / silver / gold steps (e.g. thaw 50 / 250 / 1,000), each paying a few coins.
- A **reward track** on the overall count: every 5 challenges completed opens a chest (coins plus a booster); 25 / 50 / 75 / 100% unlock exclusive cosmetics (a skin, a shot trail, a merge effect, a gold "Quest Master" frame) that can't be bought.
- Rewards are collected with a tap (the reveal moment), never auto-expire.

**How it grows**
- Each new world adds its own challenges (some hidden). The overall % is "completed / all challenges in the game so far", so a big update can lower it; show a "🆕 New challenges" badge so that reads as more to do, not lost progress.
- Lifetime counters (merges, thaws, stones, stars …) are stored locally from the start, so challenges added later can count past play.

**Rules (same as the design rules):** no time limits, nothing expires or resets, no paid shortcuts to complete a challenge.

**Open questions for later:** per-world % as well as overall; whether coins from challenges count toward the coin economy targets (keep them small, the cosmetics are the real reward).
