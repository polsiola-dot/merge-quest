# Merge Quest roadmap

Build a level mode on the existing engine first, with small boards that grow from 2×2 to 5×7 and teach one idea at a time. Add a light story layer only once the levels are fun. The full research and plan live in the "Merge Blaster Roadmap" doc.

| Phase | What | Gate to move on |
| --- | --- | --- |
| Now | Endless quick wins: bag randomiser, ∞ pays coins, two-tile preview, free rescue *(done)* | none |
| 1 | **Level mode MVP** *(built, now in playtesting)*: variable board size, 24 teaching levels, goals + shot limits + 1–3 stars, level map, free helper samples | Bot wins levels 1–6 every time; a new player finishes 1–12 without help |
| 2 | **Rewards** *(built)*: win-streak ladder (3 wins → free Hammer, 5 → + free Swap; a loss costs 2 steps), chests on levels 10 and 20 (coins + banked helpers), one-time bounties for the first 2048 / 4K / 4M / ∞, and a home screen to pick a mode | Players replay levels for 3 stars |
| 3 | **Variety** *(built, now in playtesting)*: World 2 "Stone Quarry" (levels 25–36) with stone blockers, a seeded daily challenge, and 4 tile/board skins as coin sinks | New worlds still feel fresh |
| 4 | Story: spend stars to restore an illustrated scene, one caption at a time | none |
| 5 | **Store release (final polish)**: swap in the real art, monetisation, Android and iOS builds, store listings | Closed testing passes; both stores approve |

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
