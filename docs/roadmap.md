# Merge Quest roadmap

Build a level mode on the existing engine first, with small boards that grow from 2×2 to 5×7 and teach one idea at a time. Add a light story layer only once the levels are fun. The full research and plan live in the "Merge Blaster Roadmap" doc.

| Phase | What | Gate to move on |
| --- | --- | --- |
| Now | Endless quick wins: bag randomiser, ∞ pays coins, two-tile preview, free rescue *(done)* | none |
| 1 | **Level mode MVP** *(built, now in playtesting)*: variable board size, 24 teaching levels, goals + shot limits + 1–3 stars, level map, free helper samples | Bot wins levels 1–6 every time; a new player finishes 1–12 without help |
| 2 | **Rewards** *(built)*: win-streak ladder (3 wins → free Hammer, 5 → + free Swap; a loss costs 2 steps), chests on levels 10 and 20 (coins + banked helpers), one-time bounties for the first 2048 / 4K / 4M / ∞, and a home screen to pick a mode | Players replay levels for 3 stars |
| 3 | **Variety** *(built, now in playtesting)*: World 2 "Stone Quarry" (levels 25–36) with stone blockers, a seeded daily challenge, and 4 tile/board skins as coin sinks | New worlds still feel fresh |
| 3b | **World 3: Frost Peaks** *(built, now in playtesting)*: levels 37–48 with frozen blocks (merge beside one to thaw it into a normal block), snowfall, ice + stones together, a free Heater booster sample on level 42, a Frost skin and a "thaw 50 blocks" milestone. Hard: 42; Super Hard: 47 | Tutorial levels 37–38 always won; finale about 50% for the bot |
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
